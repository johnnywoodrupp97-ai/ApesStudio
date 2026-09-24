"""KVL — Kestrel Valley (open region + districts), KES — Kestrel Complex & Township mission spaces."""

from . import L, S

DESERT = {"time": "60-min day/night cycle; missions set their own time", "palette": [("Desert sand", "#C9A66B"), ("Sage", "#8A9A6B"), ("Sky blue", "#7FB2D9"), ("Sodium night", "#E8A13A")],
          "light": "Hard desert sun by day; sodium floodlights and fires by night"}

# ---------------------------------------------------------------------------
# KVL — the open region
# ---------------------------------------------------------------------------
L("KVL", "Kestrel Valley", type="Open Region", act="I (open from 0:30) + Earth Returns", size={"w": 8000, "d": 8000, "h": 700, "area_km2": 64},
  playtime="2.5 h story, 10+ h exploration", missions=["M1.01–M1.07", "Earth Returns side content"],
  summary="A 64 km² hand-authored open region of Nevada high desert ringed by mountains: the spaceport, its company town and nine other districts. The whole valley is open from the end of the prologue; danger (Bloom threat), not walls, gates the districts.",
  goals=["Find survivors, parts and a base site", "Complete the four Wren parts in any order", "Explore districts for blueprints, caches and stories"],
  spaces=[S("Valley floor", (6000, 6000, 50), "High-desert basin, dry washes, sagebrush", (0, 0, 0)),
          S("Mountain rim", (8000, 8000, 700), "Impassable ring (visual boundary); flyable over from Act II", (0, 0, 0)),
          S("Route 93", (8, 8000, 0), "North–south highway along x = −2 km, with spurs to the Township and Complex", (-2000, 0, 0))],
  connections=[("Route 93", "Kestrel Township", "road"), ("Route 93", "Prospect", "road"), ("Kestrel Township", "Kestrel Aerospace Complex", "road"),
               ("Hollis Dam", "Silver Ridge Mines", "dirt track"), ("Fort Calder", "Red Mesa Observatory", "dirt track")],
  encounters=["Roaming hordes at night (Attraction-driven)", "Runner packs on open ground", "Coyote packs", "Directorate drone patrols near crash sites"],
  landmarks=["Launch tower at Pad 39-K (110 m, visible from anywhere)", "Hollis Dam wall (north)", "Red Mesa radio dishes (southeast)", "Prospect's burning skyline (west)"],
  mood=DESERT, audio="Wind, insects by day, distant moans and coyotes by night; the Verdance clicks rise near Prospect.",
  links="Leads to orbit via the Wren (M1.07); re-entry from Act II anywhere on Earth.",
  build="Allowed (except within 150 m of story anchors)", bloom="●○○○○ to ●●●●● by district", hazards="Heat waves, dust storms, flash floods, spore storms from Prospect",
  kits=["KIT-DST", "KIT-TWN", "KIT-KES", "KIT-BLM"],
  markers=["PS_Main", "SPL_Route93", "VOL_NoBuild_Complex", "VOL_Weather_Global", "VOL_LandingZone_JackrabbitFlats"],
  terrain={"kind": "valley", "rim_height": 650, "floor_noise": 25,
           "features": [["mesa", 2.7, -2.1, 0.55, 120], ["hills", 2.8, 2.6, 1.0, 180], ["basin", 0.3, 3.1, 0.7, -25],
                        ["flat", -2.4, -2.4, 1.0, 0], ["hills", 0.2, -3.0, 0.6, 30]]},
  on_planet={"planet": "PLN-001", "lat": 38.2, "lon": -116.3},
  notes="Authored flat in a local east-north-up frame and stamped onto Earth's cube-face heightmap (planet chapter 03): over 8 km the 60 km-radius surface drops about 133 m at the edges, which the stamp absorbs. Streams as 32 × 32 World Partition cells of 256 m. Districts are level instances placed at their map positions.")


def district(name, x, y, r, *, bloom, summary, goals, spaces, encounters, landmarks, build="Allowed", kits=("KIT-DST", "KIT-BLM"),
             audio="", mood_note="", missions=(), setpieces=(), key=None, notes="", hazards=""):
    L("KVL", name, key=key, type="District", act="I (open world)", size={"w": r * 2000, "d": r * 2000, "h": 150},
      pos=[x, y, r], bloom=bloom, summary=summary, goals=goals, spaces=spaces, encounters=encounters, landmarks=landmarks,
      build=build, kits=list(kits), audio=audio, missions=missions, setpieces=setpieces, notes=notes, hazards=hazards,
      mood={**DESERT, "light": mood_note or DESERT["light"]},
      markers=[f"LM_{name.split(' ')[0]}", f"POI_{name.split(' ')[0]}_Main"])


district("Kestrel Aerospace Complex", 1.0, 0.3, 1.1, key="kestrel_complex", bloom="●●○○○",
         summary="The spaceport: hangars, Terminal B, launch pads, Mission Control, the fuel farm and the Vault beneath. The story hub of Act I.",
         missions=["M0.01–M0.03", "M1.01", "M1.04–M1.07"],
         goals=["Story hub", "Components and tools", "The Wren and Pad 39-K"],
         spaces=[S("Hangar row (Hangars 1–6)", (600, 120, 25), "Hangar 4 is the player's first base", (-300, 200, 0)),
                 S("Terminal B & drop-off", (180, 60, 18), "M0.03 interior", (250, 300, 0)),
                 S("Launch pads 12 and 39-K", (900, 500, 110), "Pad 12 (Seraph) west, 39-K (Wren) east", (300, -300, 0)),
                 S("Mission Control tower", (40, 40, 60), "M1.05 guidance computer", (300, 600, 0)),
                 S("Fuel Farm", (300, 200, 25), "M1.05 fuel", (-600, -500, 0)),
                 S("Vault entrance (BSL-4 block)", (60, 60, 12), "Lift to the Vault (M1.04)", (-100, 600, 0)),
                 S("Substations ×3", (30, 30, 8), "Power-grid puzzle for Mission Control", (700, 100, 0))],
         encounters=["Shamblers in staff uniforms", "Runner packs on the aprons", "Screamers in the Vault", "Bloaters at the Fuel Farm", "Brutes on the Long Night"],
         landmarks=["Launch tower 39-K (110 m)", "Mission Control tower (60 m)", "Hangar 4's orange doors"],
         build="Allowed at Hangar 4 and the aprons; no-build around Pad 39-K until M1.07", kits=("KIT-KES", "KIT-TRM", "KIT-DST", "KIT-BLM"),
         audio="PA systems looping evacuation messages, alarms fading over the first days, wind through hangar doors.")
district("Kestrel Township", -0.9, 0.1, 0.7, key="kestrel_township", bloom="●●○○○",
         summary="The company town: diner, school, library, hardware store, gas station and suburbs. The first scavenging and rescue zone.",
         missions=["M1.02", "M1.05 (warehouse)"], goals=["Food, tools, first survivors (Lily, Danny, Rosa, the Webbs, Kenji)"],
         spaces=[S("Main Street", (400, 40, 12), "Diner, hardware store, pharmacy, clinic", (0, 0, 0)),
                 S("Kestrel Elementary", (70, 50, 10), "M1.02", (-250, 200, 0)),
                 S("Suburbs (3 blocks)", (500, 400, 10), "Lootable houses, backyards", (100, -300, 0)),
                 S("Warehouse district", (200, 150, 12), "M1.05 heat-shield tiles", (300, 250, 0)),
                 S("Skate park & library", (120, 80, 8), "Theo; the Webbs", (-300, -150, 0))],
         encounters=["Shamblers in homes (knocking)", "Crawlers under cars", "Runner packs on Main Street at dusk"],
         landmarks=["Water tower with 'KESTREL' painted on it", "Diner's neon coffee cup"], kits=("KIT-TWN", "KIT-DST", "KIT-BLM"),
         audio="Wind chimes, a looping car alarm, dogs barking (Danny's strays).")
district("Route 93 & the Truck Stop", -2.0, 1.9, 0.6, key="route_93", bloom="●○○○○",
         summary="The highway: pile-ups, abandoned trailers and a fortified truck stop (Big Mo). Safest early loot; a roaming trader.",
         goals=["Early loot, vehicles for parts, the roaming trader"],
         spaces=[S("Truck stop & diner", (120, 80, 10), "Big Mo's fortified rig", (0, 0, 0)), S("Pile-up (1 km)", (40, 1000, 6), "Car maze with Crawlers", (-100, -90, 0)),
                 S("Overpass", (60, 20, 12), "Aiyana holds it (M1.05)", (0, 500, 0))],
         encounters=["Crawlers in the pile-up", "Light Shambler traffic"], landmarks=["Truck-stop pylon sign (30 m)"], kits=("KIT-DST", "KIT-TWN"),
         audio="Wind across asphalt, a CB radio crackling.")
district("Jackrabbit Flats", -2.4, -2.4, 1.0, key="jackrabbit_flats", bloom="●○○○○",
         summary="A dry lake bed and old airstrip: flat, open, fast. The safest outpost site and the place to test rovers and aircraft.",
         goals=["Safe base site", "Rover speed runs", "Aircraft parts at the airstrip"],
         spaces=[S("Dry lake bed", (2000, 1600, 0), "Flat salt pan", (0, 0, 0)), S("Airstrip & hangar", (1200, 60, 12), "Aircraft parts", (400, 500, 0)),
                 S("Ranch", (200, 150, 10), "Nora and Ben", (-600, 600, 0))],
         encounters=["Runner packs in the open at night", "Coyotes", "Wild horses"], landmarks=["Windsock tower", "Crashed crop-duster"],
         audio="Open wind, distant horses.", hazards="Mirage heat shimmer; dust devils")
district("Hollis Dam & Reservoir", 0.3, 3.1, 0.8, key="hollis_dam", bloom="●●●○○",
         summary="A hydroelectric dam, lake and marina in the northern canyon. Restoring it gives enormous power, and enormous Attraction.",
         goals=["Clean water", "Huge power if restored (a base-site choice)", "Pete Hollis"],
         spaces=[S("Dam wall & powerhouse", (400, 60, 120), "Turbine hall interior", (0, 0, 0)), S("Reservoir", (1200, 760, 30), "Lake and marina behind the dam", (0, 410, -25)),
                 S("Spillway canyon", (100, 600, 80), "Micro-hydro turbine sites", (0, -480, -40))],
         encounters=["Shamblers in the powerhouse", "Drowned Hollows in the marina (slow, water-logged)", "Green Moon waves if the dam is powered"],
         landmarks=["The dam wall (visible from the Complex)"], audio="Rushing water, turbine hum when restored.")
district("Silver Ridge Mines", 2.8, 2.6, 0.8, key="silver_ridge", bloom="●●●○○",
         summary="Open-pit and shaft mines in the northeastern hills: iron, copper and silicon, with Burrowers in the deep shafts.",
         goals=["Ore", "Hannah Lindqvist", "Mining machinery parts"],
         spaces=[S("Open pit", (600, 600, 150), "Terraced pit", (0, 0, -150)), S("Shaft head & processing", (150, 100, 40), "Elevator cage to the shafts", (400, 300, 0)),
                 S("Deep shafts", (40, 400, 200), "Mine-kit tunnels; Burrowers", (400, 300, -200))],
         encounters=["Miner Hollows", "Burrowers (preview)", "Cave-ins"], landmarks=["Head-frame tower (45 m)"], kits=("KIT-MIN", "KIT-DST", "KIT-BLM"),
         audio="Creaking timbers, dripping water, machinery ghosts.")
district("Red Mesa Observatory", 2.7, -2.1, 0.5, key="red_mesa", bloom="●●○○○",
         summary="A radio-telescope array on a 120 m mesa: early signal decoding, Styx lore and a sniper's-eye view of the valley.",
         goals=["Signal decoder data", "Fatima Haddad", "Walt's Styx logs"],
         spaces=[S("Mesa top & dish array", (500, 500, 30), "Six 25 m dishes", (0, 0, 120)), S("Control building", (40, 30, 8), "Transmitters", (100, 50, 120)),
                 S("Switchback road", (30, 700, 120), "Only vehicle access (800 m of hairpins folded into 700 m)", (-300, -120, 0))],
         encounters=["Few Hollows (hard to reach)", "Directorate drone scouting"], landmarks=["Radio dishes (seen from 5 km)"],
         audio="High wind, dish servos, radio static with the five-note pulse.")
district("Fort Calder", 0.2, -2.9, 0.7, key="fort_calder", bloom="●●●●○",
         summary="An abandoned military base overrun during the evacuation: weapons, armor, vehicles and blueprint fragments (the railgun). Very dangerous.",
         goals=["Weapons and armor", "Military vehicles", "Blueprint fragments", "Chuy Ibarra"],
         spaces=[S("Barracks", (200, 120, 10), "Dense Shamblers in uniform", (-200, 100, 0)), S("Armory bunker", (60, 40, 8), "Locked; power-puzzle", (100, 0, -6)),
                 S("Motor pool", (250, 150, 10), "Military trucks", (200, -200, 0)), S("Airfield & tower", (600, 60, 20), "Helicopter wrecks", (0, -450, 0))],
         encounters=["Soldier Hollows", "Brutes", "Screamer on the tower", "Sentry turrets (still active)"], landmarks=["Control tower with a red beacon"],
         audio="Looping emergency broadcast, flags snapping.", hazards="Minefields (marked by signs)")
district("Prospect (City Edge)", -3.15, 0.9, 0.8, key="prospect", bloom="●●●●●",
         summary="The edge of a small city swallowed by a Bloom Heart cluster. The best loot on Earth and the worst danger; the source of spore storms.",
         goals=["Best loot on Earth", "Destroy Bloom Hearts to push back the Bloom", "End-game for Earth"],
         spaces=[S("Downtown blocks", (600, 600, 60), "Office towers overgrown", (0, 0, 0)), S("Hospital", (120, 80, 30), "Medical loot", (200, 200, 0)),
                 S("Bloom Heart cluster", (300, 300, 40), "3 Hearts", (-200, -100, 0)), S("Overpass exit", (40, 300, 15), "Route 93 connection", (400, 0, 0))],
         encounters=["Hordes", "Screamers", "Brutes", "Bloaters", "Bloom Hearts"], landmarks=["Burning skyline and a green spore haze"],
         kits=("KIT-TWN", "KIT-DST", "KIT-BLM"), audio="The Verdance clicks at full intensity; distant collapses.", hazards="Spore storms (masks required)")
district("Ghost Towns", 1.7, -1.1, 0.25, key="ghost_towns", bloom="●●○○○",
         summary="Three silver-rush ruins (a motel, a church, a main street) with survivor camps, side stories and hidden caches. One is here; the others sit at (−1.1, −1.6) and (3.3, 0.4) km.",
         goals=["Survivor camps", "Side stories", "Hidden caches"],
         spaces=[S("Silverton main street", (200, 40, 10), "Saloon, church", (0, 0, 0)), S("Dusty Rest Motel", (80, 40, 8), "Camp; satellite site at (−1.1, −1.6) km in KVL-001, blocked out here for layout"),
                 S("St. Brigid's Church", (40, 20, 18), "Survivor camp in the nave; satellite site at (3.3, 0.4) km in KVL-001, blocked out here for layout")],
         encounters=["Light Shamblers", "Survivor camps (friendly or hostile)"], landmarks=["Church steeple", "Motel sign"], kits=("KIT-TWN", "KIT-DST"),
         audio="Creaking signs, tumbleweeds, church bell in the wind.")

# ---------------------------------------------------------------------------
# KES — Kestrel Complex & Township mission spaces
# ---------------------------------------------------------------------------
L("KES", "Mission Control 2068", key="mission_control_2068", type="Set Piece", act="Cold Open", missions=["Cold Open"], size={"w": 30, "d": 20, "h": 6},
  pos=[1.3, 0.9], playtime="3 min",
  summary="Kestrel Mission Control three years before the outbreak. Warm monitors, cold coffee: the player operates the Persephone arm and Styx flinches.",
  goals=["Operate the drill arm", "Witness the flinch"],
  spaces=[S("Control floor", (30, 14, 6), "Four tiered console rows", (0, 0, 0)), S("Arm console", (3, 2, 1.2), "Player position (two joysticks)", (-4, -2, 0.5)),
          S("Back row", (30, 3, 6), "Mara stands here", (0, 7, 0.5)), S("Main screen wall", (20, 1, 6), "Styx feed", (0, -9.5, 0))],
  setpieces=["The flinch on the main screen", "Crane's hand on the shoulder (C01)"], landmarks=["Main screen"],
  mood={"time": "Night, November 2068", "palette": [("CRT warm", "#E8B26A"), ("Console blue", "#3A6EA5"), ("Coffee brown", "#6F4E37")], "light": "Screen glow only"},
  audio="Mission chatter, countdown, the room erupting; five radio pulses at the cut.", build="None (story)", kits=["KIT-KES"],
  markers=["PS_ColdOpen", "CAM_C01_Flinch", "TRG_ColdOpen_Drill"],
  notes="Same room as the Mission Control Tower's control floor (KES-009), dressed three years earlier.")

L("KES", "Hangar 4", key="hangar_4", type="Hub", act="Prologue–I", missions=["M0.01", "M0.03 (end)", "M1.01", "M1.06"], size={"w": 60, "d": 40, "h": 20},
  pos=[0.7, 0.5], playtime="Recurring (first base)",
  summary="Where the game begins and the player's first base. A cavernous hangar with the Wren launch stack, a parts cage, an office mezzanine and huge orange doors.",
  goals=["Tutorial (M0.01)", "Weld the doors (M0.03)", "Build the first base (M1.01)", "Defend it on the Long Night (M1.06)"],
  map="""
   N ┌──────────────── HANGAR 4 (60 × 40 m) ───────────────┐
     │  [Office mezzanine +6 m]        [Roof hatch → roof]  │
     │  ┌────────┐                                          │
     │  │ Parts  │        ┌──────────────┐                  │
     │  │ cage   │        │  WREN STACK  │   [Workbench]    │
     │  └────────┘        └──────────────┘                  │
     │ [Service door → corridors]                           │
     └════════ HANGAR DOORS (orange, 30 × 15 m) ════════════┘ S → apron""",
  spaces=[S("Hangar floor", (60, 40, 20), "Open build space", (0, 0, 0)), S("Wren launch stack", (8, 8, 18), "Crew vehicle under assembly", (0, 2, 0)),
          S("Parts cage", (10, 8, 4), "Where Tug is pinned (M0.02)", (-20, 8, 0)), S("Office mezzanine", (20, 8, 3), "Overlooks the floor", (-18, 16, 6)),
          S("Hangar doors", (30, 1, 15), "Welded shut in M0.03", (0, -20, 0)), S("Roof", (60, 40, 1), "Watch the arks leave", (0, 0, 20))],
  connections=[("Hangar floor", "Parts cage", "door"), ("Hangar floor", "Office mezzanine", "stairs"), ("Office mezzanine", "Roof", "ladder"),
               ("Hangar floor", "Hangar doors", "hangar door")],
  encounters=["Scripted horde at the doors (M0.03)", "First Horde Night (M1.01)", "Long Night (M1.06)"],
  setpieces=["Welding the doors under pressure", "Rooftop: the ark fleet (C03)"], landmarks=["The Wren stack", "Orange doors"],
  mood={"time": "Night (prologue), then player-driven", "palette": [("Kestrel orange", "#F26B1D"), ("Hangar grey", "#5A5F66"), ("Work-light white", "#F2F0E6")], "light": "Work lights, then the player's own"},
  audio="Big reverb, humming lights, rain on the roof.", build="Allowed (the first base)", kits=["KIT-KES", "KIT-BLM"],
  markers=["PS_M0_01", "TRG_M0_03_WeldDoors", "CAM_C03_Roof", "HS_M1_06_North", "HS_M1_06_East"])

L("KES", "Service Corridors", key="service_corridors", type="Interior", act="Prologue", missions=["M0.02"], size={"w": 120, "d": 40, "h": 6},
  pos=[0.6, 0.6], playtime="10 min",
  summary="Dark service corridors behind the hangar row. Emergency strobes, a first Hollow (Dana Marsh) and Tug trapped under a parts rack.",
  goals=["Find Tug", "Learn stealth, melee and the infection meter"],
  spaces=[S("Corridor loop", (100, 3, 3.5), "Main path with side rooms", (0, 0, 0)), S("Security station", (8, 6, 3.5), "Dana's post; glass window", (-30, 6, 0)),
          S("Med cabinet alcove", (4, 3, 3.5), "First Suppressant", (10, -4, 0)), S("Parts cage B", (14, 10, 5), "Tug and the forklift", (45, 10, 0)),
          S("Blast doors", (6, 1, 3), "Sealed on Code Black", (-50, 0, 0))],
  connections=[("Corridor loop", "Security station", "door"), ("Corridor loop", "Med cabinet alcove", "open"), ("Corridor loop", "Parts cage B", "door")],
  encounters=["Dana Marsh (first Hollow)", "2 Shamblers", "1 Crawler (tutorial)"], setpieces=["Dana knocks three times", "Forklift rescue"],
  landmarks=["Emergency strobes guide the path"], mood={"time": "Night", "palette": [("Strobe red", "#FF3B30"), ("Concrete", "#6E6E6E")], "light": "Strobes and flashlight"},
  audio="Alarms, dripping, the Verdance clicks for the first time.", kits=["KIT-KES"],
  markers=["PS_M0_02", "SP_DanaMarsh", "TRG_M0_02_Scratch", "TRG_M0_02_Forklift"])

L("KES", "Terminal B", key="terminal_b", type="Set Piece", act="Prologue", missions=["M0.03"], size={"w": 180, "d": 60, "h": 18},
  pos=[1.25, 0.6], playtime="6 min",
  summary="The evacuation collapses: a crowd, Hollows inside it, a skywalk falling and a fuel truck exploding. The player carries Tug to Pad 12.",
  goals=["Get Tug to Pad 12 before the Seraph leaves"],
  map="""
  HANGAR 4 → service road → ┌ CONCOURSE ─ crowd ┐→┌ GATES ─ barricade ┐→ baggage → ┌ SKYWALK (collapses) ┐ → DROP-OFF (fuel truck) → APRON → PAD 12
                            └───────────────────┘ └────────────────────┘           └─────────────────────┘""",
  spaces=[S("Concourse", (60, 30, 12), "Crowd crush (80 civilians, 12 Hollows)", (-60, 0, 0)), S("Gate hall", (40, 30, 10), "Directorate barricade", (-10, 0, 0)),
          S("Baggage handling", (30, 20, 6), "Stealth detour", (15, -18, -6)), S("Skywalk", (40, 6, 4), "Scripted collapse into baggage hall", (35, 0, 8)),
          S("Drop-off lane", (40, 20, 8), "Fuel-truck explosion; exits onto the apron", (68, -10, 0))],
  connections=[("Concourse", "Gate hall", "open"), ("Gate hall", "Baggage handling", "door"), ("Baggage handling", "Skywalk", "stairs"), ("Skywalk", "Drop-off lane", "open")],
  encounters=["12 Shamblers in 80 civilians (crowd sim)", "6 burning Shamblers on the apron"], setpieces=["Skywalk collapse", "Fuel-truck explosion"],
  landmarks=["Departure boards flashing EVACUATE", "Pad 12 floodlights through the glass"],
  mood={"time": "Night", "palette": [("Terminal white", "#E8E8E8"), ("Fire orange", "#FF7A1A"), ("Emergency red", "#FF3B30")], "light": "Emergency lighting, fire"},
  audio="PA in four languages, crowd walla, alarms; music drops at the fence.", kits=["KIT-TRM", "KIT-KES", "KIT-BLM"],
  markers=["PS_M0_03", "TRG_M0_03_Skywalk", "TRG_M0_03_FuelTruck", "CAM_M0_03_Skywalk"],
  notes="Detailed flow and beats: game bible 18 §18.1.")

L("KES", "Pad 12", key="pad_12", type="Set Piece", act="Prologue", missions=["M0.03"], size={"w": 200, "d": 150, "h": 40}, pos=[0.9, -0.3], playtime="3 min",
  summary="The fence standoff: two hundred people at the wire, troopers at the gate, the Seraph on the pad. Ada leaves.",
  goals=["Reach the fence", "Witness the ramp close"],
  spaces=[S("Crowd fence line", (120, 10, 4), "200 civilians", (0, -40, 0)), S("Trooper gate", (12, 6, 4), "Directorate troopers", (0, -35, 0)),
          S("Seraph pad", (50, 50, 20), "Shuttle with ramp down", (0, 20, 0)), S("Retreat road", (8, 60, 0), "Back to Hangar 4 (leaves the level at the south edge)", (-80, -44, 0))],
  setpieces=["Standoff (in-engine)", "Ramp closes (C02)", "Exhaust wash scatters the crowd"], encounters=["None (scripted)"],
  landmarks=["The Seraph under floodlights"], mood={"time": "Night", "palette": [("Floodlight white", "#F4F6F8"), ("Directorate gold", "#C9A227")], "light": "Stadium floodlights"},
  audio="Radio only: Ada and Crane. Wind. The launch roar.", kits=["KIT-KES"], markers=["PS_M0_03_Fence", "CAM_C02_Ramp", "TRG_M0_03_Standoff"])

L("KES", "Kestrel Elementary", key="kestrel_elementary", type="Interior", act="I", missions=["M1.02"], size={"w": 70, "d": 50, "h": 10}, pos=[-1.15, 0.3], playtime="25 min",
  summary="A two-floor school with a vent network. Lily guides the player through the building from inside the vents; the gym holds a horde.",
  goals=["Find the survivor", "Escape the gym"],
  spaces=[S("Classroom wing (1F)", (40, 12, 4), "Barricaded classes, drawings", (-15, 15, 0)), S("Library", (16, 12, 4), "Juice-box trail", (18, 15, 0)),
          S("Office", (12, 10, 4), "Ms. Alvarez's radio", (28, 5, 0)), S("Hallways", (60, 4, 4), "Main route", (0, 5, 0)),
          S("Cafeteria", (24, 16, 4.5), "Fortified by the teacher", (15, -8, 0)), S("Gym", (30, 20, 9), "The horde set piece", (-15, -12, 0)),
          S("Vent network", (60, 40, 1.2), "Crawl ducts above everything (Lily's route)", (0, 0, 4.2))],
  connections=[("Hallways", "Classroom wing (1F)", "door"), ("Hallways", "Library", "door"), ("Hallways", "Office", "door"), ("Hallways", "Cafeteria", "double door"),
               ("Cafeteria", "Gym", "double door"), ("Hallways", "Vent network", "vent grille")],
  encounters=["18 Shamblers", "4 Crawlers", "Runner pack (3) at the exit"], setpieces=["Vent-guide sequence", "Fire alarm and sprinklers split the horde"],
  landmarks=["Lily's spiral drawings mark the route"], mood={"time": "Late afternoon", "palette": [("Classroom yellow", "#F4D35E"), ("Locker blue", "#3E5C76")], "light": "Dusty sunbeams, then flashlight"},
  audio="Near silence; Lily's binaural whisper; sprinklers bring release.", kits=["KIT-TWN", "KIT-BLM"],
  markers=["PS_M1_02", "SP_MsAlvarez", "TRG_M1_02_Vents", "TRG_M1_02_FireAlarm", "CAM_M1_02_Gym"], notes="Flow: game bible 18 §18.2.")

L("KES", "Ark Transport Crash Site", key="ark_crash_site", type="Set Piece", act="I", missions=["M1.03"], size={"w": 150, "d": 150, "h": 30}, pos=[-0.2, -1.4], playtime="15 min",
  summary="A Directorate transport shot down by its own drones. Idris is the only survivor.",
  goals=["Reach the crash", "Decide Idris's fate"],
  spaces=[S("Wreck fuselage", (40, 8, 8), "Interior with bodies (covered)", (0, 0, 0)), S("Debris field", (150, 150, 5), "Loot and cover", (0, 0, 0)),
          S("Idris's position", (6, 6, 3), "Under the wing", (12, 6, 0))],
  encounters=["Drone patrol (2 Sentinels)", "Shamblers drawn by smoke"], setpieces=["Drones sweeping searchlights"], landmarks=["Smoke column (visible 3 km)"],
  mood={"time": "Morning", "palette": [("Burnt black", "#1E1E1E"), ("Directorate white", "#F4F6F8")], "light": "Harsh morning sun through smoke"},
  audio="Fire crackle, drone hum.", build="Restricted", kits=["KIT-DIR", "KIT-DST"], markers=["PS_M1_03", "SP_Idris", "SP_SentinelDrone_01", "SP_SentinelDrone_02"])

L("KES", "The Vault", key="the_vault", type="Dungeon", act="I", missions=["M1.04"], size={"w": 90, "d": 90, "h": 24}, pos=[0.9, 0.9], playtime="25 min",
  summary="The BSL-4 lab beneath the Complex: flooded sub-levels, dead scientists behind glass, the first Screamer and the first Bloom Heart.",
  goals=["Reach Mara", "Recover the Persephone Drive"],
  map="""
  LIFT ▼  SL1 offices (dry) ──► SL2 labs (knee-deep flood, Screamer) ──► SL3 CONTAINMENT (Bloom Heart) ──► Mara's safe room
          records: EDEN order          sample fridges                     coral of bodies (growths only)""",
  spaces=[S("Lift shaft", (6, 6, 24), "Entry from the surface block", (-38, 38, 0)), S("Sub-level 1 offices", (60, 30, 3.5), "Records, the EDEN order", (0, 25, 16)),
          S("Sub-level 2 labs", (70, 40, 4), "Flooded 0.6 m; Screamer", (0, -5, 8)), S("Sub-level 3 containment", (40, 40, 8), "The Bloom Heart", (10, -25, 0)),
          S("Mara's safe room", (8, 6, 3), "Pressure-locked", (38, -38, 0))],
  connections=[("Lift shaft", "Sub-level 1 offices", "lift"), ("Sub-level 1 offices", "Sub-level 2 labs", "stairs"), ("Sub-level 2 labs", "Sub-level 3 containment", "airlock"),
               ("Sub-level 3 containment", "Mara's safe room", "door")],
  encounters=["Scientist Shamblers", "First Screamer", "Bloom Heart defense waves"], setpieces=["Bloom Heart reveal (C04)"], landmarks=["Green glow from SL3"],
  mood={"time": "Timeless (underground)", "palette": [("BSL-4 blue", "#2F6DB5"), ("Bloom green", "#7FD06B"), ("Emergency red", "#FF3B30")], "light": "Emergency strips, Bloom glow"},
  audio="Dripping, pumps failing, jazz playing on a lab radio (Mara's log).", hazards="Spores (masks), electrified water", kits=["KIT-KES", "KIT-DIR", "KIT-BLM"],
  markers=["PS_M1_04", "SP_Screamer_01", "SP_BloomHeart_Vault", "CAM_C04_Coral", "VOL_Spores_SL3"])

L("KES", "Mission Control Tower", key="mission_control_tower", type="Interior", act="I", missions=["M1.05 (Guidance Computer)"], size={"w": 40, "d": 40, "h": 60},
  pos=[1.3, 0.9], playtime="30 min",
  summary="The control tower: restore power at three outdoor substations (a grid puzzle), then climb to the control floor for the guidance computer and Ada's recording.",
  goals=["Restore three substations", "Recover the guidance computer", "Find Ada's pre-flight recording"],
  spaces=[S("Lobby", (30, 20, 6), "Security desk", (0, 0, 0)), S("Stair core", (8, 8, 60), "12 flights; lift dead until powered", (14, 14, 0)),
          S("Control floor", (30, 20, 6), "The cold-open room, three years later", (0, 0, 48)), S("Roof antenna", (20, 20, 12), "Radio mast", (0, 0, 54))],
  connections=[("Lobby", "Stair core", "door"), ("Stair core", "Control floor", "door"), ("Control floor", "Roof antenna", "ladder")],
  encounters=["Staff Shamblers", "Runners on the stairs"], setpieces=["Lights coming on floor by floor"], landmarks=["Tower visible from the whole Complex"],
  mood=DESERT, audio="Wind at the top, servers rebooting.", kits=["KIT-KES"], markers=["PS_M1_05_Tower", "POI_AdaRecording", "TRG_M1_05_Substations"])

L("KES", "Fuel Farm", key="fuel_farm", type="Set Piece", act="I", missions=["M1.05 (Fuel)"], size={"w": 300, "d": 200, "h": 25}, pos=[0.4, -0.2], playtime="30 min",
  summary="Rows of LOX and methane tanks, pipe racks and a pump house. Guns are dangerous here; Bloaters are everywhere. Walt waits in the office.",
  goals=["Fill the Wren's tanks", "Rescue Walt"],
  spaces=[S("Tank rows", (200, 120, 25), "Explosive tanks as cover (and hazards)", (0, 0, 0)), S("Pump house", (30, 20, 8), "Valve puzzle", (100, 60, 0)),
          S("Farm office", (12, 10, 4), "Walt and his telescope", (-120, 80, 0)), S("Pipe racks", (250, 8, 10), "Elevated route", (0, -80, 6))],
  encounters=["Bloaters (6)", "Shamblers"], setpieces=["Chain explosion if the player fires carelessly"], landmarks=["Frosted LOX tanks"],
  mood=DESERT, audio="Hissing boil-off, metal ticking in the heat.", hazards="Explosive tanks, LOX frost burns", kits=["KIT-KES", "KIT-DST"],
  markers=["PS_M1_05_Fuel", "SP_Bloater_01", "SP_Bloater_02", "SP_Walt"])

L("KES", "Township Warehouse", key="township_warehouse", type="Interior", act="I", missions=["M1.05 (Heat Shield Tiles)"], size={"w": 120, "d": 110, "h": 12}, pos=[-0.6, 0.35], playtime="25 min",
  summary="A logistics warehouse with the heat-shield tiles; the first rover (the Mule) is built here, and Runner packs hunt the open lot outside.",
  goals=["Recover heat-shield tiles", "Build the Mule rover"],
  spaces=[S("Racking aisles", (60, 40, 12), "Vertical loot, forklift paths", (0, 25, 0)), S("Loading dock", (80, 10, 5), "Truck bays", (0, 0, 0)), S("Lot", (120, 50, 0), "Runner ambush on the drive out", (0, -30, 0))],
  encounters=["Runner packs", "Shamblers in the aisles"], setpieces=["Rover escape across the lot"], landmarks=["Warehouse sign 'DELGADO LOGISTICS'"],
  mood=DESERT, audio="Forklift beeps, echoing racks.", kits=["KIT-TWN", "KIT-KES"], markers=["PS_M1_05_Warehouse", "TRG_M1_05_Mule"])

L("KES", "Crashed Ark Shuttle", key="crashed_ark_shuttle", type="Set Piece", act="I", missions=["M1.05 (Life Support)"], size={"w": 120, "d": 120, "h": 20}, pos=[1.9, -0.9], playtime="25 min",
  summary="A crashed Directorate shuttle guarded by drones, with cleanup crews burning survivors nearby. Source of the Wren's life-support module.",
  goals=["Recover the life-support module", "Avoid or fight the cleanup crew"],
  spaces=[S("Shuttle wreck", (35, 12, 8), "Interior with the module", (0, 0, 0)), S("Cleanup camp", (40, 30, 4), "Hazmat crews, burn pits", (40, 30, 0)), S("Drone perimeter", (120, 120, 20), "Searchlight patrols", (0, 0, 0))],
  encounters=["Sentinel drones", "Directorate cleanup crew", "Shamblers drawn by fire"], setpieces=["Cleanup crew burning a camp (seen from cover)"],
  landmarks=["Burn-pit smoke"], mood={"time": "Dusk", "palette": [("Hazmat white", "#F4F6F8"), ("Fire orange", "#FF7A1A")], "light": "Flames, drone searchlights"},
  audio="Flamethrowers, drone hum, Directorate radio chatter.", build="Restricted", kits=["KIT-DIR", "KIT-DST"],
  markers=["PS_M1_05_Shuttle", "SP_CleanupCrew_01", "SP_SentinelDrone_03"])

L("KES", "Pad 39-K", key="pad_39k", type="Set Piece", act="I", missions=["M1.06", "M1.07"], size={"w": 250, "d": 250, "h": 110}, pos=[1.5, -0.2], playtime="25 min",
  summary="The Wren's launch pad: a 110 m tower, the 300 m fuel line back to the farm and a perimeter the player fortifies for the Long Night, then the launch.",
  goals=["Defend the hangar and fuel line (M1.06)", "Load cargo and launch (M1.07)"],
  spaces=[S("Launch tower", (20, 20, 110), "Clamps, gantry, valve (Lily's moment)", (0, 0, 0)), S("Pad deck", (80, 80, 2), "Flame trench", (0, 0, 0)),
          S("Fuel line", (4, 124, 3), "Pad segment of the 300 m line to the fuel farm; must stay intact during the siege", (-80, -62, 0)), S("Perimeter", (250, 250, 5), "Player-built defenses", (0, 0, 0)),
          S("Blockhouse", (20, 15, 6), "Launch control", (90, -90, 0))],
  encounters=["Long Night: ~140 Hollows in 3 waves, 4 Brutes, 3 Screamers, 6 Bloaters"], setpieces=["Lily's valve", "Clamp jam and Tug's choice", "Playable launch"],
  landmarks=["The tower itself"], mood={"time": "Night → dawn", "palette": [("Floodlight", "#F2F0E6"), ("Rocket flame", "#FFB84D")], "light": "Floodlights, engine glow, dawn"},
  audio="Engine test roar, horde bed, silence in orbit.", build="Allowed (perimeter) during M1.06", kits=["KIT-KES", "KIT-DST", "KIT-BLM"],
  markers=["PS_M1_06", "HS_M1_06_West", "HS_M1_06_South", "HS_M1_06_FuelLine", "TRG_M1_07_Launch", "CAM_C05_Glyph"], notes="Flows: game bible 18 §18.3–18.4.")
