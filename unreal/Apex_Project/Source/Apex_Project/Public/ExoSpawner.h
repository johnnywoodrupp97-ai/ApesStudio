// SP_ markers: spawn one or more Hollows, at level start or when a mission activates their group.
#pragma once

#include "CoreMinimal.h"
#include "GameFramework/Actor.h"
#include "ExoTypes.h"
#include "ExoSpawner.generated.h"

class AExoHollow;

UCLASS()
class APEX_PROJECT_API AExoSpawner : public AActor
{
	GENERATED_BODY()

public:
	AExoSpawner();

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Exodus") FName MarkerName;
	/** Mission group that activates this spawner (e.g. M0_02). None = spawn at level start. */
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Exodus") FName Group;
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Exodus") EExoHollowType HollowType = EExoHollowType::Shambler;
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Exodus") int32 Count = 1;
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Exodus") float RadiusCm = 300.f;
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Exodus") FString MeshAsset;
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Exodus") FName StoryId;

	UFUNCTION(BlueprintCallable) void Spawn();

	/** Shared spawn helper (also used by the horde director). */
	static AExoHollow* SpawnHollow(UWorld* World, const FVector& Where, EExoHollowType Type, const FString& Mesh, FName StoryId, bool bHorde);

protected:
	virtual void BeginPlay() override;

private:
	bool bSpawned = false;
};
