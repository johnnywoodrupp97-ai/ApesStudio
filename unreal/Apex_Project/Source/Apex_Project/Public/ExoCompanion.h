// Story companions in the slice: Tug (M0.01-M1.01) and Lily (M1.02). They follow the player,
// bark lines, and Lily has survivor needs (game bible 07 / 22.4): the colony sim begins with her.
#pragma once

#include "CoreMinimal.h"
#include "GameFramework/Character.h"
#include "ExoCompanion.generated.h"

UCLASS()
class APEX_PROJECT_API AExoCompanion : public ACharacter
{
	GENERATED_BODY()

public:
	AExoCompanion();

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Exodus") FName CompanionId;
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Exodus") FName Group;
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Exodus") FString MeshAsset;
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Exodus") bool bFollow = false;
	/** Standing height (character bible): Tug 1.83 m, Lily 1.42 m. */
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Exodus") float HeightCm = 180.f;
	UPROPERTY(VisibleAnywhere) TObjectPtr<class UStaticMeshComponent> Stand;
	/** Idle / Talk / Walk / Jog / Sprint by speed and dialogue, plus Wave and HitReact (tools/blender/exodus_animations.py). */
	UPROPERTY(VisibleAnywhere) TObjectPtr<class UExoAnimComponent> Anim;
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Exodus") TArray<FString> Barks;
	/** Survivor needs, 0-100 (22.4: per in-game hour = 2.5 real minutes). */
	UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "Exodus") float Hunger = 80.f;
	UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "Exodus") float Rest = 80.f;
	UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "Exodus") float Safety = 50.f;

	void Activate();
	void Deactivate();
	bool IsActive() const { return bActive; }
	/** A bark the HUD shows under the companion (empty when silent). */
	FString GetCurrentBark() const { return BarkTime > 0.f ? CurrentBark : FString(); }
	/** True when the dialogue line on screen is this companion's (in person: not a radio, PA or vent line). */
	bool IsSpeaking(const FString& Speaker) const;

	virtual void Tick(float DeltaSeconds) override;

protected:
	virtual void BeginPlay() override;

private:
	bool bActive = true;
	float BarkClock = 20.f;
	float BarkTime = 0.f;
	FString CurrentBark;
	float MoveClock = 0.f;
};
