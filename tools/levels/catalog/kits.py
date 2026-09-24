"""Modular environment kits. Pieces: (name, (W, D, H) m, pivot rule, LOD0 tris, notes).

Pivot rules: "corner" = bottom-left-back corner (snaps on the 0.5 m grid); "bottom-center";
"center". Walls are W wide, D thick, H tall. All kits snap to 0.5 m with 2.5 m modules so
player-built blocks (parts bible) sit flush against authored spaces.
"""

from . import K

K("KIT-KES", "Kestrel Industrial Interior", "IND", "Hangars, service corridors, Mission Control, the Vault, Tycho", [
    ("Wall 2.5", (2.5, 0.3, 3.0), "corner", 400), ("Wall 5.0", (5.0, 0.3, 3.0), "corner", 600), ("Wall Door 1.2", (2.5, 0.3, 3.0), "corner", 700, "1.2 × 2.2 m opening"),
    ("Wall Window", (2.5, 0.3, 3.0), "corner", 700, "Sill at 1.0 m"), ("Wall Corner Out", (0.3, 0.3, 3.0), "corner", 150), ("Floor 2.5", (2.5, 2.5, 0.2), "corner", 200),
    ("Floor Grate 2.5", (2.5, 2.5, 0.15), "corner", 600, "Masked grate trim"), ("Ceiling 2.5", (2.5, 2.5, 0.3), "corner", 300), ("Pillar", (0.6, 0.6, 3.0), "bottom-center", 300),
    ("Stairs 3 m", (2.5, 5.0, 3.0), "corner", 1500, "0.18 rise / 0.28 run"), ("Railing 2.5", (2.5, 0.1, 1.1), "corner", 400), ("Catwalk 2.5", (2.5, 1.5, 0.15), "corner", 600),
    ("Pipe Run 5 m", (5.0, 0.6, 0.6), "corner", 800), ("Cable Tray 5 m", (5.0, 0.5, 0.2), "corner", 500), ("Hangar Door 30×15", (30.0, 1.0, 15.0), "corner", 6000, "Segmented; animated"),
    ("Blast Door Frame", (5.0, 1.0, 5.0), "corner", 2000)])
K("KIT-TWN", "Township Suburban", "DOM", "Kestrel Township, Prospect, Earth Returns cities", [
    ("House Wall 5", (5.0, 0.25, 3.0), "corner", 500), ("House Wall Door", (5.0, 0.25, 3.0), "corner", 900), ("House Wall Window", (5.0, 0.25, 3.0), "corner", 900),
    ("Roof Gable 5", (5.0, 5.0, 2.5), "corner", 700), ("Porch 5", (5.0, 2.5, 3.0), "corner", 1500), ("Storefront 10", (10.0, 1.0, 4.5), "corner", 2500),
    ("Road 10 m (two-way)", (8.0, 10.0, 0.2), "corner", 300, "Lanes 4 m"), ("Sidewalk 10 m", (2.0, 10.0, 0.2), "corner", 200), ("Curb Corner", (2.0, 2.0, 0.2), "corner", 300),
    ("Streetlight", (0.4, 1.5, 7.0), "bottom-center", 800), ("Fence 2.5", (2.5, 0.1, 1.8), "corner", 400), ("Water Tower", (10.0, 10.0, 30.0), "bottom-center", 6000, "Township landmark")])
K("KIT-TRM", "Terminal & Airport", "IND", "Terminal B, airstrips", [
    ("Glass Curtain Wall 5", (5.0, 0.3, 12.0), "corner", 1200), ("Gate Desk", (4.0, 1.5, 1.2), "bottom-center", 1500), ("Seating Row", (5.0, 0.8, 1.0), "corner", 1800),
    ("Skywalk Segment 10", (10.0, 6.0, 4.0), "corner", 3000, "Destructible (collapse set piece)"), ("Baggage Carousel", (12.0, 6.0, 1.0), "bottom-center", 3500),
    ("Departure Board", (4.0, 0.3, 2.0), "bottom-center", 600, "Emissive screen"), ("Security Scanner", (1.5, 2.5, 2.3), "bottom-center", 1200)])
K("KIT-MIN", "Mine & Lunar Industry", "IND", "Silver Ridge, Tycho, asteroid mines", [
    ("Tunnel 4 m Arch 10", (4.0, 10.0, 4.0), "bottom-center", 1200), ("Tunnel Junction T", (8.0, 8.0, 4.0), "bottom-center", 2000), ("Timber Support", (4.5, 0.4, 4.2), "bottom-center", 500),
    ("Rail 10 m", (1.2, 10.0, 0.3), "bottom-center", 400), ("Ore Cart", (1.2, 2.0, 1.2), "bottom-center", 1200), ("Elevator Cage", (3.0, 3.0, 3.0), "bottom-center", 1500),
    ("Head-frame Tower", (12.0, 12.0, 45.0), "bottom-center", 8000, "Landmark"), ("Lunar Dome 20", (20.0, 20.0, 10.0), "bottom-center", 4000)])
K("KIT-HAV", "Haven Station", "IND", "Haven-9, player-extendable stations, Tycho modules", [
    ("Module Cylinder 12 m", (5.0, 12.0, 5.0), "center", 3000, "5 m diameter pressurized"), ("Node 6-way", (6.0, 6.0, 6.0), "center", 3500), ("Hatch Ring", (5.0, 0.6, 5.0), "center", 1200),
    ("Hull Plate 2.5", (2.5, 2.5, 0.2), "corner", 200), ("Truss 10 m", (1.5, 10.0, 1.5), "center", 900), ("Solar Wing 20", (20.0, 6.0, 0.3), "center", 1500),
    ("Observation Cupola", (6.0, 6.0, 4.0), "bottom-center", 3000), ("Interior Rack Wall", (5.0, 0.6, 2.5), "corner", 1500)])
K("KIT-DIR", "Directorate", "DIR", "Ark Meridian, outposts, crashed shuttles", [
    ("Corridor 5 m", (4.0, 5.0, 3.5), "bottom-center", 1500), ("Corridor Corner", (4.0, 4.0, 3.5), "bottom-center", 1800), ("Lab Wall 5", (5.0, 0.4, 3.5), "corner", 900),
    ("Holo Wall", (5.0, 0.3, 3.5), "corner", 800, "Emissive"), ("Null-carrier Pod", (1.5, 1.5, 2.4), "bottom-center", 2500), ("Checkpoint Gate", (4.0, 2.0, 3.0), "bottom-center", 2000),
    ("Prefab Barracks 15", (15.0, 8.0, 4.0), "corner", 3000)])
K("KIT-HAU", "Hauler & Tortuga", "HAU", "Tortuga Drift, waystations, derelicts", [
    ("Container 12 m", (2.5, 12.0, 2.6), "corner", 500), ("Container Stack ×3", (2.5, 12.0, 7.8), "corner", 1300), ("Catwalk Bridge 10", (2.0, 10.0, 1.2), "corner", 900),
    ("Market Stall", (4.0, 3.0, 3.0), "corner", 2000), ("Rock Cavern Wall 20", (20.0, 5.0, 15.0), "corner", 4000), ("Neon Sign", (6.0, 0.3, 2.0), "bottom-center", 800)])
K("KIT-SOW", "Sower Organic", "SOW", "Styx, ruins, Garden Engine, Cathedral archive", [
    ("Rib Arch 5", (5.0, 2.0, 6.0), "bottom-center", 2500), ("Coral Wall 5", (5.0, 1.5, 5.0), "corner", 3000), ("Glyph Door", (4.0, 1.0, 5.0), "bottom-center", 3000, "Iris; emissive"),
    ("Breathing Floor 5", (5.0, 5.0, 0.5), "corner", 1500, "Vertex-animated"), ("Shell Pillar", (1.5, 1.5, 8.0), "bottom-center", 2000), ("Filament Bridge 10", (2.5, 10.0, 1.0), "bottom-center", 2500)])
K("KIT-SEE", "Seedship Living", "SOW", "The Seedship Anthesis", [
    ("Root Corridor 10", (6.0, 10.0, 6.0), "bottom-center", 3500), ("Petal Wall", (8.0, 2.0, 10.0), "bottom-center", 3000), ("Petal-gate", (30.0, 10.0, 40.0), "bottom-center", 12000),
    ("Living Bridge 20", (3.0, 20.0, 2.0), "bottom-center", 3000), ("Heart Chamber Shell", (40.0, 40.0, 30.0), "bottom-center", 20000)])
K("KIT-ICE", "Ice Caves & Cathedral", "SOW", "Hollowmere, polar regions", [
    ("Ice Tunnel 10", (5.0, 10.0, 5.0), "bottom-center", 2000), ("Ice Chamber", (20.0, 20.0, 12.0), "bottom-center", 5000), ("Candle Alcove", (2.0, 1.0, 2.5), "corner", 1200),
    ("Cathedral Buttress", (4.0, 10.0, 25.0), "corner", 5000), ("Crevasse Bridge", (3.0, 15.0, 1.0), "bottom-center", 1500)])
K("KIT-DST", "Desert Terrain Dressing", "IND", "Kestrel Valley and desert biomes", [
    ("Rock Cluster S", (3.0, 3.0, 2.0), "bottom-center", 1500), ("Rock Cluster L", (12.0, 10.0, 8.0), "bottom-center", 4000), ("Mesa Cliff 50", (50.0, 20.0, 40.0), "bottom-center", 8000),
    ("Dry Wash Bank 20", (20.0, 5.0, 3.0), "corner", 1500), ("Joshua Tree", (4.0, 4.0, 6.0), "bottom-center", 2500), ("Sagebrush Patch", (3.0, 3.0, 0.8), "bottom-center", 800),
    ("Highway Barrier 5", (5.0, 0.6, 0.9), "corner", 300)])
K("KIT-JUN", "Veyra Jungle", "SOW", "Veyra-4 and jungle biomes", [
    ("Giant Root Arch", (15.0, 5.0, 12.0), "bottom-center", 5000), ("Violet Tree", (6.0, 6.0, 25.0), "bottom-center", 6000), ("Fern Cluster", (3.0, 3.0, 1.5), "bottom-center", 1500),
    ("Bioluminescent Pod Cluster", (2.0, 2.0, 1.5), "bottom-center", 1200), ("Coastal Rock", (8.0, 6.0, 5.0), "bottom-center", 3000)])
K("KIT-BLM", "Bloom Overlay", "SOW", "Every infected area; scales with Bloom level", [
    ("Bloom Vein Decal Set", (4.0, 4.0, 0.05), "center", 300, "Mesh decals"), ("Bloom Growth S", (1.0, 1.0, 1.0), "bottom-center", 800), ("Bloom Growth L", (4.0, 4.0, 3.0), "bottom-center", 3000),
    ("Bloom Root Tendril 5", (0.6, 5.0, 0.6), "corner", 1200), ("Bloom Heart Core", (20.0, 20.0, 25.0), "bottom-center", 15000), ("Bloom Root Node", (6.0, 6.0, 5.0), "bottom-center", 4000),
    ("Spore Chimney", (2.0, 2.0, 6.0), "bottom-center", 2000, "Emissive vent")])
