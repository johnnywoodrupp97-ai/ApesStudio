"""Export the vertical slice's parts and characters from the repo's Blender files into SourceArt/.

The FBX files are already committed, so you only need this after changing a .blend. From the repository root:

    blender -b -P unreal/Apex_Project/SourceArt/export_slice_art.py
    # or, with the stand-alone bpy module:  python unreal/Apex_Project/SourceArt/export_slice_art.py

Parts: LOD0 plus its UCX_ collision, with LOD0 renamed to the asset name so Unreal pairs the collision with it.
Characters: the LOD0 skeletal mesh written by tools/blender/exodus_characters.py (armature + meshes).
"""
import importlib.util
import shutil
import sys
import tempfile
from pathlib import Path

import bpy

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]

PARTS = [  # must match ExoTuning::SliceParts() in Source/Apex_Project/Public/ExoTypes.h
    "SM_STR_ScrapWall_ASheetAndSigns_LG", "SM_DEF_Barricade_Wooden_LG", "SM_DEF_SandbagWall_FullHeight_LG",
    "SM_STR_ArmorBlock_Light_LG", "SM_DOR_ScrapDoor_LG", "SM_PRD_Workbench_LG", "SM_PWR_DieselGenerator_LG",
    "SM_UTL_Floodlight_TripodSurvivor_LG", "SM_COL_Campfire_StoneRing_LG",
]
CHARACTERS = [  # every mesh_asset in Content/Python/exodus_ue/slice_extras.py and ExoGameMode's horde meshes
    "SK_CHR_TugBrennan", "SK_CHR_AdaOkafor", "SK_CHR_LilyChen", "SK_CHR_HalvardCrane", "SK_CHR_MaraVoss",
    "SK_CHR_DanaMarsh_Hollow", "SK_CHR_RosaAlvarez_Hollow", "SK_ENM_Shambler", "SK_ENM_Shambler_KestrelCrew",
    "SK_ENM_Shambler_Civilian", "SK_ENM_Runner", "SK_ENM_Crawler", "SK_NPC_DirectorateTrooper",
    "SK_NPC_DirectorateTrooper_Female",
]
FBX = dict(use_selection=True, apply_unit_scale=True, apply_scale_options="FBX_SCALE_UNITS", mesh_smooth_type="FACE",
           add_leaf_bones=False, bake_anim=False, axis_forward="-Z", axis_up="Y")


def find(root, name):
    hits = list((REPO / "assets" / root).rglob(f"{name}.blend"))
    if not hits:
        raise SystemExit(f"Missing assets/{root}/**/{name}.blend")
    return hits[0]


def export_part(name, out_dir):
    bpy.ops.wm.open_mainfile(filepath=str(find("parts", name)))
    for o in bpy.context.view_layer.objects:
        o.select_set(False)
    if name in bpy.data.objects:  # the root empty holds the asset name; free it for the mesh
        bpy.data.objects[name].name = f"ROOT_{name}"
    body = bpy.data.objects[f"{name}_LOD0"]
    body.name = name
    chosen = [body] + [o for o in bpy.data.objects if o.name.startswith(f"UCX_{name}_") and o.type == "MESH"]
    for o in chosen:
        o.hide_set(False)
        o.select_set(True)
    bpy.ops.export_scene.fbx(filepath=str(out_dir / f"{name}.fbx"), object_types={"MESH"}, **FBX)


def main():
    parts_dir, chars_dir = HERE / "Parts", HERE / "Characters"
    parts_dir.mkdir(exist_ok=True)
    chars_dir.mkdir(exist_ok=True)
    for name in PARTS:
        export_part(name, parts_dir)
        print("part", name)

    spec = importlib.util.spec_from_file_location("exodus_characters", REPO / "tools" / "blender" / "exodus_characters.py")
    chars = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(chars)
    with tempfile.TemporaryDirectory() as tmp:
        for name in CHARACTERS:
            blend = find("characters", name)
            chars.export_file(blend, tmp)
            shutil.copyfile(Path(tmp) / "export" / "characters" / blend.parent.name / f"{name}.fbx", chars_dir / f"{name}.fbx")
            print("character", name)
    print(f"Exported {len(PARTS)} parts and {len(CHARACTERS)} characters to {HERE}")


if __name__ == "__main__":
    sys.exit(main())
