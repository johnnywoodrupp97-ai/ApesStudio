# 08 — Exploration & Procedural Universe

> The *No Man's Sky* pillar: seamless planets, a procedural galaxy, and the joy of seeing somewhere first — layered with authored story anchors.

## 8.1 Universe structure

```
Sol System (hand-crafted)
 ├─ Earth (hand-crafted Nevada region + procedural wider Earth for "Earth Returns")
 ├─ Low Earth Orbit (Haven-9, debris fields, dead satellites)
 ├─ Moon (Tycho Outpost + procedural lunar surface)
 └─ Styx Wreck (hand-crafted)
        │  Sower Jump Lane
        ▼
The Drift (~60 procedural systems at launch, seeded per save)
 ├─ Anchor: Tortuga Drift system (hub)
 ├─ Anchor: Veyra system (Key of Roots)
 ├─ Anchor: Hollowmere system (Key of Echoes)
 ├─ Anchor: Meridian system (Key of Iron)
 ├─ Anchor: Convergence Gate (Act III climax)
 └─ ~55 procedural systems (resources, derelicts, events, side content)
        │
        ▼
Deep Drift (post-game / expansions: unlimited procedural systems)
```

- **Anchor systems** contain hand-built set pieces placed into procedurally generated stars and planets, guaranteeing story quality while keeping each save's sky unique.
- **Seed per save:** every campaign has a unique Drift layout; anchors are placed at controlled "jump distances" to keep pacing consistent.

## 8.2 Travel methods

| Method | Range | Unlock | Notes |
|---|---|---|---|
| On foot / jetpack | Local | Start | Jetpack limited in gravity |
| Rover | Planet surface | Act I | Wheeled physics; carries survivors and cargo |
| Atmospheric flight | Planet | Act II | Atmospheric thrusters, wings |
| Orbital flight | In-system local | Act II | Seamless planet ↔ space transitions |
| **Pulse Drive** (cruise) | In-system (planet to planet) | Act II | Minutes, interruptible by events |
| **Sower Jump** | System to system | Act III | Jump Core + fuel (Resonance Crystals) + cooldown |

## 8.3 Planet generation

### Parameters (generated per planet)
- **Type:** Rocky, Ocean, Ice, Desert, Jungle, Volcanic, Toxic, Barren (airless), Gas giant (orbit only — moons & stations), **Bloomed** (overrun by Verdance)
- **Size:** 8–60 km radius (scaled for gameplay; target 30 km average)
- **Gravity:** 0.1–1.8 g
- **Atmosphere:** None / Thin / Breathable / Toxic / Spore-laden; pressure & composition
- **Temperature band:** by star type, orbit distance and day/night
- **Hazards:** storms (dust, ice, acid, spore), radiation, quakes, meteor showers
- **Bloom Coverage:** 0–100% (how much the Verdance has transformed the planet) — drives enemy density and resource types
- **Biomes:** 2–5 per planet from the type's pool

### Terrain
- **Voxel-based**, fully diggable/minable, with heightmap base + noise layers + erosion approximation.
- Hand-authored **terrain stamps** (canyons, craters, mesas, Sower ruins) inserted by rules.
- Cave networks (for ores, hideouts and Hollow nests).

### Flora & fauna
- **Procedural creatures** built from part kits (body plan, limbs, heads, patterning, behavior template: grazer, predator, flyer, burrower, swarm).
- Every planet with life has a **Bloom variant** of its fauna — mutated Hollow versions — ratio set by Bloom Coverage.
- **Discovery log:** scanning species, plants, minerals and ruins grants research points and lets the player name them (shared naming in future co-op).

## 8.4 Points of interest (POI)

| POI | Frequency | Content |
|---|---|---|
| **Derelict Ship** | Common | Procedural interior, loot, logs, occasional Drifters |
| **Crash Site** | Common | Salvage, sometimes survivors |
| **Survivor Camp** | Uncommon | Recruitable survivors, trade, sometimes a quest |
| **Bloom Heart** | Uncommon | Dense Hollow nest; destroy to reduce local Bloom coverage; big rewards |
| **Sower Ruin** | Uncommon | Glyphs, puzzles, precursor components |
| **Directorate Outpost** | Uncommon | Hostile, high-tech loot, intel |
| **Choir Shrine** | Rare | Dialogue, Choir reputation, strange rewards |
| **Free Hauler Waystation** | Rare | Trade, contracts, repair |
| **Anomaly** | Rare | Unique events (a lone Sower construct, a time-dilated signal, a derelict human ship from before 2071…) |

## 8.5 Scanning & navigation
- **Handheld Scanner:** identifies objects, creatures, ores, infection in people; pings nearby POIs.
- **Ship Scanner Array:** long-range planetary scans (resource map, Bloom coverage, life signs).
- **Signal Decoder:** triangulates distress calls and Sower beacons — the main method to find POIs.
- **Galaxy Map:** shows jump lanes, discovered systems, faction territory, Bloom spread, and mission markers.

## 8.6 Outposts
- The player can build **planetary outposts** (static grids) for mining, farming unique crops, or research.
- Outposts can be **staffed** by survivors (who then need habitation there) or **automated** with drones.
- Outposts are threatened by local Hollow activity scaled by Bloom Coverage; defended with turrets or kept low-profile (noise/light attract Hollows).
- **Supply lanes:** automated cargo shuttles run between outposts and the main base/ship (T3 tech).

## 8.7 Living universe rules
- **Bloom spread simulation:** each system has a Bloom value that slowly rises unless Bloom Hearts are destroyed or Garden Engines shut down. Systems visually and mechanically change.
- **Faction territory:** Directorate, Choir and Free Haulers control systems; territory shifts based on story and player actions (lightweight simulation, updated on jumps).
- **Ambient traffic:** faction ships travel lanes; can be traded with, helped or attacked.

## 8.8 Hand-crafted anchor planets (campaign)

| Planet | Type | Signature features |
|---|---|---|
| **Earth (Nevada region)** | Temperate desert | 4 km² hand-built Kestrel Complex & Township; day/night horde cycle |
| **Moon — Tycho** | Barren, 0.16 g | Mining outpost interior, dust storms, Earthrise vista |
| **Veyra-4** | Jungle/ocean, 0.9 g | Purple seas, Tessari herds, the Garden Engine — a 2 km Sower spire |
| **Hollowmere** | Ice, 0.7 g, −80 °C | Blizzards, ice caves, Cathedral of the Hum over a Sower archive |
| **Meridian (gas giant) & Ark Meridian** | Station in orbit | Directorate flagship-station interior, zero-G sections |
| **Tortuga Drift** | Hollow asteroid city | Markets, docks, hub interior |
| **Seedship *Anthesis*** | Living megastructure | Four internal "memory garden" biomes |
