// Data-driven missions for the slice (Cold Open -> M1.02), loaded from Content/Exodus/Data/missions.json.
// Each step has an objective, actions run when it starts, and an event that completes it.
#pragma once

#include "CoreMinimal.h"
#include "Subsystems/WorldSubsystem.h"
#include "Dom/JsonObject.h"
#include "ExoMissionSubsystem.generated.h"

USTRUCT(BlueprintType)
struct FExoLine
{
	GENERATED_BODY()
	UPROPERTY(BlueprintReadOnly) FString Speaker;
	UPROPERTY(BlueprintReadOnly) FString Text;
	UPROPERTY(BlueprintReadOnly) float Seconds = 3.f;
};

struct FExoStep
{
	FString MissionId;
	FString MissionTitle;
	FString StepId;
	FString Objective;
	FString Event;      // trigger | interact | built | killed | night_survived | dialogue_done | time | none
	FString Target;     // marker / part id / story id; empty = any
	int32 Count = 1;
	float Seconds = 0.f;
	TArray<TSharedPtr<FJsonValue>> OnStart;
};

UCLASS()
class APEX_PROJECT_API UExoMissionSubsystem : public UWorldSubsystem
{
	GENERATED_BODY()

public:
	virtual void OnWorldBeginPlay(UWorld& InWorld) override;
	virtual void Deinitialize() override;

	/** Report something that happened; completes the current step if it matches. */
	UFUNCTION(BlueprintCallable, Category = "Exodus|Missions")
	void NotifyEvent(const FString& Event, const FString& Target);

	UFUNCTION(BlueprintCallable) void SkipDialogueLine();
	/** Jump to a step by id (debug console: ce ExoJump <StepId>, or the "start_step" launch option). */
	UFUNCTION(BlueprintCallable) void JumpToStep(const FString& StepId);

	FString GetObjective() const;
	FString GetMissionTitle() const;
	const FExoLine* GetCurrentLine() const { return Lines.Num() > 0 ? &Lines[0] : nullptr; }
	FString GetTitleCard() const { return TitleTime > 0.f ? TitleText : FString(); }
	FString GetFlag(const FString& Name) const { const FString* V = Flags.Find(Name); return V ? *V : FString(); }
	bool IsFinished() const { return StepIndex >= Steps.Num(); }

private:
	void Load();
	void Begin();
	void StartStep(int32 Index);
	void Advance();
	void RunAction(const TSharedPtr<FJsonObject>& A);
	void Tick();
	void Say(const FString& Speaker, const FString& Text);
	class AExoPlayerCharacter* GetPlayer() const;
	AActor* FindMarker(const FString& Name) const;

	TArray<FExoStep> Steps;
	int32 StepIndex = -1;
	int32 Progress = 0;
	float StepTime = 0.f;
	TArray<FExoLine> Lines;
	float LineTime = 0.f;
	bool bWaitingForDialogue = false;
	FString TitleText;
	float TitleTime = 0.f;
	TMap<FString, FString> Flags;
	FTimerHandle TickHandle;
};
