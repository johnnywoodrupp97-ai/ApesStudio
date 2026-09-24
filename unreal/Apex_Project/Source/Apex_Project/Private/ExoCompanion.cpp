#include "ExoCompanion.h"
#include "ExoAnimComponent.h"
#include "ExoMissionSubsystem.h"
#include "AIController.h"
#include "Components/CapsuleComponent.h"
#include "Components/SkeletalMeshComponent.h"
#include "Engine/SkeletalMesh.h"
#include "Engine/World.h"
#include "GameFramework/CharacterMovementComponent.h"
#include "Kismet/GameplayStatics.h"
#include "Misc/Paths.h"
#include "Components/StaticMeshComponent.h"
#include "Engine/StaticMesh.h"
#include "UObject/ConstructorHelpers.h"

AExoCompanion::AExoCompanion()
{
	PrimaryActorTick.bCanEverTick = true;
	AIControllerClass = AAIController::StaticClass();
	AutoPossessAI = EAutoPossessAI::PlacedInWorldOrSpawned;
	GetMesh()->SetRelativeRotation(FRotator(0.f, -90.f, 0.f));
	GetMesh()->SetRelativeLocation(FVector(0.f, 0.f, -90.f));
	GetCharacterMovement()->bOrientRotationToMovement = true;
	GetCharacterMovement()->MaxWalkSpeed = 380.f;
	bUseControllerRotationYaw = false;

	Stand = CreateDefaultSubobject<UStaticMeshComponent>(TEXT("Stand"));
	Stand->SetupAttachment(GetCapsuleComponent());
	Stand->SetCollisionEnabled(ECollisionEnabled::NoCollision);
	static ConstructorHelpers::FObjectFinder<UStaticMesh> Cylinder(TEXT("/Engine/BasicShapes/Cylinder.Cylinder"));
	if (Cylinder.Succeeded()) Stand->SetStaticMesh(Cylinder.Object);
	Anim = CreateDefaultSubobject<UExoAnimComponent>(TEXT("Anim"));
}

void AExoCompanion::BeginPlay()
{
	Super::BeginPlay();
	const float Half = HeightCm * 0.5f;
	GetCapsuleComponent()->SetCapsuleSize(FMath::Min(35.f, Half * 0.4f), Half);
	GetMesh()->SetRelativeLocation(FVector(0.f, 0.f, -Half));
	Stand->SetRelativeScale3D(FVector(0.5f, 0.5f, HeightCm / 100.f));
	if (!MeshAsset.IsEmpty())
	{
		const FString Name = FPaths::GetBaseFilename(MeshAsset);
		if (USkeletalMesh* SK = LoadObject<USkeletalMesh>(nullptr, *FString::Printf(TEXT("%s.%s"), *MeshAsset, *Name), nullptr, LOAD_NoWarn | LOAD_Quiet))
		{
			GetMesh()->SetSkeletalMesh(SK);
			Stand->SetVisibility(false);
			Anim->Setup(GetMesh(), MeshAsset);
		}
	}
	// Companions in a mission group stay hidden until the mission brings them in.
	if (!Group.IsNone()) Deactivate();
}

void AExoCompanion::Activate()
{
	bActive = true;
	SetActorHiddenInGame(false);
	SetActorEnableCollision(true);
	SetActorTickEnabled(true);
}

void AExoCompanion::Deactivate()
{
	bActive = false;
	bFollow = false;
	SetActorHiddenInGame(true);
	SetActorEnableCollision(false);
	SetActorTickEnabled(false);
}

void AExoCompanion::Tick(float DeltaSeconds)
{
	Super::Tick(DeltaSeconds);
	const float Hours = DeltaSeconds / 150.f; // 1 in-game hour = 2.5 real minutes
	Hunger = FMath::Max(0.f, Hunger - 6.f * Hours);
	Rest = FMath::Max(0.f, Rest - 4.f * Hours);

	APawn* Player = UGameplayStatics::GetPlayerPawn(this, 0);
	if (bFollow && Player)
	{
		MoveClock -= DeltaSeconds;
		if (MoveClock <= 0.f)
		{
			MoveClock = 0.5f;
			const float D = FVector::Dist(Player->GetActorLocation(), GetActorLocation());
			GetCharacterMovement()->MaxWalkSpeed = D > 800.f ? 600.f : 380.f;
			// Left far behind (a mission teleport, a fall): catch up out of sight.
			if (D > 4000.f) TeleportTo(Player->GetActorLocation() - Player->GetActorForwardVector() * 250.f, GetActorRotation());
			if (AAIController* AI = Cast<AAIController>(GetController()))
			{
				if (D > 300.f) AI->MoveToActor(Player, 200.f);
			}
		}
		// Safety rises near the player at a lit base; drops on the road.
		Safety = FMath::Clamp(Safety + (FVector::Dist(Player->GetActorLocation(), GetActorLocation()) < 600.f ? 2.f : -1.f) * Hours * 10.f, 0.f, 100.f);
	}

	const UExoMissionSubsystem* Missions = GetWorld()->GetSubsystem<UExoMissionSubsystem>();
	const FExoLine* Line = Missions ? Missions->GetCurrentLine() : nullptr;
	Anim->bTalking = BarkTime > 0.f || (Line && IsSpeaking(Line->Speaker));

	BarkTime = FMath::Max(0.f, BarkTime - DeltaSeconds);
	BarkClock -= DeltaSeconds;
	if (BarkClock <= 0.f && Player && FVector::Dist(Player->GetActorLocation(), GetActorLocation()) < 1200.f)
	{
		BarkClock = FMath::FRandRange(25.f, 45.f);
		if (Hunger < 20.f) CurrentBark = TEXT("I'm really hungry...");
		else if (Barks.Num() > 0) CurrentBark = Barks[FMath::RandRange(0, Barks.Num() - 1)];
		else CurrentBark.Reset();
		BarkTime = CurrentBark.IsEmpty() ? 0.f : 4.f;
	}
}

bool AExoCompanion::IsSpeaking(const FString& Speaker) const
{
	// "Tug", "Mara Voss", "Halvard Crane" and "Trooper" speak in person; "Ada (radio)" or "Lily (vents)" do not.
	if (CompanionId.IsNone() || Speaker.Contains(TEXT("("))) return false;
	const FString Id = CompanionId.ToString();
	TArray<FString> Words;
	Speaker.ParseIntoArrayWS(Words);
	for (const FString& W : Words)
	{
		if (W.Equals(Id, ESearchCase::IgnoreCase)) return true;
	}
	return Words.Num() == 1 && Id.StartsWith(Words[0], ESearchCase::IgnoreCase); // "Trooper" -> TrooperGate1
}
