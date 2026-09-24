// Health, stamina, hunger, thirst and the infection meter (game bible 05 and 22.2-22.3).
#pragma once

#include "CoreMinimal.h"
#include "Components/ActorComponent.h"
#include "ExoTypes.h"
#include "ExoVitalsComponent.generated.h"

DECLARE_DYNAMIC_MULTICAST_DELEGATE(FExoOnDied);
DECLARE_DYNAMIC_MULTICAST_DELEGATE_OneParam(FExoOnStageChanged, EExoInfectionStage, NewStage);

UCLASS(ClassGroup = (Exodus), meta = (BlueprintSpawnableComponent))
class APEX_PROJECT_API UExoVitalsComponent : public UActorComponent
{
	GENERATED_BODY()

public:
	UExoVitalsComponent();

	UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "Vitals") float Health = 100.f;
	UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "Vitals") float MaxHealth = 100.f;
	UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "Vitals") float Stamina = 100.f;
	UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "Vitals") float Hunger = 100.f;
	UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "Vitals") float Thirst = 100.f;
	UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "Vitals") float Infection = 0.f;
	UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "Vitals") int32 Suppressants = 0;
	/** Drain vitals over time (off during the Cold Open and cutscenes). */
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Vitals") bool bSurvivalActive = true;

	UPROPERTY(BlueprintAssignable) FExoOnDied OnDied;
	UPROPERTY(BlueprintAssignable) FExoOnStageChanged OnStageChanged;

	virtual void TickComponent(float DeltaTime, ELevelTick TickType, FActorComponentTickFunction* ThisTickFunction) override;

	UFUNCTION(BlueprintCallable) void ApplyDamage(float Amount);
	UFUNCTION(BlueprintCallable) void AddInfection(float Percent);
	UFUNCTION(BlueprintCallable) bool UseSuppressant();
	UFUNCTION(BlueprintCallable) bool SpendStamina(float Amount);
	UFUNCTION(BlueprintCallable) void Eat(float Amount) { Hunger = FMath::Min(100.f, Hunger + Amount); }
	UFUNCTION(BlueprintCallable) void Drink(float Amount) { Thirst = FMath::Min(100.f, Thirst + Amount); }
	UFUNCTION(BlueprintCallable) void ResetVitals();

	UFUNCTION(BlueprintPure) EExoInfectionStage GetStage() const;
	UFUNCTION(BlueprintPure) bool IsDead() const { return bDead; }
	UFUNCTION(BlueprintPure) float GetTurningTimeLeft() const { return TurningTimeLeft; }
	UFUNCTION(BlueprintPure) float GetSuppressionTimeLeft() const { return SuppressionTimeLeft; }
	/** Stamina ceiling: Seeded costs 20% (05), an empty thirst bar caps at 50% (22.2). */
	UFUNCTION(BlueprintPure) float GetMaxStamina() const;

	/** Set by the owner while sprinting / exerting (drains ×1.5 hunger, ×2 thirst in heat). */
	bool bExerting = false;

private:
	void Die();

	bool bDead = false;
	float SecondsSinceStaminaUse = 0.f;
	float InfectionAccumulator = 0.f;
	float StarveAccumulator = 0.f;
	float SuppressionTimeLeft = 0.f;
	float TurningTimeLeft = -1.f;
	EExoInfectionStage LastStage = EExoInfectionStage::Clean;
};
