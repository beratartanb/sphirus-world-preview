# SPHIRUS — BR_ArtistNeutral sculpt guide (Blender 5.2)

This file is the only thing you sculpt. Your work goes back into Unreal as a morph target.
That only works if the mesh keeps exactly the same vertices, triangles, UVs and weights.
Everything below is designed so you can't break that by accident, as long as you follow the red rules.

---------------------------------------------------------------------------------------------------
## 0. RED RULES (breaking any of these makes the file unusable)

1. Sculpt ONLY the object **SPH_BR_ArtistSculpt**, ONLY in **Sculpt Mode**, ONLY on shape key **ARTIST_SCULPT**.
2. NEVER use: Dyntopo (Dynamic Topology), Voxel Remesh (Ctrl+R), QuadriFlow Remesh, Multiresolution,
   Subdivision Surface (applied), Decimate, Remesh, Weld/Merge by Distance, Triangulate, Symmetrize,
   Trim/Boolean tools (Box/Lasso/Line Trim), Mask Extract, Mask Slice, Face Set Extract, Separate, Join.
3. NEVER enter Edit Mode to move/add/delete anything. NEVER "Apply" anything. NEVER add modifiers.
4. NEVER unhide the head (Alt+H) or clear/invert the mask (Alt+M / Ctrl+I) and keep sculpting —
   press **Restore Protection** afterwards if it happened.
5. NEVER edit, rename, reorder or delete shape keys or vertex groups.
6. Do not move/rotate/scale the object.
7. Save often, with **File > Save Incremental (Ctrl+Alt+S)** — never overwrite the _PRISTINE file.

---------------------------------------------------------------------------------------------------
## 1. Opening the file

1. Open `SPH_BR_ArtistSculpt_20260929.blend`.
2. If Blender shows a yellow bar "Automatic execution of Python scripts is disabled", click **Allow Execution**
   (the only script is SPH_TOOLS.py, the helper panel; it never moves vertices).
   If you missed the bar: switch any area to **Text Editor**, choose **SPH_TOOLS.py**, press **▶ Run Script**.
3. Click the **Sculpting** workspace tab at the top (if not already there).
4. Press **N** in the 3D view → sidebar → tab **SPHIRUS**. The box must say
   **"Sculpting ARTIST_SCULPT"** with a check mark. If it says WRONG KEY/STATE → press **Restore Protection**.

What you see:
- The body (clay colour) = SPH_BR_ArtistSculpt, already in Sculpt Mode.
- The head/face = **SPH_LOCKED_HEAD_DISPLAY**, a non-selectable display copy. The real head vertices are hidden
  inside the sculpt object and can't be sculpted. The face is identity-locked at 0 mm.
- A dark overlay on the neck base and head collar is the protection **mask**. Masked = cannot move.
  It fades out gradually below the head so no ridge forms.

---------------------------------------------------------------------------------------------------
## 2. Protection (already set — never touch)

| Protected | How | Why |
|---|---|---|
| FACE_LOCK | vertex group + mask 1.0 + hidden | face identity (0 mm) |
| HEAD_IDENTITY_LOCK | vertex group + mask 1.0 + hidden (all head verts above z 147 cm) | full head identity + 2 cm buffer below the QA line (z 149) |
| SEAM_LOCK | vertex group + mask 1.0, 3-ring feather | head/body seam (92 vertex pairs) must stay coincident |
| HANDS_FEET | not masked, but DO NOT sculpt | out of scope for this pass |

Shape keys (do not edit): **ACCEPTED_B2** (basis = accepted B2), **BR_NEUTRAL** (current body realism),
**SCULPT_BASE** (start snapshot = BR_NEUTRAL). All three are locked (padlock). **ARTIST_SCULPT** (value 1.0)
is your working key. It started identical to BR_NEUTRAL.

Region vertex groups (for isolating work, not locks): NECK_COLLAR, SHOULDERS, CHEST_RIBCAGE, BREASTS, ABDOMEN,
UPPER_BACK, LOWER_BACK, PELVIS_HIPS, GLUTES, THIGHS, KNEES, CALVES_ANKLES, UPPER_ARMS, ELBOWS_FOREARMS.
The ~900 other groups are the Unreal skin weights (bone names). Ignore them.

---------------------------------------------------------------------------------------------------
## 3. The SPHIRUS panel

- **Restore Protection** — re-applies the lock mask, re-hides the head and resets the shape-key state. Safe any time.
- **Isolate region** (e.g. *Breasts*) — masks everything except that region (soft edges). The locks stay on.
  Use it for every region task below. **Clear isolation** returns to the normal lock mask.
- **Compare** — *Start* shows BR_NEUTRAL, *B2* shows the accepted B2, *Side* shows both beside your sculpt, and
  *Sculpt* returns to work (and back into Sculpt Mode). Compare often: the change must read as refinement, not a new body.
- **Overlays** — *Anatomy guides* (clavicle, scapula, ribcage/costal margin, sternum, iliac crest, ASIS/PSIS, inguinal line,
  inframammary fold, gluteal fold, patella, Achilles, landmarks), *Measurement rings* (where the circumference
  gate is measured), *Bind skeleton*. Guides are **approximate references**: sculpt anatomy, not lines.
- **Validate Sculpt** — read-only check (topology, UVs, weights, locks, seam, height, circumferences). Run it after every region.
  Result: panel + Text Editor → *SPH_LAST_VALIDATION*, and a JSON next to the .blend.

---------------------------------------------------------------------------------------------------
## 4. Symmetry

- **X symmetry is ON** (Sculpt header, butterfly icon, X highlighted). This is safe: it mirrors brush strokes,
  never topology. Keep it ON for Passes 1–3.
- Turn X OFF only for Pass 4 (natural asymmetry), then turn it back ON.
- **Topology mirror = OFF** (do not enable). Edit-mode X-mirror is irrelevant: never use Edit Mode.

---------------------------------------------------------------------------------------------------
## 5. Brush kit (Blender 5.2 Essentials) and settings

The mesh has about **1 cm edges** (0.7 cm on the forearms). Forms narrower than about 3 cm won't hold, so leave pores,
veins and skin-level detail to the normal map. Brush radius in the header is in screen pixels. The file starts at
70 px and strength 0.25. Zoom so the full region you work on fills about half the screen.

| Brush | Use | Strength | Notes |
|---|---|---|---|
| **Clay Strips** | build/lower broad planes (ribcage planes, glute mass, thigh mass) | 0.10–0.25 | Ctrl = carve. Many light strokes. |
| **Draw** (or Draw Sharp for very fine lines: avoid) | soft swellings/hollows | 0.05–0.15 | falloff Smooth |
| **Inflate/Deflate** | soft-tissue fullness (breast lower pole, glute, calf) | 0.05–0.10 | tiny doses |
| **Smooth** (hold Shift) | blend every stroke; remove lumps | 0.3–0.5 | Shift-smooth after each form |
| **Flatten/Contrast** | tighten a plane (sternum, sacral plane, shin) | 0.1–0.2 | |
| **Crease Polish** | ONLY for real folds (inframammary, gluteal fold) | 0.05–0.1 | never on muscles |
| **Elastic Grab** | move a soft mass slightly (≤ 5 mm) | 0.3 | big radius |
| **Mask** | not needed — use Isolate region instead | | |

Amplitude discipline: **typical change 1–4 mm, local maximum 6–8 mm**. The validator warns above 8 mm and fails
above 20 mm. Circumferences may drift ±5 mm (warn) and must stay within ±10 mm (fail beyond). Height ±1 mm,
shoulder width ±5 mm. If a form needs more than about 5 mm, it's probably a body-type change. Don't do it.

---------------------------------------------------------------------------------------------------
## 6. Workflow — passes (X symmetry ON unless stated)

Keep the same woman and body type throughout. The priorities are, in order: stay the same character, convincingly human,
natural feminine attractiveness, soft-tissue anatomy, clean for clothing.
Current state: neck/clavicle, back, knees and calves already read well. Chest/breasts, abdomen, arms, glutes and thighs
are too subtle / too "neutral mesh". **Spend most time there.**

**Pass 1 — Primary masses (≈ 40 % of the time).** Clay Strips + Smooth. Look at silhouettes from all five cameras.
**Pass 2 — Secondary forms.** Draw / Inflate / Flatten at low strength, per region (section 7).
**Pass 3 — Soft-tissue transitions.** Smooth and Crease Polish (folds only). Check the transitions between regions
(isolate off), especially breast → ribcage → abdomen, glute → thigh and deltoid → arm.
**Pass 4 — Natural asymmetry (X symmetry OFF), max 1–2 mm.** For example, a slightly fuller right glute, slightly different breast
shape, and one iliac crest a touch higher. Then symmetry back ON.
**Pass 5 — Clean-up.** Low-strength Smooth over everything touched (not the locks). Check with the matcap/cavity at
three zoom levels. Then **Validate**.

Save Incremental after every region and Validate after every region.

---------------------------------------------------------------------------------------------------
## 7. Region tasks (Isolate the region first)

**BREASTS** (highest priority): natural, non-augmented and gravity-aware. The upper pole is a gentle slope from under the
clavicle (no step). The lower pole is fuller and rounder. The lateral side rolls smoothly toward the armpit (keep the
axillary tail soft). A soft **inframammary fold** follows the guide, deepest under the centre and fading at the sides.
Crease Polish 0.05, then Smooth. The centre is the landmark *BREAST_CENTER_EST* (an estimate, about 9 cm from the midline). Keep the
sternum gap flat. Max about 5 mm. Don't create a round "implant" dome.

**CHEST_RIBCAGE**: the sternum is a flat plane between the breasts. The ribcage reads as a barrel under soft tissue below and
beside the breasts. There's a soft **costal margin** step along the guide (1–2 mm). Around the underbust, keep a smooth
transition, not a ledge.

**ABDOMEN**: soft and healthy, not a six-pack. There's a faint linea alba groove above the navel (≤ 1 mm) and a very slight lower
abdomen roundness below the navel. The obliques flow into the iliac crest. Keep a smooth waist, and don't carve.

**SHOULDERS / UPPER_ARMS / ELBOWS_FOREARMS**: a rounded deltoid cap with a soft front/side/rear separation (1–2 mm).
The deltoid inserts about a third of the way down the arm as a gentle taper. There's a soft biceps belly in front and a triceps mass behind with the
long-head flow. The olecranon is a small bony point at the back of the elbow (landmark) with a soft hollow each side. The forearm is fuller in the upper
third and tapers to the wrist. Feminine limbs have smoother, fatter transitions than male ones.

**NECK_COLLAR** (the lower part is masked/feathered): only a gentle trapezius slope and soft sternocleidomastoid lower heads. The
neck/clavicle area already reads well, so touch it lightly.

**UPPER_BACK / LOWER_BACK**: already good. Only unify scapula edges with soft tissue. Keep the spine valley (the guide),
the lumbar valley and the two soft **PSIS dimples** (landmarks).

**PELVIS_HIPS**: the iliac crest line (guide) is a soft shelf on the side (1–2 mm). The ASIS points (landmarks) are just visible. There's a
soft inguinal line (the guide) in front. Hip/thigh roundness flows below the crest. Watch the hip circumference (rings).

**GLUTES** (high priority): one continuous round mass with fullness in the lower-middle, not a shelf. The upper-outer
quadrant blends into gluteus medius under the iliac crest. There's a soft **gluteal fold** (the guide) under the medial
half, fading laterally, with Crease Polish 0.05. The sacral plane is a flat diamond between the PSIS dimples.

**THIGHS**: a soft quadriceps volume with the vastus medialis teardrop above the inner knee. Keep a smooth outer thigh
line with only a hint of the IT band (≤ 1 mm). The inner thigh is soft and full. The hamstrings are rounded behind. Keep the thigh ring.

**KNEES / CALVES_ANKLES**: already good. You can soften the patella outline (guide) if it looks mechanical. The calves
have a medial gastrocnemius head lower and fuller than the lateral one. The Achilles (guide) is a narrow cord with hollows each side.

**HANDS_FEET**: do not sculpt.

---------------------------------------------------------------------------------------------------
## 8. Checkpoints and hand-back

- Every region: **Ctrl+Alt+S** (Save Incremental), then **Validate Sculpt**.
- If Validate shows **FAIL**: Ctrl+Z back, or reduce the change. For lock/seam FAILs: Restore Protection, then undo the
  strokes that touched the collar. Don't try to "fix" it by editing vertices.
- **WARN** lines are review items (for example, a circumference that drifted 6 mm). Decide consciously whether they're intended.
- When finished: run **Restore Protection**, then **Validate**, and save as
  `SPH_BR_ArtistSculpt_20260929_FINAL.blend` in the same folder. Tell Claude the file name.
  Claude will re-validate, import it as **BR_ArtistNeutral** in an isolated asset set, rebase SHCB, propagate LODs,
  and run the full deformation/seam/face/proportion/persistence QA.

## 9. Troubleshooting

| Symptom | Fix |
|---|---|
| Brush does nothing | You're on a masked/hidden area, the wrong key is active, or strength is 0. Press Restore Protection. |
| "Shape key is locked" message | A reference key is active. Press Restore Protection (it re-selects ARTIST_SCULPT). |
| Head disappeared / face missing | You hid SPH_LOCKED_HEAD_DISPLAY. Press Restore Protection. |
| Head became sculptable (Alt+H) | Press Restore Protection immediately. Validate. If the face moved: Ctrl+Z. |
| Panel missing | Run SPH_TOOLS.py from the Text Editor (▶). |
| Weird lumps after many strokes | Shift-Smooth at 0.3. Compare with *Start*. |
