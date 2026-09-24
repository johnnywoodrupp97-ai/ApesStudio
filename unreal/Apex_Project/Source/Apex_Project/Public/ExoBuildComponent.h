// Multitool build mode (game bible 06 / 21): pick a part, see a ghost snapped to the 2.5 m grid,
// place a frame (costs components), then hold Primary to weld it up or Secondary to grind it down.
#pragma once

#include "CoreMinimal.h"
#include "Components/ActorComponent.h"
#include "ExoTypes.h"
#include "ExoBuildComponent.generated.h"

class AExoBlock;
class AExoPlayerCharacter;

UCLASS(ClassGroup = (Exodus), meta = (BlueprintSpawnableComponent))
class APEX_PROJECT_API UExoBuildComponent : public UActorComponent
{
	GENERATED_BODY()

public:
	UExoBuildComponent();

	/** Weld rate: fraction of a block per second (a 1-cell block welds in ~3 s). */
	UPROPERTY(EditAnywhere, Category = "Exodus") float WeldRate = 0.35f;
	UPROPERTY(EditAnywhere, Category = "Exodus") float GrindRate = 0.6f;
	UPROPERTY(EditAnywhere, Category = "Exodus") float ReachCm = 900.f;

	virtual void BeginPlay() override;
	virtual void TickComponent(float DeltaTime, ELevelTick TickType, FActorComponentTickFunction* ThisTickFunction) override;

	bool IsBuildMode() const { return bBuildMode; }
	void SetBuildMode(bool bOn);
	void CyclePart(int32 Dir);
	void RotateGhost();
	/** Place the ghost as a frame, or start welding the block under the crosshair. */
	void PrimaryPressed();
	void Weld(float DeltaSeconds);
	void Grind(float DeltaSeconds);

	const FExoPartDef& GetSelectedPart() const { return Parts[SelectedIndex]; }
	AActor* GetGhost() const;
	/** Block under the crosshair (for welding / grinding / the HUD). */
	AExoBlock* GetTargetBlock() const;

	UPROPERTY() TArray<FExoPartDef> Parts;

private:
	AExoPlayerCharacter* GetPlayer() const;
	void RespawnGhost();
	bool ComputePlacement(FTransform& OutTransform) const;

	UPROPERTY() TObjectPtr<AExoBlock> Ghost;
	bool bBuildMode = false;
	int32 SelectedIndex = 0;
	float YawSteps = 0.f;
	float NoiseClock = 0.f;
	float GrindCarry = 0.f;
};
