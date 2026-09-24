#include "ExoNoiseSubsystem.h"
#include "Engine/World.h"

void UExoNoiseSubsystem::ReportNoise(FVector Location, float RadiusMeters, AActor* Instigator, FName Tag)
{
	const float Now = GetWorld() ? GetWorld()->GetTimeSeconds() : 0.f;
	// Keep the list short: drop anything older than three minutes.
	Noises.RemoveAll([Now](const FExoNoise& N) { return Now - N.Time > 180.f; });
	FExoNoise N;
	N.Location = Location;
	N.RadiusCm = RadiusMeters * 100.f;
	N.Time = Now;
	N.Instigator = Instigator;
	N.Tag = Tag;
	Noises.Add(N);
}

bool UExoNoiseSubsystem::FindAudibleNoise(const FVector& Listener, float MaxAgeSeconds, FExoNoise& OutNoise) const
{
	const float Now = GetWorld() ? GetWorld()->GetTimeSeconds() : 0.f;
	float Best = -1.f;
	for (const FExoNoise& N : Noises)
	{
		if (Now - N.Time > MaxAgeSeconds) continue;
		const float Dist = FVector::Dist(Listener, N.Location);
		if (Dist > N.RadiusCm) continue;
		const float Loudness = 1.f - Dist / FMath::Max(1.f, N.RadiusCm);
		if (Loudness > Best)
		{
			Best = Loudness;
			OutNoise = N;
		}
	}
	return Best >= 0.f;
}

int32 UExoNoiseSubsystem::CountRecent(FName Tag, float WindowSeconds) const
{
	const float Now = GetWorld() ? GetWorld()->GetTimeSeconds() : 0.f;
	int32 Count = 0;
	for (const FExoNoise& N : Noises)
	{
		if (N.Tag == Tag && Now - N.Time <= WindowSeconds) ++Count;
	}
	return Count;
}
