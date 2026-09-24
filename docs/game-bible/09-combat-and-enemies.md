# 09 — Combat & Enemies

## 9.1 Combat philosophy
- **Weighty and scarce, not twitchy.** Ammo is limited, reloads matter, and noise attracts more Hollows.
- **Avoidance is valid.** Stealth, distraction and fortification are as important as shooting.
- **Engineering is combat.** Turrets, traps, walls and doors are the player's best weapons.
- **Escalation by act:** melee & improvised (Act I) → firearms & turrets (Act II) → energy weapons & ship combat (Act III) → Sower tech (Act IV).

## 9.2 Player combat

### Weapons (launch set, 24 — examples)
| Class | Examples | Tier |
|---|---|---|
| **Melee** | Wrench, fire axe, crowbar, riot baton, plasma cutter (multitool mode), Sower blade | T0–T4 |
| **Improvised** | Nail-gun rifle, flare gun, pipe shotgun, molotov, rivet launcher | T0–T1 |
| **Firearms** | Pistol, SMG, assault rifle, shotgun, marksman rifle (Directorate and civilian variants) | T1–T2 |
| **Heavy** | Flamethrower (effective vs. Bloom), grenade launcher, rocket launcher | T2–T3 |
| **Energy** | Arc rifle (chain lightning), coil gun, laser cutter | T3 |
| **Sower** | Resonance lance, Seed-spitter (turns Bloom against itself) | T4 |
| **Throwables** | Noise maker, frag, incendiary, EMP, spore-bomb (Choir) | Various |

- **Zero-G combat:** recoil pushes the player; magnetic boots anchor to hulls; firearms work in vacuum, flamethrowers don't.
- **Damage types:** Kinetic, Fire (bonus vs. Bloom growth), Electric (bonus vs. drones/constructs), Explosive, Resonance (Sower).
- **Dismemberment & weak points:** Hollows have Bloom "nodes" (glowing growths) — destroying the node kills them fastest.

### Stealth
- **Noise meter** (movement, gunfire, machinery) and **light exposure** determine detection.
- Hollows are nearly blind but have excellent hearing; Directorate troops rely on sight and drones.
- Takedowns: silent melee kills from behind (costs stamina).

## 9.3 The Hollow bestiary

| Hollow | First seen | Behavior | Counter |
|---|---|---|---|
| **Shambler** | M0.02 | Slow, relentless, groups up. Knocks on doors. | Melee, headshots, chokepoints |
| **Runner** | M1.02 | Fast, recently turned; leaps; packs of 3–6 | Shotguns, traps, high ground |
| **Crawler** | M1.02 | Legless, hides in vents & under vehicles; ambushes | Scanner, flashlight |
| **Screamer** | M1.04 | Emits a shriek that calls the horde & stuns | Priority target; suppressed weapons |
| **Bloater** | M1.05 | Swollen with spores; explodes into a spore cloud | Ranged kill; masks |
| **Brute** | M1.06 | Huge, armored with Bloom plating; targets weak load-bearing blocks | Fire, heavy weapons, reinforced walls |
| **Drifter** | M2.01 | Zero-G infected in EVA suits; pushes off surfaces to lunge | Mag-boots, shotguns, venting |
| **Burrower** | M2.04 | Tunnels through regolith/soil, erupts under bases | Seismic sensors, floor armor |
| **Stalker** | M3.03 | Bloom-mutated native predator (varies per planet) | Planet-specific |
| **Hive Swarm** | M3.03 | Flying spore-insects; drain O₂ and clog vents | Flame, air filters |
| **Mimic** | M3.04 | Mimics survivor voices/radio calls to lure the player | Scanner; trust but verify |
| **Husk Titan** | M3.07 | Colossal walking Bloom-mass (planet event boss) | Ship weapons, orbital strike |
| **Sower Warden** | M4.02 | Precursor construct — ancient guardian, resonance shield | Electric + Resonance damage |
| **Crane (Ascendant)** | M4.03 | Final boss (3 phases) | See [03 — Storyline](03-storyline.md) |

### Bloom Hearts
- Pulsing organic nests that anchor Hollow activity and spread Bloom in a radius.
- Destroying a Heart: sustained damage to its **3–5 root nodes** while waves spawn. Rewards: Bloom samples (research), Resonance crystals, reduced local Bloom.

## 9.4 Horde Nights & base defense
- **Earth (Act I):** Every in-game night (~20 real minutes per day) brings a horde; every 3rd night is a **Blood Moon** style big wave.
- **Noise/heat attraction model:** generators, refineries, gunfire and lights raise a base's **Attraction** score, which increases horde size. Engineering trade-off: power vs. stealth.
- **Hollows path-find to weak points**; Brutes and Burrowers target structure specifically.
- **Defense tools:** walls, gates, spikes, trap corridors, flame traps, floodlights (Hollows avoid bright light briefly), turrets (need ammo via conveyors), guard survivors (need Combat skill and weapons).
- **After-action report:** damage summary, ammo used, survivors hurt — helps the player learn.

## 9.5 Human enemies (Directorate)
- **Ark Trooper:** armored, uses cover, flanks, throws grenades.
- **Ark Sentinel Drone:** flying, spotlight + taser; alerts troopers.
- **Ark Enforcer:** heavy armor, riot shield, minigun.
- **Ark Medic:** revives troopers; priority target.
- **Directorate Officer:** buffs nearby troops; can be interrogated if subdued (non-lethal takedown option).
- **Non-lethal options:** stun batons, EMP, tranquilizer darts — killing humans affects Mara/Lily approval.

## 9.6 Ship combat
- **Grid-level damage:** every player-built block can be destroyed; ships break apart realistically.
- **Weapons:** gatling turrets, missile launchers, railguns, point defense, EMP torpedoes, boarding drills.
- **Subsystem targeting:** thrusters, power, weapons, jump core (disable instead of destroy to allow boarding).
- **Boarding:** breach with drills or dock forcibly; fight room to room; capture enemy ships (then repair and use them).
- **Enemy ship types:** Directorate Interceptor, Frigate, Cruiser (Act III), Carrier (Convergence); Verdance Spore-swarm (living projectiles), Bloom-overgrown derelicts that still fire; Seedship defense organisms.

## 9.7 AI architecture (summary)
- **Hollows:** utility AI + flowfield pathfinding for hordes (thousands on planets via LOD/impostors; 300 simulated active at once target).
- **Humans:** behavior trees with cover system and squad tactics.
- **Ships:** steering behaviors + target-priority utility scoring.
- **Director system:** adjusts spawn intensity to player state (health, ammo, recent deaths) within difficulty bounds — tension curve, not cheating.

## 9.8 Difficulty knobs
Enemy health/damage · horde size · ammo scarcity · infection rate · permadeath · story immunity · structural collapse strictness. See [10 — Progression & Economy](10-progression-and-economy.md).
