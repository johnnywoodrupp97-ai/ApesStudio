"""Level metrics — the numbers every space is built around.

Consistent with the game bible (21 — 3Cs, 22 — Balance) and the parts bible grid
(large-grid cell 2.5 m). The Blender toolkit builds the Metrics Gym from GYM below.
"""

CELL_LG = 2.5
CELL_SG = 0.5

# (category, metric, value, notes)
METRICS = [
    # Player body & movement
    ("Player", "Capsule radius / height", "0.35 m / 1.80 m (1.95 m suited)", "Use suited height for all clearances"),
    ("Player", "Walk / jog / sprint", "1.6 / 3.8 / 6.2 m/s", "Game bible 21"),
    ("Player", "Step height", "0.45 m", "Higher needs a mantle"),
    ("Player", "Max walkable slope", "45°", "Steeper slides; 50° test ramp in the gym"),
    ("Player", "Standing jump height", "0.6 m", "Clears low debris only"),
    ("Player", "Sprint-jump gap", "3.0 m (1 g)", "Scales with gravity: 5.5 m on the Moon"),
    ("Player", "Vault (low mantle)", "≤ 1.0 m", "Waist-high obstacles, fences"),
    ("Player", "High mantle", "1.0–2.0 m", "Above 2.0 m needs ladders, stairs or a jetpack"),
    ("Player", "Crouch clearance", "1.1 m", "Crouch tunnels 1.1–1.3 m tall"),
    ("Player", "Prone / crawl clearance", "0.6 m", "Crawl ducts are 1.2 m square (crawl, not prone)"),
    ("Player", "Jetpack boost (1 g)", "+3.0 m per boost, 2 boosts", "Full flight in zero-G"),
    ("Player", "Zero-G handhold spacing", "≤ 1.5 m", "Along every EVA route"),
    ("Falls", "Safe / hurt / lethal fall (1 g)", "≤ 4 m / 4–12 m / ≥ 12 m", "Scaled by gravity (Moon: ×6)"),
    # Architecture
    ("Architecture", "Door (single / double)", "1.2 × 2.2 m / 2.4 × 2.2 m", "Matches parts bible doors"),
    ("Architecture", "Corridor width (min / standard / wide)", "1.2 / 2.5 / 5.0 m", "2.5 m = one large-grid cell"),
    ("Architecture", "Ceiling height (built / authored)", "2.5 m / 3.0–4.0 m", "Authored interiors leave room for pipes and light"),
    ("Architecture", "Stairs (authored / player-built)", "0.18 rise × 0.28 run (33°) / 0.25 × 0.25 (45°)", "Landings every 12 steps"),
    ("Architecture", "Ladder", "0.3 m rungs, 0.45 m wide clearance", "Top exit needs a 1.2 m landing"),
    ("Architecture", "Railing / window sill", "1.1 m / 1.0 m", "—"),
    ("Architecture", "Low / high cover", "1.0 m / 1.8 m", "Low cover = crouch cover"),
    ("Architecture", "Modular grid", "0.5 m snap, 2.5 m modules", "Player-built blocks fit flush against authored spaces"),
    # Combat & AI perception
    ("Combat", "Melee range", "2.0 m", "—"),
    ("Combat", "Effective ranges (shotgun / rifle / marksman)", "12 / 50 / 150 m", "Sets the size of combat spaces"),
    ("Combat", "Hollow hearing / sight", "5–40 m (noise) / 15 m", "Hollows are nearly blind"),
    ("Combat", "Directorate sight", "60 m", "Drones: 40 m spotlight cone"),
    ("Combat", "Screamer tell readability", "20 m", "Clear line of sight in Screamer spaces"),
    ("Combat", "Horde spawn distance", "≥ 60 m and out of sight", "Never spawn in view"),
    ("Combat", "Combat arena sizes (small / medium / large)", "15–25 / 25–50 / 50–120 m", "—"),
    # Vehicles
    ("Vehicles", "Rover (Mule) width / turning radius", "3.5 m / 8 m", "Top speed 25 m/s"),
    ("Vehicles", "Road lane / two-way road", "4 m / 8 m", "Shoulders 1.5 m"),
    ("Vehicles", "Max drivable slope / ramp", "30°", "—"),
    ("Vehicles", "Vehicle clearance (height)", "5 m", "Bridges, gates, tunnels"),
    # Ships
    ("Ships", "Landing pad (lander / medium / large)", "15 m / 30 m / 80 m diameter", "Capital ships stay in orbit or dock"),
    ("Ships", "Hangar door (small / large grid)", "10 × 6 m / 30 × 15 m", "—"),
    ("Ships", "Docking port spacing", "≥ 40 m", "—"),
    # Open world
    ("Open world", "Landmark visibility (primary / secondary)", "2 km / 500 m", "Every district has one primary landmark"),
    ("Open world", "Something to notice", "every 90 s of travel", "Game bible 08 §8.9"),
    ("Open world", "Base site (minimum flat area)", "50 × 50 m", "At least 6 per open region"),
    ("Open world", "No-build radius around story anchors", "150 m", "Enforced with VOL_NoBuild"),
]

# Navigation agents (radius, height, max step, max slope)
NAV_AGENTS = [
    ("Humanoid", 0.35, 1.80, 0.45, 45, "Player, survivors, Shamblers, Runners, units"),
    ("Suited", 0.40, 1.95, 0.45, 45, "EVA suits, Drifters on gravity decks"),
    ("Crawler", 0.40, 0.60, 0.30, 40, "Crawlers; also uses LG crawl ducts"),
    ("Large", 0.60, 2.10, 0.50, 40, "Enforcers"),
    ("Brute", 0.90, 2.60, 0.60, 35, "Brutes, Burrowers above ground"),
    ("Giant", 1.20, 3.20, 0.80, 35, "Sower Wardens, Seraph exo-frame"),
    ("Tessari", 2.00, 4.90, 0.80, 30, "Tessari adults; large grazer kits"),
    ("Small animal", 0.30, 0.60, 0.25, 50, "Dogs, coyotes, jackrabbits"),
]

# Metrics Gym layout: (lane, label, kind, params). The toolkit lays lanes out along Y.
GYM = [
    ("Jump gaps", [("1 m", "gap", 1.0), ("2 m", "gap", 2.0), ("3 m (max)", "gap", 3.0), ("4 m (fail)", "gap", 4.0)]),
    ("Mantle heights", [("0.45 step", "block", 0.45), ("1.0 vault", "block", 1.0), ("1.5", "block", 1.5), ("2.0 max", "block", 2.0), ("2.5 fail", "block", 2.5)]),
    ("Clearances", [("1.1 crouch", "tunnel", 1.1), ("0.6 prone", "tunnel", 0.6), ("1.2 duct", "tunnel", 1.2), ("2.5 corridor", "tunnel", 2.5)]),
    ("Corridors", [("1.2 min", "corridor", 1.2), ("2.5 standard", "corridor", 2.5), ("5.0 wide", "corridor", 5.0)]),
    ("Doors", [("Single 1.2x2.2", "door", (1.2, 2.2)), ("Double 2.4x2.2", "door", (2.4, 2.2)), ("Vehicle 10x6", "door", (10.0, 6.0))]),
    ("Stairs & ramps", [("Stairs 33°", "stairs", (0.18, 0.28)), ("Stairs 45° built", "stairs", (0.25, 0.25)), ("Ramp 15°", "ramp", 15), ("Ramp 30°", "ramp", 30), ("Ramp 45° max", "ramp", 45), ("Ramp 50° fail", "ramp", 50)]),
    ("Cover", [("Low 1.0", "block", 1.0), ("High 1.8", "block", 1.8), ("Window sill 1.0", "sill", 1.0)]),
    ("Falls", [("4 m safe", "ledge", 4.0), ("8 m hurt", "ledge", 8.0), ("12 m lethal", "ledge", 12.0)]),
    ("Vehicles", [("Road 8 m", "road", 8.0), ("Turn radius 8 m", "turn", 8.0)]),
    ("Landing pads", [("Lander 15 m", "pad", 15.0), ("Medium 30 m", "pad", 30.0), ("Large 80 m", "pad", 80.0)]),
    ("Nav agents", [(a[0], "agent", (a[1], a[2])) for a in NAV_AGENTS]),
]
