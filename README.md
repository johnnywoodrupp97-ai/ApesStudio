# ApesStudio

## EXODUS PROTOCOL (working title)

An **open-world, open-exploration survival game** that begins with a zombie outbreak and grows into a space-colony epic. It mixes *Space Engineers*-style physical building, *Sims*-style colony life and *No Man's Sky*-style procedural exploration, with an AAA character-driven campaign (~12-hour critical path) and a sandbox you can keep playing and expanding.

**Game Bible (Elite Edition):** [`docs/game-bible/`](docs/game-bible/README.md)

**Parts Bible (every part, with a Blender spec per asset):** [`docs/parts-bible/`](docs/parts-bible/README.md)

**Tools:** `python3 tools/parts/build.py` regenerates the Parts Bible; `blender -b -P tools/blender/exodus_parts.py -- scaffold --asset <name>` builds a starter .blend (see [chapter 20](docs/parts-bible/20-blender-toolkit.md)).
