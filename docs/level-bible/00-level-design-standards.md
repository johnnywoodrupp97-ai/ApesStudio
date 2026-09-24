# 00 — Level Design & Blender Standards

> The rules every level in EXODUS PROTOCOL follows, from a 20 m dining room to a 120 km planet. Read this first. Metrics are in [02](02-metrics-and-gym.md), modular kits in [10](10-modular-kits.md), the Blender toolkit in [15](15-blender-level-toolkit.md).

## 0.1 Level design pillars

| Pillar | What it means for a level | Test |
|---|---|---|
| **Open, not linear** | Every region can be entered from more than one side; missions happen *in* the open world, not in sealed corridors | Can the player arrive by rover, on foot, by air and (later) by ship? |
| **Danger gates, walls don't** | Districts are gated by threat (Bloom level, hordes, radiation, vacuum), never by invisible walls. Story interiors may lock, but only with a visible reason (a sealed door, a collapsed tunnel) | Is every closed route explained in the world? |
| **Build anywhere it makes sense** | Player bases are a first-class part of every open space: flat ground, resources and a reason to stay. Story anchors are protected by a 150 m no-build radius (`VOL_NoBuild_*`) | Is there a good base site within 1 km of every district? |
| **Readable from a distance** | A landmark pulls the player toward each district, and a silhouette identifies each point of interest. On small planets, landmarks must clear the horizon (§0.6) | Can a new player name the district by its skyline? |
| **Every 90 seconds, something** | Along any route, something to notice at least every 90 s of travel: a landmark, signal, wreck, creature, resource or view | Ride the main roads at rover speed: does the timer ever run out? |
| **Seamless** | No loading screens from the valley to the stars: interiors are level instances, regions stream in cells, planets are voxel worlds, travel transitions hide streaming ([11](11-space-travel-and-planet-transitions.md)) | Does any doorway or dive ever hitch? |

## 0.2 Units, axes and coordinates

| Rule | Value |
|---|---|
| Units | Meters. Blender scenes: Metric, unit scale 1.0 (the toolkit sets and checks this) |
| Up axis | +Z |
| Level frame | Origin at the level center, on the ground plane. +X east, +Y north on top-down maps |
| Space positions | A space's `pos` is the center of its **floor**; its size is width (X) × depth (Y) × height (Z) |
| Open-region placement | District and mission positions are given in **kilometers** in the region frame (Kestrel Valley: ±4 km) |
| Planet placement | Anchors are **latitude / longitude** on the planet; regions are authored flat in a local east-north-up frame at their anchor and stamped onto the planet (§0.6) |
| Engine export | FBX with −Z forward, Y up, *Apply Unit Scale*; the `.markers.json` sidecar keeps Blender coordinates (meters, Z up) |

## 0.3 Level IDs, names and files

| Item | Rule | Example |
|---|---|---|
| Level ID | `<GROUP>-<NNN>`, numbered in catalog order | `KES-004` |
| Groups | `PLN` planets · `KVL` Kestrel Valley · `KES` Kestrel Complex & Township · `ORB` orbit and the Moon · `DRF` the Drift · `SEE` the Seedship · `PRC` procedural templates | — |
| Asset name | `LVL_<GROUP>_<NNN>_<PascalName>` | `LVL_KES_004_TerminalB` |
| Blender file | `assets/levels/<group-folder>/<asset>.blend` | `assets/levels/kestrel-complex-and-township/LVL_KES_004_TerminalB.blend` |
| Engine export | `export/levels/<group-folder>/<asset>.fbx` + `<asset>.markers.json` | — |
| Kits | `KIT-<CODE>` → `assets/levels/kits/KIT_<CODE>_<Name>.blend`, pieces `SM_KIT_<CODE>_<Piece>` | `SM_KIT_KES_Wall25` |
| Metrics Gym | `assets/levels/gym/LVL_MetricsGym.blend` | — |

New levels get the next number in their group. Add them at the end of the group's catalog module so existing IDs stay stable.

## 0.4 Object naming: marker prefixes

Every object in a level file starts with one of these prefixes; the toolkit warns about anything else and the engine importer maps each prefix to an actor type.

| Prefix | Use | Engine actor |
|---|---|---|
| `LVL_` | Level root empty (metadata), planet anchors (`LVL_ANCHOR_<ID>`) | Level/world settings |
| `BLK_` | Blockout geometry (grey-box floors, walls, set dressing stand-ins) | Static mesh (blockout) |
| `TER_` | Terrain: heightfield grids, planet cube faces | Landscape / voxel source |
| `PS_` | Player start | Player start |
| `SP_` | Enemy or NPC spawn point | Spawner (template from the name) |
| `HS_` | Horde spawn zone (volume) | Horde director spawn volume |
| `TRG_` | Mission trigger volume | Trigger → mission script |
| `VOL_` | Other volumes: rooms (`VOL_Room_*`), audio, post-process, no-build, Bloom level, pressure, weather, landing zones, docking bays, no-fly, kill | Volume by sub-name |
| `POI_` | Point of interest (open-world discovery) | Map marker + discovery |
| `LM_` | Landmark | Navigation landmark (scanner, map) |
| `CAM_` | Cinematic or set-piece camera | Cine camera |
| `SPL_` | Spline: roads, paths, rails, patrol routes, approach paths | Spline actor |
| `DOOR_` | Connection between spaces (door, airlock, lift, gap) | Door / connector |
| `COV_` | Cover marker (low / high) | AI cover point |
| `LT_` | Key light reference | Light (from the name) |
| `NAV_` | Navmesh bounds or modifier volume | Nav bounds / modifier |
| `KIT_` | Modular kit piece instance | Instanced static mesh |
| `REF_` | Reference only (never exported): bounds, grids, curvature, scale human, labels | — |

Names after the prefix are PascalCase and carry the mission when they belong to one: `TRG_M0_03_Skywalk`, `HS_M1_06_West`, `CAM_C05_Glyph`.

## 0.5 File structure (Blender)

A level file produced by `exodus_levels.py scaffold` has one root empty and one collection tree:

```
LVL_KES_004_TerminalB            ← root empty: id, type, size, budget, required markers, bounds
LVL_KES_004_TerminalB (collection)
 ├─ _Blockout     BLK_* floors and walls
 ├─ _Terrain      TER_* heightfields (open regions, districts)
 ├─ _Markers      PS_, SP_, POI_, LM_, DOOR_, COV_ empties
 ├─ _Volumes      VOL_Room_*, TRG_*, HS_*, VOL_* volumes
 ├─ _Splines      SPL_* curves
 ├─ _Cameras      CAM_* cameras
 └─ _Reference    REF_Bounds, REF_StreamingGrid, REF_Curvature, REF_Human_1p8m, labels
EXODUS_NOTES (text)              ← summary, goals, encounters, budgets, required markers
```

Planet files have `_Terrain` (six `TER_Face_*` cube faces), `_Shells` (crust, gravity, atmosphere, cloud deck, pulse dropout, streaming and capital-parking spheres), `_Markers` (anchors) and `_Cameras`, plus 24 cube-face map templates in `<asset>_maps/`.

## 0.6 Planets, regions and curvature
Every planet is a voxel planet 20–120 km in diameter (the full standard is in [03](03-planets-and-voxel-scale.md)). The rules that matter when building levels:

1. **Regions are authored flat.** Open regions (Kestrel Valley, the Lunar Near Side, the Veyra-4 Jungle Region) are built in a flat local frame at their anchor. They are at most 16 km across and no more than a quarter of the planet's diameter.
2. **The stamp absorbs the curvature.** The region is stamped onto the planet's cube-face heightmap. Inside the region the ground is flat, so a landmark inside Kestrel Valley is visible across the whole valley. At the region's edge the stamp blends back into the planet's curvature: 133 m of drop over 8 km on Earth, 400 m on the Moon. **Every region must be ringed by terrain** (mountains, crater rims, ridges or jungle canopy) that hides the blend.
3. **Outside regions, curvature is real.** On procedural terrain, landmarks must clear the horizon: at eye level the horizon is 465 m away on Earth and 268 m on the Moon. A primary landmark must be seen from 2 km (20 m tall on Earth, 75 m on the Moon, 164 m on a 20 km world); put landmarks on high ground.
4. **Oceans only on planets of 40 km or more.** On smaller worlds a sea would take over the surface.
5. **Leave space for ships.** Every anchor gets a `VOL_LandingZone_*` (a pad or 40 m of flat ground) within 300 m of its entrance ([11](11-space-travel-and-planet-transitions.md)).

## 0.7 Blockout workflow

| Stage | Output | Gate |
|---|---|---|
| **1. Paper** | One-page brief: goals, beats, spaces, connections, encounters, landmarks (the level card in this bible) | Design review |
| **2. Catalog** | The level added to `tools/levels/catalog/`; `python3 tools/levels/build.py` passes | Build passes (bounds, markers, budgets) |
| **3. Scaffold** | `exodus_levels.py scaffold --level <ID>` creates the starter `.blend` with every space, connection and required marker | `validate` passes |
| **4. Blockout** | `BLK_` geometry from kit pieces (0.5 m snap), cover, sightlines, heights to the metrics | Playable in the engine; [02](02-metrics-and-gym.md) metrics met |
| **5. Playtest** | Three internal passes: navigation (can a new player find the goal?), combat (encounter timing), open world (arrive from every side) | Playtest notes resolved |
| **6. Art pass** | Kit art replaces `BLK_`; lighting ([13](13-lighting-atmosphere-and-audio.md)); audio volumes | Budgets ([01](01-level-overview.md)) within limits |
| **7. Final** | Streaming, HLOD and data layers ([14](14-world-streaming-and-voxel-pipeline.md)); performance capture | Definition of done (§0.9) |

## 0.8 Composition rules

- **Landmark first.** Block out the landmark and the main sightline before anything else. Every district has one primary landmark (seen from 2 km) and at least two secondary ones (seen from 500 m).
- **Three routes.** Every significant goal has an obvious route, a hidden route (vents, rooftops, sewers) and a built route (the player's own ramp, bridge or breach). Blockout tests all three.
- **Critical path gets the light.** Lead the eye with light, color and motion. Emergency lights, fires and the Bloom's glow do double duty as wayfinding.
- **Combat spaces at the right sizes.** Small 15–25 m, medium 25–50 m, large 50–120 m ([02](02-metrics-and-gym.md)). Hollows are nearly blind, so stealth spaces are about **noise**: loose debris, metal floors, alarms.
- **Horde spaces have approach lanes.** Every defensible site shows where a horde will come from: two or three lanes, at least 60 m long, starting out of sight ([12](12-encounters-hordes-and-ai-navigation.md)).
- **Scale for the player's builds.** Openings, bays and courtyards come in multiples of 2.5 m, so large-grid blocks fit flush; hangars take the parts bible's 30 × 15 m hangar doors.
- **Vertical first on small worlds.** At 0.16 g the player jumps 6× as far, so Moon spaces use height and craters, not wide flat floors.

## 0.9 Definition of done (a level)

- [ ] Catalog entry complete: goals, spaces, connections, encounters, landmarks, mood, audio, markers, kits, notes.
- [ ] `exodus_levels.py validate` passes: required markers present, geometry inside bounds, blockout within budget (per level, or per streaming cell for regions), prefixes approved.
- [ ] Every space meets the [02](02-metrics-and-gym.md) metrics (the Metrics Gym is the reference).
- [ ] Three routes to every key goal; every closed route explained in the world.
- [ ] Landmarks visible from their required distance on their planet (curvature table in [03](03-planets-and-voxel-scale.md)).
- [ ] Landing zone within 300 m of every anchor entrance (planets), or a docking bay (stations).
- [ ] Encounter spawns out of sight and ≥ 60 m away; horde lanes readable ([12](12-encounters-hordes-and-ai-navigation.md)).
- [ ] Lighting within its shadow-light budget; key lights marked `LT_*` ([13](13-lighting-atmosphere-and-audio.md)).
- [ ] Streaming: cells, level instances and data layers set up; no hitch on entry ([14](14-world-streaming-and-voxel-pipeline.md)).
- [ ] Performance within the [01](01-level-overview.md) budgets on target hardware.
