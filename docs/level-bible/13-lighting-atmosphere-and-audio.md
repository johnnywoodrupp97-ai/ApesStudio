# 13 — Lighting, Atmosphere & Audio

> How levels look and sound: time of day per planet, lighting budgets and rules, skies and weather, the Bloom's light, and the audio layers every space needs. Each level card (chapters 04–09) lists its mood palette, key light and audio; art direction is in game bible [12](../game-bible/12-art-audio-ui.md).

## 13.1 Time of day by planet

| Planet | Day length | Sun | Sky | Night |
|---|---|---|---|---|
| **Earth** (PLN-001) | 60 min (40 day / 20 night) | Hard desert sun in Kestrel Valley | Blue scattering; dust haze near the ground | Moonlit blue, sodium floodlights and fires; every 3rd night a **Green Moon** (green-tinted moonlight, Bloom glow ×2) |
| **The Moon** (PLN-002) | 120 min | Unfiltered white; razor-sharp shadows | Black, stars visible in daylight; **Earth always in the near-side sky** | Earthshine (blue-white fill) |
| **Veyra-4** (PLN-003) | 80 min | Warm white through humid haze | Lavender scattering; purple seas reflect | Bioluminescent jungle; Tessari herds glow faintly |
| **Hollowmere** (PLN-004) | 150 min | Low, pale; long shadows | White-grey; blizzards cut visibility to 20 m | Aurora bands; candle-lit Cathedral |
| **Drift planets** | 30–180 min (by seed) | Star type sets the light color and solar output | By atmosphere type: none (black), thin (dark blue), breathable, toxic (yellow-green), spore-laden (green haze) | By type |

Missions may lock the time of day (the Long Night, M1.06, is always night); the open world never does.

## 13.2 Lighting budgets and rules

Shadow-casting light budgets per level type (from [01](01-level-overview.md)):

| Type | Shadow lights | Notes |
|---|---|---|
| Open Region / Planet Region | 4 / 2 per streaming cell | Sun, moon and 1–2 hero lights; everything else is non-shadowing or baked |
| Space Region | 1 per cell | The star |
| District | 12 | Floodlights, fires, signage |
| Interior | 16 | Practical lights; emergency strips |
| Hub | 24 | The most complex lighting; the player spends the most time here |
| Dungeon | 20 | — |
| Set Piece | 16 | Scripted lights (fire, explosions) count |
| Space Arena | 8 | Star plus ship lights |
| Procedural Template | 8 | Templates are stamped many times; keep them cheap |

**Rules**
1. **Key light first.** Every space has one key light, marked `LT_Key_<Space>`: sun, moon, a fire, a window or a hero lamp. Fill and rim come after.
2. **Light the critical path.** The goal is always the brightest or most saturated point in view. Emergency-light color (red), fire (orange) and the Bloom (green) are the wayfinding palette; don't use them for decoration on a critical path.
3. **Player lights matter.** Floodlights, lamps and the helmet light raise a base's **Attraction** (game bible 22). Dark places are safer, and levels should make that trade-off visible.
4. **Practical sources.** Every artificial light has a visible fixture (lamp, strip, sign). No invisible fills in interiors.
5. **Airless worlds** have no ambient sky light. Fill comes only from bounce light and the planet (Earthshine on the Moon), so shadows are black unless lit. Put reflective regolith, lamps or suit lights where the player must read detail.

## 13.3 Mood palettes by group

| Group | Palette | Key light |
|---|---|---|
| **Kestrel Valley & Complex** (KVL, KES) | Desert sand `#C9A66B`, sage `#8A9A6B`, sky blue `#7FB2D9`, sodium night `#E8A13A` | Hard desert sun by day; sodium floodlights and fires by night |
| **Orbit & the Moon** (ORB) | Space black `#05070B`, Earth blue `#3D7CC9`, sun white `#FFF8E7`, habitat amber `#FFB866`; on the Moon regolith grey `#8C8C8C`, Earthshine blue `#6FA8DC` and hi-vis orange `#FF7A00` | Unfiltered sun (orbital day/night every 40 min), station practicals, Earthshine |
| **The Drift** (DRF) | Per anchor: Tortuga's cargo orange, container blue and neon pink; Veyra-4's violet foliage, purple sea and gold light; Hollowmere's ice blue and candle amber; Ark Meridian's ceramic white and gold; the Convergence Gate's teal and violet | Per anchor (see each card) |
| **The Seedship** (SEE) | Deep violet `#3A2A5C`, living green `#7FD06B`, pearl `#E9E4DA`, glyph teal `#2EE6D6` | Bioluminescence that pulses with the ship's "breath" |
| **The Bloom** (overlay on any group) | Bloom green `#7FD06B` emissive veins; spore haze | Emissive growths, brighter at night and on Green Moon nights |

## 13.4 Atmosphere, sky and weather

| Element | Rule |
|---|---|
| **Atmospheric scattering** | Per planet: density, color and height from the planet's atmosphere (top at 15% of the radius; Earth 9 km). Airless worlds have none. |
| **Cloud deck** | At 40% of the atmosphere height (Earth 3.6 km). Clouds are volumetric near the camera and an impostor layer above; flying through them is part of the entry sequence ([11](11-space-travel-and-planet-transitions.md)). |
| **Weather volumes** | `VOL_Weather_*` sets the weather for a region: dust storms and heat shimmer (desert), spore storms (Prospect, Bloomed zones), blizzards (Hollowmere), monsoon (Veyra-4). Weather changes over 60–120 s, never instantly. |
| **Spore storms** | Visibility drops to 30 m under a green haze, masks are required, and Hollow activity rises. Storms blow from Prospect's Bloom Hearts across the valley. |
| **Height fog** | Kestrel Valley basin fog at dawn; Hollowmere ground blizzard; the Seedship's spore mist. Fog never hides the primary landmark. |
| **Space** | Star-field skybox per system; nebula and gas-giant impostors; the Seedship's 1,000 km petal-sails as VFX on the skybox layer. |

## 13.5 The Bloom's light
The Verdance is also a lighting system. Bloom growths are emissive: veins pulse slowly and brighten as the player approaches a Bloom Heart. The Bloom level of a volume (`VOL_Bloom_<0–5>`) sets:

| Bloom level | Visual | Light |
|---|---|---|
| ●○○○○ | Isolated growths | Faint emissive dots |
| ●●○○○ | Veins on walls, patches of ground cover | Soft green bounce light near growths |
| ●●●○○ | Overgrown rooms, spore motes | Green fill in interiors at night |
| ●●●●○ | Canopies, hanging tendrils | Green dominates night lighting |
| ●●●●● | Bloom Hearts, spore chimneys | Pulsing green key light; the sky is tinted by spore haze |

Healing a planet (Veyra-4) or destroying Bloom Hearts (Prospect) repaints the Bloom map over in-game days. Lighting follows automatically.

## 13.6 Audio in levels

| Layer | Marker | Rules |
|---|---|---|
| **Ambience beds** | `VOL_Audio_<Name>` | One bed per space type (desert wind, hangar hum, station air, jungle, ice, the Seedship's heartbeat). Crossfade over 2–4 s at volume edges. |
| **Reverb** | `VOL_Reverb_<Preset>` | By space: open air, small room, hall, hangar, tunnel, cave, ice cathedral, living hall. Each `VOL_Room_*` gets a reverb preset. |
| **Point sources** | Empties (`LT_`/`POI_` or `VOL_Audio_Point_*`) | Machines, radios, alarms, the Diner's buzzing neon. They double as navigation cues. |
| **Audio landmarks** | `LM_Audio_*` | A sound the player can steer by when they can't see: the Cathedral's Hum in the blizzard, the five-note Sower pulse from Red Mesa, a church bell in the Ghost Towns. |
| **Hollow audio** | Spawners | Moans carry 60 m; Screamer shrieks 150 m. Knocking behind doors foreshadows encounters. |
| **Occlusion** | Blockout walls | Walls and voxel terrain occlude sound. Doors attenuate when closed. |
| **Vacuum** | Pressure volumes | No airborne sound in vacuum: only contact sounds (through the suit) and radio. Airlock cycling brings the world's sound back (game bible 21 §21.4). |
| **Travel** | Transition shells | The atmosphere's roar fades in on entry and out on exit; the pulse drive spools with a rising tone and drops out with a bass *thump*. |

**Music states** switch by level state: explore, tension (enemies aware), combat, siege, set piece and safe (in a base with no threat). Signature themes are placed by level: *Sunday* on kora for the family scenes, Crane's quartet in the Directorate spaces, and the Drowned Choir's song in Memory Garden 2.

## 13.7 Blender spec
- Key lights are marked `LT_Key_<Space>` (empties). The engine importer creates the light type from the name: `LT_Key_Sun`, `LT_Key_Spot_*` or `LT_Key_Point_*`.
- Audio and reverb volumes are `VOL_Audio_*` and `VOL_Reverb_*` wireframe boxes; weather and Bloom volumes are `VOL_Weather_*` and `VOL_Bloom_*` (usually the whole level).
- Level scaffolds put the mood (time, palette, key light) and audio notes in the `EXODUS_NOTES` text block and the level's root metadata.
