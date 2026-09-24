#include "ExoTerrain.h"
#include "Apex_Project.h"
#include "ProceduralMeshComponent.h"
#include "Materials/MaterialInterface.h"
#include "Misc/FileHelper.h"
#include "Misc/Paths.h"
#include "Serialization/JsonReader.h"
#include "Serialization/JsonSerializer.h"
#include "Dom/JsonObject.h"

AExoTerrain::AExoTerrain()
{
	Mesh = CreateDefaultSubobject<UProceduralMeshComponent>(TEXT("Mesh"));
	RootComponent = Mesh;
	Mesh->bUseComplexAsSimpleCollision = true;
	Mesh->SetCollisionProfileName(TEXT("BlockAll"));
	Mesh->SetCanEverAffectNavigation(true);
}

void AExoTerrain::OnConstruction(const FTransform& Transform)
{
	Super::OnConstruction(Transform);
	Rebuild();
}

void AExoTerrain::BeginPlay()
{
	Super::BeginPlay();
	Rebuild();
}

void AExoTerrain::Rebuild()
{
	const FString Path = FPaths::ProjectContentDir() / TEXT("Exodus/Data/slice_layout.json");
	FString Text;
	TSharedPtr<FJsonObject> Root;
	if (!FFileHelper::LoadFileToString(Text, *Path) || !FJsonSerializer::Deserialize(TJsonReaderFactory<>::Create(Text), Root) || !Root.IsValid())
	{
		UE_LOG(LogExodus, Warning, TEXT("ExoTerrain: can't read %s"), *Path);
		return;
	}
	const TSharedPtr<FJsonObject> T = Root->GetObjectField(TEXT("terrain"));
	const TArray<TSharedPtr<FJsonValue>>& Origin = T->GetArrayField(TEXT("origin"));
	const float X0 = Origin[0]->AsNumber(), Y0 = Origin[1]->AsNumber();
	const float Step = T->GetNumberField(TEXT("step"));
	const int32 NX = (int32)T->GetNumberField(TEXT("nx")), NY = (int32)T->GetNumberField(TEXT("ny"));
	const TArray<TSharedPtr<FJsonValue>>& H = T->GetArrayField(TEXT("heights"));
	if (H.Num() != NX * NY)
	{
		UE_LOG(LogExodus, Error, TEXT("ExoTerrain: %d heights for a %dx%d grid"), H.Num(), NX, NY);
		return;
	}

	TArray<FVector> Verts;
	TArray<FVector> Normals;
	TArray<FVector2D> UVs;
	TArray<int32> Tris;
	Verts.Reserve(NX * NY);
	auto Height = [&](int32 i, int32 j) { return (float)H[j * NX + i]->AsNumber(); };
	for (int32 j = 0; j < NY; ++j)
	{
		for (int32 i = 0; i < NX; ++i)
		{
			Verts.Add(FVector(X0 + i * Step, Y0 + j * Step, Height(i, j)));
			const float dX = Height(FMath::Min(i + 1, NX - 1), j) - Height(FMath::Max(i - 1, 0), j);
			const float dY = Height(i, FMath::Min(j + 1, NY - 1)) - Height(i, FMath::Max(j - 1, 0));
			Normals.Add(FVector(-dX, -dY, 2.f * Step).GetSafeNormal());
			UVs.Add(FVector2D(i * Step / 1000.f, j * Step / 1000.f)); // 10 m texture tiling
		}
	}
	// Both windings are emitted so the ground renders and collides from above whatever the
	// engine's front-face convention (cheap at this resolution, and robust for a prototype).
	for (int32 j = 0; j + 1 < NY; ++j)
	{
		for (int32 i = 0; i + 1 < NX; ++i)
		{
			const int32 A = j * NX + i, B = A + 1, C = A + NX, D = C + 1;
			Tris.Append({A, C, B, B, C, D});
			Tris.Append({A, B, C, B, D, C});
		}
	}
	TArray<FLinearColor> Colors;
	TArray<FProcMeshTangent> Tangents;
	Mesh->ClearAllMeshSections();
	Mesh->CreateMeshSection_LinearColor(0, Verts, Tris, Normals, UVs, Colors, Tangents, true);
	if (Material) Mesh->SetMaterial(0, Material);
	UE_LOG(LogExodus, Log, TEXT("ExoTerrain: %dx%d grid, %d triangles"), NX, NY, Tris.Num() / 3);
}
