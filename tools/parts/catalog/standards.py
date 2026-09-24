"""Global art & modeling standards shared by the generator and the Blender tools.

Everything here is exported into ``docs/parts-bible/data/parts.json`` under
``standards`` so the Blender scaffold/validator scripts use the same numbers.
"""

CELL_M = {"LG": 2.5, "SG": 0.5}
GRID_NAMES = {"LG": "Large grid", "SG": "Small grid"}

# Texel density targets in pixels per metre.
TEXEL_DENSITY = {"LG": 512, "SG": 1024, "1P": 2048, "3P": 1024}

# Complexity classes: LOD0 triangle budgets per grid, construction stages,
# max collision hulls and texture strategy.
COMPLEXITY = {
    "S": {
        "label": "Simple",
        "tris": {"LG": 800, "SG": 300},
        "stages": 2,
        "collision": 2,
        "texture": "Shared trim sheet only (no unique maps)",
    },
    "M": {
        "label": "Standard",
        "tris": {"LG": 4000, "SG": 1500},
        "stages": 3,
        "collision": 6,
        "texture": "Trim sheets + one 1K unique atlas",
    },
    "L": {
        "label": "Complex",
        "tris": {"LG": 12000, "SG": 5000},
        "stages": 3,
        "collision": 12,
        "texture": "Trim sheets + one 2K unique atlas",
    },
    "XL": {
        "label": "Hero",
        "tris": {"LG": 40000, "SG": 12000},
        "stages": 4,
        "collision": 24,
        "texture": "4K unique texture set + trim sheets",
    },
}

LOD_RATIOS = [1.0, 0.5, 0.2, 0.06]          # of LOD0 triangles
LOD_SCREEN_SIZE = [1.0, 0.5, 0.25, 0.1]     # engine switch thresholds
LOD_MIN_TRIS = 12

BUILD_STAGE_NAMES = {
    2: ["BS1 Frame (0–49%)", "BS2 Plated (50–99%)"],
    3: ["BS1 Frame (0–32%)", "BS2 Structure (33–65%)", "BS3 Systems (66–99%)"],
    4: ["BS1 Frame (0–24%)", "BS2 Structure (25–49%)", "BS3 Systems (50–74%)",
        "BS4 Finishing (75–99%)"],
}

ART_SETS = {
    "IND": {"name": "Kestrel Industrial", "materials": "MI_IND_*",
            "look": "Default human tech: worn NASA-punk, stencilled labels, scuffed paint, safety stripes."},
    "SCR": {"name": "Survivor Scrap", "materials": "MI_SCR_*",
            "look": "Act I improvised: welded sheet metal, car parts, road signs, duct tape, spray-paint marks."},
    "DOM": {"name": "Domestic", "materials": "MI_DOM_*",
            "look": "Colony interiors: fabric, wood-look laminate, warm lamps, hand-made touches."},
    "DIR": {"name": "Directorate", "materials": "MI_DIR_*",
            "look": "White ceramic panels, gold trim, hidden seams, sterile blue light."},
    "HAU": {"name": "Hauler", "materials": "MI_HAU_*",
            "look": "Cargo orange, container ribs, graffiti, mismatched repairs."},
    "SOW": {"name": "Sower (grown)", "materials": "MI_SOW_*",
            "look": "Grown, ribbed, coral and shell forms; no right angles; teal glyph emissives."},
}

FACES = {
    "front": "+X", "back": "-X", "left": "+Y", "right": "-Y", "top": "+Z", "bottom": "-Z",
}

SOCKET_TYPES = {
    "conveyor_large": "Large conveyor port (LG 1.0 m aperture)",
    "conveyor_small": "Small conveyor port (0.25 m aperture)",
    "air": "Ventilation port (joins the room/air graph)",
    "water": "Water line port",
    "fuel": "Fuel/hydrogen line port",
    "interact": "Player interaction point (use/terminal)",
    "seat": "Seat / character attach point (hips)",
    "bed": "Sleep attach point (character lies on +Z)",
    "work": "Survivor work slot (character stands here facing the part)",
    "light": "Point/spot light position",
    "lcd": "Screen surface (dynamic texture)",
    "vfx_exhaust": "Thruster/engine exhaust VFX origin (points out of the face)",
    "vfx_smoke": "Smoke/steam VFX origin",
    "vfx_sparks": "Sparks/welding VFX origin",
    "vfx_fire": "Fire VFX origin",
    "muzzle": "Weapon muzzle (projectile spawn, flash)",
    "audio": "Looping audio emitter",
    "attach_top": "Sub-grid attach point (rotor/hinge/piston head)",
    "wheel": "Wheel axle",
    "projector": "Hologram projection origin",
    "camera": "Camera view origin",
    "item_out": "Item output (ejected/produced items)",
    "item_in": "Item intake",
    "door": "Door leaf pivot/slide origin",
}

# Category codes → (registry key, display name, bible chapter file)
CATEGORIES = {
    "STR": ("structure", "Structure & Armor", "02-structure-and-armor.md"),
    "DOR": ("doors", "Doors & Access", "03-doors-and-access.md"),
    "PWR": ("power", "Power & Thermal", "04-power-and-thermal.md"),
    "LIF": ("lifesupport", "Life Support", "05-life-support.md"),
    "PRD": ("production", "Production & Research", "06-production-and-research.md"),
    "AGR": ("agriculture", "Agriculture", "07-agriculture.md"),
    "LOG": ("logistics", "Logistics & Storage", "08-logistics-and-storage.md"),
    "PRO": ("propulsion", "Propulsion, Flight & Launch", "09-propulsion-flight-and-launch.md"),
    "MEC": ("mechanical", "Mechanical", "10-mechanical.md"),
    "CTL": ("control", "Control & Automation", "11-control-and-automation.md"),
    "COL": ("colony", "Colony & Furniture", "12-colony-and-furniture.md"),
    "MED": ("medical", "Medical", "13-medical.md"),
    "DEF": ("defense", "Defense & Weapon Systems", "14-defense-and-weapon-systems.md"),
    "UTL": ("utility", "Utility, Sensors & Lighting", "15-utility-sensors-and-lighting.md"),
    "SOW": ("precursor", "Precursor (Sower)", "16-precursor-sower.md"),
}

CATEGORY_INTROS = {
    "STR": "Hull, frame and interior-structure parts. Armor shapes are the most-placed parts in the game: they must tile perfectly, stay cheap, and read clearly in the Structural View.",
    "DOR": "Everything people and vehicles pass through. Doors define rooms, so airtightness and animation timing are gameplay-critical (airlocks, quarantine, horde defense).",
    "PWR": "Generation, storage and heat. Power parts drive the Attraction score (noise, light, output), so their audio and light sockets matter as much as their meshes.",
    "LIF": "Air, water, pressure and temperature. These parts join the room/air graph through their air and water sockets; spores travel through the same network.",
    "PRD": "Crafting stations, from the Act I workbench to the capital-ship Fabrication Bay. Each has at least one survivor work slot.",
    "AGR": "Food production, from soil planters on Earth to protein vats and Tessari pens in the Drift.",
    "LOG": "Moving and storing items. Conveyor ports must line up exactly across grids; aperture positions are standardized.",
    "PRO": "Everything that moves a grid: thrusters, wheels, wings, drives, tanks and the Act I launch hardware.",
    "MEC": "Parts that create sub-grids and mechanisms: rotors, hinges, pistons, merge blocks and spin-gravity bearings.",
    "CTL": "Cockpits, seats, terminals, screens and no-code logic blocks.",
    "COL": "The Sims pillar in block form: beds, tables, kitchens, showers, recreation and the story furniture (Long Dining Table, Memorial Wall). Survivors use these through seat/bed/work sockets.",
    "MED": "Healing, respawn, quarantine and infection control.",
    "DEF": "Ground defense against Hollows and ship weapons. Turret rigs share one yaw/pitch standard.",
    "UTL": "Lights, sensors, antennas, scanners, tools and suit service.",
    "SOW": "Precursor parts recovered or grown from Sower technology. Organic modeling rules apply (see chapter 19).",
}
