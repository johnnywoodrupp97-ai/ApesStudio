# 24 — Systems Interaction Matrix & Emergent Stories

> The magic of EXODUS PROTOCOL is where systems collide. This chapter maps the collisions and shows the stories they produce without a writer.

## 24.1 Interaction matrix

Read across: **row system → affects → column system.**

| → | **Building** | **Power** | **Atmosphere** | **Infection** | **Colony** | **Combat** | **Open world** |
|---|---|---|---|---|---|---|---|
| **Building** | — | Blocks draw and produce power | Airtight walls make rooms; vents make air loops | Bulkheads and decon airlocks contain outbreaks | Room quality, layout, and noise drive mood | Walls, turrets and traps; structural weak points | Outposts and ships extend your reach |
| **Power** | Brownouts disable blocks | — | No power → no O₂, no heat | Filters fail → spores spread | Lights and comfort blocks off → mood drops | Turrets go dark | Generators raise Attraction |
| **Atmosphere** | Breaches pull loose blocks | Life support is the top power priority | — | Spores travel through shared vents | Bad air → sick, angry survivors | Decompression as a weapon (vent the Hollows) | Planet atmospheres set suit needs |
| **Infection** | Bloom growth damages blocks | — | Bloaters foul rooms | — | Hidden bites, fear, quarantine drama | Turned survivors attack inside | Bloom level shapes regions |
| **Colony** | Survivors build, repair and haul | Mechanics keep generators running | Janitors keep filters clean | Medics treat; *Hides Wounds* trait hides bites | — | Guards defend; morale affects accuracy | Scouts and expeditions find leads |
| **Combat** | Explosions and Brutes destroy blocks | Damaged reactors | Hull breaches | Every hit risks infection | Deaths and injuries → grief | — | Noise draws hordes and patrols |
| **Open world** | New materials and blueprints | New fuels (He-3, Resonance) | New atmospheres and hazards | New Bloom variants | New survivors, traits and traders | New enemies and factions | — |

## 24.2 Design rules for collisions
1. **Every system must touch at least three others.** If it doesn't, it's a mini-game, not a system.
2. **Every collision must be readable.** The player can always find out *why* something happened (overlays, KESTREL diagnostics, survivor dialogue).
3. **Cascades are capped.** A failure can chain at most three systems deep before a warning gives the player a chance to intervene.
4. **Good engineering is the universal counter.** Almost every cascade can be prevented by building well.

## 24.3 Emergent story examples (from playtest scenarios)

### "The Leaky Vent"
Priya, who has the *Hides Wounds* trait, is scratched on a scavenging run and doesn't tell anyone. At Haven-9 she sleeps in the barracks, which share a vent loop with the hydroponics bay. By morning the spore count in hydroponics is rising, and the lettuce has green veins. KESTREL flags it. The player traces the vent loop in the Air View, finds Priya feverish in her bunk, and has to decide: quarantine the whole barracks (everyone's mood crashes) or just Priya (and risk it). **Systems:** traits → infection → atmosphere → food → colony → player choice.

### "Walt's Window"
The player builds an observation deck with a window facing Earth. Walt Hennessey (*Storyteller*) starts spending his leisure hours there telling stories to the kids. Lily's Social and Fun needs are met, and she picks up Walt's piloting skill. Later (with *Long Haul* aging on), when Walt dies of old age, Lily keeps going to the window alone. **Systems:** building → room quality → colony autonomy → skills → memory barks.

### "The Generator That Called the Horde"
On Earth, the player builds a huge base at Hollis Dam and restores the hydroelectric plant: enormous power, enormous Attraction. The Green Moon wave comes for the dam with 5 Brutes. The player's walls are strong, but the Brutes target the one support pillar under the turbine hall. It falls; the power fails; the floodlights die; Runners pour in through the dark. **Systems:** power → Attraction → horde → structural integrity → power → combat.

### "Venting the Brute"
A Brute breaches Haven-9's cargo module. The player seals the bulkheads with survivors on the right side, then opens the outer hangar door. The Brute, the cargo and a very surprised Hollow go out into space. The survivors cheer; the cargo loss hurts. **Systems:** atmosphere → combat → logistics.

### "Oye's Debt"
Short on fuel, the player takes a Hauler contract but abandons it to rescue a refugee pod. Hauler reputation drops; fuel prices at Tortuga go up; but the refugee pod contained a Notable Survivor medic who later saves Mara in M3.06. **Systems:** economy → reputation → rescue events → story.

### "Idris Won't Go"
Idris's approval falls after the player repeatedly trusts Directorate messages. When the player orders an expedition, Idris refuses: *"Not while you're taking calls from them."* The player has to talk him around or send an untrained scout. **Systems:** approval → colony orders → expedition risk.

### "The Wedding on the Moon"
Marcus and Joel Webb (*Bonded*) have high mood for weeks. The Event Director fires a proposal-vow-renewal event; the Council asks the player to build a chapel. The player builds it on the Tycho outpost, with an Earthrise window. The wedding gives a colony-wide Purpose boost just before The Taking. **Systems:** relationships → events → building → morale → story resilience.

### "KESTREL Left On"
After Tug dies in The Taking, the player never turns on KESTREL's *Quiet Hours* setting again. Three in-game weeks later, KESTREL asks: *"You stopped switching me off. Is that because of Tug?"* This bark only exists if the player's own behavior matched the pattern. **Systems:** player habit tracking → memory barks → character arc (`kestrel_mind`).
