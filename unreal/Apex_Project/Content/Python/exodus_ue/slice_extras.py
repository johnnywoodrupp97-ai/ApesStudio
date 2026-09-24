"""Hand-placed gameplay for the vertical slice, on top of the level bible's markers.

Positions are level-local metres (+X east, +Y north, +Z up from the level's ground), matching the
room layouts in docs/level-bible/05-kestrel-complex-and-township.md. The planner converts them to
world space. Beats follow game bible 03 §3.5–3.7 and 18 §18.1–18.2.
"""

CHAR = "/Game/Exodus/Imported/Characters/"
SHAMBLER = CHAR + "SK_ENM_Shambler_KestrelCrew"
CIVILIAN = CHAR + "SK_ENM_Shambler_Civilian"
RUNNER = CHAR + "SK_ENM_Runner"
CRAWLER = CHAR + "SK_ENM_Crawler"
TROOPER = CHAR + "SK_NPC_DirectorateTrooper"


def companion(name, at, cid, group, mesh, height=180.0, barks=(), follow=False, yaw=0.0):
    return {"class": "ExoCompanion", "name": name, "at": at, "yaw": yaw, "companion_id": cid, "group": group,
            "mesh_asset": CHAR + mesh, "height_cm": height, "barks": list(barks), "follow": follow}


def spawner(name, at, group, kind="Shambler", count=1, mesh=SHAMBLER, radius=3.0, story=""):
    return {"class": "ExoSpawner", "name": name, "at": at, "group": group, "hollow_type": kind, "count": count,
            "mesh_asset": mesh, "radius_cm": radius * 100.0, "story_id": story}


def use(name, at, kind, group="", prompt="", amount=1, **extra):
    return {"class": "ExoInteractableActor", "name": name, "marker_name": name, "at": at, "kind": kind, "group": group,
            "prompt": prompt, "amount": amount, **extra}


def marker(name, at, yaw=0.0, kind="PS"):
    return {"class": "ExoMarker", "name": name, "marker_name": name, "at": at, "yaw": yaw, "kind": kind}


def trigger(name, at, half):
    return {"class": "ExoMissionTrigger", "name": name, "marker_name": name, "at": at, "extent_m": list(half)}


def zone(name, at, half=(15, 15, 3)):
    return {"class": "ExoHordeZone", "name": name, "marker_name": name, "at": at, "extent_m": list(half)}


TUG_BARKS = ["Coffee's terrible. Drink it anyway.", "Keep your head down, kid.", "Your sister's gonna owe me a steak dinner."]
LILY_BARKS = ["Are they sad? The dead ones?", "I drew the spiral again. It helps.", "You walk loud. Like my dad.", "Ms. Alvarez said help was coming."]

EXTRAS = {
    # ---------------------------------------------------------------- Cold Open: Mission Control, 2068
    "KES-001": {
        "actors": [
            use("Console_Drill", (-4.0, -0.4, 0.8), "Console", prompt="E  Guide the Persephone drill arm"),
            companion("NPC_Crane", (-1.5, -4.0, 0.0), "Crane", "COLD", "SK_CHR_HalvardCrane", 188.0, yaw=90),
            companion("NPC_Mara", (3.0, 7.0, 1.0), "Mara", "COLD", "SK_CHR_MaraVoss", 170.0, yaw=-90),
        ],
    },
    # ---------------------------------------------------------------- Hangar 4 (M0.01, M0.03 end, M1.01, home base)
    "KES-002": {
        "actors": [
            companion("NPC_Tug", (4.0, -4.0, 0.0), "Tug", "M0_01", "SK_CHR_TugBrennan", 183.0, TUG_BARKS),
            use("WrenPanel", (0.0, -2.6, 1.0), "Generic", prompt="E  Weld the Wren's guidance panel"),
            use("Salvage_1", (-25.0, -15.0, 0.4), "Salvage", amount=40),
            use("Salvage_2", (25.0, -15.0, 0.4), "Salvage", amount=40),
            use("Salvage_3", (25.0, 15.0, 0.4), "Salvage", amount=40),
            use("Salvage_4", (-6.0, -17.0, 0.4), "Salvage", amount=40),
            use("Rations", (-26.0, -8.0, 0.5), "Food", amount=1),
            use("WaterCooler", (-24.0, -8.0, 0.5), "Water", amount=1),
            use("DistressRadio", (-12.0, 17.0, 1.0), "Radio", group="M1_01_radio", prompt="E  Listen to the distress call"),
            marker("PS_M0_03_Hangar", (0.0, -12.0, 0.1), 90),
            marker("PS_M1_01", (0.0, -6.0, 0.1), 90),
            trigger("TRG_M0_03_Roof", (0.0, -12.0, 21.6), (6, 5, 1.5)),
            trigger("TRG_M1_02_Home", (0.0, -26.0, 1.5), (8, 4, 2)),
            zone("HS_Hangar_N", (0.0, 150.0, 0.0)),
            zone("HS_Hangar_E", (150.0, 0.0, 0.0)),
            zone("HS_Hangar_S", (0.0, -160.0, 0.0)),
            zone("HS_Hangar_W", (-150.0, 0.0, 0.0)),
        ],
    },
    # ---------------------------------------------------------------- Service Corridors (M0.02)
    "KES-003": {
        "spawners": {"SP_DanaMarsh": {"group": "M0_02", "hollow_type": "Shambler", "count": 1, "mesh_asset": CHAR + "SK_CHR_DanaMarsh_Hollow", "story_id": "Dana"}},
        "actors": [
            use("MedCabinet", (10.0, -5.3, 1.0), "MedCabinet", group="M0_02"),
            use("Forklift", (41.0, 12.0, 0.8), "Generic", group="M0_02_cage", prompt="E  Drive the forklift: lift the rack"),
            spawner("SP_Corridor", (25.0, 0.0, 0.0), "M0_02_corridor", count=2),
            spawner("SP_CageHollow", (47.0, 8.0, 0.0), "M0_02_cage"),
            marker("PS_TugPinned", (48.0, 13.0, 0.1), kind="NPC"),
        ],
    },
    # ---------------------------------------------------------------- Terminal B (M0.03)
    "KES-004": {
        "actors": [
            spawner("SP_Concourse", (-65.0, 0.0, 0.0), "M0_03_terminal", count=6, mesh=CIVILIAN, radius=10.0),
            spawner("SP_GateHall", (-12.0, 6.0, 0.0), "M0_03_terminal", count=4, mesh=CIVILIAN, radius=8.0),
            spawner("SP_Baggage", (20.0, -20.0, -6.0), "M0_03_terminal", count=2, radius=5.0),
            spawner("SP_Apron", (72.0, -12.0, 0.0), "M0_03_apron", count=6, mesh=CIVILIAN, radius=8.0),
            companion("NPC_Trooper_Gate1", (8.0, -2.0, 0.0), "TrooperGate1", "M0_03_terminal", "SK_NPC_DirectorateTrooper", yaw=180),
            companion("NPC_Trooper_Gate2", (8.0, 3.0, 0.0), "TrooperGate2", "M0_03_terminal", "SK_NPC_DirectorateTrooper_Female", 175.0, yaw=180),
            trigger("TRG_M0_03_Gates", (-2.0, 0.0, 1.5), (3, 10, 2)),
            # after the skywalk collapse you land in the baggage hall; stairs lead up to the drop-off lane
            use("Ladder_Baggage_DropOff", (29.0, -18.0, -4.8), "Ladder", destination=(52.0, -12.0, 0.0)),
            marker("PS_M0_03_Fall", (22.0, -14.0, -5.9), 0),
            trigger("TRG_M0_03_Apron", (80.0, -10.0, 1.5), (4, 8, 2)),
        ],
    },
    # ---------------------------------------------------------------- Pad 12 (M0.03 standoff)
    "KES-005": {
        "boxes": [
            ("Seraph_Hull", 0.0, 22.0, 0.5, 8.5, 30.0, 10.0, "ship", "cube"),
            ("Seraph_Wing", 0.0, 22.0, 3.0, 4.0, 18.0, 30.0, "ship", "cube"),
            ("Seraph_Ramp", 0.0, 13.0, 0.3, 1.5, 4.0, 8.0, "ship", "cube"),
        ],
        "actors": [
            companion("NPC_Ada", (0.0, 11.0, 0.8), "Ada", "M0_03_pad", "SK_CHR_AdaOkafor", 175.0, yaw=-90),
            companion("NPC_Trooper_Pad1", (-4.0, -36.0, 0.0), "TrooperPad1", "M0_03_pad", "SK_NPC_DirectorateTrooper", yaw=-90),
            companion("NPC_Trooper_Pad2", (4.0, -36.0, 0.0), "TrooperPad2", "M0_03_pad", "SK_NPC_DirectorateTrooper_Female", 175.0, yaw=-90),
            marker("PS_Pad12_Approach", (-40.0, -70.0, 0.1), 60),
            trigger("TRG_M0_03_Fence", (0.0, -47.0, 1.5), (15, 3, 2)),
        ],
    },
    # ---------------------------------------------------------------- Kestrel Elementary (M1.02)
    "KES-006": {
        "openings": [("ClassroomWing1F", "N", 0.0, 2.4), ("Gym", "W", 0.0, 4.8)],
        "spawners": {"SP_MsAlvarez": {"group": "M1_02", "hollow_type": "Shambler", "count": 1, "mesh_asset": CHAR + "SK_CHR_RosaAlvarez_Hollow", "story_id": "MsAlvarez"}},
        "actors": [
            trigger("TRG_M1_02_School", (-15.0, 25.0, 1.5), (4, 3, 2)),
            use("Whiteboard", (21.0, 20.4, 1.2), "Generic", group="M1_02", prompt="E  Read the whiteboard"),
            use("FireAlarm", (-5.0, 6.6, 1.4), "FireAlarm", group="M1_02_gym"),
            companion("NPC_Lily", (-27.0, -19.0, 0.0), "Lily", "M1_02_lily", "SK_CHR_LilyChen", 142.0, LILY_BARKS),
            spawner("SP_Gym_A", (-20.0, -10.0, 0.0), "M1_02_gym", count=9, radius=6.0),
            spawner("SP_Gym_B", (-9.0, -16.0, 0.0), "M1_02_gym", count=9, radius=5.0),
            spawner("SP_Gym_Crawlers", (-25.0, -19.0, 0.0), "M1_02_gym", "Crawler", 4, CRAWLER, 3.0),
            spawner("SP_Hallway", (10.0, 5.0, 0.0), "M1_02", count=2, radius=4.0),
            spawner("SP_Exit_Runners", (-48.0, -14.0, 0.0), "M1_02_exit", "Runner", 3, RUNNER, 4.0),
            trigger("TRG_M1_02_Exit", (-34.0, -12.0, 1.5), (3, 4, 2)),
        ],
    },
}
