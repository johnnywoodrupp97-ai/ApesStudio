"""ORB — Orbit & the Moon, DRF — the Drift anchors."""

from . import L, S

SPACE = {"time": "Orbital day/night every 40 min", "palette": [("Space black", "#05070B"), ("Earth blue", "#3D7CC9"), ("Sun white", "#FFF8E7"), ("Habitat amber", "#FFB866")],
         "light": "One hard sun, Earth-shine fill, no ambient in vacuum"}

# ---------------------------------------------------------------------------
# ORB
# ---------------------------------------------------------------------------
L("ORB", "Low Earth Orbit", key="low_earth_orbit", type="Space Region", act="II+", size={"w": 200000, "d": 200000, "h": 100000},
  summary="The debris belt around the 120 km Earth: dead satellites, a wrecked station ring and Haven-9 at 25 km altitude. Earth fills half the sky.",
  goals=["Salvage satellites and wrecks", "Reach Haven-9", "Re-enter anywhere on Earth"],
  spaces=[S("Haven-9 orbit", (2000, 2000, 2000), "The colony's first home", (0, 0, 85000)), S("Debris belt", (200000, 200000, 10000), "Salvage field at 20–35 km altitude", (0, 0, 87000)),
          S("Dead station ring", (1200, 1200, 200), "Big salvage POI", (40000, 20000, 90000))],
  encounters=["Drifters in wrecks", "Directorate patrols (Act II)"], landmarks=["Earth and the Bloom glyph", "The Moon"],
  mood=SPACE, audio="Silence outside; suit and hull sounds only.", build="Allowed", gravity="0 g (above 20 km: Earth's gravity well falls off)", atmosphere="Vacuum",
  hazards="Micrometeorites, solar flares", kits=["KIT-HAV"], markers=["PS_Orbit", "POI_StationRing"],
  on_planet={"planet": "PLN-001", "lat": 0.0, "lon": 0.0}, notes="Level origin is Earth's centre (Earth's surface at 60 km). Orbital space streams in 2 km cells. Earth's gravity at 25 km altitude is ~9% of surface gravity (falloff exponent 7).")

L("ORB", "Haven-9 Station", key="haven_9", type="Hub", act="II (and the colony's home until Act III)", missions=["M2.01", "M2.02", "M2.03", "M2.05", "M2.06"],
  size={"w": 120, "d": 80, "h": 30}, playtime="Recurring (colony hub)",
  summary="A derelict 12-module research station restored into the colony's first real home. Every module is player-restorable and player-extendable.",
  goals=["Dock (M2.01)", "Restore power, O₂, pressure and heat (M2.02)", "Build the colony (M2.03)", "Survive Patient Zero (M2.05)"],
  map="""
            [Solar wing]                      [Solar wing]
                 │                                 │
   [Docking]──[Node A]──[Hab 1]──[Hab 2]──[Node B]──[Lab]──[Medbay]
                 │                          │
             [Hydroponics]              [Mess]──[Observation]
                 │                          │
             [Engineering]──[Storage]──[Airlock bay]""",
  spaces=[S("Docking module", (8, 8, 5), "Where the Wren docks", (-50, 0, 0)), S("Node A", (6, 6, 6), "Junction", (-38, 0, 0)), S("Hab 1", (12, 5, 5), "Quarters", (-25, 0, 0)),
          S("Hab 2", (12, 5, 5), "Quarters", (-10, 0, 0)), S("Node B", (6, 6, 6), "Junction", (3, 0, 0)), S("Lab", (12, 5, 5), "Mara's lab later", (16, 0, 0)),
          S("Medbay", (10, 5, 5), "Quarantine-capable", (29, 0, 0)), S("Hydroponics", (12, 5, 5), "Crops (M2.03)", (-38, -12, 0)),
          S("Engineering", (12, 6, 5), "Power and life support", (-38, -24, 0)), S("Storage", (12, 5, 5), "Cargo", (-24, -24, 0)),
          S("Airlock bay", (10, 6, 5), "EVA access", (-10, -24, 0)), S("Mess", (12, 6, 5), "Sunday dinners", (3, -12, 0)),
          S("Observation", (10, 8, 6), "Earth-view window (Walt's Window)", (16, -12, 0))],
  connections=[("Docking module", "Node A", "hatch"), ("Node A", "Hab 1", "hatch"), ("Hab 1", "Hab 2", "hatch"), ("Hab 2", "Node B", "hatch"), ("Node B", "Lab", "hatch"),
               ("Lab", "Medbay", "hatch"), ("Node A", "Hydroponics", "hatch"), ("Hydroponics", "Engineering", "hatch"), ("Engineering", "Storage", "hatch"),
               ("Storage", "Airlock bay", "hatch"), ("Node B", "Mess", "hatch"), ("Mess", "Observation", "hatch"), ("Mess", "Airlock bay", "hatch")],
  encounters=["2 Drifters (M2.01)", "Patient Zero outbreak (M2.05, systemic)", "Directorate boarding (only if the colony stays for The Taking)"],
  setpieces=["First sight of Haven-9 (C06)", "Restoring the lights module by module", "Crane's broadcast on every screen (C07)"],
  landmarks=["The Observation window with Earth"], mood=SPACE, audio="Station hum that changes as systems come back; silence when power fails.",
  build="Allowed (extend with player modules)", gravity="0 g (spin ring optional via Habitat Ring Bearing)", atmosphere="Pressurized once restored",
  kits=["KIT-HAV"], markers=["PS_M2_01_Dock", "VOL_DockingBay_Main", "SPL_Approach_M2_01", "TRG_M2_02_Power", "TRG_M2_02_O2", "CAM_C06_Haven", "VOL_Pressure_AllModules"],
  on_planet={"planet": "PLN-001", "lat": 0.0, "lon": -110.0}, notes="Every module is a 5 m-diameter pressurized cylinder from KIT-HAV, so the air/room graph matches the building system.")

L("ORB", "Lunar Near Side", key="lunar_near_side", type="Planet Region", act="II", missions=["M2.04"], size={"w": 10000, "d": 10000, "h": 1200},
  summary="The playable 10 × 10 km region around Tycho on the 40 km Moon: crater rims, maria, dust storms and Earthrise. The rest of the Moon is procedural.",
  goals=["Land", "Reach Tycho", "Mine titanium and He-3"],
  spaces=[S("Tycho crater", (5000, 5000, 800), "Outpost on the crater floor", (0, 0, -300)), S("Landing flats", (1500, 1500, 0), "Safe landing zone", (-3500, -3200, 0)),
          S("Ice crater cache", (800, 800, 300), "Water ice", (3800, 3800, -200))],
  encounters=["Miner Hollows", "Burrowers", "Dust storms"], landmarks=["Earth in the sky (fixed)", "Tycho rim peaks (500 m)"],
  mood={"time": "Long lunar day/night (120 min)", "palette": [("Regolith grey", "#8C8C8C"), ("Earthshine blue", "#6FA8DC")], "light": "Hard sun, black shadows, Earthshine fill"},
  audio="Suit-only sound; thumps through the ground before Burrowers.", build="Allowed", gravity="0.16 g", atmosphere="Vacuum",
  kits=["KIT-MIN", "KIT-HAV"], markers=["PS_M2_04_Landing", "LM_TychoRim", "VOL_LandingZone_Flats"], on_planet={"planet": "PLN-002", "lat": -43.3, "lon": -11.2},
  notes="Capped at 10 km (a quarter of the Moon's 40 km diameter): the 20 km-radius surface still drops ~625 m at the region's edges, so the stamp's curvature correction is large. Keep gameplay-critical geometry within 3 km of the centre.")

L("ORB", "Tycho Outpost", key="tycho_outpost", type="Interior", act="II", missions=["M2.04"], size={"w": 120, "d": 90, "h": 25}, playtime="25 min",
  summary="A three-deck lunar mining outpost overrun by infected miners in EVA suits. Home of the He-3 core and the Styx telemetry archive.",
  goals=["Restore partial power", "Recover the He-3 core (heavy: winch it)", "Recover the Styx archive"],
  spaces=[S("Surface domes", (60, 40, 10), "Airlock, garage", (0, 0, 0)), S("Deck 1 habitation", (80, 30, 4), "Bunks, mess", (0, 10, -6)),
          S("Deck 2 processing", (90, 40, 6), "Refinery lines", (0, 0, -14)), S("Deck 3 reactor & archive", (50, 40, 6), "He-3 core, archive vault", (0, -10, -22))],
  connections=[("Surface domes", "Deck 1 habitation", "airlock"), ("Deck 1 habitation", "Deck 2 processing", "lift"), ("Deck 2 processing", "Deck 3 reactor & archive", "stairs")],
  encounters=["Infected miners (low-G Shamblers)", "Burrowers under the garage"], setpieces=["Winching the He-3 core onto the lander"],
  landmarks=["Outpost beacon tower"], mood={"time": "Lunar night", "palette": [("Hi-vis orange", "#FF7A00"), ("Regolith", "#8C8C8C")], "light": "Failing strip lights"},
  audio="Muffled low-G combat, creaking decks.", gravity="0.16 g", atmosphere="Partial pressure (breaches)", kits=["KIT-MIN", "KIT-HAV", "KIT-BLM"],
  markers=["PS_M2_04_Tycho", "POI_StyxArchive", "POI_He3Core"], on_planet={"planet": "PLN-002", "lat": -43.3, "lon": -11.2}, notes="Flow: game bible 18 §18.5.")

L("ORB", "Styx Wreck", key="styx_wreck", type="Dungeon", act="II", missions=["M2.07"], size={"w": 2200, "d": 900, "h": 900}, playtime="30 min",
  summary="The hollow Sower seed pod, 1,500 km beyond Earth: ribbed corridors that breathe, glyph puzzles, a three-way fight and the Jump Core at its heart.",
  goals=["Solve the glyph locks", "Survive the three-way fight", "Activate the Jump Core"],
  spaces=[S("Drill wound (entry)", (40, 40, 40), "Where Persephone drilled in 2068", (-1000, 0, 0)), S("Rib corridors", (1200, 30, 30), "Breathing organic tunnels", (-300, 0, 0)),
          S("Glyph chambers ×3", (60, 60, 40), "Puzzle rooms", (300, 150, 0)), S("Heart chamber", (200, 200, 200), "Jump Core, the star map (C08)", (800, 0, 0))],
  connections=[("Drill wound (entry)", "Rib corridors", "open"), ("Rib corridors", "Glyph chambers ×3", "glyph door"), ("Glyph chambers ×3", "Heart chamber", "glyph door")],
  encounters=["Hollow guardians", "Directorate strike team (Ada)"], setpieces=["Ada face to face in zero-G", "The star map blooms (C08)"],
  landmarks=["Teal glyph light down the corridors"], mood={"time": "Timeless", "palette": [("Shell pearl", "#E9E4DA"), ("Glyph teal", "#2EE6D6")], "light": "Bioluminescent glyphs"},
  audio="Slow breathing, choral hum, the five-note motif.", gravity="0.05 g", atmosphere="Vacuum", kits=["KIT-SOW"], build="None (story)",
  markers=["PS_M2_07", "SP_Ada", "CAM_C08_Map", "TRG_M2_07_JumpCore"])

# ---------------------------------------------------------------------------
# DRF
# ---------------------------------------------------------------------------
L("DRF", "Tortuga Drift", key="tortuga_drift", type="Hub", act="III", missions=["M3.02"], size={"w": 1500, "d": 1500, "h": 600}, playtime="Recurring (trade hub)",
  summary="The Free Hauler ship-city inside a hollowed 6 km asteroid: docks, markets, contracts, bars and the Hauler council.",
  goals=["Trade", "Contracts", "Recruit crew", "Meet Oye"],
  spaces=[S("Dock ring", (600, 600, 80), "Ship berths (lander to medium)", (0, 0, 250)), S("Market cavern", (400, 300, 120), "Stalls in container stacks", (0, 0, 0)),
          S("Contracts hall", (60, 40, 15), "Job board", (150, 100, 0)), S("The Rusty Airlock (bar)", (30, 20, 8), "Sunny Kapoor", (-120, 80, 0)),
          S("Oye's berth", (120, 60, 40), "Dust Queen's sister ship", (250, -200, 250))],
  encounters=["None by default (safe hub)", "Brawls (optional)"], landmarks=["Giant spinning Hauler sign", "Container towers"],
  mood={"time": "Artificial day", "palette": [("Cargo orange", "#E2711D"), ("Container blue", "#1E4E79"), ("Neon pink", "#FF4FD8")], "light": "Neon, work lights, rock caverns"},
  audio="Market walla, clanging, bar music.", build="None (city)", gravity="0.3 g (spin)", kits=["KIT-HAU"], markers=["PS_Tortuga_Dock", "VOL_DockingBay_Ring", "POI_ContractsBoard"])

L("DRF", "The Dust Queen", key="dust_queen", type="Dungeon", act="III", missions=["M3.02 (Oye's favor)"], size={"w": 180, "d": 60, "h": 40}, playtime="20 min",
  summary="Oye's lost ship: a Hauler freighter overgrown by Bloom, adrift in a debris field. Recover the black box.",
  goals=["Recover the flight recorder", "Learn how Oye lost his crew"],
  spaces=[S("Cargo holds", (100, 40, 30), "Bloom-choked containers", (0, 0, 0)), S("Crew deck", (60, 20, 4), "Personal effects", (40, 0, 15)), S("Bridge", (20, 15, 5), "Flight recorder", (80, 0, 18))],
  encounters=["Drifters", "Bloom growth hazards", "Hive Mite swarm"], landmarks=["Bloom glow through hull breaches"],
  mood={"time": "Timeless", "palette": [("Cargo orange", "#E2711D"), ("Bloom green", "#7FD06B")], "light": "Flashlight, Bloom glow"},
  audio="Creaking hull, Hauler music box still playing.", gravity="0 g", atmosphere="Vacuum (pockets)", kits=["KIT-HAU", "KIT-BLM"], markers=["PS_DustQueen", "POI_FlightRecorder"])

L("DRF", "Veyra-4 Jungle Region", key="veyra_region", type="Planet Region", act="III", missions=["M3.03"], size={"w": 16000, "d": 16000, "h": 2500},
  summary="The playable region around the Garden Engine on the 100 km Veyra-4: violet jungle, purple sea coast, Tessari plains and Bloom forest.",
  goals=["Reach the Garden Engine", "Save (or abandon) the Tessari"],
  spaces=[S("Landing coast", (3000, 2000, 50), "Purple sea beaches", (-5000, -5000, 0)), S("Tessari plains", (5000, 4000, 30), "Herds", (-1000, 3000, 0)),
          S("Bloom forest", (6000, 6000, 80), "Stalkers, Hive Mites", (3000, -2000, 0)), S("Garden Engine base", (1500, 1500, 2000), "The spire (DRF-004)", (4000, 3000, 0))],
  encounters=["Stalkers", "Hive Mite swarms", "Bloomed Tessari"], landmarks=["Garden Engine spire (2 km)"],
  mood={"time": "Veyra day (80 min)", "palette": [("Violet foliage", "#6A4C93"), ("Purple sea", "#4B2E83"), ("Gold light", "#F2C14E")], "light": "Humid golden sun, bioluminescent nights"},
  audio="Dense jungle bed, Tessari calls, the Engine's hum.", build="Allowed", gravity="0.9 g", kits=["KIT-JUN", "KIT-SOW", "KIT-BLM"],
  markers=["PS_M3_03_Landing", "LM_GardenEngine", "VOL_LandingZone_Coast"], on_planet={"planet": "PLN-003", "lat": 4.0, "lon": 22.0})

L("DRF", "The Garden Engine", key="garden_engine", type="Dungeon", act="III", missions=["M3.03"], size={"w": 400, "d": 400, "h": 2000}, playtime="35 min",
  summary="The 2 km Sower spire terraforming Veyra-4: a vertical climb through grown chambers to the vision at its core.",
  goals=["Climb the spire", "Touch the Engine (vision C10)", "Shut it down or take the Key"],
  spaces=[S("Root halls", (300, 300, 60), "Entry among Bloom roots", (0, 0, 0)), S("Spiral ascent", (120, 120, 1600), "Organic ramps and lifts", (0, 0, 60)),
          S("Seed galleries", (200, 200, 80), "Where the Bloom is grown", (0, 0, 900)), S("Core", (80, 80, 80), "The vision and the choice", (0, 0, 1900))],
  encounters=["Stalkers", "Sower constructs (minor)", "Bloom defenses"], setpieces=["The Gardener's Memory (C10)"], landmarks=["Glowing core visible up the shaft"],
  mood={"time": "Timeless", "palette": [("Shell pearl", "#E9E4DA"), ("Bloom green", "#7FD06B"), ("Glyph teal", "#2EE6D6")], "light": "Bioluminescence"},
  audio="Rising choral hum as you climb.", gravity="0.9 g", kits=["KIT-SOW", "KIT-BLM"], build="None (story)", markers=["PS_M3_03_Engine", "CAM_C10_Memory", "TRG_M3_03_Choice"],
  on_planet={"planet": "PLN-003", "lat": 4.0, "lon": 22.0})

L("DRF", "Cathedral of the Hum", key="cathedral_of_the_hum", type="Hub", act="III", missions=["M3.04"], size={"w": 300, "d": 700, "h": 80}, playtime="55 min",
  summary="The Choir's candle-lit sanctuary over a Sower archive on Hollowmere. Social stealth among pilgrims, tea with Mother Sable, the archive below.",
  goals=["Walk among the Choir unarmed", "Meet Sable", "The archive (C11)"],
  spaces=[S("Approach road", (30, 320, 0), "Blizzard walk with candle posts", (0, -190, 0)), S("Nave", (80, 40, 40), "Pilgrims in prayer", (0, 0, 0)),
          S("Sable's quarters", (15, 12, 5), "Tea scene", (40, 30, 0)), S("Ice stair", (20, 20, 60), "Down to the archive", (-40, 0, -60)),
          S("Sower archive", (100, 100, 30), "Earth's glyph (C11)", (-40, 0, -90))],
  encounters=["Choir Pilgrims and Wardens (hostile only if provoked)", "Mimics in the ice caves"], setpieces=["Sung Before (C11)"],
  landmarks=["Candle-lit spires", "The Hum (audio landmark in blizzards)"], mood={"time": "Perpetual blizzard dusk", "palette": [("Ice blue", "#BFD7EA"), ("Candle amber", "#FFB866"), ("Moss", "#5B7F3A")], "light": "Candles, aurora"},
  audio="Choir hum (diegetic), wind, ice cracking.", gravity="0.7 g", atmosphere="Thin, freezing (heated interior)", kits=["KIT-ICE", "KIT-SOW"],
  markers=["PS_M3_04_Approach", "SP_Sable", "CAM_C11_Archive"], on_planet={"planet": "PLN-004", "lat": 61.0, "lon": -8.0})

L("DRF", "Ark Meridian", key="ark_meridian", type="Dungeon", act="III", missions=["M3.07"], size={"w": 600, "d": 300, "h": 120}, playtime="40 min",
  summary="The Directorate flagship-station over the gas giant Meridian. A heist in three phases: get aboard, reach the labs, get out.",
  goals=["Board (loud or quiet)", "Free Lily and the Null carriers", "Take the third Key", "Decide the standoff"],
  map="""
  [HANGAR DECK]──(loud)──►[SECURITY DECK]──►[EDEN ROOM]──►[LABS: Null carriers, Lily]──►[STANDOFF]
       ▲                        ▲                                        │
  (quiet: cargo run)    (quiet: maintenance crawlspaces)                 ▼
                                                            [Escape: Ada's shuttle / by force]""",
  spaces=[S("Hangar deck", (200, 100, 40), "Loud approach entry", (-200, 0, 0)), S("Maintenance crawlspaces", (300, 4, 2), "Quiet route", (0, 60, 20)),
          S("Security deck", (150, 80, 8), "Checkpoints, cameras", (0, 0, 40)), S("Eden Room", (60, 60, 30), "Holo archive: the Great Dying (C13)", (100, 0, 50)),
          S("Labs", (120, 60, 6), "Null-carrier pods", (200, 0, 60)), S("Director's office", (20, 15, 5), "Bonsai, broadcast desk", (250, 40, 80))],
  connections=[("Hangar deck", "Security deck", "lift"), ("Hangar deck", "Maintenance crawlspaces", "vent"), ("Maintenance crawlspaces", "Labs", "vent"),
               ("Security deck", "Eden Room", "door"), ("Eden Room", "Labs", "door"), ("Labs", "Director's office", "lift")],
  encounters=["30–60 Directorate troops by approach", "Enforcer squad", "Drone swarms"], setpieces=["The Great Dying (C13)", "Idris/Ada standoff"],
  landmarks=["Meridian's storms through every window"], mood={"time": "Station day", "palette": [("Ceramic white", "#F4F6F8"), ("Gold", "#C9A227"), ("Storm amber", "#D98E04")], "light": "Sterile white, gas-giant amber"},
  audio="Directorate PA, hum of perfection, alarms.", build="None (story)", gravity="1 g (artificial)", kits=["KIT-DIR"],
  markers=["PS_M3_07_Loud", "PS_M3_07_Quiet", "VOL_NoFly_Interior", "CAM_C13_GreatDying", "TRG_M3_07_Standoff"], notes="Flow: game bible 18 §18.7.")

L("DRF", "Convergence Gate", key="convergence_gate", type="Space Arena", act="III", missions=["M3.08"], size={"w": 40000, "d": 40000, "h": 20000}, playtime="20 min",
  summary="A Sower gate megastructure: the fleet-battle arena where allies and the Directorate collide as Anthesis comes through.",
  goals=["Survive the fleet battle", "Protect allied ships", "Witness Anthesis"],
  spaces=[S("Gate ring", (8000, 8000, 800), "The megastructure (4 km radius)", (0, 0, 0)), S("Battle volume", (40000, 40000, 20000), "Fleet engagement space", (0, 0, 0)),
          S("Asteroid cover field", (15000, 15000, 5000), "Voxel asteroids for cover", (10000, -8000, 0))],
  encounters=["Directorate cruisers and carriers", "Spore-swarms", "Allied Hauler and Choir ships"], setpieces=["Anthesis unfolds through the gate (C14)"],
  landmarks=["The gate ring", "Anthesis"], mood={"time": "—", "palette": [("Gate teal", "#2EE6D6"), ("Violet", "#3A2A5C")], "light": "Gate glow, weapon fire"},
  audio="Battle chatter, choral swell as the gate opens.", build="None", gravity="0 g", atmosphere="Vacuum", kits=["KIT-SOW"],
  markers=["PS_M3_08", "CAM_C14_Anthesis", "TRG_M3_08_GateOpens"])
