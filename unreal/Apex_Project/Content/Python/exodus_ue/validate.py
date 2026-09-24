"""Cross-check missions.json against slice_layout.json and animations.json: every marker, group, event target,
action and animation clip exists, and every character mesh in the layout has an animation set.

Run from anywhere (pure Python):  python3 Content/Python/exodus_ue/validate.py
Exits with code 1 on any error, so it can run in CI next to the planner.
"""
import json
import sys
from pathlib import Path

DATA = Path(__file__).resolve().parents[2] / "Exodus" / "Data"
ACTIONS = {"say", "teleport", "checkpoint", "activate", "give", "survival", "input", "follow", "place", "infect",
           "time", "hordes", "horde", "title", "flag", "hide", "anim"}
EVENTS = {"trigger", "interact", "built", "killed", "night_survived", "dialogue_done", "time", "none"}
PARTS = {"STR-017", "DEF-001", "DEF-002", "STR-001", "DOR-001", "PRD-001", "PWR-001", "UTL-001", "COL-001"}
KILL_TYPES = {"Shambler", "Runner", "Crawler"}


def main():
    layout = json.loads((DATA / "slice_layout.json").read_text(encoding="utf-8"))
    missions = json.loads((DATA / "missions.json").read_text(encoding="utf-8"))
    anim_sets = json.loads((DATA / "animations.json").read_text(encoding="utf-8"))["characters"]
    actors = layout["actors"]
    markers = {a["props"].get("marker_name", a["name"]) for a in actors if a["class"] in ("ExoMarker", "ExoMissionTrigger")}
    triggers = {a["props"].get("marker_name", a["name"]) for a in actors if a["class"] == "ExoMissionTrigger"}
    interact = {a["props"].get("marker_name", a["name"]) for a in actors if a["class"] == "ExoInteractableActor"}
    groups = {a["props"]["group"] for a in actors if a["props"].get("group")}
    companions = {a["props"]["companion_id"] for a in actors if a["class"] == "ExoCompanion"}
    stories = {a["props"]["story_id"] for a in actors if a["class"] == "ExoSpawner" and a["props"].get("story_id")}
    companion_mesh = {a["props"]["companion_id"]: a["props"]["mesh_asset"].rsplit("/", 1)[-1] for a in actors if a["class"] == "ExoCompanion"}
    errors = []
    # Every character in the layout (companions, spawners) and every horde mesh in ExoGameMode.cpp needs clips.
    meshes = {a["props"]["mesh_asset"].rsplit("/", 1)[-1] for a in actors if a["props"].get("mesh_asset")}
    for mesh in sorted(meshes | {"SK_ENM_Shambler", "SK_ENM_Runner"}):
        clips = anim_sets.get(mesh, {}).get("anims", {})
        if not clips:
            errors.append(f"animations: no animation set for {mesh} (run SourceArt/export_slice_art.py -- anims)")
        elif "Idle" not in clips or not any(c["locomotion"] and c["speed_cm_s"] > 0 for c in clips.values()):
            errors.append(f"animations: {mesh} needs an Idle and a locomotion cycle with a ground speed")
    ids = set()
    steps = 0
    for m in missions["missions"]:
        for s in m["steps"]:
            steps += 1
            where = f"{m['id']}/{s['id']}"
            if s["id"] in ids:
                errors.append(f"{where}: duplicate step id")
            ids.add(s["id"])
            for a in s.get("on_start", []):
                do = a.get("do")
                if do not in ACTIONS:
                    errors.append(f"{where}: unknown action {do}")
                if "marker" in a and a["marker"] not in markers:
                    errors.append(f"{where}: {do} -> no marker {a['marker']}")
                if do in ("activate", "hide") and a["group"] not in groups:
                    errors.append(f"{where}: {do} -> no group {a['group']}")
                if do in ("follow", "place", "anim") and a["companion"] not in companions:
                    errors.append(f"{where}: {do} -> no companion {a['companion']}")
                if do == "anim" and a["companion"] in companion_mesh:
                    mesh = companion_mesh[a["companion"]]
                    if a.get("anim") not in anim_sets.get(mesh, {}).get("anims", {}):
                        errors.append(f"{where}: anim -> {mesh} has no clip {a.get('anim')}")
                if do == "say":
                    for line in a["lines"]:
                        if len(line) != 2 or not line[1]:
                            errors.append(f"{where}: bad say line {line}")
            done = s.get("complete", {})
            ev, tgt = done.get("event", "none"), done.get("target", "")
            if ev not in EVENTS:
                errors.append(f"{where}: unknown event {ev}")
            elif ev == "trigger" and tgt not in triggers:
                errors.append(f"{where}: no trigger {tgt}")
            elif ev == "interact" and tgt not in interact:
                errors.append(f"{where}: no interactable {tgt}")
            elif ev == "built" and tgt not in PARTS:
                errors.append(f"{where}: {tgt} is not a slice part")
            elif ev == "killed" and tgt and tgt not in stories | KILL_TYPES:
                errors.append(f"{where}: nothing can be killed as {tgt}")
            elif ev == "dialogue_done" and not any(a.get("do") == "say" for a in s.get("on_start", [])):
                errors.append(f"{where}: dialogue_done without any say")
    names = [a["name"] for a in actors]
    for n in {n for n in names if names.count(n) > 1}:
        errors.append(f"layout: duplicate actor name {n}")
    for e in errors:
        print("ERROR", e)
    print(f"{steps} steps, {len(actors)} actors, {len(markers)} markers, {len(groups)} groups: "
          f"{'PASS' if not errors else f'{len(errors)} error(s)'}")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
