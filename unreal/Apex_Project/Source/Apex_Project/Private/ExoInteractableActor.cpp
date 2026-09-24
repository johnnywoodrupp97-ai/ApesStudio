#include "ExoInteractableActor.h"
#include "ExoPlayerCharacter.h"
#include "ExoVitalsComponent.h"
#include "ExoNoiseSubsystem.h"
#include "ExoMissionSubsystem.h"
#include "Components/StaticMeshComponent.h"
#include "Engine/StaticMesh.h"
#include "Engine/World.h"
#include "UObject/ConstructorHelpers.h"
#include "ExoCompanion.h"
#include "EngineUtils.h"

#define LOCTEXT_NAMESPACE "Exodus"

AExoInteractableActor::AExoInteractableActor()
{
	Mesh = CreateDefaultSubobject<UStaticMeshComponent>(TEXT("Mesh"));
	RootComponent = Mesh;
	static ConstructorHelpers::FObjectFinder<UStaticMesh> Cube(TEXT("/Engine/BasicShapes/Cube.Cube"));
	if (Cube.Succeeded()) Mesh->SetStaticMesh(Cube.Object);
	Mesh->SetRelativeScale3D(FVector(0.5f));
	Mesh->SetCollisionProfileName(TEXT("BlockAll"));
}

void AExoInteractableActor::BeginPlay()
{
	Super::BeginPlay();
	bEnabled = Group.IsNone();
	if (Kind == EExoInteractKind::Door || Kind == EExoInteractKind::Ladder || Kind == EExoInteractKind::Radio) bOneShot = false;
	ConfigureVisual();
	ClosedLocation = GetActorLocation();
}

void AExoInteractableActor::ConfigureVisual()
{
	switch (Kind)
	{
	case EExoInteractKind::Door:      Mesh->SetRelativeScale3D(DoorSize / 100.f); break;
	case EExoInteractKind::MedCabinet: Mesh->SetRelativeScale3D(FVector(0.2f, 0.6f, 0.8f)); break;
	case EExoInteractKind::FireAlarm: Mesh->SetRelativeScale3D(FVector(0.1f, 0.15f, 0.2f)); break;
	case EExoInteractKind::Console:   Mesh->SetRelativeScale3D(FVector(0.8f, 1.6f, 1.0f)); break;
	case EExoInteractKind::Ladder:    Mesh->SetRelativeScale3D(FVector(0.2f, 1.0f, 2.4f)); break;
	default: break;
	}
}

FText AExoInteractableActor::GetPrompt() const
{
	if (!Prompt.IsEmpty()) return Prompt;
	switch (Kind)
	{
	case EExoInteractKind::MedCabinet: return LOCTEXT("Med", "E  Take Suppressant");
	case EExoInteractKind::Salvage:    return LOCTEXT("Salvage", "E  Salvage components");
	case EExoInteractKind::Food:       return LOCTEXT("Food", "E  Eat");
	case EExoInteractKind::Water:      return LOCTEXT("Water", "E  Drink");
	case EExoInteractKind::Door:       return bOpen ? LOCTEXT("Close", "E  Close") : LOCTEXT("Open", "E  Open");
	case EExoInteractKind::FireAlarm:  return LOCTEXT("Alarm", "E  Pull the fire alarm");
	case EExoInteractKind::Console:    return LOCTEXT("Console", "E  Use console");
	case EExoInteractKind::Radio:      return LOCTEXT("Radio", "E  Listen");
	case EExoInteractKind::Ladder:     return Destination.Z > GetActorLocation().Z ? LOCTEXT("Up", "E  Climb up") : LOCTEXT("Down", "E  Climb down");
	default:                           return LOCTEXT("Use", "E  Use");
	}
}

void AExoInteractableActor::Interact(AExoPlayerCharacter* Player)
{
	if (!Player || !CanInteract(Player)) return;
	switch (Kind)
	{
	case EExoInteractKind::MedCabinet: Player->Vitals->Suppressants += Amount; break;
	case EExoInteractKind::Salvage:    Player->Components += Amount; break;
	case EExoInteractKind::Food:       Player->Vitals->Eat(40.f * Amount); break;
	case EExoInteractKind::Water:      Player->Vitals->Drink(40.f * Amount); break;
	case EExoInteractKind::Door:
		bOpen = !bOpen;
		// Slide the leaf up into the frame (blast-door style) and clear its collision.
		SetActorLocation(ClosedLocation + FVector(0.f, 0.f, bOpen ? DoorSize.Z * 0.95f : 0.f));
		Mesh->SetCollisionEnabled(bOpen ? ECollisionEnabled::NoCollision : ECollisionEnabled::QueryAndPhysics);
		break;
	case EExoInteractKind::Ladder:
		Player->TeleportTo(Destination + FVector(0.f, 0.f, 95.f), Player->GetActorRotation());
		// Companions climb with you.
		for (TActorIterator<AExoCompanion> It(GetWorld()); It; ++It)
		{
			if (It->bFollow) It->TeleportTo(Destination + FVector(80.f, 80.f, 95.f), It->GetActorRotation());
		}
		break;
	case EExoInteractKind::FireAlarm:
		if (UExoNoiseSubsystem* Noise = GetWorld()->GetSubsystem<UExoNoiseSubsystem>())
		{
			Noise->ReportNoise(GetActorLocation(), 150.f, this, TEXT("Alarm"));
		}
		break;
	default: break;
	}
	if (bOneShot) bUsed = true;
	if (UExoMissionSubsystem* Missions = GetWorld()->GetSubsystem<UExoMissionSubsystem>())
	{
		Missions->NotifyEvent(TEXT("interact"), MarkerName.ToString());
	}
}

#undef LOCTEXT_NAMESPACE
