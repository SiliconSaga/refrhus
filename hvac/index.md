# HVAC — load calculations, professional and our own

Two independent Manual J estimates of this house, kept side by side so they can be compared. [Eldr](https://github.com/SiliconSaga/eldr) is our own engine: it reads `../sh3d-internals/Home.xml` for geometry and `../eldr-sidecar.yaml` for the thermal assumptions geometry cannot hold.

The design intent and duct scheme live one level up in [`../ducting-scheme.md`](../ducting-scheme.md). This directory is only load calculations and their inputs.

## One current run, not an archive

[`eldr-report.md`](eldr-report.md) is **generated** — the engine's output against the current model, overwritten on every regeneration. Do not edit it.

This replaces a folder of dated runs, and the reasoning is worth keeping because it was a real trade. **Totals lie by cancellation.** Between two early runs the whole-house heating figure moved 0.7% while four components underneath it moved by thousands in opposite directions — basement walls and floor up by nearly 4,000 between them, infiltration down by 3,300. Anyone comparing bottom lines alone would have concluded nothing changed. That was the argument for archiving every run, and it was sound.

What retired it is a **better answer to the same problem**. The archive compared *documents*, which only works while the documents describe the same house — and these did not. Each was produced by a different iteration of the schematic, so a difference between two of them mixed real thermal change with the schematic catching up to the building. Comparing them rewarded careful reading and still misled.

The replacement compares *runs against the same model at a known commit*: regenerate on push, diff component-by-component in the pull request, and the cancellation problem is solved by the diff rather than by the reader's diligence. Component drift becomes visible automatically instead of being available to whoever thinks to look.

**Archive again if that ever stops being true.** The practice was not wrong; it was the best available answer before the model was trustworthy enough for a diff to mean anything.

## The professional reports

An ACCA-approved Manual J by NJ Energy Auditor, commissioned 2026-08, in three progressions modelling the house at increasing tightness: **as-is 54,260**, plus insulation 44,067, plus air sealing 40,901 BTU/hr heating.

**[The figures are summarised on their own page](professional-manual-j.md)** — design conditions, every construction assembly with its area and U-value, and the infiltration measurement. That summary is the source of the area-weighted U-values this project's side-car carries.

**The reports themselves are not published.** They were produced for the owner as a customer rather than for redistribution, so this site carries the numbers our work depends on and not the documents.

Two readings in those reports are easy to get wrong and both are set out on [the summary page](professional-manual-j.md): the measured blower door exists only as a handwritten margin note (**3,751 CFM50 → ACH 0.68**, not the printed figure), and below-grade surfaces are loaded at the full outdoor ΔT with the soil path inside the U-value — which is what corrected Eldr from discounting twice.

## Our runs

[`eldr-report.md`](eldr-report.md) — the current run. Regenerate after any change to the model or the side-car.

**How the number got here**, kept as a changelog because each step was a correction rather than because the documents behind them were worth keeping:

- **The level stack** replaced ceilings and floors derived from level *bounding boxes* with resolved surfaces, per-space buffer policies, hot-attic cooling and measured ACH.
- **Measured assemblies** adopted the professionals' ceiling and crawl-floor U-values and the crawlspace's observed winter temperature: heating 31,757 → **37,962**.
- **Cooling gained its missing sensible infiltration term** — it had only latent. Cooling 17,571 → **20,794**, airflow 610 → **759 CFM**, and duct sizes moved with it.
- **The assembly true-up** took the professionals' measured wall, window and slab U-values, area-weighted off their Construction Details page, and corrected occupants 3 → 5. Heating → **42,097**.
- **The basement measurement work** then brought it down to **39,694** on geometry that is finally measured rather than estimated.
- **Site coordinates** replaced Sweet Home 3D's factory default — which sat in lower Manhattan and had never been set — with West Orange's town centroid. The design station moves New York → **Newark, NJ** and the 99% design temperature 15°F → 14°F, taking heating to the current **40,331**.

The one verdict to watch across that sequence: the existing 4-ton unit has read as oversized, then well-matched, then oversized again. **A sizing verdict that flips with each correction is a sizing verdict to hold loosely** — which is the argument for rounding up rather than shaving down.

Regenerate with the engine checked out beside this repo:

```bash
PYTHONPATH=components/eldr components/eldr/.venv/bin/python -m eldr.cli \
  hoards/refrhus/sh3d-internals/Home.xml hoards/refrhus/eldr-sidecar.yaml

# the narrative version, for handing to someone else — generate on demand, don't commit
PYTHONPATH=components/eldr components/eldr/.venv/bin/python -m eldr.cli \
  hoards/refrhus/sh3d-internals/Home.xml hoards/refrhus/eldr-sidecar.yaml --overview
```

**The overview is not committed.** `--overview` wraps the same report body in about seventy lines of framing prose that barely changes between runs, so committing it would duplicate every number while adding nothing.

`--json` gives structured output; `--walls` lists wall ids for tagging.

## Where the two still disagree, and why

Same house, two engines, and the gaps are now nameable rather than mysterious:

Currently heating **40,331** against their **54,260**, or 74%. That ratio *fell* after the basement measurement work, which looks like regression and is not: the measured basement is smaller and better sealed than the estimate it replaced, so the remaining gap is now concentrated in things that can be named — the grade line and the undrawn second-floor roof surfaces — rather than spread thinly across assumptions nobody had checked.

| Line | Eldr | Theirs | Status |
|---|---:|---:|---|
| Floor **area** | 971.9 ft² | 978 ft² | ✅ within 0.6% |
| Above-grade walls | 10,950 | 10,432 | ✅ settled. `exterior_wall: 0.123` is their three non-garage rows area-weighted; we now run 5% *over* |
| Windows | 4,730 | 5,554 | ✅ largely settled. `window: 0.588` is their ten rows area-weighted over 152.5 ft²; area was already within 4%. The residual is the *distribution* — a blend cannot put the four single-pane units in the rooms that have them |
| Crawl floor load | 5,765 | ~7,800 | U matches (0.521). We apply the crawlspace's **observed** 32 °F (factor 0.69); they model it as *exposed to outdoor air* (factor 1.0, which would give 8,290). **A deliberate difference, not an error** — see the side-car note |
| Slab | 746 | 807 | ✅ resolved. `floor` corrected 0.05 → their measured **0.020** on 713.9 ft²; we had been overshooting 2.5× |
| Ceilings | 1,550 | 5,008 | U matches. **One cause left, and it is geometry:** their ceiling area is 1,547 ft² against our 984 — sloped and knee-wall surfaces on the incomplete 2nd floor. See the attic note below; the unvented attic is *not* an error |
| Below-grade walls | 4,370 | 9,271 | Convention matches since the below-grade fix. `basement_wall: 0.07` is **deliberately not updated**; see below |
| Basement wall **area** | ~1,135 ft² | 774 ft² | They split each wall at the grade line; Eldr has no grade-line concept and classes the whole wall below-grade |
| Doors | 2,908 | 2,233 | We are **over**, and it is area not U: ~132 ft² of door against their 82.3 (38.9 opaque + 43.4 glass). Interior doors are being counted; a schematic fix, not a side-car one |
| Occupants | 5 | 5 | ✅ reconciled. The actual headcount, and the ACCA bedrooms+1 convention, agree |
| SHR | 0.80 | 0.90 | Our assumed 30-grain humidity difference vs their station's 27.805 |

**The attic divergence is deliberate and ours to keep**, and is not an Eldr error. The attic is unvented, and Eldr models the seasonal asymmetry correctly: a winter factor of **0.50** from the `vented: false` shorthand, and a summer factor of **3.66** resolved from a sol-air attic temperature. Being unvented *helps* in winter — stale air does not track outdoor temperature — and *hurts* in summer, when superheated air has nowhere to go. Declaring the attic vented to match their treatment would make the schematic less true to the house in order to close a number, which is backwards. The whole remaining ceiling gap is the 563 ft² of area we have not drawn.

**Why `basement_wall` was left at 0.07.** Their area-weighted below-grade U is 0.196 (bare 8" stone at 0.293/0.297, finished R-11 at 0.088). Applying that to *our* area gives **12,236 BTU/hr against their 9,271** — a 32% overshoot replacing today's 53% undershoot, because our area is 47% too large for want of a grade line. Substituting one error for another is not accuracy. This one waits for the grade-line split or for measured wall temperatures.

**Cooling infiltration was latent-only for a while**, with no sensible term, which is part of why our SHR read low. Fixed: cooling gained the missing sensible term and the SHR moved 0.70 → 0.80.

The pattern overall: **the geometry agrees, and the assemblies are now mostly settled.** Above-grade walls, windows, the slab and occupants are all reconciled against their measured values. What is left is three items, and only one of them is thermal:

1. **The grade line** (4,901 BTU/hr) — structural. Eldr classes a whole basement wall as below-grade; they split it at grade. Blocks setting `basement_wall` honestly.
2. **The 2nd-floor ceiling area** (3,458) — geometry. 984 ft² drawn against their 1,547; the knee-wall and sloped surfaces are not modelled.
3. **The phantom doors** (−675, we are over) — geometry. Interior doors counted as envelope doors.

Plus one deliberate divergence we intend to keep: the crawlspace's observed 32 °F, and the unvented attic.

## The measurement that would settle the most

Interior surface temperature gives heat flux directly, because the interior air film is a known resistance:

```
q = (T_air − T_surface) / 0.68        BTU/hr·ft²
U_eff = q / (T_indoor − T_outdoor)
```

Taken on the **bare cinder block** and on the **R-11 panelled** section, that measures the two assemblies currently in dispute — their 0.293 and 0.088 against our 0.07 — without arguing about convention.

Take a **vertical profile, not a single reading**: below grade the soil path lengthens with depth, so the wall runs coldest near the grade line and warmest at the slab. That gradient *is* the depth-dependent U that Manual J tabulates, measured on this house instead of read from a table. Every foot from slab to ceiling, on both wall types, and the slab too.

Conditions matter more than instrument quality — a cold stable day, indoor temperature held for several hours, no sun on the wall, nothing blowing across it. Measure air temperature 2–3 ft off the wall and log the outdoor temperature at the same moment. An IR thermometer is fine on block and painted wood (emissivity ~0.9); a taped-on thermistor under a scrap of insulation is better. The weak link is that 0.68 film resistance, so treat results as ±10% — ample to separate 0.07 from 0.29.
