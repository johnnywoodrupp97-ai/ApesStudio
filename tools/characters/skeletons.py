"""Skeleton templates, proportion profiles and facial shape-key sets.

Pure Python (no bpy): used by the Character Bible generator and by the Blender
character toolkit, so the docs and the rigs can never disagree.

Character convention (Blender): the character FACES −Y, up is +Z, the character's
LEFT is +X. Bone names follow the UE5 mannequin so animations retarget directly.
Positions below are for a 1.80 m reference adult in A-pose (arms 45° down).
"""

import math

REF_HEIGHT = 1.80
A_POSE = (math.cos(math.radians(45)), 0.0, -math.sin(math.radians(45)))


def _add(v, d, s=1.0):
    return tuple(round(v[i] + d[i] * s, 5) for i in range(3))


def _mirror(name):
    return name[:-2] + "_r" if name.endswith("_l") else name


def _mx(v):
    return (-v[0], v[1], v[2])


# --------------------------------------------------------------------------- humanoid
def _humanoid_left_and_center():
    """(name, parent, head, tail, deform, group) for the centre line and the LEFT side."""
    b = []
    add = b.append
    add(("root", None, (0, 0, 0), (0, 0, 0.12), True, "core"))
    add(("pelvis", "root", (0, 0, 0.98), (0, 0, 1.06), True, "core"))
    spine = [(1.06, 1.15), (1.15, 1.25), (1.25, 1.35), (1.35, 1.44), (1.44, 1.52)]
    parent = "pelvis"
    for i, (z0, z1) in enumerate(spine, 1):
        add((f"spine_{i:02d}", parent, (0, 0, z0), (0, 0, z1), True, "spine"))
        parent = f"spine_{i:02d}"
    add(("neck_01", "spine_05", (0, 0, 1.52), (0, -0.01, 1.585), True, "head"))
    add(("neck_02", "neck_01", (0, -0.01, 1.585), (0, -0.015, 1.635), True, "head"))
    add(("head", "neck_02", (0, -0.015, 1.635), (0, -0.015, 1.80), True, "head"))
    add(("jaw", "head", (0, -0.02, 1.665), (0, -0.095, 1.625), True, "head"))
    add(("eye_l", "head", (0.032, -0.075, 1.705), (0.032, -0.095, 1.705), True, "head"))

    # Arm (left), A-pose.
    add(("clavicle_l", "spine_05", (0.02, -0.03, 1.48), (0.165, 0.0, 1.485), True, "arm"))
    sh = (0.175, 0.0, 1.465)
    elbow = _add(sh, A_POSE, 0.29)
    wrist = _add(elbow, A_POSE, 0.26)
    hand_end = _add(wrist, A_POSE, 0.09)
    add(("upperarm_l", "clavicle_l", sh, elbow, True, "arm"))
    mid = _add(sh, A_POSE, 0.145)
    add(("upperarm_twist_01_l", "upperarm_l", mid, _add(mid, A_POSE, 0.05), True, "arm"))
    add(("lowerarm_l", "upperarm_l", elbow, wrist, True, "arm"))
    mid = _add(elbow, A_POSE, 0.13)
    add(("lowerarm_twist_01_l", "lowerarm_l", mid, _add(mid, A_POSE, 0.05), True, "arm"))
    add(("hand_l", "lowerarm_l", wrist, hand_end, True, "hand"))
    fingers = {"index": (-0.03, (0.045, 0.028, 0.022)), "middle": (-0.01, (0.05, 0.032, 0.024)),
               "ring": (0.01, (0.047, 0.03, 0.022)), "pinky": (0.03, (0.038, 0.022, 0.019))}
    for f, (yoff, lens) in fingers.items():
        p = _add(_add(hand_end, A_POSE, 0.005), (0, yoff, 0))
        par = "hand_l"
        for i, ln in enumerate(lens, 1):
            q = _add(p, A_POSE, ln)
            add((f"{f}_{i:02d}_l", par, p, q, True, "hand"))
            par, p = f"{f}_{i:02d}_l", q
    tdir = (0.45, -0.62, -0.64)
    n = math.sqrt(sum(c * c for c in tdir))
    tdir = tuple(c / n for c in tdir)
    p = _add(_add(wrist, A_POSE, 0.025), (0, -0.025, 0))
    par = "hand_l"
    for i, ln in enumerate((0.04, 0.032, 0.027), 1):
        q = _add(p, tdir, ln)
        add((f"thumb_{i:02d}_l", par, p, q, True, "hand"))
        par, p = f"thumb_{i:02d}_l", q

    # Leg (left).
    hip, knee, ankle = (0.095, 0, 0.95), (0.105, 0, 0.53), (0.115, 0.02, 0.095)
    add(("thigh_l", "pelvis", hip, knee, True, "leg"))
    mid = tuple((hip[i] + knee[i]) / 2 for i in range(3))
    add(("thigh_twist_01_l", "thigh_l", mid, _add(mid, (0, 0, -1), 0.05), True, "leg"))
    add(("calf_l", "thigh_l", knee, ankle, True, "leg"))
    mid = tuple((knee[i] + ankle[i]) / 2 for i in range(3))
    add(("calf_twist_01_l", "calf_l", mid, _add(mid, (0, 0, -1), 0.05), True, "leg"))
    add(("foot_l", "calf_l", ankle, (0.12, -0.10, 0.03), True, "leg"))
    add(("ball_l", "foot_l", (0.12, -0.10, 0.03), (0.12, -0.17, 0.03), True, "leg"))

    # IK helpers (non-deform, UE5-compatible).
    add(("ik_foot_root", "root", (0, 0, 0), (0, 0, 0.1), False, "ik"))
    add(("ik_foot_l", "ik_foot_root", (0.115, 0.02, 0.095), (0.115, 0.02, 0.145), False, "ik"))
    add(("ik_hand_root", "root", (0, 0, 0), (0, 0, 0.1), False, "ik"))
    add(("ik_hand_gun", "ik_hand_root", _mx(wrist), _add(_mx(wrist), (0, 0, 1), 0.05), False, "ik"))
    add(("ik_hand_l", "ik_hand_gun", wrist, _add(wrist, (0, 0, 1), 0.05), False, "ik"))
    return b


def _mirror_bones(bones):
    out = list(bones)
    for name, parent, head, tail, deform, group in bones:
        if name.endswith("_l"):
            out.append((_mirror(name), _mirror(parent) if parent else None, _mx(head), _mx(tail), deform, group))
    return out


LATERAL_GROUPS = {"arm", "hand", "leg"}

PROFILES = {
    # width: lateral scale of limbs/shoulders/hips · head: head size relative to an adult · bulk: proxy thickness
    "adult_average": {"width": 1.00, "head": 1.00, "bulk": 1.00, "label": "Adult, average build"},
    "adult_slim": {"width": 0.94, "head": 1.00, "bulk": 0.85, "label": "Adult, slim"},
    "adult_athletic": {"width": 1.05, "head": 1.00, "bulk": 1.08, "label": "Adult, athletic"},
    "adult_broad": {"width": 1.12, "head": 1.02, "bulk": 1.28, "label": "Adult, broad / heavy"},
    "elder": {"width": 0.97, "head": 1.00, "bulk": 0.92, "label": "Elder (stooped posture in animation)"},
    "teen": {"width": 0.95, "head": 1.10, "bulk": 0.88, "label": "Teen (13–17)"},
    "child": {"width": 0.88, "head": 1.32, "bulk": 0.78, "label": "Child (8–12)"},
    "brute": {"width": 1.45, "head": 0.82, "bulk": 2.00, "label": "Hollow Brute (overgrown)"},
    "exoframe": {"width": 1.55, "head": 0.60, "bulk": 2.20, "label": "Exo-frame / construct"},
    "colossus": {"width": 1.35, "head": 0.70, "bulk": 1.80, "label": "Colossal (Husk Titan)"},
}


def humanoid(height=REF_HEIGHT, profile="adult_average"):
    """Bones for a humanoid of ``height`` metres using a proportion profile."""
    prof = PROFILES[profile]
    head_len = 0.28  # neck_02 base (1.52) → crown (1.80)
    body_len = REF_HEIGHT - head_len
    s = height / (body_len + head_len * prof["head"])
    neck_base_z = 1.52
    out = []
    for name, parent, head, tail, deform, group in _mirror_bones(_humanoid_left_and_center()):
        def tx(v, name=name, group=group):
            x, y, z = v
            if group == "head":
                k = prof["head"]
                x, y, z = x * k, y * k, neck_base_z + (z - neck_base_z) * k
            if group in LATERAL_GROUPS or name.startswith(("clavicle", "ik_hand", "ik_foot_l", "ik_foot_r")):
                x *= prof["width"]
            return (round(x * s, 5), round(y * s, 5), round(z * s, 5))
        out.append({"name": name, "parent": parent, "head": tx(head), "tail": tx(tail), "deform": deform, "group": group})
    return out


HUMANOID_SOCKETS = [
    # (name, bone, offset from bone head in metres at 1.8 m, purpose)
    ("SOCKET_WeaponR", "hand_r", (-0.06, -0.02, -0.04), "Primary weapon / tool grip"),
    ("SOCKET_WeaponL", "hand_l", (0.06, -0.02, -0.04), "Off-hand item, flashlight, shield"),
    ("SOCKET_Back", "spine_04", (0, 0.16, 0), "Backpack, jetpack, back-slung weapon"),
    ("SOCKET_HipR", "pelvis", (-0.17, 0.0, -0.02), "Holster"),
    ("SOCKET_HipL", "pelvis", (0.17, 0.0, -0.02), "Tool loop (Ada's wrench)"),
    ("SOCKET_Helmet", "head", (0, 0.0, 0.0), "Helmet / hat attach (head bone origin)"),
    ("SOCKET_HelmetLight", "head", (0.07, -0.1, 0.1), "Helmet lamp"),
    ("SOCKET_ChestLight", "spine_05", (0.08, -0.13, 0.0), "Chest lamp, radio"),
    ("SOCKET_WristPad", "lowerarm_l", (0.0, -0.03, 0.02), "Wrist pad screen (story calls)"),
    ("SOCKET_Camera1P", "head", (0, -0.09, 0.07), "First-person camera (eye midpoint)"),
]

# --------------------------------------------------------------------------- creatures & constructs
def _chain(prefix, parent, start, end, n, group, deform=True):
    bones = []
    for i in range(n):
        a = tuple(start[k] + (end[k] - start[k]) * i / n for k in range(3))
        b = tuple(start[k] + (end[k] - start[k]) * (i + 1) / n for k in range(3))
        name = f"{prefix}_{i + 1:02d}" if n > 1 else prefix
        bones.append({"name": name, "parent": parent, "head": tuple(round(v, 5) for v in a),
                      "tail": tuple(round(v, 5) for v in b), "deform": deform, "group": group})
        parent = name
    return bones, parent


def multiped(shoulder_h, hip_h, length, legs=4, neck=0.5, head=0.4, tail=0.8, wings=0.0, width=None):
    """Quadruped/hexapod/flyer template. Head points to −Y."""
    width = width or 0.22 * length
    half = length / 2
    bones = [{"name": "root", "parent": None, "head": (0, 0, 0), "tail": (0, 0, 0.3), "deform": True, "group": "core"},
             {"name": "pelvis", "parent": "root", "head": (0, half, hip_h), "tail": (0, half - 0.15 * length, hip_h), "deform": True, "group": "core"}]
    sp, last = _chain("spine", "pelvis", (0, half - 0.15 * length, hip_h), (0, -half + 0.1 * length, shoulder_h), 4, "spine")
    bones += sp
    chest = (0, -half + 0.1 * length, shoulder_h)
    nk, last_n = _chain("neck", last, chest, (0, chest[1] - neck * 0.7, shoulder_h + neck * 0.7), 2, "head")
    bones += nk
    hd = (0, chest[1] - neck * 0.7, shoulder_h + neck * 0.7)
    bones.append({"name": "head", "parent": last_n, "head": hd, "tail": (0, hd[1] - head, hd[2] - head * 0.2), "deform": True, "group": "head"})
    bones.append({"name": "jaw", "parent": "head", "head": (0, hd[1] - head * 0.2, hd[2] - head * 0.15),
                  "tail": (0, hd[1] - head * 0.95, hd[2] - head * 0.3), "deform": True, "group": "head"})
    if tail > 0:
        tl, _ = _chain("tail", "pelvis", (0, half, hip_h), (0, half + tail, hip_h - tail * 0.3), 4, "tail")
        bones += tl
    # Leg attach points along the body (front → back).
    pairs = legs // 2
    attach_y = [chest[1] + 0.05 * length] + ([0.0] if pairs == 3 else []) + [half - 0.1 * length]
    attach_parent = ["spine_04"] + (["spine_02"] if pairs == 3 else []) + ["pelvis"]
    names = ["front", "mid", "hind"] if pairs == 3 else ["front", "hind"]
    for (y, par, nm) in zip(attach_y, attach_parent, names):
        top_z = shoulder_h if nm == "front" else (hip_h if nm == "hind" else (shoulder_h + hip_h) / 2)
        for side, sx in (("l", 1), ("r", -1)):
            x = sx * width / 2
            upper, lower, foot = (x, y, top_z * 0.95), (x * 1.05, y + 0.02 * length, top_z * 0.5), (x * 1.05, y, top_z * 0.08)
            toe = (x * 1.05, y - 0.08 * length, 0.0)
            chain = [(f"leg_{nm}_upper_{side}", par, upper, lower), (f"leg_{nm}_lower_{side}", f"leg_{nm}_upper_{side}", lower, foot),
                     (f"leg_{nm}_foot_{side}", f"leg_{nm}_lower_{side}", foot, toe)]
            for n_, p_, a, b in chain:
                bones.append({"name": n_, "parent": p_, "head": tuple(round(v, 5) for v in a),
                              "tail": tuple(round(v, 5) for v in b), "deform": True, "group": "leg"})
    if wings > 0:
        for side, sx in (("l", 1), ("r", -1)):
            wb, _ = _chain(f"wing_{side}", "spine_04", (sx * width / 2, chest[1], shoulder_h),
                           (sx * (width / 2 + wings), chest[1] + 0.1 * length, shoulder_h + 0.1 * wings), 3, "wing")
            for w in wb:  # rename wing_l_01 → wing_01_l for mirror-friendly names
                w["name"] = w["name"].replace(f"wing_{side}_", "wing_") + f"_{side}"
                if w["parent"].startswith(f"wing_{side}_"):
                    w["parent"] = w["parent"].replace(f"wing_{side}_", "wing_") + f"_{side}"
            bones += wb
    return bones


def serpentine(length, height=0.3, segments=12):
    bones = [{"name": "root", "parent": None, "head": (0, 0, 0), "tail": (0, 0, 0.2), "deform": True, "group": "core"}]
    sp, last = _chain("spine", "root", (0, length / 2, height), (0, -length / 2 + 0.1 * length, height), segments, "spine")
    bones += sp
    bones.append({"name": "head", "parent": last, "head": (0, -length / 2 + 0.1 * length, height),
                  "tail": (0, -length / 2, height), "deform": True, "group": "head"})
    bones.append({"name": "jaw", "parent": "head", "head": (0, -length / 2 + 0.08 * length, height - 0.05),
                  "tail": (0, -length / 2, height - 0.08), "deform": True, "group": "head"})
    return bones


def cetacean(length, girth):
    bones = [{"name": "root", "parent": None, "head": (0, 0, 0), "tail": (0, 0, 0.5), "deform": True, "group": "core"}]
    sp, last = _chain("spine", "root", (0, length * 0.2, girth / 2), (0, -length * 0.3, girth / 2), 5, "spine")
    bones += sp
    bones.append({"name": "head", "parent": last, "head": (0, -length * 0.3, girth / 2), "tail": (0, -length / 2, girth / 2), "deform": True, "group": "head"})
    bones.append({"name": "jaw", "parent": "head", "head": (0, -length * 0.33, girth * 0.3), "tail": (0, -length / 2, girth * 0.25), "deform": True, "group": "head"})
    tl, lt = _chain("tail", "root", (0, length * 0.2, girth / 2), (0, length * 0.45, girth / 2), 4, "tail")
    bones += tl
    for side, sx in (("l", 1), ("r", -1)):
        bones.append({"name": f"fin_{side}", "parent": "spine_04", "head": (sx * girth * 0.45, -length * 0.15, girth * 0.35),
                      "tail": (sx * girth * 1.1, -length * 0.05, girth * 0.2), "deform": True, "group": "fin"})
        bones.append({"name": f"fluke_{side}", "parent": lt, "head": (0, length * 0.45, girth / 2),
                      "tail": (sx * girth * 0.9, length * 0.5, girth / 2), "deform": True, "group": "fin"})
    return bones


def drone(size):
    h = size / 2
    b = [{"name": "root", "parent": None, "head": (0, 0, 0), "tail": (0, 0, 0.1), "deform": True, "group": "core"},
         {"name": "body", "parent": "root", "head": (0, 0, h), "tail": (0, -h, h), "deform": True, "group": "core"}]
    for nm, x, y in (("rotor_fl", 1, -1), ("rotor_fr", -1, -1), ("rotor_bl", 1, 1), ("rotor_br", -1, 1)):
        b.append({"name": nm, "parent": "body", "head": (x * h, y * h, h * 1.2), "tail": (x * h, y * h, h * 1.4), "deform": True, "group": "rotor"})
    b.append({"name": "gun_yaw", "parent": "body", "head": (0, -h * 0.5, h * 0.6), "tail": (0, -h * 0.5, h * 0.4), "deform": True, "group": "weapon"})
    b.append({"name": "gun_pitch", "parent": "gun_yaw", "head": (0, -h * 0.5, h * 0.4), "tail": (0, -h * 1.1, h * 0.4), "deform": True, "group": "weapon"})
    return b


def hologram(height):
    b = [{"name": "root", "parent": None, "head": (0, 0, 0), "tail": (0, 0, 0.1), "deform": True, "group": "core"},
         {"name": "core", "parent": "root", "head": (0, 0, height * 0.5), "tail": (0, 0, height * 0.6), "deform": True, "group": "core"}]
    for i in range(6):
        a = math.radians(60 * i)
        b.append({"name": f"ribbon_{i + 1:02d}", "parent": "core", "head": (0, 0, height * 0.55),
                  "tail": (round(math.cos(a) * height * 0.3, 5), round(math.sin(a) * height * 0.3, 5), round(height * 0.55, 5)),
                  "deform": True, "group": "ribbon"})
    return b


def build_skeleton(spec):
    """Resolve a catalog skeleton spec ``{"template": ..., **params}`` into a bone list."""
    t = spec["template"]
    if t == "humanoid":
        return humanoid(spec["height"], spec.get("profile", "adult_average"))
    if t in ("quadruped", "hexapod", "flyer"):
        legs = 6 if t == "hexapod" else 4
        return multiped(spec["shoulder_h"], spec.get("hip_h", spec["shoulder_h"]), spec["length"], legs=legs,
                        neck=spec.get("neck", 0.25 * spec["length"]), head=spec.get("head", 0.18 * spec["length"]),
                        tail=spec.get("tail", 0.3 * spec["length"]), wings=spec.get("wings", 0.0), width=spec.get("width"))
    if t == "serpentine":
        return serpentine(spec["length"], spec.get("height", 0.3))
    if t == "cetacean":
        return cetacean(spec["length"], spec["girth"])
    if t == "drone":
        return drone(spec["size"])
    if t == "hologram":
        return hologram(spec["height"])
    raise ValueError(f"Unknown skeleton template {t}")


TEMPLATE_NAMES = {
    "humanoid": "EXO_Humanoid (UE5 mannequin-compatible)",
    "quadruped": "EXO_Quadruped",
    "hexapod": "EXO_Hexapod",
    "flyer": "EXO_Flyer (quadruped + wing chains)",
    "serpentine": "EXO_Serpentine",
    "cetacean": "EXO_Cetacean",
    "drone": "EXO_Drone",
    "hologram": "EXO_Hologram",
}

# --------------------------------------------------------------------------- facial shape keys
ARKIT_52 = [
    "eyeBlinkLeft", "eyeLookDownLeft", "eyeLookInLeft", "eyeLookOutLeft", "eyeLookUpLeft", "eyeSquintLeft", "eyeWideLeft",
    "eyeBlinkRight", "eyeLookDownRight", "eyeLookInRight", "eyeLookOutRight", "eyeLookUpRight", "eyeSquintRight", "eyeWideRight",
    "jawForward", "jawLeft", "jawRight", "jawOpen",
    "mouthClose", "mouthFunnel", "mouthPucker", "mouthLeft", "mouthRight", "mouthSmileLeft", "mouthSmileRight",
    "mouthFrownLeft", "mouthFrownRight", "mouthDimpleLeft", "mouthDimpleRight", "mouthStretchLeft", "mouthStretchRight",
    "mouthRollLower", "mouthRollUpper", "mouthShrugLower", "mouthShrugUpper", "mouthPressLeft", "mouthPressRight",
    "mouthLowerDownLeft", "mouthLowerDownRight", "mouthUpperUpLeft", "mouthUpperUpRight",
    "browDownLeft", "browDownRight", "browInnerUp", "browOuterUpLeft", "browOuterUpRight",
    "cheekPuff", "cheekSquintLeft", "cheekSquintRight", "noseSneerLeft", "noseSneerRight", "tongueOut",
]
EXO_CORRECTIVES = [
    "exo_eyelidHeavy", "exo_sadInnerBrow", "exo_cryMouth", "exo_cryChin", "exo_swallow", "exo_breathIn", "exo_breathOut",
    "exo_jawClench", "exo_lipBite", "exo_nostrilFlare", "exo_smirkLeft", "exo_smirkRight", "exo_neckStrain",
    "exo_painWince", "exo_screamWide", "exo_whisper", "exo_coldShiver", "exo_tearUpLeft", "exo_tearUpRight",
    "exo_helmetFogBreath", "exo_squintSun", "exo_disgust", "exo_laughBig", "exo_exhaustedSlack",
]
INFECTION_SHAPES = ["INF_Veins", "INF_Lichen", "INF_EyeCloud", "INF_GumRecede"]
HOLLOW_SHAPES = ["jawOpen", "hol_jawSlack", "hol_snarlLeft", "hol_snarlRight", "eyeBlinkLeft", "eyeBlinkRight",
                 "noseSneerLeft", "noseSneerRight", "browDownLeft", "browDownRight", "hol_twitch", "hol_bloomPulse"]
CROWD_24 = ["eyeBlinkLeft", "eyeBlinkRight", "eyeSquintLeft", "eyeSquintRight", "eyeWideLeft", "eyeWideRight",
            "jawOpen", "mouthClose", "mouthFunnel", "mouthPucker", "mouthSmileLeft", "mouthSmileRight",
            "mouthFrownLeft", "mouthFrownRight", "mouthStretchLeft", "mouthStretchRight", "mouthPressLeft", "mouthPressRight",
            "browDownLeft", "browDownRight", "browInnerUp", "browOuterUpLeft", "browOuterUpRight", "cheekPuff"]

FACIAL_SETS = {
    "hero": ARKIT_52 + EXO_CORRECTIVES + INFECTION_SHAPES,
    "main": ARKIT_52 + EXO_CORRECTIVES[:12] + INFECTION_SHAPES,
    "secondary": ARKIT_52 + INFECTION_SHAPES,
    "crowd": CROWD_24 + INFECTION_SHAPES,
    "hollow": HOLLOW_SHAPES,
    "creature": ["jawOpen", "eyeBlinkLeft", "eyeBlinkRight", "cre_nostrilFlare", "cre_earsBack", "cre_snarl"],
    "none": [],
}
