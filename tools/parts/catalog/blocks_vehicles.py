"""PRO — Propulsion, Flight & Launch, MEC — Mechanical, CTL — Control & Automation."""

from . import P, V

LG_1 = {"LG": (1, 1, 1)}
LG_SG_1 = {"LG": (1, 1, 1), "SG": (1, 1, 1)}

THRUSTER_NOTE = ("Nozzle on the front face (+X pushes the grid toward −X). Flame VFX socket at the nozzle exit. "
                 "Thruster damage cone: 3× nozzle length behind the exhaust; keep it clear of the mesh.")

# ---------------------------------------------------------------------------
# PRO — Thrusters
# ---------------------------------------------------------------------------
P("PRO", "Atmospheric Thruster", "Thrusters", {"LG": (1, 1, 2), "SG": (1, 1, 1)}, tier="T2", cls="M",
  mass={"LG": 4000, "SG": 700}, hp={"LG": 3000, "SG": 400}, power={"LG": -6000, "SG": -600},
  recipe={"LG": {"steel_plate": 35, "construction_component": 50, "large_tube": 8, "metal_grid": 40, "motor": 90}},
  function="Electric propeller thruster; only works in atmosphere (efficiency falls with air density). 650 kN (LG) / 96 kN (SG).",
  stats={"thrust_kn": {"LG": 650, "SG": 96}},
  mounts="back", airtight="none", shape="cylinder",
  moving=["Fan blades: spin with throttle (up to 1,800 rpm)"],
  sockets=["vfx_exhaust@front", "audio@center"], vfx=["Air distortion", "Dust kick-up near ground"],
  audio=["Rotor roar (pitch follows throttle)"], notes=THRUSTER_NOTE)

P("PRO", "Large Atmospheric Thruster", "Thrusters", {"LG": (3, 3, 4), "SG": (3, 3, 3)}, tier="T2", cls="L",
  mass={"LG": 33000, "SG": 4000}, hp={"LG": 12000, "SG": 1500}, power={"LG": -16000, "SG": -2400},
  recipe={"LG": {"steel_plate": 230, "construction_component": 60, "large_tube": 50, "metal_grid": 40, "motor": 1100}},
  function="Heavy atmospheric lift. 6.5 MN (LG) / 960 kN (SG).", stats={"thrust_kn": {"LG": 6500, "SG": 960}},
  mounts="back", airtight="none", shape="cylinder",
  moving=["Fan blades ×2 stages, counter-rotating"], sockets=["vfx_exhaust@front", "audio@center"],
  vfx=["Air distortion", "Dust storm near ground"], audio=["Deep rotor roar"], notes=THRUSTER_NOTE)

P("PRO", "Ion Thruster", "Thrusters", LG_SG_1, tier="T2", cls="M",
  mass={"LG": 4300, "SG": 120}, hp={"LG": 3000, "SG": 200}, power={"LG": -3400, "SG": -200},
  recipe={"LG": {"steel_plate": 25, "construction_component": 60, "large_tube": 8, "thruster_component": 80}},
  function="Electric vacuum thruster; useless in atmosphere. 145 kN (LG) / 14.4 kN (SG).",
  stats={"thrust_kn": {"LG": 145, "SG": 14.4}},
  mounts="back", airtight="none",
  sockets=["vfx_exhaust@front"], emissive=["Blue glow ring (throttle-driven)"], vfx=["Blue ion plume"],
  audio=["Electric hum"], notes=THRUSTER_NOTE)

P("PRO", "Large Ion Thruster", "Thrusters", {"LG": (3, 3, 2), "SG": (3, 3, 3)}, tier="T3", cls="L",
  mass={"LG": 43200, "SG": 720}, hp={"LG": 12000, "SG": 800}, power={"LG": -33600, "SG": -2400},
  recipe={"LG": {"steel_plate": 150, "construction_component": 100, "large_tube": 40, "thruster_component": 960}},
  function="Main vacuum engine for capital ships. 4.3 MN (LG) / 172 kN (SG).", stats={"thrust_kn": {"LG": 4300, "SG": 172}},
  mounts="back", airtight="none",
  sockets=["vfx_exhaust@front"], emissive=["Blue glow ring"], vfx=["Blue ion plume (large)"], audio=["Deep electric hum"],
  notes=THRUSTER_NOTE)

P("PRO", "Hydrogen Thruster", "Thrusters", {"LG": (1, 1, 2), "SG": (1, 1, 2)}, tier="T2", cls="M",
  mass={"LG": 6900, "SG": 334}, hp={"LG": 4000, "SG": 300},
  recipe={"LG": {"steel_plate": 30, "construction_component": 60, "metal_grid": 8, "large_tube": 25}},
  function="Burns hydrogen: strong everywhere (atmosphere and vacuum) but fuel-hungry. 1.1 MN (LG) / 98 kN (SG).",
  stats={"thrust_kn": {"LG": 1100, "SG": 98}, "fuel": "hydrogen"},
  mounts="back", airtight="none",
  sockets=["vfx_exhaust@front", "fuel@back"], emissive=["Nozzle heat glow"], vfx=["Orange-white flame plume", "Heat shimmer"],
  audio=["Rocket roar"], notes=THRUSTER_NOTE)

P("PRO", "Large Hydrogen Thruster", "Thrusters", {"LG": (3, 3, 4), "SG": (3, 3, 3)}, tier="T3", cls="L",
  mass={"LG": 40000, "SG": 1420}, hp={"LG": 14000, "SG": 1000},
  recipe={"LG": {"steel_plate": 150, "construction_component": 180, "metal_grid": 250, "large_tube": 40}},
  function="Heavy hydrogen lift for capital ships and launches. 7.2 MN (LG) / 400 kN (SG).",
  stats={"thrust_kn": {"LG": 7200, "SG": 400}, "fuel": "hydrogen"},
  mounts="back", airtight="none",
  sockets=["vfx_exhaust@front", "fuel@back"], emissive=["Nozzle heat glow"], vfx=["Large flame plume", "Shock diamonds"],
  audio=["Heavy rocket roar"], notes=THRUSTER_NOTE)

P("PRO", "RCS Thruster Quad", "Thrusters", {"SG": (1, 1, 1)}, tier="T2", cls="S",
  mass=40, hp=60, recipe={"SG": {"steel_plate": 2, "thruster_component": 2, "small_tube": 2}},
  function="Four tiny cold-gas nozzles for precise docking and landing corrections (2 kN each).",
  mounts="back", airtight="none",
  sockets=["vfx_exhaust@front", "vfx_exhaust@top", "vfx_exhaust@left", "vfx_exhaust@right"], vfx=["White gas puffs"],
  audio=["Short hiss"], notes="Classic four-nozzle cluster on a small base plate.")

P("PRO", "Gyroscope", "Control Moment", LG_SG_1, tier="T1", cls="M",
  mass={"LG": 3500, "SG": 100}, hp={"LG": 2000, "SG": 200}, power={"LG": -30, "SG": -1},
  recipe={"LG": {"steel_plate": 600, "construction_component": 40, "large_tube": 4, "metal_grid": 50, "motor": 4, "computer": 5}},
  function="Provides rotation authority. Heavy ships need many.", stats={"torque_mnm": {"LG": 3.36, "SG": 0.45}},
  mounts="all", airtight="all",
  moving=["Flywheel: spins with demand", "Gimbal rings ×2: tilt"], emissive=["Status ring"], audio=["Rising whine"],
  notes="Visible flywheel behind a cage on two faces.")

# ---------------------------------------------------------------------------
# PRO — Ground & landing
# ---------------------------------------------------------------------------
P("PRO", "Wheel Suspension", "Ground", LG_SG_1, tier="T1", cls="M",
  mass={"LG": 700, "SG": 60}, hp={"LG": 1500, "SG": 150}, power={"LG": -20, "SG": -2},
  recipe={"LG": {"steel_plate": 25, "construction_component": 15, "large_tube": 6, "small_tube": 12, "motor": 6}},
  function="Suspension, motor and wheel for rovers. The Mule rover in M1.05 uses the SG 3×3.",
  mounts="back", airtight="none",
  moving=["Wheel: spins; steers ±35°", "Suspension arm: travels 0.3/1.0/1.6 m (by size)"],
  sockets=["wheel@left", "attach_top@left"], vfx=["Dust/mud spray"], audio=["Motor whine", "Tire rumble"],
  notes="Wheel and suspension are separate meshes. Tire tread normal map scrolls with speed; the tire bulges under load (vertex shader).",
  variants=[V("1×1"), V("3×3", grids={"LG": (1, 3, 3), "SG": (1, 3, 3)}, mass_mult=2.2, hp_mult=1.8),
            V("5×5", grids={"LG": (1, 5, 5), "SG": (1, 5, 5)}, mass_mult=4.0, hp_mult=3.0)])

P("PRO", "Landing Gear", "Landing", LG_SG_1, tier="T1", cls="M",
  mass={"LG": 700, "SG": 40}, hp={"LG": 1500, "SG": 150}, power={"LG": -0.1, "SG": -0.01},
  recipe={"LG": {"steel_plate": 150, "construction_component": 20, "motor": 6}},
  function="Magnetic landing pad; locks the grid to terrain, stations or other ships.",
  mounts="back", airtight="none", shape="flat",
  moving=["Pad: articulates ±15°", "Lock clamps ×4"], emissive=["Lock status: yellow ready / green locked"],
  audio=["Magnet thunk"], notes="Flat pad on a short strut, facing the front face.")

P("PRO", "Landing Leg", "Landing", {"LG": (1, 2, 1), "SG": (1, 3, 1)}, tier="T2", cls="M",
  mass={"LG": 1500, "SG": 120}, hp={"LG": 2500, "SG": 250}, power={"LG": -2, "SG": -0.2},
  recipe={"LG": {"steel_plate": 40, "construction_component": 20, "motor": 8, "large_tube": 4}},
  function="Hydraulic landing leg: extends 1.5 m (LG) / 0.8 m (SG), self-levels on uneven ground.",
  mounts="top", airtight="none",
  moving=["Upper strut", "Lower strut: telescopes", "Foot pad: ±25° ball joint"],
  sockets=["attach_top@top"], audio=["Hydraulic hiss"], notes="Rig pivots: PART_Hip, PART_Strut, PART_Foot.")

P("PRO", "Parachute Hatch", "Landing", LG_SG_1, tier="T1", cls="S",
  mass={"LG": 500, "SG": 40}, hp={"LG": 800, "SG": 80},
  recipe={"LG": {"steel_plate": 20, "construction_component": 10, "fabric": 40, "motor": 1}},
  function="Deploys a canopy for atmospheric descent (Earth returns, Veyra-4).",
  mounts="all", airtight="all",
  moving=["Hatch lid: pops 120°", "Canopy: cloth sim or pre-animated skeletal canopy"],
  vfx=["Deploy puff"], notes="Canopy is a separate skeletal mesh SK_PRO_ParachuteCanopy (shared by both grids, scaled).")

P("PRO", "Wing", "Aerodynamics", LG_SG_1, tier="T2", cls="S",
  mass={"LG": 900, "SG": 40}, hp={"LG": 1200, "SG": 100},
  recipe={"LG": {"steel_plate": 20, "girder": 6, "construction_component": 4}},
  function="Generates lift in atmosphere (optional aerodynamics system).",
  mounts="back,left,right", airtight="none", shape="flat",
  notes="Airfoil profile 0.4 m thick (LG). Leading edge on the front face.",
  variants=[V("1×1"), V("2×1", grids={"LG": (2, 1, 1), "SG": (2, 1, 1)}, mass_mult=2, hp_mult=2),
            V("3×1", grids={"LG": (3, 1, 1), "SG": (3, 1, 1)}, mass_mult=3, hp_mult=3),
            V("Tip", mass_mult=0.6, hp_mult=0.6)])

P("PRO", "Elevon", "Aerodynamics", LG_SG_1, tier="T2", cls="S",
  mass={"LG": 700, "SG": 30}, hp={"LG": 900, "SG": 80}, power={"LG": -1, "SG": -0.1},
  recipe={"LG": {"steel_plate": 14, "motor": 2, "construction_component": 4}},
  function="Moving control surface for pitch and roll in atmosphere.", mounts="front,left,right", shape="flat",
  moving=["Surface: hinges ±30° at the front edge"], notes="Matches the Wing profile at its hinge line.")

# ---------------------------------------------------------------------------
# PRO — Drives & fuel
# ---------------------------------------------------------------------------
P("PRO", "Pulse Drive", "Drives", {"LG": (3, 3, 5)}, tier="T3", cls="XL",
  mass=45000, hp=10000, power=-25000,
  recipe={"steel_plate": 400, "superconductor": 200, "thruster_component": 200, "computer": 80, "large_tube": 40},
  function="In-system cruise drive: planet to planet in minutes. Interrupted by gravity wells and events.",
  mounts="all", airtight="all",
  moving=["Magnetic rings ×3: counter-rotate, speed with charge"],
  sockets=["interact@left", "work@left"], emissive=["Ring charge glow (white-violet)"],
  vfx=["Space-distortion tunnel when engaged"], audio=["Charge spool", "Engage boom"],
  notes="Three stacked rings around a central core, visible through open side bays.")

P("PRO", "Small Hydrogen Tank", "Fuel", LG_SG_1, tier="T2", cls="S",
  mass={"LG": 2400, "SG": 110}, hp={"LG": 2500, "SG": 200},
  recipe={"LG": {"steel_plate": 80, "large_tube": 40, "small_tube": 60, "computer": 8, "construction_component": 40}},
  function="Stores 1,000,000 L (LG) / 15,000 L (SG) of hydrogen.", shape="cylinder",
  mounts="all", airtight="all", sockets=["fuel@top", "fuel@bottom"], emissive=["Fill gauge"],
  notes="White tank with red H₂ band.")

P("PRO", "Large Hydrogen Tank", "Fuel", {"LG": (3, 3, 3), "SG": (3, 3, 3)}, tier="T2", cls="M",
  mass={"LG": 20000, "SG": 800}, hp={"LG": 12000, "SG": 1200},
  recipe={"LG": {"steel_plate": 280, "large_tube": 80, "small_tube": 60, "computer": 8, "construction_component": 40}},
  function="Stores 15,000,000 L (LG) / 500,000 L (SG) of hydrogen.", shape="cylinder",
  mounts="all", airtight="all", sockets=["fuel@top", "fuel@bottom", "fuel@back"], emissive=["Fill gauge"],
  notes="Spherical tank inside a square frame.")

# ---------------------------------------------------------------------------
# PRO — Act I launch hardware (the Wren)
# ---------------------------------------------------------------------------
P("PRO", "Methalox Rocket Engine", "Launch Hardware", {"LG": (1, 1, 2)}, tier="T1", cls="L",
  mass=1800, hp=2500,
  recipe={"steel_plate": 30, "thruster_component": 20, "large_tube": 12, "motor": 4, "computer": 2},
  function="Kestrel's launch engine: 2.2 MN burning methane and liquid oxygen. Powers the Wren (M1.07).",
  stats={"thrust_kn": 2200, "fuel": "methane + LOX"},
  unlock="Found in Hangar 4 (prologue); buildable T2.",
  mounts="back", airtight="none",
  moving=["Nozzle: gimbals ±8° (2 axes)"], sockets=["vfx_exhaust@front", "fuel@back*2"],
  emissive=["Nozzle heat glow"], vfx=["Blue-orange methalox plume", "Shock diamonds", "Launch smoke"],
  audio=["Launch roar"], notes="Regeneratively cooled bell with visible plumbing. Gimbal pivot at the throat (PART_Gimbal).")

P("PRO", "Methalox Tank", "Launch Hardware", LG_1, tier="T1", cls="S",
  mass=800, hp=1200, recipe={"steel_plate": 30, "large_tube": 6, "small_tube": 10},
  function="Stores methane and LOX for rocket engines (from the Fuel Farm, M1.05).", shape="cylinder",
  mounts="all", airtight="all", sockets=["fuel@top", "fuel@bottom"], vfx=["LOX boil-off vapor"],
  notes="Frost on the LOX half (vertex-color mask). Kestrel logo decal.",
  variants=[V("Short"), V("Tall", grids={"LG": (1, 3, 1)}, mass_mult=3, hp_mult=2.5)])

P("PRO", "Stage Separator", "Launch Hardware", LG_SG_1, tier="T1", cls="S",
  mass={"LG": 400, "SG": 20}, hp={"LG": 600, "SG": 60},
  recipe={"LG": {"steel_plate": 10, "explosives": 2, "construction_component": 4}},
  function="Explosive-bolt ring that splits a grid into two stages.",
  mounts="top,bottom", airtight="none",
  moving=["Separation ring halves: push apart on springs"], vfx=["Pyro flash ring", "Debris bolts"], audio=["Bang"],
  notes="Thin ring (0.5 m LG). Top and bottom halves are separate meshes that become separate grids.")

P("PRO", "Launch Clamp", "Launch Hardware", {"LG": (1, 3, 1)}, tier="T1", cls="M",
  mass=6000, hp=5000, recipe={"steel_plate": 60, "girder": 20, "motor": 4},
  function="Tower arm that holds a rocket until launch. It jams in M1.07 unless you built the automated release.",
  mounts="bottom,back", airtight="none",
  moving=["Clamp arm: retracts 90°, 1.5 s", "Manual release lever (Tug's lever)"],
  sockets=["interact@front"], vfx=["Pneumatic vent"],
  notes="Two assets: SM_PRO_LaunchClamp (manual lever) and the 'Automated' variant with a pneumatic actuator — the hidden engineering solution that saves Tug.",
  variants=[V("Manual"), V("Automated", recipe={"LG": {"steel_plate": 60, "girder": 20, "motor": 6, "computer": 2}})])

P("PRO", "Heat Shield", "Launch Hardware", LG_SG_1, tier="T1", cls="S",
  mass={"LG": 800, "SG": 30}, hp={"LG": 1200, "SG": 80},
  recipe={"LG": {"steel_plate": 10, "heat_shield_tile": 25}, "SG": {"heat_shield_tile": 2}},
  function="Ablative tiles that survive re-entry heat. Collected from the Township warehouse (M1.05).",
  mounts="all", airtight="all",
  notes="Black hexagonal tile pattern; char and ablation driven by a 'Burn' parameter after re-entry.",
  variants=[V("Block"), V("Slope", shape="slope", mass_mult=0.5, hp_mult=0.5), V("Corner", shape="corner", mass_mult=0.2, hp_mult=0.2)])

P("PRO", "Aerodynamic Fairing", "Launch Hardware", LG_SG_1, tier="T1", cls="S",
  mass={"LG": 300, "SG": 12}, hp={"LG": 500, "SG": 40},
  recipe={"LG": {"steel_plate": 6, "bio_plastic": 6}},
  function="Smooth cover for launch stacks; reduces drag.", mounts="back,bottom", airtight="none",
  notes="Shares the Round Slope profile.",
  variants=[V("Straight", shape="round_slope"), V("Nose Cone", shape="round_corner")])

# ---------------------------------------------------------------------------
# MEC — Mechanical
# ---------------------------------------------------------------------------
P("MEC", "Rotor", "Rotation", LG_SG_1, tier="T2", cls="M",
  mass={"LG": 1200, "SG": 60}, hp={"LG": 2000, "SG": 200}, power={"LG": -10, "SG": -1},
  recipe={"LG": {"steel_plate": 15, "construction_component": 10, "large_tube": 4, "motor": 4, "computer": 2}},
  function="Rotating joint; the head is a separate sub-grid. Unlimited rotation.",
  mounts="bottom", airtight="none",
  moving=["Rotor head: rotates about Z, unlimited"], sockets=["attach_top@top"],
  emissive=["Lock indicator"], audio=["Servo hum"], notes="Two assets per grid: the base (this part) and SM_MEC_RotorHead_*.")

P("MEC", "Advanced Rotor", "Rotation", LG_SG_1, tier="T3", cls="M",
  mass={"LG": 1600, "SG": 80}, hp={"LG": 2400, "SG": 240}, power={"LG": -12, "SG": -1.2},
  recipe={"LG": {"steel_plate": 20, "construction_component": 12, "large_tube": 6, "motor": 6, "computer": 4}},
  function="Rotor with a hollow center: conveyors and air pass through the joint.",
  mounts="bottom", airtight="none",
  moving=["Rotor head: rotates about Z"], sockets=["attach_top@top", "conveyor_large@bottom", "conveyor_large@top"],
  notes="Ring bearing with a visible open core.")

P("MEC", "Hinge", "Rotation", LG_SG_1, tier="T2", cls="M",
  mass={"LG": 1000, "SG": 50}, hp={"LG": 1800, "SG": 180}, power={"LG": -8, "SG": -0.8},
  recipe={"LG": {"steel_plate": 12, "construction_component": 10, "large_tube": 4, "motor": 4, "computer": 2}},
  function="Hinged joint (±90°) for doors, ramps, landing gear and cranes.",
  mounts="bottom", airtight="none",
  moving=["Hinge leaf: rotates about Y, ±90°"], sockets=["attach_top@top"], notes="Knuckle hinge with a visible pin.")

P("MEC", "Piston", "Linear", LG_SG_1, tier="T2", cls="M",
  mass={"LG": 1400, "SG": 70}, hp={"LG": 2000, "SG": 200}, power={"LG": -12, "SG": -1},
  recipe={"LG": {"steel_plate": 15, "construction_component": 10, "large_tube": 4, "motor": 4, "computer": 2}},
  function="Linear actuator: extends 10 m (LG) / 2 m (SG).",
  mounts="bottom", airtight="none",
  moving=["Telescoping sections ×3", "Piston head"], sockets=["attach_top@top"], audio=["Hydraulic whine"],
  notes="Collapsed length fits the cell; each section is a separate PART_ mesh.")

P("MEC", "Merge Block", "Joining", LG_SG_1, tier="T2", cls="S",
  mass={"LG": 900, "SG": 40}, hp={"LG": 1500, "SG": 120}, power={"LG": -0.5, "SG": -0.05},
  recipe={"LG": {"steel_plate": 12, "construction_component": 15, "motor": 2, "large_tube": 6, "computer": 2}},
  function="Magnetically merges two grids into one.", mounts="all", airtight="all",
  emissive=["Alignment arrows (yellow → green)"], vfx=["Magnetic shimmer"],
  notes="The merge face has a clear alignment arrow; the opposite face is plain.")

P("MEC", "Habitat Ring Bearing", "Rotation", {"LG": (3, 3, 3)}, tier="T3", cls="L",
  mass=30000, hp=12000, power=-200,
  recipe={"steel_plate": 300, "large_tube": 40, "motor": 60, "computer": 10, "superconductor": 10},
  function="Large-diameter spin bearing for rotating habitat rings (spin gravity). Air, people and conveyors pass through its core.",
  mounts="bottom,top", airtight="all",
  moving=["Outer race: rotates about Z"], sockets=["attach_top@top", "air@top", "air@bottom", "conveyor_large@top", "conveyor_large@bottom"],
  emissive=["Rotation-speed ring lights"], audio=["Low rumble"],
  notes="A walkable 2.5 m core tunnel through the bearing; ladder rungs inside.")

# ---------------------------------------------------------------------------
# CTL — Control & Automation
# ---------------------------------------------------------------------------
P("CTL", "Flight Seat", "Seats & Cockpits", {"LG": (1, 1, 1), "SG": (1, 2, 2)}, tier="T1", cls="M",
  mass={"LG": 400, "SG": 60}, hp={"LG": 500, "SG": 100},
  recipe={"LG": {"interior_plate": 20, "construction_component": 20, "motor": 1, "display": 4, "computer": 20}},
  function="Open-frame seat that controls a grid. No pressurization: suits required in vacuum.",
  mounts="bottom,back", airtight="none",
  sockets=["seat@center", "lcd@front", "interact@center"], emissive=["Control screens"],
  notes="Joystick + throttle meshes animate with input (PART_Stick, PART_Throttle).")

P("CTL", "Industrial Cockpit", "Seats & Cockpits", {"LG": (3, 2, 3), "SG": (3, 3, 4)}, tier="T2", cls="L",
  mass={"LG": 7000, "SG": 800}, hp={"LG": 6000, "SG": 800},
  recipe={"LG": {"steel_plate": 30, "construction_component": 20, "motor": 2, "display": 10, "computer": 100, "glass_panel": 60}},
  function="Pressurized two-seat cockpit with wide glass. The standard utility-ship cockpit.",
  mounts="back,bottom,left,right", airtight="all",
  sockets=["seat@center*2", "lcd@front*4", "interact@center", "light@top"],
  emissive=["Instrument panels", "Cabin light"],
  notes="Interior is fully modeled (first-person). Glass uses the cockpit glass material with dirt and condensation.")

P("CTL", "Fighter Cockpit", "Seats & Cockpits", {"SG": (3, 3, 5)}, tier="T2", cls="L",
  mass=900, hp=900, recipe={"SG": {"steel_plate": 20, "construction_component": 20, "motor": 1, "display": 4, "computer": 20, "glass_panel": 20}},
  function="Single-seat pressurized cockpit for small ships.", mounts="back,bottom", airtight="all",
  moving=["Canopy: hinges back 70°"], sockets=["seat@center", "lcd@front*3", "interact@center"],
  emissive=["HUD glass projection", "Instrument panels"], notes="HUD projection plane on the canopy (lcd socket).")

P("CTL", "Capsule Cockpit", "Seats & Cockpits", {"LG": (3, 2, 3)}, tier="T1", cls="XL",
  mass=6500, hp=5000,
  recipe={"steel_plate": 40, "heat_shield_tile": 30, "interior_plate": 20, "display": 8, "computer": 40, "glass_panel": 6},
  function="The Wren crew capsule: six seats, heat-shielded base, pressurized. The survivors' ride to orbit (M1.07).",
  unlock="The Wren (prologue); buildable T2.",
  mounts="bottom,top", airtight="all",
  sockets=["seat@center*6", "lcd@front*3", "interact@center", "light@top"],
  emissive=["Instrument panels", "Warning lights"],
  notes="Hero asset. The six seats face up (launch posture). Hand-painted Kestrel mission patch and crew-signature decals.")

P("CTL", "Passenger Seat", "Seats & Cockpits", {"LG": (1, 1, 1), "SG": (1, 2, 2)}, tier="T1", cls="S",
  mass={"LG": 150, "SG": 30}, hp={"LG": 300, "SG": 60},
  recipe={"LG": {"interior_plate": 10, "construction_component": 6, "fabric": 4}},
  function="Seat for survivors during flights; keeps them safe from high G.",
  mounts="bottom,back", sockets=["seat@center"], notes="5-point harness; padded shell.")

P("CTL", "Bridge Console", "Consoles", {"LG": (2, 1, 1)}, tier="T3", cls="L",
  mass=900, hp=1200, power=-2,
  recipe={"interior_plate": 20, "computer": 60, "display": 12, "construction_component": 10},
  function="Captain's station for capital ships; controls the grid and shows ship systems.",
  mounts="bottom", sockets=["seat@center", "lcd@front*3", "interact@center", "projector@top"],
  emissive=["Three curved screens", "Button backlights"], notes="Curved desk with a holo emitter on top.")

P("CTL", "Holo Map Table", "Consoles", {"LG": (2, 1, 2)}, tier="T3", cls="L",
  mass=1200, hp=1000, power=-4,
  recipe={"interior_plate": 20, "computer": 40, "display": 4, "detector_component": 4},
  function="Hologram galaxy map for jump planning and briefings (the M2.07 star-map moment).",
  mounts="bottom", sockets=["projector@top", "work@front*4", "interact@front"],
  emissive=["Table edge lights", "Hologram (VFX)"], vfx=["Star-map hologram"],
  notes="Round table; the hologram volume is 3 m tall above it.")

P("CTL", "Guidance Computer", "Automation", LG_SG_1, tier="T1", cls="M",
  mass={"LG": 200, "SG": 20}, hp={"LG": 400, "SG": 60}, power={"LG": -1, "SG": -0.1},
  recipe={"LG": {"interior_plate": 4, "computer": 20, "display": 2, "radio_component": 2}},
  function="Autopilot for landing, docking and orbit. One of the four Wren parts (Mission Control, M1.05).",
  mounts="all", airtight="all", sockets=["interact@front", "lcd@front"], emissive=["Status display"],
  notes="Rack-mounted flight computer with a small screen and blinking status LEDs.")

P("CTL", "Remote Control", "Automation", LG_SG_1, tier="T2", cls="S",
  mass={"LG": 150, "SG": 10}, hp={"LG": 300, "SG": 40}, power={"LG": -0.1, "SG": -0.01},
  recipe={"LG": {"interior_plate": 10, "construction_component": 10, "motor": 1, "computer": 15}},
  function="Lets the player (or drones' AI) control a grid remotely.", mounts="all", airtight="all",
  sockets=["interact@front"], emissive=["Antenna LED"], notes="Small box with an antenna stub.")

P("CTL", "Control Terminal", "Automation", LG_SG_1, tier="T1", cls="S",
  mass={"LG": 60, "SG": 5}, hp={"LG": 200, "SG": 30}, power={"LG": -0.2, "SG": -0.02},
  recipe={"LG": {"interior_plate": 4, "computer": 4, "display": 2}},
  function="Wall terminal that opens the grid's full control panel.", mounts="back", shape="wall",
  sockets=["interact@front", "lcd@front"], emissive=["Screen"], notes="Angled wall screen with a keyboard shelf.")

P("CTL", "Button Panel", "Automation", LG_SG_1, tier="T1", cls="S",
  mass={"LG": 40, "SG": 3}, hp={"LG": 150, "SG": 20},
  recipe={"LG": {"interior_plate": 2, "construction_component": 2, "computer": 1}},
  function="Four programmable buttons with labels.", mounts="back", shape="wall",
  moving=["Buttons ×4: press 5 mm"], sockets=["interact@front", "lcd@front"], emissive=["Button backlights ×4"],
  notes="Label strips are dynamic text surfaces.")

P("CTL", "Timer Block", "Automation", LG_SG_1, tier="T2", cls="S",
  mass={"LG": 300, "SG": 15}, hp={"LG": 400, "SG": 50}, power={"LG": -0.1, "SG": -0.01},
  recipe={"LG": {"interior_plate": 6, "construction_component": 30, "computer": 5}},
  function="Runs a list of actions after a delay.", mounts="all", airtight="all",
  sockets=["interact@front"], emissive=["Countdown digits"], notes="Shares the logic-block shell with Event Controller and Sensor.")

P("CTL", "Event Controller", "Automation", LG_SG_1, tier="T2", cls="S",
  mass={"LG": 300, "SG": 15}, hp={"LG": 400, "SG": 50}, power={"LG": -0.1, "SG": -0.01},
  recipe={"LG": {"interior_plate": 6, "construction_component": 30, "computer": 10}},
  function="No-code logic: 'when X happens, do Y' (e.g., Hollows within 50 m → close blast doors).",
  mounts="all", airtight="all", sockets=["interact@front"], emissive=["Condition LEDs"], notes="Logic-block shell, green trim.")

P("CTL", "Sensor", "Automation", LG_SG_1, tier="T2", cls="S",
  mass={"LG": 300, "SG": 15}, hp={"LG": 400, "SG": 50}, power={"LG": -0.5, "SG": -0.05},
  recipe={"LG": {"interior_plate": 6, "construction_component": 8, "computer": 6, "radio_component": 6, "detector_component": 6}},
  function="Detects players, survivors, Hollows, ships and objects in a configurable box (up to 50 m).",
  mounts="back", sockets=["camera@front"], emissive=["Detection LED"], notes="Dome sensor on a short stalk.")

P("CTL", "Programmable Block", "Automation", LG_SG_1, tier="T3", cls="S",
  mass={"LG": 400, "SG": 20}, hp={"LG": 500, "SG": 60}, power={"LG": -0.5, "SG": -0.05},
  recipe={"LG": {"interior_plate": 20, "construction_component": 30, "large_tube": 2, "motor": 2, "display": 1, "computer": 2}},
  function="Runs sandboxed Lua scripts for advanced automation.", mounts="all", airtight="all",
  sockets=["interact@front", "lcd@front"], emissive=["Code-scroll screen"], notes="Logic-block shell, blue trim, small screen.")

P("CTL", "LCD Panel", "Displays", LG_SG_1, tier="T1", cls="S",
  mass={"LG": 60, "SG": 4}, hp={"LG": 150, "SG": 20}, power={"LG": -0.1, "SG": -0.01},
  recipe={"LG": {"interior_plate": 1, "construction_component": 6, "display": 10}},
  function="Shows text, images, gauges or camera feeds.", mounts="back", shape="panel",
  sockets=["lcd@front"], emissive=["Screen"], notes="Screen UVs 0–1 with a 16:9 or 1:1 aspect per variant.",
  variants=[V("1×1"), V("Wide 2×1", grids={"LG": (2, 1, 1), "SG": (2, 1, 1)}, mass_mult=2, hp_mult=2), V("Corner")])

P("CTL", "Sound Block", "Displays", LG_SG_1, tier="T1", cls="S",
  mass={"LG": 80, "SG": 5}, hp={"LG": 200, "SG": 30}, power={"LG": -0.1, "SG": -0.01},
  recipe={"LG": {"interior_plate": 4, "construction_component": 6, "computer": 3}},
  function="Speaker for alarms, music and announcements. Loud sounds raise Attraction.",
  mounts="back", shape="wall", sockets=["audio@front"], emissive=["Activity LED"], notes="Horn speaker on a bracket.")
