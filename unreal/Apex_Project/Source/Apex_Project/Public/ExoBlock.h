// A player-built block (parts bible). Placed as a frame, welded up to 100% to become functional,
// ground down for salvage, and damaged by Hollows (Brutes and hordes target blocks, game bible 09).
#pragma once

#include "CoreMinimal.h"
#include "GameFramework/Actor.h"
#include "ExoTypes.h"
#include "ExoBlock.generated.h"

class UStaticMeshComponent;
class UPointLightComponent;

UCLASS()
class APEX_PROJECT_API AExoBlock : public AActor
{
	GENERATED_BODY()

public:
	AExoBlock();

	UPROPERTY(VisibleAnywhere, BlueprintReadOnly) TObjectPtr<USceneComponent> Root;
	UPROPERTY(VisibleAnywhere, BlueprintReadOnly) TObjectPtr<UStaticMeshComponent> Mesh;
	UPROPERTY(VisibleAnywhere, BlueprintReadOnly) TObjectPtr<UPointLightComponent> Light;

	UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "Exodus") FExoPartDef Part;
	/** 0 = frame just placed, 1 = fully welded and functional. */
	UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "Exodus") float BuildProgress = 0.05f;
	UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "Exodus") float Health = 100.f;
	UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "Exodus") bool bGhost = false;

	/** Configure mesh, health and functions from a part definition. */
	void InitPart(const FExoPartDef& InPart, bool bAsGhost);
	/** Add weld progress; returns true the moment the block becomes complete. */
	bool AddProgress(float Delta);
	bool IsComplete() const { return BuildProgress >= 1.f; }
	/** Contribution to the base's Attraction score (22.5). */
	float GetAttraction() const;

	virtual float TakeDamage(float Damage, const FDamageEvent& DamageEvent, AController* EventInstigator, AActor* DamageCauser) override;
	virtual void Tick(float DeltaSeconds) override;

	/** Placeholder mesh (engine cube) used until the part's FBX is imported. */
	static UStaticMesh* LoadPartMesh(const FString& Asset);

private:
	void RefreshVisual();
	float HumClock = 0.f;
	FVector BaseScale = FVector::OneVector;
	float HalfHeight = 125.f;
};
