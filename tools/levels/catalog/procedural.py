"""PRC — procedural templates: points of interest, Wonders, Earth Returns regions and player base zones."""

from . import L, S


def poi(name, size, *, summary, spaces, encounters, freq, loot, bloom="Varies", kits=("KIT-BLM",), notes="", key=None, variants=""):
    L("PRC", name, key=key, type="Procedural Template", act="II+ (open world)", size={"w": size[0], "d": size[1], "h": size[2]},
      summary=summary + (f" Variants: {variants}." if variants else ""), goals=[f"Frequency: {freq}", f"Rewards: {loot}"], spaces=spaces,
      encounters=encounters, bloom=bloom, build="Restricted (no-build inside the footprint until cleared)", kits=list(kits), notes=notes,
      markers=["PS_POI_Entry", "POI_Main", "SP_Group_01"], mood={"time": "Planet time", "palette": [("Per biome", "—")], "light": "Planet sun + practicals"})


poi("Derelict Ship", (140, 50, 30), freq="Common", loot="Components, logs, blueprint fragments",
    summary="A drifting or crashed wreck assembled from room modules (bridge, crew, cargo, engineering) around a spine.",
    spaces=[S("Spine corridor", (100, 3, 3), "Module connector", (0, 0, 0)), S("Room modules ×4–8", (12, 10, 4), "Randomized from 24 module types", (0, 8, 0))],
    encounters=["Drifters", "Bloom growths", "Traps (depressurization)"], kits=("KIT-HAU", "KIT-DIR", "KIT-BLM"), variants="Hauler, Directorate, Kestrel, pre-2071 human")
poi("Crash Site", (120, 120, 25), freq="Common", loot="Salvage, sometimes survivors",
    summary="A debris field around a broken fuselage with a survivor chance.",
    spaces=[S("Fuselage", (30, 8, 8), "Interior loot", (0, 0, 0)), S("Debris field", (120, 120, 5), "Cover", (0, 0, 0))],
    encounters=["Wildlife", "Hollows drawn by smoke"], kits=("KIT-DIR", "KIT-HAU"))
poi("Survivor Camp", (100, 80, 15), freq="Uncommon", loot="Recruits, trade, quests",
    summary="A camp built from a kit of tents, containers and barricades around a campfire; friendly, wary or hostile.",
    spaces=[S("Camp core", (40, 30, 5), "Fire, tents", (0, 0, 0)), S("Perimeter", (100, 80, 3), "Barricades", (0, 0, 0))],
    encounters=["Survivors (dialogue)", "Night raids"], kits=("KIT-TWN", "KIT-HAU"))
poi("Bloom Heart", (80, 80, 40), freq="Uncommon", loot="Bloom samples, Resonance Crystals; lowers local Bloom",
    summary="A pulsing organic nest with 3–5 root nodes; destroying it pushes back the Bloom in its radius.",
    spaces=[S("Heart", (20, 20, 25), "Core", (0, 0, 0)), S("Root nodes ×3–5", (6, 6, 5), "Must be destroyed", (25, 0, 0)), S("Growth field", (80, 80, 10), "Hollow waves", (0, 0, 0))],
    encounters=["Hollow waves", "Screamers", "Bloaters"], bloom="High", kits=("KIT-BLM",))
poi("Sower Ruin", (120, 120, 60), freq="Uncommon", loot="Glyphs, precursor components",
    summary="Grown chambers with a glyph puzzle and a precursor cache.",
    spaces=[S("Entry arch", (20, 10, 15), "Glyph lock", (0, -50, 0)), S("Puzzle hall", (40, 40, 20), "Glyph puzzle (1 of 12 types)", (0, 0, 0)), S("Cache", (12, 12, 8), "Reward", (0, 40, 0))],
    encounters=["Sower constructs (minor)", "None (contemplative)"], kits=("KIT-SOW",))
poi("Directorate Outpost", (150, 120, 25), freq="Uncommon", loot="High-tech loot, intel, blueprint fragments",
    summary="A white-gold prefab base with turrets, drones and a comms tower.",
    spaces=[S("Barracks", (30, 15, 4), "Troopers", (-30, 0, 0)), S("Comms tower", (8, 8, 30), "Intel", (40, 30, 0)), S("Vault", (10, 8, 4), "Loot", (0, -40, 0))],
    encounters=["Troopers", "Sentinel drones", "Turrets"], kits=("KIT-DIR",))
poi("Choir Shrine", (60, 60, 20), freq="Rare", loot="Choir reputation, strange rewards",
    summary="Candles, moss and a listening stone; pilgrims tend it.", spaces=[S("Shrine", (15, 15, 10), "Listening stone", (0, 0, 0))],
    encounters=["Pilgrims (dialogue)"], kits=("KIT-ICE", "KIT-SOW"))
poi("Hauler Waystation", (120, 100, 30), freq="Rare", loot="Trade, contracts, repairs",
    summary="A container-built rest stop with a landing pad, a bar and a repair bay.",
    spaces=[S("Landing pad (30 m)", (30, 30, 1), "Medium pad", (0, 0, 0)), S("Bar", (15, 10, 4), "Rumors", (30, 20, 0)), S("Repair bay", (25, 20, 10), "Services", (-30, 20, 0))],
    encounters=["None (safe)"], kits=("KIT-HAU",))
poi("Anomaly", (200, 200, 100), freq="Rare", loot="Unique one-off rewards and lore",
    summary="Hand-authored one-off events dropped into procedural space: a lone construct, a time-dilated signal, a pre-2071 human ship.",
    spaces=[S("Anomaly core", (50, 50, 50), "Authored per anomaly", (0, 0, 0))], encounters=["Per anomaly"], kits=("KIT-SOW", "KIT-HAU"))

L("PRC", "Wonders", key="wonders", type="Procedural Template", act="III+", size={"w": 5000, "d": 5000, "h": 3000},
  summary="Rare procedural phenomena discovered once per save: the Singing Ring, the Glass Forest, the Tidal Titan, the Frozen Fleet and the Mirror World.",
  goals=["Discovery, codex entries, unique views"],
  spaces=[S("The Singing Ring", (5000, 5000, 100), "Planetary ring that hums the Verdance motif when flown through", (0, 0, 2000)),
          S("Glass Forest", (1500, 1500, 60), "Silicate trees that ring like bells", (0, 0, 0)), S("Tidal Titan", (400, 150, 120), "Sleeping mountain-sized creature in a shallow sea", (0, 0, 0)),
          S("Frozen Fleet", (2000, 2000, 500), "Sower Seedlings locked in a comet", (0, 0, 0)), S("The Mirror World", (3000, 3000, 200), "Ruins matching a human city layout", (0, 0, 0))],
  encounters=["None (wonder)"], build="None within 300 m", kits=["KIT-SOW"], markers=["POI_Wonder"],
  mood={"time": "Any", "palette": [("Per wonder", "—")], "light": "Signature lighting per wonder"})

L("PRC", "Earth Returns Region", key="earth_returns_region", type="Open Region", act="II+", size={"w": 8000, "d": 8000, "h": 1500},
  summary="The template for procedural Earth regions outside Kestrel Valley on the 120 km Earth: city ruins, forests, coasts and tundra, with Bloom density rising as the story advances.",
  goals=["Rescue survivors", "Salvage", "Push back the Bloom"],
  spaces=[S("City ruins biome", (3000, 3000, 150), "Procedural blocks from KIT-TWN", (0, 0, 0)), S("Forest biome", (8000, 8000, 60), "Foliage + clearings", (0, 0, 0)),
          S("Coast biome", (8000, 2000, 40), "Beaches, cliffs, harbours", (0, -3000, 0))],
  encounters=["Hordes (by Bloom level)", "Survivor camps", "Directorate remnants"], build="Allowed", kits=["KIT-TWN", "KIT-DST", "KIT-BLM"],
  markers=["PS_Region_Entry"], on_planet={"planet": "PLN-001", "lat": 38.4, "lon": -116.9},
  mood={"time": "60-min day", "palette": [("Per biome", "—")], "light": "Earth sun"})

L("PRC", "Player Base Zones", key="player_base_zones", type="Procedural Template", act="All", size={"w": 400, "d": 400, "h": 120},
  summary="Rules for where and how players build: base sites on every planet, no-build volumes, Attraction and horde approach lanes, and how authored spaces accept player blocks.",
  goals=["At least 6 good base sites per open region", "Readable horde approach lanes"],
  spaces=[S("Base site (flat)", (50, 50, 0), "Minimum flat area", (0, 0, 0)), S("Approach lanes ×3", (10, 150, 0), "Where hordes path from", (0, 100, 0)),
          S("No-build radius", (300, 300, 120), "Around story anchors (150 m radius)", (0, 0, 0))],
  encounters=["Horde nights sized by Attraction (game bible 22 §22.5)"], build="Allowed (this is the build rulebook)", kits=["KIT-KES"],
  markers=["VOL_BaseSite", "VOL_NoBuild"], mood={"time": "—", "palette": [("—", "—")], "light": "—"})
