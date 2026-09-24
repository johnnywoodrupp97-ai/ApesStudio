"""EXODUS PROTOCOL — Blender level toolkit (Blender 4.2+).

Scaffolds level blockouts, true-scale voxel planets, the Metrics Gym and modular kit
libraries from the Level Design Bible, validates them, and exports geometry plus a
markers sidecar for the engine.

    blender -b -P tools/blender/exodus_levels.py -- scaffold --level KES-004
    blender -b -P tools/blender/exodus_levels.py -- scaffold --group KVL PLN
    blender -b -P tools/blender/exodus_levels.py -- scaffold --all [--no-maps]
    blender -b -P tools/blender/exodus_levels.py -- gym
    blender -b -P tools/blender/exodus_levels.py -- kit --kit KIT-KES      (or --all-kits)
    blender -b -P tools/blender/exodus_levels.py -- validate assets/levels/kestrel-valley/LVL_KVL_001_KestrelValley.blend
    blender -b -P tools/blender/exodus_levels.py -- export   assets/levels/kestrel-valley/LVL_KVL_001_KestrelValley.blend
    blender -b -P tools/blender/exodus_levels.py -- list --group KES

Options: --data <levels.json>, --out <root> (default: repository root), --force.
Existing files are never overwritten without --force. Also runs with the stand-alone
``bpy`` module (``python tools/blender/exodus_levels.py ...``).
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
REGION_TYPES = {"Open Region", "Planet Region", "Space Region", "Space Arena"}
FLOOR_TYPES = {"Interior", "Hub", "Dungeon", "Set Piece", "Procedural Template"}
ALLOWED = ("LVL_", "BLK_", "TER_", "PS_", "SP_", "HS_", "TRG_", "VOL_", "POI_", "LM_", "CAM_", "SPL_", "DOOR_", "COV_", "LT_", "NAV_", "KIT_", "REF_", "SM_KIT_")
MARKER_HINTS = {"SPL_Route93": [(-2000, -4000, 0), (-2000, 4000, 0)]}
COLORS = {"PLN": (0.3, 0.5, 0.9), "KVL": (0.8, 0.65, 0.4), "KES": (0.85, 0.5, 0.2), "ORB": (0.55, 0.6, 0.7),
          "DRF": (0.5, 0.35, 0.75), "SEE": (0.35, 0.75, 0.55), "PRC": (0.6, 0.6, 0.6)}


def repo_root():
    for parent in [HERE.parent] + list(HERE.parents):
        if (parent / "docs" / "level-bible").exists() or (parent / "tools" / "levels").exists():
            return parent
    return Path.cwd()


def load_data(path=None):
    path = Path(path) if path else repo_root() / "docs" / "level-bible" / "data" / "levels.json"
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    return data, {lv["id"]: lv for lv in data["levels"]}


def pascal(t):
    t = t.replace("×", "x").replace("&", "And").replace("'", "").replace("—", " ")
    return "".join(p[:1].upper() + p[1:] for p in re.split(r"[^0-9A-Za-z]+", t) if p)


# --------------------------------------------------------------------------- scene helpers
def fresh_scene(name):
    bpy.ops.wm.read_factory_settings(use_empty=True)
    sc = bpy.context.scene
    sc.name = name
    sc.unit_settings.system = "METRIC"
    sc.unit_settings.length_unit = "METERS"
    sc.unit_settings.scale_length = 1.0
    return sc


def col(name, parent):
    c = bpy.data.collections.new(name)
    parent.children.link(c)
    return c


def mat(name, rgb, alpha=1.0):
    m = bpy.data.materials.get(name) or bpy.data.materials.new(name)
    m.diffuse_color = (*rgb, alpha)
    return m


def box_mesh(name, size, center=(0, 0, 0), origin_offset=None):
    """Axis-aligned box of ``size`` (x, y, z) around ``center``; mesh coordinates relative to the object origin."""
    bm = bmesh.new()
    bmesh.ops.create_cube(bm, size=1.0)
    bmesh.ops.transform(bm, matrix=Matrix.Diagonal(Vector((*size, 1))), verts=bm.verts[:])
    if origin_offset:
        bmesh.ops.translate(bm, vec=Vector(origin_offset), verts=bm.verts[:])
    me = bpy.data.meshes.new(name)
    bm.to_mesh(me)
    bm.free()
    obj = bpy.data.objects.new(name, me)
    obj.location = center
    return obj


def wire_box(name, size, center, collection):
    o = box_mesh(name, size, center)
    o.display_type = "WIRE"
    o.hide_render = True
    collection.objects.link(o)
    return o


def cylinder(name, radius, depth, center, collection, segments=48, wire=False):
    bm = bmesh.new()
    bmesh.ops.create_cone(bm, cap_ends=True, segments=segments, radius1=radius, radius2=radius, depth=depth)
    me = bpy.data.meshes.new(name)
    bm.to_mesh(me)
    bm.free()
    o = bpy.data.objects.new(name, me)
    o.location = (center[0], center[1], center[2] + depth / 2)
    if wire:
        o.display_type = "WIRE"
        o.hide_render = True
    collection.objects.link(o)
    return o


def empty(name, collection, loc=(0, 0, 0), display="PLAIN_AXES", size=1.0, **props):
    e = bpy.data.objects.new(name, None)
    e.empty_display_type = display
    e.empty_display_size = size
    e.location = loc
    for k, v in props.items():
        e[k] = v
    collection.objects.link(e)
    return e


def label(text, loc, size, collection, name=None):
    cu = bpy.data.curves.new(name or f"REF_Label_{pascal(text)[:40]}", "FONT")
    cu.body = text
    cu.size = size
    cu.align_x = "CENTER"
    o = bpy.data.objects.new(name or f"REF_Label_{pascal(text)[:40]}", cu)
    o.location = loc
    collection.objects.link(o)
    return o


def poly_curve(name, points, collection):
    cu = bpy.data.curves.new(name, "CURVE")
    cu.dimensions = "3D"
    sp = cu.splines.new("POLY")
    sp.points.add(len(points) - 1)
    for p, xyz in zip(sp.points, points):
        p.co = (*xyz, 1)
    o = bpy.data.objects.new(name, cu)
    collection.objects.link(o)
    return o


def grid_mesh(name, w, d, seg_x, seg_y, height_fn, collection):
    bm = bmesh.new()
    verts = []
    for j in range(seg_y + 1):
        row = []
        for i in range(seg_x + 1):
            x = -w / 2 + w * i / seg_x
            y = -d / 2 + d * j / seg_y
            row.append(bm.verts.new((x, y, height_fn(x, y))))
        verts.append(row)
    for j in range(seg_y):
        for i in range(seg_x):
            bm.faces.new((verts[j][i], verts[j][i + 1], verts[j + 1][i + 1], verts[j + 1][i]))
    uv = bm.loops.layers.uv.new("UVMap")
    for f in bm.faces:
        for lp in f.loops:
            lp[uv].uv = (lp.vert.co.x / w + 0.5, lp.vert.co.y / d + 0.5)
    me = bpy.data.meshes.new(name)
    bm.to_mesh(me)
    bm.free()
    o = bpy.data.objects.new(name, me)
    collection.objects.link(o)
    return o


def edges_grid(name, w, d, step, collection, z=0.0):
    bm = bmesh.new()
    nx, ny = max(1, round(w / step)), max(1, round(d / step))
    for i in range(nx + 1):
        x = -w / 2 + w * i / nx
        bm.edges.new((bm.verts.new((x, -d / 2, z)), bm.verts.new((x, d / 2, z))))
    for j in range(ny + 1):
        y = -d / 2 + d * j / ny
        bm.edges.new((bm.verts.new((-w / 2, y, z)), bm.verts.new((w / 2, y, z))))
    me = bpy.data.meshes.new(name)
    bm.to_mesh(me)
    bm.free()
    o = bpy.data.objects.new(name, me)
    o.hide_render = True
    collection.objects.link(o)
    return o


def smoothstep(e0, e1, x):
    t = max(0.0, min(1.0, (x - e0) / (e1 - e0)))
    return t * t * (3 - 2 * t)


def terrain_fn(lv):
    s = lv["size"]
    w, d = s["w"], s["d"]
    t = lv.get("terrain") or {}
    rim = t.get("rim_height", 0)
    noise = t.get("floor_noise", s["h"] * 0.01)
    feats = t.get("features", [])

    def f(x, y):
        z = noise * (math.sin(x / 390.0) * math.cos(y / 510.0) + 0.5 * math.sin((x + y) / 170.0) + 0.25 * math.cos(x / 83.0 - y / 97.0))
        if rim:
            edge = min(w / 2 - abs(x), d / 2 - abs(y)) / (min(w, d) / 2)
            z += rim * (1 - smoothstep(0.0, 0.14, edge)) * (0.8 + 0.2 * math.sin(x / 700.0 + y / 900.0))
        for kind, fx, fy, fr, fh in feats:
            r = math.hypot(x - fx * 1000, y - fy * 1000) / (fr * 1000)
            if kind == "mesa":
                z += fh * (1 - smoothstep(0.85, 1.0, r))
            elif kind in ("hills", "basin"):
                z += fh * max(0.0, 1 - r) ** 2 * (1.0 if kind == "basin" else 0.7 + 0.3 * math.sin(x / 220.0) * math.cos(y / 260.0))
            elif kind == "flat":
                z *= smoothstep(0.7, 1.0, r)
        return z
    return f


# --------------------------------------------------------------------------- planet scaffold
FACES = {"PX": (Vector((1, 0, 0)), Vector((0, 1, 0)), Vector((0, 0, 1))), "NX": (Vector((-1, 0, 0)), Vector((0, -1, 0)), Vector((0, 0, 1))),
         "PY": (Vector((0, 1, 0)), Vector((-1, 0, 0)), Vector((0, 0, 1))), "NY": (Vector((0, -1, 0)), Vector((1, 0, 0)), Vector((0, 0, 1))),
         "PZ": (Vector((0, 0, 1)), Vector((0, 1, 0)), Vector((-1, 0, 0))), "NZ": (Vector((0, 0, -1)), Vector((0, 1, 0)), Vector((1, 0, 0)))}


def cube_face(name, face, radius, seg, collection, material):
    normal, u_axis, v_axis = FACES[face]
    bm = bmesh.new()
    uv = bm.loops.layers.uv.new("UVMap")
    grid = []
    for j in range(seg + 1):
        row = []
        for i in range(seg + 1):
            a, b = -1 + 2 * i / seg, -1 + 2 * j / seg
            p = (normal + u_axis * a + v_axis * b).normalized() * radius
            row.append((bm.verts.new(p), (i / seg, j / seg)))
        grid.append(row)
    for j in range(seg):
        for i in range(seg):
            quad = [grid[j][i], grid[j][i + 1], grid[j + 1][i + 1], grid[j + 1][i]]
            fce = bm.faces.new([q[0] for q in quad])
            for lp, q in zip(fce.loops, quad):
                lp[uv].uv = q[1]
    bm.normal_update()
    me = bpy.data.meshes.new(name)
    bm.to_mesh(me)
    bm.free()
    me.materials.append(material)
    o = bpy.data.objects.new(name, me)
    collection.objects.link(o)
    return o


def shell(name, radius, collection, segments=48):
    bm = bmesh.new()
    bmesh.ops.create_uvsphere(bm, u_segments=segments, v_segments=segments // 2, radius=radius)
    me = bpy.data.meshes.new(name)
    bm.to_mesh(me)
    bm.free()
    o = bpy.data.objects.new(name, me)
    o.display_type = "WIRE"
    o.hide_render = True
    collection.objects.link(o)
    return o


def latlon(lat, lon, r):
    la, lo = math.radians(lat), math.radians(lon)
    return Vector((math.cos(la) * math.cos(lo), math.cos(la) * math.sin(lo), math.sin(la))) * r


def write_face_maps(lv, out_dir, res=1024):
    try:
        import numpy as np
    except ImportError:
        print("  (numpy unavailable: skipping face-map templates)")
        return []
    sc = bpy.context.scene
    sc.render.image_settings.file_format = "PNG"
    sc.render.image_settings.color_mode = "BW"
    sc.render.image_settings.color_depth = "16"
    out_dir.mkdir(parents=True, exist_ok=True)
    written = []
    for m, value in (("Height", 0.5), ("Biome", 0.0), ("Ore", 0.0), ("Bloom", 0.0)):
        for face in FACES:
            img = bpy.data.images.new(f"{m}_{face}", res, res, float_buffer=True)
            px = np.full(res * res * 4, value, dtype=np.float32)
            px[3::4] = 1.0
            img.pixels.foreach_set(px)
            path = out_dir / f"{pascal(lv['name'])}_{m}_{face}.png"
            img.save_render(str(path), scene=sc)
            bpy.data.images.remove(img)
            written.append(path.name)
    return written


def scaffold_planet(lv, data, out_root, maps=True):
    p, n, tn = lv["planet"], lv["planet_numbers"], lv["transition_numbers"]
    R = n["radius_km"] * 1000
    sc = bpy.context.scene
    root_c = col(lv["asset"], sc.collection)
    ter = col(f"{lv['asset']}_Terrain", root_c)
    shells = col(f"{lv['asset']}_Shells", root_c)
    marks = col(f"{lv['asset']}_Markers", root_c)
    cams = col(f"{lv['asset']}_Cameras", root_c)
    m = mat(f"MI_Planet_Blockout_{pascal(lv['name'])}", COLORS["PLN"])
    for face in FACES:
        cube_face(f"TER_Face_{face}", face, R, 48, ter, m)
    for nm, r in (("REF_CrustBase", R - n["crust_depth_m"]), ("REF_GravityWell", R * data["planet_standard"]["gravity_zero_frac"]),
                  ("REF_PulseDropout", R + tn["pulse_dropout_m"]), ("REF_StreamingStart", tn["streaming_start_m"]),
                  ("REF_CapitalParking", R + tn["capital_parking_m"])):
        shell(nm, r, shells)
    if not tn["airless"]:
        shell("REF_Atmosphere", R + tn["atmosphere_top_m"], shells)
        shell("REF_CloudDeck", R + tn["cloud_deck_m"], shells)
    else:
        shell("REF_ApproachCap", R + tn["approach_altitude_m"], shells)
    if p["sea_level"] is True:
        shell("REF_SeaLevel", R, shells, segments=64)
    for name, la, lo in p["anchors"]:
        m_id = re.match(r"([A-Z]{3}-\d{3})", name)
        nm = f"LVL_ANCHOR_{m_id.group(1)}" if m_id else f"LVL_ANCHOR_{pascal(name)[:40]}"
        pos = latlon(la, lo, R)
        e = empty(nm, marks, pos, "SINGLE_ARROW", R * 0.03, anchor=name, lat=la, lon=lo)
        e.rotation_euler = pos.normalized().to_track_quat("Z", "Y").to_euler()
    cam = bpy.data.cameras.new("CAM_Orbit")
    cam.clip_end = R * 20
    co = bpy.data.objects.new("CAM_Orbit", cam)
    co.location = Vector((R * 2.2, -R * 2.2, R * 1.4))
    co.rotation_euler = (-co.location).to_track_quat("-Z", "Y").to_euler()
    cams.objects.link(co)
    sc.camera = co
    written = []
    if maps:
        written = write_face_maps(lv, Path(out_root) / Path(lv["blend_path"]).parent / f"{lv['asset']}_maps")
    return written


# --------------------------------------------------------------------------- level scaffold
def bounds_of(lv):
    s = lv["size"]
    zmin, zmax = 0.0, float(s["h"])
    for sp in lv["spaces"]:
        if sp["pos"]:
            zmin = min(zmin, sp["pos"][2])
            zmax = max(zmax, sp["pos"][2] + sp["size"][2])
    if has_terrain(lv):
        fn, n = terrain_fn(lv), 64
        zs = [fn(-s["w"] / 2 + s["w"] * i / n, -s["d"] / 2 + s["d"] * j / n) for i in range(n + 1) for j in range(n + 1)]
        zmin, zmax = min(zmin, min(zs) - 5), max(zmax, max(zs) + 5)
    return (-s["w"] / 2, -s["d"] / 2, zmin), (s["w"] / 2, s["d"] / 2, zmax)


def has_terrain(lv):
    return bool(lv.get("terrain")) or lv["type"] in ("Open Region", "Planet Region", "District")


def layout_spaces(lv):
    s = lv["size"]
    placed, x, y, row_d = [], -s["w"] / 2, -s["d"] / 2, 0.0
    for sp in lv["spaces"]:
        if sp["pos"]:
            placed.append((sp, Vector(sp["pos"])))
            continue
        w, d = min(sp["size"][0], s["w"]), min(sp["size"][1], s["d"])
        if x + w > s["w"] / 2:
            x, y, row_d = -s["w"] / 2, y + row_d, 0.0
        placed.append((sp, Vector((x + w / 2, y + d / 2, 0))))
        x += w
        row_d = max(row_d, d)
    return placed


def clamp_box(size, center, lo, hi):
    """Shrink/shift a box so it stays inside the level bounds."""
    size = [min(size[i], hi[i] - lo[i]) for i in range(3)]
    c = [min(max(center[i], lo[i] + size[i] / 2), hi[i] - size[i] / 2) for i in range(3)]
    return tuple(size), tuple(c)


def marker_spot(name, placed, extra, fallback):
    """Best position for a marker: a space or district whose name matches the marker's last token, else ``fallback``."""
    tail = name.split("_")[-1].lower()
    for key, pos in list(extra.items()) + [(pascal(sp["name"]), pos) for sp, pos in placed]:
        k = key.lower()
        if len(tail) > 2 and (k == tail or k.startswith(tail) or tail.startswith(k)):
            return pos
    return fallback


def marker_objects(lv, placed, colls, lo, hi, extra=None):
    center = Vector(((lo[0] + hi[0]) / 2, (lo[1] + hi[1]) / 2, 0))
    first = placed[0][1] if placed else center
    span = max(hi[0] - lo[0], hi[1] - lo[1])
    k = 0
    for name in lv["markers"]:
        spot = marker_spot(name, placed, extra or {}, placed[k % len(placed)][1] if placed else center)
        k += 1
        if name.startswith("PS_"):
            empty(name, colls["markers"], (first.x, first.y, first.z + 0.1), "ARROWS", 1.0)
        elif name.startswith(("SP_", "POI_", "LM_", "LT_", "COV_", "NAV_")):
            empty(name, colls["markers"], (spot.x + 3, spot.y + 3, spot.z), "SPHERE" if name.startswith("SP_") else "PLAIN_AXES",
                  20.0 if name.startswith("LM_") else 2.0)
        elif name.startswith("TRG_"):
            wire_box(name, *clamp_box((4, 4, 3), (spot.x, spot.y, spot.z + 1.5), lo, hi), colls["volumes"])
        elif name.startswith("HS_"):
            side = {"North": (0, 0.45), "East": (0.45, 0), "South": (0, -0.45), "West": (-0.45, 0)}
            dx, dy = next((v for kk, v in side.items() if kk in name), None) or (0, 0)
            c = (center.x + dx * (hi[0] - lo[0]), center.y + dy * (hi[1] - lo[1]), 2.5) if (dx or dy) else (spot.x, spot.y, spot.z + 2.5)
            wire_box(name, *clamp_box((20, 20, 5), c, lo, hi), colls["volumes"])
        elif name.startswith("VOL_"):
            if "NoBuild" in name:
                size = (300, 300, 120)
            elif "Weather" in name or "NoFly" in name:
                size = (hi[0] - lo[0], hi[1] - lo[1], hi[2] - lo[2])
            elif "LandingZone" in name:
                size = (60, 60, 20)
            elif "DockingBay" in name:
                size = (60, 40, 25)
            elif "Kill" in name:
                size = (hi[0] - lo[0], hi[1] - lo[1], 10)
            elif "BaseSite" in name:
                size = (50, 50, 20)
            else:
                size = tuple(placed[0][0]["size"]) if placed else (20, 20, 10)
            c = spot if not ("Weather" in name or "NoFly" in name or "Kill" in name) else Vector((center.x, center.y, lo[2]))
            zc = c.z + size[2] / 2 if "Kill" not in name else lo[2] + 5
            wire_box(name, *clamp_box(size, (c.x, c.y, zc), lo, hi), colls["volumes"])
        elif name.startswith("CAM_"):
            cam = bpy.data.cameras.new(name)
            cam.clip_end = max(1000.0, span * 4)
            o = bpy.data.objects.new(name, cam)
            o.location = (spot.x - 12, spot.y - 12, spot.z + 6)
            o.rotation_euler = (spot + Vector((0, 0, 2)) - o.location).to_track_quat("-Z", "Y").to_euler()
            colls["cameras"].objects.link(o)
        elif name.startswith("SPL_"):
            pts = MARKER_HINTS.get(name) or [(lo[0] - span * 0.2, lo[1] - span * 0.2, hi[2] * 0.5), (first.x, first.y, first.z + 2)]
            poly_curve(name, pts, colls["splines"])
        else:
            empty(name, colls["markers"], (spot.x, spot.y, spot.z), "PLAIN_AXES", 2.0)


def scaffold_level(lv, data, index, out_root, force=False, maps=True):
    target = Path(out_root) / lv["blend_path"]
    if target.exists() and not force:
        print(f"SKIP  {lv['asset']}: {target} exists (use --force to overwrite)")
        return None
    sc = fresh_scene(lv["asset"])
    s = lv["size"]
    root = empty(lv["asset"], sc.collection, (0, 0, 0), "CUBE", max(2.0, min(s["w"], s["d"]) * 0.01))
    meta = {"exodus_level_version": TOOL_VERSION, "kind": "planet" if lv["type"] == "Planet" else "level", "level_id": lv["id"],
            "level_name": lv["name"], "type": lv["type"], "size": json.dumps(s), "budget": json.dumps(lv["budget"]),
            "markers": json.dumps(lv["markers"]), "spaces": json.dumps([sp["name"] for sp in lv["spaces"]])}
    for k, v in meta.items():
        root[k] = v
    extra = []
    if lv["type"] == "Planet":
        root["planet_numbers"], root["transition_numbers"] = json.dumps(lv["planet_numbers"]), json.dumps(lv["transition_numbers"])
        extra = scaffold_planet(lv, data, out_root, maps)
    else:
        lo, hi = bounds_of(lv)
        root["bounds_min"], root["bounds_max"] = list(lo), list(hi)
        base = col(lv["asset"], sc.collection)
        colls = {k: col(f"{lv['asset']}_{v}", base) for k, v in (("blockout", "Blockout"), ("terrain", "Terrain"), ("markers", "Markers"),
                                                                   ("volumes", "Volumes"), ("splines", "Splines"), ("cameras", "Cameras"), ("ref", "Reference"))}
        wire_box("REF_Bounds", (hi[0] - lo[0], hi[1] - lo[1], hi[2] - lo[2]), ((lo[0] + hi[0]) / 2, (lo[1] + hi[1]) / 2, (lo[2] + hi[2]) / 2), colls["ref"])
        floor_m = mat(f"MI_Blockout_{lv['group']}", COLORS[lv["group"]])
        if has_terrain(lv):
            seg = int(min(160, max(16, s["w"] / 50)))
            t = grid_mesh(f"TER_{lv['asset']}", s["w"], s["d"], seg, int(min(160, max(16, s["d"] / 50))), terrain_fn(lv), colls["terrain"])
            t.data.materials.append(mat("MI_Terrain_Blockout", (0.62, 0.55, 0.42)))
        placed = layout_spaces(lv)
        for sp, pos in placed:
            w, d, h = sp["size"]
            nm = pascal(sp["name"])[:48]
            v = wire_box(f"VOL_Room_{nm}", (w, d, h), (pos.x, pos.y, pos.z + h / 2), colls["volumes"])
            v["purpose"] = sp["purpose"]
            if lv["type"] in FLOOR_TYPES:
                fl = box_mesh(f"BLK_{nm}_Floor", (w, d, 0.2), (pos.x, pos.y, pos.z - 0.1))
                fl.data.materials.append(floor_m)
                colls["blockout"].objects.link(fl)
        by_name = {sp["name"]: pos for sp, pos in placed}
        for a, b, kind in lv["connections"]:
            if a in by_name and b in by_name:
                mid = (by_name[a] + by_name[b]) / 2
                empty(f"DOOR_{pascal(a)[:24]}_{pascal(b)[:24]}", colls["markers"], mid, "CUBE", 1.2, connection=kind)
        extra = {}
        if lv["id"] == "KVL-001":
            extra = {pascal(o["key"] or o["name"]): Vector((o["pos"][0] * 1000, o["pos"][1] * 1000, 0))
                     for o in data["levels"] if o["group"] == "KVL" and o["pos"] and o["id"] != "KVL-001"}
            extra.update({pascal(o["name"]): v for o in data["levels"] if o["group"] == "KVL" and o["pos"] and o["id"] != "KVL-001"
                          for v in [Vector((o["pos"][0] * 1000, o["pos"][1] * 1000, 0))]})
            extra["Complex"] = extra.get("KestrelComplex", Vector((0, 0, 0)))
        marker_objects(lv, placed, colls, lo, hi, extra)
        cell = lv["budget"].get("cell_m")
        if cell:
            edges_grid("REF_StreamingGrid", s["w"], s["d"], cell, colls["ref"], z=0.5)
        op = lv.get("on_planet")
        if op and lv["type"] in ("Open Region", "Planet Region") and op["planet"] in index:
            R = index[op["planet"]]["planet_numbers"]["radius_km"] * 1000
            c = grid_mesh("REF_Curvature", s["w"], s["d"], 40, 40, lambda x, y: -(x * x + y * y) / (2 * R), colls["ref"])
            c.display_type = "WIRE"
            c.hide_render = True
            root["planet_radius_m"] = R
        if lv["id"] == "KVL-001":
            for other in data["levels"]:
                if other["group"] == "KVL" and other["pos"] and other["id"] != "KVL-001":
                    x, y, r = other["pos"]
                    cyl = cylinder(f"VOL_District_{pascal(other['key'] or other['name'])}", r * 1000, min(300.0, hi[2] - lo[2]), (x * 1000, y * 1000, lo[2]), colls["volumes"], wire=True)
                    cyl["level_id"] = other["id"]
                    label(other["name"], (x * 1000, y * 1000, 320), 160, colls["ref"], f"REF_Label_{other['id']}")
                elif other["group"] == "KES" and other["pos"]:
                    empty(f"POI_Level_{other['id'].replace('-', '_')}", colls["markers"], (other["pos"][0] * 1000, other["pos"][1] * 1000, 20), "SINGLE_ARROW", 60.0,
                          level_id=other["id"], level_name=other["name"])
        human = cylinder("REF_Human_1p8m", 0.3, 1.8, (placed[0][1].x + 1.5, placed[0][1].y, placed[0][1].z) if placed else (0, 0, 0), colls["ref"], 12, wire=True)
        human["note"] = "1.8 m scale reference"
    txt = bpy.data.texts.new("EXODUS_NOTES")
    txt.write(f"{lv['id']} {lv['name']} — {lv['type']} · {lv['act']}\n\n{lv['summary']}\n\nGoals: {lv['goals']}\nEncounters: {lv['encounters']}\n"
              f"Set pieces: {lv['setpieces']}\nLandmarks: {lv['landmarks']}\nBudget: {lv['budget']}\nRequired markers: {lv['markers']}\nNotes: {lv['notes']}\n")
    target.parent.mkdir(parents=True, exist_ok=True)
    bpy.ops.wm.save_as_mainfile(filepath=str(target), check_existing=False)
    print(f"OK    {lv['asset']} -> {target}" + (f" (+{len(extra)} face-map templates)" if extra else ""))
    return target


# --------------------------------------------------------------------------- gym
def scaffold_gym(data, out_root, force=False):
    target = Path(out_root) / "assets" / "levels" / "gym" / "LVL_MetricsGym.blend"
    if target.exists() and not force:
        print(f"SKIP  LVL_MetricsGym: {target} exists (use --force to overwrite)")
        return None
    sc = fresh_scene("LVL_MetricsGym")
    root = empty("LVL_MetricsGym", sc.collection, (0, 0, 0), "CUBE", 5, exodus_level_version=TOOL_VERSION, kind="gym")
    base = col("LVL_MetricsGym", sc.collection)
    blk, ref = col("LVL_MetricsGym_Blockout", base), col("LVL_MetricsGym_Reference", base)
    grey, amber, red, blue = mat("MI_Gym_Grey", (0.55, 0.57, 0.6)), mat("MI_Gym_Max", (0.95, 0.65, 0.15)), mat("MI_Gym_Fail", (0.85, 0.2, 0.2)), mat("MI_Gym_Agent", (0.25, 0.55, 0.9))

    def add(name, size, center, m):
        o = box_mesh(name, size, center)
        o.data.materials.append(m)
        blk.objects.link(o)
        return o

    y = 0.0
    lane_w = 0
    for li, lane in enumerate(data["gym"]):
        x = 0.0
        depth = max((i["param"] if i["kind"] == "pad" else 12) for i in lane["items"]) if any(i["kind"] in ("pad", "turn") for i in lane["items"]) else 12
        depth = max(depth, 2 * max((i["param"] for i in lane["items"] if i["kind"] == "turn"), default=0) + 4)
        label(lane["lane"], (-14, y, 0.05), 1.6, ref, f"REF_Label_Lane_{pascal(lane['lane'])}")
        for it in lane["items"]:
            kind, prm, lab = it["kind"], it["param"], it["label"]
            m = red if "fail" in lab.lower() or "lethal" in lab.lower() else (amber if "max" in lab.lower() else grey)
            nm = f"BLK_Gym_{pascal(lane['lane'])}_{pascal(lab)}"[:60]
            width = 8.0
            if kind == "gap":
                add(nm + "_A", (4, 4, 1), (x + 2, y, 0.5), grey)
                add(nm + "_B", (4, 4, 1), (x + 4 + prm + 2, y, 0.5), m)
                width = 8 + prm
            elif kind in ("block", "ledge"):
                add(nm, (3, 3, prm), (x + 1.5, y, prm / 2), m)
                width = 3
            elif kind == "tunnel":
                add(nm + "_L", (6, 0.3, prm), (x + 3, y - 1.65, prm / 2), m)
                add(nm + "_R", (6, 0.3, prm), (x + 3, y + 1.65, prm / 2), m)
                add(nm + "_Roof", (6, 3.6, 0.2), (x + 3, y, prm + 0.1), m)
                width = 6
            elif kind == "corridor":
                add(nm + "_L", (10, 0.3, 3), (x + 5, y - prm / 2 - 0.15, 1.5), m)
                add(nm + "_R", (10, 0.3, 3), (x + 5, y + prm / 2 + 0.15, 1.5), m)
                width = 10
            elif kind == "door":
                dw, dh = prm
                total = dw + 4
                add(nm + "_L", (0.3, 2, dh + 1), (x, y - dw / 2 - 1, (dh + 1) / 2), m)
                add(nm + "_R", (0.3, 2, dh + 1), (x, y + dw / 2 + 1, (dh + 1) / 2), m)
                add(nm + "_Lintel", (0.3, total, 1), (x, y, dh + 0.5), m)
                width = 3
            elif kind == "stairs":
                rise, run = prm
                steps = int(round(3.0 / rise))
                for s_i in range(steps):
                    add(f"{nm}_{s_i:02d}", (run, 2.5, rise * (s_i + 1)), (x + run * (s_i + 0.5), y, rise * (s_i + 1) / 2), m)
                width = run * steps + 1
            elif kind == "ramp":
                length = 6.0
                h = min(7.0, length * math.tan(math.radians(prm)))
                bm = bmesh.new()
                pts = [(0, -1.25, 0), (length, -1.25, 0), (length, 1.25, 0), (0, 1.25, 0), (length, -1.25, h), (length, 1.25, h)]
                vs = [bm.verts.new(p) for p in pts]
                bmesh.ops.convex_hull(bm, input=vs)
                me = bpy.data.meshes.new(nm)
                bm.to_mesh(me)
                bm.free()
                o = bpy.data.objects.new(nm, me)
                o.location = (x, y, 0)
                o.data.materials.append(m)
                blk.objects.link(o)
                width = length + 1
            elif kind == "sill":
                add(nm + "_Low", (3, 0.3, prm), (x + 1.5, y, prm / 2), m)
                add(nm + "_High", (3, 0.3, 1.0), (x + 1.5, y, prm + 1.2 + 0.5), m)
                width = 3
            elif kind == "road":
                add(nm, (30, prm, 0.05), (x + 15, y, 0.025), m)
                width = 30
            elif kind == "turn":
                cylinder(nm, prm, 0.05, (x + prm, y, 0), blk, 64).data.materials.append(m)
                width = prm * 2
            elif kind == "pad":
                cylinder(nm, prm / 2, 0.3, (x + prm / 2, y, 0), blk, 64).data.materials.append(m)
                width = prm
            elif kind == "agent":
                r, h = prm
                cylinder(nm, r, h, (x + r, y, 0), blk, 24).data.materials.append(blue)
                width = max(2 * r, 1.0)
            label(lab, (x + width / 2, y - max(4.0, depth / 2 - 1), 0.05), 0.9, ref, f"REF_Label_{nm[8:]}"[:62])
            x += width + 6
        lane_w = max(lane_w, x)
        y += depth + 10
    floor = box_mesh("BLK_Gym_Floor", (lane_w + 40, y + 20, 0.2), (lane_w / 2, y / 2 - 10, -0.1))
    floor.data.materials.append(mat("MI_Gym_Floor", (0.18, 0.19, 0.22)))
    blk.objects.link(floor)
    root["size"] = json.dumps({"w": lane_w + 40, "d": y + 20})
    target.parent.mkdir(parents=True, exist_ok=True)
    bpy.ops.wm.save_as_mainfile(filepath=str(target), check_existing=False)
    print(f"OK    LVL_MetricsGym -> {target}")
    return target


# --------------------------------------------------------------------------- kits
def piece_offset(size, pivot):
    w, d, h = size
    if pivot == "corner":
        return (w / 2, d / 2, h / 2)
    if pivot == "bottom-center":
        return (0, 0, h / 2)
    return (0, 0, 0)


def scaffold_kit(kit, out_root, force=False):
    fname = f"{kit['code'].replace('-', '_')}_{pascal(kit['name'])}.blend"
    target = Path(out_root) / "assets" / "levels" / "kits" / fname
    if target.exists() and not force:
        print(f"SKIP  {kit['code']}: {target} exists (use --force to overwrite)")
        return None
    sc = fresh_scene(kit["code"])
    empty(f"KIT_{kit['code'].replace('-', '_')}", sc.collection, (0, 0, 0), "CUBE", 1.0, exodus_level_version=TOOL_VERSION, kind="kit",
          kit=kit["code"], pieces=json.dumps(kit["pieces"]))
    base = col(kit["code"], sc.collection)
    ref = col(f"{kit['code']}_Reference", base)
    m = mat(f"MI_{kit['art']}_KitBlockout", (0.6, 0.62, 0.66))
    left = 0.0
    for p in kit["pieces"]:
        name = f"SM_{kit['code'].replace('-', '_')}_{pascal(p['name'])}"
        off = piece_offset(p["size"], p["pivot"])
        w = p["size"][0]
        x = math.ceil((left - (off[0] - w / 2)) * 2) / 2  # pieces sit on the 0.5 m grid, left to right
        o = box_mesh(name, p["size"], (x, 0, 0), origin_offset=off)
        o.data.materials.append(m)
        o["pivot"], o["size_m"], o["tris_budget"] = p["pivot"], list(p["size"]), p["tris"]
        base.objects.link(o)
        label(p["name"], (x + off[0], -3, 0.02), 0.5, ref, f"REF_Label_{name}")
        left = x + off[0] + w / 2 + 3
    target.parent.mkdir(parents=True, exist_ok=True)
    bpy.ops.wm.save_as_mainfile(filepath=str(target), check_existing=False)
    print(f"OK    {kit['code']} ({len(kit['pieces'])} pieces) -> {target}")
    return target


# --------------------------------------------------------------------------- validate
def tris(o):
    return sum(len(p.vertices) - 2 for p in o.data.polygons) if o.type == "MESH" else 0


def validate_scene(data=None, index=None):
    errors, warnings, info = [], [], []
    bpy.context.view_layer.update()
    roots = [o for o in bpy.data.objects if "exodus_level_version" in o.keys()]
    if len(roots) != 1:
        return ["Expected exactly one EXODUS root empty (LVL_/KIT_)"], warnings, info
    root = roots[0]
    kind = root["kind"]
    us = bpy.context.scene.unit_settings
    if us.system != "METRIC" or abs(us.scale_length - 1) > 1e-6:
        errors.append("Scene units must be Metric with Unit Scale 1.0")
    for o in bpy.data.objects:
        if o is not root and not o.name.startswith(ALLOWED):
            warnings.append(f"Object '{o.name}' has no approved prefix")

    if kind == "kit":
        pieces = {f"SM_{root['kit'].replace('-', '_')}_{pascal(p['name'])}": p for p in json.loads(root["pieces"])}
        for name, p in pieces.items():
            o = bpy.data.objects.get(name)
            if not o:
                errors.append(f"Missing kit piece {name}")
                continue
            dims = [o.dimensions[i] for i in range(3)]
            if any(abs(dims[i] - p["size"][i]) > 0.02 for i in range(3)):
                errors.append(f"{name}: dimensions {tuple(round(v, 3) for v in dims)} ≠ catalog {tuple(p['size'])} (±2 cm)")
            lo = Vector((min(v[0] for v in o.bound_box), min(v[1] for v in o.bound_box), min(v[2] for v in o.bound_box)))
            expect = Vector(piece_offset(p["size"], p["pivot"])) - Vector(p["size"]) / 2
            if (lo - expect).length > 0.02:
                errors.append(f"{name}: pivot doesn't follow the '{p['pivot']}' rule")
            t = tris(o)
            if t > p["tris"] * 1.1:
                errors.append(f"{name}: {t:,} tris exceeds budget {p['tris']:,} by more than 10%")
            if any(abs((o.location[i] * 2) - round(o.location[i] * 2)) > 1e-4 for i in range(3)):
                warnings.append(f"{name}: not on the 0.5 m grid")
        info.append(f"Kit {root['kit']}: {len(pieces)} pieces checked")
        return errors, warnings, info

    if kind == "gym":
        info.append(f"Metrics Gym: {sum(1 for o in bpy.data.objects if o.name.startswith('BLK_'))} blockout objects")
        return errors, warnings, info

    lv = index.get(root["level_id"]) if index else None
    budget = lv["budget"] if lv else json.loads(root["budget"])
    required = lv["markers"] if lv else json.loads(root["markers"])
    info.append(f"Level {root['level_id']} {root['level_name']} ({root['type']})")
    names = {o.name for o in bpy.data.objects}
    for m in required:
        if m not in names:
            errors.append(f"Missing required marker {m}")

    if kind == "planet":
        faces = [f"TER_Face_{f}" for f in FACES]
        for f in faces:
            if f not in names:
                errors.append(f"Missing planet face {f}")
        if lv:
            R = lv["planet_numbers"]["radius_km"] * 1000
            emax = lv["planet_numbers"]["max_elevation_m"]
            for f in faces:
                o = bpy.data.objects.get(f)
                if o:
                    ds = [(o.matrix_world @ v.co).length for v in o.data.vertices]
                    if min(ds) < R - emax - 1 or max(ds) > R + emax + 1:
                        errors.append(f"{f}: surface outside radius {R:,.0f} m ± max elevation {emax:,.0f} m")
            info.append(f"Radius {R:,.0f} m; faces {sum(1 for f in faces if f in names)}/6")
        total = sum(tris(o) for o in bpy.data.objects if o.name.startswith(("BLK_", "TER_")))
        if total > budget["blockout_tris"] * 1.1:
            errors.append(f"Planet blockout {total:,} tris exceeds {budget['blockout_tris']:,}")
        return errors, warnings, info

    if lv:
        for sp in lv["spaces"]:
            if f"VOL_Room_{pascal(sp['name'])[:48]}" not in names:
                warnings.append(f"No room volume for space '{sp['name']}'")
    lo, hi = Vector(root["bounds_min"]), Vector(root["bounds_max"])
    tol = 1.0
    geo = [o for o in bpy.data.objects if o.type == "MESH" and not o.name.startswith("REF_")]
    for o in geo:
        for c in o.bound_box:
            p = o.matrix_world @ Vector(c)
            if any(p[i] < lo[i] - tol or p[i] > hi[i] + tol for i in range(3)):
                errors.append(f"{o.name}: extends outside the level bounds")
                break
    blk = [o for o in bpy.data.objects if o.name.startswith(("BLK_", "TER_", "KIT_")) and o.type == "MESH"]
    if budget.get("per") == "cell":
        cell = budget["cell_m"]
        buckets = {}
        for o in blk:
            mw = o.matrix_world
            for poly in o.data.polygons:
                c = mw @ poly.center
                key = (math.floor((c.x - lo.x) / cell), math.floor((c.y - lo.y) / cell))
                buckets[key] = buckets.get(key, 0) + len(poly.vertices) - 2
        worst = max(buckets.values(), default=0)
        if worst > budget["blockout_tris"] * 1.1:
            errors.append(f"A streaming cell has {worst:,} blockout tris (budget {budget['blockout_tris']:,} per cell)")
        info.append(f"Blockout: worst cell {worst:,} / {budget['blockout_tris']:,} tris across {len(buckets)} occupied cells")
    else:
        total = sum(tris(o) for o in blk)
        if total > budget["blockout_tris"] * 1.1:
            errors.append(f"Blockout {total:,} tris exceeds budget {budget['blockout_tris']:,}")
        info.append(f"Blockout {total:,} / {budget['blockout_tris']:,} tris")
    for o in bpy.data.objects:
        if o.name.startswith("KIT_") and any(abs(o.location[i] * 2 - round(o.location[i] * 2)) > 1e-4 for i in range(2)):
            warnings.append(f"{o.name}: kit instance not on the 0.5 m grid")
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
    root = next(o for o in bpy.data.objects if "exodus_level_version" in o.keys())
    blend = Path(path)
    out_dir = Path(out_root) / "export" / "levels" / blend.parent.name
    out_dir.mkdir(parents=True, exist_ok=True)
    kwargs = dict(use_selection=True, object_types={"MESH"}, apply_unit_scale=True, apply_scale_options="FBX_SCALE_UNITS",
                  mesh_smooth_type="FACE", axis_forward="-Z", axis_up="Y", add_leaf_bones=False, bake_anim=False)

    def select(objs):
        for o in bpy.context.view_layer.objects:
            o.select_set(False)
        for o in objs:
            o.select_set(True)

    if root["kind"] == "kit":
        for o in [o for o in bpy.data.objects if o.name.startswith("SM_KIT_") or o.name.startswith("SM_")]:
            if o.type != "MESH":
                continue
            loc = o.location.copy()
            o.location = (0, 0, 0)
            select([o])
            bpy.ops.export_scene.fbx(filepath=str(out_dir / f"{o.name}.fbx"), **kwargs)
            o.location = loc
        print(f"EXPORTED kit {root['kit']} -> {out_dir}")
        return
    geo = [o for o in bpy.data.objects if o.type == "MESH" and o.name.startswith(("BLK_", "TER_", "KIT_"))]
    if geo:
        select(geo)
        bpy.ops.export_scene.fbx(filepath=str(out_dir / f"{blend.stem}.fbx"), **kwargs)
    markers = []
    for o in bpy.data.objects:
        if o is root or o.name.startswith(("BLK_", "TER_", "REF_", "SM_")):
            continue
        entry = {"name": o.name, "type": o.type, "location": list(o.matrix_world.translation), "rotation_euler": list(o.matrix_world.to_euler()),
                 "props": {k: (v if isinstance(v, (int, float, str)) else str(v)) for k, v in o.items()}}
        if o.type == "MESH":
            entry["size"] = list(o.dimensions)
        if o.type == "CURVE":
            entry["points"] = [list(o.matrix_world @ Vector(p.co[:3])) for s_ in o.data.splines for p in s_.points]
        markers.append(entry)
    sidecar = {}
    for k, v in root.items():
        if k in ("size", "budget", "markers", "spaces", "planet_numbers", "transition_numbers"):
            v = json.loads(v)
        elif not isinstance(v, (int, float, str)):
            v = list(v)
        sidecar["required_markers" if k == "markers" else k] = v
    sidecar["markers"] = markers
    (out_dir / f"{blend.stem}.markers.json").write_text(json.dumps(sidecar, indent=1), encoding="utf-8")
    print(f"EXPORTED {blend.stem}: {len(geo)} meshes, {len(markers)} markers -> {out_dir}")


# --------------------------------------------------------------------------- CLI
def main(argv):
    ap = argparse.ArgumentParser(prog="exodus_levels")
    ap.add_argument("command", choices=["scaffold", "gym", "kit", "validate", "export", "list"])
    ap.add_argument("files", nargs="*")
    ap.add_argument("--level", nargs="+")
    ap.add_argument("--group", nargs="+")
    ap.add_argument("--all", action="store_true")
    ap.add_argument("--kit", nargs="+")
    ap.add_argument("--all-kits", action="store_true")
    ap.add_argument("--no-maps", action="store_true")
    ap.add_argument("--data")
    ap.add_argument("--out", default=str(repo_root()))
    ap.add_argument("--force", action="store_true")
    a = ap.parse_args(argv)
    data, index = load_data(a.data)

    def selected():
        out = [lv for lv in data["levels"] if a.all or (a.level and lv["id"] in a.level) or (a.group and lv["group"] in a.group)]
        if not out:
            raise SystemExit("Nothing selected: use --level, --group or --all")
        return out

    if a.command == "list":
        for lv in selected():
            b = lv["budget"]
            print(f"{lv['id']:8s} {lv['asset']:55s} {lv['type']:18s} {b['blockout_tris']:>8,} tris/{b.get('per', 'level')}")
        return 0
    if a.command == "scaffold":
        for lv in selected():
            scaffold_level(lv, data, index, a.out, a.force, maps=not a.no_maps)
        return 0
    if a.command == "gym":
        scaffold_gym(data, a.out, a.force)
        return 0
    if a.command == "kit":
        kits = data["kits"] if a.all_kits else [k for k in data["kits"] if a.kit and k["code"] in a.kit]
        if not kits:
            raise SystemExit("Use --kit KIT-XXX or --all-kits")
        for k in kits:
            scaffold_kit(k, a.out, a.force)
        return 0
    if not a.files:
        raise SystemExit(f"{a.command} needs one or more .blend files")
    ok = True
    for f in a.files:
        if a.command == "validate":
            ok = validate_file(f, data, index) and ok
        else:
            export_file(f, a.out)
    return 0 if ok else 1


if __name__ == "__main__":
    argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else sys.argv[1:]
    sys.exit(main(argv))
