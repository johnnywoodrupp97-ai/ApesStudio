# 17 — Narrative Design

> How the story is told, not just what it is. The story itself is in [03 — Storyline](03-storyline.md); the cast is in [04 — Characters](04-characters.md).

## 17.1 Narrative pillars
1. **Personal before epic.** Every galaxy-scale beat lands on a face we care about: a sister, a child, a mechanic.
2. **You never lose control for long.** First-person, in-engine storytelling. Full cutscenes are rare and earned (see [19](19-set-pieces-and-cinematics.md)).
3. **The world is the writer.** Environmental stories, logs and colony barks carry at least half of the narrative.
4. **Choices cost something you can see.** A decision shows up later in the colony, in a face, or on the memorial wall.
5. **Open world, closed arcs.** The player chooses the order; every arc still has a beginning, middle and end.

## 17.2 Theme architecture — "the gardeners"

| Philosophy | Voiced by | Belief | Ending it becomes |
|---|---|---|---|
| **Seed & harvest** | The Sowers | A world exists to be made useful | (the default the player overrides) |
| **Prune** | Crane | Cut away the weak so the tree survives | EDEN |
| **Surrender** | Sable | Let the garden grow through us | COMMUNE |
| **Tend** | Mara, Lily | Heal what's hurt, with consent | CURE |
| **Build** | The Engineer, Tug, Oye | Make somewhere new to live | EXODUS |

Every major conversation lets the player lean toward one of these philosophies. Nothing is locked by it, but companions notice, and the ending narration reflects the leaning.

## 17.3 Delivery methods

| Method | Share of story | Notes |
|---|---|---|
| **In-engine, first-person scenes** | 30% | Player keeps camera control; characters perform around them (walk-and-talks, radio, workbench conversations) |
| **Full cinematics** | 5% | ~24 minutes total across the game; used only for the biggest turns |
| **Radio & comms** | 15% | Ada's messages, Crane's broadcasts, KESTREL, distress calls |
| **Colony life** | 20% | Barks, dinners, councils, relationship events |
| **Environmental storytelling** | 15% | "Three objects" rule; the Bloom's visual progression |
| **Logs, letters & codex** | 15% | Under 45 seconds of audio or 120 words each |

## 17.4 Dialogue system
- **Tone-tagged choices:** *Direct / Warm / Pragmatic / Wry*, shown as short paraphrases (never full lines), with a tone icon.
- **Timed only in emergencies:** most conversations wait. In crises (the Pad 12 standoff, M3.07's lab) a soft timer appears, and silence is a valid choice.
- **Interrupts:** in some scenes you can act mid-line (lower your weapon, step between Idris and Ada).
- **Walk-and-talk:** companions talk during travel; conversations pause for combat and resume afterward (*"As I was saying…"*).
- **No morality meter.** Consequences are tracked per character (approval) and per world flag.

## 17.5 Companion approval & reactivity

Each companion has **Approval** (−100…+100) toward the Engineer, separate from colony-sim Opinion but feeding into it.

| Companion | Approves of | Disapproves of |
|---|---|---|
| **Tug** | Protecting the weak; clever engineering; humor | Leaving people behind; cruelty |
| **Lily** | Honesty; asking her consent; kindness to creatures | Being lied to; being "protected" without being asked |
| **Mara** | Consent-first medicine; healing Veyra; science | Using Lily without consent; destroying research |
| **Idris** | Keeping your word; discipline; protecting the colony | Trusting the Directorate; reckless risk to survivors |
| **Oye** | Keeping deals; fair trades; bold flying | Breaking contracts; attacking Haulers |
| **KESTREL** | Curiosity; answering its questions honestly | Being dismissed as "just a program" (it remembers) |
| **Ada** (`ada_bond`) | Answering her messages; sparing her pilots; Warm choices | Hostility; harming Directorate pilots; Idris's revenge |

**Thresholds:** at +60 a companion unlocks their personal quest finale and a unique perk; at −60 they may refuse orders, or leave the colony (never during a story mission).

## 17.6 Open-world narrative rules (state over sequence)

1. **Story anchors respond to the state you arrive in, not mission order.** Scenes check flags, not "has mission X completed."
2. **Every critical beat has a fallback trigger.** If the player skips a setup (e.g., never finds Ada's recording), the payoff uses a fallback version.
3. **Missing companions have understudies.** If Idris wasn't saved, his M3.06 line ("I know the Meridian") goes to a Directorate defector found in Act III, **Lt. Sana Iqbal**.
4. **Systemic beats fire at safe moments** (see [08 §8.7](08-open-world-and-exploration.md)).
5. **The journal never lies.** A lead that becomes impossible (e.g., its survivor died) resolves visibly with a short epilogue line.

### Sequence-breaking table

| If the player… | The story… |
|---|---|
| Reaches orbit in a home-built rocket before M1.07 | Starts Act II at docking. Unrescued characters become leads on Earth. Tug is alive at the hangar and radios for pickup; `tug_survived = true`. |
| Visits Veyra-4 before Tortuga | Veyra's key content plays normally; Oye's favor later points to Hollowmere only |
| Skips Tycho and reaches Styx with another power source | Ada's M2.04 messages are delivered as found letters; the archive is recovered from the Styx Wreck instead |
| Never answers Ada's messages | `ada_bond` stays low; Ada is the M4.03 boss; the talk-down still works with the recording |
| Ignores the colony for hours | Colony autopilot; escalating warnings; the Council in M3.06 is harsher |

## 17.7 Bark system
- **Categories:** combat (spotting, reloading, hurt), exploration (noticing POIs, weather), colony (needs, work, relationships), reactive (your actions: *"Did you just weld the door shut with us inside?"*), memory (callbacks to past events: *"Reminds me of the school…"*).
- **Volume:** ~9,000 companion barks; 8 voice types × 3 moods × ~350 lines for procedural survivors.
- **Anti-repetition:** each bark has a cooldown and a "heard" counter; no bark repeats within 30 minutes of play.
- **Memory barks** are the secret weapon: survivors referencing *specific* things the player did make the colony feel alive.

## 17.8 Writing style guide
- **Plain speech.** People talk like tired, frightened, funny people, not like a wiki.
- **No one says "zombie."** Lily says it once in M1.02; Tug answers: *"They're not zombies, kid. Zombies are made up. These are just… hollow."* After that they're **Hollows**, **the dead**, or **the listening** (Choir).
- **Sci-fi is grounded.** Tech is described by what it does ("the thing that makes air"), not by jargon.
- **Humor as coping.** At least one light line in every dark scene; never undercut a death.
- **Crane is never cartoonish.** Each of his broadcasts should contain one thing that's true.
- **Kids are never shown being killed.** Children are endangered, rescued, and grieve, but child death is off-screen only and never playable.
- **Profanity:** moderate (M rating); Lily never swears except once, and everyone reacts.

### Cultural & sensitivity consultants
- **Nigerian (Igbo) culture consultant** for the Okafor family (names, food, Sunday traditions, Ada's tattoo).
- **Indigenous consultant** for Aiyana Two Rivers.
- **Disability consultant** for amputation and survivor disability systems.
- **Grief and trauma consultant** for M3.05–M3.06, and for Lily's writing throughout.

## 17.9 Localization-ready writing
- No text baked into textures (except diegetic signage with localized decals).
- Lines written as complete sentences, with gender-neutral variants for the player's pronouns.
- "Wrench" is a nickname that translates: each language chooses its own tool-based nickname.
- **Launch languages:** EN, FR, IT, DE, ES (EU & LatAm), PT-BR, PL, RU, JA, KO, ZH-CN, ZH-TW, TR. Full VO in EN, FR, DE, ES, JA, PT-BR.

## 17.10 Narrative content volume (launch)

| Content | Count |
|---|---|
| Main-story missions | 32 (cold open + 31 across the prologue and four acts) |
| Companion quest chains | 6 |
| Notable Survivor stories | 12 voiced + 28 text-and-bark |
| Full cinematics | 18 (~24 minutes) |
| Voiced lines (all) | ~15,000 |
| Logs, letters & documents | ~220 |
| Codex entries | ~300 |
| Ending variants | 22 (modular slides + bespoke Weaver finales) |
