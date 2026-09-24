# 01 — Vision & Pillars

## 1.1 Vision statement

EXODUS PROTOCOL is about **rebuilding civilization one bolt and one person at a time.** The player begins with nothing but a multitool during the collapse of human society. By the end they command a fleet of self-built ships, a thriving orbital colony, and the fate of a species.

The game fuses three proven fantasies:

| Inspiration | Fantasy we borrow | Our twist |
|---|---|---|
| **Space Engineers** | "I designed and built this machine, and physics says it works." | Building is survival-critical: a badly braced wall *will* fall to a Brute. |
| **The Sims** | "These little people have lives, and I care about them." | Survivors are traumatized, can be infected, and remember how you treated them. |
| **No Man's Sky** | "Every planet is a new place nobody has seen." | The galaxy is scarred by an ancient plague; exploration is also investigation. |

## 1.2 Design pillars

### Pillar 1 — Build What Saves You
- All player structures (bases, ships, rovers, turrets) are assembled from blocks on grids.
- Structures are simulated: mass, thrust, power draw, pressurization, structural integrity, per-block damage.
- Engineering choices have survival consequences: power fails → life support fails → survivors panic.
- **Test:** *Can the player point at something and say "I built that, and it's why we're alive"?*

### Pillar 2 — People, Not Resources
- Survivors are autonomous agents with needs, traits, skills, moods and relationships.
- They work jobs, form friendships, fall in love, argue, grieve, and can break.
- Key companions carry the story; generic survivors carry emergent stories.
- **Test:** *Does the player know their survivors by name after two hours?*

### Pillar 3 — Fear on the Ground, Wonder in the Sky
- Planetside, especially on Earth and infected worlds: limited light, limited ammo, hordes, dread.
- In space: vast silence, beautiful vistas, freedom of movement, calm building.
- The rhythm alternates tension and release; the ship/station is the safe hearth you return to.
- **Test:** *Is the player relieved to hear their airlock cycle shut?*

### Pillar 4 — A Mystery Worth Crossing the Galaxy For
- A hand-authored critical path (~12 hours) with strong characters and a real ending.
- Story locations are hand-crafted "anchors" placed inside a procedural universe.
- Lore is found through environmental storytelling, logs, precursor glyphs and survivor dialogue.
- **Test:** *Does the player want to know what the Sowers were?*

### Pillar 5 — Built to Grow
- Content is defined in data (JSON/asset definitions), not hard-coded.
- New blocks, items, enemies, biomes, traits, events and story arcs are additive modules.
- The campaign ends; the universe does not.
- **Test:** *Could a designer add a new enemy type or planet biome without an engineer?*

## 1.3 Target experience — the "player story"

> Hour 1: I'm crawling through a burning spaceport with a flashlight, hearing things moan in the dark.
> Hour 2: I welded shutters over the hangar doors, and when the horde came, they held. Barely.
> Hour 3: I watched Earth shrink in the window of a rocket I assembled from salvage, while Lily cried and Tug held her.
> Hour 5: Our station has gardens now. Mara and Idris got into a shouting match over rations and I had to build a second mess hall.
> Hour 7: I landed on a world with purple oceans and found a ruin older than the dinosaurs, covered in the same growths as the dead back home.
> Hour 10: I flew the ship I designed into the mouth of something the size of a moon.
> Hour 12: I made a choice I'm still thinking about. Then I kept playing.

## 1.4 Core gameplay loops

### Moment-to-moment (seconds)
Move → scan → gather/fight → build/place → manage vitals.

### Session loop (30–60 minutes)
```
 ┌──────────────┐     ┌──────────────┐     ┌──────────────┐
 │  EXPEDITION  │ ──▶ │   RETURN &   │ ──▶ │  EXPAND THE  │
 │ explore, loot│     │  UNLOAD LOOT │     │   COLONY     │
 │ fight, rescue│     │ heal, rest   │     │ build, assign│
 └──────▲───────┘     └──────────────┘     └──────┬───────┘
        │                                         │
        │          ┌──────────────┐               │
        └───────── │   RESEARCH   │ ◀─────────────┘
                   │ unlock tech, │
                   │ story leads  │
                   └──────────────┘
```

### Campaign loop (hours)
Story mission reveals a new region → region introduces a new resource/tech tier → new tech enables the next region and the next story mission.

## 1.5 Unique selling points
1. **Horror-to-hope arc:** starts as tense zombie survival, grows into a hopeful space-colony epic.
2. **Physical engineering with social consequence:** your station's layout shapes your survivors' happiness and relationships.
3. **Infection as a systemic threat:** the plague can spread *inside* your colony through air vents, wounds and water — it's not just enemies at the door.
4. **Seamless ground-to-orbit:** walk off a burning Earth, fly to orbit, land on alien worlds, no loading screens (target).
5. **Hand-authored mystery inside a procedural galaxy.**

## 1.6 What EXODUS PROTOCOL is *not*
- Not a competitive PvP game.
- Not a twitch shooter — combat is weighty, resource-constrained and tactical.
- Not a pure sandbox — the campaign has direction, stakes and an ending.
- Not a micro-managing god game — the player is a person in the world, not a floating cursor (though a colony management overlay exists).
- Not endless grind — the 12-hour path is tuned to keep moving.

## 1.7 Audience
- **Primary:** 18–40 PC players who love survival-crafting and builders (Space Engineers, Subnautica, Valheim, 7 Days to Die, NMS).
- **Secondary:** Life-sim and colony-sim fans (The Sims, RimWorld, Frostpunk) who want a first-person, story-driven take.
- **Player types served:** Builders (engineering depth), Caretakers (colony sim), Explorers (procedural galaxy), Story-seekers (campaign), Fighters (horde defense & boarding).
