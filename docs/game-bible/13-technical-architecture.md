# 13 — Technical Architecture

> Goal: a foundation that ships a 12-hour campaign **and** keeps growing. Everything content-shaped lives in data; code provides systems.

## 13.1 Engine recommendation

| Option | Pros | Cons | Verdict |
|---|---|---|---|
| **Unreal Engine 5** | Lumen/Nanite visuals, large-world coordinates (double precision), strong animation & AI tools, Mass Entity for crowds | Heavier iteration, C++ complexity, voxel terrain needs a plugin/custom | **Recommended** for a visually ambitious team |
| **Unity 6 (DOTS/ECS)** | Fast iteration, C#, ECS for hordes & block sims, big asset ecosystem | Large-world precision needs floating origin; render pipeline setup | Strong alternative for smaller teams |
| **Godot 4** | Free, lightweight, open source, great for prototyping | Less proven at this scale (voxel planets + crowds) | Use for **paper/gray-box prototypes** |

**Recommendation:** Prototype core loops quickly (any engine), then commit to **UE5** with a custom **voxel planet module** and **Mass Entity** for Hollow hordes. (If the team is C#-heavy, Unity 6 DOTS is equally viable — the architecture below is engine-agnostic.)

## 13.2 High-level architecture

```
┌─────────────────────────────── Game Layer ───────────────────────────────┐
│ Story/Quest System · Dialogue · Event Director · Colony Sim · Factions   │
├───────────────────────────── Simulation Layer ───────────────────────────┤
│ Grid/Block Sim · Power · Atmosphere/Rooms · Logistics · Structural       │
│ Infection Sim · Needs/Mood AI · Hollow Crowd AI · Ship Physics           │
├────────────────────────────── World Layer ───────────────────────────────┤
│ Universe Generator · Voxel Planets · Streaming/LOD · Floating Origin     │
│ POI Placer · Anchor Loader · Weather/Day-Night                           │
├────────────────────────────── Core Layer ────────────────────────────────┤
│ ECS/Entity framework · Data Registry (defs) · Save/Load · Networking*    │
│ Mod Loader · Input · Audio · Rendering · Localization                    │
└──────────────────────────────────────────────────────────────────────────┘
                                                      * co-op ready, not at launch
```

## 13.3 Key systems

### Grid & block simulation
- Grids stored as sparse block maps (chunked 16³). Each block = definition ID + orientation + build % + HP + per-type state.
- **Sub-systems run on graphs**, not per-block ticks: power network graph, conveyor graph, room/air graph, structural graph. Graphs rebuild incrementally on block change.
- Structural integrity: simplified load propagation solved over the support graph at low frequency (e.g., 2 Hz) and on change.

### Rooms & atmosphere
- Flood-fill from air-tight block faces → room volumes; rooms connected by doors/vents form an atmosphere graph.
- Each room: O₂, CO₂, pressure, temperature, spores, noise, light, quality score (feeds colony sim).

### Colony simulation
- Survivors are entities with components: `Needs`, `Mood`, `Traits`, `Skills`, `Relationships`, `Schedule`, `JobPriorities`, `Health`, `Infection`, `Memory`.
- **Utility AI** picks actions: each available action (use bed, eat meal, do job X, chat with Y) advertises need satisfaction; survivors score and choose (classic *Sims* "advertisement" model).
- **Level-of-detail simulation:** survivors far from the player (other outposts/ships) run on an **abstract tick** (statistical resolution per in-game hour) instead of full agent simulation.

### Hollow crowds
- ECS/Mass-based crowd simulation with flowfield navigation to targets (noise sources, player, weak blocks).
- LOD tiers: full skeletal AI (≤ 60), simplified animation (≤ 300), vertex-animated impostors (thousands).

### Universe & planets
- **Deterministic seeds:** Galaxy seed → system seeds → planet seeds → chunk seeds. Only **deltas** (player changes) are saved.
- **Voxel terrain** (dual contouring or transvoxel) streamed in chunks, with LOD for orbit views.
- **Floating origin / large world coordinates** to support planets and interplanetary distances.
- **Anchor loader:** hand-authored levels are placed into generated worlds at fixed coordinates with terrain blending and exclusion zones.

### Story & quests
- **Quest graph** per mission (nodes: objectives, triggers, dialogue, cinematics; edges: conditions).
- **World flags** (see [03 §3.7](03-storyline.md#37-branching--consequence-tracker)) stored in a global state blackboard; all systems can query.
- **Dialogue**: Yarn Spinner / ink-style scripted dialogue with conditions on flags, relationships and traits.

## 13.4 Data-driven content (the expansion backbone)

Everything content is a **definition file** loaded into a central registry. Designers add content without code changes.

### Example: block definition
```json
{
  "id": "block.lifesupport.air_filter_spore",
  "name": "Spore Air Filter",
  "category": "life_support",
  "grid": ["large", "small"],
  "size": [1, 1, 1],
  "tier": 2,
  "components": { "component.steel_plate": 4, "component.motor": 2, "component.filter_mesh": 6 },
  "power_draw_kw": 3.5,
  "airtight_faces": "all",
  "behaviors": [
    { "type": "atmosphere.filter", "removes": "spores", "rate_per_min": 12 },
    { "type": "noise.emitter", "db": 38 }
  ],
  "colony": { "safety_advertisement": 2 },
  "research_unlock": "tech.bio.spore_filtration"
}
```

### Example: enemy definition
```json
{
  "id": "hollow.bloater",
  "archetype": "hollow",
  "health": 140,
  "speed": 1.2,
  "senses": { "hearing": 0.9, "sight": 0.2 },
  "weak_points": ["bloom_node.chest"],
  "on_death": [{ "type": "spawn_cloud", "cloud": "cloud.spores_dense", "radius_m": 5 }],
  "infection_on_hit": 0.08,
  "spawn_rules": { "min_bloom_coverage": 0.2, "biomes": ["any"], "act_min": 1 }
}
```

### Example: survivor trait definition
```json
{
  "id": "trait.claustrophobic",
  "name": "Claustrophobic",
  "description": "Hates small rooms. Loves a view.",
  "modifiers": [
    { "when": "room.size < 12", "moodlet": "moodlet.cramped_panic", "value": -10 },
    { "when": "room.has_window", "moodlet": "moodlet.open_view", "value": 6 }
  ],
  "conflicts_with": ["trait.spacer"]
}
```

### Example: mission definition (excerpt)
```json
{
  "id": "M2.04",
  "title": "Signal from Tycho",
  "act": 2,
  "prerequisites": ["flag:M2.03.complete"],
  "objectives": [
    { "id": "build_lander", "type": "build_requirement",
      "requirement": { "grid": "small", "twr_min": 1.5, "gravity_g": 0.16, "o2_minutes_min": 10, "has_block_category": "landing_gear" },
      "fallback_blueprint": "bp.story.lunar_lander_mk1" },
    { "id": "land_tycho", "type": "reach_location", "location": "anchor.moon.tycho" },
    { "id": "recover_archive", "type": "acquire_item", "item": "item.story.styx_archive" }
  ],
  "rewards": { "tech": ["tech.power.he3_fusion"], "flags": ["styx_archive_recovered"] }
}
```

### Content types in the registry
Blocks · Components · Items · Recipes · Tech nodes · Enemies · Creatures (part kits) · Biomes · Planet types · POIs · Traits · Moodlets · Needs · Jobs · Events · Dialogue · Missions · Factions · Loot tables · Audio banks · Localization strings.

## 13.5 Save system
- **Save = seeds + deltas + entity states + world flags.**
- Grids serialized in compressed binary; planets save only modified voxel chunks.
- Autosave on: mission start, docking, sleeping, jumping. Manual saves anywhere (except Hardcore).
- Versioned save schema with migrations (required for long-term expansion support).

## 13.6 Modding
- Mods = additional definition folders + assets + optional scripts (sandboxed Lua).
- Load order, dependency declarations, and conflict reports.
- Steam Workshop integration for blueprints, mods and scenarios (post-launch).

## 13.7 Performance targets
| Target | PC recommended | Console |
|---|---|---|
| Frame rate | 60 fps @ 1440p | 30 fps quality / 60 fps performance |
| Max blocks per grid (practical) | 50,000 | 25,000 |
| Simulated survivors (full AI) | 40 | 30 |
| Active Hollows (full AI / impostors) | 60 / 2,000 | 40 / 1,000 |
| Planet streaming | No loading screens planet ↔ orbit | Same |

## 13.8 Co-op readiness (post-launch)
- Deterministic sims (power, air, colony) designed to be **server-authoritative**.
- Block edits as replicated commands; grid physics owned by nearest player/host.
- Build the single-player game **on a local host/client architecture from day one** so co-op isn't a rewrite.
