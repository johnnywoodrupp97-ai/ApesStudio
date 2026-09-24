// Hollow brain: wander, investigate noises, chase what it sees within 15 m, and break through
// player blocks that stand in the way (level bible 12).
#pragma once

#include "CoreMinimal.h"
#include "AIController.h"
#include "ExoHollowAI.generated.h"

class AExoHollow;

UENUM()
enum class EExoHollowState : uint8 { Idle, Wander, Investigate, Chase, Siege };

UCLASS()
class APEX_PROJECT_API AExoHollowAI : public AAIController
{
	GENERATED_BODY()

public:
	AExoHollowAI();

	virtual void Tick(float DeltaSeconds) override;
	/** Something hurt us or shouted: go and look. */
	void Alert(const FVector& Where);
	EExoHollowState GetState() const { return State; }

protected:
	virtual void OnPossess(APawn* InPawn) override;

private:
	bool CanSeePlayer(APawn*& OutPlayer) const;
	class AExoBlock* FindBlockingBlock() const;
	void Think();

	EExoHollowState State = EExoHollowState::Wander;
	FVector Home = FVector::ZeroVector;
	FVector Goal = FVector::ZeroVector;
	float ThinkClock = 0.f;
	float WanderClock = 0.f;
	float StuckTime = 0.f;
	float LoseSightTime = 0.f;
	TWeakObjectPtr<AActor> Target;
};
