// The Engineer ("Wrench"): first-person survivor with Ada's wrench, the multitool (build mode) and a helmet light.
// Controls follow game bible 21.3; the input actions are created in code, so no input assets are needed.
#pragma once

#include "CoreMinimal.h"
#include "GameFramework/Character.h"
#include "InputActionValue.h"
#include "ExoPlayerCharacter.generated.h"

class UCameraComponent;
class USpotLightComponent;
class UExoVitalsComponent;
class UExoBuildComponent;
class UInputAction;
class UInputMappingContext;

UCLASS()
class APEX_PROJECT_API AExoPlayerCharacter : public ACharacter
{
	GENERATED_BODY()

public:
	AExoPlayerCharacter();

	UPROPERTY(VisibleAnywhere, BlueprintReadOnly) TObjectPtr<UCameraComponent> Camera;
	UPROPERTY(VisibleAnywhere, BlueprintReadOnly) TObjectPtr<USpotLightComponent> HelmetLight;
	UPROPERTY(VisibleAnywhere, BlueprintReadOnly) TObjectPtr<UExoVitalsComponent> Vitals;
	UPROPERTY(VisibleAnywhere, BlueprintReadOnly) TObjectPtr<UExoBuildComponent> Build;

	/** Salvage components for building (parts bible recipes, summed). */
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Exodus") int32 Components = 60;
	/** False during scripted moments (Cold Open console, dialogue locks). */
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Exodus") bool bInputEnabled = true;

	virtual void Tick(float DeltaSeconds) override;
	virtual void SetupPlayerInputComponent(UInputComponent* PlayerInputComponent) override;
	virtual float TakeDamage(float Damage, const FDamageEvent& DamageEvent, AController* EventInstigator, AActor* DamageCauser) override;

	/** What the crosshair is on (interactable actor), and its prompt for the HUD. */
	UFUNCTION(BlueprintPure) AActor* GetFocusActor() const { return FocusActor.Get(); }
	FText GetFocusPrompt() const;
	bool IsSprinting() const { return bSprinting; }
	bool IsCrouchingNow() const { return bIsCrouched; }

	/** Line trace from the camera. */
	bool TraceView(float DistanceCm, FHitResult& OutHit) const;

protected:
	virtual void BeginPlay() override;

private:
	void CreateInput();
	UInputAction* MakeAction(FName Name, bool bAxis2D);

	void Move(const FInputActionValue& Value);
	void Look(const FInputActionValue& Value);
	void StartSprint(const FInputActionValue& Value);
	void StopSprint(const FInputActionValue& Value);
	void ToggleCrouch(const FInputActionValue& Value);
	void DoJump(const FInputActionValue& Value);
	void Primary(const FInputActionValue& Value);
	void PrimaryReleased(const FInputActionValue& Value);
	void Secondary(const FInputActionValue& Value);
	void SecondaryReleased(const FInputActionValue& Value);
	void Interact(const FInputActionValue& Value);
	void ToggleBuild(const FInputActionValue& Value);
	void RotatePart(const FInputActionValue& Value);
	void CyclePart(const FInputActionValue& Value);
	void ToggleLight(const FInputActionValue& Value);
	void UseSuppressant(const FInputActionValue& Value);
	void SkipLine(const FInputActionValue& Value);

	UFUNCTION() void OnVitalsDied();
	void SwingWrench();
	void UpdateFocus();
	void EmitMovementNoise(float DeltaSeconds);

	UPROPERTY() TObjectPtr<UInputMappingContext> Mapping;
	UPROPERTY() TArray<TObjectPtr<UInputAction>> Actions;

	TWeakObjectPtr<AActor> FocusActor;
	bool bSprinting = false;
	bool bPrimaryHeld = false;
	bool bSecondaryHeld = false;
	float WrenchCooldown = 0.f;
	float NoiseClock = 0.f;
};
