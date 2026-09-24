"""EXODUS PROTOCOL character catalog — single source of truth for the Character Bible.

Edit the modules in this package, then run ``python3 tools/characters/build.py`` to
regenerate docs/character-bible (chapters, characters.json and the art tracker).

Every character entry drives:
  * its story and visual-design sheet,
  * its Blender assets (base body, outfits, hair, variants, first-person arms),
  * its skeleton (template + height + proportion profile, see ../skeletons.py),
  * its budgets (from its tier) and facial shape-key set.
"""

GROUPS = {
    # code: (asset prefix, chapter title, chapter file)
    "PLY": ("CHR", "The Player Character", "02-player-character.md"),
    "CST": ("CHR", "Story Cast", "03-story-cast.md"),
    "NOT": ("NPC", "Notable Survivors", "04-notable-survivors.md"),
    "HOL": ("ENM", "Hollows & Sower Constructs", "06-hollows-and-constructs.md"),
    "FAC": ("NPC", "Faction Units", "07-faction-units.md"),
    "BOS": ("ENM", "Bosses", "08-bosses.md"),
    "CRE": ("CRE", "Creatures & Fauna", "09-creatures-and-fauna.md"),
}

TIERS = {
    "Hero": {"tris": 160000, "split": {"Head": 35000, "Hair": 40000, "Body + outfit": 85000},
             "textures": "Head 4K (BC/N/ORM/SSS + 2 wrinkle normals) · Body 4K · Outfit 2× 4K · Hair 4K · Eyes 2K · Teeth & tongue 1K",
             "facial": "hero", "influences": 8, "hair": "Hair cards (40k) + groom reference; strands for cinematics only"},
    "Main": {"tris": 110000, "split": {"Head": 30000, "Hair": 30000, "Body + outfit": 50000},
             "textures": "Head 4K (BC/N/ORM/SSS + 1 wrinkle normal) · Body 4K · Outfit 4K · Hair 2K · Eyes 1K",
             "facial": "main", "influences": 8, "hair": "Hair cards (30k)"},
    "Secondary": {"tris": 60000, "split": {"Head": 18000, "Hair": 15000, "Body + outfit": 27000},
                  "textures": "Head 2K · Body 2K (shared skin detail) · Outfit 2K · Hair 2K · shared eyes",
                  "facial": "secondary", "influences": 8, "hair": "Hair cards (15k)"},
    "Crowd": {"tris": 30000, "split": {"Head": 8000, "Hair": 6000, "Body + outfit": 16000},
              "textures": "Shared 2K head atlases (48 heads) · modular outfit pieces 1K–2K · shared hair atlases",
              "facial": "crowd", "influences": 4, "hair": "Hair cards from the shared crowd library (6k)"},
    "Enemy": {"tris": 35000, "split": {"Head": 6000, "Bloom growths": 9000, "Body": 20000},
              "textures": "Hollow base 2K (from the survivor body it was) · shared Bloom overlay atlas 2K",
              "facial": "hollow", "influences": 4, "hair": "Crowd hair cards, matted (material variant)"},
    "Elite": {"tris": 60000, "split": {"Head": 8000, "Bloom growths": 17000, "Body": 35000},
              "textures": "Unique 4K body set · shared Bloom overlay atlas 2K · 2K plating/growth set",
              "facial": "hollow", "influences": 4, "hair": "None or matted cards"},
    "Boss": {"tris": 180000, "split": {"Head": 35000, "Armor / growths": 70000, "Body": 75000},
             "textures": "Unique 4K sets ×4 (body, armor/growth, head, FX masks)",
             "facial": "hero", "influences": 8, "hair": "As base character"},
    "Creature-L": {"tris": 80000, "split": {"Head": 15000, "Body": 65000},
                   "textures": "Body 4K · head 2K · shared Bloom overlay 2K (for Bloom variants)",
                   "facial": "creature", "influences": 4, "hair": "Fur/fibre shells or cards where noted"},
    "Creature-S": {"tris": 15000, "split": {"Head": 3000, "Body": 12000},
                   "textures": "Body 2K (atlased per kit)", "facial": "creature", "influences": 4, "hair": "Fur cards where noted"},
    "Hologram": {"tris": 20000, "split": {"Form": 20000},
                 "textures": "Emissive line atlas 1K · noise mask 512", "facial": "none", "influences": 4, "hair": "None"},
}
LOD_RATIOS = [1.0, 0.5, 0.2, 0.06]

CHARACTERS = []
_counters = {}


def O(key, name, acts, desc, pieces=(), shared=None):
    """An outfit. ``shared`` = name of a shared suit asset (e.g. SK_SUIT_EVASuit) worn instead of a unique mesh."""
    return {"key": key, "name": name, "acts": acts, "desc": desc, "pieces": list(pieces), "shared": shared}


def CH(group, name, *, tier, skeleton, title="", key=None, age="", pronouns="", role="", appears="",
       story=None, voice="", visual=None, outfits=(), hair=(), variants=(), extra_shapes=(), extra_bones=(),
       sockets=(), infection=True, facial_capture=False, mocap="", cloth=(), notes="", gameplay=None,
       customization=None, arms_1p=False, art="IND"):
    if group not in GROUPS:
        raise ValueError(f"Unknown group {group}")
    if tier not in TIERS:
        raise ValueError(f"Unknown tier {tier} for {name}")
    _counters[group] = _counters.get(group, 0) + 1
    CHARACTERS.append({
        "id": f"{group}-{_counters[group]:03d}", "group": group, "name": name, "title": title, "key": key,
        "tier": tier, "skeleton": skeleton, "age": age, "pronouns": pronouns, "role": role, "appears": appears,
        "story": story or {}, "voice": voice, "visual": visual or {}, "outfits": list(outfits), "hair": list(hair),
        "variants": list(variants), "extra_shapes": list(extra_shapes), "extra_bones": list(extra_bones),
        "sockets": list(sockets), "infection": infection, "facial_capture": facial_capture, "mocap": mocap,
        "cloth": list(cloth), "notes": notes, "gameplay": gameplay or {}, "customization": customization,
        "arms_1p": arms_1p, "art": art,
    })


def H(height, profile="adult_average"):
    return {"template": "humanoid", "height": height, "profile": profile}


from . import cast, survivors, enemies, creatures  # noqa: E402,F401
from .survivors import MORE_SURVIVORS, SURVIVOR_KIT  # noqa: E402,F401
