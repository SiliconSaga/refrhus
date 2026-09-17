# The professional Manual J

An ACCA-approved Manual J for this house, commissioned 2026-08 from **NJ Energy Auditor** and produced in Amply. It is the independent check every number on this site is measured against, and the source of most of the thermal assumptions our own model runs on.

**The reports themselves are not published here.** They were produced for the owner as a customer, not for redistribution. This page carries the figures our work depends on — enough that every claim elsewhere on the site can be traced to a number — and nothing beyond that.

---

## Design conditions

Identical across all three progressions.

| | |
|---|---|
| Weather station | Essex County AP (#724094, ASHRAE 2021) |
| Latitude / elevation | 40.876 / 173 ft (elevation factor 0.995) |
| Indoor heating / cooling | 70°F / 75°F |
| Outdoor heating / cooling | 13°F / 89°F |
| Design grains | 27.805 |
| Daily range | Medium |

**This is a different station from ours.** Eldr resolves the model's coordinates to Newark (99% heating 14°F); the professionals use Essex County Airport at 13°F. A 1°F difference on a 57°F design ΔT, and not a source of disagreement worth chasing.

## The three progressions

The same house modelled at increasing tightness. Together they are a do-the-envelope-work-first decision tool: each shows what the equipment could shrink to if the preceding work is done.

| | Models | Heat | Cool | Heating airflow | Cooling airflow | SHR |
|---|---|---:|---:|---:|---:|---:|
| **A** | As-is today | **54,260** | 28,485 | 1,653 CFM | 1,176 CFM | 0.90 |
| **B** | + insulation | 44,067 | 25,498 | 1,343 CFM | 1,040 CFM | 0.89 |
| **C** | + air sealing | 40,901 | 25,108 | 1,246 CFM | 1,031 CFM | 0.90 |

**Progression A is the one to compare against**, because it is the house as it stands. It is the 54,260 quoted everywhere on this site.

**The envelope work is worth 13,359 BTU/hr of heating load** — A to C, a 25% reduction, or just over a ton. That is the argument for doing insulation and air sealing before sizing equipment, made in the professionals' own numbers rather than ours.

Cooling barely moves by comparison — 28,485 to 25,108, 12% — because cooling here is driven by solar gain and internal load rather than by envelope conduction.

## Construction details

The substance of the report, and where our own assemblies come from. Areas are net; HTM is heat transfer multiplier, heating then cooling.

### Walls

| Assembly | Qty | Net area | U | HTM heat / cool |
|---|--:|--:|--:|--:|
| 2x4 framed, stucco/siding, R-0 cavity | 3 | 247.9 | 0.240 | 13.58 / 6.36 |
| 2x4 framed, stucco/siding, R-11 cavity | 27 | 942.3 | 0.097 | 5.49 / 2.34 |
| 2x4 framed, R-13 cavity | 2 | 130.5 | 0.091 | 5.15 / 1.96 |
| *Garage partition, R-11 cavity* | 4 | 222.0 | 0.097 | 5.49 / 3.08 |

The three non-garage rows are **1,320.7 ft² at an area-weighted U of 0.123**, which is what `eldr-sidecar.yaml` carries for `exterior_wall`.

### Below-grade walls

| Assembly | Qty | Net area | U | HTM heat / cool |
|---|--:|--:|--:|--:|
| Avg depth 3 ft — 8″ stone/brick, no framing, no finish | 2 | 186.8 | 0.293 | 16.58 / 1.68 |
| Avg depth 4 ft — 8″ stone/brick, no framing, no finish | 2 | 215.4 | 0.297 | 16.82 / 2.73 |
| Avg depth 3 ft — 8″ stone/brick, wood frame R-11, finished | 3 | 371.6 | 0.088 | 4.98 / 0.68 |

**773.8 ft² at an area-weighted U of 0.196.** Note the depth column: the same construction is tabulated at 0.293 at three feet and 0.297 at four, because the effective U includes the soil path. That is the mechanism Eldr has no concept of, and the reason `basement_wall` is deliberately held at 0.07 rather than adopting 0.196 — see [the comparison](index.md).

### Ceilings

| Assembly | Qty | Net area | U | HTM heat / cool |
|---|--:|--:|--:|--:|
| Under vented attic w/o radiant barrier, R-11 | 1 | 40.4 | 0.081 | 4.58 / 4.03 |
| Under vented attic w/o radiant barrier, R-13 | 3 | 541.2 | 0.070 | 3.96 / 3.49 |
| Under vented attic w/o radiant barrier, R-19 | 6 | 965.7 | 0.049 | 2.77 / 2.44 |

**1,547.3 ft² at an area-weighted U of 0.057.** Our ceiling U matches; our *area* is 984 ft², and that 563 ft² shortfall is the single largest remaining geometry gap — the sloped roof and knee-wall surfaces nobody has drawn.

### Floors

| Assembly | Qty | Net area | U | HTM heat / cool |
|---|--:|--:|--:|--:|
| Passive floor exposed to outdoor air, no insulation | 1 | 264.5 | 0.521 | 29.49 / 6.21 |
| Basement floor >2 ft below grade, 32″ short slab edge | 3 | 713.9 | 0.020 | 1.13 / 0.00 |

The slab's **0.020** corrected an Eldr assumption that had been overshooting 2.5×. Its cooling HTM of 0.00 matches our own treatment: below-grade soil is a heat sink in summer, not a source.

### Windows and doors

Ten window rows totalling **152.5 ft² at an area-weighted U of 0.588**, which is the figure `eldr-sidecar.yaml` carries.

| Orientation / type | Qty | Area | U | SHGC |
|---|--:|--:|--:|--:|
| NE clear single pane | 2 | 8.3 | 0.900 | 0.64 |
| NW clear single pane | 1 | 9.8 | 0.900 | 0.64 |
| NW clear single pane w/ storm | 1 | 9.1 | 0.570 | 0.56 |
| NE LowE double | 2 | 15.0 | 0.550 | 0.56 |
| S LowE double | 2 | 20.9 | 0.550 | 0.56 |
| SE LowE double | 3 | 26.6 | 0.550 | 0.56 |
| SW LowE double | 2 | 10.7 | 0.550 | 0.56 |
| W LowE double | 2 | 18.5 | 0.550 | 0.56 |
| SE LowE double (3A) | 1 | 6.8 | 0.530 | 0.56 |
| SW LowE double (3A) | 1 | 26.8 | 0.530 | 0.56 |

**Four single-pane units survive**, 27.2 ft² between them — 18% of the glass carrying 24% of the window heat loss. Three are bare at U-0.900; the fourth has a storm sash and comes in at 0.570. A blended U cannot put them in the rooms that have them, which is the whole of the residual window disagreement with our model.

No skylights. Doors are **82.3 ft²**: one glass door at 43.4 ft² (U-0.530), a solid-core wood door with storm at 21.5 ft² (U-0.280), and a fibreglass-core metal door at 17.4 ft² (U-0.600).

## General, internal and infiltration

From progression A.

| | |
|---|---|
| Year built | 1946 |
| Stories / bedrooms | 2 / 4 |
| Estimated living area | 1,604 ft² |
| Scanned living area | 2,261 ft² |
| Conditioned basement | yes |
| Fireplaces | 1 |
| Ventilation | none |

**Occupants: 5**, on the ACCA bedrooms-plus-one convention, contributing 4,550 BTU/hr of cooling (3,550 sensible, 1,000 latent) under a 2,400 BTU/hr standard kitchen/utility/lighting scenario, and nothing to heating. Our model agrees at 5 — the actual headcount and the convention happen to coincide.

**Infiltration is 13,154 BTU/hr of heating**, about a quarter of progression A's total, and the largest single line in the report.

---

## Two things in the reports that are easy to miss

**The measured blower door exists only in handwriting.** Progression C's infiltration panel prints `Blower Door · 1,751 CFM50 · ACH 0.32`, annotated **"speculative"** — C models the *proposed post-air-sealing* state, not the house today. The real measurement is a margin note:

> **"At Audit BD was 3751! w/ACH 0.68"**

So the measured as-is figure is **3,751 CFM50 → ACH 0.68**, and that is what `../eldr-sidecar.yaml` uses. Progression A's printed infiltration is *not* a measurement: its method line reads `Tightness: Loose`, an ACCA tightness-class estimate, with the note *"Would measure >=10 ACH50 via blower door test. Common for homes built pre-1950."* Do not cite A's figure as measured.

The arithmetic was checked against Eldr's own conditioned volume, which at the time came to 16,457 ft³: 3,751 CFM50 × 60 ÷ 16,457 = 13.7 ACH50, over an LBL N-factor of ~20 (two storeys, shielding class 4) = **0.68**. Two engines agreeing on a volume neither took from the other is a real cross-check.

**That volume has since moved to 16,859 ft³** as the basement was measured and the model gained detail, which puts the same blower-door reading at ACH **0.67**. The side-car still carries 0.68. The difference is worth about 170 BTU/hr against a 40,331 total — below every other open item — but the figure is derived rather than measured, so it should be re-derived whenever the volume moves.

**They load below-grade surfaces at the full outdoor ΔT.** Divide HTM by U on every below-grade row — 16.58/0.293, 16.82/0.297, 4.98/0.088, and the slab's 1.13/0.020 — and all four give **56.6**, against their design ΔT of 57 × the 0.995 elevation factor. The soil path lives *inside* the U-value, which is why U-0.293 sits far below bare 8″ masonry (~1.0 on its own).

That is standard Manual J, and finding it is what corrected Eldr, which had been applying an effective U *and* a ground ΔT — discounting twice. Their below-grade **cooling** HTMs do not divide out to a constant (5.73 / 9.19 / 7.73), so cooling below grade is not a single ΔT.

## Reading the numbers against ours

The line-by-line comparison, and where the two engines still disagree, is on [the load calculations page](index.md).
