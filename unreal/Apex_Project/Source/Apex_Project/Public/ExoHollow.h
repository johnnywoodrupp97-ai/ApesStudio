// A Hollow (game bible 09): Shambler, Runner or Crawler, with stats from game bible 22.6.
#pragma once

#include "CoreMinimal.h"
#include "GameFramework/Character.h"
#include "ExoTypes.h"
#include "ExoHollow.generated.h"

class UStaticMeshComponent;
class UExoAnimComponent;

UCLASS()
class APEX_PROJECT_API AExoHollow : public ACharacter
{
	GENERATED_BODY()

public:
	AExoHollow();

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Exodus") EExoHollowType HollowType = EExoHollowType::Shambler;
	/** Skeletal mesh imported by exodus_setup.py, e.g. /Game/Exodus/Imported/Characters/SK_ENM_Shambler. */
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Exodus") FString MeshAsset;
	/** Story Hollows keep a name for missions (Dana Marsh, Ms. Alvarez). */
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Exodus") FName StoryId;
	/** Horde members head for the player's base instead of wandering. */
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Exodus") bool bHorde = false;

	UPROPERTY(VisibleAnywhere) TObjectPtr<UStaticMeshComponent> Stand;
	/** Idle / Walk / Run by speed, plus Attack, HitReact and Death (tools/blender/exodus_animations.py). */
	UPROPERTY(VisibleAnywhere) TObjectPtr<UExoAnimComponent> Anim;

	/** Apply type stats, speed and visuals (call after setting HollowType / MeshAsset). */
	void ApplyType();
	/** Melee attack on the player or a block within reach; returns true if it struck. */
	bool TryAttack(AActor* Target);
	bool IsDead() const { return bDead; }
	const FExoHollowStats& GetStats() const { return Stats; }

	virtual void Tick(float DeltaSeconds) override;
	virtual float TakeDamage(float Damage, const FDamageEvent& DamageEvent, AController* EventInstigator, AActor* DamageCauser) override;

protected:
	virtual void BeginPlay() override;

private:
	void Die();

	FExoHollowStats Stats;
	float Health = 100.f;
	float AttackCooldown = 0.f;
	bool bDead = false;
	float MoanClock = 0.f;
};
