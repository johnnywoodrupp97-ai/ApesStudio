// Canvas HUD for the prototype (no widget assets needed): vitals, the infection creep, objectives,
// subtitles, title cards, prompts, build mode, clock and companion barks.
#pragma once

#include "CoreMinimal.h"
#include "GameFramework/HUD.h"
#include "ExoHUD.generated.h"

UCLASS()
class APEX_PROJECT_API AExoHUD : public AHUD
{
	GENERATED_BODY()

public:
	virtual void DrawHUD() override;

private:
	void Bar(float X, float Y, float W, float H, float Frac, const FLinearColor& Color, const FString& Label);
	void TextCentered(const FString& Text, float Y, float Scale, const FLinearColor& Color);
	void DrawInfectionVignette(float Infection);
};
