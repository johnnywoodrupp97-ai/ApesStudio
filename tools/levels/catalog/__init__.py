"""EXODUS PROTOCOL level catalog — single source of truth for the Level Design Bible.

Edit the modules here, then run ``python3 tools/levels/build.py``. The Blender level
toolkit (tools/blender/exodus_levels.py) reads the generated docs/level-bible/data/levels.json.

Conventions: metres, +Z up. Level coordinates: +X east, +Y north (top-down maps),
origin at the level centre on the ground. Space positions are floor-centre points.
"""

GROUPS = {
    "PLN": ("Planets & Voxel Scale", "03-planets-and-voxel-scale.md"),
    "KVL": ("Kestrel Valley — Open Region & Districts", "04-kestrel-valley.md"),
    "KES": ("Kestrel Complex & Township — Mission Spaces", "05-kestrel-complex-and-township.md"),
    "ORB": ("Orbit & the Moon", "06-orbit-and-the-moon.md"),
    "DRF": ("The Drift", "07-the-drift.md"),
    "SEE": ("The Seedship Anthesis", "08-the-seedship-anthesis.md"),
    "PRC": ("Procedural Templates", "09-procedural-templates.md"),
}

# Budgets per level type. "cell" types stream on a World Partition grid.
TYPES = {
    "Open Region": {"cell_m": 256, "loading_range_m": 768, "blockout_tris": 50000, "per": "cell", "memory_mb": 60, "draw_calls": 400, "shadow_lights": 4},
    "Planet Region": {"cell_m": 512, "loading_range_m": 1536, "blockout_tris": 40000, "per": "cell", "memory_mb": 40, "draw_calls": 300, "shadow_lights": 2},
    "Space Region": {"cell_m": 2048, "loading_range_m": 8192, "blockout_tris": 20000, "per": "cell", "memory_mb": 20, "draw_calls": 150, "shadow_lights": 1},
    "District": {"blockout_tris": 400000, "per": "level", "memory_mb": 350, "draw_calls": 2500, "shadow_lights": 12},
    "Interior": {"blockout_tris": 200000, "per": "level", "memory_mb": 400, "draw_calls": 3000, "shadow_lights": 16},
    "Hub": {"blockout_tris": 300000, "per": "level", "memory_mb": 600, "draw_calls": 4000, "shadow_lights": 24},
    "Dungeon": {"blockout_tris": 250000, "per": "level", "memory_mb": 500, "draw_calls": 3500, "shadow_lights": 20},
    "Set Piece": {"blockout_tris": 150000, "per": "level", "memory_mb": 350, "draw_calls": 2500, "shadow_lights": 16},
    "Space Arena": {"blockout_tris": 100000, "per": "level", "memory_mb": 300, "draw_calls": 2000, "shadow_lights": 8},
    "Procedural Template": {"blockout_tris": 80000, "per": "level", "memory_mb": 120, "draw_calls": 1200, "shadow_lights": 8},
    "Planet": {"per": "planet", "voxel_m": 1.0, "chunk_m": 32, "lod_rings": 8, "memory_mb": 900, "draw_calls": 3000, "shadow_lights": 4,
               "blockout_tris": 400000},
}

# Voxel-traversal planet scale (Space Engineers-style): every planet is a voxel planet
# 20-120 km in diameter. Derived values (horizon, curvature, landmark heights) are
# computed by build.py from these constants.
PLANET_STANDARD = {
    "diameter_km": (20, 120),
    "eye_height_m": 1.8,
    "atmosphere_height_frac": 0.15,     # of radius
    "gravity_falloff_exponent": 7,       # g(r) = g0 * (R_top / r)^7 above the tallest terrain
    "gravity_zero_frac": 2.0,            # gravity treated as zero beyond 2 R
    "max_elevation_frac": 0.035,         # terrain within ±3.5% of radius
    "crust_depth_frac": 0.035,           # minable voxel crust, then unminable bedrock
    "voxel_size_m": 1.0,
    "voxel_chunk_m": 32,
    "clipmap_lod_rings": 8,
    "region_max_km": 16,                 # largest flat-authored region stamped onto a planet...
    "region_max_frac_of_diameter": 0.25, # ...and never more than a quarter of the planet's diameter
    "cube_face_heightmap_px": {20: 2048, 40: 4096, 80: 8192, 120: 8192},
}

MARKER_PREFIXES = {
    "LVL_": "Level root empty (metadata)",
    "BLK_": "Blockout geometry (grey-box)",
    "TER_": "Terrain / heightfield",
    "PS_": "Player start",
    "SP_": "Enemy / NPC spawn point",
    "HS_": "Horde spawn zone (volume)",
    "TRG_": "Mission trigger volume",
    "VOL_": "Other volumes: rooms, audio, post-process, no-build, Bloom level, pressure, kill",
    "POI_": "Point of interest (open-world discovery)",
    "LM_": "Landmark",
    "CAM_": "Cinematic / set-piece camera",
    "SPL_": "Spline: roads, paths, rails, patrol routes",
    "DOOR_": "Connection between spaces (door, airlock, lift, gap)",
    "COV_": "Cover marker (low / high)",
    "LT_": "Key light reference",
    "NAV_": "Navmesh bounds / modifier volume",
    "KIT_": "Modular kit piece instance",
    "REF_": "Reference only (never exported)",
}

LEVELS = []
_counters = {}


def S(name, size, purpose, pos=None):
    """A space: (W, D, H) metres; ``pos`` = floor-centre (x, y, z) in level coordinates."""
    return {"name": name, "size": list(size), "purpose": purpose, "pos": list(pos) if pos else None}


def L(group, name, *, type, act, size, summary, missions=(), playtime="", goals=(), spaces=(), connections=(),
      encounters=(), setpieces=(), landmarks=(), mood=None, audio="", links="", build="None", kits=(), markers=(),
      map=None, key=None, pos=None, bloom="", gravity="1 g", atmosphere="Breathable", hazards="", notes="", terrain=None,
      planet=None, on_planet=None):
    if group not in GROUPS:
        raise ValueError(group)
    if type not in TYPES:
        raise ValueError(f"{name}: unknown type {type}")
    _counters[group] = _counters.get(group, 0) + 1
    LEVELS.append({
        "id": f"{group}-{_counters[group]:03d}", "group": group, "name": name, "key": key, "type": type, "act": act,
        "missions": list(missions), "size": size, "playtime": playtime, "summary": summary, "goals": list(goals),
        "spaces": list(spaces), "connections": [list(c) for c in connections], "encounters": list(encounters),
        "setpieces": list(setpieces), "landmarks": list(landmarks), "mood": mood or {}, "audio": audio, "links": links,
        "build": build, "kits": list(kits), "markers": list(markers), "map": map, "pos": pos, "bloom": bloom,
        "gravity": gravity, "atmosphere": atmosphere, "hazards": hazards, "notes": notes, "terrain": terrain,
        "planet": planet, "on_planet": on_planet,
    })


KITS = []


def K(code, name, art, use, pieces, notes=""):
    """A modular kit. Pieces: (name, (W, D, H) m, pivot, budget tris, notes)."""
    KITS.append({"code": code, "name": name, "art": art, "use": use,
                 "pieces": [{"name": p[0], "size": list(p[1]), "pivot": p[2], "tris": p[3], "notes": p[4] if len(p) > 4 else ""} for p in pieces],
                 "notes": notes})


from . import planets, kestrel, orbit_drift, seedship, procedural, kits  # noqa: E402,F401
from .metrics import GYM, METRICS, NAV_AGENTS  # noqa: E402,F401
from .travel import FLIGHT, JUMP, PULSE, STATIONS, THRESHOLDS  # noqa: E402,F401
