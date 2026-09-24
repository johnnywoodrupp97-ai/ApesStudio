# EXODUS PROTOCOL — Level Design Bible

> Every level, region and planet in the game, from Mission Control on the night the world ends to the Seedship at the edge of the Drift, with a **Blender spec and a built blockout for every level**. It sets the **voxel planet standard** used by every planet (20–120 km in diameter; Earth, the starter planet, is 120 km) and **No Man's Sky-style space travel and planet entry/exit**. Companion to the [Game Bible](../game-bible/README.md) (world, story and missions: chapters 02, 03, 08, 18, 19), the [Parts Bible](../parts-bible/README.md) (the blocks players build with) and the [Character Bible](../character-bible/README.md) (who appears where).

<!-- STATS:START -->
| | Count |
|---|---|
| Planets & Voxel Scale | 5 |
| Kestrel Valley — Open Region & Districts | 11 |
| Kestrel Complex & Township — Mission Spaces | 13 |
| Orbit & the Moon | 5 |
| The Drift | 7 |
| The Seedship Anthesis | 10 |
| Procedural Templates | 12 |
| **Levels total** | **63** |
| Modular kits | 13 kits · 99 pieces |
| Metrics | 39 metrics · 8 navigation agents · 11 gym lanes |
<!-- STATS:END -->

![Kestrel Valley blockout](images/kestrel-valley-map.jpg)

## How to use this bible
- **Level designers:** start with [00 — Standards](00-level-design-standards.md) and [02 — Metrics](02-metrics-and-gym.md). Each level has a card (chapters 03–09) with goals, spaces, connections, encounters, set pieces, landmarks, mood, audio, kits, required markers, budget and its Blender file. **Every level is already scaffolded** in `assets/levels/`: open the file and block out.
- **Environment artists:** the [modular kits](10-modular-kits.md) list every kit piece with size, pivot and triangle budget; `assets/levels/kits/` holds a built library for each kit.
- **Engineers:** [14 — Streaming & Voxel Pipeline](14-world-streaming-and-voxel-pipeline.md) and [11 — Space Travel](11-space-travel-and-planet-transitions.md) define the planet, streaming and transition systems; `data/levels.json` is the machine-readable registry.
- **Producers:** `data/level_tracker.csv` and `data/kit_tracker.csv` are ready-made backlogs.

## Chapters

| # | Chapter | Contents |
|---|---|---|
| 00 | [Level Design & Blender Standards](00-level-design-standards.md) | Pillars, units and axes, IDs and files, marker prefixes, file structure, planets and curvature, blockout workflow, composition rules, definition of done |
| 01 | [Level Overview](01-level-overview.md) | Every level in one list; budgets by level type; mission → level index |
| 02 | [Metrics & the Metrics Gym](02-metrics-and-gym.md) | Player, fall, architecture, combat, vehicle, ship and landmark metrics; navigation agents; the gym |
| 03 | [Planets & Voxel Scale](03-planets-and-voxel-scale.md) | The voxel planet standard (20–120 km), curvature and landmark maths, system scale; Earth, the Moon, Veyra-4, Hollowmere and the procedural Drift planet |
| 04 | [Kestrel Valley](04-kestrel-valley.md) | The 64 km² open region and its 10 districts |
| 05 | [Kestrel Complex & Township](05-kestrel-complex-and-township.md) | The 13 mission spaces of the prologue and Act I |
| 06 | [Orbit & the Moon](06-orbit-and-the-moon.md) | Low Earth orbit, Haven-9, the Lunar Near Side, Tycho, the Styx wreck |
| 07 | [The Drift](07-the-drift.md) | Tortuga, the Dust Queen, Veyra-4, the Garden Engine, the Cathedral of the Hum, Ark Meridian, the Convergence Gate |
| 08 | [The Seedship Anthesis](08-the-seedship-anthesis.md) | The approach, the Living Halls, four Memory Gardens, the Living Bridges, the Loom, the Bonsai Mind-Space, the last Sunday dinner |
| 09 | [Procedural Templates](09-procedural-templates.md) | Derelicts, crash sites, camps, Bloom Hearts, ruins, outposts, shrines, waystations, anomalies, Wonders, Earth Returns, base zones |
| 10 | [Modular Kits](10-modular-kits.md) | 13 kits, 99 pieces, with sizes, pivots and budgets |
| 11 | [Space Travel & Planet Transitions](11-space-travel-and-planet-transitions.md) | No Man's Sky-style flight, launch, atmosphere exit and entry, pulse drive, jumps, landing; per-planet thresholds; stations and docking |
| 12 | [Encounters, Hordes & AI Navigation](12-encounters-hordes-and-ai-navigation.md) | Encounter markers, enemy space needs, horde and siege rules, stealth, navigation agents and navmesh rules, pacing |
| 13 | [Lighting, Atmosphere & Audio](13-lighting-atmosphere-and-audio.md) | Time of day by planet, lighting budgets and rules, palettes, sky and weather, the Bloom's light, audio layers |
| 14 | [World Streaming & Voxel Pipeline](14-world-streaming-and-voxel-pipeline.md) | World hierarchy, streaming by level type, data layers, the voxel planet pipeline and clipmap rings, budgets, Blender → engine |
| 15 | [Blender Level Toolkit](15-blender-level-toolkit.md) | Scaffold, gym, kit, validate and export commands; what each file contains; validation rules |

## Built files
`assets/levels/` holds a validated `.blend` for every level (63, including the 5 planets with 24 cube-face map templates each), the Metrics Gym and the 13 kit libraries: 77 files, all passing `exodus_levels.py validate`. Rebuild them with `blender -b -P tools/blender/exodus_levels.py -- scaffold --all --force` (plus `gym --force` and `kit --all-kits --force`).

![Planet scale lineup](images/planet-scale.jpg)

## Source of truth
Chapters 01–11 and everything in `data/` are **generated** from `tools/levels/catalog/` by `python3 tools/levels/build.py` (which also checks the catalog: space bounds, marker prefixes, planet-region limits, kit pivots). Change the catalog, not the generated files. Chapters 00 and 12–15 and this README are hand-written; the counts table above is refreshed by the build.

## Conventions in one breath
Meters, +Z up · level origin at the center on the ground, +X east, +Y north · space positions are floor centers · open-region positions in km, planet anchors in latitude/longitude · levels named `LVL_<GROUP>_<NNN>_<Name>` · markers prefixed `PS_ SP_ HS_ TRG_ VOL_ POI_ LM_ CAM_ SPL_ DOOR_ COV_ LT_ NAV_ KIT_ BLK_ TER_ REF_` · kits on a 0.5 m grid with 2.5 m modules · planets 20–120 km, regions flat-authored and ≤ 16 km.
