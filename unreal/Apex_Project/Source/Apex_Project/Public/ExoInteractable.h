// Anything the player can use with the interact key (game bible 21: E / X).
#pragma once

#include "CoreMinimal.h"
#include "UObject/Interface.h"
#include "ExoInteractable.generated.h"

class AExoPlayerCharacter;

UINTERFACE(MinimalAPI, Blueprintable)
class UExoInteractable : public UInterface
{
	GENERATED_BODY()
};

class APEX_PROJECT_API IExoInteractable
{
	GENERATED_BODY()

public:
	virtual void Interact(AExoPlayerCharacter* Player) = 0;
	virtual FText GetPrompt() const = 0;
	virtual bool CanInteract(const AExoPlayerCharacter* Player) const { return true; }
};
