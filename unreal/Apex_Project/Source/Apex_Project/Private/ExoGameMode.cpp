#include "ExoGameMode.h"
#include "Apex_Project.h"
#include "ExoTypes.h"
#include "ExoPlayerCharacter.h"
#include "ExoVitalsComponent.h"
#include "ExoHUD.h"
#include "ExoBlock.h"
#include "ExoHollow.h"
#include "ExoCompanion.h"
#include "ExoMarker.h"
#include "ExoSpawner.h"
#include "ExoNoiseSubsystem.h"
#include "ExoMissionSubsystem.h"
#include "Components/DirectionalLightComponent.h"
#include "Engine/DirectionalLight.h"
#include "Engine/World.h"
#include "EngineUtils.h"
#include "TimerManager.h"
#include "Kismet/GameplayStatics.h"

AExoGameMode::AExoGameMode()
{
	PrimaryActorTick.bCanEverTick = true;
	DefaultPawnClass = AExoPlayerCharacter::StaticClass();
	HUDClass = AExoHUD::StaticClass();
}

void AExoGameMode::StartPlay()
{
	Super::StartPlay();
	bWasNight = IsNight();
	UpdateSun();
}

bool AExoGameMode::IsNight() const
{
	// 20 of 60 minutes are night: 20:00 to 04:00 in-game.
	const float H = GetHour();
	return H >= 20.f || H < 4.f;
}

void AExoGameMode::SetHour(float Hour)
{
	TimeOfDay = FMath::Fmod(FMath::Max(0.f, Hour), 24.f) * 150.f;
	bWasNight = IsNight();
	UpdateSun();
}

void AExoGameMode::UpdateSun()
{
	for (TActorIterator<ADirectionalLight> It(GetWorld()); It; ++It)
	{
		if (!It->ActorHasTag(TEXT("ExoSun"))) continue;
		// Day runs 04:00-20:00: the sun climbs from the east horizon to overhead and sets in the west.
		const float H = GetHour();
		const float DayT = FMath::Clamp((H - 4.f) / 16.f, 0.f, 1.f);
		const float Elevation = IsNight() ? -20.f : FMath::Sin(DayT * PI) * 70.f + 2.f;
		It->SetActorRotation(FRotator(-Elevation, 90.f + DayT * 180.f, 0.f));
		if (UDirectionalLightComponent* L = Cast<UDirectionalLightComponent>(It->GetLightComponent()))
		{
			if (IsNight())
			{
				// Moonlight; the Green Moon tints it (level bible 13).
				It->SetActorRotation(FRotator(-35.f, 200.f, 0.f));
				L->SetIntensity(0.4f);
				L->SetLightColor(bGreenMoonTonight ? FLinearColor(0.55f, 1.f, 0.6f) : FLinearColor(0.6f, 0.7f, 1.f));
			}
			else
			{
				L->SetIntensity(10.f);
				L->SetLightColor(FLinearColor(1.f, 0.96f, 0.9f));
			}
		}
	}
}

float AExoGameMode::GetAttraction() const
{
	float A = 0.f;
	for (TActorIterator<AExoBlock> It(GetWorld()); It; ++It) A += It->GetAttraction();
	if (const UExoNoiseSubsystem* Noise = GetWorld()->GetSubsystem<UExoNoiseSubsystem>())
	{
		A += Noise->CountRecent(TEXT("Gunfire"), 150.f) * 5.f;
	}
	for (TActorIterator<AExoCompanion> It(GetWorld()); It; ++It) if (It->IsActive()) A += 4.f;
	return FMath::Clamp(A, 0.f, 1000.f);
}

int32 AExoGameMode::SpawnHorde(int32 Count)
{
	APawn* Player = UGameplayStatics::GetPlayerPawn(this, 0);
	if (!Player) return 0;
	if (Count <= 0)
	{
		const float BloomMul = FMath::Lerp(0.5f, 2.f, (FMath::Clamp(BloomLevel, 1, 5) - 1) / 4.f);
		Count = FMath::RoundToInt(ExoTuning::HordeSize(GetAttraction(), bGreenMoonTonight) * BloomMul);
	}
	// Candidate zones: >= 60 m away and out of sight (never spawn in view, level bible 12).
	TArray<AExoHordeZone*> Zones;
	for (TActorIterator<AExoHordeZone> It(GetWorld()); It; ++It)
	{
		const FVector To = It->GetActorLocation() - Player->GetActorLocation();
		if (To.Size() < ExoTuning::HordeMinSpawnDistanceCm) continue;
		FHitResult Hit;
		const bool bBlocked = GetWorld()->LineTraceSingleByChannel(Hit, Player->GetActorLocation() + FVector(0, 0, 60), It->GetActorLocation() + FVector(0, 0, 100), ECC_Visibility);
		const bool bBehind = FVector::DotProduct(Player->GetActorForwardVector(), To.GetSafeNormal()) < 0.2f;
		if (bBlocked || bBehind) Zones.Add(*It);
	}
	if (Zones.Num() == 0)
	{
		UE_LOG(LogExodus, Warning, TEXT("Horde of %d: no hidden HS_ zone 60 m+ away"), Count);
		return 0;
	}
	int32 Alive = 0;
	for (TActorIterator<AExoHollow> It(GetWorld()); It; ++It) if (!It->IsDead()) ++Alive;
	const int32 Budget = FMath::Max(0, MaxActiveHollows - Alive);
	const int32 ToSpawn = FMath::Min(Count, Budget);
	for (int32 i = 0; i < ToSpawn; ++i)
	{
		AExoHordeZone* Z = Zones[i % Zones.Num()];
		// Runners join from the third night; the rest are Shamblers (22.5).
		const EExoHollowType Type = (NightIndex >= 3 && FMath::FRand() < 0.2f) ? EExoHollowType::Runner : EExoHollowType::Shambler;
		const FString Mesh = Type == EExoHollowType::Runner ? TEXT("/Game/Exodus/Imported/Characters/SK_ENM_Runner") : TEXT("/Game/Exodus/Imported/Characters/SK_ENM_Shambler");
		AExoSpawner::SpawnHollow(GetWorld(), Z->RandomPoint(), Type, Mesh, NAME_None, true);
	}
	UE_LOG(LogExodus, Log, TEXT("Horde: %d requested, %d spawned (Attraction %.0f, night %d%s)"), Count, ToSpawn, GetAttraction(), NightIndex, bGreenMoonTonight ? TEXT(", Green Moon") : TEXT(""));
	return ToSpawn;
}

void AExoGameMode::Tick(float DeltaSeconds)
{
	Super::Tick(DeltaSeconds);
	TimeOfDay = FMath::Fmod(TimeOfDay + DeltaSeconds * TimeScale, ExoTuning::DayLengthSeconds);
	UpdateSun();

	const bool bNight = IsNight();
	if (bNight && !bWasNight)
	{
		++NightIndex;
		bGreenMoonTonight = NightIndex % ExoTuning::GreenMoonEvery == 0;
		if (bHordesEnabled) SpawnHorde(0);
	}
	else if (!bNight && bWasNight)
	{
		bGreenMoonTonight = false;
		if (UExoMissionSubsystem* Missions = GetWorld()->GetSubsystem<UExoMissionSubsystem>())
		{
			Missions->NotifyEvent(TEXT("night_survived"), FString());
		}
	}
	bWasNight = bNight;
}

void AExoGameMode::SetCheckpoint(AActor* Marker)
{
	if (Marker) Checkpoint = Marker;
}

void AExoGameMode::HandlePlayerDeath(AExoPlayerCharacter* Player)
{
	if (!Player) return;
	DeadPlayer = Player;
	Player->bInputEnabled = false;
	GetWorldTimerManager().SetTimer(RespawnHandle, this, &AExoGameMode::Respawn, 4.f, false);
}

void AExoGameMode::Respawn()
{
	AExoPlayerCharacter* Player = DeadPlayer.Get();
	if (!Player) return;
	if (AActor* C = Checkpoint.Get())
	{
		Player->TeleportTo(C->GetActorLocation() + FVector(0.f, 0.f, 100.f), C->GetActorRotation());
	}
	Player->Vitals->ResetVitals();
	Player->bInputEnabled = true;
}

void AExoGameMode::ExoJump(const FString& StepId)
{
	if (UExoMissionSubsystem* M = GetWorld()->GetSubsystem<UExoMissionSubsystem>()) M->JumpToStep(StepId);
}

void AExoGameMode::ExoTime(float Hour) { SetHour(Hour); }
void AExoGameMode::ExoHorde(int32 Count) { SpawnHorde(Count); }

void AExoGameMode::ExoGive(int32 ComponentsCount)
{
	if (AExoPlayerCharacter* P = Cast<AExoPlayerCharacter>(UGameplayStatics::GetPlayerPawn(this, 0))) P->Components += ComponentsCount;
}
