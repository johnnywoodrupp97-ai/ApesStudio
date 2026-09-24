#include "ExoHollowAI.h"
#include "ExoHollow.h"
#include "ExoBlock.h"
#include "ExoTypes.h"
#include "ExoNoiseSubsystem.h"
#include "ExoGameMode.h"
#include "NavigationSystem.h"
#include "Navigation/PathFollowingComponent.h"
#include "Kismet/GameplayStatics.h"
#include "Engine/World.h"
#include "EngineUtils.h"

AExoHollowAI::AExoHollowAI()
{
	PrimaryActorTick.bCanEverTick = true;
}

void AExoHollowAI::OnPossess(APawn* InPawn)
{
	Super::OnPossess(InPawn);
	Home = InPawn->GetActorLocation();
	WanderClock = FMath::FRandRange(0.f, 6.f);
	if (const AExoHollow* H = Cast<AExoHollow>(InPawn))
	{
		if (H->bHorde) State = EExoHollowState::Siege;
	}
}

void AExoHollowAI::Alert(const FVector& Where)
{
	if (State != EExoHollowState::Chase)
	{
		State = EExoHollowState::Investigate;
		Goal = Where;
		MoveToLocation(Goal, 100.f);
	}
}

bool AExoHollowAI::CanSeePlayer(APawn*& OutPlayer) const
{
	APawn* Me = GetPawn();
	APawn* Player = UGameplayStatics::GetPlayerPawn(this, 0);
	if (!Me || !Player) return false;
	const FVector To = Player->GetActorLocation() - Me->GetActorLocation();
	if (To.Size() > ExoTuning::HollowSightCm) return false;
	// A 110 degree cone; Crawlers and close targets (< 3 m) are felt all around.
	if (To.Size() > 300.f && FVector::DotProduct(Me->GetActorForwardVector(), To.GetSafeNormal()) < FMath::Cos(FMath::DegreesToRadians(55.f))) return false;
	if (!LineOfSightTo(Player)) return false;
	OutPlayer = Player;
	return true;
}

AExoBlock* AExoHollowAI::FindBlockingBlock() const
{
	APawn* Me = GetPawn();
	if (!Me) return nullptr;
	AExoBlock* Best = nullptr;
	float BestDist = 400.f;
	for (TActorIterator<AExoBlock> It(GetWorld()); It; ++It)
	{
		if (It->bGhost) continue;
		const float D = FVector::Dist(It->GetActorLocation(), Me->GetActorLocation());
		if (D < BestDist) { BestDist = D; Best = *It; }
	}
	return Best;
}

void AExoHollowAI::Think()
{
	AExoHollow* Me = Cast<AExoHollow>(GetPawn());
	if (!Me || Me->IsDead()) return;

	APawn* Seen = nullptr;
	if (CanSeePlayer(Seen))
	{
		State = EExoHollowState::Chase;
		Target = Seen;
		LoseSightTime = 0.f;
	}
	else if (State != EExoHollowState::Chase && State != EExoHollowState::Siege)
	{
		if (const UExoNoiseSubsystem* Noise = GetWorld()->GetSubsystem<UExoNoiseSubsystem>())
		{
			FExoNoise Heard;
			const bool bHeard = Noise->FindAudibleNoise(Me->GetActorLocation(), 5.f, Heard);
			const AActor* Source = Heard.Instigator.Get();
			// Hollows ignore each other's moans; anything else (footsteps, welding, alarms) draws them.
			if (bHeard && !(Source && Source->IsA<AExoHollow>()))
			{
				State = EExoHollowState::Investigate;
				Goal = Heard.Location;
				MoveToLocation(Goal, 100.f);
			}
		}
	}

	switch (State)
	{
	case EExoHollowState::Chase:
	{
		AActor* T = Target.Get();
		if (!T) { State = EExoHollowState::Wander; break; }
		if (!Seen)
		{
			LoseSightTime += 0.25f;
			if (LoseSightTime > 6.f) { State = EExoHollowState::Investigate; Goal = T->GetActorLocation(); break; }
		}
		if (!Me->TryAttack(T))
		{
			MoveToActor(T, 90.f);
		}
		break;
	}
	case EExoHollowState::Siege:
	{
		// Horde: go for the player, pounding through any block in the way.
		APawn* Player = UGameplayStatics::GetPlayerPawn(this, 0);
		if (Player && !Me->TryAttack(Player)) MoveToActor(Player, 90.f);
		break;
	}
	case EExoHollowState::Investigate:
		if (FVector::Dist2D(Me->GetActorLocation(), Goal) < 200.f || GetMoveStatus() == EPathFollowingStatus::Idle)
		{
			State = EExoHollowState::Wander;
			WanderClock = FMath::FRandRange(3.f, 8.f);
		}
		break;
	default:
		WanderClock -= 0.25f;
		if (WanderClock <= 0.f)
		{
			WanderClock = FMath::FRandRange(8.f, 15.f);
			if (UNavigationSystemV1* Nav = FNavigationSystem::GetCurrent<UNavigationSystemV1>(GetWorld()))
			{
				FNavLocation Out;
				if (Nav->GetRandomReachablePointInRadius(Home, 1000.f, Out)) MoveToLocation(Out.Location, 50.f);
			}
		}
		break;
	}

	// Stuck while chasing or sieging: a block is in the way, so pound it (Brutes do this on purpose).
	if ((State == EExoHollowState::Chase || State == EExoHollowState::Siege) && Me->GetVelocity().Size2D() < 20.f)
	{
		StuckTime += 0.25f;
		if (StuckTime > 1.5f)
		{
			if (AExoBlock* Block = FindBlockingBlock())
			{
				StopMovement();
				Me->TryAttack(Block);
			}
		}
	}
	else
	{
		StuckTime = 0.f;
	}
}

void AExoHollowAI::Tick(float DeltaSeconds)
{
	Super::Tick(DeltaSeconds);
	ThinkClock += DeltaSeconds;
	if (ThinkClock >= 0.25f)
	{
		ThinkClock = 0.f;
		Think();
	}
}
