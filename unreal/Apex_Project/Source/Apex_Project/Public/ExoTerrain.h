// The slice's ground: a height grid (Content/Exodus/Data/slice_layout.json, written by the planner
// from the level bible's Kestrel Valley terrain) built as a procedural mesh with collision for
// walking, building and the navmesh.
#pragma once

#include "CoreMinimal.h"
#include "GameFramework/Actor.h"
#include "ExoTerrain.generated.h"

class UProceduralMeshComponent;
class UMaterialInterface;

UCLASS()
class APEX_PROJECT_API AExoTerrain : public AActor
{
	GENERATED_BODY()

public:
	AExoTerrain();

	UPROPERTY(VisibleAnywhere) TObjectPtr<UProceduralMeshComponent> Mesh;
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Exodus") TObjectPtr<UMaterialInterface> Material;
	/** Rebuild from the layout file (also runs in the editor when the actor is placed or moved). */
	UFUNCTION(CallInEditor, BlueprintCallable, Category = "Exodus") void Rebuild();

	virtual void OnConstruction(const FTransform& Transform) override;

protected:
	/** Rebuilt at play too, so collision never depends on serialized procedural-mesh state. */
	virtual void BeginPlay() override;
};
