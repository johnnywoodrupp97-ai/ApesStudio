// Level markers placed by exodus_setup.py from the Blender level exports (.markers.json):
// player starts, checkpoints, cameras, POIs, landmarks. Missions find them by name.
#pragma once

#include "CoreMinimal.h"
#include "GameFramework/Actor.h"
#include "ExoMarker.generated.h"

class UBoxComponent;

UCLASS()
class APEX_PROJECT_API AExoMarker : public AActor
{
	GENERATED_BODY()

public:
	AExoMarker();
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Exodus") FName MarkerName;
	/** Marker prefix without the underscore: PS, CAM, POI, LM, SP, NAV... */
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Exodus") FString Kind;
};

/** TRG_ volumes: report "trigger" events to the mission system when the player enters. */
UCLASS()
class APEX_PROJECT_API AExoMissionTrigger : public AActor
{
	GENERATED_BODY()

public:
	AExoMissionTrigger();
	UPROPERTY(VisibleAnywhere) TObjectPtr<UBoxComponent> Box;
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Exodus") FName MarkerName;
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Exodus") bool bOnce = true;
	/** Half-size of the volume in cm (set by exodus_setup.py from the markers' volume sizes). */
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Exodus") FVector ExtentCm = FVector(200.f, 200.f, 150.f);

	virtual void OnConstruction(const FTransform& Transform) override;

protected:
	virtual void BeginPlay() override;

private:
	UFUNCTION() void OnBeginOverlap(UPrimitiveComponent* Overlapped, AActor* Other, UPrimitiveComponent* OtherComp, int32 BodyIndex, bool bFromSweep, const FHitResult& Sweep);
	bool bFired = false;
};

/** HS_ volumes: where night hordes may spawn (at least 60 m away and out of sight). */
UCLASS()
class APEX_PROJECT_API AExoHordeZone : public AActor
{
	GENERATED_BODY()

public:
	AExoHordeZone();
	UPROPERTY(VisibleAnywhere) TObjectPtr<UBoxComponent> Box;
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Exodus") FName MarkerName;
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Exodus") FVector ExtentCm = FVector(1000.f, 1000.f, 250.f);

	virtual void OnConstruction(const FTransform& Transform) override;
	FVector RandomPoint() const;
};
