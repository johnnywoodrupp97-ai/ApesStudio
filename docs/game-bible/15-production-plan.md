# 15 — Production Plan

> A realistic path from idea to a shippable 12-hour game. Timelines assume a focused indie team (see §15.4); scale accordingly.

## 15.1 Scope strategy
The three inspirations are each huge games. We stay shippable by:
1. **Launching with one hand-crafted solar system + ~60 procedural systems**, not an infinite galaxy.
2. **Capping colony size at 40** and using LOD simulation for off-screen survivors.
3. **~220 blocks, 24 weapons, 14 Hollow types, 48 traits, 80 events** at launch — enough variety, not bloat.
4. **Single-player first**, co-op-ready architecture, co-op as a free update.
5. **Reusing the block system everywhere** — bases, ships, turrets, furniture and even story set pieces are grids.

## 15.2 Milestones

| # | Milestone | Duration | Exit criteria |
|---|---|---|---|
| **M0** | **Concept & Bible** | 1 month | This bible approved; pillars locked; engine chosen |
| **M1** | **Core Prototypes** | 3 months | Gray-box: (a) block building + power + rooms, (b) 5 survivors with needs & utility AI, (c) Hollow horde vs. walls, (d) planet → orbit flight on one voxel planet |
| **M2** | **Vertical Slice** | 4 months | Prologue + M1.01–M1.02 at near-final quality: Kestrel hangar, first horde, rescue Lily. Proves tone, horror, building and colony warmth together |
| **M3** | **First Playable (Acts I–II)** | 6 months | Earth → Haven-9 → Moon playable end to end with placeholder art where needed |
| **M4** | **Alpha (content complete)** | 8 months | All four acts playable, all systems in, all endings reachable |
| **M5** | **Beta** | 4 months | Content final, balancing, performance, localization, accessibility, closed playtests |
| **M6** | **Early Access (optional) / Launch** | — | Certification, launch marketing |
| **Total** | | **~26 months** to 1.0 (+ optional Early Access after M3 or M4) | |

### Early Access option
Ship **Acts I–II + Survival Sandbox** in Early Access after M3 (≈ 14 months in) to fund development and gather building/colony feedback. Acts III–IV and endings follow in 1.0.

## 15.3 Vertical slice definition (M2)
- **Length:** 45–60 minutes.
- **Content:** M0.01–M0.03, M1.01, M1.02 (Township + school + Lily).
- **Must prove:**
  - Horror atmosphere in the dark spaceport.
  - Building a fortification that visibly holds (or fails) under a horde.
  - Lily feels like a person within 10 minutes of meeting her (needs, barks, a small moment at the campfire).
  - Infection meter creates tension without frustration.
- **Success test:** 8/10 external playtesters want to keep playing; ≥ 6/10 remember Lily's name a week later.

## 15.4 Team (core, for ~26-month plan)

| Discipline | Headcount | Notes |
|---|---|---|
| Creative / Game Director | 1 | Owns the bible |
| Producer | 1 | |
| Game Designers | 3 | Systems (building/survival), Colony sim, Missions/levels |
| Narrative | 2 | Lead writer + writer/narrative designer |
| Engineers | 6 | Engine/voxel, gameplay, AI (colony + hordes), tools, UI, platform/save |
| Artists | 6 | Art director, environment ×2, character, props/blocks, VFX/tech art |
| Animator | 1–2 | + mocap outsourcing |
| Audio | 1 + outsourced | Sound design & music |
| QA | 2 + outsourced | |
| **Total core** | **~24** | Scale down (and cut scope per §15.6) for smaller teams |

## 15.5 Top risks & mitigations

| Risk | Impact | Mitigation |
|---|---|---|
| Scope creep from three big genres | High | Pillar tests on every feature; content caps (§15.1); cut list (§15.6) |
| Physics/grid performance with large ships | High | Graph-based subsystems; chunked grids; early stress tests in M1 |
| Colony sim feels shallow in first person | High | Vertical slice must prove it; invest in barks and ambient interactions |
| Tonal whiplash (horror ↔ cozy) | Medium | Hearth rule (§11.1); strong audio transitions; station is always a safe place |
| Procedural planets feel samey | Medium | Anchor set pieces, POI variety, Bloom coverage as a visual variable |
| Story gated by player building skill | Medium | Functional requirements + story blueprints + projector welding |
| Save compatibility breaking during expansions | Medium | Versioned schema + migrations from day one |

## 15.6 Cut list (in order, if needed)
1. Programmable Block scripting (keep event controllers).
2. Aerodynamics (wings) — use thrusters only.
3. Ship capture & repair of enemy ships.
4. Secret EDEN ending.
5. Drift size from 60 → 30 procedural systems.
6. Council meetings → simple policy menu.
7. Mimic and Burrower enemies.

**Never cut:** infection system, colony needs & relationships, block building with pressurization, the four acts, the three main endings.

## 15.7 Next steps
1. Approve this bible and lock the pillars.
2. Choose engine after a 2-week spike (voxel planet + 1,000-block grid + 200 crowd agents).
3. Start M1 prototypes in parallel (building, colony, horde, flight).
4. Write the full script for the vertical slice (Prologue + M1.01–M1.02).
5. Build the content definition registry first — it's the backbone of expansion.
