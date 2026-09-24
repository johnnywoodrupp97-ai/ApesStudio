"""EXODUS PROTOCOL — Blender character toolkit (Blender 4.2+).

Creates rigged starter files for every character asset in the Character Bible, validates
finished work against its tier budgets and rig rules, and exports it for the engine.

    blender -b -P tools/blender/exodus_characters.py -- scaffold --character CST-001
    blender -b -P tools/blender/exodus_characters.py -- scaffold --asset SK_CHR_AdaOkafor_Outfit_FlightSuit
    blender -b -P tools/blender/exodus_characters.py -- scaffold --group HOL CRE
    blender -b -P tools/blender/exodus_characters.py -- scaffold --all
    blender -b -P tools/blender/exodus_characters.py -- validate assets/characters/story-cast/SK_CHR_AdaOkafor.blend
    blender -b -P tools/blender/exodus_characters.py -- export   assets/characters/story-cast/SK_CHR_AdaOkafor.blend
    blender -b -P tools/blender/exodus_characters.py -- list --group CST

Options: --data <characters.json>, --out <root> (default: repository root), --force.
Existing .blend files are never overwritten without --force.

Also runs with the stand-alone ``bpy`` module: ``python tools/blender/exodus_characters.py scaffold ...``.
"""

import argparse
import json
import math
import re
import sys
from pathlib import Path

import bpy  # must be imported before bmesh/mathutils when running as a stand-alone module
import bmesh
from mathutils import Matrix, Vector

TOOL_VERSION = "1.0"
HERE = Path(__file__).resolve()


def repo_root():
    for parent in [HERE.parent] + list(HERE.parents):
        if (parent / "tools" / "characters" / "skeletons.py").exists():
            return parent
    return Path.cwd()


sys.path.insert(0, str(repo_root() / "tools" / "characters"))
import skeletons as SK  # noqa: E402

ALLOWED_EXTRA_BONE_PREFIXES = ("bloom_", "sac_", "plate_", "claw_", "tendril_", "growth_", "chimney_", "heart", "jaw_unhinge",
                               "wing_blade", "cannon_", "cockpit", "pilot_", "shears_", "prosthetic_", "finger_", "x_")

# Humanoid proxy radii (metres at 1.80 m, bulk 1.0): (lateral, depth)
HUMANOID_RADII = {
    "pelvis": (0.15, 0.11), "spine_01": (0.14, 0.10), "spine_02": (0.145, 0.10), "spine_03": (0.16, 0.105),
    "spine_04": (0.17, 0.11), "spine_05": (0.16, 0.10), "neck_01": (0.055, 0.055), "neck_02": (0.05, 0.05),
    "head": (0.085, 0.10), "clavicle": (0.045, 0.045), "upperarm": (0.05, 0.05), "lowerarm": (0.04, 0.04),
    "hand": (0.045, 0.02), "thigh": (0.08, 0.08), "calf": (0.055, 0.055), "foot": (0.045, 0.03), "ball": (0.045, 0.02),
}
GROUP_RADIUS = {"spine": 0.11, "core": 0.0, "head": 0.07, "tail": 0.04, "leg": 0.035, "wing": 0.012, "fin": 0.03,
                "rotor": 0.05, "weapon": 0.03, "ribbon": 0.01}


# --------------------------------------------------------------------------- data
def load_data(path=None):
    path = Path(path) if path else repo_root() / "docs" / "character-bible" / "data" / "characters.json"
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    index = {}
    for c in data["characters"]:
        for a in c["assets"]:
            index[a["asset"]] = (c, a)
    return data, index


def required_shapes(c):
    return list(SK.FACIAL_SETS[c["facial_set"]]) + [s.split(" ")[0] for s in c["extra_shapes"] if not s.startswith("body_") and not s.startswith("age_")]


def reference_size(spec):
    return spec.get("height") or spec.get("length") or spec.get("size") or 1.0


# --------------------------------------------------------------------------- geometry
def prism(bm, head, tail, rx, ry, segments=8, vgroup_layer=None, group_index=0):
    head, tail = Vector(head), Vector(tail)
    d = tail - head
    if d.length < 1e-6 or rx <= 0:
        return
    d.normalize()
    ref = Vector((1, 0, 0)) if abs(d.x) < 0.9 else Vector((0, 1, 0))
    u = (ref - d * ref.dot(d)).normalized()
    v = d.cross(u)
    rings = []
    for p in (head, tail):
        ring = []
        for i in range(segments):
            a = 2 * math.pi * i / segments
            vert = bm.verts.new(p + u * (math.cos(a) * rx) + v * (math.sin(a) * ry))
            ring.append(vert)
        rings.append(ring)
    for i in range(segments):
        j = (i + 1) % segments
        bm.faces.new((rings[0][i], rings[0][j], rings[1][j], rings[1][i]))
    caps = [bm.verts.new(head), bm.verts.new(tail)]
    for i in range(segments):  # triangle-fan caps keep the mesh tris/quads only (tangent-space export)
        j = (i + 1) % segments
        bm.faces.new((caps[0], rings[0][j], rings[0][i]))
        bm.faces.new((caps[1], rings[1][i], rings[1][j]))
    if vgroup_layer is not None:
        for vert in rings[0] + rings[1] + caps:
            vert[vgroup_layer][group_index] = 1.0


def proxy_segments(c, bones):
    """(bone_name, head, tail, rx, ry, is_head_part) for the stand-in body."""
    spec = c["skeleton"]
    out = []
    if spec["template"] == "humanoid":
        prof = SK.PROFILES[spec.get("profile", "adult_average")]
        s = spec["height"] / SK.REF_HEIGHT
        for b in bones:
            if not b["deform"]:
                continue
            base = re.sub(r"_(l|r)$", "", b["name"])
            base = "clavicle" if base.startswith("clavicle") else base
            if base not in HUMANOID_RADII:
                continue
            rx, ry = HUMANOID_RADII[base]
            k = prof["head"] if base in ("head", "neck_02") else prof["bulk"]
            lateral = prof["width"] if b["group"] in ("spine", "core") else 1.0
            out.append((b["name"], b["head"], b["tail"], rx * s * k * lateral, ry * s * k, base in ("head", "neck_02")))
    else:
        size = reference_size(spec)
        for b in bones:
            r = GROUP_RADIUS.get(b["group"], 0.02) * size
            if b["deform"] and r > 0:
                out.append((b["name"], b["head"], b["tail"], r, r, b["group"] == "head"))
    return out


def box_uvs(bm):
    uv = bm.loops.layers.uv.new("UVMap")
    bm.loops.layers.uv.new("Masks")
    for f in bm.faces:
        n = f.normal
        axis = max(range(3), key=lambda k: abs(n[k]))
        ua, va = [(1, 2), (0, 2), (0, 1)][axis]
        for loop in f.loops:
            loop[uv].uv = (loop.vert.co[ua] * 0.5 + 0.5, loop.vert.co[va] * 0.5 + 0.5)


def build_proxy_mesh(name, segments, arm_obj):
    """Skinned stand-in mesh: one prism per bone, rigidly weighted (weight 1.0)."""
    me = bpy.data.meshes.new(name)
    obj = bpy.data.objects.new(name, me)
    names = sorted({s[0] for s in segments})
    for n in names:
        obj.vertex_groups.new(name=n)
    bm = bmesh.new()
    deform = bm.verts.layers.deform.verify()
    for bone, h, t, rx, ry, _head in segments:
        prism(bm, h, t, rx, ry, vgroup_layer=deform, group_index=names.index(bone))
    bm.normal_update()
    box_uvs(bm)
    bm.to_mesh(me)
    bm.free()
    mod = obj.modifiers.new("Armature", "ARMATURE")
    mod.object = arm_obj
    obj.parent = arm_obj
    return obj


# --------------------------------------------------------------------------- scene helpers
def new_col(name, parent):
    col = bpy.data.collections.new(name)
    parent.children.link(col)
    return col


def set_units(scene):
    scene.unit_settings.system = "METRIC"
    scene.unit_settings.length_unit = "METERS"
    scene.unit_settings.scale_length = 1.0


def build_armature(c, bones, col):
    arm = bpy.data.armatures.new(f"{c['assets'][0]['asset']}_Skeleton")
    arm.display_type = "OCTAHEDRAL"
    obj = bpy.data.objects.new("Armature", arm)
    col.objects.link(obj)
    obj.show_in_front = True
    vl = bpy.context.view_layer
    vl.objects.active = obj
    obj.select_set(True)
    bpy.ops.object.mode_set(mode="EDIT")
    ebs = {}
    for b in bones:
        eb = arm.edit_bones.new(b["name"])
        eb.head, eb.tail = Vector(b["head"]), Vector(b["tail"])
        eb.use_deform = b["deform"]
        ebs[b["name"]] = eb
    for b in bones:
        if b["parent"]:
            ebs[b["name"]].parent = ebs[b["parent"]]
            ebs[b["name"]].use_connect = False
    bpy.ops.object.mode_set(mode="OBJECT")
    return obj


def add_sockets(c, arm_obj, col):
    spec = c["skeleton"]
    if spec["template"] != "humanoid":
        return []
    s = spec["height"] / SK.REF_HEIGHT
    made = []
    bpy.context.view_layer.update()
    for name, bone, off, purpose in SK.HUMANOID_SOCKETS:
        pb = arm_obj.data.bones.get(bone)
        if pb is None:
            continue
        pos = arm_obj.matrix_world @ (pb.head_local + Vector(off) * s)
        e = bpy.data.objects.new(name, None)
        e.empty_display_type = "ARROWS"
        e.empty_display_size = 0.08 * s
        e["purpose"] = purpose
        col.objects.link(e)
        e.parent = arm_obj
        e.parent_type = "BONE"
        e.parent_bone = bone
        bpy.context.view_layer.update()
        e.matrix_world = Matrix.Translation(pos)
        made.append(e)
    return made


def add_turnaround(c, col):
    size = reference_size(c["skeleton"])
    spec = c["skeleton"]
    height = spec.get("height") or spec.get("shoulder_h", size) * 1.4 or size
    span = max(height, spec.get("length", 0), spec.get("size", 0)) * 1.25
    views = {"Front": (0, -1, 0), "Side": (1, 0, 0), "Back": (0, 1, 0), "ThreeQuarter": (0.7071, -0.7071, 0)}
    for label, d in views.items():
        cam = bpy.data.cameras.new(f"REF_Cam_{label}")
        cam.type = "ORTHO"
        cam.ortho_scale = span
        obj = bpy.data.objects.new(f"REF_Cam_{label}", cam)
        target = Vector((0, 0, height / 2))
        obj.location = target + Vector(d) * (span * 3)
        obj.rotation_euler = (target - obj.location).to_track_quat("-Z", "Y").to_euler()
        col.objects.link(obj)
    # Height bar (1 cm wide) at the character's height, and a 1.8 m human for scale.
    bar = bpy.data.meshes.new("REF_HeightBar")
    bm = bmesh.new()
    bmesh.ops.create_cube(bm, size=1.0)
    bmesh.ops.transform(bm, matrix=Matrix.Diagonal(Vector((0.01, 0.01, height, 1))), verts=bm.verts[:])
    bmesh.ops.translate(bm, vec=Vector((-span / 2, 0, height / 2)), verts=bm.verts[:])
    bm.to_mesh(bar)
    bm.free()
    col.objects.link(bpy.data.objects.new("REF_HeightBar", bar))
    human = bpy.data.meshes.new("REF_Human_1p8m")
    bm = bmesh.new()
    bmesh.ops.create_cone(bm, cap_ends=True, segments=12, radius1=0.2, radius2=0.2, depth=1.8)
    bmesh.ops.translate(bm, vec=Vector((span / 2, 0, 0.9)), verts=bm.verts[:])
    bm.to_mesh(human)
    bm.free()
    h = bpy.data.objects.new("REF_Human_1p8m", human)
    h.display_type = "WIRE"
    col.objects.link(h)


def blockout_material(c):
    name = f"MI_{c['art_set']}_Blockout_{c['group']}"
    mat = bpy.data.materials.get(name) or bpy.data.materials.new(name)
    mat.diffuse_color = {"PLY": (0.95, 0.45, 0.15, 1), "CST": (0.85, 0.7, 0.35, 1), "NOT": (0.55, 0.7, 0.55, 1),
                         "HOL": (0.45, 0.7, 0.35, 1), "FAC": (0.8, 0.8, 0.85, 1), "BOS": (0.75, 0.25, 0.25, 1),
                         "CRE": (0.45, 0.55, 0.8, 1)}.get(c["group"], (0.6, 0.6, 0.6, 1))
    return mat


# --------------------------------------------------------------------------- scaffold
def scaffold(asset_name, data, index, out_root, force=False):
    c, a = index[asset_name]
    if a["kind"] in ("Kit module", "Kit texture"):
        print(f"SKIP  {asset_name}: kit-module families are authored in one kit file per family")
        return None
    target = Path(out_root) / a["blend_path"]
    if target.exists() and not force:
        print(f"SKIP  {asset_name}: {target} exists (use --force to overwrite)")
        return None
    bpy.ops.wm.read_factory_settings(use_empty=True)
    scene = bpy.context.scene
    scene.name = asset_name
    set_units(scene)
    bones = SK.build_skeleton(c["skeleton"])

    root = new_col(asset_name, scene.collection)
    rig_col = new_col(f"{asset_name}_Rig", root)
    lods = [new_col(f"{asset_name}_LOD{i}", root) for i in range(4)]
    sock_col = new_col(f"{asset_name}_Sockets", root)
    ref_col = new_col(f"{asset_name}_Reference", root)

    arm = build_armature(c, bones, rig_col)
    meta = {"exodus_tool_version": TOOL_VERSION, "asset": asset_name, "kind": a["kind"], "character_id": c["id"],
            "character": c["name"], "registry_id": c["registry_id"], "tier": c["tier"], "lod_tris": list(a["lod_tris"]),
            "influences": c["influences"], "facial_set": c["facial_set"], "skeleton": json.dumps(c["skeleton"]),
            "bone_count": len(bones)}
    for k, v in meta.items():
        arm[k] = v

    segs = proxy_segments(c, bones)
    body = [s for s in segs if not s[5]]
    head = [s for s in segs if s[5]]
    mat = blockout_material(c)
    if a["kind"] in ("Base", "Variant"):
        for seg_list, suffix in ((body, "LOD0"), (head, "Head_LOD0")):
            if not seg_list:
                continue
            obj = build_proxy_mesh(f"{asset_name}_{suffix}", seg_list, arm)
            obj.data.materials.append(mat)
            lods[0].objects.link(obj)
    else:
        # Outfit / hair / arms files: the body is reference only; artists skin their piece to the same rig.
        ref = build_proxy_mesh(f"REF_{asset_name}_Body", body + head, arm)
        ref.display_type = "WIRE"
        ref.hide_render = True
        ref_col.objects.link(ref)

    add_sockets(c, arm, sock_col)
    add_turnaround(c, ref_col)

    txt = bpy.data.texts.new("EXODUS_NOTES")
    txt.write(f"{asset_name} — {a['kind']}: {a['label']}\n{c['id']} {c['name']} ({c['tier']}) · {c['size_label']} · {c['skeleton_label']}\n\n")
    txt.write(f"Role: {c['role']}\n\nVisual:\n")
    for k, v in c["visual"].items():
        txt.write(f"  {k}: {v}\n")
    txt.write(f"\nBudgets LOD0-3: {a['lod_tris']} · Max influences: {c['influences']}\nTextures: {c['textures']}\n"
              f"Facial set: {c['facial_set']} ({c['facial_shapes']} shapes) + {c['extra_shapes']}\nNotes: {c['notes']}\n")

    target.parent.mkdir(parents=True, exist_ok=True)
    bpy.ops.wm.save_as_mainfile(filepath=str(target), check_existing=False)
    print(f"OK    {asset_name} -> {target}")
    return target


# --------------------------------------------------------------------------- validate
def tri_count(obj):
    return sum(len(p.vertices) - 2 for p in obj.data.polygons)


def validate_scene(data=None, index=None):
    errors, warnings, info = [], [], []
    bpy.context.view_layer.update()
    arms = [o for o in bpy.data.objects if o.type == "ARMATURE"]
    if len(arms) != 1 or arms[0].name != "Armature" or "exodus_tool_version" not in arms[0].keys():
        return ["Expected exactly one EXODUS armature object named 'Armature'"], warnings, info
    arm = arms[0]
    name = arm["asset"]
    info.append(f"Asset {name} ({arm['character_id']} {arm['character']}, {arm['kind']})")
    c = index[name][0] if index and name in index else None
    spec = json.loads(arm["skeleton"]) if not c else c["skeleton"]
    budgets = list(index[name][1]["lod_tris"]) if c else list(arm["lod_tris"])

    us = bpy.context.scene.unit_settings
    if us.system != "METRIC" or abs(us.scale_length - 1) > 1e-6:
        errors.append("Scene units must be Metric with Unit Scale 1.0")
    if arm.matrix_world != Matrix.Identity(4):
        errors.append("Armature must be at the origin with no rotation or scale")

    # Bones
    expected = {b["name"]: b for b in SK.build_skeleton(spec)}
    have = {b.name: b for b in arm.data.bones}
    for n in expected:
        if n not in have:
            errors.append(f"Missing bone {n}")
        elif have[n].use_deform != expected[n]["deform"]:
            errors.append(f"Bone {n}: deform flag should be {expected[n]['deform']}")
    for n in have:
        if n not in expected and not n.startswith(ALLOWED_EXTRA_BONE_PREFIXES):
            warnings.append(f"Extra bone '{n}' should use an approved prefix (chapter 10, rule 5)")
    if spec["template"] == "humanoid" and "head" in have:
        crown = (arm.matrix_world @ have["head"].tail_local).z
        if abs(crown - spec["height"]) > spec["height"] * 0.02:
            errors.append(f"Head crown at {crown:.3f} m; catalog height is {spec['height']:.2f} m (±2%)")
        else:
            info.append(f"Height {crown:.3f} m (catalog {spec['height']:.2f} m)")

    # Meshes per LOD
    bone_names = set(have)
    for i in range(4):
        col = bpy.data.collections.get(f"{name}_LOD{i}")
        meshes = [o for o in (col.all_objects if col else []) if o.type == "MESH"]
        if not meshes:
            (errors if i == 0 else warnings).append(f"No meshes in {name}_LOD{i}")
            continue
        tris = sum(tri_count(o) for o in meshes)
        limit = budgets[i]
        if tris > limit * 1.10:
            errors.append(f"LOD{i}: {tris:,} tris exceeds budget {limit:,} by more than 10%")
        elif tris > limit:
            warnings.append(f"LOD{i}: {tris:,} tris over budget {limit:,} (within 10%)")
        else:
            info.append(f"LOD{i}: {tris:,} / {limit:,} tris")
        for o in meshes:
            if o.parent != arm or not any(m.type == "ARMATURE" and m.object == arm for m in o.modifiers):
                errors.append(f"{o.name}: must be parented to 'Armature' with an Armature modifier")
            if any(abs(v - 1) > 1e-5 for v in o.scale) or any(abs(v) > 1e-5 for v in o.rotation_euler) or o.location.length > 1e-5:
                errors.append(f"{o.name}: apply transforms")
            if not o.data.uv_layers:
                errors.append(f"{o.name}: no UV map")
            ngons = sum(1 for p in o.data.polygons if len(p.vertices) > 4)
            if ngons:
                warnings.append(f"{o.name}: {ngons} polygons with more than 4 sides (triangulate for tangent-space export)")
            for slot in o.material_slots:
                if not slot.material or not slot.material.name.startswith("MI_"):
                    errors.append(f"{o.name}: material slots must use MI_* materials")
                elif "_Blockout_" in slot.material.name and i == 0:
                    warnings.append(f"{o.name}: still uses the blockout material")
            groups = {g.index: g.name for g in o.vertex_groups}
            for g in groups.values():
                if g not in bone_names:
                    warnings.append(f"{o.name}: vertex group '{g}' has no matching bone")
            over, unweighted, unnormalized = 0, 0, 0
            for v in o.data.vertices:
                ws = [g.weight for g in v.groups if g.weight > 1e-4 and groups.get(g.group) in bone_names]
                if len(ws) > arm["influences"]:
                    over += 1
                if not ws:
                    unweighted += 1
                elif abs(sum(ws) - 1.0) > 0.01:
                    unnormalized += 1
            if over:
                errors.append(f"{o.name}: {over} vertices exceed {arm['influences']} bone influences")
            if unweighted:
                errors.append(f"{o.name}: {unweighted} vertices have no bone weights")
            if unnormalized:
                warnings.append(f"{o.name}: {unnormalized} vertices have weights that don't sum to 1")

    # Facial shape keys (base heads)
    if arm["kind"] in ("Base", "Variant") and c and SK.FACIAL_SETS[c["facial_set"]]:
        head = bpy.data.objects.get(f"{name}_Head_LOD0") or bpy.data.objects.get(f"{name}_LOD0")
        keys = set(head.data.shape_keys.key_blocks.keys()) if head and head.data.shape_keys else set()
        missing = [s for s in required_shapes(c) if s not in keys]
        if missing:
            warnings.append(f"Facial set '{c['facial_set']}': {len(missing)} of {len(required_shapes(c))} shape keys missing "
                            f"(first: {', '.join(missing[:4])})")
        elif head and head.data.shape_keys:
            basis = head.data.shape_keys.reference_key
            flat = [k.name for k in head.data.shape_keys.key_blocks if k != basis and
                    max(((a.co - b.co).length for a, b in zip(k.data, basis.data)), default=0) < 1e-4]
            if flat:
                warnings.append(f"{len(flat)} shape keys don't move any vertices yet (e.g. {flat[0]})")

    for o in bpy.data.objects:
        n = o.name
        if n == "Armature" or n.startswith(("SOCKET_", "REF_")) or n.startswith(name + "_"):
            continue
        warnings.append(f"Object '{n}' does not follow the naming convention")
    return errors, warnings, info


def validate_file(path, data=None, index=None):
    bpy.ops.wm.open_mainfile(filepath=str(path))
    errors, warnings, info = validate_scene(data, index)
    status = "FAIL" if errors else ("WARN" if warnings else "PASS")
    print(f"\n== {status}: {path}")
    for tag, lines in (("info ", info), ("warn ", warnings), ("ERROR", errors)):
        for line in lines:
            print(f"   {tag} {line}")
    return not errors


# --------------------------------------------------------------------------- export
def export_file(path, out_root):
    bpy.ops.wm.open_mainfile(filepath=str(path))
    errors, _w, _i = validate_scene()
    if errors:
        raise SystemExit("Refusing to export: validation errors:\n  " + "\n  ".join(errors))
    arm = bpy.data.objects["Armature"]
    name = arm["asset"]
    blend = Path(path)
    export_dir = Path(out_root) / "export" / "characters" / blend.parent.name
    export_dir.mkdir(parents=True, exist_ok=True)
    kwargs = dict(use_selection=True, object_types={"ARMATURE", "MESH"}, apply_unit_scale=True, apply_scale_options="FBX_SCALE_UNITS",
                  add_leaf_bones=False, bake_anim=False, use_armature_deform_only=False, primary_bone_axis="Y",
                  secondary_bone_axis="X", mesh_smooth_type="FACE", use_tspace=True, axis_forward="-Z", axis_up="Y")
    written = []
    for i in range(4):
        col = bpy.data.collections.get(f"{name}_LOD{i}")
        meshes = [o for o in (col.all_objects if col else []) if o.type == "MESH"]
        if not meshes:
            continue
        for o in bpy.context.view_layer.objects:
            o.select_set(False)
        arm.select_set(True)
        for o in meshes:
            o.select_set(True)
        out = export_dir / (f"{name}.fbx" if i == 0 else f"{name}_LOD{i}.fbx")
        bpy.ops.export_scene.fbx(filepath=str(out), **kwargs)
        written.append(out.name)
    sidecar = {k: (list(v) if hasattr(v, "__len__") and not isinstance(v, str) else v) for k, v in arm.items()}
    sidecar["sockets"] = [{"name": o.name, "bone": o.parent_bone, "purpose": o.get("purpose", ""),
                           "location_world": list(o.matrix_world.translation)} for o in bpy.data.objects if o.name.startswith("SOCKET_")]
    heads = [o for o in bpy.data.objects if o.type == "MESH" and o.data.shape_keys and o.name.startswith(name)]
    sidecar["shape_keys"] = {o.name: [k.name for k in o.data.shape_keys.key_blocks][1:] for o in heads}
    (export_dir / f"{name}.meta.json").write_text(json.dumps(sidecar, indent=1), encoding="utf-8")
    print(f"EXPORTED {name}: {', '.join(written)} -> {export_dir}")


# --------------------------------------------------------------------------- CLI
def select_assets(args, data, index):
    if args.asset:
        missing = [a for a in args.asset if a not in index]
        if missing:
            raise SystemExit(f"Unknown asset(s): {', '.join(missing)}")
        return list(args.asset)
    out = []
    for c in data["characters"]:
        if args.all or (args.character and c["id"] in args.character) or (args.group and c["group"] in args.group):
            out += [a["asset"] for a in c["assets"]]
    if not out:
        raise SystemExit("Nothing selected: use --asset, --character, --group or --all")
    return out


def main(argv):
    ap = argparse.ArgumentParser(prog="exodus_characters")
    ap.add_argument("command", choices=["scaffold", "validate", "export", "list"])
    ap.add_argument("files", nargs="*")
    ap.add_argument("--asset", nargs="+")
    ap.add_argument("--character", nargs="+")
    ap.add_argument("--group", nargs="+")
    ap.add_argument("--all", action="store_true")
    ap.add_argument("--data")
    ap.add_argument("--out", default=str(repo_root()))
    ap.add_argument("--force", action="store_true")
    args = ap.parse_args(argv)
    data, index = load_data(args.data)
    if args.command == "list":
        for n in select_assets(args, data, index):
            c, a = index[n]
            print(f"{n:52s} {c['id']:8s} {a['kind']:11s} {c['tier']:10s} LOD0 {a['lod_tris'][0]:>7,}")
        return 0
    if args.command == "scaffold":
        for n in select_assets(args, data, index):
            scaffold(n, data, index, args.out, args.force)
        return 0
    if not args.files:
        raise SystemExit(f"{args.command} needs one or more .blend files")
    ok = True
    for f in args.files:
        if args.command == "validate":
            ok = validate_file(f, data, index) and ok
        else:
            export_file(f, args.out)
    return 0 if ok else 1


if __name__ == "__main__":
    argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else sys.argv[1:]
    sys.exit(main(argv))
