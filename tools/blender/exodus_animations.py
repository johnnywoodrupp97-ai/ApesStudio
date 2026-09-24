"""EXODUS PROTOCOL — procedural animation toolkit for the character rigs.

Builds a greybox animation set for every character body (Base and Variant files in assets/characters/),
checks it and exports it for the engine. Tested with Blender 4.2 (the `bpy` 4.2 module).

    blender -b -P tools/blender/exodus_animations.py -- build --all                 # every body: about 2 min
    blender -b -P tools/blender/exodus_animations.py -- build --asset SK_CHR_TugBrennan SK_ENM_Runner
    blender -b -P tools/blender/exodus_animations.py -- build --group story-cast hollows-and-constructs
    blender -b -P tools/blender/exodus_animations.py -- validate assets/animations/story-cast/SK_CHR_TugBrennan_Anims.blend
    blender -b -P tools/blender/exodus_animations.py -- export assets/animations/story-cast/SK_CHR_TugBrennan_Anims.blend
    blender -b -P tools/blender/exodus_animations.py -- export --compact <file>     # engine-ready, about 5x smaller
    blender -b -P tools/blender/exodus_animations.py -- list

`build` writes assets/animations/<chapter>/<asset>_Anims.blend: the character's rig and LOD0 body for preview plus one
action per animation (A_<asset without SK_>_<Anim>). The character files themselves are never modified, so rebuilding a
character never loses its animations (re-run `build` to refit them to a changed rig).

Every animation is generated from the rig itself (bone lengths, height, proportion profile) and the character's
style (survivor, soldier, Hollow, crawler, heavy, child, elder, limp), so the same code serves all 64 humanoids and
every creature template (quadruped, hexapod, flyer, serpentine, cetacean, drone, hologram). Locomotion is in place:
each cycle records its ground speed (`exo_speed` in cm/s) so the engine can scale the play rate to the actual speed.
Character convention (from skeletons.py): the character faces −Y, up is +Z, its left is +X.
"""
import argparse
import json
import math
import random
import sys
import zlib
from pathlib import Path

import bpy  # must be imported before mathutils when running as a stand-alone module
from mathutils import Matrix, Quaternion, Vector

HERE = Path(__file__).resolve().parent
TOOL_VERSION = "1.0"
FPS = 30
FWD = Vector((0.0, -1.0, 0.0))
BODY_KINDS = {"Base", "Variant"}


def repo_root():
    for parent in [HERE.parent] + list(HERE.parents):
        if (parent / "tools" / "characters" / "skeletons.py").exists():
            return parent
    return Path.cwd()


# --------------------------------------------------------------------------- maths
def rot(axis, deg):
    return Quaternion(axis, math.radians(deg))


def pitch(deg):
    """Rotation about the lateral axis. + swings a hanging bone's tip forward (and tips a forward bone's tip up);
    − leans an upright bone (spine, neck) forward. Knee bend is −, toes-up is +."""
    return rot((1.0, 0.0, 0.0), -deg)


def roll(deg):
    """Rotation about the forward axis: + tilts an upright bone's top toward the character's left (+X)."""
    return rot((0.0, 1.0, 0.0), deg)


def yaw(deg):
    """Rotation about up: + turns the character's front toward its left."""
    return rot((0.0, 0.0, 1.0), deg)


def cyc(p, k=1.0, ph=0.0):
    return math.cos(2 * math.pi * (k * p + ph))


def syc(p, k=1.0, ph=0.0):
    return math.sin(2 * math.pi * (k * p + ph))


def bump(x, centre, width):
    """Smooth 0..1..0 bump around centre on a looping 0..1 axis."""
    d = min(abs(x - centre), 1 - abs(x - centre))
    return math.exp(-(d / width) ** 2)


def ease(t):
    t = min(1.0, max(0.0, t))
    return t * t * (3 - 2 * t)


def seg(t, a, b):
    """0 before a, eased 0..1 between a and b, 1 after b."""
    return ease((t - a) / (b - a)) if b > a else float(t >= a)


def env_hit(t, peak=0.18):
    """A hit: fast rise to 1 at `peak`, slow settle back to 0 by t = 1."""
    return seg(t, 0.0, peak) * (1 - seg(t, peak, 1.0))


# --------------------------------------------------------------------------- rig
class Rig:
    def __init__(self, arm):
        self.obj = arm
        self.bones = {b.name: b for b in arm.data.bones}
        self.R = {n: b.matrix_local.to_3x3().to_quaternion() for n, b in self.bones.items()}
        self.dir = {n: (b.tail_local - b.head_local).normalized() for n, b in self.bones.items()}
        self.asset = arm.get("asset", arm.name)
        self.kind = arm.get("kind", "")
        self.registry = arm.get("registry_id", "")
        self.spec = json.loads(arm.get("skeleton", "{}")) if arm.get("skeleton") else {}
        self.template = self.spec.get("template", "humanoid")
        self.rng = random.Random(zlib.crc32(self.asset.encode()))
        if self.template == "humanoid":
            self.leg = self.bones["pelvis"].head_local.z                      # hip height
            self.height = self.bones["head"].tail_local.z
            self.scale = self.height / 1.8
        elif self.template in ("quadruped", "hexapod", "flyer"):
            self.leg = self.spec.get("shoulder_h", 1.0)
            self.height = self.leg
            self.scale = self.leg
        else:
            self.leg = self.height = self.scale = float(self.spec.get("length") or self.spec.get("size") or self.spec.get("height") or 1.0)

        self.M = {n: b.matrix_local.copy() for n, b in self.bones.items()}
        self.Minv = {n: m.inverted() for n, m in self.M.items()}
        self.parent = {n: (b.parent.name if b.parent else None) for n, b in self.bones.items()}
        self.contacts = self._contacts()
        self.rest_ground = min(p.z for _b, p in self.contacts) if self.contacts else 0.0

    def has(self, name):
        return name in self.bones

    def _contacts(self):
        """Points that touch the floor, as (bone, rest armature-space point): heel and toe of each foot."""
        pts = []
        if self.template == "humanoid":
            for side in ("l", "r"):
                ankle = self.bones[f"foot_{side}"].head_local
                pts.append((f"foot_{side}", Vector((ankle.x, ankle.y + 0.03 * self.scale, 0.01 * self.scale))))
                pts.append((f"ball_{side}", self.bones[f"ball_{side}"].tail_local.copy()))
            if "crawler" in self.registry or self.asset == "SK_ENM_Crawler":   # prone: hands, knees and toes carry it
                for side in ("l", "r"):
                    pts.append((f"hand_{side}", self.bones[f"hand_{side}"].tail_local.copy()))
                    pts.append((f"calf_{side}", self.bones[f"calf_{side}"].head_local.copy()))
                pts.append(("spine_02", self.bones["spine_02"].head_local.copy()))
        else:
            for n, b in self.bones.items():
                if n.startswith("leg_") and "_foot_" in n:
                    pts += [(n, b.tail_local.copy()), (n, b.head_local.copy())]
        return pts

    def fk(self, P):
        """Posed armature-space matrices for every bone (Blender's pose evaluation, done here in Python)."""
        out = {}

        def mat(n):
            if n in out:
                return out[n]
            q = self.local_rot(n, P.r[n]) if n in P.r else Quaternion()
            t = self.local_loc(n, P.t[n]) if n in P.t else Vector()
            basis = Matrix.Translation(t) @ q.to_matrix().to_4x4()
            par = self.parent[n]
            m = (mat(par) @ self.Minv[par] @ self.M[n] if par else self.M[n]) @ basis
            out[n] = m
            return m
        for n in self.bones:
            mat(n)
        return out

    def lowest_contact(self, P):
        mats = self.fk(P)
        return min((mats[b] @ self.Minv[b] @ p).z for b, p in self.contacts)

    def ground(self, P, lift=0.0):
        """Move the pelvis (the body root) so the lowest heel or toe rests on the floor, plus `lift` (flight phases)."""
        if not self.contacts:
            return
        body = "pelvis" if "pelvis" in self.bones else "root"
        P.move(body, (0.0, 0.0, self.rest_ground - self.lowest_contact(P) + lift))

    def local_rot(self, name, q):
        r = self.R[name]
        return r.inverted() @ q @ r

    def local_loc(self, name, v):
        return self.R[name].inverted() @ Vector(v)

    def hinge(self, name, deg, d=None):
        """Rotate a bone's (current) direction toward the character's front by deg (a hinge about d × forward)."""
        d = (d or self.dir[name]).normalized()
        axis = d.cross(FWD)
        if axis.length < 1e-4:
            axis = Vector((-1.0, 0.0, 0.0))
        return Quaternion(axis.normalized(), math.radians(deg))


class Pose:
    """Armature-space rotations (in each bone's parent rest frame) and armature-space pelvis/root offsets."""

    def __init__(self):
        self.r = {}
        self.t = {}

    def rot(self, bone, q):
        self.r[bone] = q @ self.r.get(bone, Quaternion())

    def move(self, bone, v):
        self.t[bone] = self.t.get(bone, Vector()) + Vector(v)


# --------------------------------------------------------------------------- humanoid styles
def humanoid_style(rig):
    """Movement style from the character's rig metadata (profile, group, name)."""
    profile = rig.spec.get("profile", "adult_average")
    reg, a = rig.registry, rig.asset
    st = {"kind": "survivor", "limp": None, "limp_amt": 0.0, "child": profile == "child", "elder": profile == "elder",
          "teen": profile == "teen", "heavy": profile in ("brute", "exoframe", "colossus"), "hollow": False, "runner": False,
          "crawler": False, "soldier": False, "tilt": 0.0, "lean": 0.0, "shoulder": 0.0}
    hollow = ".hol." in reg or "_Hollow" in a or a.startswith("SK_ENM_Shambler")
    if hollow:
        st.update(kind="hollow", hollow=True)
        st["limp"] = rig.rng.choice(("l", "r"))
        st["limp_amt"] = rig.rng.uniform(0.35, 0.8)
        st["tilt"] = rig.rng.uniform(8, 24) * rig.rng.choice((-1, 1))
        st["lean"] = rig.rng.uniform(8, 18)
        st["shoulder"] = rig.rng.uniform(4, 12) * rig.rng.choice((-1, 1))
    if "runner" in reg or a == "SK_ENM_Runner":
        st["runner"] = True
    if "crawler" in reg or a == "SK_ENM_Crawler":
        st.update(kind="crawler", crawler=True)
    if st["heavy"]:
        st["kind"] = "heavy"
    if any(k in reg for k in ("directorate_trooper", "directorate_enforcer", "directorate_officer", "idris_kaan", "crane_director",
                              "choir_warden")):
        st.update(kind="soldier" if not st["heavy"] else "heavy", soldier=True)
    if "tug_brennan" in reg:                       # character bible 11.3: Tug's limp locomotion
        st.update(limp="r", limp_amt=0.55)
    if "mara_voss" in reg:                         # frail locomotion
        st["lean"] = 6
    return st


HUMAN_SETS = {
    "survivor": ["Idle", "Walk", "Jog", "Sprint", "CrouchWalk", "Talk", "Wave", "HitReact", "Death"],
    "soldier": ["Idle", "Walk", "Jog", "Sprint", "CrouchWalk", "Talk", "Wave", "HitReact", "Death"],
    "hollow": ["Idle", "Walk", "Run", "Attack", "HitReact", "Death"],
    "crawler": ["Idle", "Walk", "Run", "Attack", "HitReact", "Death"],
    "heavy": ["Idle", "Walk", "Run", "Attack", "HitReact", "Death"],
}

# Locomotion parameters (1.80 m adult): cycle seconds, thigh swing, swing-knee, stance-knee, arm swing, elbow,
# torso lean, pelvis yaw/roll, crouch (0..1), flight (running bob)
GAITS = {
    "Walk": dict(T=1.10, thigh=24, knee=48, kstance=8, arm=16, elbow=12, lean=3, pyaw=5, proll=3, crouch=0.0, flight=False),
    "Jog": dict(T=0.72, thigh=36, knee=80, kstance=18, arm=30, elbow=70, lean=8, pyaw=7, proll=4, crouch=0.0, flight=True),
    "Sprint": dict(T=0.60, thigh=46, knee=105, kstance=22, arm=48, elbow=85, lean=14, pyaw=9, proll=4, crouch=0.0, flight=True),
    "CrouchWalk": dict(T=1.25, thigh=22, knee=40, kstance=10, arm=10, elbow=35, lean=24, pyaw=4, proll=2, crouch=0.55, flight=False),
    "Run": dict(T=0.72, thigh=36, knee=80, kstance=18, arm=30, elbow=70, lean=8, pyaw=7, proll=4, crouch=0.0, flight=True),
}


def human_gait(name, st, scale):
    g = dict(GAITS[name])
    tscale = math.sqrt(scale)                       # dynamic similarity: bigger bodies step slower
    if st["child"]:
        tscale *= 0.9
        g["arm"] *= 1.3
    if st["elder"]:
        tscale *= 1.15
        g["thigh"] *= 0.8
        g["lean"] += 14
    if st["heavy"]:
        tscale *= 1.1
        g["arm"] *= 0.6
        g["pyaw"] *= 0.6
        g["proll"] *= 1.8
        g["lean"] += 6
    if st["hollow"] and name == "Walk":             # the shamble: short, lurching, dragging steps
        g.update(T=1.35, thigh=20, knee=30, kstance=6, arm=6, elbow=10, pyaw=8, proll=7)
        g["lean"] += st["lean"]
    if st["hollow"] and name == "Run":
        if st["runner"]:                              # Runners sprint: game bible 22 — 5.8 m/s
            g.update(GAITS["Sprint"])
            g["lean"] = 22
            g["arm"] = 60
        else:                                         # a Shambler's lunging stagger
            g.update(T=0.9, thigh=30, knee=60, kstance=14, arm=14, elbow=30, pyaw=10, proll=8, flight=False)
            g["lean"] += st["lean"] + 6
    g["T"] *= tscale
    return g


def gait_speed(leg, g):
    """Ground speed (m/s) of an in-place cycle: each foot sweeps 2·L·sin(amp) during its half-cycle stance."""
    return 4 * leg * math.sin(math.radians(g["thigh"])) / g["T"]


# --------------------------------------------------------------------------- humanoid poses
def arm(rig, P, side, down=35.0, swing=0.0, elbow=10.0, wrist=0.0, curl=18.0, twist=0.0):
    """Arm from the A-pose: `down` lowers it toward the body (frontal plane), `swing` moves it forward,
    `elbow` bends the forearm forward, `curl` closes the fingers."""
    s = 1 if side == "l" else -1
    q_down = roll(s * down)
    d1 = q_down @ rig.dir[f"upperarm_{side}"]
    q = rig.hinge(f"upperarm_{side}", swing, d1) @ q_down
    if twist:
        q = Quaternion(d1, math.radians(s * twist)) @ q
    P.rot(f"upperarm_{side}", q)
    P.rot(f"lowerarm_{side}", rig.hinge(f"lowerarm_{side}", elbow))
    if wrist:
        P.rot(f"hand_{side}", rig.hinge(f"hand_{side}", wrist))
    for f in ("index", "middle", "ring", "pinky"):
        for i in (1, 2, 3):
            b = f"{f}_{i:02d}_{side}"
            if rig.has(b):
                P.rot(b, roll(s * curl * (0.8 + 0.2 * i)))


def legs(rig, P, side, thigh=0.0, knee=0.0, foot_extra=0.0, ball=0.0, spread=0.0, pelvis_pitch=0.0):
    """Leg in the sagittal plane; the foot is kept level (compensating hip, knee and pelvis) plus foot_extra."""
    s = 1 if side == "l" else -1
    P.rot(f"thigh_{side}", roll(-s * spread) @ pitch(thigh))
    P.rot(f"calf_{side}", pitch(-knee))
    P.rot(f"foot_{side}", pitch(knee - thigh - pelvis_pitch + foot_extra))
    if ball:
        P.rot(f"ball_{side}", pitch(ball))


def spine(P, lean=0.0, twist=0.0, side=0.0, chest=0.0):
    """Distribute lean (+ forward), twist (+ to the left) and side-bend over the five spine bones."""
    w = (0.14, 0.2, 0.22, 0.22, 0.22)
    for i, k in enumerate(w, 1):
        P.rot(f"spine_{i:02d}", yaw(twist * k) @ roll(side * k) @ pitch(-lean * k - (chest * k if i >= 4 else 0.0)))


def head(P, nod=0.0, turn=0.0, tilt=0.0):
    P.rot("neck_01", yaw(turn * 0.4) @ roll(tilt * 0.4) @ pitch(-nod * 0.4))
    P.rot("head", yaw(turn * 0.6) @ roll(tilt * 0.6) @ pitch(-nod * 0.6))


def upper_body_style(rig, P, st, p, amt=1.0):
    """Posture layers: soldier rifle hold, Hollow asymmetry."""
    if st["hollow"]:
        head(P, nod=st["lean"] * 0.4, tilt=st["tilt"] * amt)
        P.rot("clavicle_l" if st["shoulder"] > 0 else "clavicle_r", roll((1 if st["shoulder"] > 0 else -1) * abs(st["shoulder"])))
        if rig.has("jaw"):
            P.rot("jaw", pitch(-8 - 4 * syc(p)))


def human_locomotion(rig, P, p, g, st):
    L, s = rig.leg, rig.scale
    crouch = g["crouch"]
    pp_pitch = -40.0 * crouch                     # crouching tips the pelvis forward; the legs compensate below
    for side, ph in (("l", 0.0), ("r", 0.5)):
        q = (p + ph) % 1.0
        amp, kswing = g["thigh"], g["knee"]
        lame = st["limp"] == side
        if lame:                                   # the lame leg: short, stiff swing
            amp *= 1 - 0.35 * st["limp_amt"]
            kswing *= 1 - 0.7 * st["limp_amt"]
        th = amp * math.cos(2 * math.pi * q) + crouch * 45
        stance = q < 0.5
        flex = g["kstance"] * math.sin(2 * math.pi * q) if stance else kswing * math.sin(2 * math.pi * (q - 0.5)) ** 1.5
        if st["hollow"] and not lame and not stance:
            flex *= 1.25
        knee = flex + crouch * 85
        toe = -18 * bump(q, 0.5, 0.08) + (8 * bump(q, 0.0, 0.06) if not st["hollow"] else -6)
        legs(rig, P, side, th - pp_pitch, knee, foot_extra=toe, ball=14 * bump(q, 0.5, 0.08), spread=4 if st["heavy"] else 1.5,
             pelvis_pitch=pp_pitch)
    # pelvis height comes from the grounding pass (Rig.ground); here only the side-to-side weight shift
    P.move("pelvis", (0.012 * s * syc(p) * (3 if st["hollow"] else 1), 0.0, 0.0))
    roll_amt = g["proll"] * (1 + (st["limp_amt"] if st["limp"] else 0))
    P.rot("pelvis", yaw(-g["pyaw"] * cyc(p)) @ roll(-roll_amt * syc(p)) @ pitch(pp_pitch))
    # torso counter-rotation and lean; head stays on the horizon
    hunch = 14 if st["hollow"] and not st["runner"] else 0
    spine(P, lean=g["lean"] - 20 * crouch + hunch, twist=g["pyaw"] * 1.6 * cyc(p), side=roll_amt * 0.8 * syc(p))
    if st["hollow"]:                               # Hollows let the head hang and loll with the stride
        head(P, nod=6 - hunch * 0.2 + 5 * cyc(p, 2), turn=-g["pyaw"] * 0.3 * cyc(p), tilt=4 * syc(p))
    else:
        head(P, nod=-(g["lean"] + 20 * crouch) * 0.8, turn=-g["pyaw"] * 0.6 * cyc(p))
    # arms swing opposite the legs
    for side, sgn in (("l", -1), ("r", 1)):
        sw = g["arm"] * sgn * cyc(p)
        if st["soldier"]:                          # rifle at the low ready
            arm(rig, P, side, down=32 if side == "r" else 38, swing=40 + 0.15 * sw, elbow=95 if side == "r" else 75, curl=60)
        elif st["hollow"] and not st["runner"]:
            reach = 38 if (side == "l") == (st["tilt"] > 0) else 16   # one arm reaches, the other hangs
            arm(rig, P, side, down=28, swing=reach + sw * 0.5 + 8 * syc(p, 1, 0.3), elbow=g["elbow"] + 12, curl=35)
        else:
            arm(rig, P, side, down=37, swing=sw, elbow=g["elbow"] + (g["elbow"] * 0.3 * max(0.0, sw / max(g["arm"], 1))), curl=25)
    upper_body_style(rig, P, st, p)


def human_idle(rig, P, p, st):
    s = rig.scale
    breath = syc(p, 2)
    P.move("pelvis", (0.015 * s * syc(p), 0.0, -0.004 * s * (1 + cyc(p, 2))))
    P.rot("pelvis", roll(1.5 * syc(p)))
    lean = st["lean"] + (14 if st["elder"] else 0) + (6 if st["heavy"] else 0) + (14 if st["hollow"] else 0)
    spine(P, lean=lean + 1.2 * breath, side=-1.5 * syc(p), twist=2 * syc(p, 1, 0.2))
    head(P, nod=(4 - lean * 0.2 if st["hollow"] else -lean * 0.6) + 2 * syc(p, 2, 0.1), turn=10 * syc(p) + 4 * syc(p, 3, 0.4),
         tilt=2 * syc(p, 2, 0.3))
    for side, s2 in (("l", 1), ("r", -1)):
        P.rot(f"clavicle_{side}", roll(-s2 * 1.5 * (1 + breath)))
        legs(rig, P, side, thigh=2 + 1.5 * s2 * syc(p), knee=4 + 3 * max(0.0, s2 * syc(p)), spread=3 if st["heavy"] else 1)
        if st["soldier"]:
            arm(rig, P, side, down=32 if side == "r" else 38, swing=38, elbow=95 if side == "r" else 75, curl=60)
        elif st["hollow"]:
            arm(rig, P, side, down=28, swing=22 + 6 * syc(p, 1, 0.25 if side == "l" else 0.6), elbow=18, curl=35)
        else:
            arm(rig, P, side, down=36, swing=3 * syc(p, 1, 0.1 * s2), elbow=12, curl=22)
    if st["hollow"]:
        P.move("pelvis", (0.02 * s * syc(p, 1, 0.4), 0.01 * s * syc(p, 2), 0.0))
        spine(P, side=5 * syc(p, 1, 0.1), twist=4 * syc(p, 2, 0.3))
    upper_body_style(rig, P, st, p)


def human_talk(rig, P, p, st):
    human_idle(rig, P, p, st)
    g1 = syc(p, 2)
    arm(rig, P, "r", down=-2, swing=28 + 12 * g1, elbow=55 + 20 * syc(p, 4), wrist=10 * syc(p, 4, 0.2), curl=-4)
    arm(rig, P, "l", down=-1, swing=10 + 8 * syc(p, 2, 0.35), elbow=25 + 15 * syc(p, 2, 0.35))
    head(P, nod=4 * syc(p, 3), turn=6 * syc(p, 2, 0.15))
    if rig.has("jaw"):
        P.rot("jaw", pitch(-7 * abs(syc(p, 8))))


def human_wave(rig, P, p, st):
    human_idle(rig, P, p, st)
    P.r.pop("upperarm_r", None), P.r.pop("lowerarm_r", None)
    arm(rig, P, "r", down=-95, swing=15, elbow=45, curl=0)
    P.rot("lowerarm_r", roll(-22 * syc(p, 3)))
    head(P, turn=-6, nod=-3)


def human_hit(rig, P, t, st):
    human_idle(rig, P, 0.0, st)
    e = env_hit(t)
    spine(P, lean=-16 * e, twist=10 * e)
    head(P, nod=-18 * e, turn=12 * e)
    for side, s2 in (("l", 1), ("r", -1)):
        arm(rig, P, side, down=-25 * e, swing=25 * e, elbow=40 * e)
        legs(rig, P, side, knee=14 * e)
    P.move("pelvis", (0.0, 0.08 * rig.scale * e, -0.04 * rig.scale * e))


def human_death(rig, P, t, st):
    """Knees buckle, then the body topples forward and settles face down (holds the last frame)."""
    L, s = rig.leg, rig.scale
    buckle, fall, settle = seg(t, 0.0, 0.35), seg(t, 0.25, 0.8), seg(t, 0.75, 1.0)
    pp = -85 * fall
    P.rot("pelvis", pitch(pp) @ yaw(8 * fall) @ roll(-6 * fall))
    P.move("pelvis", (0.05 * s * fall, -0.55 * L * fall, -(L * 0.3) * buckle - (L * 0.55 - 0.13 * s) * fall))
    for side, s2 in (("l", 1), ("r", -1)):
        legs(rig, P, side, thigh=38 * buckle * (1 - fall) + 8 * fall, knee=70 * buckle * (1 - fall) + 12 * fall,
             pelvis_pitch=pp, spread=6 * fall)
        arm(rig, P, side, down=35 - 60 * fall, swing=20 * buckle + 70 * fall, elbow=30 + 30 * fall, curl=40)
    spine(P, lean=20 * buckle * (1 - fall) - 5 * settle, twist=6 * fall)
    head(P, nod=10 * buckle - 40 * fall, turn=35 * fall)


def human_attack(rig, P, t, st):
    """Hollow lunge-grab (heavy characters: an overhead two-handed slam)."""
    s, L = rig.scale, rig.leg
    wind, strike, rec = seg(t, 0.0, 0.3), seg(t, 0.3, 0.45), seg(t, 0.55, 1.0)
    k = strike * (1 - rec)
    if st["heavy"]:
        up = wind * (1 - strike)
        for side in ("l", "r"):
            arm(rig, P, side, down=20, swing=160 * up + 50 * k + 20 * (1 - wind) * (1 - rec), elbow=60 * up + 10 * k, curl=70)
        spine(P, lean=-12 * up + 38 * k)
        head(P, nod=-8 * up + 10 * k)
        for side in ("l", "r"):
            legs(rig, P, side, thigh=12 * k, knee=24 * k + 6, spread=5)
        P.move("pelvis", (0.0, -0.1 * s * k, -0.12 * L * k))
        return
    lunge = wind * 0.3 + k
    for side, lag in (("l", 0.0), ("r", 0.05)):
        kk = seg(t, 0.3 + lag, 0.45 + lag) * (1 - rec)
        arm(rig, P, side, down=15, swing=70 * wind * (1 - kk) + 95 * kk, elbow=50 * wind * (1 - kk) + 15 * kk, curl=70 * kk + 30)
    spine(P, lean=-8 * wind * (1 - strike) + 32 * k, twist=10 * k)
    head(P, nod=-10 * k, tilt=st["tilt"] * (1 - k))
    legs(rig, P, "l", thigh=28 * lunge, knee=30 * lunge)
    legs(rig, P, "r", thigh=-14 * lunge, knee=10 * lunge)
    P.move("pelvis", (0.0, -0.3 * L * lunge, -0.08 * L * lunge))
    if rig.has("jaw"):
        P.rot("jaw", pitch(-22 * k - 8))


def crawler_base(rig, P, st, lift=0.0):
    """Prone: pelvis near the floor and tipped 80° forward, legs trailing, chest and head raised."""
    L, s = rig.leg, rig.scale
    P.move("pelvis", (0.0, 0.25 * L, -(L - 0.24 * s) + lift * L * 0.25))
    P.rot("pelvis", pitch(-80 + lift * 25))
    spine(P, lean=-18 - lift * 20, chest=-10)
    head(P, nod=-45 - lift * 10, tilt=st["tilt"] * 0.5)
    if rig.has("jaw"):
        P.rot("jaw", pitch(-10))


def crawler_move(rig, P, p, st, fast=False):
    crawler_base(rig, P, st)
    reach = 30 if fast else 24
    for side, ph in (("l", 0.0), ("r", 0.5)):
        q = (p + ph) % 1.0
        sw = 100 + reach * math.cos(2 * math.pi * q)            # reach forward, drag back under the body
        lift = max(0.0, math.sin(2 * math.pi * (q - 0.5)))      # the arm lifts while it swings forward
        arm(rig, P, side, down=40, swing=sw, elbow=25 + 35 * lift, curl=50 - 30 * lift)
        s2 = 1 if side == "l" else -1
        legs(rig, P, side, thigh=4 + 6 * math.cos(2 * math.pi * (q + 0.25)), knee=6 + 14 * max(0.0, syc(q)),
             spread=6 + 2 * s2 * syc(p), pelvis_pitch=-80)
    spine(P, twist=10 * cyc(p), side=6 * syc(p))
    P.move("pelvis", (0.0, 0.03 * rig.scale * cyc(p, 2), 0.01 * rig.scale * cyc(p, 2)))


def crawler_idle(rig, P, p, st):
    crawler_base(rig, P, st, lift=0.1 + 0.05 * syc(p, 2))
    for side, s2 in (("l", 1), ("r", -1)):
        arm(rig, P, side, down=38, swing=95 + 4 * syc(p, 1, 0.2 * s2), elbow=40, curl=55)
        legs(rig, P, side, thigh=5, knee=12, spread=7, pelvis_pitch=-70)
    head(P, turn=25 * syc(p) + 8 * syc(p, 3), nod=4 * syc(p, 2))


def crawler_attack(rig, P, t, st):
    rise, strike, rec = seg(t, 0.0, 0.3), seg(t, 0.3, 0.45), seg(t, 0.6, 1.0)
    k = strike * (1 - rec)
    crawler_base(rig, P, st, lift=rise * (1 - rec) * 1.2)
    for side in ("l", "r"):
        arm(rig, P, side, down=20, swing=100 + 50 * rise * (1 - k) - 10 * k, elbow=60 * rise * (1 - k) + 10 * k, curl=80)
        legs(rig, P, side, thigh=10 * rise, knee=25 * rise, spread=8, pelvis_pitch=-60)
    P.move("pelvis", (0.0, -0.35 * rig.leg * k, 0.0))
    if rig.has("jaw"):
        P.rot("jaw", pitch(-25 * k))


# --------------------------------------------------------------------------- creatures
def leg_names(rig):
    out = []
    for pos in ("front", "mid", "hind"):
        for side in ("l", "r"):
            if rig.has(f"leg_{pos}_upper_{side}"):
                out.append((pos, side))
    return out


QUAD_PHASES = {  # foot-fall offsets per gait (0 = front contact of that leg)
    "Walk": {("hind", "l"): 0.0, ("front", "l"): 0.25, ("hind", "r"): 0.5, ("front", "r"): 0.75},
    "Trot": {("front", "l"): 0.0, ("hind", "r"): 0.0, ("front", "r"): 0.5, ("hind", "l"): 0.5},
    "Gallop": {("hind", "l"): 0.0, ("hind", "r"): 0.1, ("front", "l"): 0.5, ("front", "r"): 0.6},
}
HEX_PHASES = {("front", "l"): 0.0, ("mid", "r"): 0.0, ("hind", "l"): 0.0, ("front", "r"): 0.5, ("mid", "l"): 0.5, ("hind", "r"): 0.5}
CREATURE_GAITS = {"Walk": dict(T=0.9, amp=20, knee=35, bob=0.02), "Trot": dict(T=0.55, amp=28, knee=55, bob=0.04),
                  "Gallop": dict(T=0.42, amp=38, knee=70, bob=0.08)}


def multiped_gait(rig, name):
    g = dict(CREATURE_GAITS[name])
    g["T"] *= math.sqrt(max(rig.leg, 0.05) / 0.55)
    return g


def multiped_locomotion(rig, P, p, gait, g, wings_folded=False):
    phases = HEX_PHASES if rig.template == "hexapod" else QUAD_PHASES[gait]
    if rig.template == "hexapod" and gait == "Trot":
        phases = HEX_PHASES
    for pos, side in leg_names(rig):
        q = (p - phases.get((pos, side), 0.0)) % 1.0
        th = g["amp"] * math.cos(2 * math.pi * q)
        flex = g["knee"] * max(0.0, math.sin(2 * math.pi * (q - 0.5))) ** 1.3 + 4
        P.rot(f"leg_{pos}_upper_{side}", pitch(th))
        P.rot(f"leg_{pos}_lower_{side}", pitch(-flex))
        P.rot(f"leg_{pos}_foot_{side}", pitch(flex - th))
    s = rig.leg
    bob = g["bob"] * s
    P.move("pelvis", (0.0, 0.0, -bob * cyc(p, 2)))
    flexk = 10 if gait == "Gallop" else 3
    for i in range(1, 5):
        if rig.has(f"spine_{i:02d}"):
            P.rot(f"spine_{i:02d}", pitch(flexk * syc(p) * (1 if i < 3 else -1)) @ yaw(2 * syc(p)))
    for b in ("neck_01", "neck_02"):
        if rig.has(b):
            P.rot(b, pitch(3 * cyc(p, 2)))
    tail(rig, P, p, 12)
    if wings_folded:
        fold_wings(rig, P)


def tail(rig, P, p, amp, k=1):
    for i in range(1, 5):
        b = f"tail_{i:02d}"
        if rig.has(b):
            P.rot(b, yaw(amp * syc(p, k, -0.1 * i)) @ pitch(-3))


def fold_wings(rig, P):
    for side, s in (("l", 1), ("r", -1)):
        if rig.has(f"wing_01_{side}"):
            P.rot(f"wing_01_{side}", yaw(s * 78) @ roll(s * 10))
            P.rot(f"wing_02_{side}", yaw(s * 70))
            P.rot(f"wing_03_{side}", yaw(-s * 40))


def multiped_idle(rig, P, p):
    s = rig.leg
    P.move("pelvis", (0.0, 0.0, -0.006 * s * (1 + cyc(p, 3))))
    for i in range(1, 5):
        if rig.has(f"spine_{i:02d}"):
            P.rot(f"spine_{i:02d}", pitch(0.8 * syc(p, 3)))
    for b, k in (("neck_01", 0.5), ("neck_02", 0.5)):
        if rig.has(b):
            P.rot(b, yaw(k * 22 * syc(p)) @ pitch(k * 10 * syc(p, 2, 0.2)))
    if rig.has("head"):
        P.rot("head", yaw(6 * syc(p, 3, 0.1)))
    tail(rig, P, p, 10, 2)
    for pos, side in leg_names(rig):
        P.rot(f"leg_{pos}_upper_{side}", pitch(1.5 * syc(p, 1, 0.3 if side == "l" else 0.8)))
    fold_wings(rig, P)


def multiped_attack(rig, P, t):
    wind, strike, rec = seg(t, 0.0, 0.3), seg(t, 0.3, 0.45), seg(t, 0.6, 1.0)
    k = strike * (1 - rec)
    for b in ("neck_01", "neck_02"):
        if rig.has(b):
            P.rot(b, pitch(12 * wind * (1 - k) - 22 * k))
    if rig.has("jaw"):
        P.rot("jaw", pitch(-30 * k - 10 * wind * (1 - rec)))
    for pos, side in leg_names(rig):
        if pos == "front":
            P.rot(f"leg_{pos}_upper_{side}", pitch(-10 * wind * (1 - k) + 22 * k))
        else:
            P.rot(f"leg_{pos}_upper_{side}", pitch(12 * wind * (1 - rec)))
            P.rot(f"leg_{pos}_lower_{side}", pitch(-20 * wind * (1 - rec)))
    P.move("pelvis", (0.0, -0.25 * rig.leg * k, -0.1 * rig.leg * wind * (1 - k)))
    fold_wings(rig, P)


def generic_hit(rig, P, t, base):
    e = env_hit(t)
    for b in base:
        if rig.has(b):
            P.rot(b, pitch(10 * e) @ yaw(8 * e))
    P.move(base[0] if base[0] != "root" else base[1], (0.0, 0.05 * rig.scale * e, 0.0))


def multiped_death(rig, P, t):
    """Legs give way and the body rolls onto its side."""
    fall = seg(t, 0.15, 0.7)
    buckle = seg(t, 0.0, 0.3)
    P.rot("pelvis", roll(-88 * fall))
    P.move("pelvis", (-0.35 * rig.leg * fall, 0.0, -(rig.leg * 0.25) * buckle - rig.leg * 0.45 * fall))
    for pos, side in leg_names(rig):
        P.rot(f"leg_{pos}_upper_{side}", pitch(18 * buckle * (1 - fall) + 10 * fall))
        P.rot(f"leg_{pos}_lower_{side}", pitch(-45 * buckle * (1 - fall) - 15 * fall))
    for b in ("neck_01", "neck_02"):
        if rig.has(b):
            P.rot(b, pitch(20 * fall) @ roll(-20 * fall))
    fold_wings(rig, P)


def flyer_fly(rig, P, p, glide=False):
    for side, s in (("l", 1), ("r", -1)):
        if not rig.has(f"wing_01_{side}"):
            continue
        if glide:
            a1, a2 = 4 * syc(p) - 6, 3 * syc(p, 1, 0.2)
        else:
            a1, a2 = 55 * cyc(p), 25 * cyc(p, 1, -0.12)
        P.rot(f"wing_01_{side}", roll(-s * a1))
        P.rot(f"wing_02_{side}", roll(-s * a2))
        P.rot(f"wing_03_{side}", roll(-s * a2 * 0.6) @ yaw(-s * (6 if glide else 12 * syc(p))))
    for pos, side in leg_names(rig):
        P.rot(f"leg_{pos}_upper_{side}", pitch(-65))
        P.rot(f"leg_{pos}_lower_{side}", pitch(-50))
    P.move("pelvis", (0.0, 0.0, (0.01 if glide else 0.05) * rig.leg * cyc(p, 1, 0.25)))
    tail(rig, P, p, 4)


def serpent(rig, P, p, amp=18, k=1.0, raise_head=0.0):
    n = sum(1 for b in rig.bones if b.startswith("spine_"))
    for i in range(1, n + 1):
        P.rot(f"spine_{i:02d}", yaw(amp * syc(p, k, -i / 6.0)))
    if raise_head:
        for i in range(max(1, n - 3), n + 1):
            P.rot(f"spine_{i:02d}", pitch(raise_head / 4))
    if rig.has("head"):
        P.rot("head", yaw(-amp * 0.6 * syc(p, k, -(n + 1) / 6.0)))


def cetacean_swim(rig, P, p, amp=12):
    for i in range(1, 5):
        if rig.has(f"tail_{i:02d}"):
            P.rot(f"tail_{i:02d}", pitch(amp * syc(p, 1, -0.12 * i)))
    for i in range(1, 6):
        if rig.has(f"spine_{i:02d}"):
            P.rot(f"spine_{i:02d}", pitch(amp * 0.15 * syc(p, 1, 0.1 * i)))
    for side, s in (("l", 1), ("r", -1)):
        if rig.has(f"fin_{side}"):
            P.rot(f"fin_{side}", roll(-s * amp * 0.8 * syc(p, 1, 0.25)))
        if rig.has(f"fluke_{side}"):
            P.rot(f"fluke_{side}", pitch(amp * 0.6 * syc(p, 1, -0.6)))
    P.move("root", (0.0, 0.0, 0.01 * rig.scale * cyc(p)))


def drone_pose(rig, P, p, move=0.0, scan=0.0, spin=4):
    h = rig.scale / 2
    P.move("body", (0.0, 0.0, 0.03 * h * syc(p)))
    P.rot("body", pitch(-15 * move) @ roll(2 * syc(p, 1, 0.3)))
    for i, b in enumerate(("rotor_fl", "rotor_fr", "rotor_bl", "rotor_br")):
        if rig.has(b):
            P.rot(b, yaw((1 if i in (0, 3) else -1) * 360.0 * spin * p))
    if rig.has("gun_yaw"):
        P.rot("gun_yaw", yaw(55 * scan * syc(p) + 6 * syc(p, 2)))
        P.rot("gun_pitch", pitch(8 * scan * syc(p, 2, 0.25)))


def hologram_pose(rig, P, p, talk=False):
    P.rot("core", yaw(360.0 * p))
    P.move("core", (0.0, 0.0, (0.03 if talk else 0.015) * rig.scale * syc(p, 4 if talk else 2)))
    for i in range(1, 7):
        b = f"ribbon_{i:02d}"
        if rig.has(b):
            P.rot(b, pitch((22 if talk else 12) * syc(p, 6 if talk else 2, i / 6.0)))


# --------------------------------------------------------------------------- animation sets
class Anim:
    def __init__(self, name, seconds, loop, fn, speed=0.0, locomotion=False, ground=False, lift=None):
        self.name, self.loop, self.fn, self.locomotion = name, loop, fn, locomotion
        self.ground, self.lift = ground, lift
        self.frames = max(6, int(round(seconds * FPS)))
        self.seconds = self.frames / FPS
        self.speed = speed * (seconds / self.seconds) if speed else 0.0  # keep speed exact after frame rounding


def humanoid_anims(rig):
    st = humanoid_style(rig)
    kind = st["kind"]
    names = HUMAN_SETS[kind]
    out = []
    sc = rig.scale
    for n in names:
        if n == "Idle":
            fn = (lambda P, p, st=st: crawler_idle(rig, P, p, st)) if st["crawler"] else (lambda P, p, st=st: human_idle(rig, P, p, st))
            out.append(Anim(n, 6.0 * math.sqrt(sc), True, fn, ground=True))
        elif n in GAITS:
            if st["crawler"]:
                T = (1.3 if n == "Walk" else 0.8) * math.sqrt(sc)
                stroke = 2 * (rig.bones["upperarm_l"].length + rig.bones["lowerarm_l"].length) * math.sin(math.radians(30 if n == "Run" else 24))
                out.append(Anim(n, T, True, lambda P, p, fast=(n == "Run"): crawler_move(rig, P, p, st, fast), stroke / (T / 2) * 100, True,
                                ground=True))
                continue
            g = human_gait(n, st, sc)
            hop = (0.05 if n == "Sprint" or st["runner"] else 0.03) * sc if g["flight"] else 0.0
            out.append(Anim(n, g["T"], True, lambda P, p, g=g: human_locomotion(rig, P, p, g, st), gait_speed(rig.leg, g) * 100, True,
                            ground=True, lift=(lambda p, h=hop: h * max(0.0, cyc(p, 2))) if hop else None))
        elif n == "Talk":
            out.append(Anim(n, 4.0, True, lambda P, p: human_talk(rig, P, p, st), ground=True))
        elif n == "Wave":
            out.append(Anim(n, 2.0, True, lambda P, p: human_wave(rig, P, p, st), ground=True))
        elif n == "HitReact":
            out.append(Anim(n, 0.6 * math.sqrt(sc), False, lambda P, t: human_hit(rig, P, t, st), ground=not st["crawler"]))
        elif n == "Death":
            out.append(Anim(n, 1.8 * math.sqrt(sc), False, lambda P, t: human_death(rig, P, t, st)))
        elif n == "Attack":
            fn = (lambda P, t: crawler_attack(rig, P, t, st)) if st["crawler"] else (lambda P, t: human_attack(rig, P, t, st))
            out.append(Anim(n, (1.4 if st["heavy"] else 1.1) * math.sqrt(sc), False, fn, ground=True))
    return out


def creature_anims(rig):
    t = rig.template
    sc = rig.scale
    out = []
    if t in ("quadruped", "hexapod", "flyer"):
        out.append(Anim("Idle", 5.0 * math.sqrt(max(sc, 0.1) / 0.55), True, lambda P, p: multiped_idle(rig, P, p), ground=True))
        gaits = ["Walk", "Trot", "Gallop"] if t == "quadruped" else (["Walk", "Trot"] if t == "hexapod" else ["Walk"])
        for n in gaits:
            g = multiped_gait(rig, n)
            spd = 4 * rig.leg * math.sin(math.radians(g["amp"])) / g["T"] * 100
            lift = (lambda p, h=g["bob"] * rig.leg: h * max(0.0, cyc(p, 2))) if n != "Walk" else None
            out.append(Anim(n, g["T"], True, lambda P, p, n=n, g=g: multiped_locomotion(rig, P, p, n, g, t == "flyer"), spd, True,
                            ground=True, lift=lift))
        if t == "flyer":
            span = rig.bones["wing_01_l"].length * 3 if rig.has("wing_01_l") else 0.5
            flap = max(0.2, 0.35 * math.sqrt(span))
            out.append(Anim("Fly", flap, True, lambda P, p: flyer_fly(rig, P, p), span * 800, True))
            out.append(Anim("Glide", 2.0, True, lambda P, p: flyer_fly(rig, P, p, glide=True), span * 900, True))
        out.append(Anim("Attack", 1.0 * math.sqrt(max(sc, 0.1) / 0.55), False, lambda P, t_: multiped_attack(rig, P, t_), ground=True))
        out.append(Anim("HitReact", 0.5, False, lambda P, t_: generic_hit(rig, P, t_, ["pelvis", "spine_02", "neck_01"]), ground=True))
        out.append(Anim("Death", 1.6, False, lambda P, t_: multiped_death(rig, P, t_)))
    elif t == "serpentine":
        T = 1.2 * math.sqrt(sc / 3)
        out.append(Anim("Idle", 4.0, True, lambda P, p: serpent(rig, P, p, 4, 1, raise_head=25)))
        out.append(Anim("Slither", T, True, lambda P, p: serpent(rig, P, p, 22, 1), sc * 0.45 / T * 100, True))
        out.append(Anim("Attack", 0.9, False, lambda P, t_: (serpent(rig, P, 0.0, 4, 1, raise_head=45 * seg(t_, 0, .3) * (1 - seg(t_, .3, .45))),
                                                              P.move("root", (0.0, -0.2 * sc * seg(t_, 0.3, 0.45) * (1 - seg(t_, 0.6, 1.0)), 0.0)))))
        out.append(Anim("HitReact", 0.5, False, lambda P, t_: generic_hit(rig, P, t_, ["root", "spine_06", "spine_09"])))
        out.append(Anim("Death", 1.6, False, lambda P, t_: serpent(rig, P, 0.25, 30 * seg(t_, 0, 1), 0.5)))
    elif t == "cetacean":
        T = 2.2 * math.sqrt(sc / 10)
        out.append(Anim("Idle", T * 2, True, lambda P, p: cetacean_swim(rig, P, p, 4)))
        out.append(Anim("Swim", T, True, lambda P, p: cetacean_swim(rig, P, p, 14), sc * 0.35 / T * 100, True))
        out.append(Anim("Sing", 6.0, True, lambda P, p: (cetacean_swim(rig, P, p, 3), P.rot("jaw", pitch(-6 - 8 * (1 - cyc(p, 2)))),
                                                         P.rot("head", pitch(6 * syc(p))))))
        out.append(Anim("HitReact", 0.8, False, lambda P, t_: generic_hit(rig, P, t_, ["root", "spine_02", "spine_04"])))
        out.append(Anim("Death", 3.0, False, lambda P, t_: (cetacean_swim(rig, P, 0.0, 2), P.rot("root", roll(160 * seg(t_, 0, 1))))))
    elif t == "drone":
        out.append(Anim("Idle", 2.0, True, lambda P, p: drone_pose(rig, P, p, spin=8)))
        out.append(Anim("Move", 1.0, True, lambda P, p: drone_pose(rig, P, p, move=1.0, spin=5), 600.0, True))
        out.append(Anim("Scan", 4.0, True, lambda P, p: drone_pose(rig, P, p, scan=1.0, spin=16)))
        out.append(Anim("HitReact", 0.4, False, lambda P, t_: (drone_pose(rig, P, 0.0, spin=0), P.rot("body", roll(25 * env_hit(t_))))))
        out.append(Anim("Death", 1.5, False, lambda P, t_: (P.move("body", (0.0, 0.0, -rig.scale * 0.45 * seg(t_, 0.1, 0.8) ** 2)),
                                                            P.rot("body", roll(120 * seg(t_, 0.0, 0.8)) @ pitch(-40 * seg(t_, 0.2, 0.9))))))
    elif t == "hologram":
        out.append(Anim("Idle", 6.0, True, lambda P, p: hologram_pose(rig, P, p)))
        out.append(Anim("Talk", 3.0, True, lambda P, p: hologram_pose(rig, P, p, talk=True)))
    return out


def anims_for(rig):
    return humanoid_anims(rig) if rig.template == "humanoid" else creature_anims(rig)


# --------------------------------------------------------------------------- writing actions
def action_name(asset, anim):
    stem = asset[3:] if asset.startswith("SK_") else asset
    return f"A_{stem}_{anim}"


def write_action(rig, anim):
    arm = rig.obj
    name = action_name(rig.asset, anim.name)
    old = bpy.data.actions.get(name)
    if old:
        bpy.data.actions.remove(old)
    act = bpy.data.actions.new(name)
    act.use_fake_user = True
    frames = anim.frames + 1 if anim.loop else anim.frames + 1
    rots, locs = {}, {}
    for f in range(frames):
        x = (f / anim.frames) % 1.0 if anim.loop else f / anim.frames
        if anim.loop and f == anim.frames:
            x = 0.0                                                    # close the loop exactly
        P = Pose()
        anim.fn(P, x)
        if anim.ground:
            rig.ground(P, anim.lift(x) if anim.lift else 0.0)
        for b, q in P.r.items():
            if b in rig.bones:
                rots.setdefault(b, [None] * frames)[f] = rig.local_rot(b, q)
        for b, v in P.t.items():
            if b in rig.bones:
                locs.setdefault(b, [None] * frames)[f] = rig.local_loc(b, v)
    step = 1 if anim.frames <= 24 else (2 if anim.frames <= 90 else 3)   # FBX export re-samples every frame
    keyed = sorted(set(range(0, frames, step)) | {frames - 1})

    def add_curve(path, index, group, values):
        fc = act.fcurves.new(path, index=index, action_group=group)
        if max(values) - min(values) < 1e-6:                             # constant channel: one key
            fc.keyframe_points.add(1)
            fc.keyframe_points.foreach_set("co", [0.0, values[0]])
        else:
            fc.keyframe_points.add(len(keyed))
            co = []
            for f in keyed:
                co += [float(f), values[f]]
            fc.keyframe_points.foreach_set("co", co)
            for kp in fc.keyframe_points:
                kp.interpolation = "LINEAR" if step == 1 else "BEZIER"
                kp.handle_left_type = kp.handle_right_type = "AUTO_CLAMPED"
        fc.update()

    for b, seq in rots.items():
        prev = None
        vals = []
        for q in seq:
            q = q.copy() if q is not None else Quaternion()
            if prev is not None:
                q.make_compatible(prev)
            vals.append(q)
            prev = q
        for i in range(4):
            add_curve(f'pose.bones["{b}"].rotation_quaternion', i, b, [q[i] for q in vals])
    for b, seq in locs.items():
        for i in range(3):
            add_curve(f'pose.bones["{b}"].location', i, b, [(v[i] if v is not None else 0.0) for v in seq])
    act.frame_range = (0, anim.frames)
    act["exo_anim"] = anim.name
    act["exo_loop"] = bool(anim.loop)
    act["exo_frames"] = anim.frames
    act["exo_fps"] = FPS
    act["exo_speed"] = round(anim.speed, 2)                           # cm/s ground speed of an in-place cycle (0 = none)
    act["exo_locomotion"] = bool(anim.locomotion)
    act["exo_template"] = rig.template
    return act


# --------------------------------------------------------------------------- build
def body_files(root):
    return sorted(p for p in (root / "assets" / "characters").rglob("*.blend")
                  if not any(t in p.name for t in ("_Outfit_", "_Hair_", "_Arms1P_")) and not p.name.startswith(("T_", "SM_")))


def open_body(path):
    bpy.ops.wm.open_mainfile(filepath=str(path))
    arm = bpy.data.objects.get("Armature")
    if not arm or arm.get("kind") not in BODY_KINDS:
        return None
    return arm


def strip_to_preview(arm):
    """Keep the rig and its LOD0 meshes (for previewing the animation); drop LOD1-3, references, cameras and sockets."""
    keep = {arm}
    for o in bpy.data.objects:
        if o.type == "MESH" and o.name.endswith("_LOD0") and not o.name.startswith(("REF_", "UCX_")):
            keep.add(o)
    for o in list(bpy.data.objects):
        if o not in keep:
            bpy.data.objects.remove(o, do_unlink=True)
    for c in list(bpy.data.collections):
        if not c.all_objects:
            bpy.data.collections.remove(c)
    bpy.data.orphans_purge(do_recursive=True)


def build_file(path, out_root):
    arm = open_body(path)
    if arm is None:
        return None
    rig = Rig(arm)
    anims = anims_for(rig)
    strip_to_preview(arm)
    for pb in arm.pose.bones:
        pb.rotation_mode = "QUATERNION"
    arm.animation_data_create()
    acts = [write_action(rig, a) for a in anims]
    arm.animation_data.action = acts[0]
    scene = bpy.context.scene
    scene.render.fps = FPS
    scene.frame_start, scene.frame_end = 0, anims[0].frames
    arm["exodus_anim_version"] = TOOL_VERSION
    arm["exodus_anims"] = json.dumps([a.name for a in anims])
    out = Path(out_root) / "assets" / "animations" / path.parent.name / f"{rig.asset}_Anims.blend"
    out.parent.mkdir(parents=True, exist_ok=True)
    bpy.ops.wm.save_as_mainfile(filepath=str(out), compress=True)
    for b in out.parent.glob(f"{out.stem}.blend1"):
        b.unlink()
    print(f"BUILT {rig.asset}: {', '.join(a.name for a in anims)} -> {out}")
    return out


# --------------------------------------------------------------------------- validate
EXPECTED = {"humanoid": {"Idle", "Walk", "HitReact", "Death"}, "quadruped": {"Idle", "Walk", "Trot", "Gallop", "Death"},
            "hexapod": {"Idle", "Walk", "Trot", "Death"}, "flyer": {"Idle", "Walk", "Fly", "Glide", "Death"},
            "serpentine": {"Idle", "Slither", "Death"}, "cetacean": {"Idle", "Swim", "Death"}, "drone": {"Idle", "Move", "Death"},
            "hologram": {"Idle", "Talk"}}


def pose_snapshot(arm, frame):
    bpy.context.scene.frame_set(frame)
    return {pb.name: (pb.head.copy(), pb.tail.copy()) for pb in arm.pose.bones}


def validate_scene():
    errors, warnings, info = [], [], []
    arm = bpy.data.objects.get("Armature")
    if not arm or "exodus_anim_version" not in arm.keys():
        return ["Not an EXODUS animation file (no Armature with exodus_anim_version)"], warnings, info
    rig = Rig(arm)
    names = json.loads(arm["exodus_anims"])
    acts = {n: bpy.data.actions.get(action_name(rig.asset, n)) for n in names}
    missing = EXPECTED.get(rig.template, set()) - set(names)
    if missing:
        errors.append(f"missing animations for a {rig.template}: {', '.join(sorted(missing))}")
    arm.animation_data_create()
    for n, act in acts.items():
        if act is None:
            errors.append(f"{n}: action {action_name(rig.asset, n)} not found")
            continue
        bad = [fc.data_path for fc in act.fcurves if fc.data_path.split('"')[1] not in rig.bones]
        if bad:
            errors.append(f"{n}: curves for unknown bones: {bad[:3]}")
        if any(math.isnan(k.co[1]) for fc in act.fcurves for k in fc.keyframe_points):
            errors.append(f"{n}: NaN keys")
        if not act.fcurves:
            errors.append(f"{n}: no keys")
            continue
        arm.animation_data.action = act
        last = int(act["exo_frames"])
        if act["exo_loop"]:
            a, b = pose_snapshot(arm, 0), pose_snapshot(arm, last)
            gap = max((a[k][1] - b[k][1]).length for k in a)
            if gap > 1e-3 * max(rig.scale, 0.1):
                errors.append(f"{n}: loop does not close (last frame differs by {gap * 100:.2f} cm)")
        if act["exo_locomotion"] and float(act["exo_speed"]) <= 0:
            errors.append(f"{n}: locomotion without a ground speed")
        # feet on the ground: humanoid and multiped locomotion and idles
        feet = [b for b in rig.bones if b.startswith(("foot_", "leg_")) and ("foot" in b)]
        if feet and rig.template in ("humanoid", "quadruped", "hexapod") and n in ("Idle", "Walk", "Jog", "Sprint", "Run", "Trot", "Gallop", "CrouchWalk") \
                and humanoid_style(rig)["kind"] != "crawler":
            lows = []
            for f in range(0, last + 1, max(1, last // 12)):
                snap = pose_snapshot(arm, f)
                lows.append(min(min(snap[b][0].z, snap[b][1].z) for b in feet))
            tol = 0.06 * max(rig.scale if rig.template == "humanoid" else rig.leg, 0.2)
            if min(lows) < -tol:
                errors.append(f"{n}: a foot goes {-min(lows) * 100:.1f} cm below the ground")
            if max(lows) > tol * 2.5 and n in ("Idle", "Walk", "CrouchWalk"):
                warnings.append(f"{n}: both feet leave the ground by {max(lows) * 100:.1f} cm")
        speed = float(act["exo_speed"])
        info.append(f"{n}: {last} frames" + (" loop" if act["exo_loop"] else "") + (f", {speed:.0f} cm/s" if speed else ""))
    bpy.context.scene.frame_set(0)
    return errors, warnings, info


def validate_file(path):
    bpy.ops.wm.open_mainfile(filepath=str(path))
    errors, warnings, info = validate_scene()
    status = "FAIL" if errors else ("WARN" if warnings else "PASS")
    print(f"\n== {status}: {path}")
    for tag, lines in (("info ", info), ("warn ", warnings), ("ERROR", errors)):
        for line in lines:
            print(f"   {tag} {line}")
    return not errors


# --------------------------------------------------------------------------- export
FBX_KW = dict(use_selection=True, object_types={"ARMATURE"}, apply_unit_scale=True, apply_scale_options="FBX_SCALE_UNITS",
              add_leaf_bones=False, use_armature_deform_only=False, primary_bone_axis="Y", secondary_bone_axis="X",
              axis_forward="-Z", axis_up="Y", bake_anim=True, bake_anim_use_all_bones=True, bake_anim_use_nla_strips=False,
              bake_anim_use_all_actions=False, bake_anim_force_startend_keying=True, bake_anim_step=1.0, bake_anim_simplify_factor=0.0)
# Compact: no tracks for bones the action never moves (the engine holds them in the bind pose) and redundant keys
# simplified away. About 5x smaller; a round trip stays within 1 cm of the full export on every joint.
FBX_COMPACT = dict(bake_anim_use_all_bones=False, bake_anim_simplify_factor=1.0)


def export_file(path, out_root, compact=False):
    bpy.ops.wm.open_mainfile(filepath=str(path))
    errors, _w, _i = validate_scene()
    if errors:
        raise SystemExit(f"Refusing to export {path}: validation errors:\n  " + "\n  ".join(errors))
    arm = bpy.data.objects["Armature"]
    rig = Rig(arm)
    out_dir = Path(out_root) / "export" / "animations" / Path(path).parent.name / rig.asset
    out_dir.mkdir(parents=True, exist_ok=True)
    for o in bpy.context.view_layer.objects:
        o.select_set(False)
    arm.select_set(True)
    bpy.context.view_layer.objects.active = arm
    manifest = {"asset": rig.asset, "template": rig.template, "fps": FPS, "anims": {}}
    scene = bpy.context.scene
    for n in json.loads(arm["exodus_anims"]):
        act = bpy.data.actions[action_name(rig.asset, n)]
        arm.animation_data.action = act
        scene.frame_start, scene.frame_end = 0, int(act["exo_frames"])
        fbx = out_dir / f"{act.name}.fbx"
        bpy.ops.export_scene.fbx(filepath=str(fbx), **dict(FBX_KW, **(FBX_COMPACT if compact else {})))
        manifest["anims"][n] = {"asset": act.name, "loop": bool(act["exo_loop"]), "frames": int(act["exo_frames"]),
                                "speed_cm_s": float(act["exo_speed"]), "locomotion": bool(act["exo_locomotion"])}
    (out_dir / f"{rig.asset}.anims.json").write_text(json.dumps(manifest, indent=1), encoding="utf-8")
    print(f"EXPORTED {rig.asset}: {len(manifest['anims'])} animations -> {out_dir}")
    return manifest


# --------------------------------------------------------------------------- CLI
def select(args, root):
    files = body_files(root)
    if args.asset:
        want = set(args.asset)
        files = [f for f in files if f.stem in want]
        missing = want - {f.stem for f in files}
        if missing:
            raise SystemExit(f"Unknown asset(s): {', '.join(sorted(missing))}")
    elif args.group:
        files = [f for f in files if f.parent.name in args.group]
    elif not args.all:
        raise SystemExit("Choose --all, --asset or --group")
    return files


def main(argv):
    ap = argparse.ArgumentParser(prog="exodus_animations")
    ap.add_argument("command", choices=["build", "validate", "export", "list"])
    ap.add_argument("files", nargs="*")
    ap.add_argument("--asset", nargs="+")
    ap.add_argument("--group", nargs="+", help="chapter folder(s) under assets/characters, e.g. story-cast")
    ap.add_argument("--all", action="store_true")
    ap.add_argument("--compact", action="store_true", help="export: drop unanimated bone tracks and simplify keys")
    ap.add_argument("--out", default=str(repo_root()))
    args = ap.parse_args(argv)
    root = repo_root()
    if args.command in ("build", "list"):
        n = 0
        for f in select(args, root) if (args.asset or args.group or args.all or args.command == "build") else body_files(root):
            if args.command == "list":
                arm = open_body(f)
                if arm is not None:
                    rig = Rig(arm)
                    print(f"{rig.asset:44s} {rig.template:10s} {', '.join(a.name for a in anims_for(rig))}")
                continue
            if build_file(f, args.out):
                n += 1
        if args.command == "build":
            print(f"Built {n} animation files")
        return 0
    if not args.files:
        raise SystemExit(f"{args.command} needs one or more _Anims.blend files")
    ok = True
    for f in args.files:
        if args.command == "validate":
            ok = validate_file(f) and ok
        else:
            export_file(f, args.out, args.compact)
    return 0 if ok else 1


if __name__ == "__main__":
    argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else sys.argv[1:]
    sys.exit(main(argv))
