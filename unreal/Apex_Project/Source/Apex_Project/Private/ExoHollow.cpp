#include "ExoHollow.h"
#include "ExoHollowAI.h"
#include "ExoBlock.h"
#include "ExoPlayerCharacter.h"
#include "ExoVitalsComponent.h"
#include "ExoMissionSubsystem.h"
#include "ExoNoiseSubsystem.h"
#include "Components/CapsuleComponent.h"
#include "Components/SkeletalMeshComponent.h"
#include "Components/StaticMeshComponent.h"
#include "Engine/DamageEvents.h"
#include "Engine/SkeletalMesh.h"
#include "Engine/StaticMesh.h"
#include "Engine/World.h"
#include "GameFramework/CharacterMovementComponent.h"
#include "Kismet/GameplayStatics.h"
#include "Misc/Paths.h"
#include "UObject/ConstructorHelpers.h"

AExoHollow::AExoHollow()
{
	PrimaryActorTick.bCanEverTick = true;
	AIControllerClass = AExoHollowAI::StaticClass();
	AutoPossessAI = EAutoPossessAI::PlacedInWorldOrSpawned;
	GetCapsuleComponent()->InitCapsuleSize(35.f, 90.f);
	// Characters face -Y in Blender (character bible 10); rotate the mesh to face +X like the UE mannequin.
	GetMesh()->SetRelativeRotation(FRotator(0.f, -90.f, 0.f));
	GetMesh()->SetRelativeLocation(FVector(0.f, 0.f, -90.f));

	// Stand-in shown until the character FBX is imported: a capsule-sized cylinder.
	Stand = CreateDefaultSubobject<UStaticMeshComponent>(TEXT("Stand"));
	Stand->SetupAttachment(GetCapsuleComponent());
	Stand->SetCollisionEnabled(ECollisionEnabled::NoCollision);
	static ConstructorHelpers::FObjectFinder<UStaticMesh> Cylinder(TEXT("/Engine/BasicShapes/Cylinder.Cylinder"));
	if (Cylinder.Succeeded()) Stand->SetStaticMesh(Cylinder.Object);

	GetCharacterMovement()->bOrientRotationToMovement = true;
	GetCharacterMovement()->RotationRate = FRotator(0.f, 240.f, 0.f);
	bUseControllerRotationYaw = false;
	Tags.Add(TEXT("Hollow"));
}

void AExoHollow::BeginPlay()
{
	Super::BeginPlay();
	ApplyType();
}

void AExoHollow::ApplyType()
{
	Stats = ExoTuning::Stats(HollowType);
	Health = Stats.Health;
	GetCapsuleComponent()->SetCapsuleSize(Stats.CapsuleRadiusCm, Stats.CapsuleHalfHeightCm);
	GetCharacterMovement()->MaxWalkSpeed = Stats.SpeedMps * 100.f;
	if (HollowType == EExoHollowType::Crawler)
	{
		GetCharacterMovement()->MaxStepHeight = 30.f;
	}
	bool bHasMesh = false;
	if (!MeshAsset.IsEmpty())
	{
		const FString Name = FPaths::GetBaseFilename(MeshAsset);
		if (USkeletalMesh* SK = LoadObject<USkeletalMesh>(nullptr, *FString::Printf(TEXT("%s.%s"), *MeshAsset, *Name), nullptr, LOAD_NoWarn | LOAD_Quiet))
		{
			GetMesh()->SetSkeletalMesh(SK);
			GetMesh()->SetRelativeLocation(FVector(0.f, 0.f, -Stats.CapsuleHalfHeightCm));
			bHasMesh = true;
		}
	}
	Stand->SetVisibility(!bHasMesh);
	const float H = Stats.CapsuleHalfHeightCm * 2.f;
	Stand->SetRelativeScale3D(FVector(Stats.CapsuleRadiusCm * 2.f / 100.f, Stats.CapsuleRadiusCm * 2.f / 100.f, H / 100.f));
}

bool AExoHollow::TryAttack(AActor* Target)
{
	if (bDead || !Target || AttackCooldown > 0.f) return false;
	const float Reach = Stats.CapsuleRadiusCm + 120.f;
	if (FVector::Dist2D(GetActorLocation(), Target->GetActorLocation()) > Reach + 125.f) return false;
	AttackCooldown = HollowType == EExoHollowType::Runner ? 0.9f : 1.6f;
	if (AExoPlayerCharacter* Player = Cast<AExoPlayerCharacter>(Target))
	{
		UGameplayStatics::ApplyDamage(Player, Stats.Damage, GetController(), this, nullptr);
		// A strike is a scratch: +6% +/- 2 (Crawlers 8%). Grabs (bites) come later in Act I.
		Player->Vitals->AddInfection(Stats.InfectionPerHit + FMath::FRandRange(-2.f, 2.f));
	}
	else if (AExoBlock* Block = Cast<AExoBlock>(Target))
	{
		UGameplayStatics::ApplyDamage(Block, Stats.Damage * 2.f, GetController(), this, nullptr);
		if (UExoNoiseSubsystem* Noise = GetWorld()->GetSubsystem<UExoNoiseSubsystem>())
		{
			Noise->ReportNoise(GetActorLocation(), 20.f, this, TEXT("Pounding"));
		}
	}
	return true;
}

float AExoHollow::TakeDamage(float Damage, const FDamageEvent& DamageEvent, AController* EventInstigator, AActor* DamageCauser)
{
	if (bDead) return 0.f;
	float Final = Damage;
	if (DamageEvent.IsOfType(FPointDamageEvent::ClassID))
	{
		const FPointDamageEvent& Point = static_cast<const FPointDamageEvent&>(DamageEvent);
		const float Top = GetActorLocation().Z + Stats.CapsuleHalfHeightCm;
		if (Point.HitInfo.ImpactPoint.Z > Top - Stats.CapsuleHalfHeightCm * 0.4f)
		{
			Final *= Stats.WeakPointMultiplier; // head / bloom node
		}
	}
	Health -= Final;
	// Being hurt reveals the attacker.
	if (AExoHollowAI* AI = Cast<AExoHollowAI>(GetController()))
	{
		if (EventInstigator && EventInstigator->GetPawn()) AI->Alert(EventInstigator->GetPawn()->GetActorLocation());
	}
	if (Health <= 0.f) Die();
	return Final;
}

void AExoHollow::Die()
{
	bDead = true;
	GetCharacterMovement()->DisableMovement();
	GetCapsuleComponent()->SetCollisionEnabled(ECollisionEnabled::NoCollision);
	if (GetMesh()->GetSkeletalMeshAsset())
	{
		GetMesh()->SetCollisionProfileName(TEXT("Ragdoll"));
		GetMesh()->SetSimulatePhysics(true);
	}
	else
	{
		Stand->SetRelativeRotation(FRotator(90.f, 0.f, 0.f));
	}
	if (AController* C = GetController()) C->UnPossess();
	if (UExoMissionSubsystem* Missions = GetWorld()->GetSubsystem<UExoMissionSubsystem>())
	{
		static const TCHAR* Names[] = {TEXT("Shambler"), TEXT("Runner"), TEXT("Crawler")};
		Missions->NotifyEvent(TEXT("killed"), StoryId.IsNone() ? FString(Names[(int32)HollowType]) : StoryId.ToString());
	}
	SetLifeSpan(45.f);
}

void AExoHollow::Tick(float DeltaSeconds)
{
	Super::Tick(DeltaSeconds);
	AttackCooldown = FMath::Max(0.f, AttackCooldown - DeltaSeconds);
	// Moans carry 60 m (level bible 13): the player hears them, and so do other Hollows (loosely).
	MoanClock -= DeltaSeconds;
	if (!bDead && MoanClock <= 0.f)
	{
		MoanClock = FMath::FRandRange(6.f, 14.f);
		if (UExoNoiseSubsystem* Noise = GetWorld()->GetSubsystem<UExoNoiseSubsystem>())
		{
			Noise->ReportNoise(GetActorLocation(), 3.f, this, TEXT("Moan"));
		}
	}
}
