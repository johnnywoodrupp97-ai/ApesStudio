"""COL — Colony & Furniture, MED — Medical.

Furniture is placed on the large grid (one furniture piece per cell footprint) but the
mesh itself is human-scaled inside the cell. Survivors use furniture through
seat / bed / work sockets, so socket placement is gameplay-critical.
"""

from . import P, V

LG_1 = {"LG": (1, 1, 1)}
LG_2 = {"LG": (2, 1, 1)}
LG_22 = {"LG": (2, 1, 2)}

FURN = "Furniture sits on the bottom face. Human scale: seat height 0.45 m, table height 0.75 m, counter 0.9 m."

# ---------------------------------------------------------------------------
# COL — Survival-era comforts (Act I)
# ---------------------------------------------------------------------------
P("COL", "Campfire", "Survival Comforts", LG_1, tier="T0", art="SCR", cls="S",
  mass=80, hp=150, recipe={"salvaged_wood": 6, "scrap_metal": 2},
  function="Warmth, basic cooking and the Act I campfire conversations. Raises Attraction at night.",
  stats={"warmth_radius_m": 4, "comfort": 5, "attraction": 15},
  mounts="bottom", sockets=["work@front", "seat@front*4", "vfx_fire@center", "light@center"],
  emissive=["Embers"], vfx=["Fire", "Embers", "Smoke"], audio=["Crackle loop"],
  notes="Stone ring or cut oil-drum variant. Seat slots are logs/crates around it at 1.2 m radius.",
  variants=[V("Stone Ring"), V("Oil Drum")])

P("COL", "Radio Set", "Survival Comforts", LG_1, tier="T0", art="SCR", cls="S",
  mass=15, hp=60, recipe={"scrap_metal": 2, "wiring_bundle": 2, "radio_component": 1},
  function="Plays pre-outbreak music and picks up broadcasts (diegetic music). Fun +, Safety + at night.",
  mounts="bottom", sockets=["interact@front", "audio@center"], emissive=["Dial glow"],
  notes="Tabletop prop on a crate. Dial needle animates with the station (PART_Needle).")

P("COL", "Bedroll", "Beds", LG_1, tier="T0", art="SCR", cls="S",
  mass=5, hp=30, recipe={"fabric": 6},
  function="Sleeping bag on the floor. Rest +8/h; bad-sleep moodlet.",
  mounts="bottom", sockets=["bed@center"], notes="Rumpled sleeping bag with a rolled-jacket pillow. Three rumple variations (shape keys).")

# ---------------------------------------------------------------------------
# COL — Beds
# ---------------------------------------------------------------------------
P("COL", "Single Bed", "Beds", LG_1, tier="T1", art="DOM", cls="S",
  mass=60, hp=120, recipe={"interior_plate": 4, "fabric": 8},
  function="Rest +14/h. Personal bed (claimed by one survivor).",
  mounts="bottom", sockets=["bed@center", "interact@left"], notes=FURN + " Blanket color from the owner's palette (material parameter).")

P("COL", "Double Bed", "Beds", LG_1, tier="T1", art="DOM", cls="S",
  mass=90, hp=150, recipe={"interior_plate": 6, "fabric": 14},
  function="Rest +16/h for partners; relationship bonus when shared.",
  mounts="bottom", sockets=["bed@center*2", "interact@left"], notes=FURN)

P("COL", "Bunk Bed", "Beds", LG_1, tier="T1", art="DOM", cls="S",
  mass=110, hp=180, recipe={"interior_plate": 6, "small_tube": 4, "fabric": 12},
  function="Two sleepers per cell. Rest +12/h; 'Cramped' moodlet in small rooms.",
  mounts="bottom", sockets=["bed@center*2", "interact@left"], notes=FURN + " Ladder on one end.")

# ---------------------------------------------------------------------------
# COL — Dining & kitchen
# ---------------------------------------------------------------------------
P("COL", "Dining Table", "Dining", LG_1, tier="T1", art="DOM", cls="S",
  mass=40, hp=100, recipe={"interior_plate": 4, "small_tube": 2},
  function="Four-person table. Shared meals give +15 Social.",
  mounts="bottom", sockets=["work@front", "seat@center*4"], notes=FURN)

P("COL", "Long Dining Table", "Dining", {"LG": (3, 1, 1)}, tier="T1", art="DOM", cls="M",
  mass=120, hp=300, recipe={"interior_plate": 12, "small_tube": 6},
  function="Eight-person table. Required for the Sunday Dinner tradition (M2.03) and the final scene (M4.06).",
  mounts="bottom", sockets=["seat@center*8", "work@front"],
  notes=FURN + " Story furniture: the table where the game ends. Place-setting props (plates, a chipped pot of jollof) are a separate set-dressing kit.")

P("COL", "Chair", "Seating", LG_1, tier="T1", art="DOM", cls="S",
  mass=8, hp=40, recipe={"interior_plate": 2},
  function="Seating (Comfort +5 while seated).", mounts="bottom", sockets=["seat@center"], notes=FURN,
  variants=[V("Dining"), V("Office"), V("Stool")])

P("COL", "Bench", "Seating", LG_1, tier="T1", art="DOM", cls="S",
  mass=20, hp=60, recipe={"interior_plate": 3},
  function="Two-person bench; the best seat in front of a window.", mounts="bottom", sockets=["seat@center*2"], notes=FURN)

P("COL", "Couch", "Seating", LG_2, tier="T1", art="DOM", cls="S",
  mass=60, hp=120, recipe={"interior_plate": 4, "fabric": 12},
  function="Three-seat couch; Comfort +12, naps allowed.", mounts="bottom", sockets=["seat@center*3", "bed@center"], notes=FURN)

P("COL", "Armchair", "Seating", LG_1, tier="T1", art="DOM", cls="S",
  mass=30, hp=80, recipe={"interior_plate": 2, "fabric": 6},
  function="Comfort +10; reading chair (Bookshelf bonus).", mounts="bottom", sockets=["seat@center"], notes=FURN)

P("COL", "Kitchen Station", "Kitchen", LG_2, tier="T1", art="DOM", cls="M",
  mass=300, hp=500, power=-30, recipe={"steel_plate": 6, "interior_plate": 10, "motor": 1, "large_tube": 2},
  function="Stove, counter and sink: turns ingredients into meals (Survival Ration → Homestyle → Feast).",
  mounts="bottom", sockets=["work@front*2", "water@back", "vfx_smoke@top", "interact@front"],
  emissive=["Burner rings (orange)"], vfx=["Pan steam", "Burner flame"], audio=["Sizzle"],
  notes=FURN + " Utensils on a rail; the pot on the stove is a swappable prop.")

P("COL", "Cold Storage", "Kitchen", LG_1, tier="T1", art="DOM", cls="S",
  mass=120, hp=250, power=-5, recipe={"interior_plate": 8, "motor": 1},
  function="Stops food spoilage.", mounts="bottom", moving=["Door: hinge 110°"],
  sockets=["interact@front"], emissive=["Interior light (on open)"], vfx=["Cold fog when opened"], notes=FURN + " Fridge magnets and drawings on the door (Lily's).")

P("COL", "Bar Counter", "Dining", LG_2, tier="T2", art="DOM", cls="S",
  mass=150, hp=300, recipe={"interior_plate": 10},
  function="Social hub: +Social and +Fun for survivors hanging out.", mounts="bottom", sockets=["seat@front*3", "work@back"], notes=FURN)

# ---------------------------------------------------------------------------
# COL — Hygiene
# ---------------------------------------------------------------------------
P("COL", "Sink", "Hygiene", LG_1, tier="T1", art="DOM", cls="S",
  mass=30, hp=80, recipe={"interior_plate": 2, "small_tube": 2},
  function="Hygiene +20.", mounts="bottom,back", sockets=["work@front", "water@back"], vfx=["Running water"], notes=FURN + " Mirror above (planar reflection optional).")

P("COL", "Toilet", "Hygiene", LG_1, tier="T1", art="DOM", cls="S",
  mass=40, hp=80, recipe={"interior_plate": 2, "small_tube": 2},
  function="Required need-satisfier; zero-G variant works in space.", mounts="bottom,back", sockets=["seat@center", "water@back"],
  notes=FURN + " Two variants for gravity and zero-G.", variants=[V("Gravity"), V("Zero-G")])

P("COL", "Shower", "Hygiene", LG_1, tier="T1", art="DOM", cls="S",
  mass=80, hp=150, power=-10, recipe={"interior_plate": 6, "glass_panel": 4, "small_tube": 2},
  function="Hygiene +60.", mounts="bottom,back", airtight="none",
  moving=["Door: slide 0.7 m"], sockets=["work@center", "water@back"], vfx=["Shower spray", "Steam"], notes=FURN)

P("COL", "Laundry Station", "Hygiene", LG_1, tier="T2", art="DOM", cls="S",
  mass=90, hp=150, power=-3, recipe={"interior_plate": 6, "motor": 1},
  function="Keeps clothes clean (raises Hygiene decay time by 30%).", mounts="bottom", moving=["Drum spins"],
  sockets=["work@front", "water@back"], notes=FURN)

# ---------------------------------------------------------------------------
# COL — Storage, work & study
# ---------------------------------------------------------------------------
P("COL", "Wardrobe", "Storage", LG_1, tier="T1", art="DOM", cls="S",
  mass=60, hp=120, recipe={"interior_plate": 6},
  function="Holds a survivor's outfits; changing clothes gives a small mood bump.", mounts="bottom,back",
  moving=["Doors ×2: hinge 100°"], sockets=["interact@front"], notes=FURN,
  variants=[V("Wardrobe"), V("Locker", notes="Metal crew locker; name-tag decal slot.")])

P("COL", "Desk", "Work & Study", LG_1, tier="T1", art="DOM", cls="S",
  mass=40, hp=90, recipe={"interior_plate": 4},
  function="Study, letter writing and research (+Purpose).", mounts="bottom", sockets=["seat@center", "work@front", "lcd@top"], notes=FURN)

P("COL", "Bookshelf", "Work & Study", LG_1, tier="T1", art="DOM", cls="S",
  mass=70, hp=100, recipe={"interior_plate": 5, "salvaged_wood": 4},
  function="Skill books and Fun; improves reading-chair bonuses.", mounts="bottom,back", sockets=["interact@front"],
  notes=FURN + " Book fill-level variations (shape keys or separate meshes).")

P("COL", "Classroom Set", "Work & Study", LG_22, tier="T2", art="DOM", cls="M",
  mass=150, hp=250, recipe={"interior_plate": 12, "display": 1},
  function="Desks and a board: children learn skills here ('School in the Stars' quest).",
  mounts="bottom", sockets=["seat@center*6", "work@front", "lcd@back"],
  notes=FURN + " Chalkboard content is a dynamic texture (Lily's drawings, lessons).")

# ---------------------------------------------------------------------------
# COL — Recreation
# ---------------------------------------------------------------------------
P("COL", "Media Wall", "Recreation", LG_2, tier="T1", art="DOM", cls="S",
  mass=50, hp=100, power=-2, recipe={"interior_plate": 4, "display": 4, "computer": 1},
  function="Movies and shows: Fun +15/h for up to 6 viewers.", mounts="back", shape="wall",
  sockets=["lcd@front", "audio@front"], emissive=["Screen"], notes="Wall-mounted screen with a media shelf.")

P("COL", "Arcade Cabinet", "Recreation", LG_1, tier="T2", art="DOM", cls="S",
  mass=100, hp=150, power=-1, recipe={"interior_plate": 6, "display": 1, "computer": 2},
  function="Fun +20/h; competitive survivors bond (or fight) over high scores.", mounts="bottom",
  sockets=["work@front", "lcd@front"], emissive=["Marquee", "Screen"], notes=FURN + " Salvaged 1990s cabinet with a hand-painted marquee.")

P("COL", "Pool Table", "Recreation", LG_2, tier="T2", art="DOM", cls="S",
  mass=300, hp=250, recipe={"interior_plate": 10, "fabric": 4},
  function="Fun +18/h for 2–4 survivors.", mounts="bottom", sockets=["work@front*2", "work@back*2"],
  notes=FURN + " Zero-G variant has magnetic balls (a joke line from Tug).")

P("COL", "Music Corner", "Recreation", LG_1, tier="T2", art="DOM", cls="M",
  mass=60, hp=100, recipe={"interior_plate": 2, "salvaged_wood": 6, "wiring_bundle": 2},
  function="Instruments (guitar, keyboard, drum). Survivors with Art skill perform; performances boost everyone's mood.",
  mounts="bottom", sockets=["seat@center", "work@front", "audio@center"],
  notes=FURN + " Instrument meshes are separate hand props (shared with character animation).")

P("COL", "Gym Set", "Recreation", LG_2, tier="T2", art="DOM", cls="M",
  mass=250, hp=300, recipe={"steel_plate": 6, "small_tube": 6, "motor": 1},
  function="Treadmill and weight rack: Fitness skill, Fun, and required exercise in zero-G.",
  mounts="bottom", moving=["Treadmill belt scroll"], sockets=["work@center*2"], notes=FURN)

P("COL", "Kids' Play Area", "Recreation", LG_22, tier="T2", art="DOM", cls="M",
  mass=120, hp=200, recipe={"interior_plate": 8, "fabric": 10, "bio_plastic": 6},
  function="Slide, soft blocks and a drawing table. Children's Fun and Safety; parents' mood +.",
  mounts="bottom", sockets=["work@center*4", "seat@front*2"],
  notes=FURN + " Drawing table shows the child's current drawing (dynamic texture: Lily's spirals).")

# ---------------------------------------------------------------------------
# COL — Spiritual & story
# ---------------------------------------------------------------------------
P("COL", "Chapel Set", "Spiritual", LG_22, tier="T2", art="DOM", cls="M",
  mass=200, hp=300, recipe={"interior_plate": 10, "salvaged_wood": 12, "fabric": 4},
  function="Altar and pews: comfort for grieving survivors; hosts funerals and weddings.",
  mounts="bottom", sockets=["seat@center*6", "work@front", "light@top"], emissive=["Candles"], vfx=["Candle flames"],
  notes=FURN + " Non-denominational; symbols are swappable decals.")

P("COL", "Memorial Wall", "Spiritual", LG_2, tier="T1", art="DOM", cls="M",
  mass=180, hp=400, recipe={"interior_plate": 8, "steel_plate": 4},
  function="Names of the dead, added by the player. Story furniture: appears in M2.03 and scrolls in the ending (M4.06).",
  mounts="back", shape="wall", sockets=["interact@front", "work@front", "light@bottom*3"],
  emissive=["Candle glow"], vfx=["Candle flames"],
  notes="Name plates are generated text decals (up to 120 names). Leave clear space for photos and drawings people pin up.")

# ---------------------------------------------------------------------------
# COL — Decor
# ---------------------------------------------------------------------------
P("COL", "Rug", "Decor", LG_1, tier="T1", art="DOM", cls="S",
  mass=5, hp=20, recipe={"fabric": 6},
  function="Room Quality + Beauty.", mounts="bottom", shape="floor", notes="2 × 1.4 m floor mesh (4 cm thick) with a fringe. Three patterns.",
  variants=[V("Woven"), V("Kestrel Logo"), V("Tessari Hide", tier="T3")])

P("COL", "Potted Plant", "Decor", LG_1, tier="T1", art="DOM", cls="S",
  mass=15, hp=30, recipe={"bio_plastic": 2, "organics": 2},
  function="Beauty + Comfort; needs occasional watering.", mounts="bottom", sockets=["work@front"],
  notes="Wind/air-vent sway via vertex shader.",
  variants=[V("Earth Fern"), V("Veyra Bloom", tier="T3", notes="Bioluminescent petals (emissive)."),
            V("Juniper Bonsai", tier="T4", notes="Unlocked after M4.04: Crane's bonsai. A quiet easter egg.")])

P("COL", "Art Frame", "Decor", LG_1, tier="T1", art="DOM", cls="S",
  mass=4, hp=15, recipe={"interior_plate": 1},
  function="Displays art made by survivors (Art skill); Beauty +.", mounts="back", shape="panel",
  sockets=["lcd@front"], notes="Picture surface is a dynamic texture. Three frame styles.")

P("COL", "Floor Lamp", "Decor", LG_1, tier="T1", art="DOM", cls="S",
  mass=6, hp=20, power=-0.1, recipe={"interior_plate": 1, "construction_component": 1},
  function="Warm light; Comfort + in bedrooms and lounges.", mounts="bottom", sockets=["light@top"], emissive=["Shade glow"],
  notes="Fabric shade uses translucency.")

# ---------------------------------------------------------------------------
# MED — Medical
# ---------------------------------------------------------------------------
P("MED", "Medicine Cabinet", "Supplies", LG_1, tier="T0", cls="S",
  mass=40, hp=100, recipe={"interior_plate": 4, "medical_component": 1},
  function="Stores medical items; first-aid refill point. The M0.02 cabinet where the player finds the first Suppressant.",
  mounts="back", shape="wall", moving=["Door: hinge 110°"], sockets=["interact@front"], emissive=["Red cross backlight"],
  notes="White cabinet with a red cross; glass door with a crack state.")

P("MED", "Med-Pod", "Treatment", {"LG": (1, 2, 1)}, tier="T1", cls="L",
  mass=1200, hp=1500, power=-50,
  recipe={"interior_plate": 20, "construction_component": 20, "small_tube": 10, "display": 4, "medical_component": 15, "computer": 6},
  function="Respawn point; heals and refills suit O₂ and energy. You respawn at the nearest one.",
  mounts="bottom,back", airtight="all",
  moving=["Canopy: slides up 1.2 m"], sockets=["bed@center", "interact@front", "air@top"],
  emissive=["Scan ring", "Status panel"], vfx=["Scan sweep", "Healing mist"], audio=["Scan hum"],
  notes="Upright pod; the character stands inside. The respawn animation starts inside the pod.")

P("MED", "Medical Bed", "Treatment", LG_1, tier="T1", cls="M",
  mass=150, hp=300, power=-2, recipe={"interior_plate": 8, "medical_component": 4, "display": 1, "fabric": 4},
  function="Patients heal 2× faster; medics treat infection stages here.",
  mounts="bottom", sockets=["bed@center", "work@left", "lcd@top"], emissive=["Patient monitor"],
  notes="Adjustable bed with a monitor arm and IV stand.")

P("MED", "Surgery Table", "Treatment", LG_1, tier="T2", cls="M",
  mass=250, hp=300, power=-5, recipe={"steel_plate": 6, "medical_component": 10, "display": 1},
  function="Surgery and amputation (stops a limb bite at the source). Requires Medicine 8.",
  mounts="bottom", sockets=["bed@center", "work@left", "work@right", "light@top"], emissive=["Surgical lamp"],
  notes="Steel table with an overhead surgical light arm (PART_LampArm).")

P("MED", "Medical Lab", "Research", LG_22, tier="T2", cls="L",
  mass=900, hp=1000, power=-40,
  recipe={"interior_plate": 20, "medical_component": 20, "computer": 10, "display": 4, "glass_panel": 6},
  function="Mara's lab: crafts antivirals, medkits and stims; researches the Verdance.",
  mounts="bottom", sockets=["work@front*2", "lcd@back", "interact@front", "air@top"],
  emissive=["Microscope screens", "Centrifuge lights"], vfx=["Sample mist"],
  notes="Benches, centrifuge, fume hood and a sample fridge.")

P("MED", "Quarantine Cell", "Infection Control", LG_1, tier="T2", cls="M",
  mass=900, hp=2000, power=-8, recipe={"steel_plate": 12, "glass_panel": 12, "filter_mesh": 6, "motor": 2},
  function="Sealed room-in-a-cell with its own air supply. Holds Seeded survivors safely.",
  mounts="all", airtight="all",
  moving=["Door: slide 1.0 m, lockable"], sockets=["bed@center", "air@top", "interact@front"],
  emissive=["Negative-pressure indicator"], notes="Glass front so the patient is visible; a speaker grille for talking.")

P("MED", "Bio-Scanner Gate", "Infection Control", LG_1, tier="T2", cls="M",
  mass=500, hp=900, power=-6, recipe={"steel_plate": 10, "detector_component": 6, "computer": 4, "display": 1},
  function="Walk-through arch that detects infection (including hidden bites) and can trigger locks and alarms.",
  mounts="bottom", sockets=["camera@center", "lcd@front"],
  emissive=["Scan plane (green/red)"], vfx=["Scan sweep"], audio=["Scan chirp", "Alarm"],
  notes="Arch 2.2 m tall, 1.2 m wide.")

P("MED", "Decon Shower", "Infection Control", LG_1, tier="T1", cls="S",
  mass=100, hp=200, power=-10, recipe={"interior_plate": 6, "filter_mesh": 2, "small_tube": 2},
  function="Removes spores from suits and skin (−5% infection exposure if used within a minute); Hygiene +.",
  mounts="bottom,back", sockets=["work@center", "water@back"], emissive=["UV strip"], vfx=["Decon spray"],
  notes="Yellow-and-white hazard version of the Shower.")

P("MED", "Cryo Pod", "Treatment", {"LG": (1, 2, 1)}, tier="T3", cls="L",
  mass=1500, hp=1500, power=-40,
  recipe={"steel_plate": 20, "glass_panel": 6, "medical_component": 20, "computer": 10, "superconductor": 4},
  function="Stasis for a critically infected survivor until a cure exists (Mara's M3.06 option).",
  mounts="bottom,back", airtight="all",
  moving=["Lid: slides up"], sockets=["bed@center", "interact@front"],
  emissive=["Frost-blue interior light", "Vital signs panel"], vfx=["Cryo fog"],
  notes="Frosted glass lid; the occupant is visible through the frost (a mask parameter).")
