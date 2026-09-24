# 11 — Animation & Performance Capture

## 11.1 Principles
1. **Weight and exhaustion.** People are tired, carrying too much and scared. Locomotion has weight shift and breath; nobody moves like an action hero until they have to.
2. **Hands tell the story.** Wrench fidgets with tools, Ada touches her wrist, Tug grips his thermos, Lily draws. Every story character has at least three signature idle "fidgets."
3. **Hollows are wrong, not fast** (except Runners): asymmetry, hitches, uncanny pauses, then sudden commitment.
4. **One skeleton, shared motion.** Everything humanoid is on EXO_Humanoid, so survivors, Hollows, units and the cast share locomotion, which is then layered with character-specific additives.

## 11.2 Shared animation sets (EXO_Humanoid)

| Set | Contents | Notes |
|---|---|---|
| **Locomotion** | Idle, walk, jog, sprint, crouch, prone, turn-in-place, starts and stops, 8-way strafes | Motion-matching database (~40 minutes of capture) |
| **Carry** | Carry-person (Tug in M0.03), carry-crate, drag-body | Two-person syncs |
| **Traversal** | Mantle 1 m and 2 m, ladder, vault, squeeze, crawl-duct | Environment-aligned |
| **Zero-G** | Drift idle, push-off, handhold grab, mag-boot walk, EVA tether | Captured on wires + keyframe polish |
| **Work** | Weld, grind, scan, type, repair (low/mid/high), carry-part, install | Tied to parts-bible `work` sockets |
| **Colony life** | Sit, eat, cook, sleep, shower, exercise, play music, draw, dance, chat (8 pairs), argue, hug, comfort, cry, laugh | Sims-pillar core; synced pair animations use relative alignment |
| **Combat** | Melee sets per weapon class, firearm upper-body layers, reload per weapon, throw, hit reactions, downed, revive | First-person set captured separately |
| **Emotes** | Wave, point, beckon, shrug, salute, fist-bump, Sunday toast | Used in barks and dinners |
| **Injury & infection** | Limp (Tug), arm-sling (Idris M1.03), frail (Mara), Stage 2–3 infected (shivers, veins itching), turning (Stage 4, 60 s) | Additive layers |

## 11.3 Character-specific sets

| Character | Signature motion |
|---|---|
| **Wrench** | Tool twirl idle, wrist-pad check, inspect-the-wrench, first-person hands for every tool |
| **Ada** | Pilot stillness, wrist-touch, cockpit set (seated in the buck), exo-frame duel (mocap + keyframe) |
| **Tug** | Limp locomotion, thermos sip, big-laugh, clamp-lever pull (M1.07) |
| **Lily** | Child locomotion (captured with a child performer, short sessions), drawing idle, vent crawl, hands-up walk (M3.05) |
| **Mara** | Glasses push, pacing, lab work, frail locomotion |
| **Idris** | Tactical walk, room-scan, dog-tag touch, cover set |
| **Oye** | Lean, die spin, prosthetic-hand tool changes |
| **Crane** | Bonsai pruning (broadcasts), boss phase sets (armored, graft, spectral) |
| **Sable** | Unhurried walk, tea ritual, head-tilt listening |
| **KESTREL** | Procedural: line speed, tilt, pulse on speech (no capture) |

## 11.4 Hollow motion library
- **Shambler:** 6 asymmetric shuffles, door-knock, lunge-grab, stumble, get-up, feed idle (non-gory: kneeling over a Bloom growth).
- **Runner:** sprint, quadrupedal charge, leap, wall-scramble, pack howl.
- **Crawler:** arm-drag crawl, vent crawl, ceiling drop, under-vehicle ambush.
- **Screamer:** inhale tell (0.8 s, must read at 20 m), shriek, retreat.
- **Bloater:** waddle, gag idle, burst.
- **Brute:** heavy walk, charge, wall-punch, ground-slam, stagger.
- **Drifter / Burrower / Mimic / Warden / Husk Titan:** see their cards in chapter 06.
- **Variation:** every Hollow animation gets 3 procedural offsets (lean, limp side, head tilt) so hordes never march in step.

## 11.5 Creature motion
- Tessari six-leg gait cycles (walk, trot) keyframed from a reference of large ungulates, then captured with a two-performer "costume" rig for weight.
- Earth fauna (dog, coyote, horse, crow, jackrabbit) are keyframed from reference footage; the dog gets a full pet set.
- Procedural Drift fauna use per-kit gait generators plus 12 authored behaviors each.

## 11.6 Performance capture plan

| Block | Days | Performers | Contents |
|---|---|---|---|
| Story scenes (face + body) | 42 | Cast of 12 + stand-ins | All in-engine scenes and 18 cinematics (game bible 19) |
| Pickups | 8 | Cast | After the vertical slice and alpha |
| Locomotion & colony life | 14 | 6 movement performers (mixed ages and builds) | Motion matching, colony interactions |
| Combat & first-person | 10 | Stunt team | Melee, firearms, first-person hands |
| Hollows | 8 | Movement artists (dance and physical theatre) | All Hollow sets |
| Child performer sessions | 6 half-days | Lily's performer + supervisor | Short sessions; no graphic content on set |
| Facial (ARKit capture for barks) | 10 | Voice cast | Bark lines and systemic dialogue with live facial |

- **Facial pipeline:** head-mounted camera solve to the ARKit 52 + EXODUS correctives on each Hero and Main head; barks use lighter phone-based ARKit capture.
- **Retargeting:** everything is captured on the 1.80 m reference skeleton and retargeted to each character's height and profile; child and brute profiles get dedicated correction passes.

## 11.7 Animation budgets
- In-engine story scenes: motion matching plus layered facial; no baked cameras.
- Cinematics: 24 minutes total at 30 fps capture; cleaned at 60 fps.
- Colony life: every interaction ≤ 8 s, loopable, with enter and exit transitions.
- Memory: animation compression targets 60% of raw for gameplay sets; cinematics streamed.
