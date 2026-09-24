// EXODUS PROTOCOL — shared types and tuning for the vertical slice.
// Numbers come from the game bible: 22 (balance), 05 (infection), 21 (controls), and the level bible 02 (metrics).
#pragma once

#include "CoreMinimal.h"
#include "ExoTypes.generated.h"

/** Hollow archetypes in the slice (game bible 09 / 22.6). */
UENUM(BlueprintType)
enum class EExoHollowType : uint8
{
	Shambler,
	Runner,
	Crawler
};

/** Infection stages (game bible 05). */
UENUM(BlueprintType)
enum class EExoInfectionStage : uint8
{
	Clean,     // 0%
	Exposed,   // 1-24%
	Seeded,    // 25-59%
	Blooming,  // 60-89%
	Turning    // 90-100% (60 s countdown)
};

/** One buildable part in the slice's build menu (parts bible ids and asset names). */
USTRUCT(BlueprintType)
struct FExoPartDef
{
	GENERATED_BODY()

	UPROPERTY(EditAnywhere, BlueprintReadWrite) FName PartId;
	UPROPERTY(EditAnywhere, BlueprintReadWrite) FString Name;
	UPROPERTY(EditAnywhere, BlueprintReadWrite) FString Asset;        // SM_<CAT>_<Name>_LG, imported to /Game/Exodus/Imported/Parts/
	UPROPERTY(EditAnywhere, BlueprintReadWrite) float Integrity = 500.f;
	UPROPERTY(EditAnywhere, BlueprintReadWrite) int32 Cost = 10;         // salvage components (sum of the recipe)
	UPROPERTY(EditAnywhere, BlueprintReadWrite) float PowerKW = 0.f;     // + generates, - draws
	UPROPERTY(EditAnywhere, BlueprintReadWrite) float NoiseDb = 0.f;     // feeds Attraction (22.5)
	UPROPERTY(EditAnywhere, BlueprintReadWrite) float LightLumens = 0.f; // feeds Attraction (22.5)
	UPROPERTY(EditAnywhere, BlueprintReadWrite) FIntVector SizeCells = FIntVector(1, 1, 1);
};

/** Stats per Hollow type (game bible 22.6, Normal difficulty). */
struct FExoHollowStats
{
	float Health;
	float SpeedMps;
	float Damage;
	float InfectionPerHit; // percent
	float WeakPointMultiplier;
	float CapsuleRadiusCm;
	float CapsuleHalfHeightCm;
};

namespace ExoTuning
{
	// Grid (parts bible): large grid cell 2.5 m.
	constexpr float LargeCellCm = 250.f;

	// Player movement (level bible 02 / game bible 21).
	constexpr float WalkSpeed = 160.f;
	constexpr float JogSpeed = 380.f;
	constexpr float SprintSpeed = 620.f;
	constexpr float CrouchSpeed = 150.f;

	// Vitals (22.2), per real minute unless noted.
	constexpr float HungerDrainPerMin = 1.0f;
	constexpr float ThirstDrainPerMin = 1.5f;
	constexpr float SprintStaminaPerSec = 12.f;
	constexpr float MeleeStaminaCost = 15.f;
	constexpr float StaminaRegenPerSec = 20.f;
	constexpr float StaminaRegenDelay = 1.f;

	// Infection (22.3).
	constexpr float SeededThreshold = 25.f;
	constexpr float PlayerProgressSecondsPerPercent = 60.f;
	constexpr float SuppressantAmount = 10.f;
	constexpr float SuppressantHaltSeconds = 20.f * 60.f;
	constexpr float TurningThreshold = 90.f;
	constexpr float TurningCountdown = 60.f;

	// Senses (level bible 02 / 12): hearing is carried by each noise's radius.
	constexpr float HollowSightCm = 1500.f;
	constexpr float HordeMinSpawnDistanceCm = 6000.f;

	// Time (22.1): 60 real minutes per day, 40 day / 20 night.
	constexpr float DayLengthSeconds = 3600.f;
	constexpr float NightFraction = 20.f / 60.f;
	constexpr int32 GreenMoonEvery = 3;

	// Ada's wrench (22.7).
	constexpr float WrenchDamage = 35.f;
	constexpr float WrenchRange = 200.f;
	constexpr float WrenchNoiseRadiusM = 8.f;

	inline FExoHollowStats Stats(EExoHollowType Type)
	{
		switch (Type)
		{
		case EExoHollowType::Runner:  return {70.f, 5.8f, 10.f, 6.f, 3.f, 35.f, 90.f};
		case EExoHollowType::Crawler: return {60.f, 2.0f, 15.f, 8.f, 2.5f, 40.f, 30.f};
		default:                      return {100.f, 1.1f, 12.f, 6.f, 3.f, 35.f, 90.f};
		}
	}

	/** The slice build menu: Act I tier T0/T1 parts from the parts bible. */
	inline TArray<FExoPartDef> SliceParts()
	{
		auto P = [](const TCHAR* Id, const TCHAR* Name, const TCHAR* Asset, float Hp, int32 Cost, float Kw, float Db, float Lm)
		{
			FExoPartDef D;
			D.PartId = FName(Id); D.Name = Name; D.Asset = Asset; D.Integrity = Hp; D.Cost = Cost;
			D.PowerKW = Kw; D.NoiseDb = Db; D.LightLumens = Lm;
			return D;
		};
		return {
			P(TEXT("STR-017"), TEXT("Scrap Wall"), TEXT("SM_STR_ScrapWall_ASheetAndSigns_LG"), 700.f, 22, 0.f, 0.f, 0.f),
			P(TEXT("DEF-001"), TEXT("Barricade"), TEXT("SM_DEF_Barricade_Wooden_LG"), 800.f, 20, 0.f, 0.f, 0.f),
			P(TEXT("DEF-002"), TEXT("Sandbag Wall"), TEXT("SM_DEF_SandbagWall_FullHeight_LG"), 1400.f, 12, 0.f, 0.f, 0.f),
			P(TEXT("STR-001"), TEXT("Armor Block (steel plate)"), TEXT("SM_STR_ArmorBlock_Light_LG"), 1500.f, 25, 0.f, 0.f, 0.f),
			P(TEXT("DOR-001"), TEXT("Scrap Door"), TEXT("SM_DOR_ScrapDoor_LG"), 400.f, 17, 0.f, 0.f, 0.f),
			P(TEXT("PRD-001"), TEXT("Workbench"), TEXT("SM_PRD_Workbench_LG"), 500.f, 25, 0.f, 10.f, 0.f),
			P(TEXT("PWR-001"), TEXT("Diesel Generator"), TEXT("SM_PWR_DieselGenerator_LG"), 1200.f, 40, 60.f, 85.f, 0.f),
			P(TEXT("UTL-001"), TEXT("Floodlight"), TEXT("SM_UTL_Floodlight_TripodSurvivor_LG"), 300.f, 10, -3.f, 0.f, 6000.f),
			P(TEXT("COL-001"), TEXT("Campfire"), TEXT("SM_COL_Campfire_StoneRing_LG"), 150.f, 8, 0.f, 5.f, 800.f),
		};
	}

	/** Nightly horde size from Attraction (22.5), before the Bloom multiplier. */
	inline int32 HordeSize(float Attraction, bool bGreenMoon)
	{
		if (bGreenMoon)
		{
			return Attraction < 100.f ? 40 : Attraction < 300.f ? 90 : Attraction < 600.f ? 150 : 250;
		}
		const float T = FMath::FRand();
		if (Attraction < 100.f) return FMath::RoundToInt(FMath::Lerp(5.f, 15.f, T));
		if (Attraction < 300.f) return FMath::RoundToInt(FMath::Lerp(15.f, 40.f, T));
		if (Attraction < 600.f) return FMath::RoundToInt(FMath::Lerp(40.f, 80.f, T));
		return FMath::RoundToInt(FMath::Lerp(80.f, 150.f, T));
	}
}
