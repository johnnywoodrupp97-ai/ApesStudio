"""EXODUS PROTOCOL — vertical slice planner (pure Python, no Unreal needed).

Turns the level bible's slice levels (SourceArt/levels: level cards + Blender marker exports) into
Content/Exodus/Data/slice_layout.json, which exodus_setup.py builds in Unreal:

  * terrain: a height grid over the slice of Kestrel Valley (same terrain function as the Blender
    level toolkit), flattened into pads under every mission space;
  * boxes: walled rooms with door gaps, connectors between nearby rooms, platforms and props,
    roads, and town / spaceport buildings filling the district footprints;
  * actors: player starts, triggers, spawners, horde zones, ladders, interactables, companions.

Coordinates: level-bible metres (+X east, +Y north, +Z up) are converted to Unreal centimetres
with UE = (x, -y, z) * 100, which keeps the map un-mirrored in Unreal's left-handed frame.

    python3 Content/Python/exodus_ue/planner.py            # writes Content/Exodus/Data/slice_layout.json
"""

import json
import math
import random
from pathlib import Path

HERE = Path(__file__).resolve()
PROJECT = HERE.parents[3]
LEVELS_DIR = PROJECT / "SourceArt" / "levels"
OUT = PROJECT / "Content" / "Exodus" / "Data" / "slice_layout.json"

# The slice (level-bible metres): Route 93 (x = -2 km) to Pad 39-K, Pad 12 to Mission Control.
SLICE_MIN = (-2200.0, -550.0)
SLICE_MAX = (1600.0, 1150.0)
STEP = 25.0
MISSION_LEVELS = ["KES-001", "KES-002", "KES-003", "KES-004", "KES-005", "KES-006"]
WALL = 0.3
DOOR_W, DOOR_H = 2.4, 2.6
OUTDOOR_WORDS = ("road", "lane", "pad", "fence", "apron", "street", "yard", "lot", "gate")
BRIDGE_WORDS = ("skywalk", "bridge", "catwalk", "mezzanine")
SKIP_WORDS = ("vent",)

CHAR = "/Game/Exodus/Imported/Characters/"


# --------------------------------------------------------------------------- helpers
def pascal(t):
    import re
    t = t.replace("×", "x").replace("&", "And").replace("'", "").replace("—", " ")
    return "".join(p[:1].upper() + p[1:] for p in re.split(r"[^0-9A-Za-z]+", t) if p)


def ue(x, y, z):
    """Level-bible metres -> Unreal centimetres."""
    return [round(x * 100.0, 1), round(-y * 100.0, 1), round(z * 100.0, 1)]


def ue_size(sx, sy, sz):
    return [round(sx * 100.0, 1), round(sy * 100.0, 1), round(sz * 100.0, 1)]


def smoothstep(e0, e1, x):
    t = max(0.0, min(1.0, (x - e0) / (e1 - e0)))
    return t * t * (3 - 2 * t)


def terrain_fn(lv):
    """Same function as tools/blender/exodus_levels.py (Kestrel Valley heightfield)."""
    s = lv["size"]
    w, d = s["w"], s["d"]
    t = lv.get("terrain") or {}
    rim = t.get("rim_height", 0)
    noise = t.get("floor_noise", s["h"] * 0.01)
    feats = t.get("features", [])

    def f(x, y):
        z = noise * (math.sin(x / 390.0) * math.cos(y / 510.0) + 0.5 * math.sin((x + y) / 170.0) + 0.25 * math.cos(x / 83.0 - y / 97.0))
        if rim:
            edge = min(w / 2 - abs(x), d / 2 - abs(y)) / (min(w, d) / 2)
            z += rim * (1 - smoothstep(0.0, 0.14, edge)) * (0.8 + 0.2 * math.sin(x / 700.0 + y / 900.0))
        for kind, fx, fy, fr, fh in feats:
            r = math.hypot(x - fx * 1000, y - fy * 1000) / (fr * 1000)
            if kind == "mesa":
                z += fh * (1 - smoothstep(0.85, 1.0, r))
            elif kind in ("hills", "basin"):
                z += fh * max(0.0, 1 - r) ** 2 * (1.0 if kind == "basin" else 0.7 + 0.3 * math.sin(x / 220.0) * math.cos(y / 260.0))
            elif kind == "flat":
                z *= smoothstep(0.7, 1.0, r)
        return z
    return f


class Rect:
    """Axis-aligned rectangle (min/max) in a 2D plane."""
    def __init__(self, a0, a1, b0, b1):
        self.a0, self.a1, self.b0, self.b1 = a0, a1, b0, b1

    def valid(self, eps=0.05):
        return self.a1 - self.a0 > eps and self.b1 - self.b0 > eps


def subtract(rect, holes):
    """Rectangle minus rectangular holes -> list of rectangles (grid decomposition on hole edges)."""
    a_cuts = sorted({rect.a0, rect.a1, *[min(max(h.a0, rect.a0), rect.a1) for h in holes], *[min(max(h.a1, rect.a0), rect.a1) for h in holes]})
    b_cuts = sorted({rect.b0, rect.b1, *[min(max(h.b0, rect.b0), rect.b1) for h in holes], *[min(max(h.b1, rect.b0), rect.b1) for h in holes]})
    out = []
    for i in range(len(a_cuts) - 1):
        for j in range(len(b_cuts) - 1):
            a0, a1, b0, b1 = a_cuts[i], a_cuts[i + 1], b_cuts[j], b_cuts[j + 1]
            ca, cb = (a0 + a1) / 2, (b0 + b1) / 2
            if any(h.a0 <= ca <= h.a1 and h.b0 <= cb <= h.b1 for h in holes):
                continue
            r = Rect(a0, a1, b0, b1)
            if r.valid():
                out.append(r)
    # merge vertical neighbours with identical a-range to keep the box count down
    merged = True
    while merged:
        merged = False
        for i in range(len(out)):
            for j in range(len(out)):
                if i != j and abs(out[i].a0 - out[j].a0) < 1e-6 and abs(out[i].a1 - out[j].a1) < 1e-6 and abs(out[i].b1 - out[j].b0) < 1e-6:
                    out[i] = Rect(out[i].a0, out[i].a1, out[i].b0, out[j].b1)
                    out.pop(j)
                    merged = True
                    break
            if merged:
                break
    return out


# --------------------------------------------------------------------------- the planner
class Planner:
    def __init__(self):
        data = json.loads((LEVELS_DIR / "slice_levels.json").read_text(encoding="utf-8"))
        self.levels = {lv["id"]: lv for lv in data["levels"]}
        self.markers = {}
        for f in LEVELS_DIR.glob("*.markers.json"):
            m = json.loads(f.read_text(encoding="utf-8"))
            self.markers[m["level_id"]] = m["markers"]
        self.valley = terrain_fn(self.levels["KVL-001"])
        self.boxes, self.actors = [], []
        self.pads = []        # (x0, x1, y0, y1, height) flattened areas (metres)
        self.level_base = {}  # level id -> (origin x, y, ground z)
        self.room_geo = {}    # (level, room name) -> dict
        self.rng = random.Random(2068)

    # ---- output helpers
    def box(self, name, cx, cy, z0, z1, sx, sy, style, yaw=0.0, shape="cube"):
        if z1 - z0 < 0.01 or sx < 0.01 or sy < 0.01:
            return
        self.boxes.append({"name": name, "center": ue(cx, cy, (z0 + z1) / 2), "size": ue_size(sx, sy, z1 - z0),
                           "yaw": round(-yaw, 2), "style": style, "shape": shape})

    def actor(self, cls, name, x, y, z, yaw=0.0, **props):
        self.actors.append({"class": cls, "name": name, "location": ue(x, y, z), "yaw": round(-yaw, 2), "props": props})

    # ---- terrain
    def ground(self, x, y):
        return self.valley(x, y)

    def height_at(self, x, y):
        """Terrain after pads and edge berms (metres)."""
        h = self.ground(x, y)
        for x0, x1, y0, y1, ph, blend in self.pads:
            dx = max(x0 - x, 0.0, x - x1)
            dy = max(y0 - y, 0.0, y - y1)
            d = math.hypot(dx, dy)
            if d <= 0:
                h = ph
            elif d < blend:
                t = smoothstep(0.0, blend, d)
                h = ph * (1 - t) + h * t
        # berms at the slice edge keep the player in the prototype area
        e = min(x - SLICE_MIN[0], SLICE_MAX[0] - x, y - SLICE_MIN[1], SLICE_MAX[1] - y)
        if e < 60:
            h += 30.0 * (1 - e / 60.0) ** 2
        return h

    def terrain(self):
        nx = int(round((SLICE_MAX[0] - SLICE_MIN[0]) / STEP)) + 1
        ny = int(round((SLICE_MAX[1] - SLICE_MIN[1]) / STEP)) + 1
        heights = []
        # UE grid: X = east (same), Y = -north. Row j runs along UE +Y, i.e. from north to south.
        for j in range(ny):
            y = SLICE_MAX[1] - j * STEP
            for i in range(nx):
                x = SLICE_MIN[0] + i * STEP
                heights.append(round(self.height_at(x, y) * 100.0, 1))
        return {"origin": [SLICE_MIN[0] * 100.0, -SLICE_MAX[1] * 100.0], "step": STEP * 100.0, "nx": nx, "ny": ny, "heights": heights}

    # ---- mission levels
    def rooms_of(self, lid):
        rooms = []
        for m in self.markers[lid]:
            if m["name"].startswith("VOL_Room_"):
                x, y, zc = m["location"]
                sx, sy, sz = m["size"]
                rooms.append({"name": m["name"][9:], "x": x, "y": y, "w": sx, "d": sy, "h": sz, "floor": zc - sz / 2})
        # snap near-ground floors to the ground so connected rooms share a floor (no 0.5 m steps)
        for r in rooms:
            if abs(r["floor"]) < 0.75:
                r["h"] += r["floor"]
                r["floor"] = 0.0
        return rooms

    def classify(self, r, rooms, connected):
        n = r["name"].lower()
        if any(w in n for w in SKIP_WORDS):
            return "skip"
        if n == "roof":
            return "roof"
        thin = min(r["w"], r["d"]) <= 1.5
        if thin and r["name"] in connected:
            return "opening"
        if thin or r["h"] <= 1.5:
            return "solid"
        if any(w in n for w in OUTDOOR_WORDS) and not any(w in n for w in ("hall", "room", "office", "house")):
            return "outdoor"
        # mostly inside a bigger room and not connected: a raised platform (e.g. Mission Control's back row)
        for o in rooms:
            if o is r or o["w"] * o["d"] <= r["w"] * r["d"]:
                continue
            ox = max(0.0, min(r["x"] + r["w"] / 2, o["x"] + o["w"] / 2) - max(r["x"] - r["w"] / 2, o["x"] - o["w"] / 2))
            oy = max(0.0, min(r["y"] + r["d"] / 2, o["y"] + o["d"] / 2) - max(r["y"] - r["d"] / 2, o["y"] - o["d"] / 2))
            if ox * oy >= 0.4 * r["w"] * r["d"] and r["name"] not in connected:
                # raised rows are platforms; ground-level blocks (the Wren's launch stack) are solid props
                return "platform" if r["floor"] > 0.3 else "solid"
        return "room"

    @staticmethod
    def inside(r, o, shrink=1.0):
        return abs(r["x"] - o["x"]) < o["w"] / 2 - shrink and abs(r["y"] - o["y"]) < o["d"] / 2 - shrink

    def mission_level(self, lid, extras):
        lv = self.levels[lid]
        px, py = lv["pos"][0] * 1000.0, lv["pos"][1] * 1000.0
        rooms = self.rooms_of(lid)
        by_name = {pascal(s["name"]): s for s in lv["spaces"]}
        conns = [(pascal(a), pascal(b), kind) for a, b, kind in lv["connections"]]
        connected = {a for a, _, _ in conns} | {b for _, b, _ in conns}
        g0 = self.ground(px, py)
        min_floor = min([r["floor"] for r in rooms if self.classify(r, rooms, connected) not in ("skip", "roof")] + [0.0])
        pad = g0 + min(0.0, min_floor)
        s = lv["size"]
        self.pads.append((px - s["w"] / 2 - 15, px + s["w"] / 2 + 15, py - s["d"] / 2 - 15, py + s["d"] / 2 + 15, pad, 25.0))
        self.level_base[lid] = (px, py, g0)
        R = {r["name"]: r for r in rooms}
        for r in rooms:
            r["kind"] = self.classify(r, rooms, connected)
            r["holes"] = {"N": [], "S": [], "E": [], "W": []}
            r["floor_holes"] = []

        # door gaps, connectors and ladders
        for a, b, kind in conns:
            A, B = R.get(a), R.get(b)
            if not A or not B or "skip" in (A["kind"], B["kind"]):
                continue
            if B["kind"] == "roof" or A["kind"] == "roof":
                low, roof = (A, B) if B["kind"] == "roof" else (B, A)
                self.roof_ladder(lid, low, roof, px, py, g0)
                continue
            if abs(A["floor"] - B["floor"]) > 1.0:
                self.ladder(lid, A, B, px, py, g0)
                continue
            if B["kind"] == "opening" or A["kind"] == "opening":
                opening, host = (B, A) if B["kind"] == "opening" else (A, B)
                side = self.facing_side(host, opening)
                along = opening["x"] if side in "NS" else opening["y"]
                width = max(opening["w"], opening["d"])
                host["holes"][side].append((along - width / 2, along + width / 2, host["floor"], host["floor"] + min(opening["h"], host["h"] - 0.5)))
                continue
            if "open" in kind:
                w_gap, h_gap = None, None
            else:
                w_gap, h_gap = (DOOR_W * 2 if "double" in kind or "hangar" in kind else DOOR_W), DOOR_H
            floor = max(A["floor"], B["floor"])
            if self.inside(B, A):
                self.cut_toward(B, A, w_gap, h_gap, floor)
            elif self.inside(A, B):
                self.cut_toward(A, B, w_gap, h_gap, floor)
            else:
                self.cut_between(lid, A, B, w_gap, h_gap, floor, px, py, g0)

        for name, side, offset, width in extras.get("openings", []):
            r = R[name]
            along = (r["x"] if side in "NS" else r["y"]) + offset
            r["holes"][side].append((along - width / 2, along + width / 2, r["floor"], r["floor"] + DOOR_H))

        for r in rooms:
            self.build_room(lid, r, rooms, px, py, g0, pad)
        return R

    @staticmethod
    def facing_side(host, other):
        dx, dy = other["x"] - host["x"], other["y"] - host["y"]
        # normalise by the host's half-size so the nearest wall wins
        if abs(dx) / max(host["w"], 0.1) >= abs(dy) / max(host["d"], 0.1):
            return "E" if dx > 0 else "W"
        return "N" if dy > 0 else "S"

    def cut_toward(self, inner, outer, w_gap, h_gap, floor):
        """Inner room inside another: cut the inner room's wall that faces the outer room's centre."""
        side = self.facing_side(inner, outer)
        along = inner["x"] if side in "NS" else inner["y"]
        w = w_gap or (inner["w"] if side in "NS" else inner["d"]) * 0.6
        h = h_gap or inner["h"] - 0.3
        inner["holes"][side].append((along - w / 2, along + w / 2, floor, floor + h))

    def cut_between(self, lid, A, B, w_gap, h_gap, floor, px, py, g0):
        """Two separate rooms: cut facing walls; bridge any gap between them with a short connector."""
        sa, sb = self.facing_side(A, B), self.facing_side(B, A)
        if sa in "NS":
            lo = max(A["x"] - A["w"] / 2, B["x"] - B["w"] / 2)
            hi = min(A["x"] + A["w"] / 2, B["x"] + B["w"] / 2)
            along = (lo + hi) / 2 if hi > lo else (A["x"] + B["x"]) / 2
            span = (hi - lo) if hi > lo else DOOR_W
        else:
            lo = max(A["y"] - A["d"] / 2, B["y"] - B["d"] / 2)
            hi = min(A["y"] + A["d"] / 2, B["y"] + B["d"] / 2)
            along = (lo + hi) / 2 if hi > lo else (A["y"] + B["y"]) / 2
            span = (hi - lo) if hi > lo else DOOR_W
        w = min(w_gap or span * 0.8, max(span - 0.6, 1.2))
        h = h_gap or min(A["h"], B["h"]) - 0.3
        A["holes"][sa].append((along - w / 2, along + w / 2, floor, floor + h))
        B["holes"][sb].append((along - w / 2, along + w / 2, floor, floor + h))
        # connector across the gap between the two walls
        if sa in "NS":
            ya = A["y"] + (A["d"] / 2 if sa == "N" else -A["d"] / 2)
            yb = B["y"] + (B["d"] / 2 if sb == "N" else -B["d"] / 2)
            gap = abs(yb - ya)
            if gap > 0.2:
                cy = (ya + yb) / 2
                self.connector(lid, px + along, py + cy, w + 2 * WALL, gap, g0 + floor, h, "NS")
        else:
            xa = A["x"] + (A["w"] / 2 if sa == "E" else -A["w"] / 2)
            xb = B["x"] + (B["w"] / 2 if sb == "E" else -B["w"] / 2)
            gap = abs(xb - xa)
            if gap > 0.2:
                cx = (xa + xb) / 2
                self.connector(lid, px + cx, py + along, gap, w + 2 * WALL, g0 + floor, h, "EW")

    def connector(self, lid, cx, cy, sx, sy, z0, h, axis):
        tag = f"{lid}_Connector_{len(self.boxes)}"
        self.box(tag + "_Floor", cx, cy, z0 - 0.3, z0, sx, sy, "floor")
        self.box(tag + "_Ceiling", cx, cy, z0 + h, z0 + h + 0.2, sx, sy, "ceiling")
        if axis == "NS":
            for s in (-1, 1):
                self.box(tag + f"_Side{s}", cx + s * (sx / 2 - WALL / 2), cy, z0, z0 + h, WALL, sy, "wall")
        else:
            for s in (-1, 1):
                self.box(tag + f"_Side{s}", cx, cy + s * (sy / 2 - WALL / 2), z0, z0 + h, sx, WALL, "wall")

    def ladder(self, lid, A, B, px, py, g0):
        """Floors more than 1 m apart: a ladder / stair interactable at each end (prototype traversal)."""
        low, high = (A, B) if A["floor"] < B["floor"] else (B, A)
        def spot(room, toward):
            # a point 1 m inside `room`, on the side facing `toward`
            side = self.facing_side(room, toward)
            x = min(max(toward["x"], room["x"] - room["w"] / 2 + 1.5), room["x"] + room["w"] / 2 - 1.5)
            y = min(max(toward["y"], room["y"] - room["d"] / 2 + 1.5), room["y"] + room["d"] / 2 - 1.5)
            if side == "E": x = room["x"] + room["w"] / 2 - 1.0
            if side == "W": x = room["x"] - room["w"] / 2 + 1.0
            if side == "N": y = room["y"] + room["d"] / 2 - 1.0
            if side == "S": y = room["y"] - room["d"] / 2 + 1.0
            if self.inside(room, toward) or self.inside(toward, room):
                x, y = room["x"] + (toward["x"] - room["x"]) * 0.3, room["y"] + (toward["y"] - room["y"]) * 0.3
            return x, y
        lx, ly = spot(low, high)
        hx, hy = spot(high, low)
        zl, zh = g0 + low["floor"], g0 + high["floor"]
        n = f"Ladder_{lid}_{low['name']}_{high['name']}"
        self.actor("ExoInteractableActor", n + "_Up", px + lx, py + ly, zl + 1.2, kind="Ladder", destination=ue(px + hx, py + hy, zh))
        self.actor("ExoInteractableActor", n + "_Down", px + hx, py + hy, zh + 1.2, kind="Ladder", destination=ue(px + lx, py + ly, zl))

    def roof_ladder(self, lid, low, roof, px, py, g0):
        top = roof["floor"] + roof["h"]
        lx, ly = low["x"], low["y"] - low["d"] / 2 + 1.0
        rx, ry = roof["x"], roof["y"]
        n = f"Ladder_{lid}_{low['name']}_Roof"
        self.actor("ExoInteractableActor", n + "_Up", px + lx, py + ly, g0 + low["floor"] + 1.2, kind="Ladder", destination=ue(px + rx, py + ry, g0 + top + 0.2))
        self.actor("ExoInteractableActor", n + "_Down", px + rx + 2, py + ry, g0 + top + 1.2, kind="Ladder", destination=ue(px + lx, py + ly, g0 + low["floor"]))

    def build_room(self, lid, r, rooms, px, py, g0, pad):
        kind = r["kind"]
        cx, cy = px + r["x"], py + r["y"]
        z0 = g0 + r["floor"]
        z1 = z0 + r["h"]
        name = f"{lid}_{r['name']}"
        if kind in ("skip", "opening", "roof"):
            return
        if kind == "solid":
            self.box(name + "_Solid", cx, cy, z0, z1, r["w"], r["d"], "prop")
            return
        if kind == "platform":
            self.box(name + "_Platform", cx, cy, z0 - 0.2, z0, r["w"], r["d"], "floor")
            self.box(name + "_Riser", cx, cy, g0 + min(0.0, r["floor"]), z0 - 0.2, r["w"], r["d"], "prop")
            return
        lname = r["name"].lower()
        if kind == "outdoor":
            if "fence" in lname:
                self.fence(name, cx, cy, z0, r)
            else:
                style = "road" if any(w in lname for w in ("road", "lane", "street", "apron")) else "pad"
                self.box(name + "_Ground", cx, cy, z0 - 0.4, z0 + 0.05, r["w"], r["d"], style)
            if r["floor"] - (pad - g0) > 0.5:
                self.box(name + "_Plinth", cx, cy, pad, z0 - 0.4, r["w"], r["d"], "plinth")
            return
        # a normal room: floor, walls with holes, ceiling
        self.box(name + "_Floor", cx, cy, z0 - 0.3, z0, r["w"], r["d"], "floor")
        nested = any(o is not r and o["kind"] == "room" and self.inside(r, o, 0.0) for o in rooms)
        bridge = any(w in lname for w in BRIDGE_WORDS)
        if r["floor"] - (pad - g0) > 0.5 and not nested:
            if bridge:
                for s in (-1, 1):
                    self.box(name + f"_Pillar{s}", cx + s * r["w"] * 0.3, cy, pad, z0 - 0.3, 1.0, 1.0, "plinth")
            else:
                self.box(name + "_Plinth", cx, cy, pad, z0 - 0.3, r["w"], r["d"], "plinth")
        self.box(name + "_Ceiling", cx, cy, z1, z1 + 0.25, r["w"] + 2 * WALL, r["d"] + 2 * WALL, "ceiling")
        for side in "NSEW":
            if side in "NS":
                wy = r["y"] + (r["d"] / 2 + WALL / 2) * (1 if side == "N" else -1)
                rect = Rect(r["x"] - r["w"] / 2 - WALL, r["x"] + r["w"] / 2 + WALL, r["floor"], r["floor"] + r["h"])
            else:
                wx = r["x"] + (r["w"] / 2 + WALL / 2) * (1 if side == "E" else -1)
                rect = Rect(r["y"] - r["d"] / 2, r["y"] + r["d"] / 2, r["floor"], r["floor"] + r["h"])
            holes = [Rect(a0, a1, b0, b1) for a0, a1, b0, b1 in r["holes"][side]]
            for i, piece in enumerate(subtract(rect, holes)):
                along = (piece.a0 + piece.a1) / 2
                length = piece.a1 - piece.a0
                if side in "NS":
                    self.box(f"{name}_Wall{side}{i}", px + along, py + wy, g0 + piece.b0, g0 + piece.b1, length, WALL, "wall")
                else:
                    self.box(f"{name}_Wall{side}{i}", px + wx, py + along, g0 + piece.b0, g0 + piece.b1, WALL, length, "wall")
        self.room_geo[(lid, r["name"])] = r

    def fence(self, name, cx, cy, z0, r):
        along_x = r["w"] >= r["d"]
        length = max(r["w"], r["d"])
        gate = 12.0
        for s in (-1, 1):
            seg = (length - gate) / 2
            off = s * (gate / 2 + seg / 2)
            if along_x:
                self.box(f"{name}_Fence{s}", cx + off, cy, z0, z0 + 2.4, seg, 0.15, "fence")
            else:
                self.box(f"{name}_Fence{s}", cx, cy + off, z0, z0 + 2.4, 0.15, seg, "fence")
        # the closed gate the troopers hold (M0.03): passable only after the standoff
        if along_x:
            self.box(f"{name}_Gate", cx, cy, z0, z0 + 2.4, gate, 0.15, "fence")
        else:
            self.box(f"{name}_Gate", cx, cy, z0, z0 + 2.4, 0.15, gate, "fence")

    # ---- markers
    def level_point(self, lid, x, y, z):
        px, py, g0 = self.level_base[lid]
        return px + x, py + y, g0 + z

    def markers_for(self, lid, spawners):
        for m in self.markers[lid]:
            n = m["name"]
            x, y, z = self.level_point(lid, *m["location"])
            if n.startswith("PS_"):
                self.actor("ExoMarker", n, x, y, z + 0.1, kind="PS")
            elif n.startswith("CAM_"):
                self.actor("ExoMarker", n, x, y, z, kind="CAM")
            elif n.startswith("TRG_"):
                sx, sy, sz = m.get("size") or (4, 4, 3)
                self.actor("ExoMissionTrigger", n, x, y, z, extent=ue_size(sx / 2, sy / 2, sz / 2))
            elif n.startswith("HS_"):
                sx, sy, sz = m.get("size") or (20, 20, 5)
                self.actor("ExoHordeZone", n, x, y, z, extent=ue_size(sx / 2, sy / 2, sz / 2))
            elif n.startswith("SP_"):
                spec = spawners.get(n, {})
                self.actor("ExoSpawner", n, x, y, z + 0.1, **spec)
            elif n.startswith(("POI_", "LM_")):
                self.actor("ExoMarker", n, x, y, z, kind=n.split("_")[0])

    def extras(self, lid, spec):
        for name, x, y, z0, z1, sx, sy, style, shape in spec.get("boxes", []):
            wx, wy, wz = self.level_point(lid, x, y, 0.0)
            self.box(f"{lid}_{name}", wx, wy, wz + z0, wz + z1, sx, sy, style, 0.0, shape)
        for it in spec.get("actors", []):
            it = dict(it)
            cls, name = it.pop("class"), it.pop("name")
            x, y, z = self.level_point(lid, *it.pop("at"))
            yaw = it.pop("yaw", 0.0)
            if "destination" in it:
                it["destination"] = ue(*self.level_point(lid, *it["destination"]))
            if "extent_m" in it:
                it["extent"] = ue_size(*it.pop("extent_m"))
            if cls == "ExoCompanion":  # characters are placed by their capsule centre
                z += it.get("height_cm", 180.0) / 200.0 + 0.05
            self.actor(cls, name, x, y, z, yaw, **it)

    # ---- the open world around the missions
    def overlaps_mission(self, x, y, w, d, margin=12.0):
        for lid in MISSION_LEVELS:
            lv = self.levels[lid]
            px, py = lv["pos"][0] * 1000, lv["pos"][1] * 1000
            s = lv["size"]
            if abs(x - px) < (w + s["w"]) / 2 + margin and abs(y - py) < (d + s["d"]) / 2 + margin:
                return True
        return False

    def building(self, name, x, y, w, d, h, style="building", shape="cube", yaw=0.0):
        if self.overlaps_mission(x, y, w, d):
            return False
        if not (SLICE_MIN[0] + 40 < x < SLICE_MAX[0] - 40 and SLICE_MIN[1] + 40 < y < SLICE_MAX[1] - 40):
            return False
        g = min(self.height_at(x + dx, y + dy) for dx in (-w / 2, w / 2) for dy in (-d / 2, d / 2))
        self.box(name, x, y, g - 2.0, g + h, w, d, style, yaw, shape)
        return True

    def districts(self):
        rng = self.rng
        # Kestrel Township (KVL-003)
        tx, ty = -900.0, 100.0
        # Main Street: shops both sides
        for i in range(-6, 7):
            for s in (-1, 1):
                self.building(f"Township_Shop_{i}_{s}", tx + i * 30, ty + s * 26, 22, 14, rng.choice([5, 6, 7, 8]))
        # suburbs: 3 blocks of houses south-east of Main Street
        sx0, sy0 = tx + 100, ty - 300
        for bi in range(-7, 8):
            for bj in range(-6, 7):
                if bi % 4 == 0 or bj % 4 == 0:
                    continue  # streets
                self.building(f"Township_House_{bi}_{bj}", sx0 + bi * 30, sy0 + bj * 28, 12, 10, rng.choice([4, 5, 6]), "house")
        # warehouse district
        for i in range(3):
            for j in range(2):
                self.building(f"Township_Warehouse_{i}_{j}", tx + 230 + i * 60, ty + 200 + j * 70, 40, 30, 10, "industrial")
        # library and skate park
        self.building("Township_Library", tx - 300, ty - 150, 30, 20, 8)
        self.building("Township_WaterTower", tx - 120, ty + 90, 6, 6, 28, "tower", "cylinder")
        # Kestrel Aerospace Complex (KVL-002)
        cx, cy = 1000.0, 300.0
        for i in range(-3, 4):
            self.building(f"Complex_Hangar_{i}", cx - 300 + i * 85, cy + 200, 60, 40, 18, "industrial")
        for i in range(6):
            self.building(f"Complex_FuelTank_{i}", cx - 640 + (i % 3) * 40, cy - 520 + (i // 3) * 40, 22, 22, 14, "tank", "cylinder")
        for i in range(3):
            self.building(f"Complex_Substation_{i}", cx + 690 + i * 40, cy + 100, 20, 20, 8, "industrial")
        self.building("Complex_MissionControlTower", 1300.0, 945.0, 30, 30, 45, "tower")
        self.building("Complex_Vault", cx - 100, cy + 600, 60, 60, 12, "bunker")
        # Pad 39-K launch tower (the valley's landmark, 110 m) and its pad deck
        self.building("Pad39K_Deck", 1500.0, -200.0, 80, 80, 2, "pad")
        self.building("Pad39K_Tower", 1500.0, -175.0, 20, 20, 110, "tower")
        self.building("Pad39K_Wren", 1500.0, -200.0, 8, 8, 40, "rocket", "cylinder")

    def roads(self):
        # Route 93 (north-south) and the spur through the Township to the Complex
        paths = [
            [(-2000.0, SLICE_MIN[1] + 60), (-2000.0, SLICE_MAX[1] - 60)],
            [(-2000.0, 100.0), (-1300.0, 100.0), (-500.0, 100.0), (150.0, 300.0), (650.0, 440.0), (1200.0, 520.0)],
            [(650.0, 440.0), (750.0, -150.0), (900.0, -250.0), (1450.0, -250.0)],
        ]
        for pi, pts in enumerate(paths):
            for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
                length = math.hypot(x1 - x0, y1 - y0)
                n = max(1, int(length // 25))
                yaw = math.degrees(math.atan2(y1 - y0, x1 - x0))
                for k in range(n):
                    ax = x0 + (x1 - x0) * k / n
                    ay = y0 + (y1 - y0) * k / n
                    bx = x0 + (x1 - x0) * (k + 1) / n
                    by = y0 + (y1 - y0) * (k + 1) / n
                    mx, my = (ax + bx) / 2, (ay + by) / 2
                    if self.overlaps_mission(mx, my, 8, 8, margin=0.0):
                        continue
                    h = max(self.height_at(ax, ay), self.height_at(bx, by), self.height_at(mx, my))
                    self.box(f"Road_{pi}_{k}_{int(x0)}", mx, my, h - 0.6, h + 0.12, length / n + 1.0, 8.0, "road", yaw)

    # ---- run
    def run(self, extras):
        for lid in MISSION_LEVELS:
            self.mission_level(lid, extras.get(lid, {}))
        for lid in MISSION_LEVELS:
            self.markers_for(lid, extras.get(lid, {}).get("spawners", {}))
            self.extras(lid, extras.get(lid, {}))
        # valley POIs inside the slice sit on the terrain
        for m in self.markers["KVL-001"]:
            x, y, _ = m["location"]
            if m["name"].startswith(("POI_", "LM_")) and SLICE_MIN[0] < x < SLICE_MAX[0] and SLICE_MIN[1] < y < SLICE_MAX[1]:
                self.actor("ExoMarker", m["name"], x, y, self.height_at(x, y) + 1.0, kind=m["name"].split("_")[0])
        self.districts()
        self.roads()
        terrain = self.terrain()
        # a PlayerStart at the Cold Open, and a nav volume over the whole slice
        cold = next(a for a in self.actors if a["name"] == "PS_ColdOpen")
        start = [cold["location"][0], cold["location"][1], cold["location"][2] + 100.0]  # capsule centre, not feet
        self.actors.append({"class": "PlayerStart", "name": "PlayerStart_ColdOpen", "location": start, "yaw": cold["yaw"], "props": {}})
        zmax = max(terrain["heights"]) + 15000
        self.actors.append({"class": "NavMeshBoundsVolume", "name": "Nav_Slice",
                            "location": [(SLICE_MIN[0] + SLICE_MAX[0]) * 50.0, -(SLICE_MIN[1] + SLICE_MAX[1]) * 50.0, (min(terrain["heights"]) + zmax) / 2],
                            "yaw": 0.0, "props": {"size": [(SLICE_MAX[0] - SLICE_MIN[0]) * 100.0, (SLICE_MAX[1] - SLICE_MIN[1]) * 100.0, zmax - min(terrain["heights"]) + 2000]}})
        return {"schema": "exodus.slice_layout/1", "units": "cm", "note": "Generated by Content/Python/exodus_ue/planner.py; do not edit by hand.",
                "slice_m": {"min": SLICE_MIN, "max": SLICE_MAX}, "terrain": terrain, "boxes": self.boxes, "actors": self.actors}


def main():
    from slice_extras import EXTRAS  # noqa: E402  (same folder)
    layout = Planner().run(EXTRAS)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(layout, separators=(",", ":")), encoding="utf-8")
    t = layout["terrain"]
    print(f"slice_layout.json: terrain {t['nx']}x{t['ny']}, {len(layout['boxes'])} boxes, {len(layout['actors'])} actors -> {OUT}")


if __name__ == "__main__":
    import sys
    sys.path.insert(0, str(HERE.parent))
    main()
