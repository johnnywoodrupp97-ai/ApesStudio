#include "ExoMarker.h"
#include "ExoMissionSubsystem.h"
#include "ExoPlayerCharacter.h"
#include "Components/BoxComponent.h"
#include "Kismet/KismetMathLibrary.h"
#include "Engine/World.h"

AExoMarker::AExoMarker()
{
	RootComponent = CreateDefaultSubobject<USceneComponent>(TEXT("Root"));
}

AExoMissionTrigger::AExoMissionTrigger()
{
	Box = CreateDefaultSubobject<UBoxComponent>(TEXT("Box"));
	RootComponent = Box;
	Box->SetCollisionProfileName(TEXT("Trigger"));
	Box->SetBoxExtent(FVector(200.f, 200.f, 150.f));
}

void AExoMissionTrigger::OnConstruction(const FTransform& Transform)
{
	Super::OnConstruction(Transform);
	Box->SetBoxExtent(ExtentCm);
}

void AExoMissionTrigger::BeginPlay()
{
	Super::BeginPlay();
	Box->OnComponentBeginOverlap.AddDynamic(this, &AExoMissionTrigger::OnBeginOverlap);
}

void AExoMissionTrigger::OnBeginOverlap(UPrimitiveComponent* Overlapped, AActor* Other, UPrimitiveComponent* OtherComp, int32 BodyIndex, bool bFromSweep, const FHitResult& Sweep)
{
	if (!Other || !Other->IsA<AExoPlayerCharacter>() || (bOnce && bFired)) return;
	bFired = true;
	if (UExoMissionSubsystem* Missions = GetWorld()->GetSubsystem<UExoMissionSubsystem>())
	{
		Missions->NotifyEvent(TEXT("trigger"), MarkerName.ToString());
	}
}

AExoHordeZone::AExoHordeZone()
{
	Box = CreateDefaultSubobject<UBoxComponent>(TEXT("Box"));
	RootComponent = Box;
	Box->SetCollisionEnabled(ECollisionEnabled::NoCollision);
	Box->SetBoxExtent(FVector(1000.f, 1000.f, 250.f));
}

void AExoHordeZone::OnConstruction(const FTransform& Transform)
{
	Super::OnConstruction(Transform);
	Box->SetBoxExtent(ExtentCm);
}

FVector AExoHordeZone::RandomPoint() const
{
	return UKismetMathLibrary::RandomPointInBoundingBox(Box->GetComponentLocation(), Box->GetScaledBoxExtent() * FVector(1.f, 1.f, 0.f));
}
