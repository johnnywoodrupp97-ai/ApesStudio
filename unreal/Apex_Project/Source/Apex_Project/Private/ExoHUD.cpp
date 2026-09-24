#include "ExoHUD.h"
#include "ExoPlayerCharacter.h"
#include "ExoVitalsComponent.h"
#include "ExoBuildComponent.h"
#include "ExoBlock.h"
#include "ExoCompanion.h"
#include "ExoGameMode.h"
#include "ExoMissionSubsystem.h"
#include "Engine/Canvas.h"
#include "Engine/Engine.h"
#include "Engine/Font.h"
#include "EngineUtils.h"
#include "Kismet/GameplayStatics.h"

void AExoHUD::Bar(float X, float Y, float W, float H, float Frac, const FLinearColor& Color, const FString& Label)
{
	DrawRect(FLinearColor(0.f, 0.f, 0.f, 0.55f), X, Y, W, H);
	DrawRect(Color, X + 2.f, Y + 2.f, (W - 4.f) * FMath::Clamp(Frac, 0.f, 1.f), H - 4.f);
	DrawText(Label, FLinearColor::White, X + W + 8.f, Y - 3.f, GEngine->GetSmallFont(), 1.f);
}

void AExoHUD::TextCentered(const FString& Text, float Y, float Scale, const FLinearColor& Color)
{
	if (Text.IsEmpty()) return;
	UFont* Font = GEngine->GetLargeFont();
	float W = 0.f, H = 0.f;
	GetTextSize(Text, W, H, Font, Scale);
	DrawText(Text, FLinearColor(0.f, 0.f, 0.f, 0.8f), (Canvas->ClipX - W) * 0.5f + 2.f, Y + 2.f, Font, Scale);
	DrawText(Text, Color, (Canvas->ClipX - W) * 0.5f, Y, Font, Scale);
}

void AExoHUD::DrawInfectionVignette(float Infection)
{
	// The Infection HUD "crawls in green from the screen edges" (game bible 03 / 05).
	if (Infection <= 0.f) return;
	const float T = FMath::Clamp(Infection / 100.f, 0.f, 1.f);
	const FLinearColor Green(0.25f, 0.85f, 0.3f, 0.08f + 0.35f * T);
	const float Edge = FMath::Lerp(20.f, Canvas->ClipY * 0.22f, T);
	const int32 Steps = 6;
	for (int32 i = 0; i < Steps; ++i)
	{
		const float E = Edge * (i + 1) / Steps;
		FLinearColor C = Green;
		C.A *= 1.f - float(i) / Steps;
		DrawRect(C, 0.f, 0.f, Canvas->ClipX, E / Steps);
		DrawRect(C, 0.f, Canvas->ClipY - E / Steps, Canvas->ClipX, E / Steps);
		DrawRect(C, 0.f, 0.f, E / Steps, Canvas->ClipY);
		DrawRect(C, Canvas->ClipX - E / Steps, 0.f, E / Steps, Canvas->ClipY);
	}
}

void AExoHUD::DrawHUD()
{
	Super::DrawHUD();
	AExoPlayerCharacter* P = Cast<AExoPlayerCharacter>(GetOwningPawn());
	UExoMissionSubsystem* Missions = GetWorld()->GetSubsystem<UExoMissionSubsystem>();
	AExoGameMode* GM = GetWorld()->GetAuthGameMode<AExoGameMode>();
	const float W = Canvas->ClipX, H = Canvas->ClipY;
	UFont* Small = GEngine->GetSmallFont();
	UFont* Medium = GEngine->GetMediumFont();

	if (P)
	{
		UExoVitalsComponent* V = P->Vitals;
		DrawInfectionVignette(V->Infection);

		// Crosshair.
		DrawRect(FLinearColor(1.f, 1.f, 1.f, 0.8f), W * 0.5f - 1.f, H * 0.5f - 6.f, 2.f, 12.f);
		DrawRect(FLinearColor(1.f, 1.f, 1.f, 0.8f), W * 0.5f - 6.f, H * 0.5f - 1.f, 12.f, 2.f);

		// Vitals, bottom left.
		const float X = 32.f;
		float Y = H - 150.f;
		Bar(X, Y, 220.f, 16.f, V->Health / V->MaxHealth, FLinearColor(0.85f, 0.2f, 0.2f), FString::Printf(TEXT("Health %.0f"), V->Health)); Y += 24.f;
		Bar(X, Y, 220.f, 16.f, V->Stamina / 100.f, FLinearColor(0.9f, 0.8f, 0.3f), TEXT("Stamina")); Y += 24.f;
		Bar(X, Y, 220.f, 16.f, V->Hunger / 100.f, FLinearColor(0.8f, 0.5f, 0.2f), TEXT("Hunger")); Y += 24.f;
		Bar(X, Y, 220.f, 16.f, V->Thirst / 100.f, FLinearColor(0.3f, 0.6f, 0.95f), TEXT("Thirst")); Y += 24.f;
		static const TCHAR* Stages[] = {TEXT("Clean"), TEXT("Exposed"), TEXT("Seeded"), TEXT("Blooming"), TEXT("Turning")};
		Bar(X, Y, 220.f, 16.f, V->Infection / 100.f, FLinearColor(0.3f, 0.9f, 0.35f),
			FString::Printf(TEXT("Infection %.0f%% (%s)  Suppressants: %d [H]%s"), V->Infection, Stages[(int32)V->GetStage()], V->Suppressants,
				V->GetSuppressionTimeLeft() > 0.f ? TEXT("  suppressed") : TEXT("")));

		if (V->GetTurningTimeLeft() >= 0.f)
		{
			TextCentered(FString::Printf(TEXT("TURNING  %.0f"), V->GetTurningTimeLeft()), H * 0.2f, 2.f, FLinearColor(0.4f, 1.f, 0.4f));
		}
		if (V->IsDead())
		{
			DrawRect(FLinearColor(0.f, 0.f, 0.f, 0.6f), 0.f, 0.f, W, H);
			TextCentered(TEXT("YOU DIED"), H * 0.42f, 3.f, FLinearColor(0.9f, 0.2f, 0.2f));
			TextCentered(TEXT("Returning to the last checkpoint..."), H * 0.52f, 1.2f, FLinearColor::White);
		}

		// Interaction prompt.
		TextCentered(P->GetFocusPrompt().ToString(), H * 0.58f, 1.1f, FLinearColor(1.f, 0.95f, 0.8f));

		// Build mode panel, bottom right.
		if (P->Build->IsBuildMode())
		{
			const FExoPartDef& Part = P->Build->GetSelectedPart();
			const float BX = W - 420.f;
			DrawRect(FLinearColor(0.f, 0.f, 0.f, 0.55f), BX, H - 170.f, 390.f, 140.f);
			DrawText(TEXT("BUILD MODE  [B] exit"), FLinearColor(1.f, 0.7f, 0.2f), BX + 12.f, H - 162.f, Medium, 1.f);
			DrawText(FString::Printf(TEXT("%s  (%s)   cost %d / have %d"), *Part.Name, *Part.PartId.ToString(), Part.Cost, P->Components), FLinearColor::White, BX + 12.f, H - 132.f, Small, 1.f);
			DrawText(TEXT("LMB place / hold to weld   RMB grind   R rotate   Wheel next part"), FLinearColor(0.8f, 0.8f, 0.8f), BX + 12.f, H - 110.f, Small, 1.f);
			if (AExoBlock* T = P->Build->GetTargetBlock())
			{
				DrawText(FString::Printf(TEXT("%s: %.0f%% built, integrity %.0f"), *T->Part.Name, T->BuildProgress * 100.f, T->Health), FLinearColor(0.6f, 1.f, 0.6f), BX + 12.f, H - 84.f, Small, 1.f);
			}
		}
		else
		{
			DrawText(FString::Printf(TEXT("Components: %d"), P->Components), FLinearColor(0.9f, 0.9f, 0.9f), W - 200.f, H - 60.f, Small, 1.f);
		}
	}

	// Clock and night, top right.
	if (GM)
	{
		const float Hour = GM->GetHour();
		const int32 HH = FMath::FloorToInt(Hour), MM = FMath::FloorToInt((Hour - HH) * 60.f);
		const FString Night = GM->IsNight() ? (GM->IsGreenMoon() ? TEXT("  GREEN MOON") : TEXT("  night")) : TEXT("");
		DrawText(FString::Printf(TEXT("%02d:%02d%s   Attraction %.0f"), HH, MM, *Night, GM->GetAttraction()),
			GM->IsGreenMoon() ? FLinearColor(0.5f, 1.f, 0.5f) : FLinearColor::White, W - 330.f, 24.f, Medium, 1.f);
	}

	// Mission objective, top left.
	if (Missions)
	{
		const FString Obj = Missions->GetObjective();
		if (!Obj.IsEmpty())
		{
			DrawText(Missions->GetMissionTitle().ToUpper(), FLinearColor(1.f, 0.7f, 0.2f), 32.f, 24.f, Small, 1.f);
			DrawText(Obj, FLinearColor::White, 32.f, 44.f, Medium, 1.f);
		}
		if (const FExoLine* Line = Missions->GetCurrentLine())
		{
			const FString Sub = Line->Speaker.IsEmpty() ? Line->Text : FString::Printf(TEXT("%s: %s"), *Line->Speaker, *Line->Text);
			TextCentered(Sub, H - 120.f, 1.05f, FLinearColor(1.f, 1.f, 0.9f));
			TextCentered(TEXT("[Enter] skip"), H - 92.f, 0.7f, FLinearColor(0.7f, 0.7f, 0.7f));
		}
		const FString Title = Missions->GetTitleCard();
		if (!Title.IsEmpty())
		{
			DrawRect(FLinearColor(0.f, 0.f, 0.f, 0.5f), 0.f, H * 0.36f, W, H * 0.14f);
			TextCentered(Title, H * 0.40f, 3.f, FLinearColor(0.95f, 0.95f, 0.95f));
		}
	}

	// Companion barks, projected over their heads.
	for (TActorIterator<AExoCompanion> It(GetWorld()); It; ++It)
	{
		const FString Bark = It->GetCurrentBark();
		if (Bark.IsEmpty()) continue;
		const FVector S = Project(It->GetActorLocation() + FVector(0.f, 0.f, It->HeightCm * 0.6f));
		if (S.Z > 0.f)
		{
			float TW = 0.f, TH = 0.f;
			GetTextSize(Bark, TW, TH, Small, 1.f);
			DrawRect(FLinearColor(0.f, 0.f, 0.f, 0.5f), S.X - TW * 0.5f - 6.f, S.Y - 4.f, TW + 12.f, TH + 8.f);
			DrawText(Bark, FLinearColor::White, S.X - TW * 0.5f, S.Y, Small, 1.f);
		}
	}
}
