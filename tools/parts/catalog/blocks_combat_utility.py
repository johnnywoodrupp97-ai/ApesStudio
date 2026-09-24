"""DEF — Defense & Weapon Systems, UTL — Utility, Sensors & Lighting, SOW — Precursor (Sower)."""

from . import P, V

LG_1 = {"LG": (1, 1, 1)}
LG_SG_1 = {"LG": (1, 1, 1), "SG": (1, 1, 1)}

TURRET_RIG = ("Turret rig standard: PART_Base (static) → PART_Yaw (rotates about Z) → PART_Pitch (rotates about Y) → "
              "PART_Barrel (spins or recoils). Pivots on the axis lines; muzzle socket at the barrel tip.")

# ---------------------------------------------------------------------------
# DEF — Survivor defenses (Act I)
# ---------------------------------------------------------------------------
P("DEF", "Barricade", "Survivor Defenses", LG_1, tier="T0", art="SCR", cls="M",
  mass=300, hp=800, recipe={"scrap_metal": 10, "salvaged_wood": 10},
  function="Blocks paths and soaks Hollow damage. Hollows climb over low barricades, so height matters.",
  mounts="bottom", airtight="none",
  notes="1.8 m tall. Each variant has 3 damage states (intact, battered, collapsing) as separate meshes because barricades break visibly.",
  variants=[V("Wooden"), V("Car Wreck", mass_mult=3, hp_mult=1.6, notes="Half a sedan on its side; broken glass."), V("Pallet & Wire")])

P("DEF", "Sandbag Wall", "Survivor Defenses", LG_1, tier="T0", art="SCR", cls="S",
  mass=1200, hp=1400, recipe={"fabric": 10, "scrap_metal": 2},
  function="Cover for defenders; absorbs explosions well.", mounts="bottom", airtight="none",
  notes="Individual bag shapes (6 unique bags instanced).",
  variants=[V("Full Height"), V("Half Height", mass_mult=0.5, hp_mult=0.5)])

P("DEF", "Barbed Wire", "Survivor Defenses", LG_1, tier="T0", art="SCR", cls="S",
  mass=40, hp=250, recipe={"scrap_metal": 6},
  function="Slows Hollows by 60% and deals light damage while they push through.", mounts="bottom", airtight="none",
  notes="Coiled concertina wire on X-frames. Real geometry for the coils (no alpha); keep coils under the S budget with a spline-generated low-segment wire.")

P("DEF", "Spike Trap", "Survivor Defenses", LG_1, tier="T0", art="SCR", cls="S",
  mass=100, hp=400, recipe={"scrap_metal": 8, "salvaged_wood": 4},
  function="Floor spikes: damage and stagger Hollows walking over them. Wear out with use.",
  mounts="bottom", shape="floor",
  notes="Rebar and sharpened stakes in a pallet base; 3 wear states.")

P("DEF", "Chain-Link Fence", "Survivor Defenses", LG_1, tier="T0", art="SCR", cls="S",
  mass=60, hp=400, recipe={"scrap_metal": 4, "small_tube": 3},
  function="See-through perimeter fence. Hollows pile against it; Brutes flatten it.", mounts="bottom,left,right", airtight="none",
  shape="panel", notes="Masked chain-link material. Bends under load (vertex shader driven by 'Push').",
  variants=[V("Plain"), V("Razor Wire")])

P("DEF", "Tripwire Mine", "Traps", {"SG": (1, 1, 1)}, tier="T1", art="SCR", cls="S",
  mass=4, hp=10, recipe={"SG": {"explosives": 1, "scrap_metal": 1, "wiring_bundle": 1}},
  function="Explodes when a tripwire (up to 5 m) is crossed.", mounts="bottom",
  sockets=["vfx_fire@center"], vfx=["Explosion"], notes="Pipe-bomb canister with a wire spool.")

P("DEF", "Noise Decoy", "Traps", LG_SG_1, tier="T1", art="SCR", cls="S",
  mass={"LG": 60, "SG": 5}, hp={"LG": 150, "SG": 30}, power={"LG": -0.5, "SG": -0.05},
  recipe={"LG": {"scrap_metal": 4, "radio_component": 1, "power_cell": 1}},
  function="Plays loud sounds on a timer or trigger to pull hordes away from the base.",
  mounts="bottom", sockets=["audio@center"], emissive=["Blinking LED"], audio=["Siren / music box / recorded voice"],
  notes="Alarm-clock-and-speaker contraption; the SG version is a throwable-sized box.")

P("DEF", "Flame Trap", "Traps", LG_1, tier="T2", cls="M",
  mass=500, hp=900, power=-1, recipe={"steel_plate": 8, "large_tube": 4, "motor": 1},
  function="Floor or wall vents that spray fire (×2 damage vs. Bloom). Burns fuel from the conveyor network.",
  mounts="bottom,back", sockets=["vfx_fire@top", "fuel@bottom"], vfx=["Fire jet", "Pilot flame"],
  notes="Grated vent plate over nozzles; heat discoloration on the plate.")

# ---------------------------------------------------------------------------
# DEF — Turrets
# ---------------------------------------------------------------------------
P("DEF", "Interior Turret", "Turrets", LG_1, tier="T2", cls="M",
  mass=300, hp=600, power=-0.5, recipe={"interior_plate": 6, "construction_component": 20, "motor": 2, "computer": 5, "steel_plate": 4},
  function="Ceiling-mounted small-caliber turret for corridors (outbreak control).",
  mounts="top", sockets=["muzzle@bottom", "camera@bottom"], emissive=["Targeting laser (red)"],
  moving=["Yaw 360°", "Pitch −90° to 0°"], audio=["Servo whirr", "Rapid fire"], notes=TURRET_RIG)

P("DEF", "Gatling Turret", "Turrets", {"LG": (3, 2, 3), "SG": (3, 2, 3)}, tier="T2", cls="L",
  mass={"LG": 2200, "SG": 350}, hp={"LG": 3000, "SG": 500}, power={"LG": -2, "SG": -0.5},
  recipe={"LG": {"steel_plate": 40, "construction_component": 30, "metal_grid": 15, "small_tube": 6, "motor": 8, "computer": 10}},
  function="The workhorse turret: 700 rpm, 800 m range. Ammo arrives through conveyors.",
  stats={"rpm": 700, "range_m": 800},
  mounts="bottom", sockets=["muzzle@front", "conveyor_large@bottom", "camera@front"],
  moving=["Yaw 360°", "Pitch −10° to +90°", "Barrel cluster spin"], emissive=["Status light"],
  vfx=["Muzzle flash", "Shell ejection"], audio=["Spin-up", "Fire loop"], notes=TURRET_RIG)

P("DEF", "Rocket Turret", "Turrets", {"LG": (3, 2, 3), "SG": (3, 2, 3)}, tier="T2", cls="L",
  mass={"LG": 2600, "SG": 400}, hp={"LG": 3200, "SG": 500}, power={"LG": -2, "SG": -0.5},
  recipe={"LG": {"steel_plate": 50, "construction_component": 40, "metal_grid": 15, "large_tube": 6, "motor": 8, "computer": 10}},
  function="Rockets for Brutes, vehicles and ships. Splash damage.", stats={"range_m": 1000},
  mounts="bottom", sockets=["muzzle@front*4", "conveyor_large@bottom"],
  moving=["Yaw 360°", "Pitch −10° to +80°", "Pod doors"], vfx=["Launch smoke", "Backblast"], audio=["Launch whoosh"], notes=TURRET_RIG)

P("DEF", "Flame Turret", "Turrets", {"LG": (2, 1, 2)}, tier="T2", cls="M",
  mass=1400, hp=2200, power=-1, recipe={"steel_plate": 30, "large_tube": 8, "motor": 6, "computer": 6},
  function="Short-range (30 m) flame turret: ×2 damage vs. Bloom, burns Bloom Hearts. Useless in vacuum.",
  mounts="bottom", sockets=["muzzle@front", "fuel@bottom"],
  moving=["Yaw 360°", "Pitch −20° to +45°"], emissive=["Pilot light"], vfx=["Flame stream", "Heat haze"], audio=["Roar"], notes=TURRET_RIG)

P("DEF", "Arc Turret", "Turrets", {"LG": (2, 2, 2)}, tier="T3", cls="L",
  mass=2000, hp=2600, power=-400, recipe={"steel_plate": 30, "superconductor": 20, "power_cell": 20, "motor": 6, "computer": 10},
  function="Chain lightning (3 targets). ×2 vs. drones and Sower Wardens.",
  mounts="bottom", sockets=["muzzle@top", "camera@front"],
  moving=["Yaw 360°", "Pitch 0° to +80°", "Coil rings pulse"], emissive=["Charge coils (electric blue)"],
  vfx=["Lightning arcs"], audio=["Charge whine", "Crack"], notes=TURRET_RIG + " Tesla-coil head.")

P("DEF", "Laser Turret", "Turrets", {"LG": (2, 2, 2), "SG": (2, 2, 2)}, tier="T3", cls="L",
  mass={"LG": 1800, "SG": 300}, hp={"LG": 2400, "SG": 400}, power={"LG": -800, "SG": -80},
  recipe={"LG": {"steel_plate": 25, "superconductor": 15, "glass_panel": 4, "motor": 6, "computer": 12}},
  function="Hitscan beam; no ammo, heavy power draw.",
  mounts="bottom", sockets=["muzzle@front"], moving=["Yaw 360°", "Pitch −10° to +90°"], emissive=["Lens glow"],
  vfx=["Beam", "Impact glow"], audio=["Beam hum"], notes=TURRET_RIG)

P("DEF", "Point Defense Turret", "Turrets", LG_SG_1, tier="T3", cls="M",
  mass={"LG": 900, "SG": 120}, hp={"LG": 1400, "SG": 200}, power={"LG": -5, "SG": -0.5},
  recipe={"LG": {"steel_plate": 20, "motor": 6, "computer": 12, "detector_component": 4}},
  function="Shoots down missiles, spore-swarms and drones.",
  mounts="bottom", sockets=["muzzle@front", "camera@front"], moving=["Yaw 360°", "Pitch 0° to +90°", "Barrel spin"],
  vfx=["Tracer flash"], audio=["Buzz fire"], notes=TURRET_RIG + " Radar dish on the yaw ring (PART_Radar spins).")

# ---------------------------------------------------------------------------
# DEF — Fixed ship weapons
# ---------------------------------------------------------------------------
P("DEF", "Gatling Gun", "Fixed Weapons", {"LG": (1, 1, 3), "SG": (1, 1, 3)}, tier="T2", cls="M",
  mass={"LG": 1200, "SG": 200}, hp={"LG": 1600, "SG": 300},
  recipe={"LG": {"steel_plate": 20, "construction_component": 20, "metal_grid": 6, "small_tube": 6, "motor": 4, "computer": 2}},
  function="Forward-firing gatling for fighters and gunboats.", mounts="back,bottom",
  sockets=["muzzle@front", "conveyor_large@back"], moving=["Barrel cluster spin"], vfx=["Muzzle flash", "Shell ejection"],
  audio=["Fire loop"], notes="Barrel along +X.")

P("DEF", "Missile Launcher", "Fixed Weapons", {"LG": (1, 1, 2), "SG": (1, 1, 2)}, tier="T2", cls="M",
  mass={"LG": 1500, "SG": 250}, hp={"LG": 2000, "SG": 300},
  recipe={"LG": {"steel_plate": 30, "construction_component": 20, "large_tube": 8, "motor": 4, "computer": 4}},
  function="Four-tube forward launcher.", mounts="back,bottom", sockets=["muzzle@front*4", "conveyor_large@back"],
  moving=["Tube covers ×4"], vfx=["Launch smoke"], audio=["Launch"], notes="2×2 tube grid on the front face.")

P("DEF", "Railgun", "Fixed Weapons", {"LG": (1, 1, 6), "SG": (1, 1, 6)}, tier="T3", cls="L",
  mass={"LG": 20000, "SG": 1400}, hp={"LG": 6000, "SG": 800}, power={"LG": -50000, "SG": -4000},
  recipe={"LG": {"steel_plate": 300, "superconductor": 150, "power_cell": 20, "large_tube": 20, "computer": 20}},
  function="Charged kinetic spike (2,000 m/s). Only obtainable from exploration blueprint fragments.",
  unlock="Blueprint fragments (Fort Calder, Directorate outposts).",
  mounts="back,bottom", sockets=["muzzle@front", "conveyor_large@back"],
  moving=["Rail capacitor rings pulse"], emissive=["Charge rails (blue-white)"], vfx=["Muzzle flash", "Ionized trail"],
  audio=["Charge whine", "Thunderclap"], notes="Long twin-rail barrel with capacitor bank at the back.")

P("DEF", "EMP Torpedo Launcher", "Fixed Weapons", {"LG": (1, 1, 3)}, tier="T3", cls="M",
  mass=3000, hp=2500, recipe={"steel_plate": 40, "large_tube": 8, "power_cell": 10, "computer": 8},
  function="Disables a target's subsystems for 20 s: the first step of a boarding action.",
  mounts="back,bottom", sockets=["muzzle@front", "conveyor_large@back"],
  vfx=["Launch flash"], audio=["Launch thump"], notes="Single large tube with a blue EMP warning band.")

P("DEF", "Boarding Drill", "Boarding", {"LG": (3, 3, 4)}, tier="T3", cls="XL",
  mass=40000, hp=15000, power=-3000,
  recipe={"steel_plate": 400, "large_tube": 40, "motor": 80, "construction_component": 60, "metal_grid": 60},
  function="Drills through hulls (and the Seedship's living skin) to open a pressurized breach for a squad (M4.01).",
  mounts="back", airtight="all",
  moving=["Drill head: spins", "Cutter teeth ring: counter-spins", "Seal skirt: extends 1 m"],
  sockets=["vfx_sparks@front", "interact@back", "air@back"], vfx=["Sparks", "Debris", "Organic spray (vs Seedship)"],
  audio=["Grinding roar"], notes="Hero piece: conical cutter with a sealing skirt so the breach stays pressurized.")

P("DEF", "Ram Prow", "Boarding", {"LG": (3, 3, 2)}, tier="T2", cls="M",
  mass=24000, hp=30000, recipe={"steel_plate": 500, "metal_grid": 200},
  function="Reinforced wedge for ramming and forced docking. Takes 25% of collision damage.",
  mounts="back", airtight="all", shape="slope", notes="Layered armor plates with scrape marks.")

# ---------------------------------------------------------------------------
# UTL — Lighting
# ---------------------------------------------------------------------------
P("UTL", "Floodlight", "Lighting", LG_SG_1, tier="T0", art="SCR", cls="S",
  mass={"LG": 120, "SG": 10}, hp={"LG": 300, "SG": 40}, power={"LG": -3, "SG": -0.5},
  recipe={"LG": {"scrap_metal": 6, "glass_panel": 2, "wiring_bundle": 2}},
  function="60,000 lm stadium light. Hollows avoid bright light briefly, but it raises Attraction.",
  stats={"lumens": 60000},
  mounts="bottom,back", moving=["Head: yaw 360°, pitch −45° to +45°"], sockets=["light@front"],
  emissive=["Lamp face"], audio=["Ballast hum"], notes="Salvaged construction floodlight on a tripod (SCR) or pole mount (IND variant).",
  variants=[V("Tripod (Survivor)"), V("Pole Mount (Industrial)", tier="T1")])

P("UTL", "Interior Light", "Lighting", LG_SG_1, tier="T1", cls="S",
  mass={"LG": 20, "SG": 2}, hp={"LG": 80, "SG": 15}, power={"LG": -0.2, "SG": -0.02},
  recipe={"LG": {"construction_component": 2, "glass_panel": 1}},
  function="Room lighting; color and intensity affect mood.", mounts="top", shape="panel_top",
  sockets=["light@bottom"], emissive=["Light panel"], notes="Recessed panel light; color from the light's settings.")

P("UTL", "Spotlight", "Lighting", LG_SG_1, tier="T1", cls="S",
  mass={"LG": 60, "SG": 5}, hp={"LG": 150, "SG": 25}, power={"LG": -0.5, "SG": -0.05},
  recipe={"LG": {"construction_component": 3, "glass_panel": 2, "motor": 1}},
  function="Directional light on a rotating mount.", mounts="bottom,back,top",
  moving=["Yaw 360°", "Pitch ±90°"], sockets=["light@front"], emissive=["Lens"], notes="Can be driven by sensors to track targets.")

P("UTL", "Warning Beacon Light", "Lighting", LG_SG_1, tier="T1", cls="S",
  mass={"LG": 20, "SG": 2}, hp={"LG": 80, "SG": 15}, power={"LG": -0.1, "SG": -0.01},
  recipe={"LG": {"construction_component": 2, "glass_panel": 1, "motor": 1}},
  function="Rotating amber or red warning light for airlocks, hangars and alarms.", mounts="bottom,back,top",
  moving=["Reflector spins"], sockets=["light@center"], emissive=["Dome glow"], notes="Classic rotating dome.")

# ---------------------------------------------------------------------------
# UTL — Comms & sensing
# ---------------------------------------------------------------------------
P("UTL", "Camera", "Sensing", LG_SG_1, tier="T1", cls="S",
  mass={"LG": 30, "SG": 3}, hp={"LG": 100, "SG": 20}, power={"LG": -0.1, "SG": -0.01},
  recipe={"LG": {"construction_component": 2, "computer": 3, "glass_panel": 1}},
  function="Remote view; feeds LCDs and security monitoring.", mounts="back,top",
  moving=["Yaw ±90°", "Pitch ±45°"], sockets=["camera@front"], emissive=["Recording LED"], notes="Security-camera housing.")

P("UTL", "Antenna", "Comms", {"LG": (1, 4, 1), "SG": (1, 3, 1)}, tier="T1", cls="M",
  mass={"LG": 1500, "SG": 90}, hp={"LG": 1500, "SG": 150}, power={"LG": -2, "SG": -0.2},
  recipe={"LG": {"steel_plate": 80, "large_tube": 40, "small_tube": 60, "construction_component": 40, "computer": 8, "radio_component": 40}},
  function="Broadcasts the grid and relays remote control. Range 50 km (LG) / 5 km (SG).",
  mounts="bottom", sockets=["light@top"], emissive=["Aviation light (red)"],
  notes="Lattice mast with dipoles; the top 20% is thin (LOD1 simplifies it to cards).")

P("UTL", "Laser Antenna", "Comms", {"LG": (1, 1, 2), "SG": (1, 1, 2)}, tier="T2", cls="M",
  mass={"LG": 900, "SG": 80}, hp={"LG": 1200, "SG": 150}, power={"LG": -5, "SG": -0.5},
  recipe={"LG": {"steel_plate": 50, "construction_component": 40, "motor": 16, "detector_component": 30, "radio_component": 20, "computer": 50}},
  function="Point-to-point comms across unlimited range (line of sight).", mounts="bottom",
  moving=["Head: yaw 360°, pitch 0–90°"], sockets=["projector@front"], emissive=["Laser beam when linked"], vfx=["Beam"],
  notes="Telescope-like head on a gimbal.")

P("UTL", "Beacon", "Comms", LG_SG_1, tier="T1", cls="S",
  mass={"LG": 250, "SG": 20}, hp={"LG": 400, "SG": 60}, power={"LG": -0.5, "SG": -0.05},
  recipe={"LG": {"steel_plate": 80, "construction_component": 30, "large_tube": 20, "computer": 10, "radio_component": 40}},
  function="Marks a grid on everyone's HUD (and on Hollow hearing: it hums).", mounts="bottom",
  sockets=["light@top"], emissive=["Pulsing lamp"], audio=["Soft pulse"], notes="Short mast with a glass dome.")

P("UTL", "Beacon Relay", "Comms", {"LG": (1, 2, 1)}, tier="T2", cls="M",
  mass=1800, hp=1500, power=-50,
  recipe={"steel_plate": 30, "superconductor": 6, "radio_component": 20, "computer": 10},
  function="Fast-travel endpoint between your own bases and ships (from Act II; off in Hardcore).",
  mounts="bottom", sockets=["interact@front", "projector@top"], emissive=["Relay ring (teal)"], vfx=["Arrival flash"],
  notes="Pad with a ring arch the player steps into.")

P("UTL", "Landing Beacon", "Comms", LG_SG_1, tier="T2", cls="S",
  mass={"LG": 150, "SG": 12}, hp={"LG": 300, "SG": 40}, power={"LG": -0.5, "SG": -0.05},
  recipe={"LG": {"steel_plate": 6, "radio_component": 4, "computer": 2}},
  function="Autopilot landing target with pad lights (used in the M2.04 lunar landing).", mounts="bottom", shape="floor",
  sockets=["light@top*4"], emissive=["Chasing pad lights"], notes="Flat disc with four light posts.")

P("UTL", "Ore Detector", "Sensing", LG_SG_1, tier="T1", cls="S",
  mass={"LG": 700, "SG": 40}, hp={"LG": 900, "SG": 90}, power={"LG": -2, "SG": -0.2},
  recipe={"LG": {"steel_plate": 50, "construction_component": 40, "motor": 5, "computer": 25, "detector_component": 20}},
  function="Marks ore deposits within 150 m (LG) / 50 m (SG).", mounts="bottom,back",
  moving=["Sensor dish spins"], emissive=["Scan ring"], notes="Dish on a stubby mast.")

P("UTL", "Scanner Array", "Sensing", {"LG": (3, 3, 3)}, tier="T2", cls="L",
  mass=6000, hp=4000, power=-100,
  recipe={"steel_plate": 60, "girder": 40, "motor": 10, "computer": 30, "detector_component": 40, "radio_component": 20},
  function="Long-range planetary scans: resource maps, Bloom coverage, life signs.",
  mounts="bottom", moving=["Dish: yaw 360°, pitch 0–90°", "Feed horn"], sockets=["interact@bottom"],
  emissive=["Feed-horn glow"], audio=["Servo sweep"], notes="Parabolic dish (6 m) on a turret base.")

P("UTL", "Signal Decoder", "Sensing", {"LG": (1, 1, 2)}, tier="T1", cls="M",
  mass=600, hp=700, power=-10, recipe={"interior_plate": 10, "computer": 12, "radio_component": 10, "display": 2},
  function="Triangulates distress calls and Sower beacons: the main way to find points of interest in the open world.",
  unlock="T1 (Red Mesa Observatory data speeds it up).",
  mounts="bottom", sockets=["interact@front", "lcd@front", "work@front"], emissive=["Waveform screen"], audio=["Radio static"],
  notes="Rack of receivers with a big waveform screen and headphones on a hook.")

P("UTL", "Projector", "Construction", LG_SG_1, tier="T1", cls="M",
  mass={"LG": 700, "SG": 40}, hp={"LG": 900, "SG": 90}, power={"LG": -1, "SG": -0.1},
  recipe={"LG": {"interior_plate": 21, "construction_component": 4, "large_tube": 2, "motor": 1, "computer": 2}},
  function="Projects a blueprint hologram to weld into. Story blueprints use it so nobody is hard-blocked.",
  mounts="bottom,back", sockets=["projector@top"], emissive=["Lens"], vfx=["Hologram"], notes="Lens dome on a squat base.")

P("UTL", "Drone Bay", "Construction", {"LG": (3, 2, 3)}, tier="T2", cls="L",
  mass=8000, hp=5000, power=-60,
  recipe={"steel_plate": 80, "motor": 20, "computer": 30, "radio_component": 10, "construction_component": 40},
  function="Launches, docks and recharges construction, mining and defense drones.",
  mounts="bottom,back", airtight="all",
  moving=["Roof doors: split and slide", "Drone cradles ×4: rise"], sockets=["conveyor_large@back", "interact@front"],
  emissive=["Cradle status lights"], notes="Four drone cradles; the drones themselves are separate assets (see Equipment).")

# ---------------------------------------------------------------------------
# UTL — Tools & service
# ---------------------------------------------------------------------------
P("UTL", "Welder Arm", "Ship Tools", {"LG": (1, 1, 2), "SG": (1, 1, 2)}, tier="T2", cls="M",
  mass={"LG": 1400, "SG": 90}, hp={"LG": 1500, "SG": 150}, power={"LG": -20, "SG": -2},
  recipe={"LG": {"steel_plate": 30, "construction_component": 30, "large_tube": 1, "motor": 2}},
  function="Ship-mounted welder: builds projections and repairs.", mounts="back",
  sockets=["vfx_sparks@front", "conveyor_large@back"], moving=["Tip nozzle pulses"], vfx=["Welding arc"], audio=["Weld crackle"],
  notes="Shares the multitool's weld VFX.")

P("UTL", "Grinder Arm", "Ship Tools", {"LG": (1, 1, 2), "SG": (1, 1, 2)}, tier="T2", cls="M",
  mass={"LG": 1400, "SG": 90}, hp={"LG": 1500, "SG": 150}, power={"LG": -20, "SG": -2},
  recipe={"LG": {"steel_plate": 20, "construction_component": 30, "large_tube": 1, "motor": 4}},
  function="Ship-mounted grinder: salvages wrecks.", mounts="back",
  sockets=["vfx_sparks@front", "conveyor_large@back"], moving=["Saw disc spins"], vfx=["Sparks"], audio=["Grinding"],
  notes="Circular saw head.")

P("UTL", "Drill", "Ship Tools", {"LG": (3, 3, 4), "SG": (1, 1, 3)}, tier="T2", cls="L",
  mass={"LG": 22000, "SG": 800}, hp={"LG": 8000, "SG": 700}, power={"LG": -2000, "SG": -150},
  recipe={"LG": {"steel_plate": 300, "construction_component": 40, "large_tube": 12, "motor": 5, "computer": 5}},
  function="Mines voxel terrain into ore.", mounts="back",
  sockets=["vfx_sparks@front", "conveyor_large@back", "item_in@front"], moving=["Drill head spins", "Cutter teeth"],
  vfx=["Rock debris", "Dust"], audio=["Drilling"], notes="Conical head with cutter teeth; the mining sphere is 2× the head size.")

P("UTL", "Suit Station", "Service", LG_SG_1, tier="T1", cls="M",
  mass={"LG": 300, "SG": 30}, hp={"LG": 600, "SG": 80}, power={"LG": -20, "SG": -2},
  recipe={"LG": {"interior_plate": 6, "small_tube": 4, "power_cell": 2, "computer": 2}},
  function="Refills suit O₂, hydrogen and energy; swaps suit modules.", mounts="back", shape="wall",
  moving=["Hose reels ×2"], sockets=["interact@front", "air@back", "fuel@back"], emissive=["Refill gauges ×3"],
  audio=["Refill hiss"], notes="Wall unit with two hoses and three gauges (O₂ blue, H₂ red, energy yellow).")

# ---------------------------------------------------------------------------
# SOW — Precursor (Sower)
# ---------------------------------------------------------------------------
SOWER = ("Sower modeling rules (chapter 19): no straight edges longer than 0.5 m, ribbed and shell-like surfaces, "
         "bioluminescent teal glyph emissives with a slow 'breathing' pulse.")

P("SOW", "Sower Jump Core", "Drives", {"LG": (3, 3, 5)}, tier="T4", art="SOW", cls="XL",
  mass=60000, hp=12000, power=-50000,
  recipe={"sower_filament": 60, "resonance_crystal": 40, "superconductor": 200, "steel_plate": 300},
  function="Jumps the grid along a Sower jump lane. Needs 50 MW to charge, cooling, and Resonance Crystal fuel. 5 min cooldown.",
  stats={"range": "1 jump lane", "cooldown_s": 300, "charge_mw": 50},
  unlock="Recovered at the Styx Wreck (M2.07); a replica can be grown at T4.",
  mounts="all", airtight="all",
  moving=["Nested rings ×3: rotate on different axes, speed with charge", "Core petals: open during a jump"],
  sockets=["interact@left", "work@left", "vfx_exhaust@center"],
  emissive=["Glyph bands (teal)", "Core light (white → violet during a jump)"],
  vfx=["Charge motes", "Jump flash", "Space tear"], audio=["Choral charge swell", "Jump boom"],
  notes=SOWER + " The most important hero asset in the parts list. Human mounting cradle (Industrial) is a separate mesh around it.")

P("SOW", "Loom Node", "Fabrication", {"LG": (2, 2, 2)}, tier="T4", art="SOW", cls="L",
  mass=12000, hp=6000, power=-2000,
  recipe={"sower_filament": 30, "resonance_crystal": 10, "medical_component": 20},
  function="Grows precursor tech and Loom Serum.", mounts="bottom",
  moving=["Weaving filaments: animated (vertex animation texture)"], sockets=["work@front", "interact@front", "item_out@front"],
  emissive=["Filament glow"], vfx=["Floating motes"], audio=["Soft chorus"],
  notes=SOWER + " A cradle of filaments weaving in the air above a shell basin.")

P("SOW", "Resonance Cell", "Power", {"LG": (2, 2, 2)}, tier="T4", art="SOW", cls="L",
  mass=15000, hp=5000, power=150000,
  recipe={"sower_filament": 40, "resonance_crystal": 20, "superconductor": 60},
  function="150 MW from Resonance Crystals. Silent (no Attraction).", mounts="all", airtight="all",
  moving=["Crystal core: slow rotation"], sockets=["conveyor_large@bottom"], emissive=["Crystal glow (teal)"], audio=["Crystal hum"],
  notes=SOWER + " A pulsing crystal inside a shell lattice.")

P("SOW", "Resonance Amplifier", "Utility", {"LG": (1, 2, 1)}, tier="T4", art="SOW", cls="M",
  mass=6000, hp=3000, power=-5000,
  recipe={"sower_filament": 20, "resonance_crystal": 8},
  function="+1 jump lane of range, or ×3 scanner range when attached to a Scanner Array.",
  mounts="bottom", moving=["Fins fan open"], emissive=["Glyph fins"], vfx=["Ripple rings"], notes=SOWER)

P("SOW", "Glyph-Lock Door", "Access", LG_1, tier="T4", art="SOW", cls="M",
  mass=3000, hp=6000, power=-1,
  recipe={"sower_filament": 10, "steel_plate": 20},
  function="Iris door that opens for a chosen glyph sequence (buildable after the first glyph set).",
  mounts="all", airtight="all",
  moving=["Iris petals ×8: rotate open, 1.2 s"], sockets=["interact@front", "door@center"],
  emissive=["Glyph ring (teal)"], audio=["Stone-and-breath open"], notes=SOWER)

P("SOW", "Living Hull", "Structure", LG_SG_1, tier="T5", art="SOW", cls="S",
  mass={"LG": 700, "SG": 30}, hp={"LG": 2400, "SG": 100},
  recipe={"LG": {"living_alloy": 20}, "SG": {"living_alloy": 1}},
  function="Post-game (EXODUS): hull that grows and self-repairs 1% HP per second.",
  unlock="EXODUS ending (T5).", mounts="all", airtight="all",
  emissive=["Vein glow when repairing"],
  notes=SOWER + " Must tile like armor despite organic surfaces: flat mating faces with an organic outer skin.",
  variants=[V("Block"), V("Slope", shape="slope", mass_mult=0.5, hp_mult=0.5), V("Corner", shape="corner", mass_mult=0.17, hp_mult=0.17)])

P("SOW", "Bloom-Grown Wall", "Structure", LG_1, tier="T5", art="SOW", cls="S",
  mass=500, hp=2000, recipe={"organics": 30, "sower_filament": 2},
  function="Post-game (COMMUNE): walls grown by tamed Bloom. Purify air slowly.",
  unlock="COMMUNE ending (T5).", mounts="all", airtight="all",
  emissive=["Soft bioluminescent spots"], vfx=["Occasional spore drift (harmless)"],
  notes=SOWER + " Green-and-violet Bloom surfaces instead of teal; clearly 'tamed' (flowers, not fungus).")
