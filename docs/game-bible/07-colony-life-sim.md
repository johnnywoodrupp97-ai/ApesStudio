# 07 — Colony Life-Sim

> The *Sims* pillar: survivors are autonomous people with needs, moods, traits, skills and relationships. The player lives among them in first person and can also manage them through a colony overlay.

## 7.1 Survivor anatomy

Every survivor (generic or story) is defined by:

| Component | Description |
|---|---|
| **Identity** | Name, age, portrait/appearance, pronouns, voice set, backstory (pre-outbreak job + one "what I lost" line) |
| **Needs (8)** | Hunger, Rest, Hygiene, Comfort, Social, Fun, Safety, Purpose |
| **Mood** | Aggregate of needs + moodlets (temporary modifiers) |
| **Traits (2–3)** | Personality & quirks that alter needs, skills and behaviors |
| **Skills (12)** | Level 0–10, improved by working and learning |
| **Relationships** | Opinion values toward every other survivor and the player |
| **Health** | Injuries, illness, infection stage, disabilities |
| **Memories** | Significant events (witnessed a death, rescued by player, first meal on the station) that bias future behavior |

## 7.2 Needs

| Need | Satisfied by | Neglect effect |
|---|---|---|
| **Hunger** | Meals (quality matters) | Weakness, then health loss |
| **Rest** | Beds (quality, room noise/light) | Slower work, accidents, mood crash |
| **Hygiene** | Showers, toilets, sinks, clean rooms | Mood −, illness chance, social penalty |
| **Comfort** | Chairs, couches, decor, temperature | Mood − |
| **Social** | Conversations, shared meals, group activities | Loneliness, depression |
| **Fun** | TV, games, music, gym, observation windows, books | Boredom, stress |
| **Safety** | Defenses, lighting, locked doors, no recent attacks | Fear, panic, refusing expeditions |
| **Purpose** | Doing preferred work, skill growth, story progress | Apathy, "What's the point?" breakdowns |

*Purpose* is the survival-specific need that sets our game apart: people need to feel the colony is going somewhere. Completing story milestones gives colony-wide Purpose boosts.

## 7.3 Mood & mental states

**Mood scale:** Despairing ← Miserable ← Stressed ← Neutral → Content → Happy → Inspired

**Moodlets** (examples):
- *Ate a Feast* (+15, 8h) · *Slept in a nice bed* (+5) · *Saw Earth from the window* (+8, or −8 for *Homesick* trait)
- *Witnessed a Turning* (−25, 2 days) · *Friend died* (−35, 5 days) · *Our home held the horde* (+12)
- *Cramped quarters* (−6) · *Room too cold* (−4) · *Talked with Lily* (+5)

**Mental breaks** (at Miserable/Despairing, chance-based):
| Break | Behavior |
|---|---|
| **Shutdown** | Stays in bed, won't work |
| **Binge** | Eats double rations |
| **Rage** | Damages furniture/blocks, starts fights |
| **Flee** | Attempts to steal an escape pod or rover |
| **Confess** | Reveals a secret (e.g., hidden infection) — sometimes good! |
| **Inspired** (positive, at Inspired mood) | Work speed ×2 for a day, or creates art that raises room beauty |

## 7.4 Traits (launch set: 48 — examples)

| Trait | Effect |
|---|---|
| **Handy** | +25% building/repair speed |
| **Green Thumb** | +30% crop yield, loves hydroponics |
| **Night Owl** | Prefers night shifts; mood bonus working late |
| **Claustrophobic** | Mood penalty in small rooms; loves observation decks |
| **Comfort Eater** | Eats more; eating gives extra mood |
| **Pacifist** | Won't use weapons; excellent medic/negotiator |
| **Sharpshooter** | +accuracy; bored in non-combat jobs |
| **Hides Wounds** | Will conceal infection until Seeded stage (dangerous!) |
| **Survivor's Guilt** | Periodic sadness; big Purpose bonus from rescues |
| **Optimist / Pessimist** | Baseline mood ±10 |
| **Homesick** | Earth-view windows cause sadness; bonus when returning to Earth |
| **Bonded** (paired) | Shares mood with partner; devastated by partner's death |
| **Spacer** | No zero-G sickness; bonus on stations |
| **Frail** | Low health; high wisdom (teaching bonus) |
| **Choir-Curious** | Drawn to the Choir; may defect if colony Purpose is low |

## 7.5 Skills (12)
Engineering · Mechanics · Medicine · Research · Botany · Cooking · Combat · Piloting · Social · Art · Logistics · Security

- Skills level through use, mentoring (pair a high-skill mentor with a learner), and books/sims.
- Higher skill → faster work, better quality output, fewer accidents, unlock special actions (e.g., Medicine 8 can perform surgery; Research 6 can analyze Sower tech).

## 7.6 Jobs & schedules

**Jobs:** Builder, Mechanic, Medic, Researcher, Farmer, Cook, Guard, Pilot, Hauler, Scout (expeditions), Teacher, Counselor, Janitor, Miner.

- **Job priority grid** (per survivor, per job, 1–4 priority) — familiar to colony-sim fans.
- **Schedules:** 24h timeline with Work / Sleep / Leisure / Anything blocks. Shift presets (Day, Night, Split).
- **Autonomy:** survivors satisfy their own needs and pick tasks from the job queue. The player can issue **direct orders** in person (talk → "Follow me," "Repair this," "Guard here") or from the overlay.
- **Expeditions:** assign survivors to squads that follow the player or go on **off-screen missions** (scavenge, trade run, rescue) with risk and reward resolved in a text-event format with choices.

## 7.7 Rooms & Room Quality
Rooms are detected by the building system (airtight or wall-enclosed spaces). Each room is **auto-classified** by its furniture (Bedroom, Barracks, Mess Hall, Kitchen, Medbay, Lab, Greenhouse, Rec Room, Workshop, Chapel, Classroom) or **manually zoned**.

**Room Quality score** = Size + Cleanliness + Beauty (decor, plants, art, windows) + Comfort (furniture quality) + Environment (temp, light, noise) − Clutter.
- Tiers: Squalid → Dull → Decent → Nice → Impressive → Wondrous.
- Quality drives moodlets and sleep/eat/relax effectiveness.

## 7.8 Relationships

- **Opinion** (−100 to +100) toward each other survivor and the player, driven by: shared activities, compatible traits, conversations, gifts, conflicts, witnessed actions.
- **Relationship states:** Stranger → Acquaintance → Friend → Close Friend / Rival → Enemy; Romantic Interest → Partner → Married (adults only; opt-out setting).
- **Social interactions** (autonomous, visible as short barks & animations): Chat, Joke, Vent, Comfort, Argue, Share Food, Teach, Flirt, Insult, Reconcile.
- **Factions within the colony:** When groups form (e.g., "Earth Returners" vs. "Stay in the Stars"), they lobby the player during colony meetings.
- **Player relationship:** The player's opinion with each survivor affects obedience in crises, expedition willingness, and personal quest availability.

## 7.9 Colony events (launch set: 80+)

Generated by an **Event Director** that reads colony state (morale, resources, time since last event, story act) and picks weighted events.

| Category | Examples |
|---|---|
| **Social** | A birthday (party boosts Social), a wedding proposal, a fist-fight over rations, a talent night |
| **Crisis** | Hidden infection turns, a reactor leak, a micrometeorite breach, a food-rot blight, a survivor steals a rover |
| **Arrival** | Distress call from a lifeboat, a trader visit, a Choir envoy, a refugee pod with a sick child |
| **Discovery** | A survivor finds a Sower glyph in the mining haul, a child draws something from a dream (Lily's "visions") |
| **Moral dilemma** | Refugees want to join but one is infected; the colony votes to exile a thief; a survivor wants to euthanize a Stage 3 friend |

## 7.10 Colony meetings (the "Council")
- Every few in-game days (or when tension spikes), survivors call a **Council** at the mess hall.
- The player hears 1–3 proposals (e.g., "Double the guard rotation," "Lower rations to save seeds," "Send a mission to Earth for survivors") and chooses; alternatively lets the colony vote.
- Decisions create **Colony Policies** (ration level, work hours, quarantine protocol, weapons policy, child education) with mood trade-offs.

## 7.11 Colony stats (overlay)
Population · Morale · Food days · Water days · O₂ reserve · Power margin · Defense rating · Infection risk · Purpose · Research rate

## 7.12 Balance targets
- A reasonably maintained colony sits at **Content** without micromanagement.
- Crises should occur roughly **once per 45 min** of play and be resolvable with what the player has.
- Survivor death should be **rare, dramatic and preventable** — never random-feeling.
- Maximum colony size at launch: **40 survivors** (performance and readability target); story calibrated for 8–20.
