# 19 — Materials, Art Sets & Faction Skins

> How every part gets its look. Parts are modeled once; art sets and skins are applied through trim sheets and material instances, so the same mesh can be Industrial, Directorate or Hauler.

## 19.1 Art sets

| Code | Art set | Where it appears | Palette | Surface language |
|---|---|---|---|---|
| **SCR** | Survivor Scrap | Act I and anything improvised | Rust `#8A4B2A`, road-sign green `#1F6B3A`, safety orange `#E8641B`, faded blue `#3E5C76` | Welded sheet metal, car parts, plywood, duct tape, spray-painted marks, mismatched bolts |
| **IND** | Kestrel Industrial | The default human tech for most parts | Off-white `#E6E3DA`, graphite `#2D3035`, Kestrel orange `#F26B1D`, hazard yellow `#F5C518` | NASA-punk: stenciled labels, scuffed paint, cable runs, safety stripes, panel seams on the tiling rhythm |
| **DOM** | Domestic | Colony interiors and furniture | Warm oat `#D8C8A8`, walnut-look `#6B4A2F`, sage `#8FA58A`, lamp amber `#FFB866` | Fabric, laminate, rounded edges, hand-made touches (tape, drawings, name tags) |
| **DIR** | Directorate | Salvaged or captured Directorate parts; a cosmetic skin | Ceramic white `#F4F6F8`, gold `#C9A227`, sterile blue light `#7FC8FF` | Seamless ceramic panels, hidden fasteners, gold pinstripes, perfect bevels |
| **HAU** | Hauler | Hauler-sourced parts; a cosmetic skin | Cargo orange `#E2711D`, container blue `#1E4E79`, primer red `#8C2F24` | Corrugated container ribs, graffiti, welded patches, stickers |
| **SOW** | Sower (grown) | Precursor parts | Shell pearl `#E9E4DA`, bone `#C8BFA8`, teal glyph `#2EE6D6`, deep violet `#3A2A5C` | Grown ribs, coral and shell, no straight edges over 0.5 m, breathing emissives |

## 19.2 Trim sheets (per art set)

| Texture set | Contents | Used by |
|---|---|---|
| `T_<SET>_TrimA_Panels` | Flat panels, seams, panel edges, vents, access plates | Armor, walls, housings |
| `T_<SET>_TrimB_Mechanical` | Pipes, cables, bolts, hinges, rails, rubber seals | Machinery, doors, conveyors |
| `T_<SET>_TrimC_Hazard` | Hazard stripes, stencils, labels, port rings | Ports, edges, warnings |
| `T_<SET>_TrimD_Detail` | Grilles, screens, buttons, gauges, small lights (emissive) | Consoles, panels, status lights |
| `T_Shared_Decals` | Numbers, logos (Kestrel, Directorate, Hauler crews), wear decals, graffiti | Everything (mesh decals) |
| `T_Shared_Glass` | Clear, frosted, cockpit, cracked | All windows and screens |

All trims are 2K, authored at 512 px/m for large grid. Trim heights are standardized across art sets (same strip positions), so **any part UV'd to IND trims automatically accepts DIR, HAU or SCR skins.**

## 19.3 Faction skins (cosmetic block skins)
Skins swap the material instance, not the mesh:

| Skin | How it's earned | Notes |
|---|---|---|
| **Kestrel Industrial** | Default | — |
| **Survivor Scrap** | Start of the game | Rust and spray-paint over IND trims |
| **Directorate** | Directorate reputation +50 or salvaging 25 Directorate blocks | White-gold; gold pinstripes follow TrimC |
| **Hauler** | Hauler reputation +50 | Orange-and-blue with graffiti decals |
| **Choir Moss** | Choir alliance (M3.04) | Living moss and candle-wax drips (a `BloomGrowth`-style overlay, always on) |
| **Sower Shell** | Post-game | Pearl and teal glyph overlay on IND geometry |
| **Rust & Ruin** | Cosmetic pack | Heavy age, for derelict-style builds |

## 19.4 Material library (engine side)

| Master | Instances | Special features |
|---|---|---|
| `M_Block_Master` | `MI_<SET>_*` for every block | Damage, Burn, Dirt, Wetness, BloomGrowth, Build, EmissiveState |
| `M_Glass_Master` | `MI_Shared_Glass_*` | Crack (0–3), Frost, Condensation, Dirt |
| `M_Sower_Master` | `MI_SOW_*` | Breathing emissive pulse, subsurface shell, glyph mask |
| `M_Fabric_Master` | `MI_DOM_Fabric_*` | Owner color, wear, sheen |
| `M_Screen_Master` | `MI_Shared_Screen` | Dynamic render target, scanlines, off-state reflection |
| `M_Foliage_Master` | `MI_AGR_Crop_*` | Growth stage, wind sway, wilt |

## 19.5 Wear & storytelling rules
1. **Wear follows use:** handles, kick plates, ladder rungs and seats wear first.
2. **Every art set tells time:** SCR is new-but-crude, IND is worn from years of spaceport service, DIR is pristine (until salvaged), HAU is repaired a hundred times.
3. **Bloom growth is a gameplay signal.** The `BloomGrowth` overlay creeps from edges and seams into the middle; at 1.0 it covers 70% of the surface. It must read clearly from 20 m.
4. **Hand-made touches in DOM:** name tags, taped drawings, mugs. Survivors decorate their spaces; the prop kit supports it.
