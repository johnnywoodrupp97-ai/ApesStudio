# 00 — Blender Modeling Standards

> The rules every part card in this bible assumes. If a card and this chapter disagree, the card wins for that part; if this chapter and a tool disagree, fix the tool.
> The numbers here are also exported to `data/parts.json → standards`, which the Blender toolkit ([20](20-blender-toolkit.md)) reads.

## 0.1 Software
| Tool | Version | Use |
|---|---|---|
| **Blender** | 4.2 LTS or newer | Modeling, UVs, LODs, collision, sockets, export |
| Substance 3D Painter | 2024+ | Unique texture sets (M/L/XL parts), damage and wear masks |
| Substance 3D Designer | 2024+ | Trim sheets, tileables, faction skins |
| Marmoset Toolbag (optional) | 4+ | High-to-low bakes for L/XL hero parts |
| EXODUS toolkit | `tools/blender/exodus_parts.py` | Scaffold, validate, export |

## 0.2 Units & scale
- **Scene units:** Metric, Length = Meters, **Unit Scale 1.0**. 1 Blender unit = 1 m.
- **Grid cells:** **Large grid (LG) = 2.5 m**, **Small grid (SG) = 0.5 m**.
- **Snapping:** LG detail snap 0.05 m; SG detail snap 0.01 m. Block volumes are exact multiples of the cell size.
- **Human scale references** (the scaffold adds a 1.8 m reference figure):

| Element | Size |
|---|---|
| Character height | 1.8 m (suited 1.9–1.95 m) |
| Door opening | 1.2 × 2.2 m (double 2.4 × 2.2 m) |
| Corridor | 2.5 m (one LG cell) |
| Stair rise / run | 0.25 m / 0.25 m (45°) |
| Seat / table / counter height | 0.45 / 0.75 / 0.9 m |
| Handrail height | 1.1 m |
| Interact point height | 1.0–1.3 m above the walkable floor |
| Crawl duct | 1.2 m square |

## 0.3 Axes, pivot & orientation
- **Front = +X, Up = +Z, Left = +Y** (Blender's Front view looks along +Y, so switch to Right view, `Numpad 3`, to see the front face).
- Face names used everywhere: **front (+X), back (−X), left (+Y), right (−Y), top (+Z), bottom (−Z)**.
- **Pivot:** the origin sits at the **center of the part's grid volume** (not the mesh's bounding box). Multi-cell parts pivot at the center of the whole volume.
- **Transforms applied:** location (0,0,0) on the root, rotation 0, scale 1 on every mesh.
- **Engine import settings** (locked in the M0 engine spike; see the game bible chapter 13):
  - **Unreal Engine 5:** FBX import with *Convert Scene* ON, *Force Front XAxis* ON, uniform scale 1.0, *Combine Meshes* OFF, sockets from `SOCKET_` empties.
  - **Unity 6:** *Bake Axis Conversion* ON, scale factor 1, *Import Constraints* OFF.

## 0.4 Files & folders
```
assets/parts/<category_key>/<asset>.blend       one asset per .blend (created by the scaffold)
assets/parts/<category_key>/textures/           unique texture sets (T_*)
assets/shared/trims/                            trim sheets and tileables per art set
assets/shared/debris/                           shared debris library (SM_Debris_*)
export/parts/<category_key>/<asset>.fbx         body: LODs + collision + sockets
export/parts/<category_key>/<asset>_BuildStages.fbx
export/parts/<category_key>/<asset>_Parts.fbx   moving sub-meshes with pivots
export/parts/<category_key>/<asset>.meta.json   sidecar: mounts, airtight faces, sockets, pivots, budgets
```

## 0.5 Naming conventions

| Prefix / suffix | Meaning | Example |
|---|---|---|
| `SM_` | Static mesh asset | `SM_PWR_Battery_LG` |
| `SK_` | Skeletal mesh (weapons, suits, drones, parachute) | `SK_EQP_AssaultRifle_1P` |
| `SM_<CAT>_<Name>[_<Variant>]_<LG\|SG>` | Block asset name pattern | `SM_STR_ArmorSlope_Heavy_SG` |
| `<asset>_LOD0…3` | LOD meshes | `SM_PWR_Battery_LG_LOD2` |
| `<asset>_BS1…4` | Construction-stage meshes | `SM_PWR_Battery_LG_BS1` |
| `<asset>_Part_<Name>` | Moving sub-mesh (child of a `PART_` pivot) | `SM_DOR_Door_LG_Part_DoorLeaves` |
| `UCX_<asset>_NN` | Convex collision hull | `UCX_SM_PWR_Battery_LG_01` |
| `SOCKET_<Type>_<Face>_NN` | Attachment point (empty) | `SOCKET_ConveyorLarge_Back_01` |
| `MOUNT_<Face>` | Mount face marker (empty, custom prop `airtight`) | `MOUNT_Bottom` |
| `PART_<Name>` | Moving-part pivot (empty) | `PART_Yaw` |
| `REF_` | Reference only, never exported | `REF_Human_1p8m` |
| `MI_<SET>_<Name>` | Material instance | `MI_IND_ArmorHeavy` |
| `M_<Name>` | Master material (engine side) | `M_Block_Master` |
| `T_<Set>_<Name>_<Map>` | Texture: `_BC` base color, `_N` normal, `_ORM` occlusion/roughness/metal, `_E` emissive, `_M` masks | `T_IND_TrimA_ORM` |

Category codes: `STR DOR PWR LIF PRD AGR LOG PRO MEC CTL COL MED DEF UTL SOW` (components `CMP`, resources `RES`, equipment `EQP`, suits `SUIT`).

## 0.6 Collection structure (every part file)
```
<asset>                         ← root collection
├─ <asset> (Empty, cube)        ← root empty with metadata custom properties
├─ <asset>_LOD0 … _LOD3         ← one mesh each: <asset>_LOD0 …
├─ <asset>_BuildStages
│   ├─ <asset>_BS1 … BSn        ← construction-stage meshes
├─ <asset>_Collision            ← UCX_<asset>_NN
├─ <asset>_Sockets              ← SOCKET_* empties (+X points out of the face)
├─ <asset>_Mounts               ← MOUNT_<Face> empties
├─ <asset>_Parts                ← PART_* pivots, each parenting <asset>_Part_* meshes
└─ <asset>_Reference            ← REF_* grid volume + 1.8 m human (not exported)
```

## 0.7 Grid fit, mounting & tiling
1. **Stay inside the volume.** Every LOD must fit inside the part's grid volume (±2 mm). Deliberate overhangs (deployed radiator fins, wind-turbine blades) need the root custom property `allow_overhang = True` and a note on the card.
2. **Mount faces are flush.** A mount face must have a flat contact area covering at least 60% of the face, exactly on the volume boundary.
3. **Airtight faces are fully closed.** No gaps, holes or open grilles on a face listed as airtight.
4. **Conveyor apertures are standard:** LG port 1.0 × 1.0 m square, SG port 0.25 × 0.25 m, both centered on the face (or on the socket position). Every conveyor port gets the hazard-stripe trim ring.
5. **Armor tiling rhythm:** panel seams every **0.625 m (LG)** / **0.125 m (SG)**, edge bevel **20 mm (LG light) / 60 mm (LG heavy) / 5 mm (SG)**. Neighbouring armor pieces must read as one continuous hull in any rotation.
6. **Shape families share profiles.** All slopes, corners and round pieces use identical edge profiles so any combination closes without gaps.

## 0.8 Polycount budgets & LODs

| Complexity | LG LOD0 | SG LOD0 | Build stages | Max collision hulls | Textures |
|---|---|---|---|---|---|
| **S** Simple | 800 | 300 | 2 | 2 | Shared trim sheet only |
| **M** Standard | 4,000 | 1,500 | 3 | 6 | Trims + one 1K unique atlas |
| **L** Complex | 12,000 | 5,000 | 3 | 12 | Trims + one 2K unique atlas |
| **XL** Hero | 40,000 | 12,000 | 4 | 24 | 4K unique set + trims |

- **LOD chain:** LOD1 = 50%, LOD2 = 20%, LOD3 = 6% of LOD0 (min 12 tris). Screen sizes 1.0 / 0.5 / 0.25 / 0.1.
- **What each LOD drops:** LOD1 removes bolts, small bevels and interior details behind glass; LOD2 removes secondary shapes and moving-part detail (moving parts stay but simplify); LOD3 keeps the silhouette only (armor LOD3 may be the grid-volume box with the shape's profile).
- **Budgets are ceilings, not targets.** The validator errors above +10%, warns between 100% and 110%.
- **Heavily instanced parts** (armor, truss, catwalks, conveyors, windows) should come in at ≤ 75% of budget; a large hull can contain 50,000 of them.

## 0.9 Topology & shading
- **Mid-poly workflow** for S and M parts: real bevels + *Weighted Normal* modifier (Face Area, Keep Sharp) and trim sheets. **No per-asset high-poly bake.**
- **High-to-low bakes** are allowed for L and XL hero parts (reactors, cockpits, jump core, turrets).
- Quads and tris are both fine; the exporter triangulates. Avoid long thin triangles (aspect > 10:1) on large flat faces.
- **No hidden faces** inside closed volumes or on faces that are always covered by a neighbour (the back of a wall-mounted part).
- Smoothing via custom split normals; mark sharps at > 30°.
- **Modifiers:** only Weighted Normal, Triangulate and Bevel (harden normals) may be left live; apply everything else before export.

## 0.10 UVs & texel density
| Channel | Purpose | Rules |
|---|---|---|
| **UV0 `UVMap`** | Trim sheets / unique atlas | Trims may overlap and tile; unique atlases 0–1, 8 px padding at 2K |
| **UV1 `Masks`** | Damage, dirt, burn and Bloom-growth masks | Unique, non-overlapping, 0–1, 4 px padding at 1K. Required on every LOD0 and LOD1. |

**Texel density:** LG **512 px/m**, SG **1,024 px/m** (seen closer), 1P viewmodels 2,048 px/m, 3P equipment 1,024 px/m. Trim sheets are authored at 512 px/m for LG and reused at 2× density on SG through UV scaling.

## 0.11 Materials & texture maps
- **PBR metal/roughness.** Packed `_ORM` (R = AO, G = roughness, B = metallic). Emissive in `_E`.
- **Max material slots:** S = 1, M = 2, L = 3, XL = 4 (glass counts as a slot).
- **One master material** drives all blocks (`M_Block_Master`). Parameters every part supports:

| Parameter | Range | Driven by |
|---|---|---|
| `Damage` | 0–1 | Block HP (scratches, dents via the UV1 mask) |
| `Burn` | 0–1 | Fire / re-entry heat |
| `Dirt` | 0–1 | Age, planet dust |
| `Wetness` | 0–1 | Weather |
| `BloomGrowth` | 0–1 | Local Verdance coverage: green veins and lichen creep in from edges |
| `Build` | 0–1 | Construction % (weld-in dissolve) |
| `EmissiveState` | enum | Off / Functional / Warning / Error / Working |

- **Part-specific parameters** named on the cards: `Charge`, `Level`, `Load`, `Crack`, `StressState`, `Heat`.
- **Glass:** one shared `MI_Shared_Glass` family (clear, frosted, cockpit, crack states); the only translucent material allowed.
- **Masked materials** are allowed only for grates and chain-link fences.

## 0.12 Emissive & light standards
| Color | Meaning |
|---|---|
| Green `#3CE66E` | Functional / ready / clean |
| Amber `#FFB020` | Warning / partial / cycling |
| Red `#FF3B30` | Off / locked / error |
| Blue `#3AA8FF` | Working / processing |
| Teal `#2EE6D6` | Sower technology |
| Magenta `#FF4FD8` | Fusion plasma and grow lights |

Status lights are ≥ 2 cm (LG) so they read at 30 m. Light sockets sit 5 cm in front of the lamp surface.

## 0.13 Construction stages (build states)
The player welds blocks in over time, so each part shows its progress:

| Stage | Look | Budget |
|---|---|---|
| **BS1 Frame** | Girder skeleton outlining the volume plus a component pile (`SM_CMP_<Name>_Pile`) | ≤ 30% of LOD0 |
| **BS2 Structure** | Main panels half on; internals exposed | ≤ 60% of LOD0 |
| **BS3 Systems** | Machinery and wiring in, some cover panels missing | ≤ 90% of LOD0 |
| **BS4 Finishing** (XL only) | Everything except trim and final covers | ≤ 100% of LOD0 |

Stages share the final mesh's UVs and materials, sit exactly inside the volume, and have one collision box each (the engine generates it).

## 0.14 Damage & destruction
- **Deformation:** vertex-shader dents driven by the `Damage` parameter and the UV1 mask; no separate damaged mesh for most parts.
- **Separate damage states** only where the card says so (barricades, scrap doors, spike traps): `<asset>_Dmg1`, `_Dmg2`.
- **Destroyed:** the block is removed and replaced by debris from the shared library by size class: `SM_Debris_XS_01…08` (< 1 m), `S` (< 3 m), `M` (< 8 m), `L` (≥ 8 m). Each card lists its debris set.

## 0.15 Collision
- Convex hulls only, named `UCX_<asset>_NN`, at most the card's hull count.
- **Walkable surfaces** (floors, stairs, catwalks, ramps) must match the visible surface within 2 cm. Stairs use a ramp hull.
- Moving parts get their own hulls in the `_Parts` export (`UCX_<asset>_Part_<Name>_NN`).
- No collision on cables, antennas thinner than 5 cm, or decorative greebles.

## 0.16 Sockets & mount markers
- Sockets are **empties** with **+X pointing out** of the face (the direction of flow, exhaust or interaction).
- The scaffold places every socket the card requires at the face center (spread along the face when there are several). Move them to the real feature (nozzle exit, port center, seat hip point); **don't rename them.**
- Socket types:

| Type | Meaning |
|---|---|
| `conveyor_large` / `conveyor_small` | Conveyor port center (standard apertures, §0.7) |
| `air`, `water`, `fuel` | Utility network ports |
| `interact` | Player use point (terminal, lever, button) |
| `seat`, `bed` | Character attach at hip (seat) or spine base (bed); +X = facing direction |
| `work` | Survivor work slot, on the floor, facing the part |
| `light` | Light position |
| `lcd` | Screen surface center (screen quad UV 0–1) |
| `vfx_exhaust`, `vfx_smoke`, `vfx_sparks`, `vfx_fire` | VFX origins |
| `muzzle` | Projectile spawn and flash |
| `audio` | Looping sound emitter |
| `attach_top` | Sub-grid head attach (rotors, hinges, pistons, wheels) |
| `wheel` | Wheel axle |
| `projector` | Hologram origin |
| `camera` | Camera origin |
| `item_in` / `item_out` | Item intake and output |
| `door` | Door leaf slide or pivot origin |

- **Mount markers** (`MOUNT_<Face>`) record which faces attach to neighbours and whether each is airtight. They're data, not geometry.

## 0.17 Moving parts & rigs
- Every moving element is a **separate mesh** `<asset>_Part_<Name>` parented to a **`PART_<Name>` pivot empty** placed exactly on its hinge or rotation axis. The engine animates the pivots procedurally.
- Allowed motions: rotate about one axis (doors, fans, rotors, turret yaw/pitch), translate along one axis (sliding doors, pistons), and simple two-axis gimbals.
- **Turret rig standard:** `PART_Base → PART_Yaw (Z) → PART_Pitch (Y) → PART_Barrel (spin or recoil along −X)`.
- **Skeletal meshes (`SK_`)** only where rigid pivots can't do it: parachute canopies, first-person weapons, suits, drones.
- Moving parts must stay inside the volume in every pose, unless `allow_overhang` is set.

## 0.18 Performance rules
- Aim for a single material on S parts; trim-sheet discipline keeps hull draw calls low.
- No real-time lights baked into parts; lights come from `light` sockets and the engine's light budget.
- Instanced parts may not use vertex animation (fans are the exception: they use a rotating `PART_` pivot).
- Emissive surfaces don't cast light by default; set `light` sockets where real light matters.

## 0.19 Definition of done (every asset)
- [ ] Scaffolded with the toolkit; names untouched
- [ ] LOD0–LOD3 within budget; LOD3 is silhouette-only
- [ ] Fits the grid volume (or `allow_overhang` is justified on the card)
- [ ] Mount faces flush; airtight faces closed; conveyor apertures standard
- [ ] UV0 and UV1 present; texel density within ±10%
- [ ] Materials named `MI_*`; slot count within the class limit; blockout material removed
- [ ] Build stages BS1…BSn modeled and within their budgets
- [ ] Collision hulls within the limit; walkable surfaces accurate
- [ ] All sockets present and moved onto their features; `PART_` pivots on their axes
- [ ] `exodus_parts.py validate` shows **PASS** (or WARN with a reason in the tracker)
- [ ] Exported with `exodus_parts.py export`; imported and checked in engine; tracker status set to *Done*
