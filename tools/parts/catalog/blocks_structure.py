"""STR — Structure & Armor, DOR — Doors & Access."""

from . import P, V

LG_SG_1 = {"LG": (1, 1, 1), "SG": (1, 1, 1)}
LG_1 = {"LG": (1, 1, 1)}

# ---------------------------------------------------------------------------
# STR — Armor shape family
# (name, blockout shape, volume fraction, mount faces, modeling note)
# ---------------------------------------------------------------------------
ARMOR_SHAPES = [
    ("Block", "cube", 1.0, "all",
     "The workhorse. Panel seams every 0.625 m (LG) / 0.125 m (SG) so neighbours read as one continuous hull. All six faces identical so rotation never shows."),
    ("Slope", "slope", 0.5, "back,bottom,left,right",
     "45° face from front-bottom edge to back-top edge. Side faces are right triangles; keep seam lines matching the Block's."),
    ("Corner", "corner", 0.17, "back,bottom,right",
     "Tetrahedron filling one corner. Pairs with Slope; the three open edges need 2 mm bevel continuity."),
    ("Inverted Corner", "inv_corner", 0.83, "all",
     "Cube with one corner cut by a plane through three adjacent vertices. Used to close Slope junctions."),
    ("Half Block", "half", 0.5, "all",
     "Bottom half of the cell (0–50% height). Top face gets the full-panel trim, not a cut edge."),
    ("Slope 2×1 Base", "slope2_base", 0.75, "back,bottom,left,right",
     "Lower half of a 2-cell-long 26.6° slope (rises 0.5 cell over 1). Front edge sits at 50% height to meet the Tip."),
    ("Slope 2×1 Tip", "slope2_tip", 0.25, "back,bottom,left,right",
     "Upper half of the 2×1 slope; rises from 0 to 50% height. Must meet the Base with zero gap."),
    ("Corner 2×1 Base", "corner2_base", 0.33, "back,bottom,right",
     "Corner piece for 2×1 slopes (base half)."),
    ("Corner 2×1 Tip", "corner2_tip", 0.08, "back,bottom,right",
     "Corner piece for 2×1 slopes (tip half). Tiny: keep it under 60% of the Simple budget."),
    ("Inverted Corner 2×1 Base", "inv_corner2_base", 0.92, "all",
     "Inverted corner matching the 2×1 slope angle (base half)."),
    ("Inverted Corner 2×1 Tip", "inv_corner2_tip", 0.58, "back,bottom,left,right",
     "Inverted corner matching the 2×1 slope angle (tip half)."),
    ("Round Slope", "round_slope", 0.6, "back,bottom,left,right",
     "Quarter-cylinder profile, 8 segments at LOD0 (4 at LOD2). Normals must match Round Corner exactly."),
    ("Round Corner", "round_corner", 0.3, "back,bottom,right",
     "Eighth-sphere-style corner for Round Slopes. 8×8 segments LOD0."),
    ("Round Inverted Corner", "round_inv_corner", 0.85, "all",
     "Concave rounded corner. Custom split normals so it shades seamlessly against Round Slopes."),
    ("Panel", "panel", 0.1, "back",
     "0.25 m (LG) / 0.05 m (SG) plate on the back face. Used for thin walls and cosmetic hull skins. Both sides textured."),
    ("Panel Slope", "panel_slope", 0.12, "back,bottom",
     "Thin plate along the 45° diagonal. Pairs with Panel for lightweight sloped hulls."),
]


def _armor_recipe(fraction, heavy, grid):
    if grid == "LG":
        if heavy:
            return {"steel_plate": max(1, round(150 * fraction)), "metal_grid": max(1, round(50 * fraction))}
        return {"steel_plate": max(1, round(25 * fraction))}
    if heavy:
        return {"steel_plate": max(1, round(5 * fraction)), "metal_grid": 1}
    return {"steel_plate": 1}


for shape_name, shape, frac, mounts, note in ARMOR_SHAPES:
    airtight = "back" if shape == "panel" else ("none" if shape == "panel_slope" else "all")
    P("STR", f"Armor {shape_name}", "Armor", LG_SG_1, tier="T1", cls="S", shape=shape,
      mass={"LG": round(500 * frac), "SG": max(1, round(20 * frac))},
      hp={"LG": round(1500 * frac), "SG": max(5, round(60 * frac))},
      recipe={"LG": _armor_recipe(frac, False, "LG"), "SG": _armor_recipe(frac, False, "SG")},
      function=f"Structural hull piece ({shape_name.lower()} shape). Light armor for structure; Heavy armor for combat hulls and Brute-proof base walls.",
      unlock="Light: T1 (Assembler). Heavy: T2.",
      mounts=mounts, airtight=airtight,
      notes=note + " Deformation: vertex-shader dents driven by the damage texture; no separate damaged mesh.",
      variants=[
          V("Light", notes="Single-skin plates, 20 mm edge bevel (LG). Uses MI_IND_ArmorLight."),
          V("Heavy", mass_mult=6.6, hp_mult=4.33, tier="T2",
            recipe={"LG": _armor_recipe(frac, True, "LG"), "SG": _armor_recipe(frac, True, "SG")},
            notes="Double-skin look: 60 mm outer plates with bolt rows and recessed seams. Uses MI_IND_ArmorHeavy. Same silhouette as Light, so the two can be mixed on one hull."),
      ])

# ---------------------------------------------------------------------------
# STR — Other structure
# ---------------------------------------------------------------------------
P("STR", "Scrap Wall", "Survivor Structure", LG_1, tier="T0", art="SCR", cls="M",
  mass=350, hp=700, recipe={"scrap_metal": 20, "duct_tape": 2},
  function="The first wall of Act I (M1.01). Cheap, fast, ugly. Leaks light and sound through its gaps, which raises a base's Attraction.",
  unlock="Start of Act I.", mounts="all", airtight="none",
  notes="Four visual variants that must tile with each other in any order. Real gaps (not painted): 3–6 slits per face so floodlight shafts show through at night. Decals: Kestrel logo, road signs, spray-painted tally marks.",
  variants=[V("A Sheet & Signs"), V("B Car Doors"), V("C Corrugated"), V("D Plywood & Rebar")])

P("STR", "Foundation Block", "Base Structure", LG_1, tier="T1", cls="M",
  mass=9000, hp=8000, recipe={"steel_plate": 10, "construction_component": 10, "girder": 8},
  function="Anchors a static grid to voxel terrain. Removes terrain-settling damage and adds 50 t of load capacity.",
  unlock="T1.", mounts="all", airtight="all",
  notes="Concrete-and-rebar look. Includes a 1.25 m skirt below the cell that clips into terrain (excluded from collision). Vertex-color mask for a dirt blend on the lower 40%.")

P("STR", "Structural Pillar", "Base Structure", LG_1, tier="T1", cls="M",
  mass=2400, hp=5000, recipe={"girder": 12, "steel_plate": 20, "construction_component": 6},
  function="Load-bearing column with 60 t capacity (5× light armor). Brutes target the weakest pillar, so pillars must read clearly as structure.",
  mounts="top,bottom,left,right,front,back", airtight="none",
  notes="Square core column with diagonal bracing and bolted top/bottom flanges. Material parameter 'StressState' (0–1) drives green → amber → red paint marks for the Structural View.")

P("STR", "I-Beam", "Frame", LG_SG_1, tier="T1", cls="S",
  mass={"LG": 600, "SG": 30}, hp={"LG": 1800, "SG": 90},
  recipe={"LG": {"girder": 6, "steel_plate": 4}, "SG": {"girder": 1, "steel_plate": 1}},
  function="Open steel beam for frames, gantries and bridges. Cheaper than armor; carries load but is not airtight.",
  mounts="front,back,bottom", airtight="none",
  notes="Beam runs along the depth axis (front–back). Flange holes as geometry at LOD0, normal map at LOD1+.",
  variants=[V("1 Cell"), V("3 Cells", grids={"LG": (1, 1, 3), "SG": (1, 1, 3)}, mass_mult=3, hp_mult=3),
            V("5 Cells", grids={"LG": (1, 1, 5), "SG": (1, 1, 5)}, mass_mult=5, hp_mult=5)])

P("STR", "Truss Frame", "Frame", LG_SG_1, tier="T1", cls="S",
  mass={"LG": 300, "SG": 15}, hp={"LG": 900, "SG": 45},
  recipe={"LG": {"metal_grid": 6, "small_tube": 4}, "SG": {"metal_grid": 1, "small_tube": 1}},
  function="See-through lattice block for towers, antenna masts and scaffolding.",
  mounts="all", airtight="none",
  notes="Real strut geometry (12 edge struts + 4 diagonals, 8 nodes); no alpha. Heavily instanced: LOD0 at 600 tris max for LG.")

P("STR", "Catwalk", "Walkways", LG_1, tier="T1", cls="S",
  mass=200, hp=500, recipe={"metal_grid": 4, "small_tube": 6, "construction_component": 2},
  function="Grated floor for hangars and industrial decks. Hollows can be seen (and shot) through it.",
  mounts="bottom,left,right,front,back", airtight="none",
  notes="Grate occupies the bottom 0.15 m. The grate uses the opacity-masked trim (the only masked material allowed in structure); LOD2+ swaps to a solid plate.",
  variants=[V("Straight"), V("Corner"), V("T-Junction"), V("End")])

P("STR", "Catwalk Railing", "Walkways", LG_1, tier="T1", cls="S",
  mass=60, hp=200, recipe={"small_tube": 6, "construction_component": 1},
  function="Safety railing for catwalks, stairs and balconies.",
  mounts="bottom", airtight="none",
  notes="Railing along the front edge, 1.1 m tall. Handrail must be grab-able (zero-G handhold socket).",
  sockets=["interact@front"],
  variants=[V("Straight"), V("Corner"), V("Stair-Aligned")])

P("STR", "Stairs", "Walkways", LG_1, tier="T1", cls="M",
  mass=900, hp=1200, recipe={"steel_plate": 10, "construction_component": 8, "small_tube": 4},
  function="Climbs one cell over one cell (45°). Survivors path-find over stairs; Crawlers hide under them.",
  mounts="bottom,back,front", airtight="none", shape="slope",
  notes="10 steps, 0.25 m rise each. Open underside (hiding spot) with a cross-brace. Collision is a ramp, not steps.")

P("STR", "Ramp", "Walkways", {"LG": (1, 1, 2)}, tier="T1", cls="S",
  mass=1000, hp=1500, recipe={"steel_plate": 14, "construction_component": 4},
  function="Rover-friendly ramp rising one cell over two.", mounts="bottom,back,front", airtight="none",
  shape="slope", notes="Anti-slip tread plate trim. Collision matches the visible surface exactly (vehicles).")

P("STR", "Window 1×1", "Windows", LG_SG_1, tier="T1", cls="S",
  mass={"LG": 400, "SG": 20}, hp={"LG": 450, "SG": 40},
  recipe={"LG": {"girder": 8, "glass_panel": 20, "steel_plate": 4}, "SG": {"girder": 1, "glass_panel": 2}},
  function="Airtight window. Survivors get the 'View' moodlet from windows facing Earth, planets or nebulae.",
  mounts="all", airtight="all",
  notes="Frame 0.3 m deep (LG). Glass is a separate material slot with a 'Crack' parameter (0–3) and interior-side reflection. Two-sided frame detail.")

P("STR", "Window 1×2", "Windows", {"LG": (1, 2, 1), "SG": (1, 2, 1)}, tier="T1", cls="S",
  mass={"LG": 800, "SG": 40}, hp={"LG": 900, "SG": 80},
  recipe={"LG": {"girder": 16, "glass_panel": 40, "steel_plate": 8}, "SG": {"girder": 2, "glass_panel": 4}},
  function="Tall window for observation decks and bridges.", mounts="all", airtight="all",
  notes="One central mullion. Shares the 1×1 frame trim so rows of mixed windows line up.")

P("STR", "Window Slope", "Windows", LG_SG_1, tier="T1", cls="S", shape="slope",
  mass={"LG": 500, "SG": 25}, hp={"LG": 550, "SG": 50},
  recipe={"LG": {"girder": 10, "glass_panel": 24, "steel_plate": 6}, "SG": {"girder": 1, "glass_panel": 2}},
  function="Glass on the slope face; used for cockpits and sloped observation roofs.",
  mounts="back,bottom,left,right", airtight="all",
  notes="Glass on the sloped face; solid triangular side frames.")

P("STR", "Observation Dome", "Windows", {"LG": (3, 2, 3)}, tier="T2", cls="L",
  mass=3600, hp=2500, recipe={"girder": 40, "glass_panel": 120, "steel_plate": 30},
  function="Hero window room piece. The home of 'Walt's Window' and the best View moodlet in the game.",
  mounts="bottom", airtight="all",
  sockets=["seat@center*4", "light@top"],
  notes="Geodesic hex frame on a 3×3 base ring, 5 m tall. Interior floor lip at 0.2 m with 4 built-in seat slots. Needs a planar-reflection probe socket at the center.")

P("STR", "Interior Wall", "Interior", LG_1, tier="T1", cls="S",
  mass=150, hp=300, recipe={"interior_plate": 10, "construction_component": 4},
  function="Lightweight partition for dividing rooms. Airtight on its back face when the edges are sealed.",
  mounts="back,bottom,top,left,right", airtight="back", shape="panel",
  notes="0.15 m thick against the back face. Both sides detailed; cable-tray and outlet decals.",
  variants=[V("Plain"), V("Paneled"), V("Interior Glass", recipe={"LG": {"interior_plate": 6, "glass_panel": 6}}),
            V("Doorway Frame", notes="Open 1.2 × 2.1 m doorway; not airtight.")])

P("STR", "Interior Pillar", "Interior", LG_1, tier="T1", cls="S",
  mass=100, hp=300, recipe={"interior_plate": 6, "small_tube": 2},
  function="Decorative column; hides cable runs.", mounts="top,bottom", airtight="none",
  notes="0.4 m square column, centered. Optional light-strip emissive.", emissive=["Optional light strip (room lighting color)"])

P("STR", "Ceiling Panel", "Interior", LG_1, tier="T1", cls="S",
  mass=120, hp=250, recipe={"interior_plate": 8, "construction_component": 2},
  function="Drop-ceiling panel with cable trays; raises Room Quality over bare hull.",
  mounts="top", airtight="none", shape="panel_top",
  notes="0.2 m thick against the top face. Includes an optional recessed light slot.",
  sockets=["light@bottom"])

# ---------------------------------------------------------------------------
# DOR — Doors & Access
# ---------------------------------------------------------------------------
P("DOR", "Scrap Door", "Survivor Doors", LG_1, tier="T0", art="SCR", cls="M",
  mass=250, hp=400, recipe={"scrap_metal": 15, "duct_tape": 2},
  function="Hinged door made from a car hood and fence panels. Not airtight. Hollows can bash it open.",
  mounts="all", airtight="none",
  moving=["Door leaf: hinged swing 100° around the left edge, 0.9 s (manual)"],
  sockets=["interact@front", "interact@back", "door@left"],
  notes="Visible hinges are welded bolts. Door leaf has three damage states (dented, bent, hanging).")

P("DOR", "Blast Shutter", "Survivor Doors", LG_1, tier="T0", art="SCR", cls="M",
  mass=600, hp=1500, recipe={"scrap_metal": 25, "motor": 1},
  function="Roll-down metal shutter for doorways and windows. The first thing the player welds shut in M0.03.",
  mounts="all", airtight="none",
  moving=["Shutter slats: roll up into the top housing (2.2 m travel, 3 s)"],
  sockets=["interact@front", "door@top"],
  audio=["Rattling roll loop"],
  notes="Slats are one skinned strip or 12 separate slats driven by a curve. Hand crank on the right side.")

P("DOR", "Door", "Doors", LG_1, tier="T1", cls="M",
  mass=350, hp=800, power=-0.5,
  recipe={"interior_plate": 10, "construction_component": 20, "motor": 2, "display": 1},
  function="Standard airtight sliding door. Lockable; used for quarantine.",
  mounts="all", airtight="all",
  moving=["Door leaves ×2: slide ±Y 1.0 m, 0.8 s"],
  sockets=["interact@front", "interact@back", "door@center"],
  emissive=["Frame status strip: green open / red locked / amber cycling"],
  notes="1.2 × 2.2 m opening. Leaves fully hidden in the frame when open. Pressure seal detail on the leading edges.")

P("DOR", "Double Door", "Doors", {"LG": (2, 1, 1)}, tier="T1", cls="M",
  mass=700, hp=1400, power=-1,
  recipe={"interior_plate": 20, "construction_component": 36, "motor": 4, "display": 1},
  function="Wide airtight door for mess halls and main corridors (two survivors can pass at once).",
  mounts="all", airtight="all",
  moving=["Door leaves ×2: slide ±Y 2.2 m, 1.1 s"],
  sockets=["interact@front", "interact@back", "door@center"],
  emissive=["Frame status strip"], notes="2.4 × 2.2 m opening.")

P("DOR", "Hatch", "Doors", {"LG": (1, 1, 1), "SG": (3, 1, 3)}, tier="T1", cls="M",
  mass={"LG": 500, "SG": 120}, hp={"LG": 900, "SG": 200}, power={"LG": -0.5, "SG": -0.1},
  recipe={"LG": {"steel_plate": 12, "construction_component": 10, "motor": 2}, "SG": {"steel_plate": 3, "construction_component": 2, "motor": 1}},
  function="Floor/ceiling hatch between decks, and the small-grid access hatch for ships.",
  mounts="all", airtight="all",
  moving=["Hatch leaf: hinge 110°, 1.0 s"], sockets=["interact@top", "interact@bottom", "door@center"],
  emissive=["Ring status light"], notes="Ladder rungs integrated on the underside (LG).")

P("DOR", "Airlock Module", "Airlocks", {"LG": (1, 1, 2)}, tier="T2", cls="L",
  mass=1800, hp=3000, power=-40,
  recipe={"steel_plate": 40, "interior_plate": 20, "construction_component": 30, "motor": 6, "computer": 4, "display": 2},
  function="Self-contained auto-cycling airlock with inner and outer doors. Cycles in 4 s.",
  mounts="all", airtight="all",
  moving=["Outer door: slide +Z 2.2 m, 0.8 s", "Inner door: slide +Z 2.2 m, 0.8 s"],
  sockets=["interact@front", "interact@back", "air@top", "door@front", "door@back"],
  emissive=["Cycle light (red/amber/green)", "Pressure gauge screen"],
  vfx=["Vent jets ×4 during depressurization"], audio=["Pressure hiss", "Cycle chime"],
  notes="Interior chamber 1.6 m wide. The chamber must feel tight: handholds, stencils, a scuffed floor.")

P("DOR", "Vehicle Airlock", "Airlocks", {"LG": (3, 2, 3)}, tier="T2", cls="XL",
  mass=12000, hp=9000, power=-150,
  recipe={"steel_plate": 180, "construction_component": 120, "motor": 20, "computer": 10, "display": 4},
  function="Drive-through airlock for rovers and small ships.",
  mounts="all", airtight="all",
  moving=["Outer door: segmented, rises 5 m, 3 s", "Inner door: segmented, rises 5 m, 3 s"],
  sockets=["interact@left", "air@top*2", "light@top*4"],
  emissive=["Cycle lights", "Floor guide strips"], vfx=["Vent jets ×8"],
  notes="Interior 7 × 5 × 7 m. Tire-scuffed floor decals, tie-down points.")

P("DOR", "Decontamination Airlock", "Airlocks", {"LG": (1, 1, 2)}, tier="T2", cls="L",
  mass=2000, hp=3000, power=-60,
  recipe={"steel_plate": 40, "interior_plate": 20, "motor": 6, "computer": 4, "filter_mesh": 10, "medical_component": 4},
  function="Airlock that sprays and UV-scrubs anyone passing through: halves spore exposure carried into the base. Key quarantine tool.",
  mounts="all", airtight="all",
  moving=["Outer and inner doors (as Airlock Module)", "Spray arms ×4 rotate 60°"],
  sockets=["interact@front", "interact@back", "air@top", "water@bottom"],
  emissive=["UV lamp strips (violet)", "Cycle light"], vfx=["Decon mist", "UV glow"],
  notes="Medical white-and-hazard-yellow variant of the Airlock Module; shares the door meshes.")

P("DOR", "Blast Door Panel", "Heavy Doors", LG_1, tier="T2", cls="M",
  mass=4000, hp=9000, power=-0.2,
  recipe={"steel_plate": 120, "metal_grid": 40, "motor": 4, "construction_component": 20},
  function="Tileable heavy door. Adjacent panels join into one gate of any size and open together.",
  mounts="all", airtight="all",
  moving=["Door slab: slides down into the floor pocket 2.5 m (or up), 4 s", "Locking bolts ×4: retract 0.2 m"],
  sockets=["interact@front"], emissive=["Hazard strobe while moving"], audio=["Heavy servo", "Bolt clunk"],
  notes="Edge-matching on all four sides; the frame is a separate 'frame' mesh auto-placed on exposed edges.")

P("DOR", "Hangar Door Segment", "Heavy Doors", LG_SG_1, tier="T2", cls="S",
  mass={"LG": 900, "SG": 40}, hp={"LG": 2200, "SG": 120}, power={"LG": -0.5, "SG": -0.05},
  recipe={"LG": {"steel_plate": 30, "construction_component": 10, "motor": 1}, "SG": {"steel_plate": 2, "motor": 1}},
  function="Stackable segment (up to 10 high) that folds upward.",
  mounts="all", airtight="all",
  moving=["Segment: hinges and folds upward into the stack above, 0.6 s per segment"],
  emissive=["Edge warning lights"], notes="Horizontal ribbing; segment edges interlock visually.")

P("DOR", "Cargo Ramp", "Heavy Doors", {"LG": (3, 1, 2), "SG": (5, 1, 6)}, tier="T2", cls="L",
  mass={"LG": 3000, "SG": 350}, hp={"LG": 4500, "SG": 600}, power={"LG": -5, "SG": -1},
  recipe={"LG": {"steel_plate": 60, "motor": 6, "construction_component": 20}, "SG": {"steel_plate": 10, "motor": 2}},
  function="Hinged loading ramp for ships and rovers.",
  mounts="back,left,right", airtight="all",
  moving=["Ramp: hinges at the back edge, lowers 100°, 3 s", "Hydraulic rams ×2"],
  sockets=["interact@left"], emissive=["Edge lights"], notes="Tread plate on the walking face; underside ribbed.")

P("DOR", "Ladder", "Access", LG_SG_1, tier="T0", cls="S",
  mass={"LG": 80, "SG": 5}, hp={"LG": 200, "SG": 30},
  recipe={"LG": {"small_tube": 6, "construction_component": 2}, "SG": {"small_tube": 1}},
  function="Climbable ladder; also a zero-G handhold rail.",
  mounts="back", airtight="none", shape="panel",
  sockets=["interact@front"], notes="Rungs every 0.3 m; stand-off brackets 0.2 m from the wall.")

P("DOR", "Elevator Shaft", "Access", LG_1, tier="T2", cls="S",
  mass=700, hp=1500, recipe={"steel_plate": 12, "girder": 8, "construction_component": 6},
  function="Stackable shaft segment for the Elevator Car.",
  mounts="top,bottom,back,left,right", airtight="none",
  notes="Guide rails on the back face, cable detail, floor-number decal slot on the front.")

P("DOR", "Elevator Car", "Access", LG_1, tier="T2", cls="M",
  mass=900, hp=1200, power=-8,
  recipe={"steel_plate": 10, "interior_plate": 10, "motor": 4, "computer": 1, "display": 1},
  function="Moves people and cargo between decks along Elevator Shafts.",
  mounts="none", airtight="none",
  moving=["Car: travels along the shaft at 3 m/s", "Car doors: slide ±Y 0.6 m"],
  sockets=["interact@center", "light@top"], emissive=["Floor display", "Ceiling light"],
  notes="Interior-only car; the exterior is hidden by the shaft.")

P("DOR", "Chain-Link Gate", "Survivor Doors", {"LG": (2, 1, 1)}, tier="T0", art="SCR", cls="M",
  mass=180, hp=500, recipe={"scrap_metal": 10, "small_tube": 6},
  function="Sliding chain-link gate for compound walls (pairs with Chain-Link Fence).",
  mounts="bottom,left,right", airtight="none",
  moving=["Gate: slides ±Y 2.4 m on wheels, 2 s"], sockets=["interact@front", "interact@back"],
  notes="Chain-link mesh uses the masked fence material; razor-wire top optional (variant).",
  variants=[V("Plain"), V("Razor Wire", recipe={"LG": {"scrap_metal": 14, "small_tube": 6}})])
