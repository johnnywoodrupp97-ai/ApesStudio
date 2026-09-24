# 08 — Open World & Exploration

> **The open-world promise:** *If you can see it, you can go there — if you can survive it.*
> EXODUS PROTOCOL is an **open-world, open-exploration survival game** first. The 12-hour story is a road through that world, not a fence around it.

## 8.1 The three freedoms

| Freedom | What it means | How we deliver it |
|---|---|---|
| **Freedom of route** | Go anywhere, in any order, by any means you can build | Seamless ground-to-orbit-to-stars travel; no invisible walls; capability gates instead of story locks |
| **Freedom of pace** | The story waits for you | No global timers; story leads sit in your journal until you pick them up |
| **Freedom of purpose** | Surviving, building, exploring and following the story are all valid ways to play | Full survival sandbox under the campaign; every system rewards non-story play |

## 8.2 How open is it, act by act

| Phase | Openness | What's open | What's gated (and how) |
|---|---|---|---|
| **Cold open + Prologue** (0:00–0:30) | Linear | — | Authored tutorial. The only fully linear part of the game. |
| **Act I — Earth** | **Open region** | All of **Kestrel Valley** (64 km², §8.5) from the end of the prologue | Dangerous districts are gated by **threat** (Bloom density), not walls |
| **Act II — Orbit & Moon** | **Open frontier** | Earth (return any time), low Earth orbit, the whole Moon, the debris belt | Vacuum, radiation and fuel range gate travel. You need the right suit and ship. |
| **Act III — The Drift** | **Open galaxy** | ~60 star systems, every planet explorable | Jump range and fuel. Hazard worlds need specific tech. |
| **Act IV — Seedfall** | Focused finale | The Seedship. The rest of the galaxy stays open until you commit. | A clearly marked **point of no return** (you can save first) |
| **Post-game** | Fully open sandbox | Everything, plus the Deep Drift | — |

**Target split for a typical first playthrough:** about 40% of time on story missions, 60% on player-driven exploration, building, survival and colony life. A focused player can finish the critical path in about 12 hours; a wandering player might take 40 or more.

## 8.3 Game modes & story pace

| Mode | Description |
|---|---|
| **Campaign — Guided** | Waypoints on, KESTREL nudges if you've drifted from the story for a while. For players who want the 12-hour arc. |
| **Campaign — Open** *(default)* | Story leads appear in the journal with a rough location; no waypoint until you ask. Nudges are rare and in-fiction. |
| **Campaign — Explorer** | No waypoints, no nudges. Story is found only by following signals, rumors and scanners. |
| **Survival Sandbox** | No story. Choose a start: *Earth Outbreak*, *Derelict in Orbit*, *Crash-landed in the Drift*, or *Random*. Endless. |
| **Creative** | Unlimited resources, optional enemies. |

The story pace can be changed at any time in settings. All modes share one world simulation.

## 8.4 World structure — the Four Frontiers

```
                          ┌───────────────────────────────┐
                          │     FRONTIER 4: DEEP DRIFT     │  post-game / expansions
                          │   unlimited procedural systems │
                          └───────────────▲───────────────┘
                                          │ outer jump lanes
┌─────────────────────────────────────────┴───────────────────────────────────────┐
│                          FRONTIER 3: THE DRIFT  (Act III+)                        │
│  ~60 procedural systems seeded per save · 5 anchor systems (Tortuga, Veyra,      │
│  Hollowmere, Meridian, Convergence Gate) · faction territory · derelicts · wonders │
└─────────────────────────────────────────▲───────────────────────────────────────┘
                                          │ Sower jump lane (Styx)
┌─────────────────────────────────────────┴───────────────────────────────────────┐
│                    FRONTIER 2: ORBIT & MOON  (Act II+)                            │
│  LEO debris belt (derelict satellites, dead stations) · Haven-9 · full Moon       │
│  (procedural surface + Tycho anchor) · Earth–Moon Lagrange caches · Styx Wreck   │
└─────────────────────────────────────────▲───────────────────────────────────────┘
                                          │ launch / re-entry (seamless)
┌─────────────────────────────────────────┴───────────────────────────────────────┐
│                     FRONTIER 1: EARTH  (Act I+)                                   │
│  Kestrel Valley — 64 km² hand-authored open region  ·  "Earth Returns":          │
│  wider procedural Earth regions unlocked from orbit in Act II                     │
└──────────────────────────────────────────────────────────────────────────────────┘
```

## 8.5 Frontier 1: Kestrel Valley (Earth)

A **64 km² hand-authored open region** of Nevada high desert, bounded by mountains (visual boundary, not a wall: climb far enough and the terrain becomes impassable, and you can always fly over later).

| District | Bloom threat | What's there | Why go |
|---|---|---|---|
| **Kestrel Aerospace Complex** | ●●○○○ | Hangars, terminals, fuel farm, launch pads, Mission Control, the Vault | Story hub; components; the *Wren* |
| **Kestrel Township** | ●●○○○ | Company town: diner, school, gas station, hardware store, suburbs | Food, tools, first survivors |
| **Route 93 & the Truck Stop** | ●○○○○ | Highway pile-ups, a truck stop, abandoned cargo trailers | Early loot, vehicles for parts, roaming trader |
| **Jackrabbit Flats** | ●○○○○ | A dry lake bed and an old airstrip | Rover speed runs, safe outpost site, early aircraft parts |
| **Hollis Dam & Reservoir** | ●●●○○ | Hydroelectric dam, lake, a boat marina | Clean water, huge power if restored (a base-site choice) |
| **Silver Ridge Mines** | ●●●○○ | Open-pit and shaft mines, ore processing | Iron, copper, silicon; Burrowers in the deep shafts |
| **Red Mesa Observatory** | ●●○○○ | Radio telescope array on a mesa | Early signal decoding; Styx lore; a sniper's-eye view of the valley |
| **Fort Calder** | ●●●●○ | Abandoned military base overrun during evacuation | Weapons, armor, military vehicles; very dangerous |
| **Prospect (city edge)** | ●●●●● | A small city swallowed by a Bloom Heart cluster | The best loot on Earth; Screamers, Brutes; endgame for Earth |
| **Ghost towns (×3)** | ●●○○○ | Silver-rush ruins, a motel, a church | Survivor camps, side stories, hidden caches |

**Survival rules in the valley:**
- **Day/night:** a 60-minute cycle (40 day / 20 night). Nights bring hordes and roaming packs.
- **Weather:** heat waves (thirst), dust storms (visibility, suit filters), flash floods near the reservoir, rare **spore storms** blowing in from Prospect.
- **Base anywhere:** the hangar is where the story starts, but you can build your main base at the dam, on the mesa, at the mines, or out on the flats. The story adapts: missions reference your base, not a fixed place.
- **Earth Returns:** from Act II you can re-enter the atmosphere anywhere on the globe. Outside Kestrel Valley, Earth is procedurally generated regions (cities, forests, coasts) with Bloom density rising as the story advances.

## 8.6 Gating: capability gates, not walls

We never use invisible walls or "you can't go there yet" messages. Every limit has a **reason in the world** and a **way to beat it**.

| Gate type | Example | How the player beats it |
|---|---|---|
| **Threat** | Prospect's Bloom Heart cluster | Better weapons, turrets, or stealth — or just skill |
| **Environment** | Vacuum, spores, −80 °C, radiation, crushing gravity | Suits, filters, heaters, shielding, stronger thrusters |
| **Travel** | Orbit needs a rocket; the Drift needs a Jump Core | Build it. There's always a blueprint, and you can design your own. |
| **Knowledge** | Most points of interest are hidden until a signal is decoded | Scanners, antennas, signal decoders, talking to survivors |
| **Fuel & supply** | A ship's jump range limits how deep into the Drift you can go | Refineries, fuel depots, outposts |
| **Story anchor** | The Seedship *Anthesis* only exists after M3.08 | The one true story lock, and it's in the finale |

### Sequence breaking by engineering
If you're good enough to get somewhere early, **the game lets you.**
- **Reach orbit early:** if you design your own launch vehicle before M1.07 (it takes serious resources and skill), you can go. Act II starts when you dock at Haven-9, however you got there. Anyone you haven't rescued becomes a **lead back on Earth**. If Tug hasn't been lost at the launch pad, he's alive at the hangar and radios you to come get him.
- **Visit a Key world early:** Veyra-4 and Hollowmere can be reached as soon as you have the jump range, before Tortuga gives you their locations.
- **Rule:** *story anchors respond to the state you arrive in, not to mission order.* Every critical beat has a fallback trigger (see [17 — Narrative Design §17.6](17-narrative-design.md)).

## 8.7 How the story lives in an open world

### The Leads journal
The journal holds **Leads**, not a quest list:

| Lead type | Source | Example |
|---|---|---|
| **Story** (gold) | Main-thread missions | "A looped distress call from Kestrel Elementary." |
| **Companion** (blue) | Companion quests | "Tug keeps talking about his daughter's ashes at the house on Elm." |
| **Rumor** (grey) | Survivors, traders, radio | "Truckers say Fort Calder's armory was never emptied." |
| **Signal** (teal) | Decoded transmissions | "Repeating 5-note pulse, bearing 047, strength rising." |

Each lead shows a **recommended readiness** (e.g., *needs spore filtration*, *Bloom threat ●●●●○*) so players can judge risk without being blocked.

### Open act structure

```
        ┌─────────── ACT I: KESTREL VALLEY (open) ───────────┐
        │  Four Walls ─▶ first survivors, base anywhere       │
        │  Leads (any order): School · Crash site · Vault ·   │
        │  4 Wren parts · Survivor stories · Rumors · Caches  │
        │  Gate: the Wren is complete (or your own rocket)   │
        └──────────────────────────┬──────────────────────────┘
                                   ▼ The Long Night ▶ Liftoff
        ┌─────────── ACT II: ORBIT & MOON (open) ────────────┐
        │  Haven-9 hub · the Moon · debris belt · Earth Returns │
        │  Leads: Tycho · Patient Zero (systemic) · Styx data   │
        │  Gate: a ship that can reach Styx                   │
        └──────────────────────────┬──────────────────────────┘
                                   ▼ Into the Seed ▶ Jump Core
        ┌─────────── ACT III: THE DRIFT (open galaxy) ────────┐
        │  Tortuga hub · ~60 systems · 2 Keys in any order    │
        │  The Taking fires after the 2nd Key (at a safe      │
        │  moment: never mid-mission) ▶ Grief ▶ Meridian      │
        │  Gate: three Keys                                   │
        └──────────────────────────┬──────────────────────────┘
                                   ▼ Convergence ▶ point of no return
                       ACT IV: SEEDFALL (focused finale)
```

- **Systemic story beats** (Patient Zero, The Taking) trigger from world state and **only at safe moments**: when you're at your base or have just returned from a mission, never mid-combat or mid-flight.
- **Story waits, the world doesn't:** hordes roam, survivors age, crops grow, factions move. None of this can fail the campaign.

## 8.8 The living world

| System | What it does | Guardrail |
|---|---|---|
| **Bloom spread** | Each region/system has a Bloom level that rises slowly over time and falls when you destroy Bloom Hearts or shut down Garden Engines | Capped per act; never reaches a fail state; clearing a region is permanent unless a story event reverses it |
| **Hordes & migrations** | Hollow hordes roam Earth and Bloomed worlds, drawn by noise, light and heat | Horde size scales with difficulty and your base's Attraction score |
| **Faction patrols & territory** | Directorate, Choir and Hauler ships and ground teams move between territories | Territory updates on jumps and story beats, not in real time |
| **Dynamic events** | Distress calls, supply drops, meteor showers, trader convoys, refugee pods, spore storms | At most one major event at a time, and none during story missions |
| **Survivor camps** | NPC camps grow, trade, fight among themselves, or fall | A camp you've helped never falls without warning |
| **World memory** | Bodies stay; bases you abandon can be overrun and become points of interest; cleared zones visibly heal | Saved as deltas (see [13](13-technical-architecture.md)) |

## 8.9 Exploration rewards
Every **90 seconds of travel** should offer something to notice: a landmark, a signal, a resource, a wreck, a creature, a view.

| Reward | Found by | Why it matters |
|---|---|---|
| **Blueprint fragments** | Derelicts, military bases, Sower ruins | Some blocks (e.g., the railgun, the Bloom-grown hull) exist *only* through exploration |
| **Notable survivors** | Rescue events, camps, pods | Rare traits and skills; each has a personal story |
| **Scan data** | Scanning species, minerals, ruins | Research points; you can name what you discover |
| **Sower glyphs (64)** | Ruins, wonders, the Bloom itself | Codex, lore, the secret epilogue |
| **Wonders** | Rare procedural phenomena | Unique views and one-off rewards (see §8.14) |
| **Legendary gear** | Deep threat zones | Named weapons and suit modules with unique perks |
| **Lore** | Logs, letters, graffiti, environmental stories | Ada's letters and Crane's logs change the story |

## 8.10 Open-world survival loop (no story required)

```
 SCOUT ─▶ travel & scan ─▶ find a signal / resource / wreck
   ▲                                      │
   │                                      ▼
 PLAN ◀── upgrade & expand ◀── RETURN ◀── SURVIVE the trip
 next     base, ship,          unload,     (vitals, weather,
 trip     colony               heal, rest  Hollows, infection)
```

The sandbox has its own long-term goals, independent of the story: grow the colony to 40 survivors; push the Bloom back from a whole region; build a jump-capable capital ship; chart every system in the Drift; complete the codex; find every Wonder.

## 8.11 Travel methods

| Method | Range | Unlock | Notes |
|---|---|---|---|
| On foot / jetpack | Local | Start | Jetpack limited in gravity |
| Rover & motorbike | Planet surface | Act I | Wheeled physics; carry survivors and cargo |
| Aircraft | Planet | Late Act I (optional) / Act II | Atmospheric thrusters and wings; build from Jackrabbit Flats parts |
| Orbital flight | Local space | Act II | Seamless planet ↔ space transitions; assisted flight at 1,200 m/s (boost 2,000) |
| **Pulse Drive** (cruise) | Planet to planet in a system | Act II | 3 s spool, 30 km/s after 15 s; planet to planet in 30 s – 2.5 min; drops out automatically near planets and stations; can be interrupted by events |
| **Sower Jump** | System to system | Act III | Jump Core + Resonance Crystal fuel; 10 s charge, 8–12 s jump tunnel, 5 min cooldown; you arrive 10–20 km from the system's station or beacon |
| **Fast travel** | Between your own beacons | Act II | Optional; needs a Beacon Relay at both ends; off in Hardcore |

### Space travel and planet entry, No Man's Sky style
One continuous universe with no loading screens. Every transition is a short, readable sequence that also hides streaming:

- **Launch:** press *Launch* on the ground. The ship lifts 30 m in 3 s (it needs a thrust-to-weight ratio of at least 1.2 in local gravity), then you fly. Climbing through the cloud deck and out of the atmosphere takes about a minute from Earth's surface.
- **Leaving the atmosphere (5 s):** the sky fades to black, stars appear, the atmosphere's roar drops away and the speed cap rises from 250 to 1,200 m/s.
- **Cruise:** the Pulse Drive can't engage below half a planet's radius. Above that, it takes you across a system in seconds and drops out automatically at the destination planet's approach distance or 20 km from a station.
- **Entry (8 s):** dive toward a planet and the ship enters the atmosphere: heat glow, buffeting, clouds rushing past. Speed eases from 1,200 to 250 m/s over 4 s, so it's never a hard stop. On airless worlds a 400 m/s approach cap replaces the entry effects.
- **Landing:** below 150 m over a slope of 20° or less, a *Land* prompt auto-lands the ship in 6 s. Manual landing is always possible, and pads and landing gear lock on contact.
- **Capital ships** stay in orbit, parked just above the atmosphere. Smaller ships ferry crew and cargo to the surface.

Exact per-planet altitudes, speeds and timings (orbit to landed takes about 74 s on Earth and 22 s on the Moon) are in the level bible: [11 — Space Travel & Planet Transitions](../level-bible/11-space-travel-and-planet-transitions.md).

## 8.12 Planet generation

### Parameters (per planet)
- **Type:** Rocky, Ocean, Ice, Desert, Jungle, Volcanic, Toxic, Barren (airless), Gas giant (orbit only: moons and stations), **Bloomed** (overrun by the Verdance)
- **Size:** **20–120 km diameter**, the voxel traversal scale used by games like *Space Engineers*: small worlds (moons, barren, ice) 20–40 km (35%), medium 40–80 km (45%), large (jungle, ocean, Bloomed) 80–120 km (20%). Earth, the starter planet, is 120 km. At this scale a planet is huge on foot or by rover, the crust is deep enough for extensive voxel mining, and there are no thousands of kilometers of empty terrain. The curvature is visible from orbit, but the ground feels flat when you stand on it. Planets under 40 km never get oceans. The full standard (atmosphere height, crust depth, gravity falloff, horizon and landmark maths, face-map resolution) is in the level bible: [03 — Planets & Voxel Scale](../level-bible/03-planets-and-voxel-scale.md).
- **Gravity:** 0.1–1.8 g
- **Atmosphere:** None / Thin / Breathable / Toxic / Spore-laden
- **Temperature band:** from star type, orbital distance and day/night
- **Hazards:** storms (dust, ice, acid, spore), radiation, quakes, meteor showers
- **Bloom Coverage:** 0–100%, which drives enemy density, visuals and resources
- **Biomes:** 2–5 per planet from the type's pool

### Terrain
- **Voxel-based**, fully diggable and minable: a cube-sphere with six cube-face heightmaps (plus biome, ore and Bloom maps), noise layers and approximate erosion; 1 m voxels in 32 m chunks, streamed in 8 level-of-detail rings. The crust is minable to a depth of 3.5% of the radius (2.1 km on Earth).
- Hand-authored **regions** (Kestrel Valley, Tycho, the Garden Engine) are built flat and stamped onto the cube faces. They're capped at 16 km and at a quarter of the planet's diameter.
- Hand-authored **terrain stamps** (canyons, craters, mesas, Sower ruins) placed by rules.
- Cave networks for ore, hideouts and Hollow nests.

### Flora & fauna
- **Procedural creatures** assembled from part kits: body plan, limbs, heads, patterning, and a behavior template (grazer, predator, flyer, burrower, swarm).
- Every living planet has **Bloom variants** of its fauna, in a ratio set by Bloom Coverage.
- **Discovery log:** scan species, plants, minerals and ruins for research points, and name them.

## 8.13 Points of interest

| POI | Frequency | Content |
|---|---|---|
| **Derelict ship** | Common | Procedural interior, loot, logs, sometimes Drifters |
| **Crash site** | Common | Salvage; sometimes survivors |
| **Survivor camp** | Uncommon | Recruitable survivors, trade, sometimes a quest |
| **Bloom Heart** | Uncommon | Dense Hollow nest; destroying it cuts local Bloom; big rewards |
| **Sower ruin** | Uncommon | Glyphs, puzzles, precursor components |
| **Directorate outpost** | Uncommon | Hostile, high-tech loot, intel |
| **Choir shrine** | Rare | Dialogue, Choir reputation, strange rewards |
| **Hauler waystation** | Rare | Trade, contracts, repairs |
| **Anomaly** | Rare | Unique events: a lone Sower construct, a time-dilated signal, a human ship from before 2071… |

## 8.14 Wonders (rare procedural phenomena)
- **The Singing Ring:** a planetary ring that hums in the Verdance motif when you fly through it.
- **Glass Forest:** silicate trees that ring like bells in the wind.
- **Tidal Titan:** a creature the size of a mountain, asleep in a shallow sea.
- **Frozen Fleet:** hundreds of Sower Seedlings locked in a comet.
- **The Mirror World:** a planet whose ruins match a human city layout. (Glyph lore.)
- Wonders are discovered once per save and logged forever in the codex.

## 8.15 Scanning & navigation
- **Handheld scanner:** identifies objects, creatures, ores and infected people; pings nearby POIs.
- **Ship scanner array:** long-range planet scans (resource map, Bloom coverage, life signs).
- **Signal decoder:** triangulates distress calls and Sower beacons — the main way to find POIs.
- **Galaxy map:** jump lanes, discovered systems, faction territory, Bloom spread, leads.
- **No planetside minimap:** a compass with markers only, so the world is read by looking at it.

## 8.16 Outposts
- Build **outposts** anywhere (static grids): for mining, farming unique crops, research or refueling.
- **Staff** them with survivors (who then need homes there) or **automate** them with drones.
- Local Hollow activity threatens outposts in proportion to Bloom Coverage. Defend them with turrets, or keep them quiet (noise and light attract Hollows).
- **Supply lanes** (T3): automated cargo shuttles between outposts and your main base or ship.

## 8.17 Anchor locations (hand-crafted)

| Location | Type | Signature features |
|---|---|---|
| **Kestrel Valley (Earth)** | Temperate desert, 64 km² | Spaceport, township, dam, fort, mines, observatory, Prospect |
| **Haven-9** | Orbital station | The colony's first real home in space |
| **Moon — Tycho** | Barren, 0.16 g | Mining outpost interior, dust storms, Earthrise |
| **Styx Wreck** | Hollow seed pod | The first Sower architecture |
| **Veyra-4** | Jungle/ocean, 0.9 g | Purple seas, Tessari herds, a 2 km Garden Engine spire |
| **Hollowmere** | Ice, 0.7 g, −80 °C | Blizzards, ice caves, Cathedral of the Hum |
| **Ark Meridian** | Station over a gas giant | Directorate flagship-station, zero-G decks |
| **Tortuga Drift** | Hollow asteroid city | Markets, docks, contracts |
| **Convergence Gate** | Sower megastructure | Fleet-battle arena |
| **Seedship *Anthesis*** | Living megastructure | Four Memory Gardens |
