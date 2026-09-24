"""NOT — notable survivors (12 fully voiced), the 28 text-and-bark notables, and the
modular kit that generates every procedural survivor."""

from . import CH, H, O


def notable(name, age, pronouns, height, profile, *, job, found, traits, skills, quest, voice, look, face, hair, palette,
            props, outfit, acting, pieces=(), key=None, notes=""):
    CH("NOT", name, key=key, title=job, tier="Secondary", skeleton=H(height, profile), age=age, pronouns=pronouns,
       role=f"{job}. Found: {found}. Traits: {traits}. Skills: {skills}.",
       appears=found,
       story={"arc": quest},
       voice=voice,
       visual={"silhouette": look, "face": face, "hair": hair, "body": f"{height:.2f} m, {profile.replace('_', ' ')}",
               "palette": palette, "props": props, "acting": acting},
       outfits=[O("Signature", outfit[0], "From recruitment", outfit[1], pieces),
                O("ColonyWear", "Colony Wear", "Act II+", "Colony-made clothes in their palette (modular kit pieces with a unique top).", ["Unique top", "Kit bottoms", "Kit shoes"]),
                O("EVA", "EVA Suit", "Act II+ (EVA)", "Shared EVA suit.", shared="SK_SUIT_EVASuit")],
       hair=[("Signature", hair, "cards")], notes=notes)


notable("Danny Ruiz", "46", "he/him", 1.75, "adult_broad",
        job="Diner cook", found="Kestrel Township diner roof (M1.05), feeding stray dogs",
        traits="Comfort Eater, Optimist", skills="Cooking ★★★★, Social ★★★",
        quest="Rebuild his grandmother's recipe book from memory and scavenged pages; ends with a Feast that heals a colony rift.",
        voice="Warm Tex-Mex cadence, big laugh, never out of jokes about coffee.",
        look="Round, apron over a bowling shirt, towel on the shoulder.", face="Warm tan skin, round cheeks, thick mustache, smile lines.",
        hair="Slicked-back black hair, greying at the temples", palette=[("Diner red", "#C1272D"), ("Apron white", "#F2F2F2"), ("Bowling teal", "#2B7A78")],
        props=["Spatula", "Grandmother's recipe book (quest item)", "Dog biscuits"],
        outfit=("Diner Whites", "Stained apron, short-sleeve bowling shirt, check trousers, non-slip shoes."),
        pieces=["Apron", "Bowling shirt", "Trousers", "Shoes"], acting="Feeds people when he's worried.")

notable("Priya Nair", "38", "she/her", 1.62, "adult_slim",
        job="Air-traffic controller", found="Mission Control tower (M1.05)",
        traits="Perfectionist, Claustrophobic", skills="Logistics ★★★★, Piloting ★★",
        quest="Build the colony's first traffic-control room with a big window; she finally sleeps through the night.",
        voice="Precise, clipped, dry wit; talks faster under stress.",
        look="Headset around the neck, cardigan, lanyard; always holding a clipboard or tablet.", face="Brown skin, sharp eyes, small nose stud.",
        hair="Long black hair in a practical braid", palette=[("Cardigan plum", "#6B3E5E"), ("Headset black", "#1B1B1B"), ("Kestrel orange", "#F26B1D")],
        props=["Headset", "Tablet", "Stress ball"], outfit=("Tower Shift", "Cardigan over a Kestrel polo, slacks, flats, headset."),
        pieces=["Cardigan", "Polo", "Slacks", "Flats", "Headset"], acting="Counts under her breath in small rooms.")

notable("Walt Hennessey", "74", "he/him", 1.76, "elder",
        job="Retired astronaut", found="Fuel Farm office with his telescope (M1.05)",
        traits="Frail, Storyteller", skills="Piloting ★★★★ (teaches), Social ★★★",
        quest="Keeps a pre-2071 log about Styx; teaches Lily to fly; the 'Walt's Window' emergent story.",
        voice="Gravelly, slow, twinkling; tells the same story three ways.",
        look="Stooped, a vintage NASA flight jacket covered in mission patches, cane.", face="Pale, heavily lined skin, bright blue eyes, big ears.",
        hair="Thin white hair, neatly combed", palette=[("Flight-jacket navy", "#1C2841"), ("Patch colors", "#D9A441"), ("Cardigan cream", "#EFE6D2")],
        props=["Cane", "Telescope", "Worn mission patches", "Pre-2071 logbook"],
        outfit=("Old Flight Jacket", "NASA-style flight jacket with patches, cardigan, pressed trousers, orthopedic shoes."),
        pieces=["Flight jacket", "Cardigan", "Trousers", "Shoes"], acting="Stooped walk set; points at stars.")

notable("Aiyana Two Rivers", "33", "she/her", 1.69, "adult_athletic",
        job="Park ranger", found="Route 93, holding a highway overpass alone (M1.05)",
        traits="Outdoorsy, Sharpshooter", skills="Combat ★★★★, Scouting ★★★★",
        quest="Map every safe route in Kestrel Valley and find her missing brother's ranger station.",
        voice="Quiet, economical, deadpan humor.",
        look="Ranger uniform with a wide-brim hat, rifle sling, binoculars.", face="Brown skin, strong cheekbones, sun lines, calm eyes.",
        hair="Long black hair in a low braid", palette=[("Ranger green", "#4B5E3C"), ("Khaki", "#B7A77A"), ("Turquoise", "#40B0A6")],
        props=["Scoped rifle", "Binoculars", "Hand-drawn valley map", "Turquoise bracelet from her brother"],
        outfit=("Ranger Uniform", "Park-ranger shirt and trousers, fleece, wide-brim hat, boots."),
        pieces=["Ranger shirt", "Trousers", "Fleece", "Hat", "Boots"], acting="Scans the horizon; kneels to read tracks.",
        notes="Designed with an Indigenous consultant (game bible 17 §17.8); regalia and symbols are not used as decoration.")

notable("Marcus Webb", "41", "he/him", 1.85, "adult_average",
        job="High-school history teacher", found="Township library with Joel (M1.05)",
        traits="Bonded (with Joel), Optimist", skills="Teaching ★★★★, Social ★★★",
        quest="Start the colony school with Lily as his first student; a vow-renewal event with Joel.",
        voice="Warm, articulate, a born storyteller.",
        look="Cardigan, rolled sleeves, a satchel of rescued books.", face="Dark skin, neat beard, glasses, warm eyes.",
        hair="Short cropped hair", palette=[("Cardigan olive", "#6B7B3A"), ("Shirt blue", "#8FB3D9"), ("Satchel brown", "#6B4A2F")],
        props=["Book satchel", "Glasses", "Matching wedding ring (with Joel)"],
        outfit=("Teacher's Cardigan", "Olive cardigan, oxford shirt, chinos, loafers."), pieces=["Cardigan", "Shirt", "Chinos", "Loafers"],
        acting="Talks with his hands; always holding Joel's hand in safe scenes.")

notable("Joel Webb", "39", "he/him", 1.73, "adult_slim",
        job="ER nurse", found="Township library with Marcus (M1.05)",
        traits="Bonded (with Marcus), Light Sleeper", skills="Medicine ★★★★",
        quest="Build a real medbay and train medics; the one who talks survivors through amputations.",
        voice="Calm, practical, gallows humor.",
        look="Scrubs under a hoodie, stethoscope, trauma shears on the belt.", face="Pale skin with freckles, tired eyes, wedding ring.",
        hair="Curly red hair, short", palette=[("Scrub navy", "#243B6B"), ("Hoodie grey", "#8A8D91"), ("Ginger", "#B5532B")],
        props=["Stethoscope", "Trauma shears", "Matching wedding ring (with Marcus)"],
        outfit=("Scrubs & Hoodie", "Navy scrubs, grey hoodie, clogs, stethoscope."), pieces=["Scrubs", "Hoodie", "Clogs"],
        acting="Checks everyone's pupils without asking.")

notable("Dr. Kenji Mori", "52", "he/him", 1.70, "adult_average", key="kenji_mori",
        job="Veterinarian", found="Township animal clinic (M1.02 area), with a clinic full of rescued animals",
        traits="Gentle, Night Owl", skills="Medicine ★★★ (animals ★★★★★), Botany ★★",
        quest="Cares for the dogs from the Township and later the Tessari calves; builds the Tessari Sanctuary.",
        voice="Soft-spoken, precise, delighted by animals.",
        look="Vet coat, rolled sleeves, a dog leash always in hand.", face="Light skin, glasses, grey stubble, gentle face.",
        hair="Salt-and-pepper, short and messy", palette=[("Vet green", "#5F8A6B"), ("Coat white", "#F3F3F3"), ("Leash red", "#B3261E")],
        props=["Dog leash", "Glasses", "Treat pouch"], outfit=("Vet Coat", "Short vet coat over a sweater, jeans, clogs."), pieces=["Vet coat", "Sweater", "Jeans", "Clogs"],
        acting="Kneels to animal eye level; talks to creatures, not people, when stressed.")

notable("Rosa Delgado", "57", "she/her", 1.60, "adult_broad",
        job="Hardware-store owner and welder", found="Delgado Hardware, Township (M1.05)",
        traits="Handy, Stubborn", skills="Engineering ★★★★, Mechanics ★★★",
        quest="Rebuilds her late husband's welding rig; becomes Tug's rival and then his best friend.",
        voice="Loud, blunt, laughs like a machine gun.",
        look="Welding apron, leather gloves tucked in the belt, safety glasses pushed up.", face="Tan skin, strong jaw, burn scars on her hands.",
        hair="Short grey pixie cut", palette=[("Apron leather", "#6E4B2A"), ("Flannel red", "#A4262C"), ("Safety yellow", "#F5C518")],
        props=["Welding helmet", "Safety glasses", "Husband's old lighter"], outfit=("Welder's Apron", "Leather apron over flannel, jeans, steel-toe boots."),
        pieces=["Leather apron", "Flannel shirt", "Jeans", "Boots"], acting="Hands on hips; points with tools.")

notable("Theo Park", "16", "he/him", 1.72, "teen",
        job="High-school student and skateboarder", found="Skate park, Township (M1.05)",
        traits="Reckless, Loyal", skills="Scouting ★★, learns fast",
        quest="Becomes Lily's big-brother figure; the colony's first teenage scout; builds a skate ramp in zero-G.",
        voice="Fast, sarcastic, secretly scared.",
        look="Oversized hoodie, beanie, skateboard on his back.", face="Light-tan skin, a few acne marks, braces.",
        hair="Dyed-blue shaggy hair fading out", palette=[("Hoodie black", "#1C1C1C"), ("Faded blue", "#5B8DB8"), ("Sticker neon", "#C6FF3C")],
        props=["Skateboard (back socket)", "Earbuds", "Sticker-covered phone"], outfit=("Skater", "Oversized hoodie, ripped jeans, skate shoes, beanie."),
        pieces=["Hoodie", "Jeans", "Skate shoes", "Beanie"], acting="Never stands still; fidgets with the board.",
        notes="Teen: child-character injury rules apply (no graphic damage, no Hollow version).")

notable("Fatima Haddad", "29", "she/her", 1.66, "adult_slim",
        job="Kestrel radio operator", found="Red Mesa Observatory, keeping the transmitters alive (Act I)",
        traits="Curious, Insomniac", skills="Research ★★★, Radio ★★★★",
        quest="Decodes the Styx beacon's second answer (a sequel hook) and runs the colony radio show.",
        voice="Bright, nerdy, talks to herself while decoding.",
        look="Headphones, fingerless gloves, a jacket covered in radio-club pins.", face="Olive skin, big dark eyes, a small scar on the chin.",
        hair="Curly dark hair in a messy bun under the headphones", palette=[("Jacket olive", "#556B2F"), ("Pin enamel red", "#D7263D"), ("Headphone grey", "#6C6F73")],
        props=["Headphones", "Handheld receiver", "Notebook of frequencies"], outfit=("Radio Shack Chic", "Bomber jacket with pins, band T-shirt, cargo pants, boots."),
        pieces=["Bomber jacket", "T-shirt", "Cargo pants", "Boots"], acting="Freezes mid-sentence to listen.")

notable("Maurice \"Big Mo\" Jackson", "50", "he/him", 1.93, "adult_broad", key="maurice_jackson",
        job="Long-haul trucker", found="Route 93 truck stop, in his fortified rig (M1.05)",
        traits="Calm, Comfort Eater", skills="Driving ★★★★★, Mechanics ★★★",
        quest="Converts his rig's cab into the colony's first rover; later a natural with the Haulers.",
        voice="Deep, slow, unshakable; a CB-radio vocabulary.",
        look="Trucker cap, denim jacket with sheepskin collar, huge frame.", face="Dark skin, grey goatee, heavy brows, laugh lines.",
        hair="Shaved head under the cap; grey goatee", palette=[("Denim", "#3B5B7E"), ("Sheepskin", "#D8C3A5"), ("Cap red", "#A4262C")],
        props=["CB radio handset", "Thermos", "Truck keys on a big ring"], outfit=("Long-Haul", "Denim jacket with sheepskin collar, flannel, jeans, boots, trucker cap."),
        pieces=["Denim jacket", "Flannel", "Jeans", "Boots", "Cap"], acting="Slow, deliberate; leans on door frames.")

notable("Hannah Lindqvist", "35", "she/her", 1.78, "adult_athletic",
        job="Mine geologist", found="Silver Ridge Mines, sealed in a shaft refuge (Act I)",
        traits="Perfectionist, Brave", skills="Mining ★★★★, Research ★★★",
        quest="Surveys the Moon and the Drift; first to realize Bloom Hearts grow along ore veins.",
        voice="Precise, dry, Swedish-American.",
        look="Mining hard hat with a lamp, hi-vis coveralls, rock hammer.", face="Pale skin, wind-burned cheeks, blue-grey eyes.",
        hair="Blond hair in a tight French braid", palette=[("Hi-vis orange", "#FF7A00"), ("Coverall grey", "#6D7278"), ("Rock dust", "#A89F91")],
        props=["Rock hammer", "Hard hat with lamp", "Sample bags"], outfit=("Mine Coveralls", "Hi-vis mining coveralls, reflective tape, hard hat, steel-toe boots."),
        pieces=["Coveralls", "Hard hat", "Boots", "Belt with sample bags"], acting="Taps walls with her hammer, listening.")

# ---------------------------------------------------------------------------
# The 28 text-and-bark notable survivors (Secondary-lite: kit bodies + one unique piece each)
# (name, age, pronouns, job, where found, traits, look, body preset)
# ---------------------------------------------------------------------------
MORE_SURVIVORS = [
    ("Omar Farouk", 44, "he/him", "Pharmacist", "Township pharmacy (I)", "Careful, Hides Wounds", "Pharmacy smock, reading glasses, grey beard", "adult_average"),
    ("Beth Callahan", 52, "she/her", "School-bus driver", "Kestrel Elementary bus lot (I)", "Protective, Loud", "Bus-driver windbreaker, whistle, sunglasses", "adult_broad"),
    ("Luis Ortega", 19, "he/him", "Apprentice mechanic (Tug's protégé)", "Hangar 2 (I)", "Handy, Reckless", "Grease-stained coveralls, backwards cap", "adult_slim"),
    ("Grace Liu", 31, "she/her", "Software engineer", "Kestrel offices (I)", "Genius, Night Owl", "Hoodie, big headphones, laptop stickers", "adult_slim"),
    ("Samuel Adebayo", 45, "he/him", "Security supervisor", "Kestrel gatehouse (I)", "Disciplined, Pessimist", "Security uniform, radio, reading glasses", "adult_broad"),
    ("Tanya Volkova", 36, "she/her", "Helicopter pilot", "Kestrel helipad (I)", "Spacer, Gambler", "Flight jacket, aviators, braid", "adult_athletic"),
    ("Eddie \"Sparks\" Morales", 40, "he/him", "Electrician", "Substation 2 (I)", "Handy, Comfort Eater", "Tool vest, voltage tester, headlamp", "adult_average"),
    ("June Whitaker", 63, "she/her", "Librarian", "Township library (I)", "Storyteller, Frail", "Cardigan, pearl necklace, reading glasses", "elder"),
    ("Ravi Patel", 55, "he/him", "Gas-station owner", "Route 93 gas station (I)", "Optimist, Stubborn", "Polo shirt with name tag, cap", "adult_average"),
    ("Nora Kelly", 27, "she/her", "Ranch hand", "Jackrabbit Flats ranch (I)", "Outdoorsy, Brave", "Flannel, cowboy boots, rope", "adult_athletic"),
    ("Pete Hollis", 61, "he/him", "Dam engineer", "Hollis Dam control room (I)", "Perfectionist, Light Sleeper", "Hard hat, pocket protector, suspenders", "elder"),
    ("Ingrid Sørensen", 42, "she/her", "Meteorologist", "Kestrel weather station (I)", "Curious, Claustrophobic", "Windbreaker, anemometer, beanie", "adult_slim"),
    ("Kwame Mensah", 48, "he/him", "Structural engineer", "Prospect overpass camp (I)", "Perfectionist, Calm", "Hard hat, blueprint tube, reflective vest", "adult_average"),
    ("Lucy Tran", 15, "she/her", "High-school student", "Route 93 truck stop (I)", "Curious, Survivor's Guilt", "Oversized band T-shirt, braces, backpack", "teen"),
    ("Abe Goldstein", 68, "he/him", "Retired machinist", "Township workshop (I)", "Handy, Storyteller", "Shop apron, bifocals, suspenders", "elder"),
    ("Carmen Reyes", 34, "she/her", "Paramedic", "Crashed ambulance, Route 93 (I)", "Brave, Hides Wounds", "Paramedic uniform, trauma bag", "adult_athletic"),
    ("Dr. Olga Ivanova", 50, "she/her", "Haven-9 biologist", "Haven-9 escape pod (II)", "Spacer, Survivor's Guilt", "Haven-9 crew jumpsuit, frostbitten fingers", "adult_slim"),
    ("Felix Brandt", 38, "he/him", "Tycho miner", "Tycho refuge (II)", "Spacer, Pessimist", "Mining EVA undersuit, tattoos", "adult_broad"),
    ("Dmitri Petrov", 46, "he/him", "Hauler engineer", "Tortuga Drift (III)", "Gambler, Handy", "Hauler coveralls with stickers", "adult_average"),
    ("Yusuf Kaya", 39, "he/him", "Hauler cook", "Tortuga Drift (III)", "Comfort Eater, Optimist", "Chef's jacket over EVA undersuit", "adult_broad"),
    ("Sunny Kapoor", 30, "they/them", "Tortuga bartender", "Tortuga Drift (III)", "Charismatic, Night Owl", "Vest with pins, rings, undercut", "adult_slim"),
    ("Selene Moreau", 28, "she/her", "Choir defector", "Hollowmere outskirts (III)", "Choir-Curious, Brave", "Stitched robe over EVA, moss traces", "adult_slim"),
    ("Tomas Vega", 35, "he/him", "Choir defector", "Choir shrine (III)", "Pacifist, Storyteller", "Undyed robe, seed beads", "adult_average"),
    ("Jade Okonkwo", 32, "she/her", "Directorate engineer (defector)", "Ark Meridian (III)", "Genius, Distrustful", "Directorate engineering jumpsuit, insignia removed", "adult_average"),
    ("Hector Salazar", 26, "he/him", "Freed Null carrier", "Ark Meridian labs (III)", "Resilient, Nightmares", "Prisoner gown, then colony wear", "adult_slim"),
    ("Amara Diallo", 17, "she/her", "Freed Null carrier", "Ark Meridian labs (III)", "Resilient, Curious", "Prisoner gown, then Lily-style painted jacket", "teen"),
    ("Ben Hargrove", 58, "he/him", "Rancher", "Jackrabbit Flats (I)", "Stubborn, Outdoorsy", "Stetson, sheepskin vest", "adult_broad"),
    ("Miguel \"Chuy\" Ibarra", 20, "he/him", "Army private", "Fort Calder barracks (I)", "Survivor's Guilt, Sharpshooter", "Army combat uniform, too-big helmet", "adult_slim"),
]

# ---------------------------------------------------------------------------
# Procedural survivor kit (Crowd tier) — everyone else in the colony
# ---------------------------------------------------------------------------
SURVIVOR_KIT = {
    "Bodies": [
        ("Adult body", "Base body with height (1.50–1.98 m) and build morphs (slim / average / athletic / broad / heavy)", 1, "SK_NPC_Kit_BodyAdult"),
        ("Elder body", "Stooped-posture base, age morphs, thinner skin detail", 1, "SK_NPC_Kit_BodyElder"),
        ("Teen body", "13–17 proportions (teen profile), height 1.50–1.85 m", 1, "SK_NPC_Kit_BodyTeen"),
        ("Child body", "8–12 proportions (child profile), height 1.25–1.50 m; child-character rules apply", 1, "SK_NPC_Kit_BodyChild"),
    ],
    "Heads": [
        ("Base heads", "Diverse base heads covering a wide range of facial features and ages, shared topology, 24-shape crowd facial set", 48, "SK_NPC_Kit_Head_##"),
        ("Face morphs", "Brow, eyes, nose, jaw, lips, ears, age lines: 24 sliders shared with the player creator", 24, "(shape keys)"),
        ("Skin tones", "Tone ramp driven by one material parameter; freckles, vitiligo, birthmarks as overlays", 24, "(material)"),
    ],
    "Hair": [
        ("Head hair", "Hair-card styles across textures, lengths and cultures; 10 colors + grey mix", 40, "SK_NPC_Kit_Hair_##"),
        ("Facial hair", "Stubble to full beards", 14, "SK_NPC_Kit_Beard_##"),
        ("Headwear", "Caps, beanies, hijabs, headscarves, hard hats, bandanas", 18, "SK_NPC_Kit_Headwear_##"),
    ],
    "Outfit pieces (by origin)": [
        ("Kestrel crew", "Coveralls, polos, hi-vis, lab coats, security uniforms", 22, "SK_NPC_Kit_Kestrel_##"),
        ("Earth civilian", "T-shirts, hoodies, flannels, jeans, dresses, jackets, sneakers, boots", 48, "SK_NPC_Kit_Civ_##"),
        ("Colony-made", "Patched canvas, knitwear, cut-down suits, painted jackets", 30, "SK_NPC_Kit_Colony_##"),
        ("Hauler", "Container-orange coveralls, stickered vests, long coats", 16, "SK_NPC_Kit_Hauler_##"),
        ("Directorate defector", "Grey fatigues and white armor with insignia removed", 12, "SK_NPC_Kit_DirDefector_##"),
        ("Choir defector", "Undyed robes, seed beads, moss traces", 10, "SK_NPC_Kit_Choir_##"),
    ],
    "Accessories & marks": [
        ("Accessories", "Glasses, jewelry, bags, tool belts, lanyards, watches", 40, "SM_NPC_Kit_Acc_##"),
        ("Scars, tattoos, amputations", "Decals plus prosthetic limbs (arm and leg) for the Amputee trait", 30, "(decals) + SK_NPC_Kit_Prosthetic_##"),
        ("Infection states", "INF_ shapes plus infection masks, shared across every head and body", 4, "(shape keys + masks)"),
    ],
}
