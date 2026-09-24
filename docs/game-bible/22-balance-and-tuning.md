# 22 — Balance & Tuning

> Starting values for **Normal** difficulty. Every number lives in data (see [13](13-technical-architecture.md)) and will move during playtesting. Difficulty multipliers are in [10 §10.6](10-progression-and-economy.md).

## 22.1 Time

| Clock | Value |
|---|---|
| Earth day | 60 real minutes (40 day / 20 night) |
| Moon day | 120 real minutes (long light and dark periods; a stylized version of the real ~29.5-day cycle) |
| Drift planets | 30–180 minutes, procedural |
| In-game hour (for colony schedules) | 2.5 real minutes (1 in-game day = 60 real minutes) |
| Crop growth | 1–4 in-game days |
| Survivor aging | Off by default (on in *Long Haul* sandbox option: 1 year per 30 in-game days) |

## 22.2 Player vitals (per real minute, at rest)

| Vital | Max | Drain | Sprinting / exertion | Notes |
|---|---|---|---|---|
| Hunger | 100 | 1.0 | ×1.5 | Empty → −1 HP/10 s |
| Thirst | 100 | 1.5 | ×2.0 in heat | Empty → stamina capped at 50%, −1 HP/8 s |
| Stamina | 100 | — | Sprint −12/s; melee −15/swing | Regenerates 20/s after 1 s idle |
| Suit O₂ | 100 (= 10 min) | 10 | ×1.3 | Refills in pressurized rooms at 25/s |
| Suit energy | 100 | 0.5 | Jetpack −4/s; heater −1/s | Recharges at stations and beds |

## 22.3 Infection

| Parameter | Value |
|---|---|
| Scratch | +6% (±2) |
| Bite (grab) | +20% |
| Spore cloud, no filter | +2%/s |
| Contaminated food or water | +10% |
| Natural progression once Seeded (≥25%) | +1% per 20 s (player: +1% per 60 s, from partial resistance) |
| Suppressant | −10%; halts progression for 20 min |
| Antiviral | −40%; 10 min cooldown |
| Turning countdown at 90% | 60 s |

## 22.4 Survivor needs (per in-game hour)

| Need | Decay | Critical below | Typical restore |
|---|---|---|---|
| Hunger | −6 | 20 | Meal: +40 (Survival Ration) to +70 (Feast) |
| Rest | −4 (awake) | 15 | Bed: +12/h (bunk) to +18/h (quality bed) |
| Hygiene | −3 | 20 | Shower: +60 |
| Comfort | −2 | 20 | Seating and room quality: +5 to +15/h |
| Social | −3 | 25 | Conversation: +8; shared meal: +15 |
| Fun | −3 | 20 | Rec activity: +10 to +25/h |
| Safety | event-driven | 30 | Defenses nearby, well lit, no recent attacks |
| Purpose | −1 | 20 | Preferred job: +3/h; story milestone: +25 colony-wide |

**Mood** = weighted average of needs (0–100) + the sum of active moodlets. Mental-break chance per in-game hour: 2% below 25 mood, 6% below 10.

## 22.5 Horde & Attraction

**Attraction score** (per base, 0–1,000):
```
Attraction = Σ(block noise dB × 0.5) + Σ(light lumens × 0.01) + (power output MW × 20)
           + (gunfire events in the last in-game hour × 5) + (survivors × 4)
```

| Attraction | Nightly horde (Earth) | Green Moon wave |
|---|---|---|
| 0–100 | 5–15 Shamblers | 40 |
| 100–300 | 15–40, Runners from night 3 | 90 |
| 300–600 | 40–80, Screamers and Bloaters | 150, 2 Brutes |
| 600–1,000 | 80–150, Brutes | 250, 5 Brutes |

Horde size is further scaled by region Bloom level (×0.5 at ●○○○○ → ×2.0 at ●●●●●).

## 22.6 Enemy stats (Normal)

| Hollow | HP | Speed (m/s) | Damage | Infection/hit | Weak-point multiplier |
|---|---|---|---|---|---|
| Shambler | 100 | 1.1 | 12 | 6% | ×3 (head / bloom node) |
| Runner | 70 | 5.8 | 10 | 6% | ×3 |
| Crawler | 60 | 2.0 | 15 (ambush) | 8% | ×2.5 |
| Screamer | 90 | 1.4 | — (shriek: stun 1.5 s) | — | ×3 |
| Bloater | 140 | 1.2 | Explodes: 40 + spore cloud | 2%/s in cloud | ×2 |
| Brute | 900 | 2.2 | 45; 300/hit to blocks | 12% | ×2 (back node) |
| Drifter | 110 | 3.5 (lunge) | 14 | 6% | ×3 |
| Burrower | 400 | 3.0 underground | 30 | 10% | ×2 |
| Sower Warden | 2,500 | 2.5 | 60 | — | Resonance shield (Electric/Resonance only) |

## 22.7 Weapon stats (sample)

| Weapon | Tier | Damage | Rate (rpm) | Magazine | Noise (dB) | Notes |
|---|---|---|---|---|---|---|
| Ada's wrench | T0 | 35 | 70 | — | 20 | Never breaks; story item |
| Fire axe | T0 | 60 | 45 | — | 25 | Durability 300 hits |
| Nail-gun rifle | T0 | 22 | 240 | 40 | 55 | Quiet; nails craftable from scrap |
| Pistol | T1 | 30 | 300 | 15 | 140 | |
| Pump shotgun | T1 | 12 × 8 | 60 | 6 | 150 | Stagger |
| Assault rifle | T2 | 28 | 650 | 30 | 150 | |
| Flamethrower | T2 | 18/tick | — | 100 fuel | 90 | ×2 vs. Bloom; useless in vacuum |
| Arc rifle | T3 | 45 + chain (3) | 90 | 20 | 110 | ×2 vs. drones and Wardens |
| Resonance lance | T4 | 220 | 30 | 8 | 80 | Pierces Warden shields |

## 22.8 Block stats (sample)

| Block | Grid | Mass (kg) | HP | Power | Key stat |
|---|---|---|---|---|---|
| Light armor | Large | 500 | 1,500 | — | Load capacity 12 t |
| Heavy armor | Large | 3,300 | 6,500 | — | Load capacity 40 t |
| Blast door | Large | 4,000 | 9,000 | 0.2 kW | Airtight |
| Solar panel | Large | 400 | 600 | +120 kW (1 AU) | Scales with star distance |
| He-3 fusion reactor | Large | 28,000 | 5,000 | +80 MW | Fuel: 1 canister per 6 h at full load |
| O₂ generator | Large | 640 | 1,000 | −300 kW | 30 L/s O₂ from ice |
| Gatling turret | Large | 2,200 | 3,000 | −2 kW | 700 rpm; range 800 m |
| Atmospheric thruster | Large | 4,000 | 3,000 | −6 MW | 650 kN (in 1 atm) |
| Hydrogen thruster | Large | 6,900 | 4,000 | H₂ fuel | 1,100 kN |
| Jump core (Sower) | Large | 60,000 | 12,000 | −50 MW (charge) | Range 1 jump lane; cooldown 5 min |

## 22.9 Economy (Tortuga Drift base prices, in chits)

| Item | Buy | Sell |
|---|---|---|
| Steel plate (×100) | 400 | 250 |
| Suppressant | 120 | 70 |
| Antiviral | 600 | 380 |
| He-3 canister | 1,500 | 900 |
| Resonance crystal | 2,400 | 1,500 |
| Feast meal (×10) | 350 | 220 |
| Jump fuel (1 jump) | 800 | — |
| Recruit (skilled survivor) | 5,000 | — |

Prices shift ±40% with faction territory and supply (Choir markets pay double for medicine; Haulers pay double for fuel).

## 22.10 Research costs

| Tier | Nodes | Avg. cost per node | Main RP source |
|---|---|---|---|
| T0 | 12 | 10 Engineering RP | Scanning salvage |
| T1 | 24 | 60 | Scanning, Researcher jobs |
| T2 | 36 | 180 (+ Bio RP) | Lab analysis of Bloom samples |
| T3 | 40 | 450 | Drift scans, derelict data cores |
| T4 | 20 | 900 Precursor RP | Sower ruins, Keys |
| T5 | 12 per ending | 1,500 | Post-game |

## 22.11 Tuning principles
1. **Scarcity early, abundance late.** Act I ammo should feel precious; by Act III, logistics (not scarcity) is the challenge.
2. **Never more than one survival crisis at a time** from vitals alone.
3. **Death costs time, not progress.** Respawn is always within 2 minutes of travel of where you died (except Hardcore).
4. **Every number in this chapter lives in a data file** and is tuned from telemetry (see [11 §11.7](11-pacing-12-hours.md)).
