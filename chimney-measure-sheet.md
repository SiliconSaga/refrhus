# Chimney — measurements and derived position

First measured 2026-09-01/02. **Approximate mockup grade**, not final: the chimney's absolute position still disagrees with its own tape chain by about 2″, and the main and second floors are drywalled so their masonry is inferred rather than seen. Good enough to lay out a stacked utility closet; not good enough to cut anything.

The chimney is the spine of the duct plan — it is what the utility cabinet routes around on all three levels, and the only element besides the stairs that pierces every floor.

---

## What was measured

### Basement — the only level with raw cinder

| | Measurement |
|---|---|
| South face, east–west | **~16″** — one full masonry unit, maybe a shade less in places |
| East face, north–south | **~16″** — likewise one unit |
| West face to the centre wall's east face | ~1″ |
| West face to the joist-15 beam's east face | ~1″ |
| **South face to the south cinder inner face** | **94″** |
| North step-out | ~one unit (**8″**) deeper, beginning ~12″ below the joists and continuing down |

The main girder lands on a **4x4 stump** atop the top block of that step.

**So the basement chimney is 16 × 16 in its upper reach and 16 × 24 below the step**, the extra 8″ on the north side.

**On the masonry unit.** 16 × 16 with a void down the middle is a **chimney block** (flue block) — a standard product, typically 16 × 16 × 8 with a cast opening for the flue liner. One block per course rather than four cinder blocks around a hole, which makes the void and the 16″ faces consistent rather than contradictory.

### Main floor — drywalled, masonry inferred

| | Measurement |
|---|---|
| South face, east–west | **19.5″** |
| East face, north–south | **20.25″** |
| South face to the stump wall's north face | **94.25″** |

The box is **integrated into the interior wall on its north side**, with a closet beyond.

That last fact explains the wrap arithmetic. Against 16″ of masonry the box carries 4.25″ of wrap north–south, but the 94.25″ reading puts only **0.75″ of it on the south** — leaving ~3.5″ on the north, which is a stud wall with drywall both sides. The asymmetry is the wall, not a bad measurement.

### Second floor — drywalled

| | Measurement |
|---|---|
| South wall | **17 5/8″** |
| East wall | **17 5/8″** |
| North wall | **18 1/4″** |
| Gap, box north face → bathroom wall | **4 7/8″** (original wood paneling inside it) |
| Box south face → south wall's north face | **56.5″** |

---

## Derived position

Taking the stack as plumb — chimneys are — and anchoring on the basement's 94″:

| Level | x | y |
|---|---|---|
| Basement, upper (16 × 16) | 501.5 – 517.5 | **401.0 – 417.0** |
| Basement, lower (16 × 24) | 501.5 – 517.5 | **393.0 – 417.0** |
| Main, box (19.5 × 20.25) | 499.75 – 519.25 | **397.5 – 417.75** |
| 2nd floor, box (17.625 sq) | 500.7 – 518.3 | **400.2 – 417.8** |

Two positions fall out of the second-floor readings and are worth having in the model:

- **Bathroom wall, south face: y ≈ 395.3** — the 4 7/8″ gap north of the chimney, which the model showed as nothing at all.
- **Knee wall, north face: y ≈ 474.3** — from the 56.5″. Beyond it to the original south perimeter (interior face 511.0) leaves roughly **32″ of attic depth**, once the wall's own thickness comes out.

The basement's 94″ and the main floor's 94.25″ agree to three-quarters of an inch across two levels — the first independent cross-level check this house has produced.

---

## Under the stairs — the space the closet has to live in

Measured on the wall between the staircase door and the chimney, sketched by hand 2026-09-02.

- **Two 15″ stud bays.**
- **Stair diagonal:** 3″ of headroom at the south stud, 18″ at the middle, ~36″ at the north. Roughly 33″ of run, so a clean **45°** — matching the observed "8 inches per step every 8 inches".
- **The chimney sits behind the wall**, about 1″ off its face, and reads on the sketch as a line partway across the north bay. It takes out **roughly half the north bay's width**.
- Overall the closet gets **just over 40″ of wall × ~16″ deep**, its ceiling cut by the diagonal.

Consequence for ducting: the north bay is tall but half-blocked, and the south bay is a triangle whose headroom falls away to nothing. Only about 9–10″ of the south bay's length has 10″ or more of clearance, so **it is a place to cross, not a place to run**.

---

## Still open

- **The 2″ disagreement.** The 94″ chain puts the south face at **417.0**; the model carries **415.0**. Irrelevant for a relative layout where all three levels share one line, and it matters as soon as the closet meets real joists.
- **The wrap thickness on main and second floors** is inferred from the box dimensions, not measured. Only the basement exposes raw cinder.
- **`Chimney Void` is oversized** in the model — the flue is smaller than drawn. Left approximate deliberately while wall thicknesses and positions were being sorted.
- **A one-inch joist discrepancy nearby:** 12″ measured between the joist-15 beam and joist-16 where the grid records 13.0″, while joist-16 → joist-17 matches (13.25 against 13.37). Larger than the recorded ~½″ drift. Shifting joist-16 cascades east, so it wants one more reading before anything moves.

## Structural claims still to confirm

From `basement-structure.md`, unverified:

- The east cross-beam runs chimney → east wall, seated in a cinder pocket.
- The joist-15 beam passes **behind** the chimney without bearing on it. Confirm it before anyone cuts.
