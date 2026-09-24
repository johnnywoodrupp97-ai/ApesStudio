# 03 — Storyline

> Campaign target: **~12 hours** critical path. Mission IDs (e.g. `M1.03`) match the data files described in [13 — Technical Architecture](13-technical-architecture.md) so writers and designers share one vocabulary.

## 3.1 Story overview

**Premise:** On the night a sample from an interstellar object escapes its lab, a spaceport engineer must lead a handful of survivors off a dying Earth, build a home in orbit, and follow the plague's trail across the stars to its source.

**Theme:** *What do we owe each other at the end of the world?* Every act asks it at a larger scale — a person (Act I), a community (Act II), a species (Act III), all life (Act IV).

**Structure:**

| Act | Title | Setting | Playtime | Player fantasy |
|---|---|---|---|---|
| Prologue | Night Zero | Kestrel Complex | 0:00–0:25 | Survive |
| I | Outbreak | Kestrel Complex & Township | 0:25–2:45 | Protect |
| II | Haven | Orbit & Moon | 2:45–5:30 | Rebuild |
| III | The Drift | Procedural star systems | 5:30–9:30 | Discover |
| IV | Seedfall | The Seedship *Anthesis* | 9:30–12:00 | Decide |
| Epilogue | New Dawn | Varies by ending | — | Continue (sandbox) |

---

## 3.2 Prologue — "Night Zero" (0:00–0:25)

**Cold open.** Black screen. A radio chatter montage: a mission controller celebrating Persephone's landing three weeks earlier, then a news anchor mentioning "an incident at a Nevada research facility," then static.

### `M0.01` — "Last Shift"
- **Player:** The Engineer (customizable; default name **Ren Okafor**), a systems engineer working late in Hangar 4, fine-tuning the guidance computer of the crew vehicle *Wren*.
- **Gameplay:** Tutorial for movement, interaction, the **multitool** (grind/weld/scan). Repair a fuse box to restore hangar lights. Chat with mechanic **Tobias "Tug" Brennan** over the radio.
- **Beat:** Lights flicker. KESTREL, the facility AI, announces a *Code Black — Biological*. Blast doors seal. Tug's radio feed cuts to screaming.

### `M0.02` — "Code Black"
- **Gameplay:** Navigate darkened service corridors to reach Tug. First Hollow encounter — a security guard, slow and wrong. The player has only a wrench. Teaches stealth (crouching, noise meter) and melee.
- **Beat:** The Engineer is **scratched** during a struggle. HUD introduces the **Infection meter**. KESTREL guides them to a medical cabinet: first **Suppressant** injection. (Establishes the partial-resistance thread.)
- **Beat:** Find Tug pinned under a forklift, fighting off a Hollow. Save him (QTE-free — physics: use the forklift controls to lift the load).

### `M0.03` — "Get to the Hangar"
- Tug and the Engineer fight back to Hangar 4. Seal it using the multitool to weld the doors. **First building tutorial:** place steel plates over a broken window.
- **End of prologue:** From the hangar roof, they watch the Complex burn and a fleet of white Ark shuttles lift off into the night — leaving everyone behind.
  > **Tug:** "They had rockets fueled and waiting. They *knew.*"

---

## 3.3 Act I — "Outbreak" (0:25–2:45)

**Goal:** Turn Hangar 4 into a fortified base, gather survivors and parts, and launch the *Wren* to orbit.
**Tone:** Tense, claustrophobic survival horror with moments of warmth.
**New systems introduced:** base building, power, crafting, survivor needs, horde nights, scavenging runs, vehicles (rover).

### `M1.01` — "Four Walls" (Base building)
- Build the first **Workbench**, **Generator** and **Floodlights**. Craft a nail-gun rifle.
- First **Horde Night** tutorial: small wave at dusk. Walls take damage; teaches repair.

### `M1.02` — "Voices on the Band" (Rescue)
- KESTREL's comm array picks up a distress call from **Kestrel Elementary**, where a teacher sheltered children.
- Scavenging run into the Township by foot. The school is overrun; only one child is alive: **Lily Chen**, 11, hiding in the ventilation ducts. She was bitten days ago — and never turned.
- **Colony sim intro:** Lily joins the hangar. Introduces **needs** (hunger, sleep, comfort, safety) and the **bed/food/room** basics.

### `M1.03` — "The Soldier" (Recruitment)
- A wounded Ark security officer, **Sgt. Idris Kaan**, is found at a crashed Ark transport. He was abandoned too.
- **Choice:** Heal him (cost: rare medkit) or leave him. If healed, he becomes a companion and combat trainer; if left, he appears later in Act III as a Directorate enforcer who remembers.

### `M1.04` — "The Scientist" (Descent into the Vault)
- Survivors' radio picks up a looping message from **Dr. Mara Voss**, trapped in the Vault lab beneath the Complex.
- A horror-centric dungeon: flooded sub-levels, the first **Bloom Heart** growing out of the containment chamber, a **Screamer** enemy.
- Mara is rescued. She confesses: the Persephone sample caused this, and Crane forced the testing.
- **Key item:** The **Persephone Drive** — Mara's research data, including Styx telemetry.

### `M1.05` — "Parts List" (Open-zone objectives, any order)
The *Wren* needs four systems. The player picks the order; each is a mini-region with its own threat:

| Part | Location | Threat/Twist |
|---|---|---|
| **Guidance Computer** | Mission Control tower | Must restore power across three substations — power grid puzzle |
| **Fuel (LOX + methane)** | Fuel Farm | Explosive environment; guns are risky; Bloaters |
| **Heat Shield Tiles** | Kestrel Township warehouse | Rover driving; Runner packs in the open |
| **Life Support Module** | Crashed Ark shuttle | Directorate drones guarding it — first human-tech enemies |

- Survivors can be assigned to support: Tug speeds up rover repair; Idris escorts; Mara crafts medicine.
- More generic survivors (2–4) can be found and recruited during these runs (colony grows to 6–8).

### `M1.06` — "The Long Night" (Siege)
- Final and largest Horde Night, triggered by the *Wren*'s engine test drawing every Hollow in the valley.
- **Brute** enemy introduced. The player must defend the hangar *and* Pad 39-K's fuel line simultaneously — trains multi-front defense and turrets.

### `M1.07` — "Liftoff" (Act I climax)
- Load survivors and cargo (capacity puzzle: choose what comes — seeds, tools, medicine, weapons; affects early Act II).
- A playable launch: the player manages throttle, staging and a failing engine in real time while Hollows swarm the pad.
- **Beat:** Tug stays behind to manually release the tower clamps — unless the player built an automated clamp release earlier (hidden engineering solution; Tug survives).
  > **Tug (if he stays):** "Don't you dare turn this thing around. Go."
- **Image:** Earth receding. Green veins visible across continents from orbit.

---

## 3.4 Act II — "Haven" (2:45–5:30)

**Goal:** Restore a derelict station into a working colony, secure resources from the Moon, and discover the truth of Styx.
**Tone:** Hope and hard work; the first "Sims" hours. Horror returns in bursts.
**New systems:** zero-G movement & building, pressurization, oxygen/CO₂, hydroponics, life-sim depth (jobs, relationships, mood), ship building (small grid), mining, research.

### `M2.01` — "Dead Air" (Docking)
- *Wren* is failing. KESTREL (now uploaded to the ship) finds **Haven-9**, a derelict research station.
- **Zero-G tutorial:** EVA across the hull to manually open the docking port.
- Inside: dark, frozen, drifting bodies. Two are Hollows (**Drifters** — zero-G infected).

### `M2.02` — "Breathe" (Restore life support)
- Restore **power** (solar arrays), **oxygen** (electrolysis), **pressure** (seal hull breaches), **heat**.
- The player chooses which module to restore first. Survivors wait in the *Wren* with a ticking O₂ timer — tension without being punishing.

### `M2.03` — "Home Is Where We Build It" (Colony sandbox opens)
- The **Colony Management overlay** unlocks: assign jobs, set schedules, zone rooms.
- **Objectives (soft):** build sleeping quarters, a mess hall, hydroponics, a medbay. Raise colony morale to "Stable."
- **First relationship events** fire (e.g., Idris and Mara clash over whether to trust the Directorate).
- A memorial wall for the dead auto-appears — players can add names of lost survivors.

### `M2.04` — "Signal from Tycho" (Moon expedition)
- Station scanners catch a signal from **Tycho Outpost** on the Moon.
- The player must **build their first ship** — a small-grid lander — from blueprints or free design. It must meet thrust-to-weight requirements for lunar gravity.
- Tycho is overrun by infected miners in EVA suits. Low-gravity combat; dust storms.
- **Recover:** helium-3 reactor core (unlocks large power), titanium, and the **Styx Telemetry Archive**.

### `M2.05` — "Patient Zero" (Station-side crisis)
- An infected survivor who hid their bite turns inside Haven-9 while the player is away. The station alerts the player, who must fly back.
- Teaches **internal outbreak mechanics**: isolate modules, vent atmosphere, quarantine.
- **Moral beat:** a second survivor is infected but still in Stage 2. Options: quarantine and treat (uses precious resources), exile to an escape pod, or — if the player has Mara's trust — experimental treatment using Lily's blood.
- **Lily reveal:** Mara confirms Lily is a **Null carrier**. Lily's safety becomes a story priority (and a Directorate target).

### `M2.06` — "The Rock That Sang" (Revelation)
- Decrypting the Styx archive with Mara and KESTREL reveals Styx is **artificial and hollow**, and still transmitting — and that the Persephone sample was a "seed."
- A **Directorate transmission** interrupts: **Director Crane** addresses the station. He knows about Lily. He offers safety for everyone in exchange for her.
- **Choice (tone, not branch):** defiant, negotiating, or silent. Crane's later dialogue references it.

### `M2.07` — "Into the Seed" (Act II climax)
- Build or upgrade a ship capable of reaching Styx (fuel range, radiation shielding).
- Explore the **Styx Wreck**: first Sower architecture. Low gravity, bioluminescent corridors, puzzles using Sower glyphs.
- Directorate forces arrive simultaneously — three-way fight between the player, Ark troopers and Styx's Hollow guardians.
- **Climax:** At the core, the player finds a **Sower Jump Core**. Activating it shows a star map — dozens of systems lit up and one pulsing beacon: the source.
- The Directorate retreats — but Crane learns of the Jump Core.
  > **Mara:** "It wasn't an asteroid. It was a *seed pod.* And somewhere out there is the tree."

---

## 3.5 Act III — "The Drift" (5:30–9:30)

**Goal:** Install the Jump Core, travel the Drift, gather three **Resonance Keys** to locate the Seedship, and choose allies.
**Tone:** Wonder, freedom, dread; the "No Man's Sky" hours.
**New systems:** large-grid capital ship building, jump travel, procedural planets, faction reputation & trade, ship combat, planetary outposts, crew assignment aboard ships.

### `M3.01` — "Leap of Faith"
- Install the Jump Core into a new **large-grid ship** — the player's mobile base (default name *Second Chance*, renameable). Must provide power, cooling and structural mounting.
- First jump. Sequence: silence, light, and the first alien sky.
- **The Drift opens.** Procedural systems are available; three **Anchor Systems** hold Resonance Keys (any order).

### `M3.02` — "Tortuga Drift" (Hub & Free Haulers)
- The first jump drops the player near **Tortuga Drift**, the Free Hauler ship-city. Trade hub, contracts board, crew recruitment.
- **Captain Oye Adeyemi** offers the location of a Resonance Key in exchange for a favor.

### The Three Keys (non-linear, ~1 hour each)

#### `M3.03` — "Key of Roots" — the jungle world **Veyra-4**
- Hand-crafted anchor inside a procedural system. A lush, humid world with purple seas and continental Bloom forests.
- **Gameplay focus:** planetary exploration, outpost building, fauna (mutated native creatures).
- **Story:** A Sower "Garden Engine" is terraforming the planet in real time. Its native species — the **Tessari**, a gentle six-limbed megafauna — are dying out.
- **Choice:** Shut the Garden Engine down (Key is freed, planet begins healing, Bloom Hearts across the planet go dormant) **or** leave it running and extract the Key by force (faster, loot-rich, planet is lost). Affects the ending slides and Mara's approval.

#### `M3.04` — "Key of Echoes" — the ice world **Hollowmere** & the Choir
- The Choir's **Cathedral of the Hum** sits atop a Sower archive under the ice.
- **Gameplay focus:** cold survival, social stealth (walk among the Choir unarmed), dialogue-driven.
- **Story:** **Mother Sable** holds the Key. She reveals the Verdance is *not* mindless — it hears Sower instructions. The Choir wants to reach the Seedship to "join the song."
- **Choice:** Ally with the Choir (Sable gives the Key; unlocks the **Commune** ending), trick them, or take the Key by force.

#### `M3.05` — "Key of Iron" — the Directorate flagship **Ark Meridian**
- The Directorate has already taken the third Key and is using Null-carrier prisoners to study immunity.
- **Gameplay focus:** infiltration/boarding (ship combat → breach → interior combat), heist structure.
- **Story:** Discover Crane's plan, "**Project Eden**": use the Seedship to wipe Earth clean and resettle it with a curated, immune population.
- **Companion beat:** If Idris was saved in Act I, he defects fully here and helps free the prisoners. If not, he fights the player as a mini-boss and dies saying "You left me there."
- **Escape:** The player steals the Key; the Meridian is damaged. Crane swears pursuit.

### `M3.06` — "Grief" (Mid-Act III emotional beat)
- Triggers after the second Key. The Bloom infects the ship's hydroponics via a contaminated sample.
- **A companion is at risk.** Default: Mara is exposed while containing the breach. The player must cure her using the Loom fragment from the Key of Roots, *or* using Lily's blood (Lily consents but it weakens her), *or* Mara chooses to be put in cryo until a real cure exists.
- This is the story's lowest point — a character-driven "all is lost."

### `M3.07` — "Convergence" (Act III climax)
- With three Keys, the Jump Core resolves the location of the **Seedship *Anthesis*** — and it is **moving toward Earth's solar system**, awakened by Persephone's theft of its seed.
- Crane's fleet, the Choir's pilgrim ships and Free Hauler allies (depending on reputation) all converge.
- **Big set-piece:** fleet battle at the jump gate. Player's ship and allied NPC ships fight Directorate cruisers and Verdance "spore-swarms."

---

## 3.6 Act IV — "Seedfall" (9:30–12:00)

**Goal:** Board the Seedship, reach its heart (the **Loom**), and decide the fate of Earth.
**Tone:** Cosmic awe, horror and catharsis.

### `M4.01` — "Anthesis"
- Approach the Seedship: a living vessel the size of a moon, flowering with vast petal-sails. Ship combat against its defensive organisms.
- The player must **build a boarding craft** or modify their ship to breach the hull.

### `M4.02` — "The Living Halls"
- A dungeon across four biomes inside the Seedship — each a "memory garden" from a world the Sowers terraformed (including one that resembles prehistoric Earth).
- Companions join as a squad (up to 2). Hardest Hollow variants; Sower constructs.
- Environmental story: the Sowers' final recordings reveal they left because they finally realized some gardens held minds. They could not recall every seed. They were ashamed.

### `M4.03` — "Crane"
- Director Crane reaches the Loom first, having infused himself with a controlled Verdance strain to interface. He is becoming something new.
- **Boss fight** in three phases: Crane in augmented armor → Crane merged with Bloom growths → Crane's consciousness battling within the Loom (a surreal sequence in a Sower mind-space).
- Crane can be **talked down** in phase 3 if the player has high Directorate reputation and gathered his personal logs — he dies lucid and apologizing.

### `M4.04` — "The Loom" — the final choice

The Loom can rewrite the Verdance's instructions. The player chooses:

| Ending | Requirement | What happens | Epilogue |
|---|---|---|---|
| **CURE** | Lily's cooperation + Loom fragment (Key of Roots) | Rewrite the Verdance to self-terminate. The dead fall still across Earth. The Seedship dies. | Earth is a graveyard but free. Survivors return to rebuild. Lily grows up to lead the reconstruction. |
| **COMMUNE** | Choir alliance (Key of Echoes via Sable) | Rewrite the Verdance to recognize minds and coexist — Hollows become dormant; the Bloom becomes a planetary symbiont. Humanity is changed. | Earth becomes a strange, green, living world. People can "hear" the planet. Mara calls it "evolution with a conscience." |
| **EXODUS** | Always available | Command the Seedship itself. Leave Earth to the Bloom and carry humanity's survivors into the stars aboard a living ark. | The colony becomes a nomadic civilization. The Drift becomes home. Strongest hook for the sandbox. |
| *Secret:* **EDEN** | Side with Crane (multiple dark choices) | Carry out Project Eden. Earth is scoured and resettled by the chosen. | Clean, quiet, horrifying. Unlocks a Directorate-themed cosmetic set and a bleak epilogue. |

### `M4.05` — "New Dawn" (Epilogue)
- Narrated ending slides reflect: which planets were saved, which companions lived, colony morale, faction alliances, Tug's fate, Idris's fate.
- Final scene: the player's own station or ship, days later — survivors doing ordinary things. Lily asks the Engineer: *"So… what do we build next?"*
- **Return to sandbox:** the universe continues with the ending's consequences (e.g., CURE → Earth becomes a safe, rebuildable planet; COMMUNE → new "symbiotic" tech tree; EXODUS → Seedship becomes a buildable mega-base).

---

## 3.7 Branching & consequence tracker

| Flag | Set in | Affects |
|---|---|---|
| `tug_survived` | M1.07 | Tug appears in Act II–IV as chief engineer; epilogue |
| `idris_saved` | M1.03 | Idris companion vs. mini-boss in M3.05 |
| `cargo_manifest` | M1.07 | Starting resources in Act II |
| `patient_zero_choice` | M2.05 | Colony trust, Mara approval, a survivor lives/dies |
| `crane_stance` | M2.06 | Crane dialogue, talk-down possibility in M4.03 |
| `veyra_healed` | M3.03 | Ending slides, planet state in sandbox, Mara approval |
| `choir_allied` | M3.04 | Commune ending availability, Choir ships in M3.07 |
| `mara_fate` | M3.06 | Mara alive/cryo; Lily health; Cure ending availability |
| `faction_rep_*` | Ongoing | Allies in M3.07, trade, blueprints |
| `ending` | M4.04 | Epilogue and sandbox world state |

## 3.8 Side content (adds 6–13 hours)
- **Survivor Stories (12):** personal quests for recruitable survivors (e.g., finding a musician's guitar on Earth; a doctor who wants to return to the hospital where her family died).
- **Derelicts of the Drift (procedural):** derelict ships and stations with randomized layouts, logs and loot.
- **Hauler Contracts:** repeatable delivery, bounty and salvage missions.
- **Glyph Hunt:** find all 64 Sower glyphs to unlock the codex epilogue "Where the Sowers Went."
- **Earth Returns:** after Act II, the player can fly back to Earth to rescue more survivors and salvage. The Bloom's spread advances with campaign progress.
- **Tessari Sanctuary:** build a preserve for the Tessari after healing Veyra-4.
