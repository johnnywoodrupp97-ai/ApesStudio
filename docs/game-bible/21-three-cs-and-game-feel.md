# 21 — Character, Camera, Controls & Game Feel

> The "3 Cs": how it feels to *be* the Engineer, second to second.

## 21.1 Character: the player's verbs

| Verb | On foot | In zero-G | Notes |
|---|---|---|---|
| **Move** | Walk 1.6 m/s · jog 3.8 m/s · sprint 6.2 m/s | Jetpack thrust (6 DOF) | Sprint drains stamina; heavy inventory slows you |
| **Crouch / prone** | Yes / yes | — | Lowers noise and profile |
| **Mantle & climb** | Up to 2 m; ladders | Grab handholds | Contextual, no button-mashing |
| **Lean** | Yes | — | Peek around cover |
| **Jetpack** | Short boosts (gravity) | Full flight | Suit energy; limited above 1 g |
| **Mag-boots** | — | Walk on hulls | Toggle; required for heavy tools in zero-G |
| **Weld / grind / scan** | Multitool modes | Same | The core verb set, always one button away |
| **Place block** | Build mode | Build mode | Ghost preview; rotate; symmetry |
| **Carry** | Objects and people | Objects float, momentum kept | Carrying people slows you; you can't shoot while carrying |
| **Interact** | Doors, terminals, survivors | Same | One button; hold for context menu |
| **Talk** | Survivors and companions | Same | Tone wheel |
| **Command** | Squad orders (follow, hold, guard, repair) | Same | Quick radial |
| **Fight** | Melee, firearms, throwables | Recoil pushes you | See [09](09-combat-and-enemies.md) |
| **Drive / fly** | Rovers, aircraft | Ships | Seamless; step into a cockpit |

## 21.2 Camera
- **First-person default** for everything on foot: horror, intimacy, immersion.
- **Optional third-person** (toggle) for exploration, building and vehicles, as in *Space Engineers*. Some story scenes force first-person for staging.
- **Build camera:** a free-fly orbit camera for large builds, available in safe zones (no Hollows within 50 m) and always in Creative.
- **Colony Overlay camera:** isometric/top-down view of the current grid, with cutaway floors.
- **FOV:** 70–110 slider. **Head-bob:** off/low/full. **Zero-G horizon lock** for motion comfort.

## 21.3 Controls

### On foot — keyboard & mouse / controller

| Action | KB/M | Controller |
|---|---|---|
| Move / look | WASD / mouse | Left stick / right stick |
| Sprint / crouch | Shift / Ctrl (C for prone) | L3 / B (hold for prone) |
| Jump / jetpack | Space (hold) | A (hold) |
| Primary / secondary | LMB / RMB | RT / LT |
| Multitool mode wheel | Q (hold) | LB (hold) |
| Interact / context | E / hold E | X / hold X |
| Build mode | B | D-pad Up |
| Inventory | Tab | View |
| Squad command wheel | Z (hold) | RB (hold) |
| Scanner pulse | F | R3 |
| Journal / map | J / M | Menu → tabs |
| Colony Overlay | O | D-pad Down |
| Mag-boots | G | D-pad Left |
| Helmet light | L | D-pad Right |

### Build mode (additions)

| Action | KB/M | Controller |
|---|---|---|
| Place / remove frame | LMB / RMB | RT / LT |
| Rotate block | Arrow keys / PgUp/PgDn | Right stick click + stick |
| Block menu | G (radial) · 1–9 hotbar | LB (radial) |
| Symmetry toggle | N | D-pad Left (in build mode) |
| Structural / power / air views | F5 / F6 / F7 | View (hold) + face buttons |
| Copy / paste (when unlocked) | Ctrl+C / Ctrl+V | Hold RB + X / Y |

### Ship flight

| Action | KB/M | Controller |
|---|---|---|
| Translate (6 DOF) | WASD + Space / C | Left stick + LB / RB |
| Rotate (pitch/yaw) | Mouse | Right stick |
| Roll | Q / E | LT / RT (with modifier) |
| Throttle (cruise) | Shift / Ctrl | D-pad Up / Down |
| Inertial dampeners | Z | B |
| Landing gear lock | P | Y |
| Weapons fire | LMB | RT |
| Pulse / jump drive | J (hold) | Hold Menu + A |

All bindings are remappable; hold/toggle is selectable per action. Mouse-and-keyboard and controller have full parity, including in the Colony Overlay (controller uses a snapping cursor).

## 21.4 Game feel targets

| Moment | Target feel | How |
|---|---|---|
| **Welding** | Satisfying, tactile, "making" | Spark VFX that fill the block; rising pitch as the build % climbs; a *clunk* and a light pulse when the block becomes functional; haptic buzz |
| **Grinding** | Destructive, noisy | Harsh audio; debris; components popping into inventory |
| **Melee** | Heavy, desperate | 300–500 ms swings; hit-stop on impact (60 ms); stamina drain; Hollows stagger |
| **Firearms** | Loud, scarce, consequential | Strong recoil; loud reports that audibly echo across the valley (a noise-meter spike) |
| **Zero-G** | Weightless but controllable | Momentum preserved; subtle thruster audio; mag-boot *thunk* |
| **Ship flight** | Heavy ships feel heavy | Physically driven; the camera shakes with the thrusters; creaks under high G |
| **Landing** | Tense, rewarding | Proximity beeps; dust or regolith kick-up; gear-lock *clank* |
| **Airlock cycling** | Relief | Hiss → silence → pressure → full sound rushes back in; the helmet visor clears |

## 21.5 Haptics & adaptive triggers
- **DualSense:** resistance ramps on RT while welding (as the block fills); heavier trigger pull on the throttle at max thrust; weapon-specific trigger stops.
- **Rumble language:** a heartbeat pulse at high infection; a low rumble for approaching hordes (felt before they're heard); a sharp jolt for hull breaches.

## 21.6 Responsiveness budgets
- **Input latency:** ≤ 60 ms at 60 fps (performance mode).
- **Block placement:** ghost preview updates within one frame; placement feedback within 50 ms.
- **UI:** any menu opens in under 150 ms; the Colony Overlay transition in 400 ms (animated, skippable).
