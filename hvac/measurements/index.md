# Surface-temperature measurements

A protocol for readings that stay comparable across days, seasons and instruments. The goal is not one accurate number; it is a **series** — the same spots, repeatedly, with enough context recorded that a reading from February can be compared against one from August.

Raw readings live in [`wall-temperatures.csv`](wall-temperatures.csv). Nothing here is derived or computed — store what you observed, derive later. A reading you can't reconstruct the conditions for is nearly worthless, so the conditions columns are not optional.

## Why bother

Eldr's `basement_wall` U-value is currently a guess (0.07) that nobody has measured, and it is the single largest remaining disagreement with the professional Manual J — see [the load comparison](../index.md). Interior surface temperature measures it directly, because the interior air film is a known resistance:

```
q      = (T_air − T_surface) / R_film        BTU/hr·ft²      R_film ≈ 0.68 for still air, vertical
U_eff  = q / (T_indoor − T_outdoor)          BTU/hr·ft²·°F
```

Take that on the **bare cinder block** and on the **R-11 panelled** section and you have measured the two assemblies in dispute — the professionals' 0.293 and 0.088 against our 0.07 — with no argument about convention.

## Take winter readings

**Summer readings cannot give you the heating U.** The far-side boundary in summer is deep soil at an unknown temperature grading to outdoor air near the surface; without knowing it, flux is all you get. In winter the driving ΔT is large, the indoor side is held steady by the heating system, and the outdoor temperature is knowable — so `U_eff` falls out.

Summer readings are still worth taking: they show the below-grade wall behaving as a heat *sink*, which is what justifies Eldr reporting zero below-grade cooling load. Just don't expect a U from them.

The gradient reverses between seasons, which is the check that the readings are real:

| | Coldest | Warmest | Why |
|---|---|---|---|
| **Winter** | near grade | at the slab | deep soil is *warmer* than outdoor air |
| **Summer** | at the slab | near grade | deep soil is *colder* than outdoor air |

## Point naming

`<AREA>-<WALL>-<CONSTRUCTION>-H<inches>`

- **AREA** — `BSMT`, `CRAWL`, `MAIN`, …
- **WALL** — `N` `S` `E` `W`, matching the model's compass (`northDirection` ≈ 318°, set from the survey — plan-north is not true north)
- **CONSTRUCTION** — `BARE` (8" cinder/stone, unfinished), `R11` (wood-framed, finished), `SLAB`, `RIM`
- **H** — height in **inches above the slab**, the one datum that doesn't move

So `BSMT-N-BARE-H12` is the north basement wall, bare block, one foot up. Use the same heights every time; 12 / 24 / 36 / 48 / 60 / 72 / 84 is a good ladder and lands on the joist bottoms at the top.

**Mark the spots physically.** A dot of paint pen or a strip of tape with the point ID, so the January reading is the same square inch as the August one. This is the difference between a series and a pile of numbers.

## What to record every time

Everything in the CSV header, and these matter more than instrument precision:

- **`air_f`** — air temperature 2–3 ft off the wall **at the same height as the surface probe**. **The single most important companion reading**; every flux calculation is `air_f − surface_f`, so a missing air temperature makes the row unusable.

  **One air reading is not enough.** Basements stratify — warm air rises, and the difference between ankle height and joist height can be several degrees, which is the same order as the film ΔT being measured. A single air temperature taken at chest height will overstate flux at the slab and understate it near the ceiling, in a pattern that looks exactly like a depth-dependent U-value. That is a fake gradient, and it would be easy to believe. Pair air probes with the surface ladder at the same heights, or at minimum at low / mid / high.
- **`outdoor_f`** — at the same moment, not from a forecast.
- **`outdoor_24h_avg_f`** — approximate. Below-grade walls lag by days, so the instantaneous outdoor temperature is the wrong driver for them; the trailing average is closer. Leave blank if unknown.
- **`method`** — `IR` or `contact`. They disagree by a degree or two and you want to know which was which.
- **`steady`** — `y` only if indoor temperature has been stable for several hours, no sun on that wall, nothing blowing across it. An unsteady reading is not wrong, but it should be flagged.

## Where to put a permanent strip

Match everything except the variable under test. The strips are there to isolate **construction** — bare cinder against R-11 finished — so grade depth, orientation and soil conditions should be as close to identical as the house allows. Two strips in opposite corners answer one question with three confounders attached.

The professionals' construction page gives the matching target: bare sections at **3 ft and 4 ft** average depth, R-11 sections at **3 ft**. The clean pairing is therefore **bare-at-3ft against R-11-at-3ft** — same soil path, only the assembly differs.

- **Prefer the true-north side.** The top of each strip covers the above-grade band, where solar gain contaminates readings. A south or west wall bakes in the afternoon and the upper probes end up measuring sunshine.
- **`northDirection` is ~318°, so plan-north is not true north** — the front of this house faces roughly southwest. Name points by *true* compass direction and let the model resolve which wall that is, or a sunny wall gets labelled `N` and nobody understands the drift.
- **Avoid:** below a downspout or in a low spot (wet soil conducts far better — that measures soil, not wall); garage- or crawlspace-adjacent walls (those face buffer space, not soil); within a few feet of a supply register or the stairs (air movement destroys the still-air film assumption); and anywhere storage will end up stacked.

A later refinement, once the first pair is trusted: a third strip on a **4 ft** bare section gives a second depth and starts to describe the depth-dependence directly rather than inferring it from one wall's vertical profile.

## Conditions that matter more than the instrument

- **Steady state beats precision.** A cheap IR thermometer on a stable day beats a good one an hour after the heat kicked on.
- **No sun on the wall**, and nothing blowing across it. A supply register washing the wall destroys the film assumption the whole method rests on.
- **Emissivity ~0.9** covers cinder block and painted wood. Bare metal or foil-faced insulation will read badly with IR — use contact there.
- **The film resistance is the weak link.** R-0.68 is the standard still-air figure; real air movement shifts it. Treat derived U-values as **±10%** — ample to separate 0.07 from 0.29, which are 4× apart, but not enough to argue about the third decimal.

## Reading the series

With a winter row in hand:

```
q     = (air_f − surface_f) / 0.68
U_eff = q / (air_f − outdoor_24h_avg_f)
```

Compare `U_eff` on the `BARE` points against the professionals' 0.293 and on the `R11` points against their 0.088. Then set `assemblies.basement_wall` in `../../eldr-sidecar.yaml` — area-weighted if the two constructions cover meaningfully different areas — and note in the side-car that it came from measurement rather than estimate.

The vertical profile is the more interesting output. Plot `U_eff` against height and you have this house's own version of the depth-dependent below-grade U that Manual J tabulates — which is also the data any future grade-line support in Eldr would calibrate against.

## What the readings so far show

The 2026-08-14 session settled a modelling question that had been open. Bottom of joists measured **84 in** above the slab; bottom of subfloor **92 in**. So the basement's *clear* height is 7.00 ft and its floor-to-floor height is about 7.7 ft — and the model carries both: the Basement level height is 7.00 ft (correct for air volume) while its walls are drawn 8.00 ft (correct in kind for conduction area, over by ~3 in). Both numbers are right for their own purpose; this is not the error it looked like.

Structural detail belongs in [`../../basement-structure.md`](../../basement-structure.md) — this note only records what it resolved for the load model.
