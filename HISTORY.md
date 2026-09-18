# Refrhus — construction history & model ground truth

The interpretation key for `Home.xml`. The model encodes a house that grew in
stages, so **the levels are deliberately different shapes** — apparent
"misalignment" between levels is usually real construction history, not a tracing
error. Read this before trusting (or "fixing") any cross-level overlay.

Captured from owner knowledge on 2026-06-13, alongside the first overlay
assessment (see `realms/realm-siliconsaga/docs/plans/2026-06-13-sh3d-overlay-tool-design.md`).

## Build sequence

1. **Original house** — roughly **800 sqft**. The current **Basement is the correct
   shape of this first edition**; the original main-floor exterior walls stood
   directly atop the **entire basement perimeter**.
2. **Garage added** — *not* original. Sits at an odd split-level height (~4 ft,
   roughly midway between basement floor and main floor). On the survey it is
   bundled with the house with **no wall drawn between garage and house**.
3. **Two main-floor extensions:**
   - **Kitchen extended north** (~8 ft up on the diagram), then a **deck** added
     north of that. The little wall **stump by "DINING AREA"** marks where the
     *original* exterior wall started, running east.
   - **Primary bedroom extended south.** The **original exterior wall crosses
     where "COVERED PORCH" begins** — i.e. the porch region is the southern
     extension.
4. **Upstairs finished** — awkwardly. The 2nd floor was expanded **south** over the
   extended bedroom (ending in a **gable with a window**, not the original sloped
   roof). It was **not** expanded north over the kitchen extension.

## Levels & elevations (from Home.xml)

| Level | elev | notes |
|---|---|---|
| Basement | 0 ft | Original ~800 sqft footprint. Background: floor plan (image 0). |
| Garage | 4 ft | Added later; split-level. Background: **survey** (image 1) — its own frame. |
| Crawlspace | 4 ft (~3–4 ft tall) | Under the kitchen north extension. Floor matches garage height. Partial, not a full level. No background. |
| basement-main-transition | 7 ft (~1 ft tall) | Thin split-level transition (stair landing). No background. |
| Main (FIRST FLOOR) | 8.4 ft | Original core + kitchen north extension + bedroom south extension. Background: floor plan (image 0). |
| 2nd floor | 16.8 ft | **Partial** floor. Original core hit only on **W & E** sides + south bedroom extension. North edge = knee-wall attic, inset ~3–4 ft **south** of the original exterior wall. Some N–S walls **angled** (roofline — not a true full floor). Background: floor plan (image 0). |

Heights are correct; the split-level/extension reality is already encoded in the
elevations. **The only thing needing work is in-plane (X/Y) frame consistency.**

## Why the Main and 2nd-floor north walls are ~8 ft apart

It is in-plane, not a level-height difference — the **kitchen's ~8 ft north
extension**:

- **Main** reaches ~8 ft north of the original exterior wall (the kitchen addition).
- The **2nd-floor** north wall ("BEDROOM 4" knee wall) sits ~**3–4 ft south** of
  that original exterior wall.
- So Main's north edge and the 2nd-floor north wall are separated by the extension
  plus the knee-wall inset — they are **not supposed to match.** Measured, the
  gap is ~243 cm / 8 ft between the north wall-bbox edges, while the south
  edges match within 3 cm.

## Basement framing — the joist datum (measured 2026-07-23)

The basement floor joists are now the **most confident geometry in the house** —
relative spacing measured to ~1/8″. Joists run **N–S**, spaced along **X (E–W)**,
numbered **west→east** (`joist-01` … `joist-25`), and are modeled on the
`basement-main-transition` level (they sit atop the basement walls). Two ~3.5″
post-width main beams and one extra joist sit in the stair area (tighter spacing).
Real-world caveat: some eastern joists **drift** (not perfectly parallel — up to
~½″ over a few feet); measure at a consistent Y. Per-bay spacing + the derived
basement width: **`basement-joists.md`**. The basement is **not a uniform box** —
zones, staggered posts/beams, and per-wall edge conditions: **`basement-structure.md`**.

**What sits on top of the cinderblock** (standard platform-framing perimeter):

- A flat plank laid atop the block, ~**centered**, shorter than a joist — the
  **sill plate (mudsill):** pressure-treated, anchor-bolted, the code-required
  wood-to-concrete interface. Along the **E & W** walls it appears to "support
  nothing" because the joists run **parallel** to those walls and bear on the
  **N & S** walls instead — so the E/W sill is just the perimeter plate (and a
  handy nailer; wires get stapled to it). Present on N & S walls' eastern half too.
- An on-edge member at the **outer edge** of the block — the **rim / band joist**
  (a.k.a. the outermost joist), capping the floor framing flush to the block's
  outer face. This is the common, expected pattern.

**East vs. west wall edge conditions differ** (important for the X frame):

- **East wall — confident.** Raw cinder is visible; a true **1″ clear gap** from
  the block's inner face to the first joist's east face. Anchor the model here.
- **West wall — fuzzy.** Wood paneling/furring hides the block; ~**8″** (estimated)
  from where the block likely ends to the first joist's west face. Confirm the raw
  west block face on the scan visit before trusting the total basement width.

**SH3D anchoring, so the model matches reality:**

- A **wall's coordinate is its centerline** — an 8″ cinderblock extends 4″ each
  side. To leave a gap to a *face*, place the line **½·thickness beyond** it.
- **Furniture X is the piece's center** — a joist face is `x ± ½·width` (±0.75″
  for a 1.5″ joist). The joists were entered aligned to their **left (west) edge**,
  so every stored center is ~0.75″ west of true — a **uniform, correctable** shift
  (nudge all joists +0.75″ E so stored X = true center; relative spacing is fine).

**Datum workflow:** treat the joists as ground truth → position the **E/W basement
walls** to the outermost joists using the real edge conditions (east 1″ + ½·wall;
west ~8″ + ½·wall) → the **basement width falls out** of the result (no independent
width measurement needed; its uncertainty lives entirely in the fuzzy west side).
Then, because the **E/W walls align across levels** (next section), that corrected
basement X frame is the anchor the Main and 2nd floors register to.

## Alignment invariants (what *should* line up across levels)

Use these — and only these — to register levels into one plan frame:

- **East & West walls** align across Basement / Main / 2nd floor (the original
  perimeter). Exceptions: the **garage**, and the **south** (extended) part of the
  2nd floor.
- **Staircase** roughly aligns first ↔ second (scale / exact placement may be a
  little off — verify, don't assume).
- **North & South walls align too — but only on the original perimeter.** See the
  clarification below.

**Do NOT** expect the **extensions'** north/south walls to align with anything
below them — they diverge by era (kitchen +8 ft north; bedroom/2nd-floor extension
south; knee-wall inset). That is real construction history, not tracing error.

**But the original perimeter is one wall stack, all the way down, on every side.**
Where the Main floor still sits on the original footprint, its north and south walls
*do* register to the basement block:

- The **north wall of the main-floor bathroom and kids room** follows the original
  perimeter — it is not an extension, and it should land on the basement's north
  block line.
- Same for the **stump near the middle of the kitchen's west wall**, which is
  north-aligned with the original wall, and the corresponding **stump on the west
  wall by the main bedroom extension**.
- The two **extensions themselves** (kitchen north, bedroom south) need their own
  measurements and must not be dragged onto the basement footprint.

Clarified 2026-08-23 by the owner, after the blanket reading nearly stopped a
justified correction. The rule is about *eras*, not about compass directions.

### Framed wall vs. cinder block — where the exterior face goes

Derived 2026-08-23. It had not been written down, so the upper floors drifted
without anyone being able to say by how much.

**A framed exterior wall's OUTER face sits on the block's OUTER face.** It follows
from the rim/band joist above: that member caps the floor framing *flush to the
block's outer face*, and the wall's sheathing continues the same plane. So an
exterior wall of thickness `t` on a level above has its centerline at
`block_outer_face ∓ t/2` — not on the block's centerline, and not on its inner face.

Two consequences follow, and both are easy to get backwards:

- The wall thicknesses **differ by level** (8″ block, 7″ framed), so aligning
  *centerlines* across levels is wrong by 0.5″ and aligning *inner* faces is wrong
  by 1.5″. Only the outer faces coincide.
- The rule may run a siding-thickness shy of exact, since siding usually laps the
  foundation with a drip edge. Treat sub-inch residuals as noise, not error.

**Anchor east, not west, and never the average.** The east gap to raw cinder is a
confident 1″; the west is a ~8″ estimate through paneling, so the basement's own
west face carries all the uncertainty in its width. Registering an upper floor onto
the *east* face puts the known end of the datum against the thing being corrected.

## Two registration seams

1. **Floor-plan levels vs. each other** — Basement / Main / 2nd all trace the same
   not-to-scale floor-plan bitmap (image 0) at independently eyeballed origins.
   Align via the E/W walls + stairs.
2. **Survey frame vs. floor-plan frame** — the Garage uses the authoritative survey
   (image 1) in a separate coordinate frame; it does not currently agree with the
   floor-plan frame. The **survey is authoritative for the true exterior footprint**;
   the floor plan is explicitly *not to scale* (good for interior layout only).

## The parcel, from the survey

The lot as surveyed 2022-09-23. Recorded here because the survey endorsement that
carried it has been removed from the repository — it was title paperwork wrapped
around four useful numbers, and these are the four numbers.

| Leg | Bearing | Length |
|---|---|---:|
| 1 | N 39°29′ E | 125.00 ft |
| 2 | S 48°05′ E | 68.15 ft |
| 3 | S 39°29′ W | 125.00 ft |
| 4 | N 48°05′ W | 68.15 ft — the street frontage |

**A parallelogram, not a rectangle** — 125 ft deep by 68.15 ft wide, matching the
`125.00'` and `68.15'` dimensions printed on `SurveyAlone.png`, but with interior
angles of **92°26′ and 87°34′**. Opposite sides are equal and parallel; the corners
are not square. Anything that squares the house to the lot boundary inherits that
2.43° error.

**The frontage bearing is the one that matters beyond the footprint.** The street
line runs N 48°05′ W, so a front elevation square to the street faces roughly
**S 42° W** — which is the source of the "front faces roughly southwest" claim used
in the window and solar-gain reasoning. Anything that re-derives orientation should
reconcile against this rather than against the floor plan, which is not to scale and
carries no true north at all.

**Not recorded, deliberately:** the street address, deed book reference, tax lot and
block, title file number and surveyor details that accompanied these bearings. None
of them affect any measurement, and this repository is public.

## Background-image facts (for any registration math)

Placement, taken verbatim from `PlanComponent.paintBackgroundImage`:

- `plan = pixel · scale − origin`; image top-left sits at plan `(−xOrigin, −yOrigin)`.
- `scale = scaleDistance / dist(scaleStart, scaleEnd)` (cm per image-pixel).
- Plan **Y is down**; SH3D background images **cannot be rotated** (the two scale
  points only set a scalar scale) — any rotation must be baked into the image file.

| Image | file | size | cm/px | used by | origin(s) |
|---|---|---|---|---|---|
| Floor plan (not to scale) | `0` | 1940×1500 | 1.5646 | Basement, Main, 2nd | (−10.2, 788.7) / (574.3, 308.4) / (1902.2, 121.4) |
| Survey (authoritative) | `1` | 645×1020 | 3.9862 | Garage | (320.0, 1013.5) |
