// Plays a character's greybox animation set (tools/blender/exodus_animations.py) on its skeletal mesh.
// The clips are imported by exodus_setup.py to /Game/Exodus/Imported/Animations/<mesh>/<clip>; their loop flags and
// ground speeds come from Content/Exodus/Data/animations.json. No Animation Blueprint: the mesh runs in single-node
// mode, the component picks Idle / Talk or the locomotion cycle closest to the actual speed and scales its play rate
// so the feet match the ground, and plays one-shots (Attack, HitReact, Wave, Death) on top.
#pragma once

#include "CoreMinimal.h"
#include "Components/ActorComponent.h"
#include "ExoAnimComponent.generated.h"

class UAnimSequence;
class USkeletalMeshComponent;

/** One clip of a character's set (from animations.json). */
struct FExoAnimClip
{
	TObjectPtr<UAnimSequence> Sequence = nullptr;
	bool bLoop = false;
	bool bLocomotion = false;
	float SpeedCmS = 0.f; // ground speed of an in-place locomotion cycle at play rate 1
};

UCLASS(ClassGroup = (Exodus), meta = (BlueprintSpawnableComponent))
class APEX_PROJECT_API UExoAnimComponent : public UActorComponent
{
	GENERATED_BODY()

public:
	UExoAnimComponent();

	/** Load the set for a skeletal mesh asset path, e.g. /Game/Exodus/Imported/Characters/SK_CHR_TugBrennan.
	 *  Returns false (and the character keeps its bind pose) when the clips were not imported. */
	bool Setup(USkeletalMeshComponent* InMesh, const FString& MeshAsset);
	bool HasClips() const { return Clips.Num() > 0; }
	bool HasClip(FName Name) const { return Clips.Contains(Name); }

	/** Play a clip once over the base state; looping clips (Wave) repeat for Seconds (0 = one cycle).
	 *  Returns false if the character has no such clip. */
	bool PlayOnce(FName Name, float Seconds = 0.f);
	/** Play Death and hold its last frame. */
	bool PlayDeath();

	/** Talk replaces Idle while standing (dialogue, barks). */
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Exodus") bool bTalking = false;

	virtual void TickComponent(float DeltaTime, ELevelTick TickType, FActorComponentTickFunction* ThisTickFunction) override;

private:
	const FExoAnimClip* Find(FName Name) const { return Clips.Find(Name); }
	void Play(FName Name, bool bLoop, float Rate);
	FName PickBase(float Speed, float& OutRate) const;

	UPROPERTY() TObjectPtr<USkeletalMeshComponent> Mesh;
	UPROPERTY() TArray<TObjectPtr<UAnimSequence>> Loaded; // keeps the sequences referenced
	TMap<FName, FExoAnimClip> Clips;
	FName Current;
	FName OneShot;
	float OneShotLeft = 0.f;
	bool bHold = false;
};
