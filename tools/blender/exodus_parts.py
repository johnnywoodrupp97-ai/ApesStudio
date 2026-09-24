"""EXODUS PROTOCOL — Blender parts toolkit (Blender 4.2+).

Creates standards-compliant starter files for every part in the Parts Bible, validates
finished files against their budgets, and exports them for the engine.

Command line (from the repository root):

    blender -b -P tools/blender/exodus_parts.py -- scaffold --asset SM_STR_ArmorBlock_Light_LG
    blender -b -P tools/blender/exodus_parts.py -- scaffold --part PWR-010
    blender -b -P tools/blender/exodus_parts.py -- scaffold --category LIF
    blender -b -P tools/blender/exodus_parts.py -- scaffold --all
    blender -b -P tools/blender/exodus_parts.py -- validate assets/parts/power/SM_PWR_Battery_LG.blend
    blender -b -P tools/blender/exodus_parts.py -- export   assets/parts/power/SM_PWR_Battery_LG.blend
    blender -b -P tools/blender/exodus_parts.py -- list --category PRO

Options: --data <parts.json> (default docs/parts-bible/data/parts.json), --out <root>
(default: repository root), --force (overwrite existing .blend files: off by default so
artists' work is never replaced).

Inside Blender: open this file in the Text Editor and press Run Script. An "EXODUS" tab
appears in the 3D View sidebar (N) with Scaffold / Validate / Export buttons.

The same file also runs with the stand-alone ``bpy`` Python module
(``python tools/blender/exodus_parts.py scaffold --asset ...``).
"""

import argparse
import json
import math
import os
import re
import sys
from pathlib import Path

import bpy  # must be imported before bmesh/mathutils when running as a stand-alone module
import bmesh
from mathutils import Matrix, Vector

TOOL_VERSION = "1.0"
FACE_VECTORS = {
    "front": Vector((1, 0, 0)), "back": Vector((-1, 0, 0)),
    "left": Vector((0, 1, 0)), "right": Vector((0, -1, 0)),
    "top": Vector((0, 0, 1)), "bottom": Vector((0, 0, -1)),
    "center": Vector((0, 0, 0)),
}
# Axis along which multiple sockets on one face are spread (unit-cube coords).
FACE_SPREAD_AXIS = {"front": 1, "back": 1, "left": 0, "right": 0, "top": 1, "bottom": 1, "center": 1}
CATEGORY_COLORS = {
    "STR": (0.55, 0.57, 0.60), "DOR": (0.85, 0.55, 0.15), "PWR": (0.95, 0.80, 0.20),
    "LIF": (0.30, 0.65, 0.95), "PRD": (0.60, 0.45, 0.30), "AGR": (0.35, 0.75, 0.30),
    "LOG": (0.95, 0.50, 0.10), "PRO": (0.90, 0.30, 0.25), "MEC": (0.50, 0.50, 0.75),
    "CTL": (0.30, 0.80, 0.75), "COL": (0.85, 0.65, 0.55), "MED": (0.95, 0.95, 0.95),
    "DEF": (0.70, 0.20, 0.20), "UTL": (0.75, 0.75, 0.35), "SOW": (0.20, 0.85, 0.80),
}
ALLOWED_PREFIXES = ("UCX_", "SOCKET_", "MOUNT_", "PART_", "REF_")


# --------------------------------------------------------------------------- data
def repo_root():
    here = Path(__file__).resolve()
    for parent in [here.parent] + list(here.parents):
        if (parent / "docs" / "parts-bible").exists():
            return parent
    return Path.cwd()


def load_data(path=None):
    path = Path(path) if path else repo_root() / "docs" / "parts-bible" / "data" / "parts.json"
    with open(path, encoding="utf-8") as fh:
        data = json.load(fh)
    index = {}
    for part in data["parts"]:
        for asset in part["assets"]:
            index[asset["asset"]] = (part, asset)
    return data, index


def pascal(text):
    text = text.replace("×", "x").replace("&", "And").replace("'", "")
    return "".join(p[:1].upper() + p[1:] for p in re.split(r"[^0-9A-Za-z]+", text) if p)


def socket_instances(part):
    """Expand socket specs into named instances with unit-cube positions."""
    out = []
    for s in part["sockets"]:
        n = s["count"]
        for i in range(n):
            pos = FACE_VECTORS[s["face"]] * 0.5
            if n > 1:
                offset = (i + 0.5) / n - 0.5
                pos = pos.copy()
                pos[FACE_SPREAD_AXIS[s["face"]]] += offset * 0.8
            out.append({
                "name": f"SOCKET_{pascal(s['type'])}_{pascal(s['face'])}_{i + 1:02d}",
                "type": s["type"], "face": s["face"], "unit_pos": pos,
            })
    return out


# --------------------------------------------------------------------------- shapes
def _box(x0, x1, y0, y1, z0, z1):
    return [Vector((x, y, z)) for x in (x0, x1) for y in (y0, y1) for z in (z0, z1)]


def shape_points(shape):
    """Point clouds (unit cube, -0.5..0.5, X=depth/front, Y=width/left, Z=height) whose
    convex hull is the blockout. Returns None for shapes built another way."""
    h = 0.5
    cube = _box(-h, h, -h, h, -h, h)
    if shape in ("box", "cube"):
        return cube
    if shape == "half":
        return _box(-h, h, -h, h, -h, 0)
    if shape == "slope":
        return _box(-h, h, -h, h, -h, -h) + [Vector((-h, y, h)) for y in (-h, h)]
    if shape == "corner":
        return [Vector((-h, -h, -h)), Vector((h, -h, -h)), Vector((-h, h, -h)), Vector((-h, -h, h))]
    if shape in ("inv_corner", "round_inv_corner"):
        return [p for p in cube if not (p.x > 0 and p.y > 0 and p.z > 0)]
    if shape == "slope2_base":
        return (_box(-h, h, -h, h, -h, -h) + [Vector((-h, y, h)) for y in (-h, h)]
                + [Vector((h, y, 0)) for y in (-h, h)])
    if shape == "slope2_tip":
        return _box(-h, h, -h, h, -h, -h) + [Vector((-h, y, 0)) for y in (-h, h)]
    if shape == "corner2_base":
        return [Vector(v) for v in ((-h, -h, -h), (-h, h, -h), (-h, -h, h), (h, -h, -h), (h, 0, -h), (h, -h, 0))]
    if shape == "corner2_tip":
        return [Vector(v) for v in ((-h, -h, -h), (-h, 0, -h), (-h, -h, 0), (h, -h, -h))]
    if shape == "inv_corner2_base":
        pts = [p for p in cube if not (p.y > 0 and p.z > 0)]
        return pts + [Vector((h, h, -h)), Vector((h, -h, h)), Vector((-h, 0, h)), Vector((-h, h, 0))]
    if shape == "inv_corner2_tip":
        pts = [p for p in cube if not (p.x > 0 and p.y > 0 and p.z > 0)]
        return pts + [Vector((h, 0, h)), Vector((h, h, 0))]
    if shape == "round_slope":
        pts = [Vector((-h, y, -h)) for y in (-h, h)]
        for i in range(9):
            t = (math.pi / 2) * i / 8
            for y in (-h, h):
                pts.append(Vector((-h + math.cos(t), y, -h + math.sin(t))))
        return pts
    if shape == "round_corner":
        pts = [Vector((-h, -h, -h))]
        for i in range(9):
            for j in range(9):
                a, b = (math.pi / 2) * i / 8, (math.pi / 2) * j / 8
                pts.append(Vector((-h + math.cos(a) * math.cos(b), -h + math.sin(a) * math.cos(b), -h + math.sin(b))))
        return pts
    if shape == "panel":
        return _box(-h, -h + 0.1, -h, h, -h, h)
    if shape == "panel_top":
        return _box(-h, h, -h, h, h - 0.1, h)
    if shape == "panel_slope":
        t = 0.14
        pts = []
        for y in (-h, h):
            pts += [Vector((h, y, -h)), Vector((-h, y, h)), Vector((h - t, y, -h)), Vector((-h, y, h - t))]
        return pts
    if shape == "flat":
        return _box(-h, h, -h, h, -h, -h + 0.1)
    if shape == "wall":
        return _box(-h, -h + 0.12, -h, h, -h, h)
    if shape == "floor":
        return _box(-h, h, -h, h, -h, -h + 0.02)
    return None


def _box_uvs(bm, dims):
    """Box-projected placeholder UVs: UV0 'UVMap' (trims/atlas) and UV1 'Masks' (damage/dirt/Bloom masks)."""
    layers = [bm.loops.layers.uv.new("UVMap"), bm.loops.layers.uv.new("Masks")]
    for face in bm.faces:
        n = face.normal
        axis = max(range(3), key=lambda k: abs(n[k]))
        u_axis, v_axis = [(1, 2), (0, 2), (0, 1)][axis]
        for loop in face.loops:
            co = loop.vert.co
            uv = (co[u_axis] / max(dims[u_axis], 1e-6) + 0.5, co[v_axis] / max(dims[v_axis], 1e-6) + 0.5)
            for layer in layers:
                loop[layer].uv = uv


def build_blockout(name, shape, dims):
    """Mesh sized to ``dims`` (X, Y, Z metres) centred on the origin."""
    bm = bmesh.new()
    scale = Matrix.Diagonal(Vector((dims[0], dims[1], dims[2], 1.0)))
    if shape == "cylinder":
        r = 0.5 * min(dims[0], dims[1])
        bmesh.ops.create_cone(bm, cap_ends=True, cap_tris=False, segments=16, radius1=r, radius2=r, depth=dims[2])
    else:
        pts = shape_points(shape) or shape_points("box")
        unique = list({tuple(round(c, 6) for c in p): p for p in pts}.values())
        verts = [bm.verts.new(p) for p in unique]
        res = bmesh.ops.convex_hull(bm, input=verts, use_existing_faces=False)
        junk = list({v for v in res["geom_interior"] + res["geom_unused"] if isinstance(v, bmesh.types.BMVert)})
        if junk:
            bmesh.ops.delete(bm, geom=junk, context="VERTS")
        bmesh.ops.dissolve_limit(bm, angle_limit=math.radians(0.5), verts=bm.verts[:], edges=bm.edges[:])
        bmesh.ops.transform(bm, matrix=scale, verts=bm.verts[:])
    bm.normal_update()
    _box_uvs(bm, dims)
    me = bpy.data.meshes.new(name)
    bm.to_mesh(me)
    bm.free()
    return me


# --------------------------------------------------------------------------- scene helpers
def new_collection(name, parent):
    col = bpy.data.collections.new(name)
    parent.children.link(col)
    return col


def new_empty(name, col, display="PLAIN_AXES", size=0.25, location=(0, 0, 0)):
    obj = bpy.data.objects.new(name, None)
    obj.empty_display_type = display
    obj.empty_display_size = size
    obj.location = location
    col.objects.link(obj)
    return obj


def look_rotation(direction):
    """Rotation that points an empty's +X along ``direction``."""
    if direction.length == 0:
        return (0, 0, 0)
    return direction.to_track_quat("X", "Z").to_euler()


def blockout_material(part):
    name = f"MI_{part['art_set']}_Blockout_{part['category']}"
    mat = bpy.data.materials.get(name) or bpy.data.materials.new(name)
    r, g, b = CATEGORY_COLORS.get(part["category"], (0.6, 0.6, 0.6))
    mat.diffuse_color = (r, g, b, 1.0)
    return mat


def set_units(scene):
    us = scene.unit_settings
    us.system = "METRIC"
    us.length_unit = "METERS"
    us.scale_length = 1.0


# --------------------------------------------------------------------------- scaffold
def scaffold(asset_name, data, index, out_root, force=False):
    part, asset = index[asset_name]
    target = Path(out_root) / asset["blend_path"]
    if target.exists() and not force:
        print(f"SKIP  {asset_name}: {target} exists (use --force to overwrite)")
        return None

    bpy.ops.wm.read_factory_settings(use_empty=True)
    scene = bpy.context.scene
    scene.name = asset_name
    set_units(scene)
    std = data["standards"]
    cell = std["cell_m"][asset["grid"]]
    w, h, d = asset["size_cells"]
    dims = Vector((d * cell, w * cell, h * cell))  # X=depth, Y=width, Z=height
    unit = lambda p: Vector((p.x * dims.x, p.y * dims.y, p.z * dims.z))  # noqa: E731

    root_col = new_collection(asset_name, scene.collection)
    lods = [new_collection(f"{asset_name}_LOD{i}", root_col) for i in range(4)]
    stages_col = new_collection(f"{asset_name}_BuildStages", root_col)
    for i in range(1, part["build_stages"] + 1):
        new_collection(f"{asset_name}_BS{i}", stages_col)
    coll_col = new_collection(f"{asset_name}_Collision", root_col)
    sock_col = new_collection(f"{asset_name}_Sockets", root_col)
    mount_col = new_collection(f"{asset_name}_Mounts", root_col)
    parts_col = new_collection(f"{asset_name}_Parts", root_col)
    ref_col = new_collection(f"{asset_name}_Reference", root_col)

    # Root empty with metadata (read by validate/export).
    root = new_empty(asset_name, root_col, "CUBE", 0.5 * min(dims))
    meta = {
        "exodus_tool_version": TOOL_VERSION,
        "asset": asset_name, "part_id": part["id"], "registry_id": part["registry_id"],
        "part_name": part["name"], "variant": asset["variant"] or "", "grid": asset["grid"],
        "size_cells": list(asset["size_cells"]), "dims_m": [round(v, 4) for v in dims],
        "tier": asset["tier"], "art_set": part["art_set"], "complexity": part["complexity"],
        "lod_tris": list(asset["lod_tris"]), "build_stages": part["build_stages"],
        "collision_max_hulls": part["collision_max_hulls"],
        "mount_faces": list(part["mount_faces"]), "airtight_faces": list(part["airtight_faces"]),
        "texel_density_px_per_m": asset["texel_density_px_per_m"], "shape": asset["shape"],
    }
    for k, v in meta.items():
        root[k] = v

    # LOD0 blockout.
    me = build_blockout(f"{asset_name}_LOD0", asset["shape"], dims)
    me.materials.append(blockout_material(part))
    lod0 = bpy.data.objects.new(f"{asset_name}_LOD0", me)
    lods[0].objects.link(lod0)
    lod0.parent = root

    # Collision: one hull matching the blockout (artists split it into ≤ N hulls).
    cme = build_blockout(f"UCX_{asset_name}_01", asset["shape"], dims)
    ucx = bpy.data.objects.new(f"UCX_{asset_name}_01", cme)
    ucx.display_type = "WIRE"
    ucx.hide_render = True
    coll_col.objects.link(ucx)
    ucx.parent = root

    # Sockets.
    size = 0.2 * cell
    for s in socket_instances(part):
        e = new_empty(s["name"], sock_col, "ARROWS", size, unit(s["unit_pos"]))
        e.rotation_euler = look_rotation(FACE_VECTORS[s["face"]])
        e["socket_type"] = s["type"]
        e.parent = root

    # Mount faces (+X of each empty points out of the face).
    for face in part["mount_faces"]:
        e = new_empty(f"MOUNT_{pascal(face)}", mount_col, "SINGLE_ARROW", 0.35 * cell, unit(FACE_VECTORS[face] * 0.5))
        e.rotation_euler = look_rotation(FACE_VECTORS[face])
        e["airtight"] = face in part["airtight_faces"]
        e.parent = root

    # Moving-part pivots.
    for i, text in enumerate(part["moving_parts"]):
        label = text.split(":", 1)[0]
        e = new_empty(f"PART_{pascal(label)[:40] or f'Part{i + 1}'}", parts_col, "SPHERE", 0.1 * cell)
        e["motion"] = text
        e.parent = root

    # Reference (never exported): exact grid volume and a 1.8 m human for scale.
    vol = bpy.data.objects.new(f"REF_{asset_name}_Volume", build_blockout(f"REF_{asset_name}_Volume", "box", dims))
    vol.display_type = "WIRE"
    vol.hide_render = True
    vol.hide_select = True
    ref_col.objects.link(vol)
    human_me = build_blockout("REF_Human_1p8m", "cylinder", Vector((0.5, 0.5, 1.8)))
    human = bpy.data.objects.new("REF_Human_1p8m", human_me)
    human.location = (dims.x / 2 + 0.6, 0, -dims.z / 2 + 0.9)
    human.display_type = "WIRE"
    human.hide_render = True
    ref_col.objects.link(human)

    # Notes text block for the artist.
    txt = bpy.data.texts.new("EXODUS_NOTES")
    txt.write(f"{asset_name}\n{part['id']} {part['name']} ({asset['variant'] or 'base'}) — {asset['grid']}\n\n")
    txt.write(f"Function: {part['function']}\n\nModeling notes: {part['modeling_notes']}\n")
    if asset.get("variant_notes"):
        txt.write(f"Variant notes: {asset['variant_notes']}\n")
    txt.write(f"\nBudgets (tris LOD0-3): {asset['lod_tris']}\nBuild stages: {part['build_stages']}\n"
              f"Collision hulls: <= {part['collision_max_hulls']}\nMoving parts: {part['moving_parts']}\n"
              f"Emissive: {part['emissive']}\nVFX: {part['vfx']}\n")

    target.parent.mkdir(parents=True, exist_ok=True)
    bpy.ops.wm.save_as_mainfile(filepath=str(target), check_existing=False)
    print(f"OK    {asset_name} -> {target}")
    return target


# --------------------------------------------------------------------------- validate
def tri_count(obj):
    return sum(len(p.vertices) - 2 for p in obj.data.polygons)


def world_bounds(obj):
    pts = [obj.matrix_world @ Vector(c) for c in obj.bound_box]
    return (Vector((min(p[i] for p in pts) for i in range(3))), Vector((max(p[i] for p in pts) for i in range(3))))


def validate_scene(data=None, index=None):
    """Validate the open scene. Returns (errors, warnings, info)."""
    errors, warnings, info = [], [], []
    bpy.context.view_layer.update()  # refresh world matrices after any unapplied edits
    roots = [o for o in bpy.data.objects if o.type == "EMPTY" and "exodus_tool_version" in o.keys()]
    if len(roots) != 1:
        return [f"Expected exactly one EXODUS root empty, found {len(roots)}"], warnings, info
    root = roots[0]
    name = root["asset"]
    info.append(f"Asset {name} ({root['part_id']} {root['part_name']})")

    # Keep metadata in sync with the current catalog when available.
    budgets = list(root["lod_tris"])
    if index and name in index:
        part, asset = index[name]
        budgets = asset["lod_tris"]
        if list(root["size_cells"]) != list(asset["size_cells"]):
            errors.append(f"Size changed in catalog: file {list(root['size_cells'])} vs catalog {asset['size_cells']}")
        expected_sockets = {s["name"] for s in socket_instances(part)}
    else:
        expected_sockets = set()

    us = bpy.context.scene.unit_settings
    if us.system != "METRIC" or abs(us.scale_length - 1.0) > 1e-6:
        errors.append("Scene units must be Metric with Unit Scale 1.0")
    if root.location.length > 1e-5 or any(abs(v) > 1e-5 for v in root.rotation_euler) or any(abs(v - 1) > 1e-5 for v in root.scale):
        errors.append("Root empty must sit at the origin with no rotation or scale")

    dims = Vector(root["dims_m"])
    tol = 0.002
    for i in range(4):
        obj = bpy.data.objects.get(f"{name}_LOD{i}")
        if obj is None or obj.type != "MESH":
            (errors if i == 0 else warnings).append(f"Missing mesh {name}_LOD{i}")
            continue
        if any(abs(v - 1) > 1e-5 for v in obj.scale) or any(abs(v) > 1e-5 for v in obj.rotation_euler):
            errors.append(f"{obj.name}: apply rotation and scale")
        tris = tri_count(obj)
        limit = budgets[i]
        if tris > limit * 1.10:
            errors.append(f"{obj.name}: {tris:,} tris exceeds budget {limit:,} by more than 10%")
        elif tris > limit:
            warnings.append(f"{obj.name}: {tris:,} tris is over budget {limit:,} (within 10% tolerance)")
        else:
            info.append(f"{obj.name}: {tris:,} / {limit:,} tris")
        if not obj.data.uv_layers:
            errors.append(f"{obj.name}: no UV map")
        elif i <= 1 and len(obj.data.uv_layers) < 2:
            warnings.append(f"{obj.name}: missing UV1 'Masks' (damage/dirt/Bloom masks)")
        for slot in obj.material_slots:
            if not slot.material:
                errors.append(f"{obj.name}: empty material slot")
            elif not slot.material.name.startswith("MI_"):
                errors.append(f"{obj.name}: material '{slot.material.name}' must start with MI_")
            elif "_Blockout_" in slot.material.name and i == 0:
                warnings.append(f"{obj.name}: still uses the blockout material")
        lo, hi = world_bounds(obj)
        allow = bool(root.get("allow_overhang", False))
        if not allow and any(hi[k] > dims[k] / 2 + tol or lo[k] < -dims[k] / 2 - tol for k in range(3)):
            errors.append(f"{obj.name}: extends outside the {tuple(round(v, 3) for v in dims)} m grid volume "
                          "(set custom property allow_overhang on the root if intentional)")

    ucx = [o for o in bpy.data.objects if o.name.startswith(f"UCX_{name}_")]
    if not ucx:
        errors.append("No collision hulls (UCX_<asset>_NN)")
    elif len(ucx) > root["collision_max_hulls"]:
        errors.append(f"{len(ucx)} collision hulls exceeds the maximum of {root['collision_max_hulls']}")
    else:
        info.append(f"Collision hulls: {len(ucx)} / {root['collision_max_hulls']}")

    present = {o.name for o in bpy.data.objects if o.name.startswith("SOCKET_")}
    for s in sorted(expected_sockets - present):
        errors.append(f"Missing socket {s}")

    for i in range(1, root["build_stages"] + 1):
        col = bpy.data.collections.get(f"{name}_BS{i}")
        if col is None:
            errors.append(f"Missing build-stage collection {name}_BS{i}")
        elif not any(o.type == "MESH" for o in col.all_objects):
            warnings.append(f"Build stage {name}_BS{i} has no mesh yet")

    for obj in bpy.data.objects:
        n = obj.name
        if n == name or n.startswith(ALLOWED_PREFIXES) or re.fullmatch(rf"{re.escape(name)}_(LOD[0-3]|BS\d+(_.+)?|Part_.+)", n):
            continue
        warnings.append(f"Object '{n}' does not follow the naming convention")
    return errors, warnings, info


def validate_file(path, data=None, index=None):
    bpy.ops.wm.open_mainfile(filepath=str(path))
    errors, warnings, info = validate_scene(data, index)
    status = "FAIL" if errors else ("WARN" if warnings else "PASS")
    print(f"\n== {status}: {path}")
    for line in info:
        print(f"   info  {line}")
    for line in warnings:
        print(f"   warn  {line}")
    for line in errors:
        print(f"   ERROR {line}")
    return not errors


# --------------------------------------------------------------------------- export
def export_file(path, out_root):
    bpy.ops.wm.open_mainfile(filepath=str(path))
    roots = [o for o in bpy.data.objects if o.type == "EMPTY" and "exodus_tool_version" in o.keys()]
    if len(roots) != 1:
        raise SystemExit("Not an EXODUS parts file (no root empty)")
    root = roots[0]
    name = root["asset"]
    errors, _w, _i = validate_scene()
    if errors:
        raise SystemExit(f"Refusing to export {name}: validation errors:\n  " + "\n  ".join(errors))

    def select(objs):
        for o in bpy.context.view_layer.objects:
            o.select_set(False)
        for o in objs:
            o.hide_set(False)
            o.select_set(True)

    blend = Path(path)
    cat_dir = blend.parent.name
    export_dir = Path(out_root) / "export" / "parts" / cat_dir
    export_dir.mkdir(parents=True, exist_ok=True)
    fbx_kwargs = dict(use_selection=True, object_types={"MESH", "EMPTY"}, apply_unit_scale=True,
                      apply_scale_options="FBX_SCALE_UNITS", mesh_smooth_type="FACE", use_mesh_modifiers=True,
                      add_leaf_bones=False, bake_anim=False, axis_forward="-Z", axis_up="Y")

    body = [o for o in bpy.data.objects if re.fullmatch(rf"{re.escape(name)}_LOD[0-3]", o.name)
            or o.name.startswith(f"UCX_{name}_") or o.name.startswith("SOCKET_")]
    select(body)
    bpy.ops.export_scene.fbx(filepath=str(export_dir / f"{name}.fbx"), **fbx_kwargs)

    stages = [o for o in bpy.data.objects if re.fullmatch(rf"{re.escape(name)}_BS\d+(_.+)?", o.name) and o.type == "MESH"]
    if stages:
        select(stages)
        bpy.ops.export_scene.fbx(filepath=str(export_dir / f"{name}_BuildStages.fbx"), **fbx_kwargs)

    moving = [o for o in bpy.data.objects if o.name.startswith("PART_") or o.name.startswith(f"{name}_Part_")]
    if any(o.type == "MESH" for o in moving):
        select(moving)
        bpy.ops.export_scene.fbx(filepath=str(export_dir / f"{name}_Parts.fbx"), **fbx_kwargs)

    sidecar = {k: (list(v) if hasattr(v, "__len__") and not isinstance(v, str) else v) for k, v in root.items()}
    sidecar["sockets"] = [{"name": o.name, "type": o.get("socket_type", ""),
                           "location": list(o.matrix_world.translation), "rotation_euler": list(o.matrix_world.to_euler())}
                          for o in bpy.data.objects if o.name.startswith("SOCKET_")]
    sidecar["mounts"] = [{"name": o.name, "airtight": bool(o.get("airtight", False)), "location": list(o.matrix_world.translation)}
                         for o in bpy.data.objects if o.name.startswith("MOUNT_")]
    sidecar["parts"] = [{"name": o.name, "motion": o.get("motion", ""), "pivot": list(o.matrix_world.translation)}
                        for o in bpy.data.objects if o.name.startswith("PART_")]
    (export_dir / f"{name}.meta.json").write_text(json.dumps(sidecar, indent=1), encoding="utf-8")
    print(f"EXPORTED {name} -> {export_dir}")


# --------------------------------------------------------------------------- CLI
def select_assets(args, data, index):
    if args.asset:
        missing = [a for a in args.asset if a not in index]
        if missing:
            raise SystemExit(f"Unknown asset(s): {', '.join(missing)}")
        return list(args.asset)
    names = []
    for part in data["parts"]:
        if args.all or (args.part and part["id"] in args.part) or (args.category and part["category"] in args.category):
            names += [a["asset"] for a in part["assets"]]
    if not names:
        raise SystemExit("Nothing selected: use --asset, --part, --category or --all")
    return names


def main(argv):
    ap = argparse.ArgumentParser(prog="exodus_parts")
    ap.add_argument("command", choices=["scaffold", "validate", "export", "list"])
    ap.add_argument("files", nargs="*", help=".blend files for validate/export")
    ap.add_argument("--asset", nargs="+")
    ap.add_argument("--part", nargs="+")
    ap.add_argument("--category", nargs="+")
    ap.add_argument("--all", action="store_true")
    ap.add_argument("--data")
    ap.add_argument("--out", default=str(repo_root()))
    ap.add_argument("--force", action="store_true")
    args = ap.parse_args(argv)
    data, index = load_data(args.data)

    if args.command == "list":
        for name in select_assets(args, data, index):
            part, asset = index[name]
            print(f"{name:55s} {part['id']}  {asset['grid']}  {asset['size_cells']}  tris {asset['lod_tris'][0]:>6}")
        return 0
    if args.command == "scaffold":
        for name in select_assets(args, data, index):
            scaffold(name, data, index, args.out, args.force)
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


# --------------------------------------------------------------------------- UI (interactive Blender)
class EXODUS_OT_scaffold(bpy.types.Operator):
    bl_idname = "exodus.scaffold"
    bl_label = "Scaffold Asset"
    bl_description = "Create a new starter file for the asset named in the EXODUS panel"

    def execute(self, context):
        wm = context.window_manager
        data, index = load_data(wm.exodus_data_path or None)
        if wm.exodus_asset not in index:
            self.report({"ERROR"}, f"Unknown asset {wm.exodus_asset}")
            return {"CANCELLED"}
        path = scaffold(wm.exodus_asset, data, index, wm.exodus_out_root or str(repo_root()), wm.exodus_force)
        if path:
            bpy.ops.wm.open_mainfile(filepath=str(path))
        return {"FINISHED"}


class EXODUS_OT_validate(bpy.types.Operator):
    bl_idname = "exodus.validate"
    bl_label = "Validate Scene"
    bl_description = "Check the open file against its Parts Bible budgets and naming rules"

    def execute(self, context):
        try:
            data, index = load_data(context.window_manager.exodus_data_path or None)
        except OSError:
            data, index = None, None
        errors, warnings, info = validate_scene(data, index)
        for line in info:
            print("info ", line)
        for line in warnings:
            self.report({"WARNING"}, line)
        for line in errors:
            self.report({"ERROR"}, line)
        if not errors and not warnings:
            self.report({"INFO"}, "PASS")
        return {"FINISHED"}


class EXODUS_PT_panel(bpy.types.Panel):
    bl_label = "EXODUS Parts"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "EXODUS"

    def draw(self, context):
        wm = context.window_manager
        col = self.layout.column()
        col.prop(wm, "exodus_asset")
        col.prop(wm, "exodus_data_path")
        col.prop(wm, "exodus_out_root")
        col.prop(wm, "exodus_force")
        col.operator("exodus.scaffold", icon="MESH_CUBE")
        col.operator("exodus.validate", icon="CHECKMARK")


def register_ui():
    wm = bpy.types.WindowManager
    wm.exodus_asset = bpy.props.StringProperty(name="Asset", default="SM_STR_ArmorBlock_Light_LG")
    wm.exodus_data_path = bpy.props.StringProperty(name="parts.json", subtype="FILE_PATH", default="")
    wm.exodus_out_root = bpy.props.StringProperty(name="Output root", subtype="DIR_PATH", default="")
    wm.exodus_force = bpy.props.BoolProperty(name="Overwrite existing", default=False)
    for cls in (EXODUS_OT_scaffold, EXODUS_OT_validate, EXODUS_PT_panel):
        bpy.utils.register_class(cls)


if __name__ == "__main__":
    if "--" in sys.argv:
        sys.exit(main(sys.argv[sys.argv.index("--") + 1:]))
    elif bpy.app.background or not getattr(bpy.context, "window_manager", None):
        sys.exit(main(sys.argv[1:]))
    else:
        register_ui()
