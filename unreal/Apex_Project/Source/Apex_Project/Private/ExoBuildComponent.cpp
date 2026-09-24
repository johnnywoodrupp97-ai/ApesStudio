#include "ExoBuildComponent.h"
#include "ExoBlock.h"
#include "ExoPlayerCharacter.h"
#include "ExoNoiseSubsystem.h"
#include "Engine/World.h"

UExoBuildComponent::UExoBuildComponent()
{
	PrimaryComponentTick.bCanEverTick = true;
}

void UExoBuildComponent::BeginPlay()
{
	Super::BeginPlay();
	Parts = ExoTuning::SliceParts();
}

AExoPlayerCharacter* UExoBuildComponent::GetPlayer() const
{
	return Cast<AExoPlayerCharacter>(GetOwner());
}

AActor* UExoBuildComponent::GetGhost() const
{
	return Ghost;
}

void UExoBuildComponent::SetBuildMode(bool bOn)
{
	bBuildMode = bOn;
	if (bBuildMode) RespawnGhost();
	else if (Ghost) { Ghost->Destroy(); Ghost = nullptr; }
}

void UExoBuildComponent::CyclePart(int32 Dir)
{
	if (Parts.Num() == 0) return;
	SelectedIndex = (SelectedIndex + Dir + Parts.Num()) % Parts.Num();
	if (bBuildMode) RespawnGhost();
}

void UExoBuildComponent::RotateGhost()
{
	YawSteps = FMath::Fmod(YawSteps + 1.f, 4.f);
}

void UExoBuildComponent::RespawnGhost()
{
	if (Ghost) Ghost->Destroy();
	FActorSpawnParameters P;
	P.SpawnCollisionHandlingOverride = ESpawnActorCollisionHandlingMethod::AlwaysSpawn;
	Ghost = GetWorld()->SpawnActor<AExoBlock>(AExoBlock::StaticClass(), FTransform::Identity, P);
	if (Ghost) Ghost->InitPart(Parts[SelectedIndex], true);
}

bool UExoBuildComponent::ComputePlacement(FTransform& OutTransform) const
{
	AExoPlayerCharacter* Player = GetPlayer();
	FHitResult Hit;
	if (!Player || !Player->TraceView(ReachCm, Hit)) return false;
	const float Cell = ExoTuning::LargeCellCm;
	// Step off the hit surface by half a cell along its normal, then snap to the world grid.
	const FVector P = Hit.ImpactPoint + Hit.ImpactNormal * (Cell * 0.5f);
	FVector Snapped(FMath::GridSnap(P.X, Cell), FMath::GridSnap(P.Y, Cell), 0.f);
	// Rest on whatever is below: ground hits keep the block's bottom on the surface.
	if (Hit.ImpactNormal.Z > 0.7f && !(Hit.GetActor() && Hit.GetActor()->ActorHasTag(TEXT("ExoBlock"))))
	{
		Snapped.Z = Hit.ImpactPoint.Z + Cell * 0.5f;
	}
	else
	{
		Snapped.Z = FMath::GridSnap(P.Z - Cell * 0.5f, Cell) + Cell * 0.5f;
		if (AActor* HitActor = Hit.GetActor())
		{
			if (HitActor->ActorHasTag(TEXT("ExoBlock")))
			{
				// Stack cleanly on existing blocks: align to their grid height.
				const float BaseZ = HitActor->GetActorLocation().Z;
				Snapped.Z = BaseZ + FMath::GridSnap(P.Z - BaseZ, Cell);
			}
		}
	}
	OutTransform = FTransform(FRotator(0.f, YawSteps * 90.f, 0.f), Snapped);
	return true;
}

AExoBlock* UExoBuildComponent::GetTargetBlock() const
{
	AExoPlayerCharacter* Player = GetPlayer();
	FHitResult Hit;
	if (Player && Player->TraceView(ReachCm, Hit))
	{
		AExoBlock* B = Cast<AExoBlock>(Hit.GetActor());
		return (B && !B->bGhost) ? B : nullptr;
	}
	return nullptr;
}

void UExoBuildComponent::PrimaryPressed()
{
	AExoPlayerCharacter* Player = GetPlayer();
	if (!Player || !bBuildMode) return;
	if (AExoBlock* Target = GetTargetBlock())
	{
		if (!Target->IsComplete()) return; // welding happens while held (Weld)
	}
	const FExoPartDef& Part = Parts[SelectedIndex];
	FTransform Where;
	if (!ComputePlacement(Where) || Player->Components < Part.Cost) return;
	// Don't place inside the player or another block.
	if (FVector::Dist(Where.GetLocation(), Player->GetActorLocation()) < ExoTuning::LargeCellCm * 0.6f) return;
	FActorSpawnParameters P;
	P.SpawnCollisionHandlingOverride = ESpawnActorCollisionHandlingMethod::DontSpawnIfColliding;
	if (AExoBlock* Block = GetWorld()->SpawnActor<AExoBlock>(AExoBlock::StaticClass(), Where, P))
	{
		Block->InitPart(Part, false);
		Player->Components -= Part.Cost;
	}
}

void UExoBuildComponent::Weld(float DeltaSeconds)
{
	if (AExoBlock* Block = GetTargetBlock())
	{
		if (Block->IsComplete()) return;
		// Bigger parts take longer: rate scales with 1 / cell count.
		const FIntVector S = Block->Part.SizeCells;
		const float Cells = FMath::Max(1, S.X * S.Y * S.Z);
		Block->AddProgress(WeldRate * DeltaSeconds / Cells);
		NoiseClock += DeltaSeconds;
		if (NoiseClock > 0.5f)
		{
			NoiseClock = 0.f;
			if (UExoNoiseSubsystem* Noise = GetWorld()->GetSubsystem<UExoNoiseSubsystem>())
			{
				Noise->ReportNoise(Block->GetActorLocation(), 10.f, GetOwner(), TEXT("Welding"));
			}
		}
	}
}

void UExoBuildComponent::Grind(float DeltaSeconds)
{
	if (AExoBlock* Block = GetTargetBlock())
	{
		const float Before = Block->BuildProgress;
		const int32 Cost = Block->Part.Cost;
		Block->AddProgress(-GrindRate * DeltaSeconds);
		// Grinding refunds components in proportion to the frame removed.
		if (AExoPlayerCharacter* Player = GetPlayer())
		{
			const float Removed = Before - (IsValid(Block) ? Block->BuildProgress : 0.f);
			GrindCarry += Removed * Cost;
			const int32 Whole = FMath::FloorToInt(GrindCarry);
			Player->Components += Whole;
			GrindCarry -= Whole;
		}
	}
}

void UExoBuildComponent::TickComponent(float DeltaTime, ELevelTick TickType, FActorComponentTickFunction* ThisTickFunction)
{
	Super::TickComponent(DeltaTime, TickType, ThisTickFunction);
	if (!bBuildMode || !Ghost) return;
	FTransform Where;
	const bool bValid = ComputePlacement(Where);
	Ghost->SetActorHiddenInGame(!bValid);
	if (bValid) Ghost->SetActorTransform(Where);
}
