# 19 — Set Pieces & Cinematics

## 19.1 Cinematic philosophy
- **First person by default.** The player keeps the camera through 95% of the story. Characters perform *to* the player.
- **Cut only when the player *can't* be present, or when scale demands it:** Ada's cockpit, Crane's office, the Seedship through the Gate.
- **Never cut to kill the player's agency.** If the player could act in a moment (e.g., Tug at the clamps), it's in-engine and playable.
- **Every cinematic is in-engine and reflects player state:** your ship, your colony's faces, your cargo, the damage on your suit.
- **Short.** No cinematic over 3 minutes; 18 cinematics, ~24 minutes total.

## 19.2 Camera language
| Mode | Used for | Rules |
|---|---|---|
| **Player eyes** | Gameplay, in-engine scenes | Subtle helmet frame in suits; no forced head-turns (a soft "look-at" hint instead) |
| **Documentary** | Crane's broadcasts, Directorate footage | Locked-off, clean, symmetrical: cold power |
| **Handheld** | Ada's cockpit, Directorate raids | Close, anxious, shallow focus |
| **Cosmic** | Seedship, jumps, Wonders | Long lenses, slow moves, enormous scale |

## 19.3 Cinematic list

| # | Mission | Title | Length | Content |
|---|---|---|---|---|
| C01 | Cold Open | "Contact" | 0:40 | Styx's surface ripples; Crane's hand on your shoulder |
| C02 | M0.03 | "The Ramp" | 1:10 | Ada's cockpit: Crane's order, her face, the ramp closing |
| C03 | M0.03 | "Night Zero" (title) | 0:50 | The ark fleet rising over a burning spaceport; title card |
| C04 | M1.04 | "Coral" | 0:45 | The Vault Bloom Heart revealed |
| C05 | M1.07 | "It's Writing" | 0:50 | The glyph across Earth from orbit |
| C06 | M2.01 | "Haven" | 1:00 | First sight of Haven-9, tumbling and dark |
| C07 | M2.06 | "The Director" | 2:10 | Crane's broadcast; the bonsai |
| C08 | M2.07 | "The Map" | 1:30 | The Jump Core's star map blooms; Ada and Wrench inside it |
| C09 | M3.01 | "First Leap" | 1:00 | The first jump; the first alien sky |
| C10 | M3.03 | "The Gardener's Memory" | 1:40 | A Sower vision of gardening Veyra |
| C11 | M3.04 | "Sung Before" | 1:20 | Sable shows Earth's glyph in the archive |
| C12 | M3.05 | "Hands Up" | 1:30 | Lily walks out to Ada — in-engine, staged procedurally inside *your* base (see [18 §18.6](18-mission-design-documents.md)) |
| C13 | M3.07 | "The Great Dying" | 2:30 | The Eden Room: Permian Earth, the first harvest, the mark |
| C14 | M3.08 | "Anthesis" | 1:40 | The Seedship through the Gate |
| C15 | M4.02 | "Sorry" | 1:00 | Lily hears the Permian fossil |
| C16 | M4.03 | "Blood" | 1:30 | Ada's resolution (two versions) |
| C17 | M4.05 | "The Weaver" | 2:00 | The Weaver enters the Loom (6 versions) |
| C18 | M4.06 | "Sunday" | 2:00 | The last Sunday dinner; "So… what do we build next?" |

## 19.4 The "trailer moments" (the ten images that sell the game)
1. **The flinch:** Styx's surface rippling under the drill.
2. **Dana Marsh knocking** three times on the hangar glass.
3. **The skywalk collapse** in Terminal B, the crowd falling into the dark.
4. **Ada's ramp closing** with the crowd and her sibling beyond the fence.
5. **Earth with the glyph** — green veins forming a spiral across continents.
6. **Haven-9 at dawn**, the Earth-glow, survivors eating at a long table by the window.
7. **A player-built ship** lifting off from a purple sea past Tessari herds.
8. **Lily's raised hands** in a corridor full of smoke.
9. ***Anthesis* unfolding** petal-sails wider than a planet.
10. **The bonsai** in the Loom mind-space, a city going dark with each cut.

## 19.5 Reveal trailer script (2:00)

| Time | Picture | Sound |
|---|---|---|
| 0:00 | Black. A grainy Persephone camera feed; a drill touching a rock surface. | Mission control chatter, a countdown. |
| 0:08 | The surface **flinches.** | Silence. One soft radio pulse. |
| 0:12 | Kestrel spaceport at night. A hangar. Hands tuning a spacecraft. | Ada (V.O., warm): *"Sunday dinner. You're cooking, I'm eating."* |
| 0:20 | A guard waves through a window. Lights flicker. | KESTREL: *"Code Black."* |
| 0:24 | Rapid cuts: dark corridors, knocking on glass, a wrench raised. | The five-note Verdance motif in the Hollow clicks. |
| 0:34 | Terminal B chaos; the skywalk collapsing. | Rising strings. |
| 0:42 | Pad 12. The *Seraph*'s ramp closing. Ada's face. | Ada: *"Wrench, I'll come back for you. I swear it."* |
| 0:50 | The ark fleet rising over a burning spaceport. | Music drops out. Tug: *"They knew."* |
| 0:55 | **Hard cut:** welding sparks. Walls going up. A horde hitting a wall that holds. | The main theme begins: percussion. |
| 1:05 | A rocket built from salvage, launching. Earth from orbit; the glyph. | KESTREL: *"It's… writing."* |
| 1:12 | Montage: zero-G building, a colony dinner, a lander touching down on the Moon, a first jump, alien skies, a jungle world, ice, a Directorate cruiser breaking apart. | The theme at full orchestra and choir. |
| 1:35 | Lily, in a corridor full of smoke, raising her hands. | Music cuts. Lily: *"She said that to you too, didn't she?"* |
| 1:42 | *Anthesis* unfolding through the Gate. | One enormous low note. |
| 1:48 | Title: **EXODUS PROTOCOL** | Crane (V.O.): *"I didn't end the world. I simply refused to go down with it."* |
| 1:55 | *"Build your way out."* Platforms, date. | The five-note motif, alone. |

## 19.6 Key art brief
- **Composition:** split frame. Bottom half: a burning Earth spaceport at night, a lone figure holding a wrench, silhouetted against floodlights, Hollows at the fence. Top half: the same figure's reflection in a helmet visor, showing a player-built ship over an alien world under a violet sky, with *Anthesis* on the horizon.
- **Palette:** sodium orange below, teal and violet above, and a thin green vein of Bloom crossing the boundary between them.
- **Tagline:** *"We brought it home. Now we build our way out."*
