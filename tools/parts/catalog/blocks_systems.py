"""PWR — Power & Thermal, LIF — Life Support, PRD — Production, AGR — Agriculture, LOG — Logistics."""

from . import P, V

LG_1 = {"LG": (1, 1, 1)}
LG_SG_1 = {"LG": (1, 1, 1), "SG": (1, 1, 1)}

# ---------------------------------------------------------------------------
# PWR — Power & Thermal
# ---------------------------------------------------------------------------
P("PWR", "Diesel Generator", "Generation", LG_1, tier="T0", art="SCR", cls="M",
  mass=900, hp=1200, power=60, recipe={"scrap_metal": 30, "motor": 4, "wiring_bundle": 6},
  function="Act I's first power source (M1.01). Burns diesel or ethanol canisters. Loud (85 dB), so it draws Hollows.",
  stats={"fuel": "1 canister per 40 min at full load", "noise_db": 85},
  mounts="bottom,back", airtight="none",
  moving=["Cooling fan: spins 1,200 rpm when running", "Engine block: idle vibration (vertex shader)"],
  sockets=["interact@front", "fuel@left", "vfx_smoke@top", "audio@center"],
  emissive=["Running lamp (amber)"], vfx=["Exhaust smoke", "Sparks when damaged"], audio=["Diesel chug loop"],
  notes="A salvaged construction-site generator on a welded skid. Fuel canister strapped to the side.")

P("PWR", "Solar Panel", "Generation", {"LG": (4, 1, 2), "SG": (4, 1, 8)}, tier="T1", cls="S",
  mass={"LG": 400, "SG": 60}, hp={"LG": 600, "SG": 80}, power={"LG": 120, "SG": 12},
  recipe={"LG": {"steel_plate": 4, "construction_component": 14, "girder": 12, "computer": 4, "solar_cell": 32, "glass_panel": 4},
          "SG": {"steel_plate": 1, "construction_component": 2, "girder": 2, "computer": 1, "solar_cell": 6}},
  function="Silent power from starlight; output scales with star distance and angle. Zero Attraction.",
  mounts="bottom", airtight="none", shape="flat",
  emissive=["None (cells use a clear-coat anisotropic material)"],
  notes="Panel surface 0.1 m thick on a 0.3 m frame, occupying the bottom of the volume. Cell grid via trim; backside wiring detail.")

P("PWR", "Tracking Solar Array", "Generation", {"LG": (3, 2, 3)}, tier="T2", cls="L",
  mass=1600, hp=1400, power=180,
  recipe={"steel_plate": 12, "construction_component": 30, "girder": 20, "motor": 4, "computer": 6, "solar_cell": 64},
  function="Two panel wings that follow the brightest star: +50% average output over fixed panels.",
  mounts="bottom", airtight="none",
  moving=["Mast head: yaw 360°", "Panel wings ×2: pitch 0–80°"],
  sockets=["interact@front"], notes="Wings fold flat for storms. Pivot empties: PART_Yaw at mast top, PART_PitchL/R at wing roots.")

P("PWR", "Wind Turbine", "Generation", {"LG": (3, 4, 1)}, tier="T1", cls="L",
  mass=2600, hp=2000, power=400,
  recipe={"steel_plate": 20, "construction_component": 40, "girder": 24, "motor": 8, "computer": 2},
  function="Planet-only generator; 0–400 kW depending on wind speed and altitude. Great on the Hollis Dam ridge.",
  stats={"output_curve": "0 kW < 3 m/s; 400 kW ≥ 12 m/s"},
  mounts="bottom", airtight="none",
  moving=["Rotor: 3 blades, 7 m diameter, 12–30 rpm", "Nacelle: yaws into the wind"],
  sockets=["interact@bottom", "light@top"], emissive=["Aviation beacon (red, blinking)"], audio=["Blade whoosh"],
  notes="Hub height 7.5 m. Blades must stay inside the 7.5 m wide volume at every rotation angle.")

P("PWR", "Micro-Hydro Turbine", "Generation", {"LG": (1, 1, 2)}, tier="T2", cls="M",
  mass=3200, hp=2600, power=2000,
  recipe={"steel_plate": 30, "construction_component": 20, "motor": 12, "large_tube": 4},
  function="Generates 2 MW when placed in flowing water (rivers, the Hollis Dam spillway). Quiet and clean.",
  mounts="all", airtight="none",
  moving=["Runner (impeller): spins with water speed"],
  sockets=["water@front", "water@back", "interact@top"], vfx=["Water churn at outlet"],
  notes="Intake grille on the front, draft tube on the back. Algae/wet-grime vertex mask on the lower half.")

P("PWR", "Battery", "Storage", LG_SG_1, tier="T1", cls="M",
  mass={"LG": 3800, "SG": 90}, hp={"LG": 2500, "SG": 150}, power=0,
  recipe={"LG": {"steel_plate": 80, "construction_component": 30, "power_cell": 80, "computer": 25},
          "SG": {"steel_plate": 2, "construction_component": 2, "power_cell": 2, "computer": 2}},
  function="Stores energy. LG 3 MWh (12 MW in/out); SG 0.05 MWh (0.2 MW).",
  stats={"capacity_mwh": {"LG": 3, "SG": 0.05}, "max_io_mw": {"LG": 12, "SG": 0.2}},
  mounts="all", airtight="all",
  sockets=["interact@front"], emissive=["Charge bars ×5 (front)", "Mode lamp: charge/discharge/auto"],
  notes="Cell stacks visible behind a grille on the front. Emissive bars driven by a 0–1 'Charge' parameter.")

P("PWR", "Hydrogen Engine", "Generation", {"LG": (1, 1, 2), "SG": (1, 1, 2)}, tier="T2", cls="M",
  mass={"LG": 4800, "SG": 450}, hp={"LG": 3500, "SG": 400}, power={"LG": 5000, "SG": 500},
  recipe={"LG": {"steel_plate": 80, "construction_component": 30, "large_tube": 12, "motor": 12, "computer": 4, "power_cell": 1}},
  function="Burns hydrogen for steady power; the bridge between batteries and reactors.",
  mounts="all", airtight="none",
  moving=["Turbine fan: spins with load"],
  sockets=["fuel@back", "vfx_exhaust@top", "interact@front"], emissive=["Combustion window glow"],
  vfx=["Heat shimmer at exhaust"], audio=["Turbine whine"],
  notes="Visible combustion chamber through a small heat-glass window.")

P("PWR", "Fission Reactor", "Generation", LG_SG_1, tier="T2", cls="M",
  mass={"LG": 7000, "SG": 400}, hp={"LG": 4000, "SG": 500}, power={"LG": 15000, "SG": 500},
  recipe={"LG": {"steel_plate": 80, "construction_component": 40, "metal_grid": 10, "large_tube": 8, "reactor_component": 100, "motor": 6, "computer": 25}},
  function="Compact uranium reactor. Emits low radiation within 3 m; explodes when destroyed.",
  stats={"fuel": "1 uranium rod per 4 h at full load", "radiation_radius_m": 3},
  mounts="all", airtight="all",
  sockets=["interact@front", "conveyor_large@back"], emissive=["Core viewport (Cherenkov blue)", "Status lights"],
  vfx=["Radiation shimmer when damaged"], audio=["Low hum"],
  notes="Radiation trefoil stencils. A blue viewport onto the core is the recognizable feature.")

P("PWR", "Large Fission Reactor", "Generation", {"LG": (3, 3, 3)}, tier="T3", cls="XL",
  mass=70000, hp=7000, power=60000,
  recipe={"steel_plate": 1000, "construction_component": 70, "metal_grid": 40, "large_tube": 40, "reactor_component": 2000, "motor": 20, "computer": 75},
  function="Capital-ship and major-base power plant.",
  mounts="all", airtight="all",
  moving=["Control rods ×6: rise/fall with output"],
  sockets=["interact@front", "conveyor_large@back", "work@front"], emissive=["Core viewport", "Rod position lights"],
  vfx=["Coolant steam vents ×2"], audio=["Deep hum", "Alarm klaxon"],
  notes="Cylindrical containment inside a square frame; walkway ring around the top.")

P("PWR", "He-3 Fusion Reactor", "Generation", {"LG": (3, 3, 3)}, tier="T3", cls="XL",
  mass=28000, hp=5000, power=80000,
  recipe={"steel_plate": 400, "construction_component": 120, "large_tube": 40, "superconductor": 120, "reactor_component": 400, "computer": 60, "motor": 24},
  function="80 MW of clean power from lunar helium-3 (unlocked at Tycho, M2.04). No radiation.",
  stats={"fuel": "1 He-3 canister per 6 h at full load"},
  unlock="Recovered He-3 core at Tycho (M2.04).",
  mounts="all", airtight="all",
  moving=["Magnetic rings ×2: counter-rotate", "Plasma: animated emissive torus"],
  sockets=["interact@front", "conveyor_large@back", "work@front"],
  emissive=["Plasma torus (magenta-white)", "Ring status lights"], vfx=["Plasma arcs when damaged"], audio=["Rising harmonic hum"],
  notes="Tokamak torus visible through four viewports. The rings' motion must be readable from 30 m.")

P("PWR", "Radiator Panel", "Thermal", {"LG": (1, 1, 1), "SG": (2, 1, 4)}, tier="T3", cls="M",
  mass={"LG": 1200, "SG": 120}, hp={"LG": 800, "SG": 100},
  recipe={"LG": {"steel_plate": 10, "large_tube": 10, "construction_component": 6, "motor": 2}},
  function="Dumps waste heat to space: 20 MW (LG) / 1 MW (SG). Required around jump cores and big reactors.",
  stats={"heat_dissipation_mw": {"LG": 20, "SG": 1}},
  mounts="back", airtight="none",
  moving=["Fins: fold out from the housing to 3× area, 2 s"],
  emissive=["Fin heat glow (dull red → orange with heat)"],
  notes="Folded state fits the cell; deployed fins extend 5 m (LG) beyond it (excluded from the placement bounds, included in collision when deployed).")

P("PWR", "Heat Sink", "Thermal", LG_1, tier="T3", cls="M",
  mass=5000, hp=3000, recipe={"steel_plate": 30, "superconductor": 10, "large_tube": 6},
  function="Buffers 200 MJ of heat for short bursts (jump charging, railgun volleys).",
  mounts="all", airtight="all", emissive=["Heat gauge strip"],
  notes="Dense ribbed block with a heat-gauge strip; ribs glow faintly when near capacity.")

P("PWR", "Power Distribution Panel", "Distribution", LG_1, tier="T1", cls="M",
  mass=200, hp=400, recipe={"interior_plate": 6, "construction_component": 6, "computer": 2, "display": 1},
  function="Diegetic breaker box: flip physical breakers to set power priorities (Life Support > Defense > Production > Comfort).",
  mounts="back", airtight="none", shape="wall",
  moving=["Breaker switches ×12: toggle"], sockets=["interact@front", "lcd@front"],
  emissive=["Breaker LEDs ×12", "Load meter screen"],
  notes="Wall-mounted box, 0.3 m deep. Labels printed per priority group; the door opens 110°.")

# ---------------------------------------------------------------------------
# LIF — Life Support
# ---------------------------------------------------------------------------
P("LIF", "Rain Collector & Purifier", "Water", LG_1, tier="T0", art="SCR", cls="M",
  mass=150, hp=300, recipe={"scrap_metal": 10, "fabric": 6, "duct_tape": 2},
  function="Act I water: collects rain and dew (up to 20 L/h), then solar-stills and charcoal-filters it. No power.",
  mounts="bottom", airtight="none",
  sockets=["interact@front", "water@bottom"], vfx=["Drips during rain"],
  notes="Tarp funnel over a blue barrel with a charcoal filter stack; water level visible through a cut-open bottle.")

P("LIF", "Water Purifier", "Water", LG_1, tier="T1", cls="M",
  mass=500, hp=800, power=-20, recipe={"steel_plate": 10, "motor": 2, "filter_mesh": 4, "large_tube": 2},
  function="Removes contamination (including Verdance traces) at 60 L/h.",
  mounts="all", airtight="none",
  moving=["Pump impeller"], sockets=["water@back", "water@front", "interact@front"],
  emissive=["Purity indicator (green/red)"], notes="Clear inspection tube shows water moving.")

P("LIF", "Water Tank", "Water", {"LG": (1, 2, 1), "SG": (1, 1, 1)}, tier="T1", cls="S",
  mass={"LG": 1200, "SG": 60}, hp={"LG": 1500, "SG": 120},
  recipe={"LG": {"steel_plate": 20, "large_tube": 4, "construction_component": 4}},
  function="Stores 20,000 L (LG) / 400 L (SG) of clean water.", shape="cylinder",
  mounts="all", airtight="all", sockets=["water@bottom", "water@top"], emissive=["Level gauge strip"],
  notes="Vertical cylinder in a square cage frame; the level gauge is a 0–1 parameter.")

P("LIF", "Water Recycler", "Water", {"LG": (1, 1, 2)}, tier="T2", cls="M",
  mass=1600, hp=1500, power=-80, recipe={"steel_plate": 20, "motor": 6, "filter_mesh": 10, "large_tube": 6, "computer": 2},
  function="Recovers 90% of grey water from showers, sinks and kitchens.",
  mounts="all", airtight="all", sockets=["water@back", "water@front", "interact@left"],
  moving=["Centrifuge drum spins"], emissive=["Cycle lights"], audio=["Gurgle loop"],
  notes="Centrifuge drum visible behind a round window.")

P("LIF", "Oxygen Generator", "Air", {"LG": (1, 1, 1), "SG": (1, 1, 2)}, tier="T1", cls="M",
  mass={"LG": 640, "SG": 120}, hp={"LG": 1000, "SG": 150}, power={"LG": -300, "SG": -30},
  recipe={"LG": {"steel_plate": 120, "construction_component": 5, "large_tube": 2, "motor": 4, "computer": 5}},
  function="Splits ice into O₂ (30 L/s LG) and H₂. Fills rooms, tanks and suits.",
  stats={"o2_lps": {"LG": 30, "SG": 3}},
  mounts="all", airtight="all",
  sockets=["conveyor_large@back", "air@top", "interact@front"], emissive=["Output lamp (blue)"],
  vfx=["Frost at the intake when running"], audio=["Electrolysis bubble hum"],
  notes="Ice hopper visible through a frosted window.")

P("LIF", "Oxygen Tank", "Air", {"LG": (1, 2, 1), "SG": (1, 1, 1)}, tier="T1", cls="S",
  mass={"LG": 1500, "SG": 60}, hp={"LG": 1400, "SG": 120},
  recipe={"LG": {"steel_plate": 80, "large_tube": 40, "small_tube": 60, "computer": 8, "construction_component": 10}},
  function="Stores 100,000 L (LG) / 5,000 L (SG) of oxygen.", shape="cylinder",
  mounts="all", airtight="all", sockets=["air@top", "conveyor_small@bottom"], emissive=["Fill gauge"],
  notes="Blue-banded pressure cylinder (O₂ color code).")

P("LIF", "Compact Life Support Module", "Air", LG_1, tier="T1", art="DIR", cls="L",
  mass=1100, hp=1600, power=-120,
  recipe={"steel_plate": 20, "motor": 6, "filter_mesh": 8, "computer": 6, "medical_component": 2},
  function="All-in-one O₂, CO₂ scrubbing and heat for small crews (up to 6). A Wren part recovered from the crashed Ark shuttle (M1.05).",
  unlock="Salvaged in M1.05; buildable (Industrial skin) at T2.",
  mounts="all", airtight="all", sockets=["air@top", "interact@front"],
  emissive=["Directorate status panel (sterile blue)"],
  notes="Ships with two skins: Directorate (story salvage) and Industrial (buildable). Directorate skin shows scorch marks from the crash.")

P("LIF", "Air Vent", "Air", LG_SG_1, tier="T1", cls="S",
  mass={"LG": 250, "SG": 12}, hp={"LG": 500, "SG": 60}, power={"LG": -2, "SG": -0.2},
  recipe={"LG": {"steel_plate": 15, "construction_component": 10, "motor": 2, "computer": 5}},
  function="Joins a room to the ventilation network; can depressurize a room (a weapon against Hollows).",
  mounts="all", airtight="all", shape="panel",
  moving=["Louvers ×6: open/close 70°"], sockets=["air@back", "air@front"],
  vfx=["Dust/air flow particles"], audio=["Air rush"],
  notes="Grille on the front face. Louvers must visibly close when the vent seals (quarantine readability).")

P("LIF", "Air Duct", "Air", LG_SG_1, tier="T1", cls="S",
  mass={"LG": 300, "SG": 8}, hp={"LG": 800, "SG": 50},
  recipe={"LG": {"steel_plate": 8, "small_tube": 6}, "SG": {"steel_plate": 1, "small_tube": 1}},
  function="Ventilation network piece. The LG version is a crawlable maintenance duct (Crawlers and players can move through it).",
  mounts="all", airtight="all",
  sockets=["air@front", "air@back"],
  notes="LG: 1.2 m square crawl tunnel inside an armor shell, with access panels. SG: 0.3 m round pipe. Spores travel through these, so the vent network must be traceable in the Air View.",
  variants=[V("Straight"), V("Corner"), V("T-Junction"), V("Cross"), V("End Cap")])

P("LIF", "CO₂ Scrubber", "Air", LG_1, tier="T1", cls="M",
  mass=700, hp=900, power=-150, recipe={"steel_plate": 10, "motor": 4, "filter_mesh": 12, "computer": 2},
  function="Removes CO₂ from connected rooms (enough for 12 people).",
  mounts="all", airtight="all", sockets=["air@top", "interact@front"],
  moving=["Fan"], emissive=["Cartridge saturation lights ×4"],
  notes="Four swappable cartridge slots on the front; the cartridges are separate meshes.")

P("LIF", "Spore Air Filter", "Air", LG_SG_1, key="air_filter_spore", tier="T2", cls="M",
  mass={"LG": 480, "SG": 30}, hp={"LG": 700, "SG": 80}, power={"LG": -3.5, "SG": -0.4},
  recipe={"LG": {"steel_plate": 4, "motor": 2, "filter_mesh": 6}, "SG": {"steel_plate": 1, "motor": 1, "filter_mesh": 1}},
  function="Removes spores from the air network at 12 units/min. The core defense against colony outbreaks.",
  stats={"removes": "spores", "rate_per_min": 12, "noise_db": 38},
  unlock="T2 (tech.bio.spore_filtration)",
  mounts="all", airtight="all", sockets=["air@back", "air@front", "interact@front"],
  moving=["Fan"], emissive=["Filter status: green clean / amber loaded / red clogged"],
  notes="The visible filter mesh turns green-grey as it loads (material parameter 'Load'). Matches the JSON example in bible chapter 13.")

P("LIF", "Heater", "Temperature", LG_SG_1, tier="T1", cls="S",
  mass={"LG": 300, "SG": 15}, hp={"LG": 500, "SG": 50}, power={"LG": -50, "SG": -5},
  recipe={"LG": {"steel_plate": 6, "construction_component": 4, "power_cell": 2}},
  function="Warms a room. Essential on Hollowmere and in the long lunar night.",
  mounts="back", shape="wall", sockets=["air@front"], emissive=["Heating coil glow"],
  notes="Wall-mounted radiator; coils glow orange with a 'Heat' parameter.")

P("LIF", "Cooler", "Temperature", LG_1, tier="T1", cls="S",
  mass=320, hp=500, power=-60, recipe={"steel_plate": 6, "motor": 2, "large_tube": 2},
  function="Cools a room. Essential in desert daytime and near reactors.",
  mounts="back", shape="wall", moving=["Fan"], sockets=["air@front"], emissive=["Blue status lamp"],
  vfx=["Cold mist at the grille"], notes="Wall unit with a large fan grille.")

P("LIF", "Atmosphere Monitor", "Monitoring", LG_SG_1, tier="T1", cls="S",
  mass={"LG": 40, "SG": 3}, hp={"LG": 150, "SG": 30}, power={"LG": -0.3, "SG": -0.05},
  recipe={"LG": {"interior_plate": 2, "computer": 2, "display": 1}, "SG": {"computer": 1, "display": 1}},
  function="Shows a room's O₂, CO₂, pressure, temperature and spore count; sounds alarms.",
  mounts="back", shape="wall", sockets=["lcd@front", "audio@front"], emissive=["Screen", "Alarm strobe"],
  notes="Small wall screen with a strobe on top. Screen UI is rendered live, not baked.")

# ---------------------------------------------------------------------------
# PRD — Production & Research
# ---------------------------------------------------------------------------
P("PRD", "Workbench", "Crafting", LG_1, tier="T0", art="SCR", cls="M",
  mass=300, hp=500, recipe={"scrap_metal": 15, "salvaged_wood": 10},
  function="Act I crafting station: tools, melee weapons, basic components, barricades (M1.01).",
  mounts="bottom", airtight="none",
  sockets=["work@front", "interact@front", "light@top"],
  notes="A heavy wooden bench with a vise, pegboard of tools and a work lamp. Tools on the pegboard change as tiers unlock (swap meshes).")

P("PRD", "Scrap Recycler", "Refining", {"LG": (1, 1, 2)}, tier="T1", art="SCR", cls="M",
  mass=1500, hp=1400, power=-200, recipe={"scrap_metal": 40, "motor": 6, "steel_plate": 10},
  function="Grinds scrap into raw iron, nickel and silicon (60% yield).",
  mounts="all", airtight="none",
  moving=["Shredder rollers ×2", "Hopper lid"], sockets=["item_in@top", "item_out@front", "conveyor_large@back"],
  vfx=["Sparks and debris"], audio=["Shredder grind"],
  notes="Converted wood-chipper look with a welded hopper.")

P("PRD", "Basic Refinery", "Refining", {"LG": (1, 2, 1)}, tier="T1", cls="M",
  mass=4000, hp=3000, power=-400,
  recipe={"steel_plate": 120, "construction_component": 20, "large_tube": 10, "motor": 10, "computer": 10},
  function="Refines ore into ingots at 50% speed and 70% yield. The first refinery.",
  mounts="all", airtight="none",
  sockets=["conveyor_large@back", "conveyor_large@bottom", "interact@front", "work@front"],
  emissive=["Furnace window glow"], vfx=["Heat shimmer"], audio=["Furnace roar"],
  notes="Tall furnace with a glowing viewport.")

P("PRD", "Refinery", "Refining", {"LG": (3, 4, 3)}, tier="T2", cls="XL",
  mass=35000, hp=12000, power=-1000,
  recipe={"steel_plate": 1200, "construction_component": 40, "large_tube": 20, "motor": 16, "metal_grid": 20, "computer": 20},
  function="Full-speed ore refining at 80% yield.",
  mounts="all", airtight="none",
  moving=["Crusher drums", "Crucible tilt 30°"],
  sockets=["conveyor_large@back*2", "conveyor_large@bottom", "interact@front", "work@front*2"],
  emissive=["Molten metal glow", "Status panels"], vfx=["Molten pour", "Smoke stack"], audio=["Industrial loop"],
  notes="Hero industrial piece: crusher, conveyor, crucible and chimney.")

P("PRD", "Assembler", "Crafting", {"LG": (1, 2, 1)}, tier="T1", cls="L",
  mass=4500, hp=2600, power=-300,
  recipe={"steel_plate": 140, "construction_component": 80, "motor": 20, "display": 10, "metal_grid": 10, "computer": 160},
  function="Builds components from ingots. The heart of every base.",
  mounts="all", airtight="none",
  moving=["Robot arms ×2: 4-axis", "Print bed slides"], sockets=["conveyor_large@back", "interact@front", "work@front"],
  emissive=["Work light", "Queue display"], vfx=["Welding sparks"], audio=["Servo whirr"],
  notes="Glass-fronted cabinet with two visible robot arms. Arms are separate PART_ meshes with pivots.")

P("PRD", "Fabrication Bay", "Crafting", {"LG": (5, 4, 5)}, tier="T3", cls="XL",
  mass=90000, hp=20000, power=-5000,
  recipe={"steel_plate": 2000, "construction_component": 400, "motor": 80, "computer": 200, "superconductor": 40, "display": 20},
  function="Builds ship-scale parts and jump components. Large-grid welding happens inside it.",
  mounts="bottom,back", airtight="all",
  moving=["Gantry: travels along the bay", "Robot arms ×4 on the gantry", "Bay doors: segmented, 12.5 m opening"],
  sockets=["conveyor_large@back*3", "interact@front", "work@front*4", "light@top*6"],
  emissive=["Gantry work lights", "Status boards"], vfx=["Welding sparks ×4"], audio=["Factory loop"],
  notes="A room-sized hangar module. The interior is walkable.")

P("PRD", "3D Printer", "Crafting", LG_1, tier="T2", cls="M",
  mass=400, hp=600, power=-50, recipe={"steel_plate": 6, "motor": 4, "computer": 6, "bio_plastic": 10},
  function="Prints furniture, decor and small items from bio-plastic.",
  mounts="bottom", sockets=["interact@front", "work@front"],
  moving=["Print head: XYZ gantry"], emissive=["Print progress ring"], notes="Enclosed printer with a visible print in progress (parameter-driven build height).")

P("PRD", "Research Station", "Research", {"LG": (2, 1, 1)}, tier="T1", cls="M",
  mass=600, hp=700, power=-30, recipe={"interior_plate": 10, "computer": 10, "display": 4, "detector_component": 2},
  function="Turns scan data into Engineering research points. Staffed by Researchers.",
  mounts="bottom", sockets=["work@front*2", "lcd@front*2", "interact@front"],
  emissive=["Screens ×3"], notes="Lab bench with monitors, microscopes and sample trays.")

P("PRD", "Sample Analyzer", "Research", LG_1, tier="T2", cls="M",
  mass=700, hp=600, power=-40, recipe={"steel_plate": 6, "glass_panel": 6, "computer": 6, "medical_component": 4, "filter_mesh": 4},
  function="Glovebox for Bloom samples: produces Bio research points. If damaged, it leaks spores.",
  mounts="bottom", sockets=["work@front", "air@top", "interact@front"],
  emissive=["Containment status (green/red)", "UV sterilizer"], vfx=["Spore leak when damaged"],
  notes="Glovebox with two rubber gloves (cloth sim optional) and a pass-through airlock.")

P("PRD", "Armory Bench", "Crafting", {"LG": (2, 1, 1)}, tier="T2", cls="M",
  mass=900, hp=1000, power=-20, recipe={"steel_plate": 20, "construction_component": 10, "motor": 2, "computer": 2},
  function="Crafts firearms, ammunition, armor and turret ammo.",
  mounts="bottom", sockets=["work@front*2", "interact@front"],
  moving=["Reloading press arm"], notes="Gun-smith bench with a wall rack. Rack shows crafted weapons (swap meshes).")

# ---------------------------------------------------------------------------
# AGR — Agriculture
# ---------------------------------------------------------------------------
P("AGR", "Planter Box", "Crops", LG_1, tier="T0", art="SCR", cls="S",
  mass=600, hp=300, recipe={"salvaged_wood": 12, "scrap_metal": 2},
  function="Soil planter for 4 crops. Needs Earth soil (or imported soil off-world) and water.",
  mounts="bottom", sockets=["work@front", "water@bottom"],
  notes="Raised wooden box, 0.8 m high. Crop meshes are separate growth-stage props (4 stages).",
  variants=[V("Survivor", notes="Pallet wood and chicken wire."), V("Colony", notes="Clean composite box (Domestic set).")])

P("AGR", "Hydroponics Tray", "Crops", {"LG": (1, 1, 2)}, tier="T2", cls="M",
  mass=800, hp=500, power=-25, recipe={"steel_plate": 6, "large_tube": 4, "motor": 1, "bio_plastic": 8},
  function="Soil-free tray for 8 crops; needs water and light.",
  mounts="bottom", sockets=["work@front", "water@back", "light@top"],
  moving=["Nutrient pump"], emissive=["Grow-light strip (magenta)"],
  notes="Two-tier rack. Crop props snap to 8 slots.")

P("AGR", "Grow Light", "Crops", LG_SG_1, tier="T1", cls="S",
  mass={"LG": 30, "SG": 3}, hp={"LG": 100, "SG": 20}, power={"LG": -8, "SG": -1},
  recipe={"LG": {"interior_plate": 2, "glass_panel": 2, "construction_component": 2}},
  function="Full-spectrum light; lets crops grow without sunlight.",
  mounts="top", shape="panel_top", sockets=["light@bottom"], emissive=["Magenta/white LED panel"],
  notes="Ceiling fixture; the emitted light color is part of the Hydroponics look.")

P("AGR", "Algae Farm", "Food & Air", {"LG": (1, 2, 1)}, tier="T2", cls="M",
  mass=1200, hp=700, power=-30, recipe={"steel_plate": 8, "glass_panel": 16, "large_tube": 4, "motor": 2},
  function="Produces food paste and a little oxygen from light and CO₂.",
  mounts="bottom", sockets=["air@top", "water@bottom", "work@front", "item_out@front"],
  emissive=["Backlit green tubes"], vfx=["Rising bubbles"], notes="Vertical glass bubble tubes with green fluid.")

P("AGR", "Protein Vat", "Food", {"LG": (2, 2, 1)}, tier="T2", cls="M",
  mass=2500, hp=1500, power=-60, recipe={"steel_plate": 30, "large_tube": 6, "motor": 4, "computer": 2},
  function="Grows bland but reliable protein from organics.",
  mounts="bottom", sockets=["item_in@top", "item_out@front", "work@front"],
  moving=["Mixer paddle"], emissive=["Temperature display"], notes="Stainless steel vat with an inspection hatch.")

P("AGR", "Seed Vault", "Storage", LG_1, tier="T1", cls="M",
  mass=900, hp=1500, power=-5, recipe={"steel_plate": 20, "computer": 2, "motor": 1},
  function="Cold storage for seeds (the Act I cargo-triage item). Seeds stored here never spoil.",
  mounts="all", airtight="all", sockets=["interact@front"], moving=["Vault door: hinge 100°"],
  emissive=["Frost indicator"], vfx=["Cold fog when opened"],
  notes="Round vault door; racks of labeled seed tins inside.")

P("AGR", "Livestock Pen", "Animals", {"LG": (3, 1, 3)}, tier="T3", art="DOM", cls="L",
  mass=2000, hp=1200, recipe={"steel_plate": 10, "salvaged_wood": 30, "construction_component": 10},
  function="Houses Tessari calves (after Veyra is healed) and other livestock: milk, fiber and happy survivors.",
  mounts="bottom", sockets=["work@front*2", "water@left"],
  moving=["Gate: swings 90°"], notes="Fence, feeders, water trough and a hay-bale shelter. Sized for Tessari (2 m tall calves).")

P("AGR", "Aquaponics Tank", "Food", {"LG": (2, 1, 1)}, tier="T3", cls="M",
  mass=3000, hp=800, power=-20, recipe={"steel_plate": 10, "glass_panel": 20, "motor": 2, "large_tube": 2},
  function="Fish tank with a grow bed on top: food plus the Fun of watching fish.",
  mounts="bottom", sockets=["work@front", "water@back"], vfx=["Water caustics", "Bubbles"],
  notes="Glass tank with animated fish (a shared boids system), grow bed above.")

# ---------------------------------------------------------------------------
# LOG — Logistics & Storage
# ---------------------------------------------------------------------------
P("LOG", "Conveyor Junction", "Conveyors", LG_SG_1, tier="T1", cls="S",
  mass={"LG": 900, "SG": 25}, hp={"LG": 1500, "SG": 100}, power={"LG": -0.5, "SG": -0.1},
  recipe={"LG": {"interior_plate": 20, "construction_component": 30, "small_tube": 20, "motor": 6}},
  function="Six-way conveyor hub.", mounts="all", airtight="all",
  sockets=["conveyor_large@front", "conveyor_large@back", "conveyor_large@left", "conveyor_large@right", "conveyor_large@top", "conveyor_large@bottom"],
  notes="Port apertures at exact face centers (the conveyor standard). Hazard stripes around each port.")

P("LOG", "Conveyor Tube", "Conveyors", LG_SG_1, tier="T1", cls="S",
  mass={"LG": 300, "SG": 10}, hp={"LG": 600, "SG": 40},
  recipe={"LG": {"interior_plate": 10, "construction_component": 10, "small_tube": 12, "motor": 4}},
  function="Connects conveyor ports.", mounts="front,back", airtight="none",
  sockets=["conveyor_large@front", "conveyor_large@back"],
  notes="Ribbed tube with inspection windows showing items moving (animated texture).",
  variants=[V("Straight"), V("Curved"), V("T-Junction")])

P("LOG", "Conveyor Sorter", "Conveyors", LG_SG_1, tier="T2", cls="M",
  mass={"LG": 900, "SG": 30}, hp={"LG": 1500, "SG": 100}, power={"LG": -10, "SG": -1},
  recipe={"LG": {"interior_plate": 20, "construction_component": 30, "small_tube": 20, "motor": 6, "computer": 10}},
  function="Filters items between conveyor lines (whitelist/blacklist).",
  mounts="all", airtight="all", sockets=["conveyor_large@front", "conveyor_large@back", "interact@top"],
  moving=["Diverter flap"], emissive=["Filter mode lights"], notes="Junction housing with a diverter and a small screen.")

P("LOG", "Small Cargo Container", "Storage", LG_SG_1, tier="T1", cls="S",
  mass={"LG": 1200, "SG": 40}, hp={"LG": 2000, "SG": 150},
  recipe={"LG": {"interior_plate": 40, "construction_component": 40, "metal_grid": 4, "small_tube": 20, "motor": 4, "display": 1, "computer": 2}},
  function="Storage: 15,625 L (LG) / 125 L (SG).", mounts="all", airtight="all",
  sockets=["conveyor_large@back", "interact@front"], emissive=["Fill level strip"],
  notes="Lockable front hatch. Fill-level strip parameter 0–1.")

P("LOG", "Large Cargo Container", "Storage", {"LG": (3, 3, 3), "SG": (3, 3, 3)}, tier="T2", cls="M",
  mass={"LG": 9000, "SG": 300}, hp={"LG": 9000, "SG": 800},
  recipe={"LG": {"interior_plate": 360, "construction_component": 80, "metal_grid": 24, "small_tube": 60, "motor": 20, "display": 1, "computer": 8}},
  function="Storage: 421,875 L (LG) / 3,375 L (SG).", mounts="all", airtight="all",
  sockets=["conveyor_large@back*2", "conveyor_large@bottom", "interact@front"], emissive=["Fill level strip"],
  notes="Hauler skin available (cargo-orange container ribs).")

P("LOG", "Connector", "Docking", {"LG": (1, 1, 2), "SG": (1, 1, 2)}, tier="T2", cls="M",
  mass={"LG": 1400, "SG": 90}, hp={"LG": 2400, "SG": 200}, power={"LG": -2, "SG": -0.2},
  recipe={"LG": {"steel_plate": 150, "construction_component": 40, "small_tube": 12, "motor": 8, "computer": 20}},
  function="Docks two grids and shares their conveyor networks.",
  mounts="back,left,right,top,bottom", airtight="all",
  moving=["Magnetic collar: extends 0.2 m on lock"], sockets=["conveyor_large@back", "conveyor_large@front", "attach_top@front"],
  emissive=["Status ring: yellow ready / green locked"], audio=["Magnetic clamp"],
  notes="The docking face must be rotationally symmetric so any two connectors mate.")

P("LOG", "Ejector", "Handling", LG_SG_1, tier="T2", cls="S",
  mass={"LG": 500, "SG": 25}, hp={"LG": 800, "SG": 60}, power={"LG": -2, "SG": -0.2},
  recipe={"LG": {"steel_plate": 10, "construction_component": 4, "motor": 2}},
  function="Throws items out of the conveyor network (dumping stone, jettisoning cargo).",
  mounts="all", airtight="all", sockets=["conveyor_large@back", "item_out@front"],
  moving=["Ejector plate"], notes="Short barrel-shaped port on the front face.")

P("LOG", "Collector", "Handling", LG_SG_1, tier="T2", cls="M",
  mass={"LG": 800, "SG": 40}, hp={"LG": 1000, "SG": 80}, power={"LG": -20, "SG": -2},
  recipe={"LG": {"steel_plate": 45, "construction_component": 50, "small_tube": 12, "motor": 8, "display": 4, "computer": 10}},
  function="Pulls in loose items and ore near its intake.",
  mounts="all", airtight="all", sockets=["conveyor_large@back", "item_in@front"],
  vfx=["Suction particles"], notes="Funnel-shaped intake with a mesh grille.")
