# 15 — Production Plan

> A realistic path from this bible to a shippable game. The design is ambitious (open world, physical building, colony sim, procedural galaxy, performance-captured story), so the plan offers **two scope tiers**. Pick one before pre-production ends.

## 15.1 Scope tiers

| | **Tier A — "Focused AA"** | **Tier B — "Full AAA"** |
|---|---|---|
| **Core team** | ~40 | ~110 + outsourcing (art, animation, QA, localization) |
| **Time to 1.0** | ~30 months | ~42 months |
| **Kestrel Valley** | 32 km² | 64 km² |
| **Drift systems** | 30 procedural + 5 anchors | 60 procedural + 5 anchors |
| **Story delivery** | Performance capture for Ada, Crane and Lily only; others in-engine animation | Full performance capture for all story characters |
| **Cinematics** | 10 (~12 min) | 18 (~24 min) |
| **Voiced lines** | ~8,000 | ~15,000 |
| **Full VO languages** | EN (+ subtitles in 12) | EN, FR, DE, ES, JA, PT-BR (+ subtitles in 7 more) |
| **Launch parts / weapons / Hollows** | ~160 parts / 18 / 11 | 237 parts (446 assets, see the [Parts Bible](../parts-bible/README.md)) / 24 / 14 |
| **Co-op** | Post-launch (+9 months) | Post-launch (+6 months) |
| **Early Access** | Recommended (funds development) | Optional |

The rest of this bible describes **Tier B**; §15.7 lists what Tier A cuts.

## 15.2 Scope strategy (both tiers)
1. **One hand-crafted solar system + a bounded procedural Drift**, not an infinite galaxy at launch.
2. **Colony size capped at 40**, with LOD simulation for off-screen survivors.
3. **Reuse the block system everywhere:** bases, ships, turrets, furniture and even story set pieces are grids.
4. **Single-player first**, with a co-op-ready host/client architecture from day one.
5. **Build the data registry first.** It's the backbone of both production speed and expansions.

## 15.3 Milestones (Tier B)

| # | Milestone | Duration | Exit criteria |
|---|---|---|---|
| **M0** | Concept & bible | 2 months | Bible approved; pillars locked; engine spike done; scope tier chosen |
| **M1** | Core prototypes | 4 months | Gray-box: (a) blocks + power + rooms, (b) 10 survivors with utility AI, (c) a 200-agent horde vs. walls, (d) seamless planet → orbit, (e) a 4 km² open-world streaming test |
| **M2** | Vertical slice | 6 months | Cold Open → M1.02 at final quality in a 4 km² slice of Kestrel Valley (§15.4) |
| **M3** | First playable (Acts I–II) | 8 months | Earth → Haven-9 → Moon end to end; the open valley at full size |
| **M4** | Alpha (content complete) | 12 months | All four acts; all endings reachable; the Drift at full size |
| **M5** | Beta | 7 months | Content final; balance; performance; localization; accessibility; certification prep |
| **M6** | Launch | 3 months | Certification; launch marketing; day-one patch |
| **Total** | | **~42 months** | |

## 15.4 Vertical slice definition (M2)
- **Length:** 60–75 minutes.
- **Content:** Cold Open, M0.01–M0.03, M1.01, M1.02, plus free exploration of a 4 km² slice of Kestrel Valley (Complex, Township, Route 93).
- **Must prove:**
  - Horror atmosphere in the dark spaceport.
  - **The Ada gut-punch works:** playtesters feel betrayed at Pad 12 and want to see her again.
  - The open world invites wandering: players leave the path within 20 minutes of the prologue ending.
  - Building a fortification that visibly holds (or fails) against a horde.
  - Lily feels like a person within 10 minutes of meeting her.
  - The infection meter creates tension without frustration.
- **Success test:** 8/10 external playtesters want to keep playing; ≥ 6/10 remember Lily's *and* Ada's names a week later.

## 15.5 Team (Tier B core, ~110)

| Discipline | Headcount | Notes |
|---|---|---|
| Direction (creative, game, art, audio, narrative, technical) | 6 | The owners of the bible |
| Production | 8 | Producers per pillar; release management |
| Game design | 16 | Systems (building/survival), colony sim, open world, combat, missions/levels, economy/balance |
| Narrative | 7 | Lead writer, 3 writers, 2 narrative designers, 1 cinematic designer |
| Engineering | 34 | Engine/voxel/streaming, gameplay, AI (colony, crowds, raid planner), physics/grids, tools, UI, online/co-op, platform, save |
| Art | 24 | Environment, characters, props/blocks, VFX, tech art, lighting, concept |
| Animation | 8 | Plus mocap stage partner |
| Audio | 5 | Sound design, music (plus composer), VO direction |
| QA (internal) | 8 | Plus an outsourced QA partner for full passes |
| User research & analytics | 3 | Playtests; telemetry |
| Community & marketing | 4 | Plus publisher/agency support |

## 15.6 Top risks & mitigations

| Risk | Impact | Mitigation |
|---|---|---|
| Scope from four big genres (open world, builder, life-sim, space) | Very high | Pillar tests on every feature; scope tiers; cut list (§15.7); content caps |
| Open-world streaming + voxel planets + physics grids performance | High | Engine spike in M0; stress tests in M1; strict per-platform budgets ([13 §13.7](13-technical-architecture.md)) |
| Story breaks under open-world sequence-breaking | High | State-based narrative ([17 §17.6](17-narrative-design.md)); fallback triggers; automated "story state" tests |
| The Taking's procedural staging in any player base | High | Prototype in M1; fallback to comms-screen staging |
| The colony sim feels shallow in first person | High | Vertical slice must prove it; barks and memory barks |
| Tonal whiplash (horror ↔ cozy) | Medium | The hearth rule; strong audio transitions |
| Procedural planets feel samey | Medium | Anchors, POI variety, Wonders, Bloom as a visual variable |
| Story gated by building skill | Medium | Functional requirements, story blueprints, projector welding |
| Save compatibility across expansions | Medium | Versioned schema and migrations from day one |

## 15.7 Cut list (in order, if needed)
1. Programmable Block scripting (keep event controllers).
2. Aerodynamics (wings); thrusters only.
3. Ship capture and repair of enemy ships.
4. The secret EDEN ending.
5. Drift size 60 → 30 procedural systems.
6. Council meetings → a simple policy menu.
7. Mimic and Burrower enemies.
8. The *Legacy* ending (play as adult Lily) → epilogue slides only.
9. Kestrel Valley 64 → 32 km².

**Never cut:** the open world, the infection system, colony needs and relationships, block building with pressurization, Ada's storyline, the four acts, the CURE / COMMUNE / EXODUS endings, and at least three Weavers.

## 15.8 Next steps
1. Approve this bible; lock pillars and the scope tier.
2. A 6-week engine spike: voxel planet + seamless orbit + a 1,000-block grid + 200 crowd agents + a 4 km² streamed region.
3. Start M1 prototypes in parallel (building, colony, horde, flight, open-world streaming).
4. Write the full vertical-slice script (Cold Open → M1.02) and cast Ada, Wrench and Lily for chemistry reads.
5. Build the content data registry first.
