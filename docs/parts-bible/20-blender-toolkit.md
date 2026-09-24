# 20 — Blender Toolkit & Art Pipeline

> `tools/blender/exodus_parts.py` turns every card in this bible into a ready-to-model Blender file, checks finished work against the budgets, and exports it for the engine. Tested with Blender 4.2 (the `bpy` 4.2 module) on all 446 block assets.

## 20.1 Pipeline at a glance

```
 catalog (tools/parts/catalog/*.py)
        │  python3 tools/parts/build.py
        ▼
 docs/parts-bible/*.md  +  data/parts.json  +  data/art_tracker_*.csv
        │  exodus_parts.py scaffold
        ▼
 assets/parts/<category>/<asset>.blend   ← artist models here
        │  exodus_parts.py validate   (repeat until PASS)
        ▼
 exodus_parts.py export
        ▼
 export/parts/<category>/<asset>.fbx (+ _BuildStages, _Parts, .meta.json)  →  engine import
```

## 20.2 Commands
Run from the repository root. `blender -b -P` runs Blender in the background; everything after `--` goes to the tool.

| Task | Command |
|---|---|
| Scaffold one asset | `blender -b -P tools/blender/exodus_parts.py -- scaffold --asset SM_STR_ArmorBlock_Light_LG` |
| Scaffold every asset of a part | `… -- scaffold --part PWR-010` |
| Scaffold a whole category | `… -- scaffold --category LIF PRO` |
| Scaffold everything (446 files, ~20 s) | `… -- scaffold --all` |
| Overwrite an existing file | add `--force` (off by default: artists' files are never replaced by accident) |
| Validate files | `… -- validate assets/parts/power/SM_PWR_Battery_LG.blend [more.blend …]` |
| Export (validates first) | `… -- export assets/parts/power/SM_PWR_Battery_LG.blend` |
| List assets and budgets | `… -- list --category SOW` |
| Other data or output location | `--data path/to/parts.json`, `--out path/to/root` |

The script also runs with the stand-alone `bpy` Python module: `python tools/blender/exodus_parts.py scaffold --asset …`.

**Inside Blender:** open `exodus_parts.py` in the Text Editor and press **Run Script**. An **EXODUS** tab appears in the 3D View sidebar (`N`) with an asset-name field and **Scaffold Asset** / **Validate Scene** buttons.

## 20.3 What the scaffold creates
For each asset, a `.blend` at the path listed on its card, containing:

| Item | Details |
|---|---|
| **Scene units** | Metric, meters, unit scale 1.0 |
| **Root empty** `<asset>` | At the origin; custom properties: part ID, registry ID, grid, size, dimensions, tier, art set, complexity, LOD budgets, build stages, collision limit, mount and airtight faces, texel density, blockout shape |
| **LOD0 blockout** `<asset>_LOD0` | The exact grid volume in the part's blockout shape (cube, slope, corner, 2×1 pieces, round pieces, panels, wall units, flat plates, cylinders), with box-projected UV0 `UVMap` and UV1 `Masks`, and a category-colored `MI_<SET>_Blockout_<CAT>` material |
| **LOD1–3 collections** | Empty, ready for the reduced meshes |
| **Build-stage collections** | `<asset>_BS1…BSn` (2–4 by complexity) |
| **Collision** | `UCX_<asset>_01` matching the blockout (split it into ≤ N hulls) |
| **Sockets** | Every `SOCKET_*` the card lists, on the right face, +X pointing out |
| **Mount markers** | `MOUNT_<Face>` for each mount face, with an `airtight` flag |
| **Moving-part pivots** | `PART_*` empties with the motion text from the card |
| **Reference** | `REF_<asset>_Volume` (exact grid volume, wireframe) and `REF_Human_1p8m` |
| **Notes** | A text block `EXODUS_NOTES` with the card's function, modeling notes, budgets, moving parts, emissives and VFX |

## 20.4 Validation rules

| Check | Result if it fails |
|---|---|
| Exactly one root empty; at the origin with no rotation or scale | **Error** |
| Scene units Metric, scale 1.0 | **Error** |
| `<asset>_LOD0` exists | **Error** (LOD1–3 missing: warning) |
| Rotation and scale applied on LOD meshes | **Error** |
| Triangles ≤ budget | Over by > 10%: **error**; over by ≤ 10%: warning |
| UV0 present | **Error**; missing UV1 `Masks` on LOD0/1: warning |
| Materials named `MI_*`, no empty slots | **Error**; blockout material still on LOD0: warning |
| LODs inside the grid volume (±2 mm) unless the root has `allow_overhang` | **Error** |
| Collision hulls: at least 1, at most the card's limit | **Error** |
| Every socket required by the card exists | **Error** |
| Build-stage collections exist | **Error**; empty stage: warning |
| Size still matches the catalog (catches catalog changes) | **Error** |
| Object names follow the convention | Warning |

`validate` exits with code 1 when any file has errors, so it can run in CI or a pre-commit hook.

## 20.5 Export outputs
`export` refuses to run on a file with validation errors, then writes:

| File | Contents |
|---|---|
| `<asset>.fbx` | LOD0–3, `UCX_` collision, `SOCKET_` empties |
| `<asset>_BuildStages.fbx` | BS1…BSn meshes (if modeled) |
| `<asset>_Parts.fbx` | `PART_` pivots with their `<asset>_Part_*` meshes (if any) |
| `<asset>.meta.json` | Root metadata, sockets (world transforms), mounts (airtight flags) and moving-part pivots, for the engine's block-definition importer |

FBX settings: selection only, mesh + empty, *Apply Unit Scale*, *FBX Units Scale*, face smoothing, modifiers applied, no leaf bones, no animation. Import settings are in [00 §0.3](00-blender-modeling-standards.md).

## 20.6 Production tracking
- `data/art_tracker_parts.csv` has **one row per block asset** (446 rows): budgets, faces, sockets, paths, plus `status`, `owner` and `notes` columns for production.
- `data/art_tracker_props.csv` covers components, resources, equipment, suits and drones.
- Import either CSV into a spreadsheet (Google Sheets, Excel, ShotGrid, Jira) as the art backlog. Suggested statuses: *Not started → Blockout → High-poly → Low-poly → UV/Texture → Stages & LODs → Validated → In engine → Done*.

**Suggested production order** (matches the vertical slice in the game bible, chapter 15):
1. Survivor Scrap set and Act I parts (Tier T0): Scrap Wall, Barricades, Workbench, Diesel Generator, Floodlight, Campfire.
2. Armor shape family (Light), Doors, Catwalks, Windows: everything that's placed thousands of times.
3. Wren launch hardware (Capsule Cockpit, Methalox Engine, Launch Clamp) for M1.07.
4. Life support and colony furniture for Act II.
5. Ships (thrusters, cockpits, tanks), then precursor hero parts.

## 20.7 Adding or changing a part
1. Edit the right module in `tools/parts/catalog/` (for example, add a `P("PWR", "Geothermal Tap", …)` call to `blocks_systems.py`).
2. Run `python3 tools/parts/build.py`. It validates the catalog (unknown recipe items, faces, socket types, duplicate names) and regenerates every chapter, JSON and CSV.
3. Scaffold the new asset: `blender -b -P tools/blender/exodus_parts.py -- scaffold --part PWR-014`.
4. If a size changed on an existing part, `validate` flags the old file: re-scaffold with `--force` into a new file and move the work across.

New parts get the next ID in their category. IDs are assigned in catalog order, so **add new parts at the end of their category** to keep existing IDs stable.
