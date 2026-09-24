using UnrealBuildTool;

public class Apex_ProjectEditorTarget : TargetRules
{
	public Apex_ProjectEditorTarget(TargetInfo Target) : base(Target)
	{
		Type = TargetType.Editor;
		DefaultBuildSettings = BuildSettingsVersion.Latest;
		IncludeOrderVersion = EngineIncludeOrderVersion.Latest;
		ExtraModuleNames.Add("Apex_Project");
	}
}
