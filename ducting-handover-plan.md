# Handover package — design plan

Written 2026-09-07, deliberately before a context compaction, so the next session can pick this up cold.

**Goal:** turn the duct design into something an HVAC company can be handed — a public GitHub Pages site with real navigation, backed by the measured model, carrying a parts list and renders. The company still favours a second air handler upstairs; this package is the argument against it, made in their own units.

**`Cervator/refrhus` is public**, as is `SiliconSaga/eldr`. Refr Hus is a public worked example of GDD applied to home improvement, and public repos publish Pages on the free plan — so neither the Pages tier nor CI repo access is a constraint.

---

## Where things stand

| | State |
|---|---|
| Model | Basement measurement-true; all three levels registered east–west; **74 `Ducting:` objects and 25 registers** drawn |
| Loads | Eldr, heat-pump airflow (30°F rise), biased 2nd ×1.35 / basement ×0.70 |
| Schedule | `ducting-register-schedule.md` — per-register sizes, editable |
| Audit | `ducting-model-audit.md` — drawn objects vs schedule |
| Branch | `ducts/poc`, so the diff is the proposal |

Both utility closets have ample space for any combination or placement of ducts, so cabinet capacity is not a constraint on the layout. Plenums are 12×20, sized as an estimate that will be refined at install.

**Now expressed in the model rather than carried as doc-only metadata.** The single 4x8 running 30 ft — Main Bed 227, Kids Room 64, Utility Room 83, about 374 CFM through 32 in² — is drawn as two runs split where the duct stops being buried. The open basement portion is 6x10 and carries the Kids Room and Utility returns at 353 fpm; the buried portion stays 4x8 because that is what is there. **Splitting the object was what let the model say it** — one run could only carry one section, so the distinction between the fixable half and the fixed half had to live in prose.

---

## Task 1 — Duct metadata convention

Ducts are *furniture*, and furniture names are editable directly in Sweet Home 3D. So use a **bracketed keyword in the name**, the same convention already established for tagging windows:

```
Ducting: SE supply trunk 3 [spiral]
Ducting: Return branch for main bed room 1 [oval]
Ducting: North supply trunk 4 [rect]
```

Vocabulary: `[rect]` · `[spiral]` · `[dwspiral]` (double-wall) · `[oval]` · `[flex]`

**Defaults, so most objects need no tag at all:** a box is `[rect]`, and **a cylinder is `[dwspiral]`**. Only the exceptions get written down — squeeze a dimension and add `[oval]` where oval earns its place.

Every cylinder in the model is in the basement, and every basement *supply* needs insulation against condensation anyway. That leaves exactly one return run that could be plain spiral — not worth a second product line. One round part, ordered one way.

**The explicit `[dwspiral]` tags on the supply runs stay**, even though the default now covers them, because they carry a distinction the default cannot: on a supply, double-wall is **required**; on the return it is merely **convenient**. If cost ever forces the question, the tagged runs are the ones that cannot change.

**Oval is deliberately partial.** Only part of the north return is tagged `[oval]`, because that stretch is entirely new work. Elsewhere a run would have to transition spiral → oval → existing rect, and specifying that mid-run is the kind of detail better left to the installer than pinned in a drawing.

**The caveat that comes with standardising on double-wall:** the insulation sits inside the shell, so the airway is smaller than the nominal size. Sizing here is by *airway*, so confirm whether a supplier quotes inner or outer diameter before ordering — getting it backwards costs two inches of diameter on every round run at once.

### When insulation is required

**Supply ducts sweat; returns do not.** A supply carries ~55°F air in cooling, and a basement at 75°F / 50% RH has a dew point right at 55°F — 60°F at 60% RH. So exposed basement supply runs condense *even in conditioned space*. Returns run near 75°F, above any indoor dew point, and never sweat.

| | Treatment |
|---|---|
| Supply, **exposed** (basement feature runs) | **`[dwspiral]`** — insulation inside the shell keeps the outer surface warm |
| Supply, concealed (joist bays, cabinet) | `[rect]` / `[spiral]` with external wrap |
| All returns | plain for *condensation* purposes — but a round return still orders as `[dwspiral]`, since one round part ordered one way beats a second product line for a single run |
| Returns in the knee-wall attic | plain; the blown insulation around them *is* the insulation |

Why names rather than `<property>` elements: properties need `tag.py`, which currently handles only walls and rooms, and furniture already has an editable name. The bracket is self-validating in the same way the assembly tags are — a token without a known keyword is just text.

**Do not** put material in the prose part of the name. The names already carry run identity, destination and sequence, and they are close to unwieldy.

### Registers and grilles are objects, not tags

They carry things a tag on a duct cannot. A register has a **position** — which end of the run, which wall — and `Supply branch for main bed north and basement east` is the case that proves it: one run, two registers, two levels, two rooms. A tag could say "this run has 2" and would leave the contractor guessing which end. Face size and mounting type are per-register too, and the parts list needs something countable.

Modelled with the catalogue's **`frame`** object, under a single `Register:` prefix so they stay countable separately from `Ducting:`. Supply and return are already distinguishable from the destination text, so a second prefix would only invite the two to drift apart:

```
Register: Return from living room
Register: Supply to play room south
```

**Only the position matters, not the precision.** Attachment is resolved by adjacency against the duct runs, so a small frame at the right end of the right run is enough. The living-room return overlaps its branch by 0.1″ — the grille face sitting flush against the duct's end, which is exactly right physically and well inside the 3″ tolerance.

**Face style is tagged the same way as duct material, and defaults the same way.** Bare means a standard louvred grille — the venetian-blind face used everywhere in the house. The exception is tagged:

```
Register: NW ceiling duct supply for future media room [circular]
```

`[circular]` is the round commercial-style diffuser, and it is deliberately confined to **the four basement ceiling registers**, where the runs are exposed double-wall spiral and a round face is what belongs under them. Everywhere else the duct is concealed and a rectangular grille is both cheaper and correct.

**Preposition carries the side:** air returns *from* a room and is supplied *for* one. `Return from kitchen`, `SW supply for kitchen`. This is load-bearing — with a register attached to whichever duct is nearest, a supply face sitting on a return branch is the signal that something is mislabelled or misplaced, and two of them were.

Duct names must not contain the word *register*; it collides with the object prefix.

**The Main Closet has no duct of its own** — its register hangs off `Supply branch for office east`, which is the "tiny split from orphan" the schedule records. At 17 CFM that is the right call; a dedicated run for a closet would cost more in fittings than the air is worth.

### Duct naming, normalised

`<Trunk?> <supply|return> <trunk|branch> for <destination> <n> [material]`

Leading word capitalised, compass trunk designators keep their case (`North`, `SE`, `SW`), every run carries an ordinal even when it is a single object — run membership is derived from *stem plus ordinal*, so a missing ordinal silently makes a run of one. Names must be unique within a run; two objects both called `SE return trunk 2` collapse into one segment for length and parts purposes.

## Task 2 — Compute the real hierarchy from geometry

The audit reads each object in isolation. What is missing is **connectivity**, and it is what the SE riser question turns on.

Approach: two objects are connected when their bounding boxes touch or overlap within a tolerance (the owner notes some only barely touch and some overlap). Build a graph, root it at each plenum, and walk outward. Then each segment's carried CFM is **the sum of the destination CFMs downstream of it** — which is the correct way to size a trunk, and something no amount of per-object inspection can produce.

Deliverables:
- A tree per system, plenum → trunk → branch → register
- Carried CFM at every segment
- **Required** size versus **drawn** size, flagged both ways

**Rotation will break a naive implementation, and the obvious fix is also wrong.** Sweet Home 3D already publishes the rotated bounding box: a piece tilted by `pitch` or `roll` carries `widthInPlan` / `depthInPlan` / `heightInPlan`, and its `elevation` is the bottom of *that* box. Use those three and apply only the yaw (`angle`) to the footprint. Rotating `width`/`depth`/`height` yourself gets the plan position right but the **elevation wrong by tens of inches**, which manufactures broken chains out of runs that are visibly joined on screen. Nineteen of the 74 carry a non-zero pitch or roll — every horizontal cylinder run.

Connectivity has been verified under the corrected reading: **every run joins, nothing dead-ends mid-run.** What remains is the graph walk itself.

### The SE supply riser — settled, and it reduces

It serves **six registers**: three on the second floor (Play Room ×1, Office ×2) and three on the main floor (Kids Room ×1, Main Bed ×2). So it leaves the plenum carrying **519 CFM** and sheds load twice on the way up:

| Segment | Carries | Section | Equiv | fpm |
|---|---:|---|---:|---:|
| Plenum → Main Bed takeoff | **519** | 12×12 | 13.1″ | 519 |
| → Kids Room takeoff | **292** | 8×10 | 9.8″ | 526 |
| → 2nd floor split | **228** | 8×8 | 8.8″ | 513 |

That is the reducing-trunk approach, and it is the right one here — velocity stays near 520 fpm the whole way rather than collapsing as branches leave. **The 12×12 already drawn is correct at the bottom.**

**The step-downs stay in this document rather than in the model.** Splitting one box into three at exact takeoff points is fiddly to draw and adds nothing an installer needs — the schedule above is the instruction, and reducing a trunk as branches leave is ordinary practice they will do by habit. This is the same call as the main-bedroom return note: design intent the docs carry because the schematic cannot say it cleanly.

Keeping velocity up matters more on this riser than anywhere else in the house, because it splits three ways at the top. Damper every takeoff regardless.

**Return riser: 9×9.** It collects the two upstairs returns — Office 113 plus Play Room 168 at the generous sizing, 228 by mass balance — giving 9.84″ equivalent and 357 CFM capacity, running 405 fpm at 228 and 499 at 281, both inside the 400–600 window returns want. 8×8 would be 8.75″ and slightly under. Square is fine because it collects rather than branches.

## Task 3 — Parts list

Derivable from the objects once Task 2 lands. Per run: material, cross-section, total length, and a count of direction changes (inferable from segment-to-segment angle) even though elbows are not modelled.

Report as: schedule of runs, then a materials summary — linear feet by size and material, register and grille counts, damper counts. **Connectors are explicitly out of scope** and the document should say so, since a parts list that silently omits fittings reads as complete when it is not.

## Task 4 — Renders

Sweet Home 3D exports the 3D view to OBJ natively. Worth having: the air handler and plenum area, each trunk system, and the second-floor riser through the utility cabinet. Alternative: photograph the plan view per level with the duct layer visible.

## Task 5 — The site

GitHub Pages from `Cervator/refrhus`, public. Side navigation across the existing documents plus the generated parts list and renders. The existing docs are already written to be read cold, so the work is navigation and presentation, not rewriting.

Suggested order: the scheme primer as the landing page, then the argument against a second unit, the register schedule, the model audit, the parts list, the measurement records, and the renders.

---

## Task 6 — CI: run Eldr on every push, diff the loads on every PR

The idea that completes "PR your house". As-built anchors live on `main` and proposals live on a branch **so the diff is the proposal** — but today that diff is geometric. Running the engine in CI makes it *quantitative*: change a room, and the load change shows up in the pull request.

**On push to `main`:** regenerate the report and publish it to Pages, so the site is never stale relative to the model.

**On a pull request:** run Eldr against both the PR head and `main`, then comment the difference. `--json` already emits the whole analysis as structured data, so the diff is a dict comparison rather than text scraping:

```
## Eldr — load change vs main

| Component  |   main |     PR |    Δ |
|------------|-------:|-------:|-----:|
| ceiling    |  1,555 |  2,340 | +785 |
| **total**  | 39,439 | 40,224 | +785 |

Design airflow 1,217 → 1,241 CFM · Manual S 3.3 → 3.4 tons (recommendation unchanged)
```

**Eldr's warnings become CI checks**, which may be the more valuable half. A pull request that draws a room badly and introduces a new schematic gap, an unbound `spaces:` key or a borrowed U-value would surface it in the comment instead of being discovered three sessions later. That is regression testing for a house.

Practicalities:

- **The engine is a separate public repo**, so CI checks out `SiliconSaga/eldr` alongside this one. No secrets involved.
- **Eldr has no packaging metadata** — a known limitation from the level-stack work. CI checks it out and sets `PYTHONPATH` rather than pip-installing. Worth fixing eventually; not a blocker.
- **Runs against `sh3d-internals/Home.xml` directly**, which is the tracked artefact. The packed `.sh3d` is gitignored and irrelevant to CI.
- Dependencies are only `pyyaml` and `defusedxml`.

## What to fix before handover

**Done:** material tags are in and `tools/partslist.py` consumes them; registers and grilles are modelled as `Register:` objects with faces; the parts list, cost bands and whole-job estimate are generated from the model.

**Deliberately not done:** the SE riser step-downs stay in the schedule rather than the model — splitting one box into three at exact takeoff points is fiddly to draw and adds nothing an installer needs, since reducing a trunk as branches leave is ordinary practice.

**Still open, and all three are the owner's call rather than modelling work:**

1. **The kitchen SE supply's 4″ of cabinet height.** The model now draws 4x15 at 403 fpm, but getting the height still means moving one cabinet over or modifying it — a construction decision the drawing has run ahead of.
2. **Where the main-floor return stops being buried.** The model now splits it there, so the split point is load-bearing: it decides how much duct can be enlarged. Worth a site visit before anything is priced.
3. **The main bedroom's own return**, which the split does not solve. The buried 4x8 passes roughly 91 CFM against a 227 CFM design, and the remedy is a transfer path rather than a duct.

## What to be upfront about in the package

**Total effective length is not derivable from this model.** No elbows, tees or takeoffs are drawn, and Eldr's Manual D uses a flat 1.5× fitting factor rather than true equivalent lengths. Real fittings on a three-storey run add 50–150 ft of equivalent length.

This matters more than any other caveat, because **the second-unit argument will be decided on static pressure**. Going in with an acknowledged gap is far stronger than being caught with an optimistic number — and it invites the contractor to supply the fitting counts, which is work they are better placed to do anyway.

Two other honest notes already written into the documents and worth keeping visible: the second-floor loads are deliberately conservative (ceiling area modelled at 984 ft² against the professionals' 1,547), and the biases applied to the airflow are stated rather than buried.
