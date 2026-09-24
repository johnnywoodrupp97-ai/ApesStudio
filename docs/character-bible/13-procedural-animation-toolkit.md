# 13 — Procedural Animation Toolkit

> `tools/blender/exodus_animations.py` generates a greybox animation set for every character body from its rig, checks it, and exports it for the engine. Tested with Blender 4.2 (the `bpy` 4.2 module). These are **placeholder** animations: they let every character move in engine from day one, until the capture sets in [chapter 11](11-animation-and-performance-capture.md) replace them.

**Every body is already animated.** `assets/animations/` holds a validated `<asset>_Anims.blend` for all **93** character bodies (every Base and Variant file in `assets/characters/`), **93 / 93 PASS**.

## 13.1 Pipeline

```
 assets/characters/<chapter>/<asset>.blend      (rig + LOD0 body, never modified)
        │  exodus_animations.py build
        ▼
 assets/animations/<chapter>/<asset>_Anims.blend  (rig + LOD0 preview + one action per clip)
        │  exodus_animations.py validate   (loop closure, feet on the ground, bones, keys)
        ▼
 exodus_animations.py export [--compact]  →  export/animations/<chapter>/<asset>/A_<name>_<Clip>.fbx  +  <asset>.anims.json
```

The character files are never touched, so rebuilding a character never loses its animations: re-run `build` to refit the set to a changed rig.

## 13.2 Commands
Run from the repository root.

| Task | Command |
|---|---|
| **Build every body** (about 2 min) | `blender -b -P tools/blender/exodus_animations.py -- build --all` |
| Build some assets / a chapter | `… -- build --asset SK_CHR_TugBrennan SK_ENM_Runner` · `… -- build --group story-cast` |
| Validate | `… -- validate assets/animations/story-cast/SK_CHR_TugBrennan_Anims.blend` |
| Export (validates first) | `… -- export assets/animations/story-cast/SK_CHR_TugBrennan_Anims.blend` |
| Export for the engine, about 5× smaller | add `--compact` |
| List every body with its template and clips | `… -- list` |

Also runs with the stand-alone `bpy` module: `python tools/blender/exodus_animations.py build --all`.

## 13.3 Animation sets

Every clip is computed from the rig itself (bone lengths, height, proportion profile), so one set of rules serves all 93 bodies. Bigger bodies step slower (cycle time scales with √height).

| Template / style | Bodies | Clips |
|---|---|---|
| Humanoid: survivor and soldier | 42 | Idle, Walk, Jog, Sprint, CrouchWalk, Talk, Wave, HitReact, Death (Directorate soldiers keep a rifle-ready upper body) |
| Humanoid: Hollow, Crawler, heavy | 22 | Idle, Walk, Run, Attack, HitReact, Death |
| Quadruped | 15 | Idle, Walk, Trot, Gallop, Attack, HitReact, Death |
| Hexapod (tripod gait) | 4 | Idle, Walk, Trot, Attack, HitReact, Death |
| Flyer | 3 | Idle, Walk, Fly, Glide, Attack, HitReact, Death |
| Serpentine | 1 | Idle, Slither, Attack, HitReact, Death |
| Cetacean | 1 | Idle, Swim, Sing, HitReact, Death |
| Drone | 1 | Idle, Move, Scan, HitReact, Death |
| Hologram | 4 | Idle, Talk |

**Character touches** (from [11.3](11-animation-and-performance-capture.md#113-character-specific-sets)):
- Tug limps on his right leg.
- Lily moves with a child's cadence.
- Elders stoop, and Mara leans with a frail gait.
- Every Hollow gets its own limp side, forward lean, head tilt and dropped shoulder, seeded from its asset name so they stay the same on every rebuild.
- Crawlers drag themselves along on their arms.
- Heavies attack with an overhead slam.

## 13.4 Conventions

| Item | Rule |
|---|---|
| Action name | `A_<asset without SK_>_<Clip>`, e.g. `A_CHR_TugBrennan_Walk` |
| Frame rate | 30 fps. Loops close exactly (the last frame equals the first) |
| Locomotion | **In place**. Each cycle records its ground speed as `exo_speed` (cm/s at play rate 1), so the engine scales the play rate to the character's actual speed and the feet don't slide |
| Grounding | A forward-kinematics pass puts the lowest foot contact on the floor on every frame of Idle, the gaits, Talk, Wave, HitReact and Attack |
| Custom properties per action | `exo_anim`, `exo_loop`, `exo_frames`, `exo_fps`, `exo_speed`, `exo_locomotion`, `exo_template` |

## 13.5 Validation rules
- Every clip the template expects is present, and every action exists and has keys.
- No curve targets a bone the rig does not have, and no key is NaN.
- Looping clips close: the last frame matches the first to within 1 mm, scaled to the body's size.
- Locomotion clips have a ground speed.
- On humanoids, quadrupeds and hexapods, the feet stay within tolerance of the ground in Idle and the gaits. A warning is raised if both feet leave the ground in Idle, Walk or CrouchWalk.

## 13.6 Export
`export` writes one FBX per clip: the armature only, baked at every frame, with the same bone axes and unit scale as the character FBX from [chapter 12](12-blender-character-toolkit.md#125-export). It also writes `<asset>.anims.json`, which lists each clip's loop flag, length in frames and ground speed.

`--compact` makes the files about 5× smaller: it drops tracks for bones a clip never moves (the engine holds them in the bind pose) and simplifies redundant keys. In a round trip, every joint of a compact clip stays within 1 cm of the full export.

## 13.7 In Unreal (vertical slice)
The slice's 14 characters use these sets. See the [Apex_Project README](../../unreal/Apex_Project/README.md).
- `blender -b -P unreal/Apex_Project/SourceArt/export_slice_art.py -- anims` exports their 105 clips (compact) to `SourceArt/Animations/<mesh>/` and writes `Content/Exodus/Data/animations.json`.
- On the first editor start, `exodus_setup.py` imports the clips onto each character's skeleton.
- `UExoAnimComponent` plays them on companions and Hollows, with no Animation Blueprint:
  - Idle, or Talk while the companion is speaking;
  - the gait closest to the character's speed, with the play rate matched to that speed;
  - Attack, HitReact, Death and Wave as one-shots on top.
