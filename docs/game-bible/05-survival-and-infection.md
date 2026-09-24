# 05 — Survival & Infection

## 5.1 Player vitals

| Vital | Range | Drains from | Restored by | At zero |
|---|---|---|---|---|
| **Health** | 0–100 | Damage, starvation, suffocation, cold/heat | Medkits, rest in medbay, food buffs | Downed → death |
| **Stamina** | 0–100 | Sprint, melee, jetpack boost (planetside) | Rest, food | Can't sprint/melee |
| **Hunger** | 0–100 | Time (~1/min), exertion | Food | Health drain |
| **Thirst** | 0–100 | Time (~1.5/min), heat | Water (must be purified) | Health drain, stamina cap |
| **Oxygen** | Suit tank | Time in vacuum/toxic air | Pressurized rooms, O₂ bottles, O₂ generators | Suffocation damage |
| **Suit Energy** | Battery | Jetpack, helmet light, suit heating/cooling | Charging stations, medical rooms, batteries | Systems off |
| **Temperature** | Comfort band | Biome, weather, vacuum shadow | Suit, shelter, fire, heaters | Hypo/hyperthermia |
| **Infection** | 0–100% | Hollow attacks, spores, bad food/water | Suppressant, Antiviral, Loom Serum | Turning (death) |
| **Radiation** | 0–100 | Stellar flares, reactors, deep space | Shielding, Rad-Away | Health cap reduction |

**Design intent:** Vitals create pressure and planning, not busywork. Tuned so a well-prepared player manages them in under 5% of attention. **Difficulty presets** scale drain rates (see [10 — Progression & Economy](10-progression-and-economy.md)).

## 5.2 The Infection system

The infection meter is the game's signature tension mechanic and applies to **the player and every survivor**.

### Stages
| Stage | Meter | Symptoms (player) | Symptoms (survivors) |
|---|---|---|---|
| **Clean** | 0% | — | — |
| **Exposed** | 1–24% | Faint green HUD vignette | Hidden unless scanned; "Feeling unwell" |
| **Seeded** | 25–59% | Stamina −20%, occasional audio whispers, green veins on arms | Mood −, works slower, may hide it (trait-dependent) |
| **Blooming** | 60–89% | Hallucinations (fake enemies/sounds), Health regen off | Delirious, may attack, spreads spores in rooms |
| **Turning** | 90–100% | 60s countdown → death | Turns into a Hollow inside your colony |

### Sources & amounts (baseline Normal difficulty)
| Source | Infection gain |
|---|---|
| Hollow scratch | +5–10% |
| Hollow bite (grab attack) | +20% |
| Spore cloud (no mask) | +2%/sec |
| Contaminated food/water | +10% |
| Handling Bloom samples without gloves | +1% per item |

### Treatments
| Item | Effect | Tier |
|---|---|---|
| **Suppressant** | Halts progression for 20 min; −10% | T0 (craftable from medical scrap) |
| **Antiviral Cocktail** | −40%; can't be used again for 10 min | T2 (Mara's lab) |
| **Null Serum** | Cures fully, grants 30 min immunity | T3 (requires Lily's cooperation; ethical cost) |
| **Loom Serum** | Cures fully and permanently raises resistance | T4 (Key of Roots) |
| **Amputation** (survivors only, limb bites) | Stops a bite at the source; survivor gets *Amputee* trait | Medbay surgery |

### Player resistance
The Engineer's partial resistance means infection **progresses 3× slower** once seeded, giving players room to learn. **Hardcore** removes this.

### Colony outbreaks
- A hidden infected survivor can turn **inside the colony** (see M2.05).
- Spores spread through **ventilation networks** — the building system models air as connected room volumes, so good engineering (air filters, bulkheads, separate vent loops) is real defense.
- **Quarantine tools:** lockable doors, vent shutoffs, decontamination airlocks, bio-scanners at entrances, emergency venting.

## 5.3 Death, downed state & respawn
- **Downed:** At 0 Health, the player is downed for 30 seconds. Companions or survivors with the *Medic* job can revive.
- **Death:** The player respawns at the nearest **Med-Pod** (buildable respawn point) with a debuff (*Shaken*: −10% max health for 5 minutes).
- **Your corpse:** Drops a backpack with inventory. If the player died infected, **their body rises as a Hollow wearing their gear** — you must kill yourself to get your stuff back. (Memorable, and a gentle punishment.)
- **Survivor death:** Permanent. Survivors mourn. Bodies must be recovered and cremated/ejected or they reanimate.
- **Story companions:** Protected by story immunity (downed instead of killed) except at authored moments. *Hardcore Story* removes this; the story adapts using fallback dialogue.

## 5.4 Gathering & crafting

### Gathering methods
| Tool | Gathers | Notes |
|---|---|---|
| **Multitool — Grinder mode** | Salvage from props/blocks/vehicles | Primary early source of components |
| **Multitool — Mining laser** | Ore from voxel terrain | Upgradable range/speed |
| **Hand Drill** (ship/rover) | Bulk ore | Requires cargo storage |
| **Harvester** | Plants, alien flora, Bloom samples | Gloves reduce infection |
| **Scanner** | Data (research points), resource locations | Also identifies infected survivors |

### Crafting stations (tiers)
| Station | Tier | Crafts |
|---|---|---|
| **Pocket Fabricator** (on suit) | T0 | Bandages, Suppressant, basic ammo, torches |
| **Workbench** | T0 | Tools, melee weapons, basic components |
| **Refinery** | T1 | Ingots from ore |
| **Assembler** | T1 | Components (steel plates, motors, circuits) for building |
| **Medical Lab** | T2 | Antivirals, medkits, stims |
| **Kitchen** | T1 | Meals (better mood & buffs than raw food) |
| **Armory** | T2 | Firearms, turrets ammo, armor |
| **Fabrication Bay** | T3 | Ship-scale parts, jump components |
| **Sower Loom Node** | T4 | Precursor tech, Loom Serum |

### Components (building materials)
Steel Plate · Interior Plate · Construction Component · Metal Grid · Motor · Computer · Display · Glass Panel · Thruster Component · Power Cell · Reactor Component · Medical Component · Radio Component · Superconductor · **Sower Filament** (T4) · **Living Alloy** (post-game)

## 5.5 Food & water
- **Early (Earth):** canned food, vending machines, scavenged water bottles.
- **Mid (Orbit):** hydroponics (lettuce, potatoes, soy, algae), water recycling, protein vats.
- **Late (Drift):** alien crops (require analysis — some are toxic, some Bloom-tainted), fishing, livestock (Tessari milk, after Veyra is healed).
- **Meals:** cooking combines ingredients into meals with **quality tiers** (Survival Ration → Homestyle → Feast) affecting survivor mood.
- **Water:** must be purified. Unpurified water carries infection risk and is a common early-game mistake.

## 5.6 Equipment
- **Suits:** Work Coveralls (Earth start) → Hazmat Suit (spores) → EVA Suit (vacuum) → Engineer Hardsuit → Sower-Woven Suit.
- **Suit modules:** jetpack, extra O₂, armor plates, spore filter, thermal lining, scanner range, stealth dampers.
- **Inventory:** Grid-based, weight-limited. Ships and bases use **conveyor-connected storage** so inventory management moves to engineering as the game progresses.
