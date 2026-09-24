# 00 — Character Art & Blender Standards

> The rules every character card assumes. Numbers here match `tools/characters/catalog/__init__.py` (tiers) and `tools/characters/skeletons.py` (skeletons and facial sets), which the Blender toolkit reads.

## 0.1 Art direction for people
1. **Grounded near-future.** Real fabrics, real wear, real bodies. No superhero proportions: heroes look like tired people who kept going.
2. **Everyone tells a story in three details** (the environmental-storytelling rule applied to people): Tug's thermos, tape and cap; Ada's tattoo, bun and photo; Lily's hoodie, crayons and plaster.
3. **Readable at three distances:** silhouette at 30 m (profession and faction), costume at 10 m (act and state), face at 1 m (emotion and history).
4. **Characters age through the game.** Hair grows, clothes patch, weight changes and scars accumulate act by act. Wardrobe tables list the changes.
5. **Diversity is designed, not randomized.** The cast and the head library are reviewed together for a wide range of ancestries, ages, body types and abilities, without caricature. Cultural details get a consultant (game bible 17 §17.8).
6. **Horror without gore.** Hollows are wrong, not splattered. The Verdance replaces blood with growth. No child is ever shown hurt beyond scrapes, and there are no child Hollows.

## 0.2 Units, axes & rest pose
- Metric, meters, **unit scale 1.0**.
- **Characters face −Y**, up +Z, the character's **left is +X** (Blender/Rigify convention; building parts use front +X, see parts bible 00).
- **A-pose** rest (arms 45° down), feet flat at Z = 0, root bone at the origin.
- **Heights are exact:** the crown of the head sits at the character's catalog height (±2%, checked by the validator).
- **Engine import:** UE5 skeletal mesh, *Convert Scene* on, *Import Morph Targets* on, *Use T0 As Ref Pose* off; Unity *Bake Axis Conversion* on, *Blend Shapes* on.

## 0.3 Budget tiers

| Tier | Used for | LOD0 tris | Split | Max influences |
|---|---|---|---|---|
| **Hero** | Wrench, Ada, Lily, Crane, adult Lily | 160,000 | Head 35k · Hair 40k · Body + outfit 85k | 8 |
| **Main** | Companions and antagonists | 110,000 | Head 30k · Hair 30k · Body + outfit 50k | 8 |
| **Secondary** | Notable survivors, officers, traders, story NPCs | 60,000 | Head 18k · Hair 15k · Body + outfit 27k | 8 |
| **Crowd** | Procedural survivors, helmeted units | 30,000 | Head 8k · Hair 6k · Body + outfit 16k | 4 |
| **Enemy** | Common Hollows | 35,000 | Head 6k · Bloom 9k · Body 20k | 4 |
| **Elite** | Special Hollows, Enforcer, Warden | 60,000 | Head 8k · Bloom 17k · Body 35k | 4 |
| **Boss** | Boss forms | 180,000 | Head 35k · Armor/growth 70k · Body 75k | 8 |
| **Creature-L / S** | Large / small fauna | 80,000 / 15,000 | Head + body | 4 |
| **Hologram** | KESTREL | 20,000 | Form | 4 |

**LOD chain:** 100% / 50% / 20% / 6%. LOD2 drops finger bones' deformation detail and hair to shells; LOD3 is a silhouette with baked hair. **Hordes:** Enemy tier also gets a vertex-animation-texture (VAT) impostor for crowds over 300.

## 0.4 Files & naming

| Pattern | Meaning |
|---|---|
| `SK_CHR_<Name>` | Story character base (head + body) — player and story cast |
| `SK_NPC_<Name>` | Notable survivors, faction units, kit pieces (`SK_NPC_Kit_*`) |
| `SK_ENM_<Name>` | Hollows, constructs and boss forms |
| `SK_CRE_<Name>` | Creatures and fauna kits |
| `SK_SUIT_<Name>` | Shared suits (parts bible chapter 18), worn by every humanoid |
| `<base>_Outfit_<Key>` | Outfit (separate skinned mesh on the same rig) |
| `<base>_Hair_<Key>` | Hair mesh (cards, shells or cloth) |
| `<base>_<Variant>` | Variant (e.g. `_Hollow`, `_Bloomed`, `_Female`) |
| `<base>_Arms1P_<Outfit>` | First-person arms for an outfit |
| `<asset>_LOD0…3`, `<asset>_Head_LOD0…3` | LOD meshes; facial shape keys live on `_Head_` meshes |
| `Armature` | The one armature object in every file (so UE doesn't add an extra root bone) |
| `SOCKET_*` | Socket empties parented to bones |
| `REF_*` | Reference only (turnaround cameras, height bar, stand-in body): never exported |
| `MI_<SET>_*` / `T_<Char>_<Map>` | Material instances / textures (`_BC _N _ORM _SSS _E _M`, `_Wrinkle1/2`, `_InfectionMask`) |

Files: `assets/characters/<chapter>/<asset>.blend`, one asset per file; exports to `export/characters/<chapter>/`.

## 0.5 Collections (every character file)
```
<asset>
├─ <asset>_Rig          Armature (template bones at the catalog height)
├─ <asset>_LOD0 … LOD3  skinned meshes: <asset>_LOD0 (body), <asset>_Head_LOD0 (head, facial shape keys) …
├─ <asset>_Sockets      SOCKET_* empties parented to bones
└─ <asset>_Reference    REF_Cam_Front/Side/Back/ThreeQuarter (ortho turnaround), REF_HeightBar, REF_Human_1p8m, REF_*_Body
```

## 0.6 Heads & faces
- **Shared head topology** across all humanoids (one base head mesh, retopologized to each likeness). This makes the family resemblance (Wrench/Ada), aging (Lily 11 → 21, Crane −3 years) and the boss transitions possible with shape keys.
- **Edge loops:** concentric loops around eyes and mouth; nasolabial loop; 3 loops across the lips; eyelids with at least 4 loops for clean blinks.
- **Eyes:** separate meshes (cornea + iris/sclera + tear line + occlusion shell), `eye_l/r` bones.
- **Teeth and tongue:** separate meshes weighted to `jaw` and `head`.
- **Facial rig:** shape keys on `<asset>_Head_LOD0` by tier set (chapter 10): Hero = ARKit 52 + 24 EXODUS correctives + 4 infection (80); Main 68; Secondary 56; Crowd 28. ARKit names are exact, so live facial capture drives them directly. LOD1 keeps all shapes; LOD2 keeps the ARKit 52; LOD3 keeps jawOpen and the blinks.
- **Wrinkle maps** (Hero, Main): two wrinkle normal maps blended by brow and smile shape weights.

## 0.7 Bodies, outfits & layering
- **Body under clothes:** only the visible skin is modeled under an outfit (hidden-face masks per outfit), but every base body is complete for suits and damage.
- **Outfits are separate skinned meshes** on the same armature, weighted with the same bones; each outfit ships its own LOD0–3.
- **Shared suits** (hazmat, EVA, hardsuit, Sower-woven) fit every humanoid through shared body morph targets (`body_slim`, `body_athletic`, `body_broad`, `body_heavy`, `age_older`). Character files never contain suit meshes.
- **Layer order:** skin → underlayer → top → outerwear → gear → hair → headwear. Layers are pushed out ≥ 3 mm to avoid clipping at extreme poses.
- **Cloth simulation** only where listed on the card (coat tails, robes, hijab, bandana tails). Everything else is skinned.

## 0.8 Hair
- **Hair cards** for gameplay (Hero 40k tris, Main 30k, Secondary 15k, Crowd 6k); 4K/2K card atlases with alpha-to-coverage, depth-prepass friendly.
- **Groom reference** (Blender Hair Curves) is kept for Hero characters and used for cinematics at the engine's discretion.
- **Physics:** braids, ponytails and long hair get 3–6 bone chains (`x_hair_*`), not simulation.
- **States:** clean → messy → matted (Hollow) via material parameters, not new meshes.

## 0.9 Skin & materials
- **Skin:** subsurface scattering with a per-character SSS map; micro-detail tiling normal; melanin-aware base color (tone set by one parameter for kit heads).
- **Standard layers:** dirt, blood-free wounds (plasters, stitches, bruises), sweat and wetness, frost (cryo, space), soot.
- **Eyes:** refraction (cornea), iris parallax, wet tear line; Stage 3+ infection clouds the sclera via `INF_EyeCloud` and the mask.
- **Fabrics:** one master (`M_Fabric_Master`) with weave detail, wear and owner-color masks; leather and armor on the block master's character variant.

## 0.10 Infection states (Stage 0–4)
Every human who can be infected (player, cast, survivors) supports five stages:

| Stage | Look | Shape keys | Mask |
|---|---|---|---|
| 0 Clean | — | 0 | 0 |
| 1 Exposed | Faint green tint at the wound site | `INF_Veins` 0.1 | Wound-local |
| 2 Seeded | Green veins at the neck, hands and around the wound | `INF_Veins` 0.5, `INF_EyeCloud` 0.2 | 30% coverage |
| 3 Blooming | Lichen crust, clouded eyes, receding gums | `INF_Lichen` 0.6, `INF_EyeCloud` 0.6, `INF_GumRecede` 0.4 | 65% |
| 4 Turning | Full Hollow look (60 s countdown) | all 1.0 | 100% |

`T_<Char>_InfectionMask` (UV1) drives color; `INF_` shapes add raised veins and lichen. Child characters stop at Stage 1 visually (story rule).

## 0.11 Hollow conversion
Any adult kit survivor becomes a Hollow by: the Hollow skin material (grey-green, bruised veins), the Hollow facial set, matted hair state, torn outfit variants, and **Bloom attachments** (60 shared growth meshes, `SM_ENM_BloomGrowth_##`, attached to `bloom_growth_*` bones). Named Hollows (Dana Marsh, Ms. Alvarez) are hand-finished variants.

## 0.12 First-person arms
- The player (and adult Lily in Legacy) need **first-person arms per outfit**: `SK_CHR_<Name>_Arms1P_<Outfit>`, 25k tris, 4K texture, same skeleton, clavicle to fingertips.
- Shared suits ship their own 1P arms (`SK_SUIT_<Suit>_Arms1P`).
- The FOV-safe zone: forearms must read at 70–110° FOV without stretching; check with the toolkit's `REF_Cam_*` plus a 90° first-person camera.

## 0.13 Definition of done (every character asset)
- [ ] Scaffolded with `exodus_characters.py`; armature untouched except approved extra bones
- [ ] Height within ±2% of the catalog
- [ ] LOD0–3 within budget; LOD3 silhouette-only
- [ ] Every mesh parented to `Armature` with an Armature modifier; transforms applied
- [ ] Weights: no unweighted vertices, ≤ max influences, normalized
- [ ] UV0 + UV1 (masks) on LOD0/1; `MI_*` materials; blockout material removed
- [ ] Facial shape keys complete for the tier set (base heads) and all moving
- [ ] Infection states (if applicable) and hidden-face masks for outfits
- [ ] Sockets present; turnaround renders approved by art direction
- [ ] `validate` PASS; exported; imported and checked in engine against the animation test level
