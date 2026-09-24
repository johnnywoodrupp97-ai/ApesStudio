#include "ExoMissionSubsystem.h"
#include "Apex_Project.h"
#include "ExoMarker.h"
#include "ExoSpawner.h"
#include "ExoCompanion.h"
#include "ExoInteractableActor.h"
#include "ExoPlayerCharacter.h"
#include "ExoVitalsComponent.h"
#include "ExoGameMode.h"
#include "EngineUtils.h"
#include "Engine/World.h"
#include "TimerManager.h"
#include "Kismet/GameplayStatics.h"
#include "Misc/FileHelper.h"
#include "Misc/Paths.h"
#include "Misc/CommandLine.h"
#include "Serialization/JsonReader.h"
#include "Serialization/JsonSerializer.h"

static constexpr float MissionTickSeconds = 0.1f;

void UExoMissionSubsystem::OnWorldBeginPlay(UWorld& InWorld)
{
	Super::OnWorldBeginPlay(InWorld);
	if (!InWorld.IsGameWorld()) return;
	Load();
	InWorld.GetTimerManager().SetTimer(TickHandle, FTimerDelegate::CreateUObject(this, &UExoMissionSubsystem::Tick), MissionTickSeconds, true);

	// Start once the player pawn exists (a short delay after BeginPlay).
	FTimerHandle StartHandle;
	InWorld.GetTimerManager().SetTimer(StartHandle, FTimerDelegate::CreateUObject(this, &UExoMissionSubsystem::Begin), 0.5f, false);
}

void UExoMissionSubsystem::Begin()
{
	// -ExoStep=<step id> starts the slice at any step (testing and playtest checkpoints).
	FString Start;
	if (FParse::Value(FCommandLine::Get(), TEXT("ExoStep="), Start))
	{
		JumpToStep(Start);
	}
	else
	{
		StartStep(0);
	}
}

void UExoMissionSubsystem::Deinitialize()
{
	if (UWorld* W = GetWorld()) W->GetTimerManager().ClearTimer(TickHandle);
	Super::Deinitialize();
}

void UExoMissionSubsystem::Load()
{
	Steps.Reset();
	const FString Path = FPaths::ProjectContentDir() / TEXT("Exodus/Data/missions.json");
	FString Text;
	if (!FFileHelper::LoadFileToString(Text, *Path))
	{
		UE_LOG(LogExodus, Error, TEXT("Missing %s"), *Path);
		return;
	}
	TSharedPtr<FJsonObject> Root;
	if (!FJsonSerializer::Deserialize(TJsonReaderFactory<>::Create(Text), Root) || !Root.IsValid())
	{
		UE_LOG(LogExodus, Error, TEXT("Could not parse %s"), *Path);
		return;
	}
	for (const TSharedPtr<FJsonValue>& MV : Root->GetArrayField(TEXT("missions")))
	{
		const TSharedPtr<FJsonObject> M = MV->AsObject();
		for (const TSharedPtr<FJsonValue>& SV : M->GetArrayField(TEXT("steps")))
		{
			const TSharedPtr<FJsonObject> S = SV->AsObject();
			FExoStep Step;
			Step.MissionId = M->GetStringField(TEXT("id"));
			Step.MissionTitle = M->GetStringField(TEXT("title"));
			Step.StepId = S->GetStringField(TEXT("id"));
			S->TryGetStringField(TEXT("objective"), Step.Objective);
			const TSharedPtr<FJsonObject>* Done = nullptr;
			if (S->TryGetObjectField(TEXT("complete"), Done))
			{
				(*Done)->TryGetStringField(TEXT("event"), Step.Event);
				(*Done)->TryGetStringField(TEXT("target"), Step.Target);
				double Num = 0.0;
				if ((*Done)->TryGetNumberField(TEXT("count"), Num)) Step.Count = FMath::Max(1, (int32)Num);
				if ((*Done)->TryGetNumberField(TEXT("seconds"), Num)) Step.Seconds = (float)Num;
			}
			const TArray<TSharedPtr<FJsonValue>>* Actions = nullptr;
			if (S->TryGetArrayField(TEXT("on_start"), Actions)) Step.OnStart = *Actions;
			Steps.Add(Step);
		}
	}
	UE_LOG(LogExodus, Log, TEXT("Loaded %d mission steps"), Steps.Num());
}

AExoPlayerCharacter* UExoMissionSubsystem::GetPlayer() const
{
	return Cast<AExoPlayerCharacter>(UGameplayStatics::GetPlayerPawn(GetWorld(), 0));
}

AActor* UExoMissionSubsystem::FindMarker(const FString& Name) const
{
	const FName Key(*Name);
	for (TActorIterator<AExoMarker> It(GetWorld()); It; ++It)
	{
		if (It->MarkerName == Key) return *It;
	}
	for (TActorIterator<AExoMissionTrigger> It(GetWorld()); It; ++It)
	{
		if (It->MarkerName == Key) return *It;
	}
	return nullptr;
}

void UExoMissionSubsystem::StartStep(int32 Index)
{
	StepIndex = Index;
	Progress = 0;
	StepTime = 0.f;
	bWaitingForDialogue = false;
	if (!Steps.IsValidIndex(Index))
	{
		TitleText = TEXT("END OF THE VERTICAL SLICE");
		TitleTime = 12.f;
		return;
	}
	UE_LOG(LogExodus, Log, TEXT("Mission step %s / %s"), *Steps[Index].MissionId, *Steps[Index].StepId);
	for (const TSharedPtr<FJsonValue>& V : Steps[Index].OnStart)
	{
		RunAction(V->AsObject());
	}
	if (Steps[Index].Event == TEXT("dialogue_done")) bWaitingForDialogue = true;
	if (Steps[Index].Event == TEXT("none") || Steps[Index].Event.IsEmpty()) Advance();
}

void UExoMissionSubsystem::Advance()
{
	StartStep(StepIndex + 1);
}

void UExoMissionSubsystem::JumpToStep(const FString& StepId)
{
	for (int32 i = 0; i < Steps.Num(); ++i)
	{
		if (Steps[i].StepId == StepId)
		{
			// Replay the setup actions of every earlier step without their dialogue, so the world is consistent.
			for (int32 j = 0; j < i; ++j)
			{
				for (const TSharedPtr<FJsonValue>& V : Steps[j].OnStart)
				{
					const TSharedPtr<FJsonObject> A = V->AsObject();
					const FString Do = A->GetStringField(TEXT("do"));
					if (Do != TEXT("say") && Do != TEXT("title") && Do != TEXT("horde")) RunAction(A);
				}
			}
			Lines.Reset();
			StartStep(i);
			return;
		}
	}
	UE_LOG(LogExodus, Warning, TEXT("No mission step %s"), *StepId);
	StartStep(0);
}

void UExoMissionSubsystem::Say(const FString& Speaker, const FString& Text)
{
	FExoLine L;
	L.Speaker = Speaker;
	L.Text = Text;
	L.Seconds = 1.6f + 0.055f * Text.Len();
	Lines.Add(L);
}

void UExoMissionSubsystem::RunAction(const TSharedPtr<FJsonObject>& A)
{
	if (!A.IsValid()) return;
	const FString Do = A->GetStringField(TEXT("do"));
	AExoPlayerCharacter* Player = GetPlayer();
	AExoGameMode* GM = GetWorld()->GetAuthGameMode<AExoGameMode>();
	FString S;
	double N = 0.0;
	bool B = false;

	if (Do == TEXT("say"))
	{
		for (const TSharedPtr<FJsonValue>& LV : A->GetArrayField(TEXT("lines")))
		{
			const TArray<TSharedPtr<FJsonValue>>& Pair = LV->AsArray();
			if (Pair.Num() >= 2) Say(Pair[0]->AsString(), Pair[1]->AsString());
		}
	}
	else if (Do == TEXT("teleport") && Player && A->TryGetStringField(TEXT("marker"), S))
	{
		if (AActor* M = FindMarker(S))
		{
			Player->TeleportTo(M->GetActorLocation() + FVector(0.f, 0.f, 100.f), M->GetActorRotation());
			if (AController* C = Player->GetController()) C->SetControlRotation(FRotator(0.f, M->GetActorRotation().Yaw, 0.f));
		}
		else UE_LOG(LogExodus, Warning, TEXT("teleport: no marker %s"), *S);
	}
	else if (Do == TEXT("checkpoint") && GM && A->TryGetStringField(TEXT("marker"), S))
	{
		GM->SetCheckpoint(FindMarker(S));
	}
	else if (Do == TEXT("activate") && A->TryGetStringField(TEXT("group"), S))
	{
		const FName Group(*S);
		for (TActorIterator<AExoSpawner> It(GetWorld()); It; ++It) if (It->Group == Group) It->Spawn();
		for (TActorIterator<AExoCompanion> It(GetWorld()); It; ++It) if (It->Group == Group) It->Activate();
		for (TActorIterator<AExoInteractableActor> It(GetWorld()); It; ++It) if (It->Group == Group) It->SetEnabled(true);
	}
	else if (Do == TEXT("give") && Player && A->TryGetStringField(TEXT("item"), S))
	{
		const int32 Count = A->TryGetNumberField(TEXT("count"), N) ? (int32)N : 1;
		if (S == TEXT("suppressant")) Player->Vitals->Suppressants += Count;
		else if (S == TEXT("components")) Player->Components += Count;
		else if (S == TEXT("food")) Player->Vitals->Eat(40.f * Count);
		else if (S == TEXT("water")) Player->Vitals->Drink(40.f * Count);
	}
	else if (Do == TEXT("survival") && Player && A->TryGetBoolField(TEXT("on"), B))
	{
		Player->Vitals->bSurvivalActive = B;
	}
	else if (Do == TEXT("input") && Player && A->TryGetBoolField(TEXT("on"), B))
	{
		Player->bInputEnabled = B;
	}
	else if (Do == TEXT("follow") && A->TryGetStringField(TEXT("companion"), S))
	{
		A->TryGetBoolField(TEXT("on"), B);
		for (TActorIterator<AExoCompanion> It(GetWorld()); It; ++It)
		{
			if (It->CompanionId == FName(*S)) { It->Activate(); It->bFollow = B; }
		}
	}
	else if (Do == TEXT("place") && A->TryGetStringField(TEXT("companion"), S))
	{
		// Move a companion to a marker (story staging: Tug pinned in the cage, Lily at the campfire).
		FString MarkerName;
		AActor* M = A->TryGetStringField(TEXT("marker"), MarkerName) ? FindMarker(MarkerName) : nullptr;
		if (!M) UE_LOG(LogExodus, Warning, TEXT("place: no marker %s"), *MarkerName);
		const bool bHasFollow = A->TryGetBoolField(TEXT("follow"), B);
		for (TActorIterator<AExoCompanion> It(GetWorld()); It; ++It)
		{
			if (It->CompanionId != FName(*S)) continue;
			It->Activate();
			if (M) It->TeleportTo(M->GetActorLocation() + FVector(0.f, 0.f, It->HeightCm * 0.5f + 5.f), M->GetActorRotation());
			if (bHasFollow) It->bFollow = B;
		}
	}
	else if (Do == TEXT("infect") && Player && A->TryGetNumberField(TEXT("percent"), N))
	{
		Player->Vitals->AddInfection((float)N);
	}
	else if (Do == TEXT("time") && GM)
	{
		if (A->TryGetNumberField(TEXT("hour"), N)) GM->SetHour((float)N);
		if (A->TryGetNumberField(TEXT("scale"), N)) GM->TimeScale = (float)N;
	}
	else if (Do == TEXT("hordes") && GM && A->TryGetBoolField(TEXT("on"), B))
	{
		GM->bHordesEnabled = B;
	}
	else if (Do == TEXT("horde") && GM)
	{
		const int32 Count = A->TryGetNumberField(TEXT("count"), N) ? (int32)N : 0;
		GM->SpawnHorde(Count);
	}
	else if (Do == TEXT("title") && A->TryGetStringField(TEXT("text"), S))
	{
		TitleText = S;
		TitleTime = A->TryGetNumberField(TEXT("seconds"), N) ? (float)N : 5.f;
	}
	else if (Do == TEXT("flag") && A->TryGetStringField(TEXT("name"), S))
	{
		FString Value;
		A->TryGetStringField(TEXT("value"), Value);
		Flags.Add(S, Value);
	}
	else if (Do == TEXT("hide") && A->TryGetStringField(TEXT("group"), S))
	{
		for (TActorIterator<AExoCompanion> It(GetWorld()); It; ++It) if (It->Group == FName(*S)) It->Deactivate();
	}
	else
	{
		UE_LOG(LogExodus, Warning, TEXT("Unknown or incomplete mission action '%s'"), *Do);
	}
}

void UExoMissionSubsystem::NotifyEvent(const FString& Event, const FString& Target)
{
	if (!Steps.IsValidIndex(StepIndex)) return;
	const FExoStep& Step = Steps[StepIndex];
	if (Step.Event != Event) return;
	if (!Step.Target.IsEmpty() && !Step.Target.Equals(Target, ESearchCase::IgnoreCase)) return;
	if (++Progress >= Step.Count) Advance();
}

void UExoMissionSubsystem::SkipDialogueLine()
{
	if (Lines.Num() > 0) { Lines.RemoveAt(0); LineTime = 0.f; }
}

void UExoMissionSubsystem::Tick()
{
	const float Dt = MissionTickSeconds;
	StepTime += Dt;
	TitleTime = FMath::Max(0.f, TitleTime - Dt);
	if (Lines.Num() > 0)
	{
		LineTime += Dt;
		if (LineTime >= Lines[0].Seconds) { Lines.RemoveAt(0); LineTime = 0.f; }
	}
	if (!Steps.IsValidIndex(StepIndex)) return;
	const FExoStep& Step = Steps[StepIndex];
	if (Step.Event == TEXT("time") && StepTime >= Step.Seconds) Advance();
	else if (bWaitingForDialogue && Lines.Num() == 0 && StepTime > 0.2f) Advance();
}

FString UExoMissionSubsystem::GetObjective() const
{
	return Steps.IsValidIndex(StepIndex) ? Steps[StepIndex].Objective : FString();
}

FString UExoMissionSubsystem::GetMissionTitle() const
{
	return Steps.IsValidIndex(StepIndex) ? Steps[StepIndex].MissionTitle : FString();
}
