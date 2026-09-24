#include "ExoSpawner.h"
#include "ExoHollow.h"
#include "Engine/World.h"
#include "NavigationSystem.h"

AExoSpawner::AExoSpawner()
{
	RootComponent = CreateDefaultSubobject<USceneComponent>(TEXT("Root"));
}

void AExoSpawner::BeginPlay()
{
	Super::BeginPlay();
	if (Group.IsNone()) Spawn();
}

AExoHollow* AExoSpawner::SpawnHollow(UWorld* World, const FVector& Where, EExoHollowType Type, const FString& Mesh, FName StoryId, bool bHorde)
{
	if (!World) return nullptr;
	FVector At = Where;
	if (UNavigationSystemV1* Nav = FNavigationSystem::GetCurrent<UNavigationSystemV1>(World))
	{
		FNavLocation Out;
		if (Nav->ProjectPointToNavigation(Where, Out, FVector(300.f, 300.f, 500.f))) At = Out.Location;
	}
	FActorSpawnParameters P;
	P.SpawnCollisionHandlingOverride = ESpawnActorCollisionHandlingMethod::AdjustIfPossibleButAlwaysSpawn;
	const FTransform T(FRotator(0.f, FMath::FRandRange(0.f, 360.f), 0.f), At + FVector(0.f, 0.f, 95.f));
	AExoHollow* H = World->SpawnActorDeferred<AExoHollow>(AExoHollow::StaticClass(), T, nullptr, nullptr, P.SpawnCollisionHandlingOverride);
	if (H)
	{
		H->HollowType = Type;
		H->MeshAsset = Mesh;
		H->StoryId = StoryId;
		H->bHorde = bHorde;
		H->FinishSpawning(T);
	}
	return H;
}

void AExoSpawner::Spawn()
{
	if (bSpawned) return;
	bSpawned = true;
	for (int32 i = 0; i < Count; ++i)
	{
		const FVector Offset = Count > 1 ? FVector(FMath::FRandRange(-RadiusCm, RadiusCm), FMath::FRandRange(-RadiusCm, RadiusCm), 0.f) : FVector::ZeroVector;
		SpawnHollow(GetWorld(), GetActorLocation() + Offset, HollowType, MeshAsset, Count == 1 ? StoryId : NAME_None, false);
	}
}
