"""CRE — creatures & fauna: Tessari, Earth animals, procedural Drift fauna kits, memory-garden creatures."""

from . import CH, H, O


def creature(name, tier, skel, *, role, look, palette, anim, audio, where, gp=None, outfits=(), variants=(), notes="", extra_bones=(), fur=""):
    CH("CRE", name, tier=tier, skeleton=skel, pronouns="—", infection=False, role=role, appears=where,
       visual={"silhouette": look, "palette": palette, "acting": anim, "audio": audio, "fur": fur},
       gameplay=gp or {}, outfits=list(outfits), variants=list(variants), notes=notes, extra_bones=list(extra_bones))


creature("Tessari (Adult)", "Creature-L", {"template": "hexapod", "shoulder_h": 3.6, "hip_h": 3.2, "length": 7.0, "neck": 1.8, "head": 1.1, "tail": 2.0},
         role="Gentle six-limbed megafauna native to Veyra-4, dying under the Garden Engine. Can be saved, milked and sheltered (Tessari Sanctuary).",
         where="Veyra-4 (M3.03), Memory Garden 1 (M4.02), Tessari Sanctuary (post-M3.03)",
         look="Elephant-scale grazer with six legs, a long neck and a broad, gentle head with four soft eyes; a shaggy violet mane down the spine.",
         palette=[("Hide slate-blue", "#56657A"), ("Mane violet", "#6A4C93"), ("Belly cream", "#E8E0CF"), ("Eye amber", "#E0A030")],
         anim="Six-leg gait cycle (walk, trot), grazing, herd-call, calf-nuzzle, lying down.", audio="Low whale-like calls; soft chuffing.",
         gp={"hp": 3000, "behaviour": "Herd grazer; protective of calves; never attacks first"},
         variants=[("Bloomed", "Dying Tessari overgrown by the Garden Engine's Bloom (Veyra before healing)")],
         fur="Mane uses fur cards (8k tris) plus a shell-fur shader on the body.",
         notes="Hero creature for Act III. The hexapod template's middle leg pair attaches at spine_02.")

creature("Tessari (Calf)", "Creature-L", {"template": "hexapod", "shoulder_h": 1.6, "hip_h": 1.4, "length": 3.0, "neck": 0.9, "head": 0.6, "tail": 0.9},
         role="Young Tessari: follows the player once healed, lives in the Livestock Pen (parts bible AGR-007).",
         where="Veyra-4, Tessari Sanctuary, colony pens",
         look="Big-headed, knock-kneed miniature of the adult with a fluffy mane.", palette=[("Hide pale blue", "#8FA3BF"), ("Mane lilac", "#A28BC4")],
         anim="Wobbly six-leg gait, play, sleep curled up.", audio="Squeaky calls.", fur="Fluffier fur cards.",
         notes="Shares the adult's topology with calf proportions (separate skeleton scale).")

creature("Dog", "Creature-S", {"template": "quadruped", "shoulder_h": 0.55, "length": 0.95, "neck": 0.25, "head": 0.25, "tail": 0.35},
         role="Township strays fed by Danny; become colony pets (Hearthside update).", where="Kestrel Township (I), colony (II+)",
         look="Medium mutt; four coat and breed variants on one base.", palette=[("Tan", "#C19A6B"), ("Black", "#222222"), ("White", "#F2F2F2")],
         anim="Full pet set: walk, run, sit, beg, sleep, fetch.", audio="Barks, whines, panting.", fur="Fur cards (4k tris) + shell shader.",
         variants=[("Shepherd", "Shepherd mix"), ("Terrier", "Scruffy terrier mix"), ("Hound", "Lean hound mix")],
         notes="There are no Hollow dogs: pets are always safe.")

creature("Coyote", "Creature-S", {"template": "quadruped", "shoulder_h": 0.6, "length": 1.1, "neck": 0.25, "head": 0.25, "tail": 0.4},
         role="Kestrel Valley wildlife; its Bloom variant is Earth's Stalker equivalent.", where="Kestrel Valley (open world)",
         look="Lean desert coyote.", palette=[("Desert tan", "#B08D57"), ("Grey", "#8A8A8A")],
         anim="Trot, howl, pack circling.", audio="Yips and howls.", fur="Fur cards.",
         gp={"hp": 60, "behaviour": "Skittish; packs at night"},
         variants=[("Hollow", "Bloom-mutated: spine ridges, split jaw, glowing eyes (Hollow Coyote, hp 140)")])

creature("Crow", "Creature-S", {"template": "flyer", "shoulder_h": 0.12, "length": 0.35, "wings": 0.4, "neck": 0.06, "head": 0.07, "tail": 0.12},
         role="Ambient Earth bird; flocks mark carrion and Hollow activity (a readable open-world cue).", where="Kestrel Valley",
         look="Glossy black crow.", palette=[("Black", "#111111"), ("Blue sheen", "#2B3A67")],
         anim="Hop, peck, take-off, glide, flock.", audio="Caws.", fur="Feather cards on wings and tail.")

creature("Jackrabbit", "Creature-S", {"template": "quadruped", "shoulder_h": 0.25, "length": 0.5, "neck": 0.08, "head": 0.1, "tail": 0.05},
         role="Ambient wildlife and early food source (Jackrabbit Flats).", where="Kestrel Valley",
         look="Long-eared desert hare.", palette=[("Sand", "#C9B28A"), ("Ear pink", "#E0A9A0")],
         anim="Hop, freeze, bolt.", audio="Rustle.", fur="Fur cards.")

creature("Wild Horse", "Creature-L", {"template": "quadruped", "shoulder_h": 1.5, "length": 2.4, "neck": 0.8, "head": 0.6, "tail": 0.8},
         role="Feral horses in Kestrel Valley; can be tamed as mounts in the post-launch 'Return to Earth' expansion.", where="Kestrel Valley",
         look="Mustang with a wind-tangled mane.", palette=[("Bay", "#6B3E26"), ("Dun", "#C8A165"), ("Grey", "#9FA3A6")],
         anim="Walk, trot, gallop, rear, graze.", audio="Whinnies, hoofbeats.", fur="Mane and tail cards.")

# --- Procedural Drift fauna kits -------------------------------------------------
def kit(name, skel, role, modules, look, anim):
    creature(name, "Creature-L", skel, role=role, where="The Drift (procedural planets)", look=look,
             palette=[("Per planet", "Generated palette (4 colors)")], anim=anim, audio="Procedural voice synth per species",
             outfits=[O("Modules", "Kit modules", "Act III+", "Interchangeable parts that snap onto the kit skeleton.", modules)],
             notes="Every module shares the kit's skeleton and snap sockets; species are assembled at runtime from a seed. Bloom variants use the shared Bloom overlay.")


kit("Fauna Kit — Grazer", {"template": "quadruped", "shoulder_h": 1.8, "length": 3.5},
    "Herd herbivores of Drift planets.", ["Bodies ×6", "Heads ×10", "Legs ×6 sets", "Tails ×6", "Horns and crests ×12", "Pattern masks ×16"],
    "Barrel bodies, long necks, crests; 1–3 m at the shoulder by scale.", "Walk, graze, flee, herd.")
kit("Fauna Kit — Predator", {"template": "quadruped", "shoulder_h": 1.4, "length": 3.2},
    "Drift predators; each has a Bloom 'Stalker' variant.", ["Bodies ×5", "Heads ×8 (jaw variants)", "Legs ×5 sets", "Tails ×5", "Spines and frills ×10", "Pattern masks ×16"],
    "Low-slung, muscular, forward-facing eyes.", "Stalk, pounce, fight, eat.")
kit("Fauna Kit — Flyer", {"template": "flyer", "shoulder_h": 0.6, "length": 1.4, "wings": 1.6},
    "Birds, gliders and sky-rays.", ["Bodies ×5", "Heads ×8", "Wings ×8 (membrane and feather)", "Tails ×6", "Pattern masks ×12"],
    "Light bodies, broad wings or membranes.", "Flap, glide, land, flock.")
kit("Fauna Kit — Burrower", {"template": "serpentine", "length": 4.0, "height": 0.4},
    "Serpentine diggers and sand-swimmers.", ["Bodies ×4", "Heads ×6 (drill, maw)", "Fins and plates ×8", "Pattern masks ×10"],
    "Segmented, armored heads.", "Burrow, surface, strike.")
kit("Fauna Kit — Hexapod", {"template": "hexapod", "shoulder_h": 1.2, "length": 2.5},
    "Six-limbed species (Tessari cousins) and large insects.", ["Bodies ×4", "Heads ×6", "Legs ×4 sets (6)", "Carapaces ×8", "Pattern masks ×12"],
    "Six legs, carapace or hide.", "Six-leg gait set, feed, threat display.")

# --- Memory-garden creatures (M4.02) ------------------------------------------------
creature("Gorgonopsid (Permian)", "Creature-L", {"template": "quadruped", "shoulder_h": 0.9, "length": 3.0, "neck": 0.4, "head": 0.55, "tail": 0.8},
         role="Permian predator seen in Memory Garden 4, covered in the Bloom of the first harvest.", where="M4.02 Memory Garden 4 (Permian Earth)",
         look="Saber-toothed synapsid; Bloom crusting its back.", palette=[("Hide ochre", "#9C6B3C"), ("Bloom green", "#7FD06B")],
         anim="Prowl, roar, collapse into Bloom.", audio="Rasping roar.", variants=[("Bloomed", "Covered in first-harvest Bloom")],
         notes="Paleontology consultant reviews the base model.")
creature("Dicynodont (Permian)", "Creature-L", {"template": "quadruped", "shoulder_h": 0.8, "length": 2.5, "neck": 0.3, "head": 0.45, "tail": 0.3},
         role="Permian grazer in Memory Garden 4; herds dying in the burning sky.", where="M4.02 Memory Garden 4",
         look="Stocky, beaked, tusked herbivore.", palette=[("Hide olive", "#6B6B3A")], anim="Walk, graze, stumble.", audio="Honks and grunts.",
         variants=[("Bloomed", "Covered in first-harvest Bloom")])
creature("Drowned Choir Singer", "Creature-L", {"template": "cetacean", "length": 22.0, "girth": 5.0},
         role="The whale-like people the Sowers harvested before they understood; seen in Memory Garden 2. Their song is why the Sowers stopped.",
         where="M4.02 Memory Garden 2",
         look="22 m cetacean with bioluminescent song-patterns along its flanks and gentle, intelligent eyes.",
         palette=[("Deep indigo", "#1D2B53"), ("Song glow", "#7DF9FF"), ("Belly pearl", "#E9E4DA")],
         anim="Slow swim, song pose (patterns ripple), family groups.", audio="Layered song (a key musical motif).",
         notes="Emissive song-patterns are driven by an audio-reactive mask.")
creature("Sower Echo", "Secondary", H(2.8, "adult_slim"),
         role="A memory of a Sower in the First Garden (M4.02): tall, luminous beings of shell and filament. Never fought; only witnessed.",
         where="M4.02 Memory Garden 3 (the First Garden)",
         look="Elongated, graceful humanoid made of pearl shell plates and glowing filaments; no mouth, eyes like teal lamps.",
         palette=[("Shell pearl", "#E9E4DA"), ("Glyph teal", "#2EE6D6"), ("Violet", "#3A2A5C")],
         anim="Slow gestures of tending plants; a final 'bowing' pose.", audio="Choral breath.",
         notes="Uses the Sower material master with translucency. Performance-captured by a dancer.")
