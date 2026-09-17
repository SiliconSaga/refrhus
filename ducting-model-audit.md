# Duct model audit

What the drawn model says about itself, and where it disagrees with the [register schedule](ducting-register-schedule.md). Currently **74 `Ducting:` objects and 25 registers**.

**Per-run sections, lengths and materials are not repeated here** — they live in [`ducting-parts-list.md`](ducting-parts-list.md), which is generated from the model on demand. This document carries only the findings that a table cannot: how the geometry was read, what the topology can and cannot tell us, and which sizing conclusions are contested.

---

## The plenum area

Where all four supply trunks leave the air handler and the three return trunks arrive, drawn straight from `Home.xml` rather than by hand — so it cannot drift from the model the way a hand-drawn diagram does. Green is supply, yellow return, grey walls; each colour is the one the object carries in Sweet Home 3D.

The crop comes from a box named `View: Plenum area [plan]` drawn in the model itself, so moving the plenum and re-dragging the box re-cuts the figure. Runs that leave the region are clipped at the frame, which is what a close-up should do to them.

{% include schematics/plenum-area-plan.md %}

Two things this view is for. **The supply plenum takes four trunks directly** rather than one trunk splitting later, which is what keeps the largest duct in the house a 10″ instead of a 16″. And **the return plenum is ten feet long** — it runs along the joist bay rather than sitting as a box, which is why the north return arrives along its length instead of at one end.

---

## Connectivity

A 3D adjacency pass over all 74 duct objects and 25 registers at 3″ tolerance. **Every run joins something, no trunk or plenum dead-ends mid-run, and every register attaches to a duct** — the supply, SE, north and SW systems are all continuous as drawn.

**Read Sweet Home 3D's own rotated dimensions, not the raw ones.** A piece tilted by `pitch` or `roll` carries `widthInPlan` / `depthInPlan` / `heightInPlan` — the bounding box *after* that tilt — and its `elevation` is measured to the bottom of that box, not of the upright model. Nineteen of the 74 carry a non-zero pitch or roll, all of them horizontal runs drawn as pitched cylinders. Reconstructing the rotation from `width`/`depth`/`height` instead puts those runs **tens of inches off in elevation** while leaving the plan position right — so they read as badly broken chains that look perfectly joined on screen. Only the yaw (`angle`) still needs applying, to the in-plan footprint.

The SW return is the run that exposed this: trunks 3 and 4 overlap by 1″ in elevation (74–83″ and 82–91″), and a naive pass reported them 26″ apart. **Two rounds of model edits chased that phantom before the reader was suspected** — the owner's own observation that the pieces touched was correct throughout.

**The opposite mistake for the parts list.** In-plan dimensions are an axis-aligned envelope, so for anything tilted off a right angle they *overstate* the part — a rolled cylinder reported a 29″ diameter. Sections and lengths come from the raw `width`/`depth`/`height`, which are true at any rotation. Two questions, two correct answers, and using either one for the other's job produces confident nonsense.

## Topology cannot be inferred from geometry — only the return side works

Adjacency tells you two objects touch. It does not tell you they are *joined*, and in this model that distinction cannot be recovered:

- **Touching is too loose.** In the basement the branches run parallel along the joist bays and touch side by side. At 3″ tolerance the SE supply trunk comes out with **seven** neighbours and four sibling branches appear to tee into each other.
- **Intersecting is too tight.** Requiring real volume overlap disconnects the North return trunk from the return plenum — a joint that is certainly real, drawn as a butt rather than a penetration.

Joints here are a mix of butts and overlaps, so no single threshold separates a tee from a neighbour. **The return side survives anyway**, because its runs are sparse enough not to graze, and it walks into exactly the tree the design describes:

```
Return plenum
├── North return trunk → kitchen branch
│                      → main bedroom          (the buried 4x8)
│                      → kids room + basement NE (the enlarged 6x10)
├── SE return trunk   → office, play room south      (the 2nd-floor riser)
└── SW return trunk   → SW return branch (living room / SW basement)
```

**The supply side needs its hierarchy declared rather than computed**, and it already is — the trunk tables in the register schedule are hand-authored and carry the reducing schedule an installer needs. Re-deriving them from geometry would confirm something already known at the cost of real modelling discipline.

**The parts list does not need any of this.** Run membership comes from the object *names* — stem plus ordinal — so per-run length, section, material and direction changes are all derivable without resolving a single junction. That is also why duplicate names are a correctness bug rather than untidiness: two segments sharing an ordinal sort arbitrarily and the bend count silently loses a turn. The generator now refuses to run when it finds one.

## The contested sizing

**The main-floor return path was the system's bottleneck** — a single 4x8 running 30 ft with Main Bed 227, Kids Room 64 and the Utility Room's 83 all hanging off it, about 374 CFM through 32 in².

**It is now drawn as two runs, split where the duct stops being buried.** `Return branch for kids room and basement NE` takes the open basement portion at 6x10 over 8.9 ft, carrying 147 CFM at 353 fpm. `Return branch for main bedroom` keeps the buried 4x8 over 21 ft, because that is what is physically there. The two rooms that were behind the pinch are no longer behind it; the bedroom still is, and that remains a capacity problem to solve at the grille or with a transfer path rather than a duct to re-size.

**The Utility Room return shares the Kids Room branch**, which takes that branch from 64 CFM to 147. It is drawn at 8″, which runs 421 fpm and is fine; the 6″ the schedule originally specified would have run 747. A shared branch is sized for the sum, and once shared, the room name on it stops being the whole story.

**Both kitchen faces have been redrawn at the sizes the schedule asked for** — the SE supply from 2x15 to 4x15 (806 → 403 fpm) and the return from 3x20 to 8x14 (602 → 323). Getting the SE supply's 4″ of height still needs a cabinet moved or modified, so the model now records a decision that the carpentry has yet to catch up with.

### The north return trunk, and why an oval is not its box

Everything north of the return plenum funnels through two segments in series, both carrying the same **625 CFM** — kitchen 251, main bed 227, kids room and utility 147.

| Segment | Section | Free area | fpm |
|---|:-:|---:|---:|
| `North return trunk 1` — the vertical drop into the plenum | 12x12 rect | 144 in² | **625** |
| `North return trunk 2 [oval]` — the horizontal run | 14x18 oval | 210 in² | 429 |

**Trunk 2 was widened from 12x14 because its `[oval]` tag costs it area the box does not show.** The model draws a rectangular solid; the tag says what gets fabricated. A flat oval of the same overall dimensions has a semicircular end at each side rather than a corner, so 12x14 is **137 in² of airway, not 168** — and 656 fpm, not the 536 the box implies. Reading section area off the drawn box overstates every `[oval]` run in the model by roughly 20%, and the parts list prints the box because that is what a shop needs to know it must fit.

**That makes trunk 1 the binding constraint**, at 625 fpm through a genuinely rectangular 144 in². It is a 64″ vertical drop straight onto the plenum, so the fix is not the same kind of change as widening a horizontal run in a joist bay: it has to clear the plenum top and whatever the joist framing allows around it. **Unmeasured, and worth a look on the same site visit as the return split.**

## Modelling caveats

Cross-section assumes the longest edge is the run direction; where a box is nearly cubic that assumption is weak. **No elbows, tees, takeoffs or transitions are modelled**, so run lengths are centre-line and indicative, and **total effective length is not derivable from this model**. That matters more than it sounds, because effective length is what a static-pressure argument turns on — and static pressure is what decides the one-unit-versus-two question.
