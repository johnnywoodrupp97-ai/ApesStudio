"""EXODUS PROTOCOL — Blender parts toolkit (Blender 4.2+).

Creates standards-compliant starter files for every part in the Parts Bible, validates
finished files against their budgets, and exports them for the engine.

Command line (from the repository root):

    blender -b -P tools/blender/exodus_parts.py -- scaffold --asset SM_STR_ArmorBlock_Light_LG
    blender -b -P tools/blender/exodus_parts.py -- scaffold --part PWR-010
    blender -b -P tools/blender/exodus_parts.py -- scaffold --category LIF
    blender -b -P tools/blender/exodus_parts.py -- scaffold --all
    blender -b -P tools/blender/exodus_parts.py -- build --all              (complete greybox: every block + prop)
    blender -b -P tools/blender/exodus_parts.py -- build --category PWR
    blender -b -P tools/blender/exodus_parts.py -- build --props            (components, resources, equipment)
    blender -b -P tools/blender/exodus_parts.py -- build --prop multitool iron_ore
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
    text = text.translate(str.maketrans("₀₁₂₃₄₅₆₇₈₉", "0123456789")).replace("×", "x").replace("&", "And").replace("'", "").replace("’", "")
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


def shape_points(shape, res=8):
    """Point clouds (unit cube, -0.5..0.5, X=depth/front, Y=width/left, Z=height) whose
    convex hull is the blockout; ``res`` is the number of steps on curved shapes.
    Returns None for shapes built another way."""
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
        for i in range(res + 1):
            t = (math.pi / 2) * i / res
            for y in (-h, h):
                pts.append(Vector((-h + math.cos(t), y, -h + math.sin(t))))
        return pts
    if shape == "round_corner":
        pts = [Vector((-h, -h, -h))]
        for i in range(res + 1):
            for j in range(res + 1):
                a, b = (math.pi / 2) * i / res, (math.pi / 2) * j / res
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
def scaffold(asset_name, data, index, out_root, force=False, full=False):
    """Create the asset's .blend. ``full`` (the ``build`` command) also generates the complete greybox."""
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
    stage_cols = [new_collection(f"{asset_name}_BS{i}", stages_col) for i in range(1, part["build_stages"] + 1)]
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

    if full:
        build_greybox(asset_name, part, asset, dims, cell, root, lods, stage_cols, parts_col)

    # Notes text block for the artist.
    txt = bpy.data.texts.new("EXODUS_NOTES")
    txt.write(f"{asset_name}\n{part['id']} {part['name']} ({asset['variant'] or 'base'}) — {asset['grid']}\n\n")
    txt.write(f"Function: {part['function']}\n\nModeling notes: {part['modeling_notes']}\n")
    if asset.get("variant_notes"):
        txt.write(f"Variant notes: {asset['variant_notes']}\n")
    txt.write(f"\nBudgets (tris LOD0-3): {asset['lod_tris']}\nBuild stages: {part['build_stages']}\n"
              f"Collision hulls: <= {part['collision_max_hulls']}\nMoving parts: {part['moving_parts']}\n"
              f"Emissive: {part['emissive']}\nVFX: {part['vfx']}\n")

    if full:
        txt.write(f"\nGreybox build {GREYBOX_VERSION}: LOD0-3, build stages and moving parts are generated stand-ins "
                  "at final size and budget. Replace them with final art; keep names, pivots and sockets.\n")

    target.parent.mkdir(parents=True, exist_ok=True)
    bpy.ops.wm.save_as_mainfile(filepath=str(target), check_existing=False, compress=True)
    print(f"{'BUILT' if full else 'OK   '} {asset_name} -> {target}")
    return target


# --------------------------------------------------------------------------- greybox build
# ``build`` turns a scaffold into a complete greybox asset: detailed LOD0 (panel grid, bevels,
# recessed panels), LOD1-3, build-stage meshes, moving-part meshes and greybox materials, all
# inside the part's grid volume and within its triangle budgets.
GREYBOX_VERSION = "1.0"
PANEL_CELLS = {"S": 1.0, "M": 0.5, "L": 0.5, "XL": 0.5}   # panel size in grid cells, by complexity
EMISSIVE_RGB = (0.25, 0.85, 1.0)
SLAB_WORDS = ("door", "leaf", "leaves", "hatch", "slab", "gate", "shutter", "ramp", "segment", "wing", "lid", "flap",
              "plate", "louver", "fin", "panel", "slat", "cover", "bay")
SPIN_WORDS = ("fan", "rotor", "impeller", "turbine", "drum", "roller", "flywheel", "ring", "wheel", "centrifuge",
              "propeller", "blade", "torus", "plasma", "runner", "dish", "spinner", "reel", "spool", "gyro")


def pbr_material(name, rgb, emission=None, metallic=0.3, roughness=0.55):
    mat = bpy.data.materials.get(name)
    if mat:
        return mat
    mat = bpy.data.materials.new(name)
    mat.diffuse_color = (*rgb, 1.0)
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    bsdf.inputs["Base Color"].default_value = (*rgb, 1.0)
    bsdf.inputs["Metallic"].default_value = metallic
    bsdf.inputs["Roughness"].default_value = roughness
    if emission:
        bsdf.inputs["Emission Color"].default_value = (*emission, 1.0)
        bsdf.inputs["Emission Strength"].default_value = 1.5
    return mat


def greybox_materials(art_set, category):
    rgb = CATEGORY_COLORS.get(category, (0.6, 0.6, 0.6))
    return (pbr_material(f"MI_{art_set}_Greybox_{category}", rgb),
            pbr_material(f"MI_{art_set}_Emissive_{category}", (0.05, 0.05, 0.05), emission=EMISSIVE_RGB, metallic=0.0, roughness=0.3),
            pbr_material(f"MI_{art_set}_BuildFrame", (0.85, 0.7, 0.2), metallic=0.6, roughness=0.4))


def hull_bm(shape, dims, res=8, segments=16):
    """Base convex shape scaled to ``dims`` (a fresh BMesh the caller owns)."""
    bm = bmesh.new()
    if shape == "cylinder":
        r = 0.5 * min(dims[0], dims[1])
        bmesh.ops.create_cone(bm, cap_ends=True, cap_tris=False, segments=segments, radius1=r, radius2=r, depth=dims[2])
    else:
        pts = shape_points(shape, res) or shape_points("box")
        unique = list({tuple(round(c, 6) for c in p): p for p in pts}.values())
        verts = [bm.verts.new(p) for p in unique]
        res_ = bmesh.ops.convex_hull(bm, input=verts, use_existing_faces=False)
        junk = list({v for v in res_["geom_interior"] + res_["geom_unused"] if isinstance(v, bmesh.types.BMVert)})
        if junk:
            bmesh.ops.delete(bm, geom=junk, context="VERTS")
        bmesh.ops.dissolve_limit(bm, angle_limit=math.radians(0.5), verts=bm.verts[:], edges=bm.edges[:])
        bmesh.ops.transform(bm, matrix=Matrix.Diagonal(Vector((dims[0], dims[1], dims[2], 1.0))), verts=bm.verts[:])
    bm.normal_update()
    return bm


def bm_tris(bm):
    return sum(len(f.verts) - 2 for f in bm.faces)


def panelize(bm, panel):
    """Straight cuts along each axis so flat faces become a grid of ~``panel``-sized panels."""
    for axis in range(3):
        groups = {}
        for e in bm.edges:
            d = e.verts[1].co - e.verts[0].co
            length = d.length
            if length < 1e-6 or abs(abs(d[axis]) - length) > 1e-5:
                continue
            cuts = min(int(round(length / panel)) - 1, 15)
            if cuts > 0:
                groups.setdefault(cuts, []).append(e)
        for cuts, edges in groups.items():
            bmesh.ops.subdivide_edges(bm, edges=edges, cuts=cuts, use_grid_fill=True)
    bm.normal_update()


def bevel_sharp(bm, width, segments):
    edges = [e for e in bm.edges if e.is_manifold and e.calc_face_angle(0.0) > math.radians(30)]
    if edges and width > 1e-5:
        verts = list({v for e in edges for v in e.verts})
        bmesh.ops.bevel(bm, geom=edges + verts, offset=width, offset_type="OFFSET", segments=segments, profile=0.5,
                        affect="EDGES", clamp_overlap=True)
    bm.normal_update()


def face_min_extent(f):
    n = f.normal
    t = f.calc_tangent_edge().normalized()
    b = n.cross(t)
    us = [v.co.dot(t) for v in f.verts]
    vs = [v.co.dot(b) for v in f.verts]
    return min(max(us) - min(us), max(vs) - min(vs))


def inset_panels(bm, thickness, depth, min_extent):
    faces = [f for f in bm.faces if face_min_extent(f) > min_extent]
    if faces:
        bmesh.ops.inset_individual(bm, faces=faces, thickness=thickness, depth=-depth, use_even_offset=True)
    bm.normal_update()
    return faces


def finish_bm(bm):
    big = [f for f in bm.faces if len(f.verts) > 4]
    if big:
        bmesh.ops.triangulate(bm, faces=big)
    bm.normal_update()
    return bm


def greybox_lod(shape, dims, cell, level, panel=None, bevel_segments=2, res=8, segments=16, emissive=False):
    """One LOD: level 0 = panels + bevels + recessed panels, 1 = bevels, 2 = hull, 3 = minimal hull."""
    bm = hull_bm(shape, dims, res, segments)
    thin = min(max(v.co[k] for v in bm.verts) - min(v.co[k] for v in bm.verts) for k in range(3))
    inner = []
    if level == 0 and panel:
        panelize(bm, panel)
    if level <= 1 and bevel_segments:
        bevel_sharp(bm, min(0.04 * cell, 0.12 * thin), bevel_segments)
    if level == 0:
        t = min(0.02 * cell, 0.05 * thin)
        inner = inset_panels(bm, t, 0.5 * t, 6 * t)
        front = [f for f in inner if f.is_valid and f.normal.x > 0.9]
        if front and emissive:
            max(front, key=lambda f: f.calc_area()).material_index = 1
    return finish_bm(bm)


def fit_budget(builders, budget):
    """First builder whose mesh fits ``budget`` tris (else the last one)."""
    bm = None
    for build in builders:
        if bm is not None:
            bm.free()
        bm = build()
        if bm_tris(bm) <= budget:
            return bm
    return bm


def lod_builders(shape, dims, cell, complexity, level, emissive=False):
    panel = PANEL_CELLS[complexity] * cell
    if level == 0:
        return ([lambda p=p, b=b: greybox_lod(shape, dims, cell, 0, p, b, emissive=emissive) for p in (panel, panel * 2, panel * 4, None) for b in (2, 1)]
                + [lambda: greybox_lod(shape, dims, cell, 1, None, 1)])
    if level == 1:
        return [lambda: greybox_lod(shape, dims, cell, 1, None, 1), lambda: greybox_lod(shape, dims, cell, 1, None, 1, 4, 12),
                lambda: greybox_lod(shape, dims, cell, 2, res=4, segments=12)]
    if level == 2:
        return [lambda r=r, sg=sg: greybox_lod(shape, dims, cell, 2, res=r, segments=sg) for r, sg in ((4, 12), (2, 8), (1, 6))]
    return ([lambda sg=sg: greybox_lod(shape, dims, cell, 3, res=1, segments=sg) for sg in (6, 5, 4)]
            + [lambda: greybox_lod("box", dims, cell, 3)])


def frame_bm(dims, strut):
    """The 12 edge struts of the grid volume (construction frame)."""
    bm = bmesh.new()
    for axis in range(3):
        o1, o2 = [k for k in range(3) if k != axis]
        for a in (-1, 1):
            for b in (-1, 1):
                size = [strut, strut, strut]
                size[axis] = dims[axis]
                c = [0.0, 0.0, 0.0]
                c[o1] = a * (dims[o1] / 2 - strut / 2)
                c[o2] = b * (dims[o2] / 2 - strut / 2)
                geom = bmesh.ops.create_cube(bm, size=1.0)
                bmesh.ops.transform(bm, matrix=Matrix.Translation(Vector(c)) @ Matrix.Diagonal(Vector((*size, 1.0))), verts=geom["verts"])
    return bm


def append_bm(dst, src):
    me = bpy.data.meshes.new("_tmp")
    src.to_mesh(me)
    src.free()
    dst.from_mesh(me)
    bpy.data.meshes.remove(me)


def stage_bm(shape, dims, cell, k, n, body_dims=None, body_offset=None):
    """Build stage k of n: frame only, then the body growing along the build axis."""
    bm = frame_bm(dims, min(0.06 * cell, 0.25 * min(dims)))
    for f in bm.faces:
        f.material_index = 2
    if k >= 2:
        bd = body_dims or dims
        axis = 2 if bd[2] >= 0.25 * max(bd) else max(range(3), key=lambda i: bd[i])
        hb = hull_bm(shape, bd, 4, 12)
        cut = -bd[axis] / 2 + bd[axis] * (k - 1) / n
        no = [0.0, 0.0, 0.0]
        no[axis] = 1.0
        co = [0.0, 0.0, 0.0]
        co[axis] = cut
        bmesh.ops.bisect_plane(hb, geom=hb.verts[:] + hb.edges[:] + hb.faces[:], plane_co=co, plane_no=no, clear_outer=True)
        boundary = [e for e in hb.edges if e.is_boundary]
        if boundary:
            bmesh.ops.holes_fill(hb, edges=boundary, sides=0)
        if body_offset is not None:
            bmesh.ops.translate(hb, vec=body_offset, verts=hb.verts[:])
        append_bm(bm, hb)
    return finish_bm(bm)


def part_instances(text):
    m = re.search(r"[×x]\s*(\d+)", text.split(":", 1)[0])
    return max(1, min(int(m.group(1)), 6)) if m else 1


def moving_part_kind(label):
    head = label.lower()
    if head.startswith("yaw"):
        return "yaw"
    if head.startswith("pitch") or head.startswith("elevation"):
        return "pitch"
    if "barrel" in head:
        return "barrel"
    if any(w in head for w in SPIN_WORDS):
        return "spin"
    if any(w in head for w in SLAB_WORDS):
        return "slab"
    return "top"


def moving_part_reserve(label, dims, cell):
    """Space (axis, metres) a moving part needs in front of / on top of the body."""
    kind = moving_part_kind(label)
    if kind == "spin":
        return 0, min(0.1 * dims[0], 0.2 * cell)
    if kind == "slab":
        return 0, min(0.08 * cell, 0.15 * dims[0])
    if kind in ("yaw", "pitch", "barrel"):
        return 2, turret_height(dims, cell)
    return 2, min(0.3 * dims[2], 0.5 * cell)


def turret_height(dims, cell):
    return min(0.35 * dims[2], 0.6 * cell)


def turret_bms(kind, dims, cell, top_z):
    """Turret head stand-ins stacked on the body: yaw turntable, pitch cradle, barrel along +X."""
    depth, width, height = dims
    t = max(0.02 * cell, min(turret_height(dims, cell), height / 2 - top_z))
    r = 0.35 * min(depth, width)
    bm = bmesh.new()
    if kind == "yaw":
        bmesh.ops.create_cone(bm, cap_ends=True, cap_tris=False, segments=16, radius1=r, radius2=r, depth=0.25 * t)
        return [(finish_bm(bm), Vector((0, 0, top_z + 0.125 * t)), Vector((2 * r, 2 * r, 0.25 * t)))]
    if kind == "pitch":
        size = Vector((0.9 * r, 1.2 * r, 0.6 * t))
        bmesh.ops.create_cube(bm, size=1.0)
        bmesh.ops.transform(bm, matrix=Matrix.Diagonal(Vector((*size, 1.0))), verts=bm.verts[:])
        return [(finish_bm(bm), Vector((0, 0, top_z + 0.55 * t)), size)]
    length = 0.45 * depth
    rad = max(0.01 * cell, 0.12 * t)
    bmesh.ops.create_cone(bm, cap_ends=True, cap_tris=False, segments=12, radius1=rad, radius2=rad, depth=length)
    bmesh.ops.rotate(bm, cent=Vector(), matrix=Matrix.Rotation(math.radians(90), 3, "Y"), verts=bm.verts[:])
    bmesh.ops.translate(bm, vec=Vector((length / 2, 0, 0)), verts=bm.verts[:])  # pivot at the pitch axis
    return [(finish_bm(bm), Vector((0, 0, top_z + 0.55 * t)), Vector((length, 2 * rad, 2 * rad)))]


def moving_part_bms(label, text, dims, cell, top_z=None, side=1, shift=0.0, slot=(0, 1)):
    """Greybox stand-ins for a moving part: [(bmesh, pivot, size)] inside the grid volume.
    Spinning parts and slabs (doors, hatches, flaps) sit on the front face; others on top of the body (``top_z``)."""
    low = f"{label} {text}".lower()
    head = label.lower()
    n = part_instances(text)
    depth, width, height = dims
    out = []
    kind = moving_part_kind(label)
    if kind in ("yaw", "pitch", "barrel"):
        return turret_bms(kind, dims, cell, top_z if top_z is not None else 0.0)
    if kind == "spin":
        r = 0.35 * min(width / n, height) / (1 + 2 * shift / max(cell, 1e-6))
        th = min(0.1 * depth, 0.2 * cell)
        for i in range(n):
            y = -width / 2 + width * (i + 0.5) / n
            bm = bmesh.new()
            bmesh.ops.create_cone(bm, cap_ends=True, cap_tris=False, segments=16, radius1=r, radius2=r, depth=th)
            bmesh.ops.rotate(bm, cent=Vector(), matrix=Matrix.Rotation(math.radians(90), 3, "Y"), verts=bm.verts[:])
            out.append((finish_bm(bm), Vector((side * (depth / 2 - th / 2 - 0.01 * cell + shift), y, 0)), Vector((th, 2 * r, 2 * r))))
    elif kind == "slab":
        th = min(0.08 * cell, 0.15 * depth)
        w, h = 0.9 * width / n, 0.9 * height
        for i in range(n):
            y = -0.45 * width + w * (i + 0.5)
            center = Vector((side * (depth / 2 - th / 2 - 0.005 * cell + shift), y, 0))
            if "hinge" in low or "swing" in low:
                pivot = center + (Vector((0, 0, -h / 2)) if "back edge" in low or "ramp" in head else Vector((0, w / 2, 0)))
            else:
                pivot = center
            bm = bmesh.new()
            bmesh.ops.create_cube(bm, size=1.0)
            bmesh.ops.transform(bm, matrix=Matrix.Translation(center - pivot) @ Matrix.Diagonal(Vector((th, w, h, 1.0))), verts=bm.verts[:])
            out.append((finish_bm(bm), pivot, Vector((th, w, h))))
    else:
        k, count = slot  # each top-mounted part gets its own slot across the width, so parts never overlap
        lane = width / count
        size = Vector((min(0.25 * depth, 0.4 * cell), min(0.2 * lane / n, 0.3 * cell), min(0.3 * height, 0.5 * cell)))
        z = height / 2 - size.z / 2 if top_z is None else min(top_z + size.z / 2, height / 2 - size.z / 2)
        for i in range(n):
            y = -width / 2 + lane * k + lane * (i + 0.5) / n
            bm = bmesh.new()
            bmesh.ops.create_cube(bm, size=1.0)
            bmesh.ops.transform(bm, matrix=Matrix.Diagonal(Vector((*size, 1.0))), verts=bm.verts[:])
            out.append((finish_bm(bm), Vector((0, y, z)), size))
    return out


def bm_object(name, bm, uv_dims, col, mats, parent=None, location=(0, 0, 0)):
    _box_uvs(bm, uv_dims)
    me = bpy.data.meshes.new(name)
    bm.to_mesh(me)
    bm.free()
    for m in mats:
        me.materials.append(m)
    obj = bpy.data.objects.new(name, me)
    col.objects.link(obj)
    obj.location = location
    if parent is not None:
        obj.parent = parent
    return obj


def build_greybox(asset_name, part, asset, dims, cell, root, lods, stage_cols, parts_col):
    grey, emissive, frame = greybox_materials(part["art_set"], part["category"])
    mats = [grey, emissive, frame]
    budgets = asset["lod_tris"]
    old = bpy.data.objects.get(f"{asset_name}_LOD0")
    if old is not None:
        old_me = old.data
        bpy.data.objects.remove(old)
        bpy.data.meshes.remove(old_me)
    # Moving parts need room on the front face / on top: shrink the body there if the shape fills the volume.
    probe = hull_bm(asset["shape"], dims)
    hull_hi = [max(v.co[k] for v in probe.verts) for k in range(3)]
    probe.free()
    # Front parts (doors, discs) alternate front face / back face, so an airlock's inner door sits at the back;
    # a third or later part on the same face is nudged outward to avoid overlapping faces.
    reserve = {"front": 0.0, "back": 0.0, "top": 0.0}
    placement, k = [], 0
    tops = [t for t in part["moving_parts"] if moving_part_kind(t.split(":", 1)[0]) == "top"]
    for text in part["moving_parts"]:
        axis, need = moving_part_reserve(text.split(":", 1)[0], dims, cell)
        if axis == 2:
            placement.append((1, 0.0, (tops.index(text), len(tops)) if text in tops else (0, 1)))
            if dims[2] / 2 - hull_hi[2] < need - 1e-6:
                reserve["top"] = max(reserve["top"], min(need, 0.4 * dims[2]))
            continue
        side = 1 if k % 2 == 0 else -1
        placement.append((side, (k // 2) * 0.004 * cell, (0, 1)))
        k += 1
        if dims[0] / 2 - hull_hi[0] < need - 1e-6:
            key = "front" if side == 1 else "back"
            reserve[key] = max(reserve[key], min(need, 0.3 * dims[0]))
    body = Vector((dims[0] - reserve["front"] - reserve["back"], dims[1], dims[2] - reserve["top"]))
    offset = Vector(((reserve["back"] - reserve["front"]) / 2, 0, -reserve["top"] / 2))

    for level in range(4):
        bm = fit_budget(lod_builders(asset["shape"], body, cell, part["complexity"], level, bool(part["emissive"])), budgets[level])
        bmesh.ops.translate(bm, vec=offset, verts=bm.verts[:])
        bm_object(f"{asset_name}_LOD{level}", bm, dims, lods[level], mats[:2] if level == 0 else mats[:1], root)
    for k in range(1, part["build_stages"] + 1):
        bm_object(f"{asset_name}_BS{k}", stage_bm(asset["shape"], dims, cell, k, part["build_stages"], body, offset), dims,
                  stage_cols[k - 1], mats, root)
    top_z = min(hull_hi[2] * body.z / dims[2] + offset.z, dims[2] / 2) if dims[2] else 0
    for i, text in enumerate(part["moving_parts"]):
        label = text.split(":", 1)[0]
        key = pascal(label)[:40] or f"Part{i + 1}"
        pivot_empty = bpy.data.objects.get(f"PART_{key}")
        side, shift, slot = placement[i]
        pieces = moving_part_bms(label, text, dims, cell, top_z, side, shift, slot)
        for j, (bm, pivot, size) in enumerate(pieces):
            nm = f"{asset_name}_Part_{key}" + (f"_{j + 1:02d}" if len(pieces) > 1 else "")
            o = bm_object(nm, bm, size, parts_col, [grey], root, pivot)
            o["pivot_of"] = f"PART_{key}"
            if j == 0 and pivot_empty is not None:
                pivot_empty.location = pivot
    root["greybox"] = GREYBOX_VERSION


# --------------------------------------------------------------------------- props
# Components, resources, handheld equipment (1P rigged + 3P), suits (character skeleton),
# suit modules and drones from components.json / equipment.json. Built as greybox props at
# catalog size, with LODs, pivots, sockets and bones per the Parts Bible prop rules (ch. 17-18).
PROP_VERSION = "1.0"
GUN_KINDS = {"Firearm", "Energy", "Heavy", "Improvised", "Sower"}
PROP_COLORS = {"component": (0.62, 0.64, 0.68), "ore": (0.45, 0.38, 0.32), "ingot": (0.72, 0.72, 0.75), "fuel": (0.85, 0.75, 0.2),
               "resource": (0.35, 0.7, 0.45), "Firearm": (0.22, 0.23, 0.25), "Energy": (0.3, 0.45, 0.62), "Heavy": (0.4, 0.42, 0.3),
               "Improvised": (0.55, 0.4, 0.25), "Sower": (0.2, 0.72, 0.68), "Melee": (0.5, 0.5, 0.53), "Tool": (0.88, 0.6, 0.15),
               "Throwable": (0.35, 0.45, 0.3), "Consumable": (0.85, 0.85, 0.85), "Suit": (0.9, 0.55, 0.2),
               "Suit Module": (0.6, 0.62, 0.68), "Drone": (0.8, 0.75, 0.25)}
# Bone / part stand-in positions as fractions of the half-extents (x forward, y left, z up), before fitting.
BONE_POS = {"trigger": (-0.05, 0, -0.15), "mag": (0.08, 0, -0.45), "slide": (0.1, 0, 0.35), "hammer": (-0.35, 0, 0.3),
            "bolt": (0.0, -0.5, 0.25), "stock": (-0.75, 0, 0.05), "charging_handle": (-0.25, 0, 0.45), "selector": (-0.15, -0.6, 0.05),
            "pump": (0.35, 0, -0.05), "shell_gate": (0.0, -0.6, -0.05), "bolt_handle": (-0.05, -0.7, 0.25), "scope_turret": (0.0, 0, 0.75),
            "igniter": (0.8, 0, 0.1), "hose": (-0.45, 0, -0.55), "cylinder": (0.1, 0, 0.05), "sight_flip": (0.15, 0, 0.7),
            "coils": (0.45, 0, 0.2), "rings": (0.5, 0, 0.2), "lens": (0.85, 0, 0.2), "petals": (0.8, 0, 0.2), "pod": (0.1, 0, 0.55),
            "break_action": (0.1, 0, 0.1), "breech": (0.0, 0, 0.2), "piston": (0.35, 0, 0.1), "mode_dial": (-0.1, 0.5, 0.45),
            "emitter_head": (0.8, 0, 0.2), "canister": (-0.55, 0, 0.3), "bit": (0.85, 0, 0.1), "blades": (0.85, 0, 0.1),
            "focus": (0.0, 0, 0.6), "pin": (0.0, 0.45, 0.8), "spoon": (0.0, 0.7, 0.3), "plunger": (-0.85, 0, 0.0),
            "arm": (0.2, 0, -0.7), "drill": (0.6, 0, -0.6), "gun_yaw": (0.3, 0, -0.55), "gun_pitch": (0.5, 0, -0.55), "camera": (0.8, 0, -0.2)}
SOCKET_POS = {"support_l": (0.4, 0, -0.35), "grip_l": (0.3, 0.5, 0), "muzzle": (1.0, 0, 0.2), "emitter": (1.0, 0, 0.2), "nozzle": (1.0, 0, 0.2),
              "bit_tip": (1.0, 0, 0.1), "blade_tip": (1.0, 0, 0.1), "impact_point": (0.9, 0, 0), "needle": (1.0, 0, 0), "eject": (-0.05, -1.0, 0.3),
              "sight": (-0.2, 0, 1.0), "scope": (0.0, 0, 1.0), "view": (1.0, 0, 0.3), "screen": (-0.4, 0, 1.0), "rail_light": (0.55, -1.0, 0.1),
              "pilot_light": (0.9, 0, -0.1), "backblast": (-1.0, 0, 0.2), "sample_port": (0.2, -1.0, 0), "audio": (0, 0, 1.0), "wick": (0, 0, 1.0),
              "valve": (0, 0, 1.0), "back_attach": (-1.0, 0, 0), "chest_attach": (-1.0, 0, 0), "shoulder_attach": (0, 0, -1.0),
              "helmet_attach": (0, 0, -1.0), "boot_attach": (0, 0, -1.0), "nozzles": (-0.2, 0, -1.0), "weld_tip": (0.9, 0, -1.0),
              "drill_tip": (1.0, 0, -0.8), "cargo": (0, 0, -1.0), "light": (1.0, 0, 0.1), "camera": (1.0, 0, -0.2)}
SUIT_SOCKET_BONES = {"helmet": "head", "helmet_light": "head", "backpack": "spine_05", "jetpack": "spine_05", "tool_belt": "pelvis",
                     "filter_l": "spine_05", "filter_r": "spine_05", "wrist_pad": "lowerarm_l", "shoulder_lamp": "clavicle_r",
                     "module_slots": ["spine_03", "spine_05", "thigh_l", "thigh_r", "upperarm_l", "upperarm_r"]}
EMISSIVE_PIECES = {"lens", "emitter_head", "coils", "rings", "petals", "camera", "screen", "light", "core", "glow"}


def slug(text):
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")


def props_catalog(data_dir=None):
    base = Path(data_dir) if data_dir else repo_root() / "docs" / "parts-bible" / "data"
    comp = json.loads((base / "components.json").read_text(encoding="utf-8"))
    eqp = json.loads((base / "equipment.json").read_text(encoding="utf-8"))
    out = []

    def add(asset, item, family, folder, budgets, pivot, sub, bones=(), art="PRP"):
        out.append({"asset": asset, "item": item, "id": item["id"], "family": family, "sub": sub, "pivot": pivot, "art": art,
                    "lod_tris": [int(b) for b in budgets], "bones": list(bones), "blend_path": f"assets/props/{folder}/{asset}.blend",
                    "dims": [item["dims_m"][0], item["dims_m"][2], item["dims_m"][1]]})  # catalog L×H×W -> X, Y, Z

    for c in comp["components"]:
        add(f"SM_CMP_{pascal(c['name'])}", c, "component", "components", [c["tris"], max(12, c["tris"] // 2)], "base", "component")
    for r in comp["resources"]:
        add(f"SM_RES_{pascal(r['name'])}", r, "resource", "resources", [r["tris"], max(12, r["tris"] // 2)], "base", r["kind"])
    for e in eqp["equipment"]:
        folder, n, art = f"equipment/{slug(e['kind'])}", pascal(e["name"]), e.get("art") or "PRP"
        three = [e["tris_3p"], e["tris_3p"] // 2, e["tris_3p"] // 5] if e["tris_3p"] else [e["tris_1p"]]
        if e["kind"] == "Suit":
            add(f"SK_SUIT_{n}", e, "suit", folder, three, "feet", "Suit", art=art)
        elif e["kind"] == "Drone":
            add(f"SK_EQP_{n}" if e["bones"] else f"SM_EQP_{n}", e, "drone", folder, three, "center", "Drone", e["bones"], art)
        elif e["kind"] == "Suit Module":
            add(f"SK_EQP_{n}" if e["bones"] else f"SM_EQP_{n}", e, "module", folder, three, "base", "Suit Module", e["bones"], art)
        else:
            add(f"SK_EQP_{n}_1P", e, "1p", folder, [e["tris_1p"]], "grip", e["kind"], e["bones"] or ["root"], art)
            add(f"SM_EQP_{n}_3P", e, "3p", folder, three, "grip", e["kind"], (), art)
    return out


# ---- primitives (each returns a BMesh; sizes in metres, X forward, Y left, Z up)
def prim_box(size, center=(0, 0, 0), bevel=0.0):
    bm = bmesh.new()
    bmesh.ops.create_cube(bm, size=1.0)
    bmesh.ops.transform(bm, matrix=Matrix.Translation(Vector(center)) @ Matrix.Diagonal(Vector((*size, 1.0))), verts=bm.verts[:])
    if bevel > 0:
        w = min(bevel, 0.2 * min(size))
        bmesh.ops.bevel(bm, geom=bm.edges[:] + bm.verts[:], offset=w, offset_type="OFFSET", segments=1, profile=0.5,
                        affect="EDGES", clamp_overlap=True)
    return bm


def prim_cyl(radius, length, center=(0, 0, 0), axis="Z", segments=12, radius2=None):
    bm = bmesh.new()
    bmesh.ops.create_cone(bm, cap_ends=True, cap_tris=False, segments=max(3, segments), radius1=radius,
                          radius2=radius if radius2 is None else radius2, depth=length)
    rot = {"X": Matrix.Rotation(math.radians(90), 4, "Y"), "Y": Matrix.Rotation(math.radians(90), 4, "X"), "Z": Matrix.Identity(4)}[axis]
    bmesh.ops.transform(bm, matrix=Matrix.Translation(Vector(center)) @ rot, verts=bm.verts[:])
    return bm


def prim_rock(size, center=(0, 0, 0), subdiv=2, seed=0, rough=0.22):
    import random
    bm = bmesh.new()
    bmesh.ops.create_icosphere(bm, subdivisions=subdiv, radius=0.5)
    rnd = random.Random(seed)
    for v in bm.verts:
        v.co *= 1 + rough * (rnd.random() - 0.5)
    bmesh.ops.transform(bm, matrix=Matrix.Translation(Vector(center)) @ Matrix.Diagonal(Vector((*size, 1.0))), verts=bm.verts[:])
    return bm


def prim_hull(points):
    bm = bmesh.new()
    verts = [bm.verts.new(p) for p in {tuple(round(c, 6) for c in p): p for p in points}.values()]
    res = bmesh.ops.convex_hull(bm, input=verts, use_existing_faces=False)
    junk = list({v for v in res["geom_interior"] + res["geom_unused"] if isinstance(v, bmesh.types.BMVert)})
    if junk:
        bmesh.ops.delete(bm, geom=junk, context="VERTS")
    bmesh.ops.dissolve_limit(bm, angle_limit=math.radians(0.5), verts=bm.verts[:], edges=bm.edges[:])
    return bm


# ---- recipes: return [(piece_name, bmesh)] at approximately catalog proportions
def recipe_gun(L, W, H, e, q):
    seg, bev = (16, 0.004) if q == 0 else ((10, 0.0) if q == 1 else (6, 0.0))
    bones = set(e["bones"])
    out = [("receiver", prim_box((0.42 * L, W, 0.4 * H), (-0.05 * L, 0, 0.12 * H), bev)),
           ("barrel", prim_cyl(min(0.12 * H, 0.45 * W), 0.42 * L, (0.29 * L, 0, 0.16 * H), "X", seg)),
           ("grip", prim_box((0.12 * L, 0.8 * W, 0.48 * H), (-0.14 * L, 0, -0.26 * H), bev))]
    if L > 0.35:
        out.append(("stock", prim_box((0.24 * L, 0.7 * W, 0.34 * H), (-0.38 * L, 0, 0.04 * H), bev)))
        out.append(("handguard", prim_box((0.22 * L, 0.9 * W, 0.2 * H), (0.22 * L, 0, 0.06 * H), bev)))
    if "cylinder" in bones:
        out.append(("cylinder", prim_cyl(0.22 * H, 0.16 * L, (0.04 * L, 0, 0.06 * H), "X", seg)))
    if any("scope" in s for s in e["sockets"]) or "sight_flip" in bones:
        out.append(("scope", prim_cyl(0.08 * H, 0.22 * L, (0.0, 0, 0.42 * H), "X", seg)))
    if "coils" in bones or "rings" in bones:
        name = "coils" if "coils" in bones else "rings"
        for i in range(3):
            out.append((name, prim_cyl(min(0.2 * H, 0.49 * W), 0.03 * L, ((0.18 + 0.09 * i) * L, 0, 0.16 * H), "X", seg)))
    if "petals" in bones:
        for a in (-1, 1):
            out.append(("petals", prim_box((0.12 * L, 0.2 * W, 0.12 * H), (0.44 * L, a * 0.3 * W, 0.2 * H))))
    if e["kind"] == "Heavy" and "hose" in bones:
        out.append(("tank", prim_cyl(0.2 * H, 0.3 * L, (-0.1 * L, 0, -0.18 * H), "X", seg)))
    return out


def recipe_melee(L, W, H, e, q):
    seg = 12 if q == 0 else (8 if q == 1 else 6)
    return [("grip", prim_cyl(0.3 * min(W, H), 0.62 * L, (-0.19 * L, 0, 0), "X", seg)),
            ("head", prim_box((0.36 * L, W, H), (0.32 * L, 0, 0), 0.003 if q == 0 else 0))]


def recipe_tool(L, W, H, e, q):
    seg = 12 if q == 0 else (8 if q == 1 else 6)
    if e["id"] == "binoculars":
        return [("barrel_l", prim_cyl(0.3 * min(W, H), 0.8 * L, (0, 0.25 * W, 0), "X", seg)),
                ("barrel_r", prim_cyl(0.3 * min(W, H), 0.8 * L, (0, -0.25 * W, 0), "X", seg)),
                ("grip", prim_box((0.3 * L, 0.2 * W, 0.4 * H), (-0.1 * L, 0, 0)))]
    return [("body", prim_box((0.5 * L, W, 0.5 * H), (-0.12 * L, 0, 0.18 * H), 0.004 if q == 0 else 0)),
            ("head", prim_cyl(0.18 * H, 0.35 * L, (0.3 * L, 0, 0.18 * H), "X", seg, 0.1 * H)),
            ("grip", prim_box((0.12 * L, 0.7 * W, 0.45 * H), (-0.18 * L, 0, -0.22 * H)))]


def recipe_small(L, W, H, e, q):
    """Throwables and consumables."""
    seg = 12 if q == 0 else (8 if q == 1 else 6)
    name = e["name"].lower()
    if "grenade" in name or "bomb" in name or "noise" in name:
        body = prim_rock((L, W, 0.85 * H), (0, 0, -0.07 * H), 2 if q == 0 else 1, 7, 0.0) if "frag" in name else prim_cyl(0.5 * min(L, W), 0.85 * H, (0, 0, -0.07 * H), "Z", seg)
        return [("body", body), ("spoon", prim_box((0.2 * L, 0.3 * W, 0.3 * H), (0, 0.35 * W, 0.2 * H))),
                ("pin", prim_cyl(0.12 * min(L, W), 0.15 * H, (0, 0, 0.42 * H), "Z", 6))]
    if "molotov" in name or "bottle" in name:
        return [("body", prim_cyl(0.5 * min(L, W), 0.7 * H, (0, 0, -0.15 * H), "Z", seg)),
                ("neck", prim_cyl(0.18 * min(L, W), 0.3 * H, (0, 0, 0.35 * H), "Z", seg))]
    if "injector" in name or "serum" in name or "cocktail" in name:
        return [("body", prim_cyl(0.45 * min(W, H), 0.6 * L, (0, 0, 0), "X", seg)),
                ("plunger", prim_cyl(0.3 * min(W, H), 0.25 * L, (-0.38 * L, 0, 0), "X", seg)),
                ("needle", prim_cyl(0.06 * min(W, H), 0.15 * L, (0.42 * L, 0, 0), "X", 6))]
    if "can" in name:
        return [("body", prim_cyl(0.5 * min(L, W), H, (0, 0, 0), "Z", seg))]
    if "bandage" in name:
        return [("body", prim_cyl(0.5 * min(L, H), W, (0, 0, 0), "Y", seg))]
    return [("body", prim_box((L, W, 0.8 * H), (0, 0, -0.1 * H), 0.004 if q == 0 else 0)),
            ("handle", prim_box((0.4 * L, 0.1 * W, 0.2 * H), (0, 0, 0.4 * H)))]


def recipe_module(L, W, H, e, q):
    seg = 12 if q == 0 else (8 if q == 1 else 6)
    name = e["name"].lower()
    if "jetpack" in name:
        return [("frame", prim_box((0.4 * L, W, H), (-0.3 * L, 0, 0), 0.01 if q == 0 else 0))] + [
            ("tank", prim_cyl(0.28 * min(L, W), 0.8 * H, (0.2 * L, s * 0.25 * W, 0.05 * H), "Z", seg)) for s in (-1, 1)]
    if "tank" in name:
        return [("tank", prim_cyl(0.48 * min(L, W), H, (0, 0, 0), "Z", seg))]
    if "armor" in name:
        return [("plate", prim_hull([Vector((x, y, z)) for x in (-0.5 * L, 0.5 * L) for y in (-0.5 * W, 0.5 * W) for z in (-0.5 * H, 0.5 * H)
                                     if not (x > 0 and z > 0)]))]
    if "filter" in name:
        return [("body", prim_cyl(0.48 * min(W, H), L, (0, 0, 0), "X", seg))]
    if "scanner" in name:
        return [("body", prim_box((L, W, 0.6 * H), (0, 0, -0.2 * H))), ("dish", prim_cyl(0.45 * min(L, W), 0.4 * H, (0, 0, 0.3 * H), "Z", seg, 0.1 * min(L, W)))]
    if "damper" in name:
        return [("body", prim_box((L, 0.45 * W, H), (0, s * 0.27 * W, 0))) for s in (-1, 1)]
    return [("body", prim_box((L, W, H), (0, 0, 0), 0.01 if q == 0 else 0))]


def recipe_drone(L, W, H, e, q):
    seg = 16 if q == 0 else (10 if q == 1 else 6)
    out = [("body", prim_cyl(0.3 * min(L, W), 0.45 * H, (0, 0, 0.05 * H), "Z", seg))]
    for i, (sx, sy) in enumerate(((1, 1), (-1, 1), (-1, -1), (1, -1))):
        out.append(("strut", prim_box((0.34 * L, 0.05 * W, 0.08 * H), (sx * 0.2 * L, sy * 0.2 * W, 0.1 * H))))
        out.append((f"rotor_{i + 1:02d}", prim_cyl(0.16 * min(L, W), 0.05 * H, (sx * 0.34 * L, sy * 0.34 * W, 0.3 * H), "Z", seg)))
    bones = set(e["bones"])
    if "drill" in bones:
        out.append(("drill", prim_cyl(0.08 * L, 0.45 * H, (0.25 * L, 0, -0.25 * H), "X", seg, 0.0)))
    elif "arm" in bones:
        out.append(("arm", prim_box((0.3 * L, 0.06 * W, 0.08 * H), (0.2 * L, 0, -0.3 * H))))
    elif "gun_yaw" in bones:
        out.append(("gun_yaw", prim_box((0.15 * L, 0.15 * W, 0.2 * H), (0.1 * L, 0, -0.3 * H))))
        out.append(("gun_pitch", prim_cyl(0.04 * L, 0.3 * L, (0.3 * L, 0, -0.35 * H), "X", seg)))
    elif "camera" in bones:
        out.append(("camera", prim_cyl(0.08 * L, 0.12 * L, (0.3 * L, 0, -0.1 * H), "X", seg)))
    return out


def recipe_component(L, W, H, item, q):
    seg = 12 if q == 0 else (8 if q == 1 else 6)
    bev = 0.004 if q == 0 else 0.0
    n = item["name"].lower()
    if "tube" in n or "filament" in n or "superconductor" in n:
        return [("body", prim_cyl(0.5 * min(W, H), L, (0, 0, 0), "X", seg))]
    if "girder" in n:
        return [("flange", prim_box((L, W, 0.15 * H), (0, 0, s * 0.425 * H))) for s in (-1, 1)] + [("web", prim_box((L, 0.15 * W, 0.7 * H)))]
    if "power cell" in n:
        return [("body", prim_cyl(0.5 * min(L, W), 0.9 * H, (0, 0, -0.05 * H), "Z", seg)), ("core", prim_cyl(0.25 * min(L, W), 0.1 * H, (0, 0, 0.45 * H), "Z", seg))]
    if "motor" in n or "thruster" in n:
        return [("body", prim_cyl(0.45 * min(W, H), 0.8 * L, (0.1 * L, 0, 0.05 * H), "X", seg)), ("base", prim_box((0.8 * L, 0.8 * W, 0.15 * H), (0, 0, -0.42 * H)))]
    if "reactor" in n:
        return [("body", prim_box((L, W, 0.8 * H), (0, 0, -0.1 * H), bev)), ("core", prim_cyl(0.3 * min(L, W), 0.2 * H, (0, 0, 0.4 * H), "Z", seg))]
    if "duct tape" in n or "wiring" in n:
        return [("body", prim_cyl(0.5 * min(L, W), H, (0, 0, 0), "Z", seg))]
    if "wood" in n:
        return [("plank", prim_box((L, 0.3 * W, 0.3 * H), (0, (i - 1) * 0.34 * W, (-0.35 + 0.35 * (i % 2)) * H), bev)) for i in range(3)]
    if "scrap" in n:
        return [("sheet", prim_hull([Vector((x, y, z)) for x in (-0.5 * L, 0.5 * L) for y in (-0.5 * W, 0.5 * W)
                                      for z in ((-0.5 * H, -0.3 * H) if x < 0 else (0.3 * H, 0.5 * H))]))]
    if "fabric" in n or "bio-plastic" in n or "living alloy" in n or "explosives" in n:
        return [("body", prim_box((L, W, H), (0, 0, 0), 0.3 * min(L, W, H) if q == 0 else 0))]
    if H <= 0.06:  # plates, panels, tiles, grids, wafers
        return [("body", prim_box((L, W, H), (0, 0, 0), bev))]
    return [("body", prim_box((L, W, 0.85 * H), (0, 0, -0.075 * H), bev)), ("top", prim_box((0.6 * L, 0.6 * W, 0.15 * H), (0, 0, 0.425 * H)))]


def recipe_resource(L, W, H, item, q):
    seg = 12 if q == 0 else (8 if q == 1 else 6)
    k, n = item["kind"], item["name"].lower()
    seed = sum(map(ord, item["id"]))
    if k == "ore":
        return [("body", prim_rock((L, W, H), (0, 0, 0), 2 if q == 0 else 1, seed, 0.35 if "ice" not in n else 0.15))]
    if k == "ingot":
        if "wafer" in n:
            return [("body", prim_cyl(0.5 * min(L, W), H, (0, 0, 0), "Z", seg * 2))]
        if "powder" in n:
            return [("body", prim_box((L, W, H), (0, 0, 0), 0.3 * min(L, W, H) if q == 0 else 0))]
        return [("body", prim_hull([Vector((x * (0.5 if z < 0 else 0.4) * L, y * (0.5 if z < 0 else 0.35) * W, z * 0.5 * H))
                                    for x in (-1, 1) for y in (-1, 1) for z in (-1, 1)]))]
    if k == "fuel":
        return [("body", prim_cyl(0.48 * min(L, W), 0.88 * H, (0, 0, -0.06 * H), "Z", seg)), ("cap", prim_cyl(0.2 * min(L, W), 0.12 * H, (0, 0, 0.44 * H), "Z", seg))]
    if "crystal" in n:
        return [("body", prim_hull([Vector((0, 0, 0.5 * H)), Vector((0, 0, -0.5 * H))]
                                   + [Vector((0.5 * L * math.cos(a), 0.5 * W * math.sin(a), 0)) for a in (i * math.pi / 3 for i in range(6))]))]
    if "sample" in n:
        return [("body", prim_cyl(0.45 * min(L, W), 0.85 * H, (0, 0, -0.075 * H), "Z", seg)), ("cap", prim_cyl(0.5 * min(L, W), 0.15 * H, (0, 0, 0.425 * H), "Z", seg))]
    return [("body", prim_rock((L, W, H), (0, 0, 0), 2 if q == 0 else 1, seed, 0.3))]


def prop_pieces(p, q):
    L, W, H = p["dims"]
    e = p["item"]
    fam, sub = p["family"], p["sub"]
    if fam == "component":
        return recipe_component(L, W, H, e, q)
    if fam == "resource":
        return recipe_resource(L, W, H, e, q)
    if fam == "drone":
        return recipe_drone(L, W, H, e, q)
    if fam == "module":
        return recipe_module(L, W, H, e, q)
    if sub in GUN_KINDS:
        return recipe_gun(L, W, H, e, q)
    if sub == "Melee":
        return recipe_melee(L, W, H, e, q)
    if sub == "Tool":
        return recipe_tool(L, W, H, e, q)
    return recipe_small(L, W, H, e, q)


def bone_list(p):
    out = []
    for b in p["bones"]:
        m = re.match(r"([a-z_]+)\s*×\s*(\d+)", b)
        out += [f"{m.group(1)}_{i + 1:02d}" for i in range(int(m.group(2)))] if m else [b]
    return out if "root" in out or not out else ["root"] + out


def socket_list(item):
    out = []
    for s in item.get("sockets", []):
        m = re.match(r"([A-Za-z_]+)", s)
        if not m:
            continue
        token = m.group(1).rstrip("_")
        c = re.search(r"×\s*(\d+)", s)
        n = int(c.group(1)) if c else 1
        out += [(token, f"SOCKET_{pascal(token)}" + (f"_{i + 1:02d}" if n > 1 else ""), i, n) for i in range(n)]
    return out


def build_prop_geometry(p, q, groups, emissive):
    """Pieces for quality ``q`` fitted to the catalog size and pivot. Returns (bmesh, transform, grip, piece_centers)."""
    L, W, H = p["dims"]
    pieces = prop_pieces(p, q) if q < 3 else [("body", prim_box((L, W, H)))]  # q 3: last-resort box
    extra = {}
    for b in groups:
        base = re.sub(r"_\d\d$", "", b)
        if b != "root" and not any(nm == b or nm == base for nm, _ in pieces) and base in BONE_POS:
            fx, fy, fz = BONE_POS[base]
            size = (0.12 * L, 0.45 * W, 0.15 * H)
            extra[b] = prim_box(size, (fx * 0.5 * L, fy * 0.5 * W, fz * 0.5 * H))
    pieces += list(extra.items())
    pts = [v.co for _, bm in pieces for v in bm.verts]
    lo = Vector([min(v[k] for v in pts) for k in range(3)])
    hi = Vector([max(v[k] for v in pts) for k in range(3)])
    size = hi - lo
    scale = Matrix.Diagonal(Vector((L / max(size.x, 1e-6), W / max(size.y, 1e-6), H / max(size.z, 1e-6), 1.0)))
    fit = scale @ Matrix.Translation(-(lo + hi) / 2)
    centers = {}
    for nm, bm in pieces:
        c = sum((v.co for v in bm.verts), Vector()) / max(1, len(bm.verts))
        centers.setdefault(nm, fit @ c)
    if p["pivot"] == "base":
        pivot = Vector((0, 0, -H / 2))
    elif p["pivot"] == "grip":
        pivot = centers.get("grip", Vector((-0.2 * L, 0, -0.2 * H))) if p["sub"] not in ("Throwable", "Consumable") else Vector()
    else:
        pivot = Vector()
    M = Matrix.Translation(-pivot) @ fit
    out = bmesh.new()
    dl = out.verts.layers.deform.verify()
    for nm, bm in pieces:
        base = re.sub(r"_\d\d$", "", nm)
        bone = nm if nm in groups else (base if base in groups else "root")
        gi = groups.index(bone) if bone in groups else 0
        vmap = {}
        for v in bm.verts:
            nv = out.verts.new(M @ v.co)
            nv[dl][gi] = 1.0
            vmap[v] = nv
        mat = 1 if emissive and base in EMISSIVE_PIECES else 0
        for f in bm.faces:
            nf = out.faces.new([vmap[v] for v in f.verts])
            nf.material_index = mat
        bm.free()
    finish_bm(out)
    return out, M, {k: Matrix.Translation(-pivot) @ v for k, v in centers.items()}, (lo, hi)


def build_prop(p, out_root, force=False):
    target = Path(out_root) / p["blend_path"]
    if target.exists() and not force:
        print(f"SKIP  {p['asset']}: {target} exists (use --force to overwrite)")
        return None
    bpy.ops.wm.read_factory_settings(use_empty=True)
    scene = bpy.context.scene
    scene.name = p["asset"]
    set_units(scene)
    name, e = p["asset"], p["item"]
    root_col = new_collection(name, scene.collection)
    lods_col = new_collection(f"{name}_LODs", root_col)
    sock_col = new_collection(f"{name}_Sockets", root_col)
    root = new_empty(name, root_col, "CUBE", 0.5 * min(p["dims"]))
    color = PROP_COLORS.get(p["sub"], PROP_COLORS.get(p["family"], (0.6, 0.6, 0.6)))
    mats = [pbr_material(f"MI_{p['art']}_Greybox_{pascal(p['sub'])}", color),
            pbr_material(f"MI_{p['art']}_Emissive_Prop", (0.05, 0.05, 0.05), emission=EMISSIVE_RGB, metallic=0.0, roughness=0.3)]
    emissive = bool(e.get("emissive"))
    meta = {"exodus_tool_version": TOOL_VERSION, "kind": "prop", "prop_version": PROP_VERSION, "asset": name, "item_id": p["id"],
            "item_name": e["name"], "family": p["family"], "type": p["sub"], "dims_m": [round(v, 4) for v in p["dims"]],
            "lod_tris": list(p["lod_tris"]), "pivot": p["pivot"], "sockets": json.dumps([s[1] for s in socket_list(e)]),
            "bones": json.dumps([] if p["family"] == "suit" else bone_list(p) if name.startswith("SK_") else [])}
    for k, v in meta.items():
        root[k] = v

    if p["family"] == "suit":
        build_suit(p, root, root_col, lods_col, sock_col, mats)
    else:
        skeletal = name.startswith("SK_")
        groups = bone_list(p) if skeletal else ["root"]
        arm = None
        if skeletal:
            arm_data = bpy.data.armatures.new(f"{name}_Skeleton")
            arm = bpy.data.objects.new("Armature", arm_data)
            root_col.objects.link(arm)
            arm.parent = root
        placed = None
        for level, budget in enumerate(p["lod_tris"]):
            bm = None
            for q in range(level, 4):
                if bm is not None:
                    bm.free()
                bm, M, centers, box = build_prop_geometry(p, q, groups, emissive)
                if bm_tris(bm) <= budget:
                    break
            if level == 0:
                placed = (M, centers, box)
            _box_uvs(bm, p["dims"])
            me = bpy.data.meshes.new(f"{name}_LOD{level}")
            bm.to_mesh(me)
            bm.free()
            for m in mats:
                me.materials.append(m)
            obj = bpy.data.objects.new(f"{name}_LOD{level}", me)
            lods_col.objects.link(obj)
            if skeletal:
                for g in groups:
                    obj.vertex_groups.new(name=g)
                obj.parent = arm
                obj.modifiers.new("Armature", "ARMATURE").object = arm
            else:
                obj.parent = root
        M, centers, (lo, hi) = placed
        if skeletal:
            bpy.context.view_layer.objects.active = arm
            arm.select_set(True)
            bpy.ops.object.mode_set(mode="EDIT")
            ebs = {}
            blen = max(0.02, 0.08 * max(p["dims"]))
            for g in groups:
                base = re.sub(r"_\d\d$", "", g)
                head = Vector() if g == "root" else centers.get(g, centers.get(base, Vector()))
                eb = arm_data.edit_bones.new(g)
                eb.head, eb.tail = head, head + Vector((blen, 0, 0))
                ebs[g] = eb
            for g in groups:
                if g != "root":
                    ebs[g].parent = ebs["root"]
            bpy.ops.object.mode_set(mode="OBJECT")
        half = (hi - lo) / 2
        mid = (lo + hi) / 2
        for token, sname, i, n in socket_list(e):
            key = token.lower()
            if key.startswith("grip_r"):
                loc = Vector()
            else:
                f = SOCKET_POS.get(key, SOCKET_POS.get(key.split("_")[0], (0, 0, 1.0)))
                spread = ((i + 0.5) / n - 0.5) * 1.2 if n > 1 else 0.0
                local = mid + Vector((f[0] * half.x, (f[1] + spread) * half.y, f[2] * half.z))
                loc = M @ local
            s = new_empty(sname, sock_col, "ARROWS", max(0.02, 0.1 * max(p["dims"])), loc)
            s["socket"] = token
            s.parent = root
    txt = bpy.data.texts.new("EXODUS_NOTES")
    txt.write(f"{name}\n{e['name']} ({p['sub']}) — greybox prop {PROP_VERSION}\n\nSize (X×Y×Z m): {p['dims']}\nPivot: {p['pivot']}\n"
              f"Budgets: {p['lod_tris']}\nLook / notes: {e.get('look') or e.get('notes', '')}\n")
    target.parent.mkdir(parents=True, exist_ok=True)
    bpy.ops.wm.save_as_mainfile(filepath=str(target), check_existing=False, compress=True)
    print(f"BUILT {name} -> {target}")
    return target


def build_suit(p, root, root_col, lods_col, sock_col, mats):
    """Suit greybox on the player's UE5-compatible skeleton (character toolkit), scaled to the suit's height and bulk."""
    here = str(Path(__file__).resolve().parent)
    if here not in sys.path:
        sys.path.insert(0, here)
    import exodus_characters as X
    cdata, _ = X.load_data()
    base = next(c for c in cdata["characters"] if c["id"] == "PLY-001")
    spec = dict(base["skeleton"], height=p["dims"][2])
    c = dict(base, skeleton=spec, assets=[{"asset": p["asset"]}])
    bones = X.SK.build_skeleton(spec)
    arm = X.build_armature(c, bones, root_col)
    arm.parent = root
    lat, dep = p["dims"][0] / 0.6, p["dims"][1] / 0.35
    segs = X.proxy_segments(c, bones)
    names = sorted({s[0] for s in segs})
    for level, (budget, seg) in enumerate(zip(p["lod_tris"], (10, 8, 6))):
        me = bpy.data.meshes.new(f"{p['asset']}_LOD{level}")
        obj = bpy.data.objects.new(me.name, me)
        for n in names:
            obj.vertex_groups.new(name=n)
        bm = bmesh.new()
        dl = bm.verts.layers.deform.verify()
        for bone, h, t, rx, ry, _head in segs:
            X.prism(bm, h, t, rx * lat, ry * dep, segments=seg, vgroup_layer=dl, group_index=names.index(bone))
        for v in bm.verts:  # flat boot soles on the ground plane
            v.co.z = max(v.co.z, 0.0)
        bm.normal_update()
        _box_uvs(bm, (1.0, 1.0, 2.0))
        bm.to_mesh(me)
        bm.free()
        me.materials.append(mats[0])
        lods_col.objects.link(obj)
        obj.parent = arm
        obj.modifiers.new("Armature", "ARMATURE").object = arm
    heads = {b["name"]: Vector(b["head"]) for b in bones}
    for token, sname, i, n in socket_list(p["item"]):
        bone = SUIT_SOCKET_BONES.get(token.lower(), "spine_05")
        if isinstance(bone, list):
            bone = bone[i % len(bone)]
        s = new_empty(sname, sock_col, "ARROWS", 0.1, heads.get(bone, Vector((0, 0, 1.2))))
        s["socket"], s["bone"] = token, bone
        s.parent = root
    root["bones"] = json.dumps([b["name"] for b in bones])
    root["facing"] = "-Y (character convention)"


def validate_prop(root, catalog=None):
    errors, warnings, info = [], [], []
    name = root["asset"]
    info.append(f"Prop {name} ({root['item_name']}, {root['type']})")
    us = bpy.context.scene.unit_settings
    if us.system != "METRIC" or abs(us.scale_length - 1.0) > 1e-6:
        errors.append("Scene units must be Metric with Unit Scale 1.0")
    if root.location.length > 1e-5:
        errors.append("Root empty must sit at the origin")
    budgets = list(root["lod_tris"])
    if catalog and name in catalog:
        budgets = catalog[name]["lod_tris"]
    dims = Vector(root["dims_m"])
    lod0 = None
    for i, limit in enumerate(budgets):
        obj = bpy.data.objects.get(f"{name}_LOD{i}")
        if obj is None or obj.type != "MESH":
            errors.append(f"Missing mesh {name}_LOD{i}")
            continue
        lod0 = lod0 or obj
        t = tri_count(obj)
        if t > limit * 1.10:
            errors.append(f"{obj.name}: {t:,} tris exceeds budget {limit:,} by more than 10%")
        elif t > limit:
            warnings.append(f"{obj.name}: {t:,} tris is over budget {limit:,} (within 10% tolerance)")
        else:
            info.append(f"{obj.name}: {t:,} / {limit:,} tris")
        if not obj.data.uv_layers:
            errors.append(f"{obj.name}: no UV map")
        for slot in obj.material_slots:
            if not slot.material or not slot.material.name.startswith("MI_"):
                errors.append(f"{obj.name}: material slots must hold MI_ materials")
        if name.startswith("SK_"):
            mod = next((m for m in obj.modifiers if m.type == "ARMATURE" and m.object), None)
            if not mod:
                errors.append(f"{obj.name}: no Armature modifier")
            unweighted = sum(1 for v in obj.data.vertices if not any(g.weight > 0 for g in v.groups))
            if unweighted:
                errors.append(f"{obj.name}: {unweighted} unweighted vertices")
    if lod0 is not None:
        lo, hi = world_bounds(lod0)
        size = hi - lo
        if root["family"] == "suit":
            if abs(size.z - dims.z) > 0.05 * dims.z:
                errors.append(f"Suit height {size.z:.3f} m ≠ catalog {dims.z:.3f} m (±5%)")
        elif any(abs(size[k] - dims[k]) > max(0.03 * dims[k], 0.005) for k in range(3)):
            errors.append(f"LOD0 size {tuple(round(v, 3) for v in size)} ≠ catalog {tuple(round(v, 3) for v in dims)} (±3%)")
        pv = root["pivot"]
        if pv in ("base", "feet") and abs(lo.z) > 0.005:
            errors.append(f"Pivot rule '{pv}': bottom must sit at Z=0 (is {lo.z:.3f})")
        if pv == "base" and (abs(lo.x + hi.x) > 0.01 or abs(lo.y + hi.y) > 0.01):
            errors.append("Pivot rule 'base': prop must be centred on X and Y")
        if pv == "center" and ((lo + hi) / 2).length > 0.01:
            errors.append("Pivot rule 'center': bounds must be centred on the origin")
        if pv == "grip" and any(lo[k] > 1e-4 or hi[k] < -1e-4 for k in range(3)):
            errors.append("Pivot rule 'grip': origin must lie inside the prop")
    for s in json.loads(root["sockets"]):
        if s not in bpy.data.objects:
            errors.append(f"Missing socket {s}")
    if name.startswith("SK_"):
        arm = next((o for o in bpy.data.objects if o.type == "ARMATURE"), None)
        if arm is None:
            errors.append("Skeletal prop without an armature")
        else:
            missing = [b for b in json.loads(root["bones"]) if b not in arm.data.bones]
            if missing:
                errors.append(f"Missing bones: {', '.join(missing[:8])}")
            info.append(f"Bones: {len(arm.data.bones)}")
    return errors, warnings, info


# --------------------------------------------------------------------------- validate
def tri_count(obj):
    return sum(len(p.vertices) - 2 for p in obj.data.polygons)


def world_bounds(obj):
    pts = [obj.matrix_world @ Vector(c) for c in obj.bound_box]
    return (Vector((min(p[i] for p in pts) for i in range(3))), Vector((max(p[i] for p in pts) for i in range(3))))


def validate_scene(data=None, index=None, props=None):
    """Validate the open scene. Returns (errors, warnings, info)."""
    errors, warnings, info = [], [], []
    bpy.context.view_layer.update()  # refresh world matrices after any unapplied edits
    roots = [o for o in bpy.data.objects if o.type == "EMPTY" and "exodus_tool_version" in o.keys()]
    if len(roots) != 1:
        return [f"Expected exactly one EXODUS root empty, found {len(roots)}"], warnings, info
    root = roots[0]
    if root.get("kind") == "prop":
        return validate_prop(root, props)
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


def validate_file(path, data=None, index=None, props=None):
    bpy.ops.wm.open_mainfile(filepath=str(path))
    errors, warnings, info = validate_scene(data, index, props)
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
    if root.get("kind") == "prop":
        return export_prop(root, Path(path), out_root)

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


def export_prop(root, blend, out_root):
    name = root["asset"]
    rel = blend.parent.relative_to(blend.parents[2]) if len(blend.parents) > 2 and blend.parents[1].name == "equipment" else Path(blend.parent.name)
    export_dir = Path(out_root) / "export" / "props" / rel
    export_dir.mkdir(parents=True, exist_ok=True)
    objs = [o for o in bpy.data.objects if re.fullmatch(rf"{re.escape(name)}_LOD\d", o.name) or o.name.startswith("SOCKET_") or o.type == "ARMATURE"]
    for o in bpy.context.view_layer.objects:
        o.select_set(False)
    for o in objs:
        o.select_set(True)
    bpy.ops.export_scene.fbx(filepath=str(export_dir / f"{name}.fbx"), use_selection=True, object_types={"MESH", "EMPTY", "ARMATURE"},
                             apply_unit_scale=True, apply_scale_options="FBX_SCALE_UNITS", mesh_smooth_type="FACE", add_leaf_bones=False,
                             bake_anim=False, axis_forward="-Z", axis_up="Y", use_armature_deform_only=True)
    sidecar = {}
    for k, v in root.items():
        if k in ("sockets", "bones"):
            v = json.loads(v)
        elif hasattr(v, "__len__") and not isinstance(v, str):
            v = list(v)
        sidecar[k] = v
    sidecar["socket_transforms"] = [{"name": o.name, "socket": o.get("socket", ""), "bone": o.get("bone", ""),
                                     "location": list(o.matrix_world.translation), "rotation_euler": list(o.matrix_world.to_euler())}
                                    for o in bpy.data.objects if o.name.startswith("SOCKET_")]
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
    ap.add_argument("command", choices=["scaffold", "build", "validate", "export", "list"])
    ap.add_argument("files", nargs="*", help=".blend files for validate/export")
    ap.add_argument("--asset", nargs="+")
    ap.add_argument("--part", nargs="+")
    ap.add_argument("--category", nargs="+")
    ap.add_argument("--all", action="store_true", help="every block part (and, with build, every prop too)")
    ap.add_argument("--props", action="store_true", help="every component, resource and equipment prop")
    ap.add_argument("--prop", nargs="+", help="props by item id (e.g. multitool iron_ore)")
    ap.add_argument("--data")
    ap.add_argument("--out", default=str(repo_root()))
    ap.add_argument("--force", action="store_true")
    args = ap.parse_args(argv)
    data, index = load_data(args.data)
    props = props_catalog(Path(args.data).parent if args.data else None)
    props_index = {p["asset"]: p for p in props}
    want_props = args.props or args.prop or (args.all and args.command == "build")
    chosen_props = [p for p in props if args.props or args.all or (args.prop and p["id"] in args.prop)] if want_props else []
    blocks = args.asset or args.part or args.category or args.all

    if args.command == "list":
        for name in (select_assets(args, data, index) if blocks else []):
            part, asset = index[name]
            print(f"{name:55s} {part['id']}  {asset['grid']}  {asset['size_cells']}  tris {asset['lod_tris'][0]:>6}")
        for p in (props if args.props or args.prop else []):
            if not args.prop or p["id"] in args.prop:
                print(f"{p['asset']:55s} {p['id']:24s} {p['sub']:12s} tris {p['lod_tris']}")
        return 0
    if args.command in ("scaffold", "build"):
        if blocks:
            for name in select_assets(args, data, index):
                scaffold(name, data, index, args.out, args.force, full=args.command == "build")
        if args.command == "build":
            for p in chosen_props:
                build_prop(p, args.out, args.force)
        if not blocks and not chosen_props:
            raise SystemExit("Nothing selected: use --asset, --part, --category, --all, --props or --prop")
        return 0
    if not args.files:
        raise SystemExit(f"{args.command} needs one or more .blend files")
    ok = True
    for f in args.files:
        if args.command == "validate":
            ok = validate_file(f, data, index, props_index) and ok
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
