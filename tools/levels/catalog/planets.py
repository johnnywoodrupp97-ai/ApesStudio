"""PLN — planets at voxel-traversal scale (20–120 km diameter).

Every planet is a voxel cube-sphere: six cube-face heightmaps + biome/ore/Bloom maps
generate the base terrain, hand-authored regions are stamped on top, and the full crust
is minable down to the bedrock layer. Derived numbers (horizon, curvature, landmark
heights, travel times, face-map resolution) are computed by build.py.
"""

from . import L

ORE_LAYERS_ROCKY = [("0–50 m", "Iron, silicon, stone, ice (poles)"), ("50–500 m", "Nickel, cobalt, silver, magnesium"),
                    ("500 m – crust base", "Uranium, gold, platinum (rare veins)")]

L("PLN", "Earth (starter planet)", key="earth", type="Planet", act="I (Kestrel Valley), II+ (Earth Returns)",
  size={"w": 120000, "d": 120000, "h": 120000}, playtime="Kestrel Valley ~12 h + Earth Returns",
  summary="The gameplay-scale Earth: a 120 km voxel planet, the largest size in the game. Kestrel Valley is its hand-authored starting region; the rest of the globe is procedural 'Earth Returns' territory (desert, forest, coast, tundra and the ruins of cities) that the Bloom spreads across as the story advances.",
  goals=["Survive the outbreak in Kestrel Valley", "Reach orbit (Act I climax)", "Return anywhere on the globe from Act II"],
  landmarks=["The Bloom glyph drawn across the continents (visible from orbit)", "Launch tower 39-K"],
  build="Allowed (no-build around story anchors)", bloom="Rises with story progress (0% → 45% of the land surface)",
  atmosphere="Breathable", gravity="1.0 g", hazards="Weather, spore storms, hordes",
  planet={"diameter_km": 120, "gravity_g": 1.0, "atmosphere": "Breathable (1 atm)", "sea_level": True, "day_min": 60,
          "biomes": ["High desert (Kestrel Valley)", "Temperate forest", "Coast and ocean", "Tundra and polar ice", "City ruins", "Bloom zones"],
          "ore_layers": ORE_LAYERS_ROCKY,
          "anchors": [("KVL-001 Kestrel Valley", 38.2, -116.3), ("Earth Returns: Prospect metro", 38.4, -116.9),
                      ("Earth Returns: Pacific coast region", 36.0, -121.5), ("Earth Returns: Northern forest", 47.0, -121.0)],
          "orbit": "Haven-9 at 25 km altitude (above the 9 km atmosphere); the Moon's orbit at 360 km from Earth's centre",
          "notes": "Gameplay scale, not astronomical scale: Earth keeps its continents and oceans, compressed into a 377 km circumference. Coastlines and continents come from a stylized cube-face heightmap so the Bloom glyph (M1.07) reads from orbit."},
  kits=["KIT-DST", "KIT-TWN", "KIT-BLM"], markers=["LVL_ANCHOR_KVL-001", "TER_Face_PX"])

L("PLN", "The Moon", key="moon", type="Planet", act="II", size={"w": 40000, "d": 40000, "h": 40000}, playtime="2–5 h",
  summary="A 40 km airless voxel moon: grey regolith, craters, Earthrise, and the Tycho mining outpost. The first world the player lands a self-built ship on.",
  goals=["Build a lander that can lift off in 0.16 g", "Tycho Outpost (M2.04)", "Mine titanium, cobalt and helium-3"],
  landmarks=["Earth in the sky (always visible from the near side)", "Tycho's crater rim"], build="Allowed", bloom="Low (infected miners only at Tycho)",
  atmosphere="None (vacuum)", gravity="0.16 g", hazards="Vacuum, radiation during flares, Burrowers, dust storms (static-charged regolith)",
  planet={"diameter_km": 40, "gravity_g": 0.16, "atmosphere": "None", "sea_level": False, "day_min": 120,
          "biomes": ["Highland regolith", "Maria (dark plains)", "Crater fields", "Polar ice craters"],
          "ore_layers": [("0–30 m", "Silicon, iron, He-3 (surface regolith)"), ("30–300 m", "Titanium, cobalt, nickel"), ("300 m – crust base", "Platinum veins, ice pockets")],
          "anchors": [("ORB-004 Tycho Outpost", -43.3, -11.2), ("Polar ice cache", -88.0, 0.0), ("Lagrange relay crash", 12.0, 40.0)],
          "orbit": "Lunar orbit at 8 km altitude; 360 km from Earth's centre",
          "notes": "Tidally locked: Earth never moves in the near-side sky (a navigation landmark)."},
  kits=["KIT-MIN", "KIT-HAV"], markers=["LVL_ANCHOR_ORB-004"])

L("PLN", "Veyra-4", key="veyra_4", type="Planet", act="III", size={"w": 100000, "d": 100000, "h": 100000}, playtime="1–4 h",
  summary="A 100 km jungle-and-ocean world with purple seas, continent-sized Bloom forests, Tessari herds and a 2 km Sower Garden Engine terraforming it in real time.",
  goals=["Key of Roots (M3.03)", "Heal or plunder the planet", "Tessari Sanctuary"],
  landmarks=["The Garden Engine spire (2 km, visible from 16 km away)"], build="Allowed", bloom="High (falls as the Engine is shut down)",
  atmosphere="Breathable, humid", gravity="0.9 g", hazards="Spore-laden forests, Stalkers, storms",
  planet={"diameter_km": 100, "gravity_g": 0.9, "atmosphere": "Breathable, humid (1.2 atm)", "sea_level": True, "day_min": 80,
          "biomes": ["Violet jungle", "Purple sea and reefs", "Tessari grasslands", "Bloom forest", "Volcanic highlands"],
          "ore_layers": ORE_LAYERS_ROCKY,
          "anchors": [("DRF-004 Garden Engine", 4.0, 22.0), ("Tessari migration plains", -12.0, 40.0)],
          "orbit": "Orbit at 18 km altitude", "notes": "Healing the planet (veyra_healed) repaints the Bloom map over the following in-game days."},
  kits=["KIT-JUN", "KIT-SOW", "KIT-BLM"], markers=["LVL_ANCHOR_DRF-004"])

L("PLN", "Hollowmere", key="hollowmere", type="Planet", act="III", size={"w": 80000, "d": 80000, "h": 80000}, playtime="1–3 h",
  summary="An 80 km ice world at −80 °C: blizzards, ice caves and the Choir's Cathedral of the Hum over a Sower archive.",
  goals=["Key of Echoes (M3.04)", "Cold survival", "Choir alliance"],
  landmarks=["Cathedral of the Hum (candle-lit spires)", "Aurora bands"], build="Allowed (heaters required)", bloom="Medium (under the ice)",
  atmosphere="Thin, freezing", gravity="0.7 g", hazards="Extreme cold, blizzards (visibility 20 m), crevasses",
  planet={"diameter_km": 80, "gravity_g": 0.7, "atmosphere": "Thin, unbreathable (0.4 atm), −80 °C", "sea_level": False, "day_min": 150,
          "biomes": ["Ice plains", "Crevasse fields", "Ice caves", "Frozen sea", "Geothermal vents"],
          "ore_layers": [("0–80 m", "Ice, stone, iron"), ("80–600 m", "Cobalt, nickel, silver"), ("600 m – crust base", "Uranium, platinum")],
          "anchors": [("DRF-005 Cathedral of the Hum", 61.0, -8.0)], "orbit": "Orbit at 14 km altitude",
          "notes": "Blizzards cap visibility at 20 m, so navigation relies on the Cathedral's audio and the aurora."},
  kits=["KIT-ICE", "KIT-SOW"], markers=["LVL_ANCHOR_DRF-005"])

L("PLN", "Drift Planet (procedural)", key="drift_planet", type="Planet", act="III+", size={"w": 120000, "d": 120000, "h": 120000},
  summary="The template every procedural Drift planet is generated from: a seed picks size, type, gravity, atmosphere, biomes, Bloom coverage, ores and points of interest within the voxel-traversal scale.",
  goals=["Exploration, resources, derelicts, Wonders"], build="Allowed", bloom="0–100% by seed",
  atmosphere="By type", gravity="0.1–1.8 g",
  planet={"diameter_km": 120, "diameter_range_km": [20, 120],
          "size_classes": [("Small (moons, barren, ice)", "20–40 km", "35%"), ("Medium (most types)", "40–80 km", "45%"), ("Large (jungle, ocean, Bloomed)", "80–120 km", "20%")],
          "gravity_g": 1.0, "atmosphere": "By type (none / thin / breathable / toxic / spore-laden)", "sea_level": "Ocean and jungle types", "day_min": "30–180",
          "biomes": ["2–5 per planet from the type's pool (see game bible 08 §8.12)"], "ore_layers": ORE_LAYERS_ROCKY, "anchors": [],
          "orbit": "Orbit at atmosphere top + 5 km",
          "notes": "Gravity is a gameplay value chosen by type, not derived from size. Planets under 40 km never get oceans (the sea would dominate the surface)."},
  kits=["KIT-DST", "KIT-JUN", "KIT-ICE", "KIT-BLM"])

OTHER_BODIES = [
    ("Asteroids", "Voxel", "0.1–3 km", "Fully minable; debris belts and the Drift's ore fields"),
    ("Tortuga Drift", "Voxel (hollowed)", "6 km", "Hollow asteroid city (DRF-001); interior cavern 1.5 km"),
    ("Styx (seed pod)", "Authored hero asset", "2.2 km long", "Hollow Sower seed pod (ORB-005); not minable"),
    ("Meridian (gas giant)", "Visual only (impostor + atmosphere shader)", "Renders as 1,500 km", "Orbit-only; the Ark Meridian station orbits it (DRF-006)"),
    ("Seedship Anthesis", "Authored megastructure", "30 km (petal-sails 1,000 km as VFX)", "Act IV (SEE group)"),
    ("Stars", "Sky and lighting", "—", "One star per system; star type drives light color and solar output"),
]

SYSTEM_SCALE = [
    ("Earth surface → Haven-9 (LEO)", "25 km altitude", "About 1 min: launch, atmosphere exit, short space hop (pulse is blocked this close to Earth)"),
    ("Earth → Moon", "360 km centre to centre", "About 30 s by pulse drive, plus the Moon's approach"),
    ("Earth → Styx Wreck", "1,500 km", "About 1 min by pulse drive (needs extended range and radiation shielding, M2.07)"),
    ("Planet → planet in a Drift system", "800–4,000 km", "Pulse drive, 45 s – 2.5 min (may be interrupted by encounters)"),
    ("System → system", "Sower jump lane", "Jump: 10 s charge + 8–12 s jump tunnel, 5 min cooldown"),
]
