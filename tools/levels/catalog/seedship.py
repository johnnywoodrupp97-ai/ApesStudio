"""SEE — the Seedship Anthesis (Act IV)."""

from . import L, S

LIVING = {"time": "Timeless (inside a living ship)", "palette": [("Deep violet", "#3A2A5C"), ("Living green", "#7FD06B"), ("Pearl", "#E9E4DA"), ("Glyph teal", "#2EE6D6")],
          "light": "Bioluminescence that pulses with the ship's 'breath'"}

L("SEE", "Anthesis Approach", key="anthesis_approach", type="Space Arena", act="IV", missions=["M4.01"], size={"w": 60000, "d": 60000, "h": 40000}, playtime="25 min",
  summary="Ship combat against the Seedship's defensive organisms, then the breach. Anthesis is a 30 km living vessel; its petal-sails are a 1,000 km VFX.",
  goals=["Break through the defenses", "Breach the hull with a boarding craft"],
  spaces=[S("Seedship hull", (30000, 30000, 12000), "Living exterior (hero megastructure)", (0, 0, 0)), S("Defense layer", (50000, 50000, 30000), "Spore-swarms, tendril batteries", (0, 0, 0)),
          S("Breach site", (300, 300, 200), "Where the boarding drill enters", (0, -15000, 0))],
  encounters=["Spore-swarms", "Tendril batteries", "Directorate stragglers"], setpieces=["Petal-sails unfolding"], landmarks=["Anthesis itself"],
  mood=LIVING, audio="Low organ-like groans; the five-note motif in the ship's calls.", build="Boarding-craft modifications only", gravity="0 g", atmosphere="Vacuum",
  kits=["KIT-SEE"], markers=["PS_M4_01", "TRG_M4_01_Breach", "TRG_M4_01_PointOfNoReturn", "SPL_Approach_M4_01"], notes="The point of no return is marked with a clear prompt before this level loads.")

L("SEE", "The Living Halls", key="living_halls", type="Hub", act="IV", missions=["M4.02 (hub)"], size={"w": 800, "d": 800, "h": 300}, playtime="10 min (between gardens)",
  summary="The breathing hub between the four Memory Gardens: root corridors, pulsing chambers, and four petal-gates that open one garden each.",
  goals=["Choose a garden", "Regroup (squad of two companions)"],
  spaces=[S("Breach chamber", (60, 60, 40), "Entry wound", (0, -350, 0)), S("Heart hall", (200, 200, 150), "Hub with four petal-gates", (0, 0, 0)),
          S("Petal-gate: Veyra Before", (30, 10, 40), "Garden 1", (-150, 0, 0)), S("Petal-gate: Drowned Choir", (30, 10, 40), "Garden 2", (0, 150, 0)),
          S("Petal-gate: First Garden", (30, 10, 40), "Garden 3", (150, 0, 0)), S("Petal-gate: Permian Earth", (30, 10, 40), "Garden 4", (0, -150, 0)),
          S("Loom stair", (40, 40, 150), "Opens after all gardens", (0, 0, 150))],
  connections=[("Breach chamber", "Heart hall", "root corridor"), ("Heart hall", "Loom stair", "petal-gate")],
  encounters=["Sower Wardens (patrols)", "Elite Hollows"], landmarks=["The Heart hall's central light column"], mood=LIVING,
  audio="Heartbeat bed that speeds up as gardens are completed.", build="None", kits=["KIT-SEE", "KIT-SOW"], markers=["PS_M4_02_Hub"])

L("SEE", "Memory Garden 1 — Veyra, Before", key="garden_veyra", type="Dungeon", act="IV", missions=["M4.02"], size={"w": 1200, "d": 1200, "h": 400}, playtime="15 min",
  summary="Veyra-4 before the gardening: Tessari herds in their millions. It heals or haunts the player depending on veyra_healed.",
  goals=["Cross the preserved plains", "Find the memory core"],
  spaces=[S("Preserved plains", (1000, 1000, 50), "Tessari herds (VAT crowds)", (0, 0, 0)), S("Memory core", (60, 60, 60), "Exit node", (400, 400, 0))],
  encounters=["Wardens", "(If Veyra was abandoned) Bloomed Tessari"], landmarks=["A giant Tessari skull-arch"], mood=LIVING, audio="Tessari calls, wind", kits=["KIT-JUN", "KIT-SEE"],
  markers=["PS_Garden1", "POI_MemoryCore1"])

L("SEE", "Memory Garden 2 — The Drowned Choir", key="garden_drowned_choir", type="Dungeon", act="IV", missions=["M4.02"], size={"w": 1200, "d": 1200, "h": 600}, playtime="15 min",
  summary="An ocean world whose whale-like people sang. The Sowers harvested them before they understood. The reason the Sowers stopped.",
  goals=["Descend through the flooded song-halls (swimming)", "Hear the last song"],
  spaces=[S("Surface reefs", (800, 800, 40), "Entry", (0, 0, 0)), S("Song-halls (flooded)", (600, 600, 400), "Swimming traversal", (0, 0, -400)), S("The last song", (100, 100, 100), "Singer encounter (non-hostile)", (0, 0, -550))],
  encounters=["Drowned Wardens", "Singers (non-hostile)"], setpieces=["The last song"], landmarks=["Singers' glowing song-patterns"], mood=LIVING,
  audio="The Drowned Choir song (key musical motif).", atmosphere="Water (suits required)", kits=["KIT-SEE"], markers=["PS_Garden2", "POI_MemoryCore2"])

L("SEE", "Memory Garden 3 — The First Garden", key="garden_first", type="Dungeon", act="IV", missions=["M4.02"], size={"w": 1000, "d": 1000, "h": 500}, playtime="15 min",
  summary="The Sowers' own homeworld and their final recordings: they left because some gardens held minds, and they were ashamed.",
  goals=["Walk the Sower city", "Witness the Sower Echoes' last recording"],
  spaces=[S("Shell city", (800, 800, 300), "Grown towers", (0, 0, 0)), S("Recording hall", (80, 80, 40), "Sower Echoes bow", (0, 300, 0))],
  encounters=["Few (contemplative)"], setpieces=["The Sowers' confession"], landmarks=["A tower of shell and filament"], mood=LIVING, audio="Choral breath, silence.",
  kits=["KIT-SOW", "KIT-SEE"], markers=["PS_Garden3", "POI_MemoryCore3"])

L("SEE", "Memory Garden 4 — Permian Earth", key="garden_permian", type="Dungeon", act="IV", missions=["M4.02"], size={"w": 1500, "d": 1500, "h": 400}, playtime="15 min",
  summary="Earth 252 million years ago, during the Great Dying: a dying Pangaea under a burning sky, Bloom-covered gorgonopsids, and Lily hearing 'sorry'.",
  goals=["Cross the dying Pangaea", "Lily's moment at the fossil (C15)"],
  spaces=[S("Burning plains", (1200, 1200, 60), "Ash, lava rivers, Bloom", (0, 0, 0)), S("Fossil-to-be", (40, 40, 20), "Lily's moment", (500, 500, 0))],
  encounters=["Bloomed gorgonopsids", "Dicynodont herds (non-hostile)", "Wardens"], setpieces=["Sorry (C15)"], landmarks=["A volcanic horizon"],
  mood={"time": "Burning sky", "palette": [("Ash grey", "#6E6A66"), ("Lava orange", "#FF5A1F"), ("Bloom green", "#7FD06B")], "light": "Red sun through ash"},
  audio="Rumbling ground, Bloom clicks, gorgonopsid roars.", kits=["KIT-SEE", "KIT-BLM"], markers=["PS_Garden4", "CAM_C15_Sorry"])

L("SEE", "The Living Bridges", key="living_bridges", type="Set Piece", act="IV", missions=["M4.03"], size={"w": 400, "d": 600, "h": 300}, playtime="20 min",
  summary="Root-bridges over a 300 m bioluminescent chasm: where Ada holds the breach, or fights her sibling in the Seraph exo-frame.",
  goals=["Hold the breach with Ada (defected)", "Or duel Ada (loyal) and talk her down"],
  spaces=[S("Breach door", (20, 10, 20), "Ada's last stand", (0, -250, 0)), S("Bridge network", (300, 500, 20), "Duel arena, three tiers", (0, 0, 0)), S("Chasm", (400, 600, 300), "Kill volume below", (0, 0, -300))],
  encounters=["Crane's Ascendant troops", "Ada — Seraph exo-frame (boss)"], setpieces=["Blood (C16)"], landmarks=["The Loom's glow ahead"], mood=LIVING,
  audio="'Sunday' theme on kora breaking through the battle.", kits=["KIT-SEE"], markers=["PS_M4_03", "SP_AdaExoframe", "CAM_C16_Blood", "VOL_Kill_Chasm"])

L("SEE", "The Loom Chamber", key="loom_chamber", type="Set Piece", act="IV", missions=["M4.04 (phases 1–2)", "M4.05"], size={"w": 200, "d": 200, "h": 120}, playtime="25 min",
  summary="A tiered organic amphitheatre around the Loom. Crane fights here in armor, then as the Graft while the arena grows; later, the final choice is made here.",
  goals=["Defeat or talk down Crane", "Choose the Instruction and the Weaver"],
  spaces=[S("Tiers", (180, 180, 40), "Cover, pulsing vents", (0, 0, 0)), S("Loom", (40, 40, 100), "Centre", (0, 0, 0)), S("Growth zones", (200, 200, 60), "Arena changes shape in phase 2", (0, 0, 0))],
  encounters=["Crane — The Director", "Crane — The Graft", "Drones and wall-Hollows"], setpieces=["The Weaver (C17)"], landmarks=["The Loom"], mood=LIVING,
  audio="Crane's quartet theme inverted; the Loom's chorus.", kits=["KIT-SEE", "KIT-SOW"], markers=["PS_M4_04", "SP_CraneDirector", "CAM_C17_Weaver", "TRG_M4_05_Choice"])

L("SEE", "Bonsai Mind-Space", key="bonsai_mind_space", type="Set Piece", act="IV", missions=["M4.04 (phase 3)"], size={"w": 600, "d": 600, "h": 500}, playtime="10 min",
  summary="Inside the Loom: a colossal bonsai whose branches are platforms. Each branch Crane cuts darkens a city on the Earth below.",
  goals=["Race along the branches", "Protect the branches that hold cities", "Talk Crane down (if possible)"],
  spaces=[S("Trunk", (80, 80, 400), "Central climb", (0, 0, 0)), S("Branch platforms ×12", (300, 30, 20), "Arena paths", (0, 0, 250)), S("Earth below", (600, 600, 1), "Cities lit on a globe", (0, 0, -100))],
  encounters=["Crane — The Bonsai"], setpieces=["City lights going dark", "Talk-down"], landmarks=["The trunk"],
  mood={"time": "Dreamlike", "palette": [("Silver", "#C0C0C0"), ("Juniper green", "#4E6B3A"), ("City gold", "#FFD166")], "light": "Moonlit silver, city lights below"},
  audio="Snip of shears as a rhythm; distant cities humming.", gravity="Dream gravity (0.6 g, no fall damage)", kits=["KIT-SEE"], markers=["PS_M4_04_Bonsai", "SP_CraneBonsai"])

L("SEE", "The Last Sunday Dinner", key="last_sunday_dinner", type="Set Piece", act="Epilogue", missions=["M4.06"], size={"w": 30, "d": 20, "h": 6}, playtime="8 min",
  summary="The final scene, staged in the player's own home (station, ship or base): a long table, the survivors, bad jollof, an empty chair for the Weaver.",
  goals=["Sit down", "'So… what do we build next?'"],
  spaces=[S("Dining space", (12, 8, 3), "Long Dining Table (parts bible COL-008) in the player's mess hall", (0, 0, 0))],
  setpieces=["Sunday (C18)"], landmarks=["The table"], mood={"time": "Evening", "palette": [("Lamp amber", "#FFB866"), ("Table walnut", "#6B4A2F")], "light": "Warm practical lamps"},
  audio="'Sunday' theme; laughter; cutlery.", build="(Player's own base)", kits=["KIT-HAV", "KIT-KES"], markers=["PS_M4_06", "CAM_C18_Sunday"],
  notes="Procedurally staged: finds the player's largest mess hall with a Long Dining Table; falls back to a hand-built dining room on the ship.")
