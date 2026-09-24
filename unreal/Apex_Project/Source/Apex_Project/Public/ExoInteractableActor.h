// Usable world objects in the slice: med cabinets, salvage, food and water, doors, radios,
// consoles (the Cold Open drill arm), and the school's fire alarm (M1.02).
#pragma once

#include "CoreMinimal.h"
#include "GameFramework/Actor.h"
#include "ExoInteractable.h"
#include "ExoInteractableActor.generated.h"

class UStaticMeshComponent;

UENUM(BlueprintType)
enum class EExoInteractKind : uint8
{
	Generic,     // just reports "interact" to the mission system
	MedCabinet,  // +1 Suppressant (M0.02)
	Salvage,     // +components
	Food,
	Water,
	Door,        // opens / closes (DOOR_ markers)
	FireAlarm,   // a 150 m noise that pulls Hollows toward it (M1.02 gym)
	Console,     // mission console (Cold Open drill, wrist-pad calls)
	Radio,
	Ladder       // stairs / ladder / lift between floors: moves the player to Destination
};

UCLASS()
class APEX_PROJECT_API AExoInteractableActor : public AActor, public IExoInteractable
{
	GENERATED_BODY()

public:
	AExoInteractableActor();

	UPROPERTY(VisibleAnywhere) TObjectPtr<UStaticMeshComponent> Mesh;
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Exodus") FName MarkerName;
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Exodus") EExoInteractKind Kind = EExoInteractKind::Generic;
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Exodus") FText Prompt;
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Exodus") int32 Amount = 1;
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Exodus") bool bOneShot = true;
	/** Mission group that enables this object; disabled objects can't be used. None = always enabled. */
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Exodus") FName Group;
	/** Door size in cm (width, depth, height) for DOOR_ markers. */
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Exodus") FVector DoorSize = FVector(120.f, 20.f, 220.f);
	/** Ladder destination (world, cm). */
	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Exodus") FVector Destination = FVector::ZeroVector;

	virtual void Interact(AExoPlayerCharacter* Player) override;
	virtual FText GetPrompt() const override;
	virtual bool CanInteract(const AExoPlayerCharacter* Player) const override { return bEnabled && !bUsed; }

	void SetEnabled(bool bOn) { bEnabled = bOn; }
	void ConfigureVisual();

protected:
	virtual void BeginPlay() override;

private:
	bool bEnabled = true;
	bool bUsed = false;
	bool bOpen = false;
	FVector ClosedLocation = FVector::ZeroVector;
};
