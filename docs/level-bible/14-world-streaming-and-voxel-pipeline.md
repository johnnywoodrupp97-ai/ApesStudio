# 14 — World Streaming & Voxel Pipeline

> How one seamless universe fits in memory: the world hierarchy, World Partition cells for regions, level instances for interiors, data layers for story state, and the voxel planet pipeline from cube-face maps to minable terrain. Engine architecture is in game bible [13](../game-bible/13-technical-architecture.md); the travel thresholds that trigger streaming are in [11](11-space-travel-and-planet-transitions.md).

## 14.1 World hierarchy

```
Universe (galaxy seed)
 └─ Star system (system seed; ~60 in the Drift)            Space Region cells (2,048 m)
     ├─ Planet (planet seed; voxel cube-sphere, 20–120 km)   voxel clipmap + planet impostor
     │   ├─ Hand-authored region (≤ 16 km, stamped)        Open / Planet Region cells (256 / 512 m)
     │   │   └─ District (level instance)
     │   │       └─ Mission space (level instance)          Interior, Hub, Set Piece, Dungeon
     │   └─ Procedural POIs (template instances)            Procedural Template
     ├─ Stations, wrecks, asteroids                         level instances in Space Region cells
     └─ Space arenas (scripted)                             Space Arena
```

Everything uses **large-world coordinates** (double precision) with a floating origin that re-centers on the player's ship or body every 10 km, so a 120 km planet and a system 4,000 km across both stay precise.

## 14.2 Streaming by level type

| Type | Streams as | Cell / unit | Loading range | Notes |
|---|---|---|---|---|
| Open Region | World Partition grid | 256 m | 768 m | Kestrel Valley = 32 × 32 cells; HLODs for everything beyond range |
| Planet Region | World Partition grid | 512 m | 1,536 m | Lunar Near Side, Veyra-4 Jungle Region, Earth Returns |
| Space Region | World Partition grid | 2,048 m | 8,192 m | Low Earth orbit, system space around stations |
| District | Level instance | — | Loads with its region cells | Placed at its map position (e.g. Kestrel Township at −0.9, +0.1 km) |
| Interior / Hub / Dungeon / Set Piece | Level instance | — | Pre-loads at its entrance (doors and lifts hide the rest) | Never behind a loading screen; airlocks and elevators give 2–4 s of cover |
| Space Arena | Level instance | — | Loads on approach (pulse dropout) | — |
| Procedural Template | Template instance | — | With the planet chunk that holds it | Stamped by seed; only player changes are saved |
| Planet | Voxel clipmap | 32 m chunks, 8 rings | Streaming starts at 6 planet radii from the center (360 km for Earth) | An impostor sphere before that |

**HLODs.** Every open region builds HLODs for its cells: district silhouettes and landmarks stay visible across the whole region (the Pad 39-K tower and the Hollis Dam wall read from anywhere in Kestrel Valley).

## 14.3 Data layers (world state)

The same level serves different story states through data layers instead of copies.

| Layer family | Examples | Switches when |
|---|---|---|
| **Story state** | `pre_outbreak` (Cold Open, Mission Control 2068), `night_zero`, `act1`, `earth_returns` | Mission beats |
| **Choices** | `tug_survived`, `veyra_healed`, `ada_state` (defected, loyal or dead), `crane_tracking` | Choices recorded in the save |
| **Bloom level** | `bloom_1`…`bloom_5` per district | Bloom spread and Bloom Hearts destroyed |
| **Time of day / weather** | Night-only encounters, spore-storm dressing | Day cycle, weather volumes |
| **Player presence** | Survivor camps that join the player's colony, cleared POIs | Player actions |

## 14.4 The voxel planet pipeline

```
 planet seed + planet card (diameter, gravity, biomes, ore layers, anchors)
      │
      ▼
 6 cube-face maps per planet  (16-bit PNG; 2,048² at 20 km · 4,096² at 40 km · 8,192² at 80–120 km)
   Height · Biome · Ore · Bloom
      │  noise layers + approximate erosion (procedural planets)
      │  hand-painted / generated faces (story planets: Earth's continents and Bloom glyph, the Moon's maria)
      ▼
 region stamps  (flat-authored regions blended onto the faces at their lat/lon; §0.6 of chapter 00)
      │
      ▼
 voxel generation on demand  (1 m voxels, 32 m chunks, density + material per voxel)
      │  ore veins from the Ore map and the planet's depth layers; bedrock below the crust (3.5% of R)
      ▼
 clipmap LOD rings  → meshing (dual contouring / transvoxel) → collision and navmesh tiles
      │
      ▼
 player edits saved as compressed per-chunk deltas (mining, building foundations, craters)
```

**Clipmap rings** (8 rings, each doubling voxel size and radius):

| Ring | Voxel size | Radius | Use |
|---|---|---|---|
| 0 | 1 m | 256 m | Full detail: mining, collision, navmesh |
| 1 | 2 m | 512 m | Vehicle range |
| 2 | 4 m | 1 km | — |
| 3 | 8 m | 2 km | **Full-detail radius** that must stream within the 8 s atmosphere entry ([11](11-space-travel-and-planet-transitions.md)) |
| 4 | 16 m | 4 km | Low flight |
| 5 | 32 m | 8 km | — |
| 6 | 64 m | 16 km | High flight |
| 7 | 128 m | 32 km | Beyond this: a planet mesh built from the cube-face maps, then the impostor sphere past 6 R |

**Saves** store only deltas: modified voxel chunks (run-length compressed), player grids and colony state. An untouched planet costs nothing to save.

## 14.5 Memory and performance budgets
Per-type memory, draw-call and shadow-light budgets are in [01](01-level-overview.md). On top of those:

| Item | Budget |
|---|---|
| Voxel planet (all rings + planet mesh) | 900 MB |
| Open region: resident cells | 3 × 3 around the player at full detail, HLOD beyond |
| Level-instance pre-load | ≤ 250 MB per instance; ≤ 2 instances pre-loading at once |
| Streaming hitch | 0 ms target, ≤ 16 ms worst case (one frame at 60 fps) |
| Navmesh rebuild (voxel edits, player building) | 4 tiles of 32 m per frame |

## 14.6 From Blender to the engine

| Blender output | Engine import |
|---|---|
| `export/levels/<group>/<asset>.fbx` (all `BLK_`/`TER_`/`KIT_` meshes) | Static meshes for the blockout; replaced by kit art as the level is dressed |
| `<asset>.markers.json` | The level importer creates actors from marker prefixes (§0.4 of chapter 00): spawns, triggers, volumes, splines, cameras, doors, lights, POIs, landmarks |
| Root metadata (`level_id`, type, bounds, budgets, required markers) | World settings and validation in the engine (the same checks run in CI) |
| Planet files: `TER_Face_*`, transition shells, anchors, `<asset>_maps/*.png` | Planet definition: radius, thresholds, anchor transforms; the cube-face map templates are the starting point for the final Height/Biome/Ore/Bloom maps |
| Kit libraries: one FBX per `SM_KIT_*` piece | Kit meshes for level dressing (pivot rules in [10](10-modular-kits.md)) |

A level is re-exported whenever its blockout changes. The engine keeps actor GUIDs stable by marker name, so renaming a marker is a breaking change: add a new marker and retire the old one.
