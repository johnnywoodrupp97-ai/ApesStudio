# 12 — Art, Audio & UI

## 12.1 Visual direction

**Keywords:** *Worn industrial · NASA-punk · bioluminescent rot · vast and lonely*

| Region | Palette | Lighting | Reference mood |
|---|---|---|---|
| **Earth (Act I)** | Sodium orange, smoke grey, emergency red | Flashlight, fires, floodlights; night-heavy | *The Last of Us*, *Alien: Isolation* |
| **Orbit (Act II)** | Cold white, steel blue, warm habitat amber | Harsh sunlight vs. deep shadow; Earth glow | *Gravity*, *The Expanse* |
| **The Drift (Act III)** | Saturated alien palettes per planet; teal Sower accents | Multiple suns, auroras, nebula skies | *No Man's Sky*, *Annihilation* |
| **Seedship (Act IV)** | Deep violet, living green, pearl white | Bioluminescence, pulsing organic light | *Prometheus*, *Scavengers Reign* |

### The Verdance look
- Starts as **green veining** and **lichen-like crust**, progresses to **fleshy fungal plates**, then **flowering growths** with teal bioluminescent spores.
- **Beautiful and wrong:** the Bloom should be pretty from a distance and horrifying up close.

### Human tech
- Chunky, modular, labelled, scuffed. Stencilled warnings, duct tape, cable runs.
- **Faction reads:** Survivors = mismatched & patched; Directorate = white/gold, clean lines; Choir = cloth, moss & candles; Haulers = graffiti & cargo orange.

### Sower tech
- Grown, ribbed, coral and seashell forms; no right angles; glyphs glow teal; surfaces "breathe."

### Characters
- Semi-realistic, readable silhouettes. Survivors show wear over time (dirt, bandages, haircuts grown out) and change clothes based on colony wardrobe.

## 12.2 Audio direction

- **Hollows:** layered human breath + wet fungal textures + distant radio-like clicks. Each variant has a signature tell (Screamer's inhale, Bloater's gurgle, Runner's footfalls).
- **Space:** near-silence outside; sound transmitted through the suit and hull contact (muffled, bassy). Inside pressurized rooms, full sound.
- **Machines:** every block type has an audio identity so players can *hear* problems (sputtering generator, hissing leak, overheating reactor).
- **Colony ambience:** layered chatter, cooking, laughter, music from rec rooms — the colony should *sound* alive; silence is a warning.

### Music
- **Act I:** sparse synth drones, heartbeat percussion, dissonant strings during hordes.
- **Act II:** hopeful piano and acoustic guitar themes in the colony; ambient pads in space.
- **Act III:** expansive, planet-specific motifs; the "Drift theme" (analog synth arpeggios + choir).
- **Act IV:** the **Verdance motif** (a 5-note phrase heard in Hollows' clicks since Act I) blooms into a full orchestral/choral piece.
- **Diegetic music:** survivors play instruments; radios play pre-outbreak songs.
- **Adaptive system:** layered stems react to threat level, location and colony morale.

### Leitmotifs
| Theme | Instrumentation | Where it lives |
|---|---|---|
| **Main theme — "Build Your Way Out"** | Low brass, taiko, rising strings | Title card, Liftoff, Convergence |
| **"Sunday"** (the Okafor family) | Solo kora and acoustic guitar | Ada's calls, Sunday dinners, M4.03, the final scene |
| **The Verdance motif** | Five notes; first heard in Hollow clicks, later full choir | Hollows, Sower ruins, the Loom |
| **"The Director"** | Cold, perfect string quartet | Crane's broadcasts; inverted and distorted in the boss fight |
| **"Lily"** | Music box and celesta | Lily's scenes; it gains an orchestra as she grows |
| **"The Drift"** | Analog synth arpeggios and choir | Free exploration in space |

### Voice
- ~15,000 lines at launch (companions, antagonists, KESTREL, 12 notable survivors, barks for procedural survivors).
- Procedural survivors use **bark sets** (8 voice types × 3 moods).

## 12.3 UI / UX

### HUD (diegetic-first)
- Vitals projected on the **suit helmet visor** (KESTREL overlay). Minimal by default; expands when values are critical.
- **Infection** shown as green veining creeping in from the screen edge plus a meter.
- Building UI: radial block menu + hotbar; ghost preview with fit colors (green valid, red blocked, yellow unsupported).
- Compass with POI and signal markers; no minimap on planets (preserve exploration).

### Key screens
| Screen | Purpose |
|---|---|
| **Terminal / Control Panel** | Manage any block on a grid (power, doors, turrets, production queues) |
| **Colony Overlay** | Top-down/isometric station view: survivors, rooms, jobs, schedules, needs, relationships graph |
| **Survivor Card** | Portrait, needs bars, mood + moodlets, traits, skills, relationships, history |
| **Research Web** | Tech tree with branches and costs |
| **Galaxy Map** | Jump lanes, factions, Bloom spread, missions |
| **Codex** | Lore, glyphs, species, logs, characters |
| **Blueprint Library** | Saved/story/community blueprints |

### Accessibility (launch requirements)
- Full remapping (keyboard/mouse & controller); hold/toggle options.
- Subtitles with speaker names, size & background options; captions for important sounds (e.g., "[Screamer inhales]").
- Colorblind modes (Bloom/infection also readable by pattern/shape, not just green).
- **Arachnophobia-style toggle for body horror** (reduces gore and fungal detail).
- Motion sickness options: FOV slider, head-bob off, zero-G horizon lock.
- Difficulty customization per system (see [10](10-progression-and-economy.md)); **"Builder's Peace"** mode disables hordes entirely.
- Pause anywhere in single-player.
