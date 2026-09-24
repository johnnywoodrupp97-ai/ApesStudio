# 18 — Mission Design Documents (Flagship Missions)

> Mission design documents (MDDs) for the eight missions that define the game's quality bar. Every other mission uses the same template (§18.0). Timings are for a story-following player on Normal.

## 18.0 MDD template
1. **Overview** — ID, act, location, length, pillars served, prerequisites, unlocks
2. **Player goals** — what the player is trying to do, in their own words
3. **Layout** — top-down sketch of the space
4. **Beat flow** — numbered beats with target times
5. **Encounters** — enemies, counts, placement intent
6. **Systems exercised** — which game systems the mission tests
7. **Checkpoints & failure** — what happens when the player dies or fails
8. **Reactivity** — flags read and written
9. **Audio & music cues**
10. **Telemetry** — what we measure
11. **Scope** — unique assets needed

---

## 18.1 `M0.03` — "The Promise"

| | |
|---|---|
| **Act / location** | Prologue · Kestrel Terminal B → Pad 12 → Hangar 4 roof |
| **Length** | 10 min |
| **Pillars** | Fear on the ground; A mystery worth crossing the galaxy for (Strand C inciting incident) |
| **Prerequisites** | M0.02 |
| **Unlocks** | Title card; Act I; the open valley |

**Player goals:** *"Get Tug to Pad 12 before Ada has to leave."*

**Layout:**
```
 HANGAR 4 ──service road── TERMINAL B (concourse → gates → skywalk) ──apron── PAD 12 FENCE ── [SERAPH]
    ▲                          │  crowd crush   │ skywalk collapse  │ fuel-truck blast
    └──────── retreat path (burning apron, Hollows closing) ◀──────────────┘
```

**Beat flow:**
1. **0:00** Ada's call. A countdown appears on the wrist pad: *"Seraph departure: 6:00."* (The timer is fake: the shuttle leaves when the player reaches the fence, whatever the clock says.)
2. **0:45** The concourse: a panicking crowd. Hollows *inside* the crowd. The player carries Tug (slow; can't fight while carrying; can set him down).
3. **2:30** Gates: Directorate barricade. A trooper refuses entry; you must route through baggage handling (short stealth section).
4. **4:30** **Skywalk collapse**, scripted physics: the glass floor fails under the crowd. The player falls a floor with debris, lands in the baggage hall.
5. **6:00** The apron: a fuel truck, hit by a panicked car, explodes. The shockwave knocks the player down (controller rumble peak). Hollows set alight keep coming.
6. **7:30** **Pad 12 fence standoff:** a playable in-engine scene. Troopers aim at the crowd. Ada and Crane on the radio. The player can shout (a dialogue choice) but can't change the outcome.
7. **8:30** The ramp closes. *"I'll come back for you."* Exhaust wash scatters everyone. Tug drags you up.
8. **9:00** Hangar 4: weld the doors under pressure (first build; the doors buckle until finished).
9. **9:40** The roof. Ark ships rising. Tug's line. **Title card.**

**Encounters:** Terminal B — 12 Shamblers mixed into ~80 civilian NPCs (crowd sim); Apron — 6 burning Shamblers; Hangar doors — scripted horde pressure.

**Systems exercised:** carrying, crowd AI, physics destruction, first block placement and welding, infection (a second scratch is possible; Suppressant from a first-aid box).

**Checkpoints & failure:** checkpoints at the concourse, baggage hall, and apron. Death restarts from the last checkpoint with Tug nearby. The fence scene can't be failed.

**Reactivity:** writes `pad12_choice` (shout for Ada / shout at Crane / silent), referenced in Ada's M2.04 message.

**Audio & music:** Terminal: alarms, PA looping evacuation messages in four languages. Standoff: music drops out entirely; only radio and wind. Title card: the first statement of the main theme.

**Telemetry:** time per section; deaths per section; % who set Tug down; `pad12_choice` distribution.

**Scope:** Terminal B (hero interior), crowd-sim tech, skywalk destruction, Seraph shuttle (hero asset), Ada and Crane VO, 1 short cinematic (ramp close).

---

## 18.2 `M1.02` — "The Girl in the Walls"

| | |
|---|---|
| **Act / location** | Act I · Kestrel Township → Kestrel Elementary |
| **Length** | 25 min (plus optional Township exploration) |
| **Pillars** | People, not resources; Fear on the ground |
| **Prerequisites** | M1.01 (distress call lead) |
| **Unlocks** | Lily; colony needs; campfire scenes |

**Player goals:** *"Someone's alive in the school. Get them out."*

**Layout:**
```
 SCHOOL (2 floors)
 ┌───────────┬───────────┬────────────┐
 │ Classrooms│  Library  │  Office    │  1F: Ms. Alvarez at the whiteboard (turned)
 ├───────────┴─────┬─────┴────────────┤
 │    Hallways     │    Cafeteria     │  Vent network runs above everything
 ├─────────────────┴──────────────────┤
 │               GYM                  │  Set piece: horde + sprinklers
 └────────────────────────────────────┘
```

**Beat flow:**
1. **0:00** Township approach; the looping teacher message gets louder on the radio as you get closer.
2. **4:00** Enter the school. Kids' drawings, barricaded doors, a trail of juice boxes. (Environmental story: the teacher kept them together for days.)
3. **8:00** Ms. Alvarez: turned, standing at the whiteboard, marker in hand. The whiteboard reads *"We are brave. Help is coming."*
4. **10:00** A small voice from the vent grille: *"Are you real?"* Lily won't come out. She guides you instead.
5. **12:00** **The vent guide sequence:** Lily moves through the vents (you hear her above; she whispers directions). You move below through Hollow-filled halls. Her spiral drawings appear on vent grilles to mark the route.
6. **18:00** **The gym:** a horde fills it. Lily: *"The fire alarm! Pull it!"* The sprinklers and alarm split the horde toward the noise. Escape through the equipment room.
7. **22:00** Lily drops down from the last vent. She shows you the healed bite without being asked.
8. **24:00** Back at base: the campfire scene. *"Are they sad?"*

**Encounters:** 18 Shamblers, 4 Crawlers (in lower vents and under bleachers), 1 Runner pack (3) at the exit.

**Systems exercised:** noise/distraction, stealth, survivor needs (Lily gets hungry on the trip back), rover not yet available.

**Reactivity:** reads `pad12_choice` (Lily asks who you were shouting at if you shouted); writes `lily_trust_start` (+ if you let her lead, − if you forced the vent open).

**Audio & music:** the school is almost silent; Lily's whisper is binaural. The sprinklers bring a musical release.

**Telemetry:** time in the vent sequence; % who pull the alarm before prompted; deaths in the gym.

**Scope:** school interior (hero), Lily vent traversal animations, sprinkler VFX, drawing decals (spiral glyph).

---

## 18.3 `M1.06` — "The Long Night"

| | |
|---|---|
| **Act / location** | Act I · The player's base + Pad 39-K fuel line |
| **Length** | 13 min of siege (plus preparation time chosen by the player) |
| **Pillars** | Build what saves you |
| **Prerequisites** | All four *Wren* parts |
| **Unlocks** | M1.07 |

**Player goals:** *"Hold until the Wren's tanks are full."*

**Design:** the first **real test of the player's own base.** The mission starts only when the player presses *"Begin engine test"* at the pad, so they can prepare as long as they want. KESTREL shows the predicted horde size from the base's Attraction score.

**Beat flow:**
1. **Preparation (player-paced):** a readiness screen lists wall strength, turret coverage, ammo, lighting and armed survivors.
2. **0:00** Engine test. The valley lights up. A fueling progress bar appears (13 minutes).
3. **0:00–4:00** Wave 1: Shamblers and Runners from three directions.
4. **4:00–8:00** Wave 2: **Brutes** go for the weakest load-bearing blocks (shown on the Structural View). Screamers call reinforcements.
5. **~7:00** **Lily's valve moment** (scripted in-engine; the player keeps control and can watch or keep fighting).
6. **8:00–13:00** Wave 3: everything, plus Bloaters on the fuel line. If the fuel line breaks, fueling pauses until it's repaired.
7. **13:00** Tanks full. Dawn breaks; the surviving Hollows retreat from the light.

**Encounters (Normal, typical Attraction):** ~140 Hollows total; 4 Brutes; 3 Screamers; 6 Bloaters.

**Checkpoints & failure:** failure = the pad's fuel line destroyed for 60 continuous seconds, or the player's main base breached with survivors killed. On failure, restart at the preparation phase **with everything you built kept**.

**Reactivity:** writes `long_night_losses`; survivors who fought get *Our home held* (+12 mood) or *We lost people* moodlets.

**Telemetry:** preparation time; turret count; failure causes; % who build the automated clamp release (feeds `tug_survived`).

**Scope:** horde tech at 140+ agents, a Structural View readability pass, Lily gantry animation.

---

## 18.4 `M1.07` — "Liftoff"

| | |
|---|---|
| **Act / location** | Act I → orbit |
| **Length** | 12 min |
| **Pillars** | Build what saves you; Fear on the ground, wonder in the sky |
| **Unlocks** | Act II; Earth orbit |

**Beat flow:**
1. **Cargo triage:** a physical loading puzzle. Crates must fit the *Wren*'s cargo bay, and mass affects the launch.
2. **Countdown:** Hollows breach the pad perimeter. Survivors board while you cover them.
3. **Clamp jam:** if no automated release was built, Tug stays. The player *can* try to go back; the game lets them get halfway before Tug's line stops them. (We never take control away; we make the choice obvious.)
4. **Playable ascent:** throttle, staging, a failing engine (manually cut it, rebalance thrust). A cockpit view with Earth curving away.
5. **Orbit:** silence. The glyph across Earth. KESTREL's line; Lily's line. Fade.

**Failure:** a failed ascent restarts at the countdown. Cargo choices persist.
**Telemetry:** cargo choices; % Tug survived; ascent attempts.
**Scope:** *Wren* cockpit (hero), launch VFX, Earth-from-orbit glyph (hero matte and real-time), 1 cinematic (the glyph reveal, 50 seconds).

---

## 18.5 `M2.04` — "The Far Side" (Tycho)

| | |
|---|---|
| **Act / location** | Act II · Haven-9 → Moon → Tycho Outpost |
| **Length** | 40 min (including ship building) |
| **Pillars** | Build what saves you; Go anywhere |
| **Unlocks** | He-3 fusion; the Styx archive; the whole Moon as an open frontier |

**Player goals:** *"Build a ship that can land on the Moon and come back, then get what Ada said was there."*

**Beat flow:**
1. Ada's message (in-engine, at the station's comms console).
2. **Ship build:** functional requirements (TWR ≥ 1.5 at 0.16 g, 10 minutes of O₂, landing gear). A story blueprint is available on the projector.
3. Transit and landing (manual, or autopilot once KESTREL has a landing beacon).
4. **Tycho exterior:** dust storm, Burrowers under the regolith (seismic tells), infected miners in EVA suits.
5. **Tycho interior:** three decks. Restore partial power to reach the archive vault. Low-G melee is floaty and heavy.
6. Recover the He-3 core (heavy; it must be carried or winched onto the ship — an engineering mini-puzzle).
7. Return. Ada's second message: *"Don't answer."*

**Reactivity:** writes `ada_bond` (+5 for replying, +0 for silence, −5 for a hostile reply) and `crane_tracking = true`.
**Telemetry:** custom vs. blueprint lander; number of landing attempts; time to recover the core.

---

## 18.6 `M3.05` — "The Taking" (systemic raid)

| | |
|---|---|
| **Act / location** | Act III · Wherever the colony lives (Haven-9, the capital ship, or an outpost) |
| **Length** | 15–20 min |
| **Pillars** | Build what saves you; People, not resources |
| **Trigger** | *Systemic:* the next time the player arrives home after completing the second Key, never mid-mission |
| **Unlocks** | M3.06 |

**The design promise:** *the raid is fought against the base you actually built.* No authored "safe" layout. This is where Pillar 1 and Pillar 2 collide.

**How it works:**
1. **Raid planner (AI):** the Directorate AI reads your base: entrances, airlocks, hull thickness, turret coverage, the rooms where named characters are assigned.
2. **Breach points:** it picks 2–4 breach points (weak hull sections, docking ports, hangar doors), with preference toward the rooms containing Lily, Mara and Tug.
3. **Squads:** 4–6 Directorate squads (troopers, an enforcer, a medic, drones), scaled by difficulty and your defense rating.
4. **Named-character risk:**
   - Each named character in the raid has a **Peril meter.** It rises while hostiles occupy their room and falls with nearby defenses (turrets, sealed doors, armed survivors, the player's presence).
   - A full Peril meter means that character is **killed** (Tug), **exposed** (Mara, always exposed at minimum), or **wounded** (others).
   - Generic survivors can die as normal colonists.
5. **Lily's surrender:** at 6 minutes, or when the first named character's Peril passes 75%, whichever comes first, Lily leaves her hiding place and walks to Ada. The player sees it on the nearest screen or in person. The fighting stops.
6. **Withdrawal:** the Directorate leaves with Lily. Casualties are counted.

**What good engineering buys:** strong design can keep everyone alive except Mara's exposure and Lily's surrender. That's the authored cost. Weak design can lose Tug and several colonists.

**Checkpoints & failure:** the mission **can't be failed**; the outcome varies. The player dying sends them to the Med-Pod and the raid continues (and hurts more).

**Reactivity:** writes `taking_casualties`, `tug_alive`, `mara_exposed`, and `ada_bond` (± by whether the player fought Ada directly).

**Audio & music:** station alarms, Directorate comm chatter the player can hear (and learn from), the Verdance motif absent. Music cuts to a single sustained note when Lily walks out.

**Telemetry:** casualties by base-defense rating; time to Lily's surrender; how many players reload a save (we accept some; we want the outcome to feel fair).

**Scope:** raid planner AI (major system), breach VFX for any hull, Directorate squads, Ada/Lily in-engine scene that must work in *any* player-built room (procedural staging: find a clear 6 m path, align actors, fallback to a comms-screen version).

---

## 18.7 `M3.07` — "Key of Iron" (Ark Meridian)

| | |
|---|---|
| **Act / location** | Act III · Meridian system → Ark Meridian |
| **Length** | 40 min |
| **Pillars** | A mystery worth crossing the galaxy for; Build what saves you |
| **Unlocks** | The third Key; `ada_state`; M3.08 |

**Structure — a heist in three phases (player picks the approach):**

| Phase | Loud approach | Quiet approach |
|---|---|---|
| **1. Get aboard** | Ship combat vs. an escort, then a breaching drill | Pose as a Hauler cargo run (needs Hauler rep ≥ 30 or a stolen transponder) |
| **2. Reach the labs** | Fight through the hangar and security deck | Maintenance crawlspaces, disabled cameras, disguises |
| **3. Get out** | Escape by force | Escape in Ada's shuttle (if she defects) |

**Key scenes:**
- **The Eden Room:** a vast holo-archive. Crane's research, the Great Dying reconstruction, the mark. Mara (or Idris) narrates; KESTREL decodes.
- **The Lab:** Null-carrier prisoners in pods; Lily in the last one, drawing spirals on the glass.
- **The Standoff:** Ada, Wrench and Idris. `ada_bond` decides the version; Idris's trigger is the player's choice (an interrupt prompt).

**Encounters:** 30–60 Directorate enemies depending on approach; 1 Enforcer mini-boss squad; drone swarms.
**Reactivity:** reads `idris_saved`, `ada_bond`, Hauler rep, `crane_stance`; writes `ada_state`, `meridian_approach`, `null_prisoners_freed`.
**Scope:** Meridian interior (hero, three decks), the Eden Room (hero set, holographic Permian Earth), the lab (hero).

---

## 18.8 `M4.04` — "Crane" (final boss)

| | |
|---|---|
| **Act / location** | Act IV · The Loom chamber → Loom mind-space |
| **Length** | 20–25 min |
| **Pillars** | A mystery worth crossing the galaxy for |

| Phase | Arena | Crane's kit | Player counter-play | Talk-down window |
|---|---|---|---|---|
| **1 — The Director** | The Loom chamber: tiered, organic, with cover | Augmented armor, 4 drones, shock mines, calls in troopers | EMP the drones; flank; use the Loom's pulsing vents as cover | — |
| **2 — The Graft** | The chamber *grows*: Bloom walls move, floors open | Tendril sweeps, spore bursts, summons Hollows from the walls | Fire damage on graft nodes; fight while the arena changes shape | — |
| **3 — The Bonsai** | Mind-space: a colossal bonsai; branches are platforms | Prunes branches away from under you; each cut, a city on Earth goes dark (visible below) | Race along branches; strike his shears; protect the branches that hold cities | **Yes** — needs `crane_stance` ≠ defiant and his 6 logs |

**Talk-down:** mid-phase 3, a dialogue interrupt. Using Elena's name (from his logs) and the bonsai ("You kept it alive for ninety years. That's not pruning. That's *tending.*"), the player can end the fight. Crane stays lucid and can become the Weaver.

**Failure:** checkpoints at the start of each phase.
**Scope:** 3 arenas (1 physical, 1 transforming, 1 mind-space), Crane's 3 forms, the bonsai (hero), the Earth-below matte.
