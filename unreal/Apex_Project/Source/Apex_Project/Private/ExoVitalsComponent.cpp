#include "ExoVitalsComponent.h"

UExoVitalsComponent::UExoVitalsComponent()
{
	PrimaryComponentTick.bCanEverTick = true;
}

EExoInfectionStage UExoVitalsComponent::GetStage() const
{
	if (Infection >= ExoTuning::TurningThreshold) return EExoInfectionStage::Turning;
	if (Infection >= 60.f) return EExoInfectionStage::Blooming;
	if (Infection >= ExoTuning::SeededThreshold) return EExoInfectionStage::Seeded;
	if (Infection > 0.f) return EExoInfectionStage::Exposed;
	return EExoInfectionStage::Clean;
}

float UExoVitalsComponent::GetMaxStamina() const
{
	float Max = 100.f;
	if (GetStage() >= EExoInfectionStage::Seeded) Max *= 0.8f;
	if (Thirst <= 0.f) Max = FMath::Min(Max, 50.f);
	return Max;
}

void UExoVitalsComponent::TickComponent(float DeltaTime, ELevelTick TickType, FActorComponentTickFunction* ThisTickFunction)
{
	Super::TickComponent(DeltaTime, TickType, ThisTickFunction);
	if (bDead) return;

	// Stamina regenerates after a short pause.
	SecondsSinceStaminaUse += DeltaTime;
	if (SecondsSinceStaminaUse >= ExoTuning::StaminaRegenDelay)
	{
		Stamina = FMath::Min(GetMaxStamina(), Stamina + ExoTuning::StaminaRegenPerSec * DeltaTime);
	}
	Stamina = FMath::Min(Stamina, GetMaxStamina());

	if (!bSurvivalActive) return;

	const float Minutes = DeltaTime / 60.f;
	Hunger = FMath::Max(0.f, Hunger - ExoTuning::HungerDrainPerMin * Minutes * (bExerting ? 1.5f : 1.f));
	Thirst = FMath::Max(0.f, Thirst - ExoTuning::ThirstDrainPerMin * Minutes * (bExerting ? 2.f : 1.f));

	// Empty hunger: -1 HP / 10 s. Empty thirst: -1 HP / 8 s.
	StarveAccumulator += DeltaTime;
	if (Hunger <= 0.f && StarveAccumulator >= 10.f) { ApplyDamage(1.f); StarveAccumulator = 0.f; }
	if (Thirst <= 0.f && StarveAccumulator >= 8.f) { ApplyDamage(1.f); StarveAccumulator = 0.f; }

	// Infection: once Seeded it creeps up (player: +1% per 60 s) unless a Suppressant is active.
	if (SuppressionTimeLeft > 0.f)
	{
		SuppressionTimeLeft = FMath::Max(0.f, SuppressionTimeLeft - DeltaTime);
	}
	else if (Infection >= ExoTuning::SeededThreshold && Infection < 100.f)
	{
		InfectionAccumulator += DeltaTime;
		if (InfectionAccumulator >= ExoTuning::PlayerProgressSecondsPerPercent)
		{
			InfectionAccumulator = 0.f;
			AddInfection(1.f);
		}
	}

	// Blooming: no health regen. Otherwise slow regen when fed and watered.
	if (GetStage() < EExoInfectionStage::Blooming && Hunger > 20.f && Thirst > 20.f)
	{
		Health = FMath::Min(MaxHealth, Health + 0.5f * DeltaTime);
	}

	// Turning: a 60 s countdown to death, which a Suppressant can't stop once it has begun.
	if (GetStage() == EExoInfectionStage::Turning)
	{
		if (TurningTimeLeft < 0.f) TurningTimeLeft = ExoTuning::TurningCountdown;
		TurningTimeLeft -= DeltaTime;
		if (TurningTimeLeft <= 0.f) Die();
	}
	else
	{
		TurningTimeLeft = -1.f;
	}

	const EExoInfectionStage Stage = GetStage();
	if (Stage != LastStage)
	{
		LastStage = Stage;
		OnStageChanged.Broadcast(Stage);
	}
}

void UExoVitalsComponent::ApplyDamage(float Amount)
{
	if (bDead || Amount <= 0.f) return;
	Health = FMath::Max(0.f, Health - Amount);
	if (Health <= 0.f) Die();
}

void UExoVitalsComponent::AddInfection(float Percent)
{
	if (bDead) return;
	Infection = FMath::Clamp(Infection + Percent, 0.f, 100.f);
}

bool UExoVitalsComponent::UseSuppressant()
{
	if (Suppressants <= 0 || bDead) return false;
	--Suppressants;
	Infection = FMath::Max(0.f, Infection - ExoTuning::SuppressantAmount);
	SuppressionTimeLeft = ExoTuning::SuppressantHaltSeconds;
	return true;
}

bool UExoVitalsComponent::SpendStamina(float Amount)
{
	if (Stamina < Amount) return false;
	Stamina -= Amount;
	SecondsSinceStaminaUse = 0.f;
	return true;
}

void UExoVitalsComponent::ResetVitals()
{
	bDead = false;
	Health = MaxHealth;
	Stamina = 100.f;
	Hunger = FMath::Max(Hunger, 60.f);
	Thirst = FMath::Max(Thirst, 60.f);
	Infection = FMath::Min(Infection, 20.f);
	TurningTimeLeft = -1.f;
}

void UExoVitalsComponent::Die()
{
	if (bDead) return;
	bDead = true;
	Health = 0.f;
	OnDied.Broadcast();
}
