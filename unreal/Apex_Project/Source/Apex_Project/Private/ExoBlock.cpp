#include "ExoBlock.h"
#include "ExoNoiseSubsystem.h"
#include "ExoMissionSubsystem.h"
#include "Components/StaticMeshComponent.h"
#include "Components/PointLightComponent.h"
#include "Engine/StaticMesh.h"
#include "Engine/World.h"
#include "UObject/ConstructorHelpers.h"

AExoBlock::AExoBlock()
{
	PrimaryActorTick.bCanEverTick = true;
	PrimaryActorTick.TickInterval = 0.25f;
	Root = CreateDefaultSubobject<USceneComponent>(TEXT("Root"));
	RootComponent = Root;
	Mesh = CreateDefaultSubobject<UStaticMeshComponent>(TEXT("Mesh"));
	Mesh->SetupAttachment(Root);
	Mesh->SetCollisionProfileName(TEXT("BlockAll"));
	Mesh->SetCanEverAffectNavigation(true);

	Light = CreateDefaultSubobject<UPointLightComponent>(TEXT("Light"));
	Light->SetupAttachment(Mesh);
	Light->SetRelativeLocation(FVector(0.f, 0.f, 180.f));
	Light->SetVisibility(false);
	Tags.Add(TEXT("ExoBlock"));
}

UStaticMesh* AExoBlock::LoadPartMesh(const FString& Asset)
{
	// exodus_setup.py imports every part FBX to /Game/Exodus/Imported/Parts/<Asset>.<Asset>.
	const FString Path = FString::Printf(TEXT("/Game/Exodus/Imported/Parts/%s.%s"), *Asset, *Asset);
	if (UStaticMesh* M = LoadObject<UStaticMesh>(nullptr, *Path, nullptr, LOAD_NoWarn | LOAD_Quiet))
	{
		return M;
	}
	return LoadObject<UStaticMesh>(nullptr, TEXT("/Engine/BasicShapes/Cube.Cube"));
}

void AExoBlock::InitPart(const FExoPartDef& InPart, bool bAsGhost)
{
	Part = InPart;
	bGhost = bAsGhost;
	Health = Part.Integrity;
	UStaticMesh* M = LoadPartMesh(Part.Asset);
	Mesh->SetStaticMesh(M);
	// The engine cube is 1 m; part meshes are already at size (2.5 m cells).
	const bool bPlaceholder = M && M->GetName() == TEXT("Cube");
	BaseScale = bPlaceholder ? FVector(Part.SizeCells) * (ExoTuning::LargeCellCm / 100.f) : FVector::OneVector;
	HalfHeight = M ? M->GetBounds().BoxExtent.Z * BaseScale.Z : Part.SizeCells.Z * ExoTuning::LargeCellCm * 0.5f;
	Mesh->SetCollisionEnabled(bGhost ? ECollisionEnabled::NoCollision : ECollisionEnabled::QueryAndPhysics);
	Mesh->SetCanEverAffectNavigation(!bGhost);
	if (bGhost)
	{
		BuildProgress = 1.f;
		Mesh->SetRenderCustomDepth(true);
		Mesh->SetCastShadow(false);
	}
	RefreshVisual();
}

void AExoBlock::RefreshVisual()
{
	// Construction stages (parts bible BS1..BSn): the frame rises with weld progress.
	// The root sits at the cell centre; the mesh keeps its bottom on the ground and grows upward.
	const float Z = bGhost ? 1.f : FMath::Clamp(BuildProgress, 0.15f, 1.f);
	Mesh->SetRelativeScale3D(FVector(BaseScale.X, BaseScale.Y, BaseScale.Z * Z));
	Mesh->SetRelativeLocation(FVector(0.f, 0.f, -HalfHeight * (1.f - Z)));
	const bool bLit = IsComplete() && !bGhost && Part.LightLumens > 0.f;
	Light->SetVisibility(bLit);
	if (bLit)
	{
		Light->SetIntensity(Part.LightLumens);
		Light->SetAttenuationRadius(Part.LightLumens > 2000.f ? 3000.f : 1200.f);
		Light->SetLightColor(Part.PartId == TEXT("COL-001") ? FLinearColor(1.f, 0.55f, 0.2f) : FLinearColor(1.f, 0.95f, 0.85f));
	}
}

bool AExoBlock::AddProgress(float Delta)
{
	const bool bWas = IsComplete();
	BuildProgress = FMath::Clamp(BuildProgress + Delta, 0.f, 1.f);
	RefreshVisual();
	if (!bWas && IsComplete())
	{
		if (UExoMissionSubsystem* Missions = GetWorld()->GetSubsystem<UExoMissionSubsystem>())
		{
			Missions->NotifyEvent(TEXT("built"), Part.PartId.ToString());
		}
		return true;
	}
	if (BuildProgress <= 0.f)
	{
		Destroy();
	}
	return false;
}

float AExoBlock::GetAttraction() const
{
	if (!IsComplete() || bGhost) return 0.f;
	return Part.NoiseDb * 0.5f + Part.LightLumens * 0.01f + FMath::Max(0.f, Part.PowerKW) / 1000.f * 20.f;
}

float AExoBlock::TakeDamage(float Damage, const FDamageEvent& DamageEvent, AController* EventInstigator, AActor* DamageCauser)
{
	if (bGhost) return 0.f;
	Health -= Damage;
	if (Health <= 0.f)
	{
		if (UExoMissionSubsystem* Missions = GetWorld()->GetSubsystem<UExoMissionSubsystem>())
		{
			Missions->NotifyEvent(TEXT("block_destroyed"), Part.PartId.ToString());
		}
		Destroy();
	}
	return Damage;
}

void AExoBlock::Tick(float DeltaSeconds)
{
	Super::Tick(DeltaSeconds);
	// Running generators hum (noise for Hollows): 85 dB heard ~20 m away.
	if (!bGhost && IsComplete() && Part.NoiseDb >= 50.f)
	{
		HumClock += DeltaSeconds;
		if (HumClock >= 2.f)
		{
			HumClock = 0.f;
			if (UExoNoiseSubsystem* Noise = GetWorld()->GetSubsystem<UExoNoiseSubsystem>())
			{
				Noise->ReportNoise(GetActorLocation(), Part.NoiseDb / 4.f, this, TEXT("Machine"));
			}
		}
	}
}
