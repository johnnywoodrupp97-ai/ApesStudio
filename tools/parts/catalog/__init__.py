"""EXODUS PROTOCOL parts catalog — the single source of truth for every buildable part.

Edit the category modules in this package, then run ``python3 tools/parts/build.py``
to regenerate the Parts Bible (docs/parts-bible/*.md), the JSON registry and the
CSV art-production tracker.

Conventions
-----------
* Sizes are in grid cells as ``(W, H, D)`` = width (Blender Y), height (Blender Z),
  depth (Blender X, front = +X).
* Large grid (LG) cell = 2.5 m, small grid (SG) cell = 0.5 m.
* ``power`` is in kW: positive = generation, negative = draw.
* ``mass`` / ``hp`` / ``power`` / ``recipe`` may be a single value (LG, with SG derived)
  or a dict keyed by grid (``{"LG": ..., "SG": ...}``).
* Socket shorthand: ``"type@face"`` or ``"type@face*N"``; faces are
  front, back, left, right, top, bottom, center.
"""

from .standards import CATEGORIES

PARTS = []

# Derivation factors used when a small-grid value isn't given explicitly.
SG_FACTOR = {"mass": 0.05, "hp": 0.1, "power": 0.1, "recipe": 0.15}


def _per_grid(value, grids, kind):
    """Expand a scalar-or-dict stat into ``{grid: value}`` for every grid the part has."""
    if value is None:
        return {g: None for g in grids}
    if isinstance(value, dict) and set(value) <= {"LG", "SG"} and value:
        out = dict(value)
        if "LG" in out and "SG" in grids and "SG" not in out:
            out["SG"] = _derive(out["LG"], kind)
        return {g: out.get(g) for g in grids}
    out = {}
    for g in grids:
        out[g] = value if g == "LG" else _derive(value, kind)
    if "LG" not in grids:  # SG-only part given a scalar: the scalar is the SG value
        out = {g: value for g in grids}
    return out


def _derive(lg_value, kind):
    f = SG_FACTOR[kind]
    if kind == "recipe":
        return {k: max(1, round(v * f)) for k, v in lg_value.items()}
    if isinstance(lg_value, (int, float)):
        v = lg_value * f
        return round(v, 1) if abs(v) < 10 else int(round(v))
    return lg_value


def P(code, name, sub, grids, *, tier, function, art="IND", cls="M", mass=None, hp=None,
      power=0, recipe=None, unlock="", mounts="all", airtight="none", sockets=(),
      moving=(), emissive=(), vfx=(), audio=(), notes="", shape="box", variants=None,
      key=None, stages=None, stats=None):
    """Register a part. See module docstring for conventions."""
    if code not in CATEGORIES:
        raise ValueError(f"Unknown category code {code!r} for {name}")
    grids = {g: tuple(s) for g, s in grids.items()}
    PARTS.append({
        "code": code,
        "name": name,
        "key": key,
        "sub": sub,
        "grids": grids,
        "tier": tier,
        "art": art,
        "cls": cls,
        "function": function,
        "unlock": unlock,
        "mass": _per_grid(mass, grids, "mass"),
        "hp": _per_grid(hp, grids, "hp"),
        "power": _per_grid(power, grids, "power"),
        "recipe": _per_grid(recipe or {}, grids, "recipe"),
        "stats": stats or {},
        "mounts": mounts,
        "airtight": airtight,
        "sockets": list(sockets),
        "moving": list(moving),
        "emissive": list(emissive),
        "vfx": list(vfx),
        "audio": list(audio),
        "notes": notes,
        "shape": shape,
        "variants": variants or [],
        "stages": stages,
    })


def V(name, *, grids=None, mass_mult=1.0, hp_mult=1.0, recipe=None, tier=None, notes="", shape=None):
    """Declare a variant (a separate Blender asset sharing the part's function)."""
    return {"name": name, "grids": grids, "mass_mult": mass_mult, "hp_mult": hp_mult,
            "recipe": recipe, "tier": tier, "notes": notes, "shape": shape}


# Import order defines part numbering within each category.
from . import (  # noqa: E402,F401
    blocks_structure,
    blocks_systems,
    blocks_vehicles,
    blocks_life,
    blocks_combat_utility,
)
from .components import COMPONENTS, RESOURCES  # noqa: E402,F401
from .equipment import EQUIPMENT  # noqa: E402,F401
