using UnrealBuildTool;

public class Apex_Project : ModuleRules
{
	public Apex_Project(ReadOnlyTargetRules Target) : base(Target)
	{
		PCHUsage = PCHUsageMode.UseExplicitOrSharedPCHs;
		PublicDependencyModuleNames.AddRange(new string[] {
			"Core", "CoreUObject", "Engine", "InputCore", "EnhancedInput",
			"AIModule", "NavigationSystem", "Json", "JsonUtilities", "ProceduralMeshComponent"
		});
	}
}
