---
title: Overview
---

# Refr Hus — HVAC design package

A 1950s Cape Cod in West Orange, NJ, drawn to measured dimensions in [Sweet Home 3D](https://www.sweethome3d.com/) and used to work out the heating and cooling loads a duct design can be sized against.

The schematic is not a sketch. Every exterior dimension is measured — joist by joist in the basement, the chimney on all three floors, the posts to the eighth of an inch — and cross-registered so the levels stack. Room volumes, wall areas, window orientations and duct runs are read straight out of that geometry rather than estimated from floor area.

[**Eldr**](https://github.com/SiliconSaga/eldr) is an open-source engine written for this house: it reads the Sweet Home 3D file and computes the ACCA chain from it directly, aiming at numbers that could stand up to certification rather than at a rule of thumb. It reports its own assumptions — which U-values were borrowed, which floor area sits over a space not yet drawn — so the gaps stay visible instead of being buried in a total.

What it computes:

| | |
|---|---|
| **Manual J** | Heating and cooling loads — whole-house and per room, with solar gain resolved per window bearing |
| **Manual S** | Equipment sizing against those loads |
| **Manual D** | Duct sizing by equal friction |
| **Manual T** | Not done. Register throw, spread and drop need a manufacturer's catalogue — see [known drawbacks](#known-drawbacks) |

This is a working record of one house, not a document written for a single job. Some of it would be useful to hand an HVAC contractor asked to estimate work; the rest is here because the house keeps having projects and the measurements outlast any one of them. Every figure is open to challenge, and the reasoning behind each is in the linked pages.

**The contents is grouped by what each part is about:**

| | |
|---|---|
| **The proposal** | What changing the ductwork would involve, and what it would cost — the [scheme](ducting-scheme.md), the [register schedule](ducting-register-schedule.md), the [parts list](ducting-parts-list.md) |
| **Calculations** | Where the numbers come from and how far they can be trusted — [ours against the professionals'](hvac/index.md), [their Manual J](hvac/professional-manual-j.md), [the current run](hvac/eldr-report.md) |
| **The house as measured** | The building itself: what was measured, how, and what it turned out to be |
| **Appendix** | Method and tooling — how the schematic is read, how this site is built, what is still unmeasured |

An HVAC company probably wants **The proposal** and little else. The **Calculations** are there for anyone who would rather check the numbers than take them.

## Load and equipment

| | |
|---|---:|
| Heating load, 70°F / 14°F design | **40,331 BTU/hr** |
| Cooling load, 75°F / 91°F design | **23,125 BTU/hr** (18,228 sensible) |
| Sensible heat ratio | 0.79 |
| Design supply airflow | **1,245 CFM** |
| Manual S on the current model | 3.4 tons |
| **Size to quote** | **4.0 tons** |
| Existing unit | 4.0 tons |
| Duct, straight runs | 344 ft across 29 live runs |
| Registers and grilles | 25 |
| Whole job, pre-incentive | **$12,200–29,200** |

Design temperatures come from the Newark, NJ station.

**Airflow assumes a 30°F supply-air rise**, which is the heat-pump figure. A 50°F rise is a gas furnace and undersizes every heating-driven duct by 1.67×.

## Where these numbers come from

Two independent load calculations sit behind this package.

**A professional Manual J**, commissioned in August 2026 from an ACCA-certified energy auditor. It covers the house in three progressions — as-is, plus insulation, plus air sealing — so each one shows what the equipment could shrink to if the preceding envelope work is done. The as-is progression gives **54,260 BTU/hr heating**. It also includes a blower-door test and a construction-details page listing every assembly with its measured area and U-value.

**Our own model**, built in Sweet Home 3D from hand measurements and run through [Eldr](https://github.com/SiliconSaga/eldr), an open-source Manual J engine. It gives **40,331 BTU/hr**, or 74% of the professional figure.

The two are not competing estimates. **The measured inputs come from the professional report** — wall, window, ceiling and slab U-values are taken from its construction page, and the infiltration rate is its blower-door result of 3,751 CFM50. What our model adds is geometry: per-room loads and per-register airflow, which a whole-house figure cannot give and which duct sizing needs.

Where the two still differ is documented line by line in [the calculations](hvac/index.md). In the same units throughout: ours is **40,331 BTU/hr — 3.4 tons**, theirs **54,260 — 4.5 tons**, a gap of about **1.2 tons**. It is concentrated in two known omissions, and both understate our number:

- **No grade line.** Eldr classes each basement wall as below-grade over its full height, where the professionals split it at grade and use a lower U-value on the buried part. Adopting their measured value takes ours to roughly **45,600 BTU/hr — 3.8 tons**.
- **The second-floor roof is not drawn.** The knee-wall attic and sloped ceilings are missing, so the schematic covers 984 ft² of ceiling against their 1,547. That surface sits under an attic our own model puts at about 133°F on a summer design day, so drawing it matters more than the area alone suggests — indicatively another **3,500 BTU/hr**, taking ours to roughly **4.1 tons**.

**Which is why 4.0 tons is the size to quote rather than 3.5.** Manual S on the schematic as it stands says 3.4, but that is a floor: correcting both known omissions walks it up past 4.0, and the professional report brackets it from above at 4.5.

**Estimated pricing is pre-incentive.** No rebate, credit or utility programme is netted off anywhere, so the figures compare against a quote line for line.

## Major proposal options

**One air handler**, moved to the basement — tucked under the stairs, in what used to be the bar area — with trunks running out to each part of the house.

The feature that makes it work is a **stacked utility cabinet built alongside the chimney**, carrying supply and return from the basement up through the main floor to the second. Getting conditioned air upstairs is the usual difficulty with a Cape Cod, and it is why the alternative below reaches for a second unit in the attic. A cabinet inside the heated envelope solves the same problem without putting equipment or ductwork in an unconditioned space. This is the design documented here.

**Two air handlers**, the second in the north knee-wall attic, reached through the wall at the top of the stairs. Proposed by the contractor.

| | One unit | Two units |
|---|---|---|
| Per-floor zoning | Damper throttling only | Real, independent |
| Second-floor duct location | Conditioned chase | Unconditioned attic |
| Equipment, filters, condensate paths | One | Two |
| Reaches the south side of the upstairs rooms | Yes | No — see below |

Two handlers buy genuine per-floor zoning, which a single unit cannot provide here: neither the basement nor the second floor alone can be a hard zone without starving the blower.

Against that, the proposed location has two costs. Attic air reaches an estimated 133°F on a summer design day, and the unit, its coil and its supply ducts would sit in it. And a north knee-wall unit does not reach the south side of the upstairs rooms, which carry real load. The suggested remedy — a duct channel along the office wall into the small east attic — is itself a chase, and the single-unit design is built around one that stays inside the envelope and serves all three floors.

**The deciding question is static pressure**, and answering it needs fitting counts the schematic does not carry yet. Those counts are a contractor's to produce, and they settle the question either way.

## Known drawbacks

**Total effective length is not derivable from this model.** No elbows, tees or takeoffs are drawn, and duct sizing uses a flat fitting factor rather than true equivalent lengths. Real fittings on a three-storey run add 50–150 ft of equivalent length. Since the one-unit-versus-two question turns on static pressure, this is the most consequential gap in the package.

**The main bedroom's return is undersized.** Its duct runs through an inaccessible crawlspace and passes roughly 91 CFM against a 227 CFM design. The rest of that run has been split off and enlarged, so the Kids Room and Utility Room are no longer behind the same pinch, but the bedroom still is. Worth verifying on site before pricing a remedy.

**The kitchen SE supply needs cabinet work.** It is drawn at 4x15, which runs a comfortable 403 fpm, but the 4″ of height that requires means moving one cabinet over or modifying it. The drawing records the decision; the carpentry has not happened.

**Some loads are deliberately biased.** Second-floor airflow is multiplied by 1.35 and the basement by 0.70, because the second floor runs hot and the basement holds temperature unconditioned. The second floor's ceiling area is modelled at 984 ft² against a professional report's 1,547, which makes the second-floor figures conservative.

**Our own load figures are not ACCA-certified.** The professional Manual J referenced above is; this model is not, and is offered as the per-room detail that report does not carry rather than as a replacement for it.
