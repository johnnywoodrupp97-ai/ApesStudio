# 12 — Encounters, Hordes & AI Navigation

> How levels host fights, sieges, stealth and creatures: the spaces each enemy needs, horde spawn and approach rules, and the navigation agents every level must support. Enemy stats are in game bible [09](../game-bible/09-combat-and-enemies.md) and [22](../game-bible/22-balance-and-tuning.md); the metrics are in [02](02-metrics-and-gym.md).

## 12.1 Encounter building blocks

| Marker | What it is | Rules |
|---|---|---|
| `SP_<Enemy>_<NN>` | A spawn point for one enemy or a small group | Out of the player's sight when it fires; ≥ 60 m from the player for anything that isn't a scripted reveal |
| `HS_<Mission>_<Side>` | A horde spawn **zone** (20 × 20 m volume) | At the far end of an approach lane (§12.3); several zones per base site |
| `TRG_<Mission>_<Beat>` | A trigger volume that starts a beat | Sized to the whole doorway or path, so it can't be skipped by jumping |
| `COV_<Low|High>_<NN>` | A cover point | Low 1.0 m (crouch), high 1.8 m (standing); both sides reachable |
| `NAV_*` | Navmesh bounds and modifiers | Every walkable level has one bounds volume; modifiers mark crawl ducts, ledges and no-go areas |
| `SPL_Patrol_*` | A patrol route | Directorate and drone patrols only; Hollows roam by noise, not by spline |

Every encounter in a mission level is listed on the level's card (chapters 04–09). Open-world encounters come from the **encounter director**, which spawns from `SP_` and `HS_` markers based on the time of day, Bloom level, Attraction and story state.

## 12.2 Enemy space needs

Hollows are nearly blind (15 m sight) and hunt by **noise** (5–40 m). The Directorate sees 60 m. Level geometry is the difficulty dial.

| Enemy | Space it needs | Space that counters it | Level rules |
|---|---|---|---|
| **Shambler** | Anywhere; doors it can bang on | Doors, fences, narrow corridors | Put knocking Shamblers behind doors on the critical path: audio foreshadowing |
| **Runner** (packs of 3–6) | Long open ground to sprint | High ground, fences, traps, narrow gaps | Open ground at dusk is Runner country (Main Street, Jackrabbit Flats); give a climbable escape within 30 m |
| **Crawler** | Vents, underfloors, under vehicles | Light, the scanner | Every crawl duct (1.2 m square) that Crawlers use has a visible entry; never an ambush without a tell (scrape audio, loose grate) |
| **Screamer** | Line of sight to the player | Suppressed weapons, cover | Clear 20 m sightline to the Screamer so its tell is readable; never in the dark |
| **Bloater** | Tight spaces (burst radius 4 m) | Range | Keep corridors wider than 2.5 m where Bloaters patrol |
| **Brute** (2.6 m) | Large doorways, weak walls | Reinforced walls, fire | Brute routes need 2.5 × 3.0 m openings; Brutes target load-bearing blocks, so base sites show their weak points |
| **Burrower** | Soft terrain, mine shafts | Rock floors, armor foundations | Burrowers surface through voxel terrain; base sites on bedrock or armor are immune |
| **Sower Warden** (3.2 m) | Tall halls (≥ 4 m) | Elevation, pillars | Seedship halls are sized for Wardens; the player has pillar cover every 15 m |
| **Directorate troopers** | Lanes with cover | Flanks, smoke, verticality | Medium arenas (25–50 m); cover every 8–10 m; two flanking routes |
| **Directorate drones** | Open sky, 40 m spotlight cones | Roofs, dense canopy, EMP | Crash-site and camp levels provide overhead cover within 20 m of any open patch |

## 12.3 Hordes and sieges

Nightly hordes, Green Moon waves and scripted sieges (the Long Night, M1.06) all use the same rules.

**Horde size** comes from the base's **Attraction** (game bible 22 §22.5): 5–15 Shamblers at 0–100, up to 80–150 with Brutes at 600–1,000, scaled by the region's Bloom level (×0.5 to ×2.0). Green Moon waves (every 3rd night) are 40–250 with up to 5 Brutes.

| Rule | Value |
|---|---|
| Spawn distance | ≥ 60 m and out of sight; hordes never pop in on screen |
| Approach lanes per defensible site | 2–3, each ≥ 60 m long, readable from the site (a road, a wash, a gap in a fence) |
| Lane width | ≥ 8 m, so a horde reads as a mass, not a queue |
| Choke points | Every lane has one natural choke 3–5 m wide within 40 m of the site, which is where the player builds |
| Build space | ≥ 50 × 50 m of flat ground around a site's core for walls and turrets (`VOL_BaseSite_*`) |
| Retreat | A fallback position (roof, bunker, second wall ring) inside every siege site |
| Crowd budget | 60 full-AI Hollows plus up to 2,000 impostors on PC (40 / 1,000 on console); a lane can hold ~300 agents at the simplified-animation tier |

**Scripted sieges** (Pad 39-K, M1.06) mark each lane with `HS_<Mission>_<Side>` and the objective the horde targets (`HS_M1_06_FuelLine`). Waves alternate lanes so the player moves between defenses.

## 12.4 Stealth spaces

- **Noise surfaces:** metal floors and grates (loud), carpet and sand (quiet), glass and debris fields (very loud). Mark them with `VOL_Surface_<Type>` so footstep noise matches.
- **Hollows** hear gunfire at 40 m, sprinting at 15 m and walking at 5 m; crouch-walking is silent. Stealth routes need continuous quiet surfaces.
- **Directorate** spaces use sightlines. Give every patrolled area at least one route with broken line of sight (cover every 8 m, shadows under 20% light).
- **Social stealth** (the Cathedral of the Hum, Ark Meridian): crowds of pilgrims or crew the player can walk among; weapons drawn break it.

## 12.5 Navigation agents
Every walkable level supports the navigation agents below. The Metrics Gym has a lane with each agent's capsule at scale.

| Agent | Radius | Height | Max step | Max slope | Used by |
|---|---|---|---|---|---|
| **Humanoid** | 0.35 m | 1.8 m | 0.45 m | 45° | Player, survivors, Shamblers, Runners, units |
| **Suited** | 0.4 m | 1.95 m | 0.45 m | 45° | EVA suits, Drifters on gravity decks |
| **Crawler** | 0.4 m | 0.6 m | 0.3 m | 40° | Crawlers; also uses large-grid crawl ducts |
| **Large** | 0.6 m | 2.1 m | 0.5 m | 40° | Enforcers |
| **Brute** | 0.9 m | 2.6 m | 0.6 m | 35° | Brutes, Burrowers above ground |
| **Giant** | 1.2 m | 3.2 m | 0.8 m | 35° | Sower Wardens, Seraph exo-frame |
| **Tessari** | 2.0 m | 4.9 m | 0.8 m | 30° | Tessari adults; large grazer kits |
| **Small animal** | 0.3 m | 0.6 m | 0.25 m | 50° | Dogs, coyotes, jackrabbits |

**Navmesh rules**
- **Nav links** for every traversal the player can make: mantles (≤ 2.0 m), jump gaps (≤ 3.0 m at 1 g), ladders, drops (≤ 4 m safe). AI uses the same links, so a Runner follows you over a fence.
- **Player-built structures** rebuild the navmesh in 32 m tiles when blocks are placed or destroyed (budget: 4 tiles per frame). Doors are nav links that Hollows try to break.
- **Voxel terrain** rebuilds its navmesh tiles when mined or deformed. A mined tunnel becomes walkable for Burrowers and Crawlers first (smaller agents).
- **Zero-G** spaces use a 3D volume graph instead of a navmesh; EVA routes have handholds every ≤ 1.5 m and drones path on the same graph.
- **Flying enemies** (drones, flyers) use sparse 3D volumes above walkable areas, with height limits per level (`NAV_FlyCeiling_*`).
- **Wall crawlers** (Bloom tendrils, some Seedship organisms) use surface navigation on meshes tagged `NAV_Climbable`.

## 12.6 Encounter pacing in missions
Each mission level alternates tension and release. The beat flows for the flagship missions are in game bible [18](../game-bible/18-mission-design-documents.md); the rule for every level:

| Beat | Share of level time | Content |
|---|---|---|
| Arrival and read | 10–15% | See the landmark, the objective and the threat; no combat for the first 30 s |
| Build-up | 25–30% | Small encounters (2–6 enemies), resources, a stealth option |
| Peak | 20–30% | The level's set piece or largest fight |
| Release | 10–15% | Safe room, story, loot, a view |
| Exit | 10–20% | A short final push; a second route home |

**Difficulty scaling** changes counts and timing, never the geometry: the same level must be completable at every difficulty with the same routes.

## 12.7 Blender spec
- Spawn and cover markers are empties (`SP_` spheres, `COV_` axes); horde zones and triggers are wireframe volumes. `exodus_levels.py validate` fails a level whose card lists a marker the file doesn't have.
- Nav bounds (`NAV_Bounds_*`) wrap every walkable space; blockout floors (`BLK_*_Floor`) are the navmesh source until art replaces them.
- The `.markers.json` sidecar carries every marker's transform and custom properties (e.g. `connection` on `DOOR_*`) for the engine's encounter importer.
