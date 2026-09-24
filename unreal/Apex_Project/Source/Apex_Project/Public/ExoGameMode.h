// Slice rules: the 60-minute day (40 day / 20 night, game bible 22.1), nightly hordes sized by the
// base's Attraction (22.5), a Green Moon every third night, checkpoints and respawn.
#pragma once

#include "CoreMinimal.h"
#include "GameFramework/GameModeBase.h"
#include "ExoGameMode.generated.h"

class AExoPlayerCharacter;

UCLASS()
class APEX_PROJECT_API AExoGameMode : public AGameModeBase
{
	GENERATED_BODY()

public:
	AExoGameMode();

	/** Seconds into the 60-minute day; 0 = midnight. */
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Exodus") float TimeOfDay = 2250.f; // 21:00, Night Zero (M0.01 is 21:40)
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Exodus") float TimeScale = 1.f;
	/** Hordes only roam after the prologue (the mission turns them on in M1.01). */
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Exodus") bool bHordesEnabled = false;
	/** Region Bloom level 1-5 (Kestrel Complex/Township: 2) scales horde size x0.5..x2.0. */
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Exodus") int32 BloomLevel = 2;
	/** Full-AI Hollow cap (game bible 13.7: 60 on PC); extra horde members are skipped in the prototype. */
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Exodus") int32 MaxActiveHollows = 60;

	virtual void Tick(float DeltaSeconds) override;
	virtual void StartPlay() override;

	float GetHour() const { return TimeOfDay / 150.f; }
	bool IsNight() const;
	bool IsGreenMoon() const { return bGreenMoonTonight && IsNight(); }
	int32 GetNightIndex() const { return NightIndex; }
	float GetAttraction() const;

	void SetHour(float Hour);
	void SetCheckpoint(AActor* Marker);
	void HandlePlayerDeath(AExoPlayerCharacter* Player);
	/** Spawn a horde now (Count <= 0: size it from Attraction). Returns how many spawned. */
	int32 SpawnHorde(int32 Count);

	// Debug console (~): ExoJump M1_02_school, ExoTime 19.5, ExoHorde 20, ExoGive 100
	UFUNCTION(Exec) void ExoJump(const FString& StepId);
	UFUNCTION(Exec) void ExoTime(float Hour);
	UFUNCTION(Exec) void ExoHorde(int32 Count);
	UFUNCTION(Exec) void ExoGive(int32 ComponentsCount);

private:
	void UpdateSun();
	void Respawn();

	TWeakObjectPtr<AActor> Checkpoint;
	TWeakObjectPtr<AExoPlayerCharacter> DeadPlayer;
	FTimerHandle RespawnHandle;
	int32 NightIndex = 0;
	bool bWasNight = false;
	bool bGreenMoonTonight = false;
	bool bSunInitialised = false;
};
