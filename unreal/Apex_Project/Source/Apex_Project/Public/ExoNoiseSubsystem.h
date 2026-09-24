// World noise events. Hollows are nearly blind (15 m) and hunt by sound (5-40 m, level bible 12);
// gunfire and machines also feed a base's Attraction score (game bible 22.5).
#pragma once

#include "CoreMinimal.h"
#include "Subsystems/WorldSubsystem.h"
#include "ExoNoiseSubsystem.generated.h"

USTRUCT(BlueprintType)
struct FExoNoise
{
	GENERATED_BODY()

	UPROPERTY(BlueprintReadOnly) FVector Location = FVector::ZeroVector;
	UPROPERTY(BlueprintReadOnly) float RadiusCm = 0.f;
	UPROPERTY(BlueprintReadOnly) float Time = 0.f;
	UPROPERTY(BlueprintReadOnly) TWeakObjectPtr<AActor> Instigator;
	UPROPERTY(BlueprintReadOnly) FName Tag;
};

UCLASS()
class APEX_PROJECT_API UExoNoiseSubsystem : public UWorldSubsystem
{
	GENERATED_BODY()

public:
	/** Report a sound heard up to RadiusMeters away (walk 5, sprint 15, gunfire 40, fire alarm 150). */
	UFUNCTION(BlueprintCallable, Category = "Exodus|Noise")
	void ReportNoise(FVector Location, float RadiusMeters, AActor* Instigator, FName Tag = NAME_None);

	/** Loudest recent noise audible at Listener (within its radius, in the last MaxAgeSeconds). */
	bool FindAudibleNoise(const FVector& Listener, float MaxAgeSeconds, FExoNoise& OutNoise) const;

	/** Gunfire events in the last in-game hour (2.5 real minutes), for Attraction. */
	int32 CountRecent(FName Tag, float WindowSeconds) const;

private:
	TArray<FExoNoise> Noises;
};
