# ApesStudio

## EXODUS PROTOCOL (working title)

An **open-world, open-exploration survival game** that begins with a zombie outbreak and grows into a space-colony epic. It mixes *Space Engineers*-style physical building, *Sims*-style colony life and *No Man's Sky*-style procedural exploration, with an AAA character-driven campaign (~12-hour critical path) and a sandbox you can keep playing and expanding.

**Game Bible (Elite Edition):** [`docs/game-bible/`](docs/game-bible/README.md)

**Parts Bible (every part, with a Blender spec per asset):** [`docs/parts-bible/`](docs/parts-bible/README.md)

**Character Bible (every character and creature, with Blender specs and rigging toolkit):** [`docs/character-bible/`](docs/character-bible/README.md)

**Level Design Bible (every level and planet, voxel planet scale, No Man's Sky-style travel, with a Blender level toolkit):** [`docs/level-bible/`](docs/level-bible/README.md)

**Built Blender assets:** `assets/parts/` and `assets/props/` (all 601 parts, props, weapons, suits and drones as validated greybox files) and `assets/levels/` (a blockout of every level and planet, the Metrics Gym and 13 modular kits).

**Tools:** `python3 tools/parts/build.py` regenerates the Parts Bible; `blender -b -P tools/blender/exodus_parts.py -- build --all` builds every part as a complete greybox (see [chapter 20](docs/parts-bible/20-blender-toolkit.md)); `python3 tools/levels/build.py` regenerates the Level Design Bible and `blender -b -P tools/blender/exodus_levels.py -- scaffold --all` builds every level blockout (see [chapter 15](docs/level-bible/15-blender-level-toolkit.md)); `python3 tools/characters/build.py` regenerates the Character Bible and `blender -b -P tools/blender/exodus_characters.py -- scaffold --character <ID>` builds rigged character files (see [chapter 12](docs/character-bible/12-blender-character-toolkit.md)).
