# SPHIRUS Art Director Review

2026-09-25 · senior art-director review, environment and interior quality audit, asset-gap decision

SPHIRUS does not yet reach The Last of Us / A Plague Tale environment-art quality, and the gap is not caused by missing assets: the map uses 51 of more than 600 installed vegetation meshes. Evidence is the latest Bridge run `2026-09-25_024058_725422_06d8c8` (matching the saved map of 2026-09-25 02:40), the FinalGate before/after sheets, the gameplay-camera route sheets, and the exported actor, foliage and lighting data. No new captures were taken, so most interior rows are UNVERIFIED.

## 1. Verdict

The current game reads as a competent vendor-pack woodland placed on a landscape, not as a place hand-built by environment artists.

**Where it works**

- **Terrain structure exists.** The house sits on a shelf above the pond, ground rises behind it, and the uphill trail has real banks and cuts (views 02, 04, 14, 15).
- **The uphill and side trail is close to the target**: layered midstory, compression, and a lookback to the roof that feels nested (14, 15, 09).
- **Nested-house moments exist**: the house glimpsed through saplings and trunks (04, 15, gameplay exit lookbacks).
- **The interior has a real resident story in its inventory**: mask workbench and work in progress, pigment jars, drawer and wall rack, herbarium sheets in three rooms, sewing machine and spools, family ledger and chest, attic photo box and keepsakes.

**Where it falls short**

- **Ground.** One landscape texture with sparse, evenly scattered copies of one or two plant meshes fills 30–50% of almost every gameplay frame.
- **Forest.** One even-aged stand of 6 tree meshes with straight grey trunks. The most-placed foliage mesh is a single scraggly sapling (`SM_Pine_Juvenile_01`, 1,414 instances, 17% of all foliage). Almost no snags or fallen trees; sky leaks through the canopy.
- **Values and atmosphere.** Backlit pond views are washed out by beige haze and god rays (07, 12, 17); frontlit views are flat (A01–A05); foliage has a blue-grey sage cast; no deep dark masses.
- **Front of the house**, the refuge's hero view, is the emptiest area: a broad lawn-like clearing (A05, H01, H06, R01, R02, 16), which AGENTS.md forbids.
- **House** reads as a clean digital building at medium range: clean upper plaster, pure-white unaged strips, uniform grey cladding, straight plinth, pinkish porch boards.
- **Interior** reads as a showroom: warm fill light, uniform floorboards, one rug mesh in 8 rooms, 31 daily-use props placed but hidden.

## 2. Top bottlenecks

Ranked by visible quality impact, not by effort.

| # | Bottleneck | Views | Class | Root cause |
| --- | --- | --- | --- | --- |
| 1 | Empty forest floor away from paths | 00, 03, 12, 13, 16, A05, R01, all gameplay lower thirds | Ground / ecology | Filler-only layer: about 3,000 small plants and litter over roughly 2.5 ha (1 per 8 m²); 2 ground-cover meshes, 1 litter mesh, 2 grasses; no landscape grass; 0 moss patches; about 40 deadwood pieces; little micro-relief |
| 2 | Weak value structure; haze-dependent atmosphere | 03, 07, 12, 17 (backlit); A01–A05 (frontlit) | Lighting | Height fog 0.012 (raised from 0.007) plus global god rays veil midground and pond; bluish fog colour; blue-white foliage specular; depth comes from haze, not layered darks |
| 3 | One age class, few species, visible repetition | 08, 09, 11, 00, 01, top view | Forest mass | 6 canopy meshes; one sapling mesh ×1,414; almost no snags; evenly spaced crowns in row-like lanes |
| 4 | Showroom interior (evidence limited) | I01, I02, D16 | Interior | Even warm fill, no dark pockets; uniform floor and plaster; generic tins in 8 rooms; one rug ×8; 31 useful props hidden |
| 5 | Front clearing and house-to-pond descent | A05, H01, H06, R01, R02, 12, 16, top view | Macro composition | Broad open area in front of the porch with a patterned scatter of one plant; three engine cubes (`YARD_AccessStep_1/2/3`) used as a concrete step |
| 6 | House still reads digital | 10, R05, R07, H01–H07 | Materials | White trim strips outside the ageing materials; clean upper plaster; uniform stretched cladding; straight plinth; pinkish porch boards; catalogue prop spacing |
| 7 | Shoreline | C03, 07, 17, S03 | Rendering + art | Faceted stepped shelf; evenly scattered single sedges; no alternating bank types; white glare and speckle noise on the water |

## 3. Exterior review

Terrain carries enclosure on the trail side; everywhere else the composition is spread-out individuals on smooth ground.

**Macro (large-scale layout)**

- Terrain has real volume in the uphill, side and descent areas (02, 04, 15). Shelf, basin and rear rise all read.
- Too flat or broad: the front clearing and porch forecourt; the pond-side path field (03/13); the ground past the exit mouth (gameplay st10); the descent slope (12, about half the frame bare brown slope).
- The top view shows the house in a sunlit open patch, with straight sunlit strips of bare ground between tree rows: a forest planted in lanes.
- The house reads as focal in 04, 08 and 15; in front views it competes with an empty foreground.

**Meso (mid-scale grouping)**

- Trees are spread-out individuals, not groups with a dominant specimen.
- Support masses work on the uphill trail (14); elsewhere same-sized juveniles are evenly spaced (12, 03).
- Connective detail is one broadleaf ground-cover mesh stamped in regular rows: front yard (A05, R01), west wall base (R07, reads as a garden border), view 16.
- Negative space does not read as intentional. Missing: varied cluster sizes, deadwood or rock anchors that plants grow from, dark gaps.

**Micro (close range)**

- Flat orange broadleaf litter cards under conifers (03, 16, H01), also wrong ecologically.
- Smooth landscape texture; stepping stones that look like floating discs (10, B04, gameplay st11); a clean grey step block.
- Moss contact almost absent; root contact only where the Megascans root patches are placed.

## 4. Forest density and ecology

The intended dense → compressed → release rhythm exists only on the uphill trail; elsewhere density is uniformly medium-sparse.

| Layer | Current | Verdict |
| --- | --- | --- |
| Canopy | about 3,100 trees from 6 meshes; tall straight trunks; sky gaps (00, 08, 15) | PARTIAL: encloses at distance, trunk gallery at mid range |
| Sub-canopy | `SM_Pine_Juvenile_01` ×1,414 plus Young Black Spruce ×395 | FAIL: one sparse, pale sapling dominates |
| Midstory | Fishermans Bush 02/03/06 (about 600) | PARTIAL: good on the trail (14); one broadleaf species everywhere |
| Understory | ferns about 880 (6 meshes) | PARTIAL: good pockets, not tied to moisture or shade |
| Ground | ground cover 640, grass 530, litter 194, moss 0, deadwood about 40, stones about 80 | FAIL |

- Canopy strong but understory missing: lower-left of 09 and 11. Ground dominant: 03, 12, 13, 16, A05. Small plants but no medium-height mass: front yard, descent.
- **Why off-path ground looks bare**, in order: no support masses for filler to connect to; filler too sparse and uniform; no landscape grass layer or micro-scale surface; terrain smooth at the metre scale; no shadow structure from nearby masses. None of this is caused by missing assets.
- **Enclosure leaks**: sky through the canopy (00, 08, 15); bright open background band behind the pond (07, 12, 17); open grassy lanes beyond the trunks (11, 09 upper-left); the front clearing.

## 5. Colour, lighting and atmosphere

The atmosphere depends on camera angle: backlit views look smoggy, frontlit views look flat.

**Colour**

- The scene compresses into three bands: sage-grey vegetation, beige haze, orange-brown ground.
- Missing: deep cool conifer greens, moss greens, wet near-black soils, restrained accents (the only flowers are 9 at the house).
- The loudest saturated element is the wrong one: orange broadleaf litter cards.
- The warm house barely reads warm from outside; only the rear door lamp does (R03, 10).
- Not a saturation problem. Fixes: dark values in foliage and ground; the blue fog colour; specular sheen on vendor foliage (through project-owned material instances); needle and twig litter instead of broadleaf cards.

**Atmosphere**

- Backlit views look smoggy, not humid (07, 17, 12). Frontlit views (A01–A05) have no depth beyond fog and are value-flat.
- No dappled canopy light on the ground in most views, except the side passage and backyard.

**Forest life**: wind, insects and pollen NOT_TESTED (stills only); 11 VFX actors (`AD_Air_*`) are placed.

**Review lights**: the `ReviewOnly_*` rect lights and `ReviewOnly_R05_LocalExposure` are still in the map and not hidden at actor level. They were recorded as disabled at component level on 2026-09-22, and the export does not show component visibility. REVIEW_REQUIRED before any lighting judgement.

## 6. Routes

The uphill trail is the best space in the game; the other routes lose their surroundings once you look off the tread.

| Route | Assessment | State |
| --- | --- | --- |
| Pond-side | Tread reads as compacted soil, but runs through a wide flat field; no displaced litter or plant intrusion at the shoulders | PARTIAL |
| Pond-left exit | Good threshold framing (gameplay st06, st08); dies into open ground past the mouth (st10) | PARTIAL |
| Side → backyard | Side passage has good pressure (st06); backyard is a flat textured pad with disc stones and a lone stump | PARTIAL |
| Uphill | Bank cut, compression, lookback (14, 15, U-series); weak on palette and repeated species | PARTIAL, near pass |

## 7. Shoreline

The shoreline fails on both counts, and neither is an asset shortage.

**Rendering problems**

- Single Layer Water grazing-angle reflection of unfogged sky gaps clips to white (confirmed at the last gate; material parameter changes had no effect).
- Speckle/dither noise on the water in stills (03, 07, 12, 17): REVIEW_REQUIRED. It may be an unconverged Lumen/SSR reflection in high-res captures; check in gameplay.

**Art problems**

- Faceted, stepped shelf geometry (C03).
- Sedges placed as evenly scattered single stems.
- No roots, logs or overhanging shrubs entering the water; no alternating bank types; flat open bank around the path.

**Overlap**: a denser, taller mass on the opposite bank would cut the sky gaps that cause the glare. Composition can reduce the rendering defect, but it does not replace a reflection-level fix.

## 8. House exterior

The house reads as an old house recently repainted, not yet a cause-weathered woodland home.

- **Remaining tells**: pure-white trim/pilaster strips outside the ageing materials (10, R05, R07); clean upper plaster on front and sides; cladding in one grey value, stretched horizontally; a straight plinth line; a plant row lined along the wall base (R07); pinkish porch boards; evenly spaced pots; clean concrete steps (H02).
- **Age consistency**: the rear plausibly reads older than the front. But the front is showroom-clean at close and medium range, not just maintained. No rain logic (drip line, sill streaks) reads at medium distance.
- **Integration**: nested well from the forest and uphill (04, 15); floats above an empty lawn from the front and west (A05, H03); roof sits well against the canopy (00).

## 9. Interior, room by room

Only the living hall (I01, I02) and kitchen (D16, dated 2026-09-23) have current visual evidence; the rest is judged from the placed-actor inventory.

| Room | Who / what | Evidence | State |
| --- | --- | --- | --- |
| Living hall / library | Evening rest and reading; herbarium rail; loveseat, armchair, fireplace, library shelf | I01, I02 | FAIL: armchair floating in open floor, console against the wall, bare floor areas, same rug twice, even warm fill |
| Kitchen / pantry | Daily cooking: range, hutch, kettle, tea/coffee, onions, bread board | D16 | FAIL: tidy catalogue look; dishes, bread and rags placed but hidden; orange-flooded light |
| Workshop / mask work | The resident's craft: mask workbench, work-in-progress mask, pigment rack, clamp lamp, tool caddy | none | UNVERIFIED (strongest story on paper) |
| Reading room | Books ×30+, reading armchair, floor lamp | none | UNVERIFIED |
| Bedroom | Patchwork bed, wardrobe, curtains, herbarium leaf, sewing surface | none | UNVERIFIED |
| Bathroom(s) / lower WC | Enamel bath, towels, soap, vanity | none | UNVERIFIED |
| Lower store / attic | Crates, family cases, photo box, keepsakes | none | UNVERIFIED |

Staging leftovers still placed in or near the house (REVIEW_REQUIRED): `House/UnusedCatalog` (7 visible items); `ASSET_YARD` catalogue meshes, one at (2500, 150) outside the house; `House/Balcony/Ivy` built from engine cubes and cylinders.

## 10. Interior lived-in quality

The primary story objects are strong; the supporting, micro, wear and light layers that make it feel lived-in are missing.

| Aspect | Assessment |
| --- | --- |
| Primary story objects | Present and specific |
| Supporting groups | Thin: usage folders hold 1–7 generic items each (tins, crates, buckets), repeated in every room |
| Micro story | Mostly hidden or absent |
| Material history | Uniform floorboards (I01), clean plaster, no traffic, contact, soot or dust; contradicts the weathered exterior |
| Lighting | Filled, warm and even; no hierarchy or dark pockets (I02); hotel-like |

**Interior acceptance matrix**

| Row | State |
| --- | --- |
| Composition | FAIL |
| Circulation | PASS in I02 only |
| Density | FAIL |
| Wear | FAIL |
| Clutter logic | PARTIAL |
| Furniture placement | PARTIAL |
| Storytelling | REVIEW_REQUIRED |
| Floor/wall variation | FAIL |
| Light hierarchy | FAIL |
| Dark/light rhythm | UNVERIFIED |
| Window integration | PARTIAL |
| Room identity | UNVERIFIED |
| Continuity with exterior | FAIL |
| Performance | UNVERIFIED |

## 11. Existing asset library

Every need below is already installed and unused or underused.

| Need | Installed but unused or underused |
| --- | --- |
| Sapling / young-growth variety | PN_coniferBushes Spruce_01–08, Pine_01–07, Larch_01–07; PineForest SonoSapling01–04, PineTreeLow/LowMed/LowSmall; Calysto Black_Spruce_01–05; Fir_Tree_05–08 |
| Snags / deadfall | PineTreeLowDead01–05, PineDeadTrunk04, FallenTree01, TrunkPile01; Calysto Dead_Tree_01–03, Fallen_Log_01/02, Branches_Batch_01–04; OakForest FallenBranch/DryBranch |
| Needle / twig litter (correct under conifers) | PN Pine/Spruce/Larch GroundTwig_01–04, DeadPineNeedle01, PineGroundPatch01–06, ForestTrailPatches01/02, ForestFloor SM_FF_01–12 |
| Moss / fungi | GroundMossPatch01–03 (0 placed), MossClump01, MossPlant01, MossLeaf01–04; Calysto MossPatch, Dryad_Saddle fungi; Mushroom01–05 |
| Understory variety | GroundCover02/04; OakForest GroundPlant_1–5; Environment_Set nettle, heather, clover, ground_foliage (incl. flowering); Calysto Bunchberry ×6 (restrained flower accent), Fireweed (clearing accent); GrassLarge, GrassSmallDead; Galli grasses A–J |
| Midstory variety | Fishermans Bush 01/04/05/07–10; PineForest Bush/BushB/BushC; Calysto Bog_Laurel, Speckled_Alder |
| Shoreline | Sedge clumps 01–04, Sedge 03/05/06; Bluejoint grass clumps; SalixElag willow bushes; Speckled_Alder; Fab River pack (Riverbank, River_Branch_Root, River_Log, Pebbles, River_Vegetation); OakForest Scatter_Water |
| Interior micro story | Fishermans_Cabin: dishes ×32, glasses ×24, books ×14, candles ×16, spice rack ×32, kitchen add-ons ×19, picture frames ×9, hung clothes, rags, notebook, matches, thermos, keys, clocks; InfinityAssets about 27 carpet variants |
| Ground / wear systems | Landscape grass output (none configured); habitat mask `T_EX_RefugeHabitat`; owned decals `MI_HP_SettledDust`, `MI_HP_WindowRunoff` |

## 12. Asset-gap matrix

Every gap resolves to existing assets, a project-owned derivative, or a material/procedural/rendering fix.

| Area | Visual need | Existing candidates | Actual problem | Gap class | Solution |
| --- | --- | --- | --- | --- | --- |
| Off-path floor | Continuous micro layer | GroundTwig, needle and ground patches, FF patches, moss | Sparse, uniform, wrong litter | Material / procedural + existing | Landscape grass from the habitat mask, no shadows, short cull; hand-placed clusters |
| Off-path floor | Medium-height habitat mass | Ferns, nettle, heather, GroundPlant, Bog Laurel | Filler without support masses | Existing sufficient | Hero → support → filler clusters with a stated cause |
| Sub-canopy | Young-growth variety | PN spruce/pine/larch, SonoSapling, Black Spruce | One mesh ×1,414 | Existing sufficient | Replace about half; vary scale and age |
| Canopy | Age classes, snags | PineTreeLowDead, Dead_Tree, Fir 05–08 | Even-aged stand | Existing sufficient | Groups with dominants; snags with a cause |
| Deadwood | Storm/decay history | Fallen_Log, FallenTree, TrunkPile, Branches_Batch | About 40 pieces | Existing sufficient | Source-tree logic |
| Foliage colour | Dark cool greens, less sheen | Existing foliage materials | Blue-white specular; sage cast | Derivative | Project-owned MIs (spec/roughness/tint), never vendor edits |
| Shoreline | Alternating bank types | River pack, sedge clumps, willow, alder | Faceted shelf, single stems | Existing + terrain | Terrain reshaping + bank families |
| Shoreline | No white glare | — | Grazing-angle sky reflection | Rendering | Reflection/fog/exposure fix + opposite-bank mass |
| House | Cause-based age on trims and plaster | `M_EX_Integration_ExposureLime` family | Trims excluded from the ageing pass | Derivative | Assign the owned ageing MIs to the trims; stronger rain/shelter age on the front |
| Porch | Worn boards, owned props | `MI_EX_VerandaBoards_Weathered`; Fishermans props | Hue outlier, catalogue spacing | Derivative + existing | Correct hue; group props by use |
| Front yard | No concrete step | — | Engine cubes | Existing (remove) | Delete, or replace with a natural step |
| Interior | Micro story, rug variety | Fishermans interior set, InfinityAssets carpets, 31 hidden props | Hidden / generic / repeated | Existing sufficient | Re-dress by room story |
| Interior | Wear, dust | Owned decals, material variation | Uniform, clean | Material / procedural | Traffic, contact and dust logic |
| Interior | Craft hero props (masks, pigments) | Project-built R3/R05 pieces | Fidelity UNVERIFIED | Possibly generation-suitable | Inspect first (section 13) |

## 13. Genuine asset shortages and purchase candidates

**No external asset purchase is currently required.**

- No generation-class shortage is proven either.
- **Watch item, not a proven shortage**: the bespoke craft hero props (masks, pigments, herbarium pieces) are built from primitives, and their close-up fidelity is UNVERIFIED because there are no current views. If close captures show they fail, the class is GENERATION SUITABLE through `sphirus-asset-pipeline` (project-specific objects), priority MEDIUM.
- **Purchase candidates**: none. No gap passed the purchase gate, so no market research was done.

## 14. Exterior production plan

Ordered by dependency and visible impact. No item has a genuine asset gap.

| Pass | Visible problem | Root cause | Skills | Existing assets | Evidence needed | Acceptance |
| --- | --- | --- | --- | --- | --- | --- |
| E0 Baseline | Current state cannot be judged without matched views | No fresh baseline; review-light shipped state unconfirmed | environment-art (pass 0), editor-automation, source-control asset safety | — | Checkpoint; matched stations; confirm every `ReviewOnly_*` light and the review exposure volume are disabled | Baseline sheet tied to the saved map |
| E1 Forest floor and understory | Empty forest floor (bottleneck 1) | Filler-only ground; wrong litter under conifers | environment-art (passes 4–5), worldbuilding, project-assets, performance | Section 11 ground, moss, litter, understory rows | Gameplay forward, ±90°, lookback at all route stations + 00, 03, 12, 16, A05 | No gameplay frame >25% single-value ground; Tier ≥3 at thumbnail; GPU within about 1 ms of baseline; ground cover casts no shadows |
| E2 Front clearing and descent | Lawn-like hero view; engine-cube step | Macro composition; missing framing masses | level-art-direction + environment-art | Existing shrubs, saplings, deadwood | H01, H06, A05, 12, 16, gameplay front stations | 1–2 person footpath; asymmetric framing; no broad clearing |
| E3 Forest structure | Even-aged stand; dead-looking sapling; sky leaks | 6 canopy meshes in lanes; one sapling ×1,414; almost no snags | environment-art (passes 3–4) | Section 11 sapling, snag, deadfall rows | 01, 08, 09, 11, top view, ±90° | No clone rhythm or lanes; readable age classes; key views closed at canopy |
| E4 Value and atmosphere | Smoggy backlit, flat frontlit, blue-grey foliage | Haze and god rays carry depth; bluish fog; foliage sheen | visual-art-direction + materials/lighting/rendering | Existing light, fog, post actors; owned foliage MIs | A01–A05, 07, 12, 17 side by side | Depth without fog; three clear value masses per view; no global saturation change |
| E5 Shoreline | Faceted shelf, single sedges, glare, speckle | Terrain and bank composition (art); grazing sky reflection (rendering) | environment-art (pass 6) + materials/lighting/rendering | Section 11 shoreline row | C01, C03, 07, 17, S03, gameplay pond stations | Alternating banks; no clipped glare in gameplay; noise checked in gameplay |
| E6 House materials | White strips, clean plaster, uniform cladding, pink boards | Trims outside ageing materials; weak front rain/shelter logic | environment-art (house age logic) | Owned ageing MIs | 10, R01–R07, H01–H07 | Front facade row reaches PASS; interior floor unchanged |
| E7 Route shoulders | Flat pond-side field; exit dies past the mouth | No shoulders or intrusion; nothing beyond the mouth | level-art-direction + environment-art | Existing ground and midstory | Gameplay runs both directions, zero stalls | Continuation beyond every mouth; routes readable without markers |
| E8 Life and final polish | Motion, insects, pollen unknown | Not verified (stills only) | vfx-atmosphere-niagara + aaa-environment-polish | `AD_Air_*` systems; foliage wind | 5–15 s traversal video | Particles only in sun pockets; full 16-row exterior matrix |

## 15. Interior production plan

The room baseline comes first; five of seven rooms have no current evidence.

| Pass | Visible problem | Root cause | Skills | Existing assets | Asset gap | Evidence needed | Acceptance |
| --- | --- | --- | --- | --- | --- | --- | --- |
| I0 Room baseline | Most rooms unseen | No interior captures since the rebuild | interior-lived-in | — | No | Entry, main, close view per room with shipped lights; needs an authorized session (the capture tool dirties the map) | All 14 interior rows scored |
| I1 Lighting language | Even warm fill; orange-flooded kitchen | Fill instead of window key + practical accents | interior-lived-in + materials/lighting/rendering | Existing practical lights | No | Same room views | Window key; one brightest story area per room; dark corners; review lights off |
| I2 Composition (living hall first) | Furniture placed into available floor space | No grouping around use | interior-lived-in | Existing furniture | No | I02 matched | Seating group anchored on its rug; nothing floating |
| I3 Lived-in dressing | Generic tins; one rug ×8; daily props missing | 31 useful props hidden; micro story not placed | interior-lived-in + project-assets | 31 hidden props, Fishermans_Cabin interior set, InfinityAssets carpets | No | Per-room views | Clear primary / supporting / micro layers; no showroom, no hoard |
| I4 Material history | Uniform floor and plaster | No wear logic | materials/lighting/rendering | Owned decals, material variation | No | Close views | Traffic, contact, soot, dust follow cause; decal edges never read |
| I5 Craft story in sightlines | Strongest story not visible in any current view | Unknown until I0 | interior-lived-in (asset-pipeline only if needed) | R3/R05 craft pieces | Possible generation, only if inspection fails | Close views of craft props | Craft story readable at medium range |
| I6 Cohesion and final review | Clean interior vs weathered exterior | Exterior aged, interior not | aaa-environment-polish | — | No | Full-house sequence | Continuity row passes; full interior matrix |

## 16. Highest-value next pass

**E1: forest floor and understory habitat pass, zone-locked to house → front path → descent → pond-side path.**

- **It is on screen almost all the time.** The shipped over-shoulder camera puts the ground in the lower third of almost every frame.
- **It fixes three named failures at once**: empty game terrain, uniform vegetation, and the empty front clearing.
- **It needs only assets already installed.**
- **It unblocks the rest.** Lighting and atmosphere (E4) cannot be judged fairly while the midground is empty, and hazy light currently hides that emptiness.

## 17. Validation

The audit changed nothing in the project.

- [x] No production Unreal asset modified
- [x] No map modified or saved (no editor jobs, captures, gameplay sessions or exports run)
- [x] No asset imported
- [x] Nothing purchased
- [x] No foliage altered
- [x] No lighting altered
- [x] No material altered

Only file reads and offline Python over exported JSON were used, outside the editor.

**Not tested**: live unsaved editor state; review-light component visibility; water noise in gameplay; motion and wind; interior performance; 5 of the 7 interior rooms.
