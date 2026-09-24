# 06 — Engineering & Building

> The *Space Engineers* pillar: everything the player builds is made of blocks on grids, simulated physically and systemically.

## 6.1 Grid types

| Grid | Block size | Used for | Unlock |
|---|---|---|---|
| **Structure (static)** | 2.5 m | Planet bases, station modules; anchored to terrain or orbit | Act I |
| **Large grid (dynamic)** | 2.5 m | Capital ships, large rovers, stations that move | Act III |
| **Small grid (dynamic)** | 0.5 m | Landers, fighters, rovers, drones, turrets, furniture detail | Act I (rover) / Act II (ships) |

- Grids can be connected via **connectors, rotors, pistons, hinges and merge blocks** to build mechanisms (drawbridges, cranes, landing gear, rotating habitat rings).
- **Projection:** a Projector block displays a blueprint hologram; the player (or drones) welds components into it.

## 6.2 Build flow
1. **Select block** from the radial/hotbar menu (filtered by category and unlocked tech).
2. **Place** a frame (costs only the first component — cheap placeholder).
3. **Weld** with the multitool to add components until the block is functional (block shows fill %).
4. **Grind** to deconstruct and recover components (losses: 0% normal, 10% on Hardcore).

**Build modes:** First-person (default), Build Camera (free-fly, planetside only when safe), Symmetry mode (mirror planes), Copy/Paste (Creative & unlocked Blueprint Tech).

## 6.3 Block categories (launch set ≈ 220 blocks)

| Category | Examples |
|---|---|
| **Structure** | Armor blocks (light/heavy), slopes, corners, catwalks, stairs, windows, beams |
| **Doors & Access** | Door, blast door, hangar door, airlock (auto-cycling), ladder, elevator |
| **Power** | Solar panel, wind turbine (planet), battery, hydrogen engine, fission reactor, He-3 fusion reactor, Sower resonance cell |
| **Life Support** | O₂ generator, air vent, CO₂ scrubber, air filter (spore), heater, cooler, water recycler, decon shower |
| **Production** | Refinery, assembler, kitchen, medical lab, fabrication bay, 3D printer |
| **Logistics** | Conveyors (small/large), sorters, cargo containers, connector, ejector, collector |
| **Propulsion** | Atmospheric thruster, ion thruster, hydrogen thruster, gyroscope, wheels/suspension, landing gear, jump drive |
| **Colony** | Beds, bunks, dining tables, stoves, showers, toilets, couches, TVs, bookshelves, workout gear, hydroponics trays, planters, memorial wall, kids' play area, chapel |
| **Defense** | Barricades, spike traps, flamethrower trap, floodlights, turrets (gatling, rocket, flame, laser), decoy, point-defense |
| **Control** | Cockpit, remote control, programmable block, sensor, timer, event controller, button panel, LCD |
| **Utility** | Medbay/Med-Pod (respawn), antenna, beacon, ore detector, scanner array, projector, drone bay, welder/grinder arms |
| **Precursor** | Sower jump core, Loom node, glyph-lock door, resonance amplifier |

## 6.4 Physical simulation

### Structural integrity
- Each block has **mass, hit points, deformation resistance** and **load-bearing capacity**.
- On planets, **gravity + load** are simulated: unsupported overhangs fail, weak supports buckle under heavy blocks.
- A **Structural View** overlay colors blocks green → red by stress.
- Hollow Brutes deliberately target the **weakest load-bearing block** — base design matters.

### Damage model
- Per-block HP and deformation. Destroyed blocks drop partial components.
- Ship collisions compute kinetic damage based on mass and velocity.
- Explosions (fuel tanks, reactors, Bloaters) propagate damage through adjacent blocks.

### Pressurization & atmosphere
- Enclosed, airtight volumes form **rooms**. Each room tracks **O₂, CO₂, pressure, temperature, spore concentration**.
- Breaches cause **decompression** (loose objects and people get pulled toward the hole).
- **Ventilation loops** connect rooms to life-support blocks; infection can travel through shared vents.
- Rooms are the bridge to the colony sim: the room system also computes **Room Quality** (see [07](07-colony-life-sim.md)).

### Power
- Blocks have **power draw** and **priority** (Life Support > Defense > Production > Comfort).
- On shortage, the lowest priority blocks brown out first; the player can change priorities per block.
- **Power grid view** shows generation vs. load, batteries and faults.

### Thrust & flight
- Ships need thrust in each direction greater than mass × gravity to hover/manoeuvre. The **Ship Info panel** shows thrust-to-weight per axis, fuel/power endurance, and jump range.
- Flight model: Newtonian with **inertial dampeners** (toggleable). Planetside atmosphere adds drag and lift for wing blocks (optional aerodynamics).
- **Gyroscopes** give rotation authority; heavy ships feel heavy.

### Logistics
- Conveyors connect inventories. **Sorters** filter by item. Refineries pull ore from cargo automatically; assemblers pull ingots.
- Survivors with the **Hauler** job move items between unconnected storage manually (the early-game solution before conveyors).

## 6.5 Automation (optional depth)
- **Event Controllers & Sensors:** no-code logic ("when Hollows detected within 50 m → close blast doors, turn on floodlights").
- **Timer Blocks & Button Panels:** sequences (auto airlock, landing sequence).
- **Programmable Block:** sandboxed scripting (Lua) for advanced players. Available on every difficulty — scripting is a player skill, not a cheat.
- **Drones:** Construction drones (weld projections), mining drones, defense drones. Controlled by drone bays; count limited by tech tier.

## 6.6 Blueprints
- Players can save any grid as a **blueprint** (with thumbnail and part list).
- **Story blueprints** are provided for key requirements (e.g., the *Wren* launch stack, the basic lunar lander) so non-builders are never hard-blocked.
- **Community sharing:** blueprints export/import as files and through Steam Workshop (post-launch).
- **Blueprint rule for story gates:** requirements are stated **functionally** ("lander must have TWR ≥ 1.5 in 0.16 g and 10 min O₂") rather than "build blueprint X," so creativity is respected.

## 6.7 Signature builds in the campaign

| Build | Mission | Requirement | Teaches |
|---|---|---|---|
| Hangar fortification | M1.01 | Seal openings, 1 generator, 2 floodlights | Placement, welding, power |
| Rover *"Mule"* | M1.05 | Wheels, cockpit, battery, cargo | Small grid, vehicle physics |
| *Wren* launch stack | M1.05–1.07 | Guidance, fuel, heat shield, life support installed | Subsystems, staging |
| Haven-9 restoration | M2.02 | Power, O₂, pressure, heat | Pressurization, priorities |
| Lunar lander | M2.04 | TWR ≥ 1.5 @ 0.16 g, O₂, landing gear | Thrust-to-weight, flight |
| Styx runner | M2.07 | Range 400k km, rad shielding | Fuel, shielding |
| *Second Chance* (capital ship) | M3.01 | Large grid, jump core mount, power ≥ 50 MW, cooling | Large-grid design, heat |
| Boarding craft | M4.01 | Breaching drill or ram, pressurized bay for 3 | Specialized design |

## 6.8 Building ↔ colony sim interplay
- Survivors **use** what you build: beds, stoves, showers, gym equipment, planters.
- **Layout matters:** long walks between bed and workstation reduce productivity; bunks crammed in small rooms reduce comfort; windows onto Earth or nebulae raise mood.
- **Noise & light:** reactors and refineries are loud — placing them next to bedrooms reduces sleep quality.
- **Safety perception:** survivors feel safer near turrets, blast doors and well-lit areas.

## 6.9 Creative & sandbox modes
- **Creative:** unlimited resources, all blocks, no enemies (toggleable), instant build.
- **Survival Sandbox:** no story; choose start (Earth outbreak, orbital derelict, or random Drift planet).
- **Scenario Editor (post-launch):** place grids, spawners, triggers and dialogue for custom scenarios.
