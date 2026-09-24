"""Build the vertical slice map inside the Unreal Editor (UE 5.8) from the files in this project.

    1. Import SourceArt/Parts/*.fbx      -> /Game/Exodus/Imported/Parts/<name>        (static meshes, UCX collision)
       Import SourceArt/Characters/*.fbx -> /Game/Exodus/Imported/Characters/<name>   (skeletal meshes + skeleton + physics)
       Import SourceArt/Animations/<name>/*.fbx -> /Game/Exodus/Imported/Animations/<name>/<clip> (on <name>'s skeleton)
    2. Create greybox material instances (one colour per style) under /Game/Exodus/Materials.
    3. Create /Game/Exodus/Maps/L_VerticalSlice and fill it from Content/Exodus/Data/slice_layout.json:
       terrain, 600 greybox boxes, markers, triggers, spawners, companions, interactables, sky and sun.
    4. Build the navmesh, then save.

Runs from the "Exodus" menu (init_unreal.py), automatically on the first editor start when the map is missing,
or by hand in the Output Log's Python console:
    import exodus_ue.exodus_setup as s; s.build()          # everything
    s.build(reimport=False)                                  # keep imported assets, rebuild the map only
Regenerate slice_layout.json first if you changed the planner or slice_extras.py:  python3 Content/Python/exodus_ue/planner.py
"""
import json
import re
from pathlib import Path

import unreal

ROOT = "/Game/Exodus"
MAP = f"{ROOT}/Maps/L_VerticalSlice"
PARTS_PATH = f"{ROOT}/Imported/Parts"
CHARS_PATH = f"{ROOT}/Imported/Characters"
ANIMS_PATH = f"{ROOT}/Imported/Animations"  # ExoAnimComponent loads <ANIMS_PATH>/<mesh name>/<clip>
MAT_PATH = f"{ROOT}/Materials"

STYLE_COLORS = {  # linear RGB, greybox palette (level bible 13: cool concrete complex, warm township)
    "wall": (0.55, 0.55, 0.52), "floor": (0.32, 0.32, 0.33), "ceiling": (0.42, 0.42, 0.44), "building": (0.48, 0.46, 0.42),
    "house": (0.62, 0.50, 0.38), "industrial": (0.40, 0.42, 0.45), "road": (0.07, 0.07, 0.08), "tank": (0.70, 0.70, 0.66),
    "prop": (0.30, 0.34, 0.40), "plinth": (0.35, 0.35, 0.35), "fence": (0.45, 0.45, 0.40), "pad": (0.25, 0.25, 0.26),
    "ship": (0.85, 0.83, 0.78), "tower": (0.60, 0.20, 0.12), "bunker": (0.30, 0.32, 0.28), "rocket": (0.90, 0.90, 0.88),
    "terrain": (0.36, 0.30, 0.22),
}
ENGINE_SHAPES = {"cube": "/Engine/BasicShapes/Cube.Cube", "cylinder": "/Engine/BasicShapes/Cylinder.Cylinder"}
SHAPE_MATERIAL = "/Engine/BasicShapes/BasicShapeMaterial.BasicShapeMaterial"
SKIP_PROPS = {"extent", "size", "marker_name"}


def project_dir():
    return Path(unreal.Paths.convert_relative_path_to_full(unreal.Paths.project_dir()))


def log(msg):
    unreal.log(f"[Exodus] {msg}")


def enum_value(enum_cls, name):
    """ 'MedCabinet' -> unreal.ExoInteractKind.MED_CABINET """
    return getattr(enum_cls, re.sub(r"(?<!^)(?=[A-Z])", "_", name).upper())


# --------------------------------------------------------------------------- 1. import
def _fbx_task(fbx, dest, skeletal):
    ui = unreal.FbxImportUI()
    ui.set_editor_property("import_mesh", True)
    ui.set_editor_property("import_textures", False)
    ui.set_editor_property("import_materials", True)
    ui.set_editor_property("import_animations", False)
    ui.set_editor_property("import_as_skeletal", skeletal)
    ui.set_editor_property("automated_import_should_detect_type", False)
    if skeletal:
        ui.set_editor_property("mesh_type_to_import", unreal.FBXImportType.FBXIT_SKELETAL_MESH)
        ui.set_editor_property("create_physics_asset", True)
        ui.skeletal_mesh_import_data.set_editor_property("import_morph_targets", True)
    else:
        ui.set_editor_property("mesh_type_to_import", unreal.FBXImportType.FBXIT_STATIC_MESH)
        ui.static_mesh_import_data.set_editor_property("combine_meshes", True)
        ui.static_mesh_import_data.set_editor_property("auto_generate_collision", False)  # UCX_ hulls come with the FBX
    task = unreal.AssetImportTask()
    task.set_editor_property("filename", str(fbx))
    task.set_editor_property("destination_path", dest)
    task.set_editor_property("destination_name", fbx.stem)
    task.set_editor_property("automated", True)
    task.set_editor_property("replace_existing", True)
    task.set_editor_property("save", True)
    task.set_editor_property("options", ui)
    return task


def _anim_task(fbx, dest, skeleton):
    ui = unreal.FbxImportUI()
    ui.set_editor_property("import_mesh", False)
    ui.set_editor_property("import_textures", False)
    ui.set_editor_property("import_materials", False)
    ui.set_editor_property("import_animations", True)
    ui.set_editor_property("import_as_skeletal", True)
    ui.set_editor_property("automated_import_should_detect_type", False)
    ui.set_editor_property("mesh_type_to_import", unreal.FBXImportType.FBXIT_ANIMATION)
    ui.set_editor_property("skeleton", skeleton)
    data = ui.anim_sequence_import_data
    data.set_editor_property("animation_length", unreal.FBXAnimationLengthImportType.FBXALIT_EXPORTED_TIME)
    data.set_editor_property("import_bone_tracks", True)
    data.set_editor_property("remove_redundant_keys", False)  # keeps the loops closing exactly
    task = unreal.AssetImportTask()
    task.set_editor_property("filename", str(fbx))
    task.set_editor_property("destination_path", dest)
    task.set_editor_property("destination_name", fbx.stem)
    task.set_editor_property("automated", True)
    task.set_editor_property("replace_existing", True)
    task.set_editor_property("save", True)
    task.set_editor_property("options", ui)
    return task


def import_animations(tools):
    """Clips go onto the skeleton of the character imported just before; characters that failed to import are skipped."""
    root = project_dir() / "SourceArt" / "Animations"
    folders = sorted(d for d in root.glob("*") if d.is_dir()) if root.exists() else []
    jobs = []
    for d in folders:
        mesh_path = f"{CHARS_PATH}/{d.name}"
        mesh = unreal.load_asset(mesh_path) if unreal.EditorAssetLibrary.does_asset_exist(mesh_path) else None
        skeleton = mesh.get_editor_property("skeleton") if mesh else None
        if skeleton is None:
            unreal.log_warning(f"[Exodus] No skeleton for {d.name}; its animations are skipped")
            continue
        jobs += [(f, f"{ANIMS_PATH}/{d.name}", skeleton) for f in sorted(d.glob("*.fbx"))]
    with unreal.ScopedSlowTask(len(jobs), "Exodus: importing animations") as slow:
        slow.make_dialog(False)
        for fbx, dest, skeleton in jobs:
            slow.enter_progress_frame(1, f"Importing {fbx.name}")
            tools.import_asset_tasks([_anim_task(fbx, dest, skeleton)])
    missing = [fbx.stem for fbx, dest, _s in jobs if not unreal.EditorAssetLibrary.does_asset_exist(f"{dest}/{fbx.stem}")]
    if missing:
        unreal.log_warning(f"[Exodus] Animations not imported (those characters hold their pose): {', '.join(missing)}")
    log(f"Imported {len(jobs) - len(missing)} / {len(jobs)} animations")


def import_art():
    art = project_dir() / "SourceArt"
    jobs = [(f, PARTS_PATH, False) for f in sorted((art / "Parts").glob("*.fbx"))]
    jobs += [(f, CHARS_PATH, True) for f in sorted((art / "Characters").glob("*.fbx"))]
    # The FbxImportUI options above drive the classic FBX importer; ask for it where Interchange handles FBX.
    unreal.SystemLibrary.execute_console_command(None, "Interchange.FeatureFlags.Import.FBX 0")
    tools = unreal.AssetToolsHelpers.get_asset_tools()
    with unreal.ScopedSlowTask(len(jobs), "Exodus: importing slice art") as slow:
        slow.make_dialog(False)
        for fbx, dest, skeletal in jobs:
            slow.enter_progress_frame(1, f"Importing {fbx.name}")
            tools.import_asset_tasks([_fbx_task(fbx, dest, skeletal)])
    missing = [fbx.stem for fbx, dest, _s in jobs if not unreal.EditorAssetLibrary.does_asset_exist(f"{dest}/{fbx.stem}")]
    if missing:
        unreal.log_warning(f"[Exodus] Not imported (stand-in shapes will be used): {', '.join(missing)}")
    log(f"Imported {len(jobs) - len(missing)} / {len(jobs)} FBX files")
    import_animations(tools)


# --------------------------------------------------------------------------- 2. materials
def material_for(style, cache={}):
    if style in cache:
        return cache[style]
    path = f"{MAT_PATH}/MI_Greybox_{style.capitalize()}"
    mi = unreal.EditorAssetLibrary.load_asset(path) if unreal.EditorAssetLibrary.does_asset_exist(path) else None
    if mi is None:
        mi = unreal.AssetToolsHelpers.get_asset_tools().create_asset(
            f"MI_Greybox_{style.capitalize()}", MAT_PATH, unreal.MaterialInstanceConstant, unreal.MaterialInstanceConstantFactoryNew())
        unreal.MaterialEditingLibrary.set_material_instance_parent(mi, unreal.load_asset(SHAPE_MATERIAL))
    r, g, b = STYLE_COLORS.get(style, (0.5, 0.5, 0.5))
    unreal.MaterialEditingLibrary.set_material_instance_vector_parameter_value(mi, "Color", unreal.LinearColor(r, g, b, 1.0))
    unreal.EditorAssetLibrary.save_loaded_asset(mi)
    cache[style] = mi
    return mi


# --------------------------------------------------------------------------- 3. map
def vec(v):
    return unreal.Vector(float(v[0]), float(v[1]), float(v[2]))


def spawn(cls, location, yaw=0.0, label=None, folder=None):
    actors = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
    a = actors.spawn_actor_from_class(cls, vec(location), unreal.Rotator(roll=0.0, pitch=0.0, yaw=float(yaw)))
    if label:
        a.set_actor_label(label)
    if folder:
        a.set_folder_path(folder)
    return a


def spawn_box(b, meshes):
    a = spawn(unreal.StaticMeshActor, b["center"], b["yaw"], b["name"], f"Slice/Greybox/{b['style']}")
    smc = a.static_mesh_component
    smc.set_static_mesh(meshes[b["shape"]])
    smc.set_material(0, material_for(b["style"]))
    sx, sy, sz = (s / 100.0 for s in b["size"])  # engine shapes are 1 m
    a.set_actor_scale3d(unreal.Vector(sx, sy, sz))
    return a


def apply_props(actor, cls_name, name, props):
    if cls_name in ("ExoMarker", "ExoMissionTrigger", "ExoHordeZone", "ExoInteractableActor", "ExoSpawner"):
        actor.set_editor_property("marker_name", props.get("marker_name", name))
    if "extent" in props:
        actor.set_editor_property("extent_cm", vec(props["extent"]))
    for key, value in props.items():
        if key in SKIP_PROPS:
            continue
        if key == "kind" and cls_name == "ExoInteractableActor":
            value = enum_value(unreal.ExoInteractKind, value)
        elif key == "hollow_type":
            value = enum_value(unreal.ExoHollowType, value)
        elif key in ("destination", "door_size"):
            value = vec(value)
        elif key == "prompt":
            value = unreal.Text(value)
        elif key == "barks":
            value = [str(v) for v in value]
        actor.set_editor_property(key, value)


def spawn_actor(entry):
    cls_name, name, props = entry["class"], entry["name"], entry.get("props", {})
    if cls_name == "NavMeshBoundsVolume":
        return None  # added last, after the geometry exists
    cls = getattr(unreal, cls_name)
    folder = {"ExoSpawner": "Slice/Spawners", "ExoCompanion": "Slice/Companions", "ExoMissionTrigger": "Slice/Triggers",
              "ExoHordeZone": "Slice/HordeZones", "ExoInteractableActor": "Slice/Interactables"}.get(cls_name, "Slice/Markers")
    a = spawn(cls, entry["location"], entry.get("yaw", 0.0), name, folder)
    apply_props(a, cls_name, name, props)
    return a


def spawn_environment():
    sun = spawn(unreal.DirectionalLight, (0, 0, 50000), 0.0, "ExoSun", "Slice/Lighting")
    sun.root_component.set_mobility(unreal.ComponentMobility.MOVABLE)
    sun.set_editor_property("tags", [unreal.Name("ExoSun")])
    sun.light_component.set_editor_property("atmosphere_sun_light", True)
    sun.light_component.set_editor_property("intensity", 8.0)
    spawn(unreal.SkyAtmosphere, (0, 0, 0), 0.0, "SkyAtmosphere", "Slice/Lighting")
    sky = spawn(unreal.SkyLight, (0, 0, 60000), 0.0, "SkyLight", "Slice/Lighting")
    sky.root_component.set_mobility(unreal.ComponentMobility.MOVABLE)
    sky.light_component.set_editor_property("real_time_capture", True)
    fog = spawn(unreal.ExponentialHeightFog, (0, 0, 0), 0.0, "HeightFog", "Slice/Lighting")
    fog.component.set_editor_property("fog_density", 0.01)
    fog.component.set_editor_property("enable_volumetric_fog", True)
    spawn(unreal.VolumetricCloud, (0, 0, 0), 0.0, "Clouds", "Slice/Lighting")
    ppv = spawn(unreal.PostProcessVolume, (0, 0, 0), 0.0, "PostProcess", "Slice/Lighting")
    ppv.set_editor_property("unbound", True)


def build_map(layout):
    les = unreal.get_editor_subsystem(unreal.LevelEditorSubsystem)
    actor_sub = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
    if unreal.EditorAssetLibrary.does_asset_exist(MAP):
        # Rebuild in place (the map may be the one open right now): load it and clear everything we placed.
        les.load_level(MAP)
        old = [a for a in actor_sub.get_all_level_actors() if not isinstance(a, (unreal.WorldSettings, unreal.Brush))
               or isinstance(a, unreal.NavMeshBoundsVolume)]
        actor_sub.destroy_actors(old)
    elif not les.new_level(MAP):
        raise RuntimeError(f"Could not create {MAP}")
    meshes = {k: unreal.load_asset(v) for k, v in ENGINE_SHAPES.items()}

    terrain = spawn(unreal.ExoTerrain, (0, 0, 0), 0.0, "Terrain_KestrelValley", "Slice")
    terrain.set_editor_property("material", material_for("terrain"))
    terrain.rebuild()

    boxes, actors = layout["boxes"], layout["actors"]
    with unreal.ScopedSlowTask(len(boxes) + len(actors), "Exodus: building L_VerticalSlice") as slow:
        slow.make_dialog(False)
        for b in boxes:
            slow.enter_progress_frame(1, b["name"])
            spawn_box(b, meshes)
        for entry in actors:
            slow.enter_progress_frame(1, entry["name"])
            try:
                spawn_actor(entry)
            except Exception as exc:  # keep building; report every problem at the end of the log
                unreal.log_error(f"[Exodus] {entry['class']} {entry['name']}: {exc}")
    spawn_environment()

    nav = next(a for a in actors if a["class"] == "NavMeshBoundsVolume")
    vol = spawn(unreal.NavMeshBoundsVolume, nav["location"], 0.0, nav["name"], "Slice")
    sx, sy, sz = (s / 200.0 for s in nav["props"]["size"])  # the default brush is 2 m across
    vol.set_actor_scale3d(unreal.Vector(sx, sy, sz))
    log(f"Placed terrain, {len(boxes)} boxes and {len(actors)} actors")


# --------------------------------------------------------------------------- 4. navmesh + save
_pending = {}


def _wait_for_nav(_dt):
    world = unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_editor_world()
    _pending["ticks"] = _pending.get("ticks", 0) + 1
    try:
        building = unreal.NavigationSystemV1.is_navigation_being_built(world)
    except Exception:
        building = _pending["ticks"] < 600
    if _pending["ticks"] < 30 or (building and _pending["ticks"] < 20000):
        return
    unreal.unregister_slate_post_tick_callback(_pending.pop("handle"))
    _pending.clear()
    unreal.get_editor_subsystem(unreal.LevelEditorSubsystem).save_current_level()
    log(f"Saved {MAP}. Press Play (Alt+P) to start the slice at the Cold Open.")
    unreal.EditorDialog.show_message("Exodus", "The vertical slice is built and saved.\nPress Play to start at the Cold Open.",
                                     unreal.AppMsgType.OK)


def build(reimport=True):
    layout = json.loads((project_dir() / "Content" / "Exodus" / "Data" / "slice_layout.json").read_text(encoding="utf-8"))
    if reimport or not unreal.EditorAssetLibrary.does_directory_exist(PARTS_PATH):
        import_art()
    build_map(layout)
    unreal.get_editor_subsystem(unreal.LevelEditorSubsystem).save_current_level()
    world = unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_editor_world()
    unreal.SystemLibrary.execute_console_command(world, "RebuildNavigation")
    if "handle" not in _pending:
        _pending["handle"] = unreal.register_slate_post_tick_callback(_wait_for_nav)
    log("Building the navmesh; the map saves again when it finishes")


def map_exists():
    return unreal.EditorAssetLibrary.does_asset_exist(MAP)
