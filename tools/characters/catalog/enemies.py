"""HOL — Hollows & Sower constructs, FAC — faction units, BOS — bosses.

Style rules for every Hollow (see chapter 06 intro): horror through wrongness, not gore.
Bloom growth replaces blood. Hollows are converted from survivor-kit bodies, so any
adult body/outfit combination can become a Hollow. There are no child Hollows.
"""

from . import CH, H, O

KIT_SOURCE = "Converted from any adult survivor-kit body and outfit (Earth civilian, Kestrel crew, Directorate, miner, Hauler). Conversion = Hollow material + INF_/hol_ shapes + Bloom attachments on sockets."


def hollow(name, tier, skel, *, gp, silhouette, bloom, weak, anim, audio, outfits, notes="", extra_bones=(), variants=(), first=""):
    CH("HOL", name, tier=tier, skeleton=skel, pronouns="—", infection=False,
       role=gp.get("role", ""), appears=first,
       visual={"silhouette": silhouette, "bloom": bloom, "weak_points": weak, "acting": anim, "audio": audio},
       outfits=outfits, gameplay=gp, notes=notes, extra_bones=extra_bones, variants=variants)


# ---------------------------------------------------------------------------
# HOL — Hollows
# ---------------------------------------------------------------------------
hollow("Shambler", "Enemy", H(1.75), first="M0.02 (Dana Marsh)",
       gp={"role": "The common Hollow: slow, relentless, groups up, knocks on doors.", "hp": 100, "speed_mps": 1.1, "damage": 12, "infection_per_hit": "6%", "counter": "Melee, headshots, chokepoints"},
       silhouette="A person, almost: head tilted too far, shoulders uneven, one arm hanging.",
       bloom="Green veins under grey skin; lichen crust at the collar and hands; one fist-sized Bloom node on the head or chest.",
       weak="Bloom node (×3 damage): SOCKET_BloomNode on head or spine_04, placed per variant.",
       anim="Asymmetric shuffle set (6 variants), door-knock idle, lunge-grab, stumble recovery.",
       audio="Wet breath, radio-like clicks in the Verdance five-note rhythm.",
       outfits=[O("KitConversion", "Survivor-kit conversion", "All acts", KIT_SOURCE)],
       variants=[("Civilian", "Earth civilian outfits"), ("KestrelCrew", "Kestrel coveralls and uniforms"), ("Directorate", "Directorate armor and fatigues"),
                 ("Miner", "Hi-vis and mining gear (Tycho, Silver Ridge)"), ("Hauler", "Hauler coveralls (the Drift)")],
       extra_bones=["bloom_node_01", "bloom_growth_01…06 (attach bones)"],
       notes="Dana Marsh's Hollow form (CST) is the style benchmark. Crowd LODs: LOD3 plus a vertex-animation-texture (VAT) impostor for hordes over 300.")

hollow("Runner", "Enemy", H(1.78, "adult_athletic"), first="M1.02",
       gp={"role": "Recently turned, fast, leaps; hunts in packs of 3–6.", "hp": 70, "speed_mps": 5.8, "damage": 10, "infection_per_hit": "6%", "counter": "Shotguns, traps, high ground"},
       silhouette="Leaner, more human than a Shambler: fresh clothes, fresh wounds, sprinting on all fours when it charges.",
       bloom="Minimal: bright green veins at the neck and wrists, eyes filmed green.",
       weak="Head (×3); no visible node yet (the growth is under the skin).",
       anim="Sprint, quadrupedal charge, wall-leap, pack howl.", audio="Ragged panting, high clicks.",
       outfits=[O("KitConversion", "Survivor-kit conversion", "All acts", KIT_SOURCE)])

hollow("Crawler", "Enemy", H(1.70), first="M1.02 (school vents)",
       gp={"role": "Legless Hollow that hides in vents and under vehicles, then ambushes.", "hp": 60, "speed_mps": 2.0, "damage": "15 (ambush)", "infection_per_hit": "8%", "counter": "Scanner, flashlight"},
       silhouette="Low to the ground (0.5 m): arms doing all the work, lower body fused into a root-like Bloom mass.",
       bloom="Lower body replaced by a trailing root mass; claws of Bloom-hardened nails.",
       weak="Bloom mass at the pelvis (×2.5).",
       anim="Arm-drag crawl, vent crawl, ceiling drop, under-car ambush.", audio="Scraping, clicks.",
       outfits=[O("KitConversion", "Survivor-kit upper body + root mass", "All acts", "Upper-body kit pieces only; the root mass replaces the legs (leg bones remain, weighted to the root mass).")],
       notes="Keeps the full humanoid skeleton so it shares locomotion retargeting; the leg bones drive the root-mass sway.")

hollow("Screamer", "Elite", H(1.80, "adult_slim"), first="M1.04 (the Vault)",
       gp={"role": "Emits a shriek that calls the horde and stuns (1.5 s).", "hp": 90, "speed_mps": 1.4, "damage": "— (stun)", "infection_per_hit": "—", "counter": "Priority target; suppressed weapons"},
       silhouette="Too tall and thin, neck stretched, jaw unhinged, chest opened like bellows.",
       bloom="Throat and chest converted into a Bloom bellows sac that inflates before the shriek (shape key + jiggle bones).",
       weak="Throat sac (×3).",
       anim="Inhale tell (0.8 s, readable from 20 m), shriek, retreat behind the horde.", audio="A long inhale, then a layered human-and-feedback shriek.",
       outfits=[O("VaultScientist", "Vault scientist", "Act I", "Lab scrubs from the Vault staff (first Screamer); kit outfits after that.")],
       extra_bones=["sac_inflate_01…03", "jaw_unhinge"])

hollow("Bloater", "Elite", H(1.76, "adult_broad"), first="M1.05 (Fuel Farm)",
       gp={"role": "Swollen with spores; bursts into a spore cloud when killed.", "hp": 140, "speed_mps": 1.2, "damage": "40 burst + spore cloud", "infection_per_hit": "2%/s in cloud", "counter": "Ranged kill; masks"},
       silhouette="Round and heavy, clothes split at the seams, belly and back covered in translucent spore sacs.",
       bloom="Clusters of glowing spore sacs (emissive pulse) that wobble with movement.",
       weak="Spore sacs (×2); each sac can pop individually.",
       anim="Waddle, gag idle, burst.", audio="Gurgling, wet creaks.",
       outfits=[O("KitConversion", "Survivor-kit conversion (split seams)", "All acts", KIT_SOURCE + " Uses torn outfit variants.")],
       extra_bones=["sac_jiggle_01…08"],
       notes="The burst is a spore cloud and deflated husk (swap mesh), never gore.")

hollow("Brute", "Elite", H(2.60, "brute"), first="M1.06 (The Long Night)",
       gp={"role": "Huge, armored with Bloom plating; targets the weakest load-bearing block.", "hp": 900, "speed_mps": 2.2, "damage": "45 (300 to blocks)", "infection_per_hit": "12%", "counter": "Fire, heavy weapons, reinforced walls"},
       silhouette="2.6 m of overgrown mass: massive arms, small head, Bloom plates like tree bark.",
       bloom="Layered bark-like plates over the shoulders and back; one exposed glowing node between the shoulder blades.",
       weak="Back node (×2), exposed after a charge or from above.",
       anim="Heavy walk, charge, wall-punch, ground-slam, stagger.", audio="Deep groans, cracking wood.",
       outfits=[O("Overgrown", "Overgrown remnants", "All acts", "Scraps of a construction worker's hi-vis and a tool belt embedded in the plates.")],
       extra_bones=["plate_shoulder_l/r", "plate_back_01…03"])

hollow("Drifter", "Enemy", H(1.82), first="M2.01 (Haven-9)",
       gp={"role": "Zero-G Hollow in an EVA suit; pushes off surfaces to lunge.", "hp": 110, "speed_mps": "3.5 (lunge)", "damage": 14, "infection_per_hit": "6%", "counter": "Mag-boots, shotguns, venting"},
       silhouette="A drifting EVA suit, limbs splayed, visor cracked.",
       bloom="The helmet is filled with Bloom growth pressing against the cracked visor (emissive).",
       weak="Visor crack (×3).",
       anim="Zero-G drift idle, push-off lunge, hull crawl.", audio="Muffled clicks through the helmet radio.",
       outfits=[O("EVAConversion", "Haven-9 / Kestrel EVA suit", "Act II+", "Shared EVA suit (SK_SUIT_EVASuit) with the Hollow damage variant: cracked visor, torn fabric, frost.")])

hollow("Burrower", "Elite", H(1.60, "adult_broad"), first="M2.04 (Tycho)",
       gp={"role": "Ex-miner Hollow that tunnels and erupts under bases.", "hp": 400, "speed_mps": "3.0 underground", "damage": 30, "infection_per_hit": "10%", "counter": "Seismic sensors, floor armor"},
       silhouette="Hunched and wide; forearms fused into shovel-like Bloom-bone claws; a miner's helmet lamp still flickering.",
       bloom="Bone-white Bloom claws; regolith-encrusted back.",
       weak="Helmet-lamp node (×2) on the head.",
       anim="Burrow, erupt, claw swipe, dig-under.", audio="Grinding, muffled thumps before an eruption.",
       outfits=[O("Miner", "Tycho miner", "Act II", "Mining undersuit and hi-vis remnants; helmet lamp as an emissive socket.")],
       extra_bones=["claw_l_01…03", "claw_r_01…03"])

hollow("Mimic", "Elite", H(1.74), first="M3.04 (Hollowmere)",
       gp={"role": "Mimics survivor voices and radio calls to lure the player.", "hp": 150, "speed_mps": 2.5, "damage": 18, "infection_per_hit": "8%", "counter": "Scanner; trust but verify"},
       silhouette="Almost human from one side: clean clothes, one intact half of a face.",
       bloom="The other half of the face and throat are a delicate Bloom lattice with a voice organ (a glowing throat sac).",
       weak="Throat organ (×3).",
       anim="Human idle (convincing at range), 'reveal' head turn, fast lunge.", audio="Recorded human voice lines in the voices of the player's own survivors.",
       outfits=[O("KitConversion", "Survivor-kit conversion (clean)", "Act III+", "Clean outfits (the lure).")],
       notes="Uses the Secondary-tier facial set on the intact half so its lip-sync reads.")

hollow("Husk Titan", "Boss", H(18.0, "colossus"), first="M3.08 (planet event boss)",
       gp={"role": "Colossal walking Bloom mass; a planetary event boss.", "hp": 20000, "speed_mps": 4.0, "damage": "400 stomp", "infection_per_hit": "spore rain", "counter": "Ship weapons, orbital strike"},
       silhouette="An 18 m giant of Bloom grown around a skeleton of wreckage, trees and shipping containers.",
       bloom="Forest-scale growths, spore chimneys on the back (emissive vents), a glowing Heart in the chest.",
       weak="Chest Heart (×2), four spore chimneys.",
       anim="Slow stride, stomp, sweep, collapse.", audio="Sub-bass groans, wood cracking, wind.",
       outfits=[O("Colossus", "Wreckage frame", "Act III+", "Unique mesh: wreckage, trees and containers inside the Bloom mass (no human remains visible).")],
       extra_bones=["chimney_01…04", "heart"], notes="Needs a large-scale LOD chain (visible from 3 km). Cast shadows only at LOD0–1.")

hollow("Stalker", "Creature-L", {"template": "quadruped", "shoulder_h": 1.4, "length": 3.2}, first="M3.03 (Veyra-4); varies by planet",
       gp={"role": "Bloom-mutated native predator; each planet's predator kit gets a Stalker variant.", "hp": 450, "speed_mps": 9.0, "damage": 35, "infection_per_hit": "8%", "counter": "Planet-specific"},
       silhouette="The planet's predator, but wrong: extra growth along the spine, a split jaw.",
       bloom="Spine ridges of Bloom, a glowing split jaw.", weak="Spine ridge node (×2).",
       anim="Stalk, pounce, circle.", audio="Planet-specific base with the Verdance clicks layered in.",
       outfits=[O("CreatureKit", "Predator kit + Bloom overlay", "Act III+", "Built from the procedural predator kit (CRE) with the Bloom overlay set.")])

hollow("Hive Mite", "Creature-S", {"template": "flyer", "shoulder_h": 0.06, "length": 0.12, "wings": 0.08}, first="M3.03",
       gp={"role": "Flying spore insect; swarms drain O₂ and clog vents.", "hp": 5, "speed_mps": 7.0, "damage": "O₂ drain", "infection_per_hit": "1%", "counter": "Flame, air filters"},
       silhouette="A beetle-sized flyer with translucent wings; seen as swarms of hundreds.",
       bloom="Glowing abdomen.", weak="Any hit kills.", anim="Swarm flocking (GPU), individual crawl.", audio="Buzzing swarm bed.",
       outfits=[O("Swarm", "Swarm unit", "Act III+", "LOD0 only for close-ups; swarms render as GPU particles with a 200-tri mesh.")],
       notes="Budget is per individual; swarms use instanced 200-tri LOD2.")

hollow("Sower Warden", "Elite", H(3.2, "exoframe"), first="M4.02 (the Memory Gardens)",
       gp={"role": "Ancient precursor construct guarding the Seedship; resonance shield.", "hp": 2500, "speed_mps": 2.5, "damage": 60, "infection_per_hit": "—", "counter": "Electric + Resonance damage"},
       silhouette="A 3.2 m shell-and-coral knight with no face, a halo of floating shell plates.",
       bloom="None: Sower materials (pearl shell, teal glyph channels).", weak="Glyph core in the chest when the shield drops.",
       anim="Measured stride, plate-shield rotation, resonance slam.", audio="Choral hum, stone-on-glass footsteps.",
       outfits=[O("Construct", "Sower shell body", "Act IV", "Unique: rigid shell segments (no skin deformation) plus floating plates on their own bones.")],
       extra_bones=["plate_orbit_01…08"], notes="Rigid-segment skinning (one bone per segment, weight 1.0). Uses the SOW material master.")

# ---------------------------------------------------------------------------
# FAC — Faction units
# ---------------------------------------------------------------------------
def unit(name, tier, skel, faction, *, role, look, outfit, gp=None, face_visible=False, notes="", variants=(), infection=True):
    CH("FAC", name, tier=tier, skeleton=skel, pronouns="Varies (male and female body variants)", infection=infection,
       role=f"{faction}. {role}", visual={"silhouette": look, "faction": faction, "face_visible": "Yes" if face_visible else "No (helmeted)"},
       outfits=[O("Standard", outfit[0], "Act I+", outfit[1], outfit[2] if len(outfit) > 2 else [])], gameplay=gp or {}, notes=notes, variants=variants,
       art={"Ark Directorate": "DIR", "Free Haulers": "HAU"}.get(faction, "IND"))


unit("Directorate Trooper", "Crowd", H(1.82, "adult_athletic"), "Ark Directorate",
     role="Armored infantry; uses cover, flanks, throws grenades.", gp={"hp": 180, "weapons": "Assault rifle, grenades"},
     look="White ceramic armor with gold trim, black visor, sterile and anonymous.",
     outfit=("Trooper Armor", "White ceramic plates over a grey undersuit, black visor helmet, gold rank stripe.", ["Helmet", "Chest plate", "Arm and leg plates", "Undersuit", "Webbing"]),
     variants=[("Female", "Female body variant"), ("Damaged", "Scorched and cracked armor (Meridian, Convergence)")])
unit("Directorate Enforcer", "Elite", H(2.05, "brute"), "Ark Directorate",
     role="Heavy armor, riot shield and minigun.", gp={"hp": 900, "weapons": "Minigun, riot shield"},
     look="A walking wall: bulky powered armor, tower shield.", outfit=("Enforcer Armor", "Powered heavy armor with a riot shield (separate prop mesh).", ["Powered armor", "Shield", "Minigun"]),
     notes="Powered armor adds 0.2 m of height; the body inside is a standard adult.")
unit("Directorate Medic", "Crowd", H(1.75), "Ark Directorate",
     role="Revives troopers; priority target.", gp={"hp": 150, "weapons": "SMG, revive beam"},
     look="Trooper armor with blue medical crosses and a backpack medical drone dock.", outfit=("Medic Armor", "Trooper armor, blue crosses, medical backpack.", ["Trooper armor", "Medical backpack"]))
unit("Directorate Officer", "Secondary", H(1.80), "Ark Directorate",
     role="Buffs nearby troops; can be interrogated if subdued.", gp={"hp": 160, "weapons": "Pistol"}, face_visible=True,
     look="Grey officer uniform, gold rank bar, cap; face visible (interrogation scenes).", outfit=("Officer Uniform", "Grey uniform with gold rank bar and officer's cap.", ["Uniform", "Cap", "Boots", "Sidearm"]))
unit("Directorate Pilot", "Crowd", H(1.76), "Ark Directorate",
     role="Shuttle and fighter crews (Seraph crew, Convergence).", look="Flight suit like Ada's without her commander marks.",
     outfit=("Flight Suit", "White-and-gold flight suit and helmet.", ["Flight suit", "Helmet"]))
unit("Directorate Cleanup Crew", "Crowd", H(1.78), "Ark Directorate",
     role="'Sterilization' teams burning survivors in Act I (M1.05).", gp={"hp": 140, "weapons": "Flamethrower"},
     look="White hazmat suits with gold hoods, flamethrower tanks; faceless.", outfit=("Cleanup Hazmat", "Sealed white hazmat suit with a gold hood and flamethrower tanks.", ["Hazmat suit", "Hood", "Tank pack"]))
unit("Directorate Sentinel Drone", "Creature-S", {"template": "drone", "size": 0.8}, "Ark Directorate",
     role="Flying spotlight-and-taser drone; alerts troopers.", gp={"hp": 80, "weapons": "Taser, spotlight"}, infection=False,
     look="Smooth white lozenge with four ducted rotors and a gold sensor eye.", outfit=("Drone Shell", "White ceramic shell, ducted rotors, spotlight.", ["Shell", "Rotors ×4", "Gun pod"]))
unit("Choir Pilgrim", "Crowd", H(1.72), "The Choir",
     role="Choir members: unsettlingly kind; can fight with spore bombs.", gp={"hp": 120, "weapons": "Spore bombs, staffs"}, face_visible=True,
     look="Stitched robes over patched EVA suits, moss armor, candle lanterns; faint green veins (Stage 2).",
     outfit=("Pilgrim Robes", "Layered undyed robes over an EVA suit with moss armor and a candle lantern.", ["Robes", "EVA undersuit", "Moss armor", "Lantern"]),
     notes="Stage-2 infection look is permanent (INF_Veins 0.4).")
unit("Choir Warden", "Secondary", H(1.85, "adult_broad"), "The Choir",
     role="Guards the Cathedral of the Hum.", gp={"hp": 300, "weapons": "Resonance staff"}, face_visible=True,
     look="Taller pilgrim with bark-like moss armor and a staff hung with seed pods.", outfit=("Warden Robes", "Heavy robes, bark-moss armor, seed-pod staff.", ["Robes", "Moss armor", "Staff"]))
unit("Hauler Deckhand", "Crowd", H(1.78), "Free Haulers",
     role="Crew of Hauler ships and Tortuga Drift; traders, brawlers, boarders.", gp={"hp": 130, "weapons": "Shotgun, wrench"}, face_visible=True,
     look="Cargo-orange coveralls covered in stickers, mismatched armor, goggles.", outfit=("Hauler Coveralls", "Cargo-orange coveralls with stickers and a patched vest.", ["Coveralls", "Vest", "Goggles", "Boots"]))
unit("Hauler Trader", "Secondary", H(1.74), "Free Haulers",
     role="Market vendors and contract brokers at Tortuga Drift.", face_visible=True,
     look="Long coat with container-rib armor panels, lots of jewelry, a data slate.", outfit=("Trader Coat", "Long coat, jewelry, data slate.", ["Coat", "Shirt", "Trousers", "Jewelry"]))

# ---------------------------------------------------------------------------
# BOS — Bosses
# ---------------------------------------------------------------------------
CH("BOS", "Ada — Seraph Exo-frame", key="ada_seraph_exoframe", title="M4.03 (if Ada stayed loyal)", tier="Boss", skeleton=H(3.0, "exoframe"),
   pronouns="she/her (pilot)", infection=False, facial_capture=True, art="DIR",
   role="Ada inside a Directorate Seraph exo-frame: a two-phase sibling duel on the Seedship's living bridges.",
   visual={"silhouette": "A 3 m white-and-gold armored frame shaped like the Seraph shuttle's wings; an open cockpit shows Ada's face.",
           "phases": "Phase 1 — full armor, wing blades, shoulder cannons. Phase 2 — armor torn open, Ada visible and exposed; the frame limps.",
           "weak_points": "Wing actuators, then the exposed cockpit (talk-down window)."},
   gameplay={"hp": 6000, "phases": 2, "talk_down": "Play her pre-flight recording with ada_bond above the threshold"},
   outfits=[O("Phase1", "Full Armor", "M4.03", "Pristine white-gold armor, folded wing blades."), O("Phase2", "Torn Armor", "M4.03", "Damaged armor mesh swap; cockpit canopy gone.")],
   extra_bones=["wing_blade_l/r (3 bones each)", "cannon_l/r", "cockpit_canopy", "pilot_attach (Ada's skeleton rides here)"],
   notes="Ada's Hero model sits in the cockpit (pilot_attach socket) with her facial rig live for the talk-down.")

CH("BOS", "Crane — The Director", key="crane_director", title="M4.04 Phase 1", tier="Boss", skeleton=H(2.05, "adult_athletic"), pronouns="he/him",
   infection=False, facial_capture=True, art="DIR",
   role="Crane in augmented Directorate armor commanding drones.",
   visual={"silhouette": "White-gold powered armor over his slim frame; face bare, silver hair perfect; four drones orbiting.",
           "weak_points": "Drone links (EMP), back power spine."},
   gameplay={"hp": 5000, "summons": "4 Sentinel Drones, trooper waves"},
   outfits=[O("AugmentedArmor", "Augmented Armor", "M4.04", "Powered armor adding 0.19 m of height; the Director's head exposed.")],
   notes="Shares the head with Crane (CST) for continuity across the phases.")

CH("BOS", "Crane — The Graft", key="crane_graft", title="M4.04 Phase 2", tier="Boss", skeleton=H(2.4, "brute"), pronouns="he/him",
   infection=False, facial_capture=True,
   role="Crane half-merged with Bloom growths as the Loom rejects his imperfect mark; the arena fights with him.",
   visual={"silhouette": "Armor split open by Bloom growth; one arm a mass of tendrils; half his face still Crane.",
           "weak_points": "Graft nodes (fire ×2) at the shoulder, spine and tendril root."},
   gameplay={"hp": 7000, "attacks": "Tendril sweeps, spore bursts, Hollows from the walls"},
   outfits=[O("GraftArmor", "Graft", "M4.04", "The augmented armor mesh with Bloom-growth breakthroughs (separate growth meshes on attach bones).")],
   extra_bones=["tendril_r_01…08", "growth_spine_01…04"],
   notes="Transition from Phase 1 is a shape-key and growth-mesh sequence on the same head.")

CH("BOS", "Crane — The Bonsai", key="crane_bonsai", title="M4.04 Phase 3", tier="Boss", skeleton=H(12.0, "colossus"), pronouns="he/him",
   infection=False, facial_capture=True,
   role="Crane's consciousness inside the Loom mind-space: a colossal spectral gardener pruning a bonsai the size of a world.",
   visual={"silhouette": "A 12 m translucent Crane made of light and root-lines, holding giant silver shears.",
           "weak_points": "The shears; protecting the branches that hold cities.",
           "environment": "Plays on the Bonsai arena (level asset): branches are platforms; each cut branch darkens a city below."},
   gameplay={"hp": 9000, "talk_down": "crane_stance not defiant + all 6 personal logs"},
   outfits=[O("Spectral", "Spectral Gardener", "M4.04", "Crane's CST head and body scaled up with the hologram-light material and root-line overlays.")],
   extra_bones=["shears_blade_l/r"],
   notes="Uses Crane's base topology at 12 m scale (the talk-down is a close-up on his face).")
