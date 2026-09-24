#include "ExoAnimComponent.h"
#include "Apex_Project.h"
#include "Animation/AnimSequence.h"
#include "Components/SkeletalMeshComponent.h"
#include "GameFramework/Character.h"
#include "Misc/FileHelper.h"
#include "Misc/Paths.h"
#include "Serialization/JsonReader.h"
#include "Serialization/JsonSerializer.h"

static const TCHAR* AnimsPath = TEXT("/Game/Exodus/Imported/Animations");
static const FName IdleClip(TEXT("Idle")), TalkClip(TEXT("Talk")), CrouchClip(TEXT("CrouchWalk")), DeathClip(TEXT("Death"));

/** Content/Exodus/Data/animations.json, parsed once: { "characters": { "<mesh>": { "anims": { "<clip>": {...} } } } }. */
static TSharedPtr<FJsonObject> AnimManifest()
{
	static TSharedPtr<FJsonObject> Characters;
	static bool bLoaded = false;
	if (!bLoaded)
	{
		bLoaded = true;
		const FString Path = FPaths::ProjectContentDir() / TEXT("Exodus/Data/animations.json");
		FString Text;
		TSharedPtr<FJsonObject> Root;
		if (FFileHelper::LoadFileToString(Text, *Path) && FJsonSerializer::Deserialize(TJsonReaderFactory<>::Create(Text), Root) && Root.IsValid())
		{
			Characters = Root->GetObjectField(TEXT("characters"));
		}
		else
		{
			UE_LOG(LogExodus, Error, TEXT("Missing or unreadable %s: characters will hold their bind pose"), *Path);
		}
	}
	return Characters;
}

UExoAnimComponent::UExoAnimComponent()
{
	PrimaryComponentTick.bCanEverTick = true;
	PrimaryComponentTick.bStartWithTickEnabled = false; // until Setup finds clips
}

bool UExoAnimComponent::Setup(USkeletalMeshComponent* InMesh, const FString& MeshAsset)
{
	Mesh = InMesh;
	Clips.Reset();
	Loaded.Reset();
	Current = OneShot = NAME_None;
	bHold = false;
	const FString MeshName = FPaths::GetBaseFilename(MeshAsset);
	const TSharedPtr<FJsonObject> Characters = AnimManifest();
	const TSharedPtr<FJsonObject>* Entry = nullptr;
	if (!Mesh || !Mesh->GetSkeletalMeshAsset() || !Characters.IsValid() || !Characters->TryGetObjectField(MeshName, Entry))
	{
		SetComponentTickEnabled(false);
		return false;
	}
	int32 Missing = 0;
	for (const TPair<FString, TSharedPtr<FJsonValue>>& It : (*Entry)->GetObjectField(TEXT("anims"))->Values)
	{
		const TSharedPtr<FJsonObject> A = It.Value->AsObject();
		const FString Asset = A->GetStringField(TEXT("asset"));
		const FString Path = FString::Printf(TEXT("%s/%s/%s.%s"), AnimsPath, *MeshName, *Asset, *Asset);
		UAnimSequence* Seq = LoadObject<UAnimSequence>(nullptr, *Path, nullptr, LOAD_NoWarn | LOAD_Quiet);
		if (!Seq)
		{
			++Missing;
			continue;
		}
		FExoAnimClip& Clip = Clips.Add(FName(*It.Key));
		Clip.Sequence = Seq;
		Clip.bLoop = A->GetBoolField(TEXT("loop"));
		Clip.bLocomotion = A->GetBoolField(TEXT("locomotion"));
		Clip.SpeedCmS = (float)A->GetNumberField(TEXT("speed_cm_s"));
		Loaded.Add(Seq);
	}
	if (Missing > 0)
	{
		UE_LOG(LogExodus, Warning, TEXT("%s: %d animation(s) not imported under %s/%s"), *MeshName, Missing, AnimsPath, *MeshName);
	}
	SetComponentTickEnabled(Clips.Contains(IdleClip));
	return Clips.Contains(IdleClip);
}

void UExoAnimComponent::Play(FName Name, bool bLoop, float Rate)
{
	const FExoAnimClip* Clip = Find(Name);
	if (!Clip || !Mesh) return;
	if (Current != Name)
	{
		Current = Name;
		Mesh->PlayAnimation(Clip->Sequence, bLoop);
	}
	Mesh->SetPlayRate(Rate);
}

bool UExoAnimComponent::PlayOnce(FName Name, float Seconds)
{
	const FExoAnimClip* Clip = Find(Name);
	if (!Clip || bHold) return false;
	OneShot = Name;
	OneShotLeft = Seconds > 0.f ? Seconds : Clip->Sequence->GetPlayLength();
	Current = NAME_None; // restart the clip even if it is already playing
	Play(Name, Clip->bLoop, 1.f);
	return true;
}

bool UExoAnimComponent::PlayDeath()
{
	if (!PlayOnce(DeathClip)) return false;
	bHold = true; // a non-looping single-node clip stays on its last frame
	return true;
}

FName UExoAnimComponent::PickBase(float Speed, float& OutRate) const
{
	OutRate = 1.f;
	if (Speed < 20.f)
	{
		return bTalking && HasClip(TalkClip) ? TalkClip : IdleClip;
	}
	const ACharacter* Char = Cast<ACharacter>(GetOwner());
	const bool bCrouched = Char && Char->bIsCrouched && HasClip(CrouchClip);
	// The cycle whose ground speed is closest (in ratio) to the actual speed, sticking with the current one
	// unless another is clearly better, so the gait does not flicker at a boundary.
	FName Best = NAME_None;
	float BestCost = TNumericLimits<float>::Max();
	for (const TPair<FName, FExoAnimClip>& It : Clips)
	{
		const FExoAnimClip& C = It.Value;
		if (!C.bLocomotion || C.SpeedCmS <= 0.f) continue;
		if ((It.Key == CrouchClip) != bCrouched) continue;
		const float Cost = FMath::Abs(FMath::Loge(Speed / C.SpeedCmS)) - (It.Key == Current ? 0.15f : 0.f);
		if (Cost < BestCost) { BestCost = Cost; Best = It.Key; }
	}
	if (Best.IsNone()) return IdleClip;
	OutRate = FMath::Clamp(Speed / Clips.FindChecked(Best).SpeedCmS, 0.5f, 2.f);
	return Best;
}

void UExoAnimComponent::TickComponent(float DeltaTime, ELevelTick TickType, FActorComponentTickFunction* ThisTickFunction)
{
	Super::TickComponent(DeltaTime, TickType, ThisTickFunction);
	if (bHold || !Mesh) return;
	if (!OneShot.IsNone())
	{
		OneShotLeft -= DeltaTime;
		if (OneShotLeft > 0.f) return;
		OneShot = NAME_None;
	}
	float Rate = 1.f;
	const FName Base = PickBase(GetOwner()->GetVelocity().Size2D(), Rate);
	Play(Base, true, Rate);
}
