# The duct scheme

**One air handler in the basement — tucked under the stairs, in what used to be the bar area — feeding all three floors, with the second floor reached through a three-level chase built alongside the chimney.**

The main floor is served by basement runs — south through the under-stair space, north through the basement bathroom and then west along the girder. The second floor takes one supply and one return riser up the chase: the supply branches short and central, the return splits in the knee-wall attic to reach the far corners of both rooms.

| | |
|---|---:|
| Design airflow (Eldr, equipment basis) | 1,245 CFM |
| Plenums | 12x20 supply and return |
| Largest trunk | 12x16 |
| Straight duct | 344 ft across 29 runs |
| Registers and grilles | 15 supply, 8 return |
| Faces outside the velocity band | None |
| Worst constraint | Main bed return, 227 CFM design against a buried duct good for ~91 |

Two contractors have instead proposed a second air handler in the knee-wall attic. That option is compared against this one [below](#one-air-handler-or-two).

Related: [the register schedule](ducting-register-schedule.md) for per-register sizes, [the parts list](ducting-parts-list.md) for materials and cost, [the load calculations](hvac/index.md) for where our numbers and the professional Manual J differ, and [the chimney measurements](chimney-measure-sheet.md) for the geometry the chase is built against.

---

## The governing principle

Everything below follows from one rule, which decides every routing question that comes up:

> **Supplies stay inside the thermal envelope. Returns may cross buffer spaces.**

The reason is asymmetric cost. Air leaving the coil at 55°F and arriving at a register at 62°F has lost delivered capacity *and* the room feels it. Air leaving a room at 75°F and reaching the unit at 80°F only makes the unit work a little harder — the register still delivers 55°F. Losses on the supply side cost comfort and capacity; losses on the return side cost efficiency alone.

So where a duct has to cross a crawlspace, an attic, or any unconditioned run, it should be the return. That single rule is what makes the knee-wall attic acceptable for returns, the crawlspace acceptable for the kitchen return, and neither acceptable for supply.

**One caveat that comes with it:** a return leak is worse than a supply leak. A leaking supply wastes conditioned air outward; a leaking *return* pulls attic or crawlspace air inward — hot, humid, dusty, and capable of depressurising the house. Returns crossing buffer space get sealed with mastic, not tape.

---

## What each floor needs

Design airflow from Eldr's per-room Manual J, on geometry that is deliberately conservative (see the caveat below):

| Level | CFM | Dominated by |
|---|---:|---|
| Basement | 256 | Future Media 124, Utility 118 |
| **Main** | **751** | Kitchen 254, Main Bed 225, Living room 134 |
| 2nd floor | 238 | Office 100, Play Room 86 |
| **Total** | **1,245** | |

> **Two airflow totals appear across these documents and they are not interchangeable.** **1,245 CFM** is the whole-house design airflow Eldr computes, and the per-room figures now sum to the same number — the figure the *equipment* is sized on. **1,201** is the [register schedule](ducting-register-schedule.md)'s twelve rooms summed after the second-floor ×1.35 and basement ×0.70 biases. The 44 CFM between them is closets, chases and voids that fall below the threshold for a duct of their own — not staleness. **The schedule is authoritative for duct sizes; Eldr's total is authoritative for equipment.**

**The main floor is the load** — two and a half times the second floor. That reframes the problem: the second floor is not the hard part *volumetrically*, it is the hard part *geometrically*. The distinction is worth holding onto when weighing the two proposals, because a second air handler adds capacity where the difficulty is access.

**These numbers understate the second floor and should be presented that way.** Our ceiling area on that level is 984 ft² against the professional Manual J's 1,547 — the sloped roof and knee-wall surfaces are not fully modelled yet. It cuts both ways: it makes *"the south side needs real supply"* stronger than shown, and *"one unit can do it"* easier than reality. Quote them as a floor, not an estimate: *on geometry that understates our second-floor ceiling by a third, the office still needs 100 CFM.* A number biased against your own case is much harder to argue with.

---

## Per-room duct sizing

Airflow deliberately biased before sizing, on the owner's read of how the house behaves rather than what the model computes:

- **Second floor ×1.35.** Its ceiling is modelled at 984 ft² whole-house against the professionals' 1,547, its knee walls are not drawn at all, and it is observed to run hot. The uplift sits between the moderate correction (~×1.15) and the worst case (~×1.40).
- **Basement ×0.70.** Largely below grade, thermally massive, and observed to hold temperature with no conditioning at all. Its design-day peak overstates the airflow it needs.
- **Main floor unchanged.**

Rooms under 10 CFM get no dedicated run — door undercut or a transfer grille instead.

| Level | Room | Raw | Biased | Exact | Duct | fpm |
|---|---|---:|---:|---:|---|---:|
| Basement | Future Media Room | 124 | 87 | 5.8″ | 6″ | 443 |
| Basement | Utility Room | 118 | 82 | 5.6″ | 6″ | 420 |
| Main | Main Bed | 225 | 225 | 8.3″ | 9″ | 510 |
| Main | Kitchen | 254 | 254 | 8.7″ | 9″ | 576 |
| Main | Living room | 134 | 134 | 6.8″ | 7″ | 502 |
| Main | Kids Room | 65 | 65 | 5.2″ | 6″ | 329 |
| Main | Main Bath | 36 | 36 | 4.2″ | 5″ | 268 |
| Main | Main Closet | 17 | 17 | 3.1″ | 4″ | 191 |
| 2nd | Office | 100 | 134 | 6.8″ | 7″ | 503 |
| 2nd | Play Room | 86 | 117 | 6.4″ | 7″ | 436 |
| 2nd | Upper Bath | 21 | 28 | 3.7″ | 4″ | 320 |
| 2nd | Upstairs Hallway | 17 | 22 | 3.4″ | 4″ | 255 |

Velocities run 191–576 fpm — inside the 500–750 supply band at the top end and comfortably under it elsewhere.

> **The register schedule was re-derived against these same loads on 2026-09-18.** It tracks them to 2% overall; the Office was the one room to move materially (113 → 134 CFM, taking its supplies from 5″ to 6″). It remains authoritative for what gets installed.

| | CFM | Round | Rectangular |
|---|---:|---|---|
| Basement branch | 169 | 8″ | 4×14 |
| Main branch | 731 | 14″ | 8×20 |
| 2nd floor riser | **301** | **10″** | **5×16** |
| Trunk at the unit | **1,202** | **16″** | **10×22** |

**The riser moves 9″ → 10″** on the re-derived figures — 301 biased CFM against the 276 the schedule was built on. That is the one sizing change here large enough to matter, and it lands on the duct this whole scheme turns on.

**The biases nearly cancel at the trunk**, so the largest single piece of ductwork is insensitive to how those judgement calls land. And **the 16″ never has to exist** — if the plenum carries four takeoffs directly rather than one duct splitting later, the largest duct in the house becomes a 10″. See the trunk section of the [register schedule](ducting-register-schedule.md), which is where that decision lives.

**But the uplift changes the old ducts' role.** At design friction a 3×10 carries **86 CFM**, against a re-derived biased Office at 134 and Play Room at 117. Together the two old ducts cover 172 of 251 — **69%** — so they remain a substantial contribution rather than the base, and the riser should be planned to carry the shortfall rather than leaning on them running hard. A 3×10 pushed to the Office's full 134 CFM reaches **643 fpm**: audible, and bought with pressure drop.

Sizes are computed with Eldr's own `ductd` equal-friction math at 0.08 in.wc/100 ft; rectangular equivalents use the ASHRAE relation `De = 1.30·(ab)^0.625 / (a+b)^0.25`.

| Size | Area | Equiv round | CFM @ 0.08 |
|---|---:|---:|---:|
| 3×10 | 30 in² | 5.74″ | 86 |
| 4×10 | 40 | 6.74″ | 131 |
| 4×14 | 56 | 7.81″ | 194 |
| 6×10 | 60 | 8.40″ | 235 |
| 8×8 | 64 | 8.75″ | 261 |
| 9×9 | 81 | 9.84″ | 357 |
| 6×14 | 84 | 9.80″ | 353 |
| 8×12 | 96 | 10.66″ | 441 |
| 8×16 | 128 | 12.19″ | 628 |
| 8×24 | 192 | 14.61″ | 1015 |

## The three-level chase

The chase is the whole argument in physical form. The standard, correct objection to retrofit second-floor ducting is that ducts in an unconditioned knee-wall attic lose 20–30%. A chase running basement → main → second floor keeps them inside the thermal envelope, which dissolves the objection rather than arguing with it.

**It is not the same construction on every level.** The basement and main floor take a full built-in cabinet. The second floor has room for one, but the current thinking is a smaller enclosure holding ducts only — or none at all, with the risers leaning diagonally through the main floor so they emerge on the far side of the knee wall. "Chase" is the accurate word throughout; "cabinet" only describes the lower two levels.

It carries **only the second floor**, not the whole 1,245 — the main floor is fed from basement runs and never enters the chase. That is what keeps a chase this modest sufficient.

**Two figures, two scopes — and they are not one multiplication apart.**

- **238 CFM** is Eldr's current unbiased second-floor total, aggregated across every room on the level.
- **276 CFM** is the sum of the [register schedule](ducting-register-schedule.md)'s four second-floor rows — Play Room 115, Office 113, Upper Bath 28, Upstairs Hallway 20 — each biased at *room* level against an earlier model state, with the Play Room row since revised upward to carry the whole room rather than half of it.

**The schedule is authoritative for what gets installed, so the riser as specified is 276 at 9″.** Two fresh figures both sit above it:

| Basis | CFM | Exact | At 9″ |
|---|---:|---:|---:|
| Register schedule, as built to | 276 | 8.93″ | 625 fpm |
| Four second-floor rooms, biased individually today | **301** | 9.23″ | 681 fpm |
| Level total × 1.35 (238 → 321), closets included | **321** | 9.45″ | 727 fpm |

**A 9″ round carries about 276 CFM at design friction**, so the riser is sized exactly at its own design figure with no headroom. (A *9×9 rectangular* duct is a different thing — 9.84″ equivalent round, 357 CFM — and the two are easy to confuse.)

That leaves no margin, but it does not overturn the design. At 301 the 9″ runs 681 fpm and at 321 it runs 727, both inside the 500–750 supply band and both at the top of it. Equal-friction sizing on either figure calls for a **10″** (552 and 589 fpm respectively).

**So the choice is explicit rather than incidental:** keep the 9″ and accept the top of the band, or take the 10″ and the quiet. Re-derive the schedule against current loads before anything is fabricated.

**Why the riser carries 276 when the floor's registers are scheduled for 228.** Upper Bath and Upstairs Hallway have no supply register: their 48 CFM reaches them as transfer air from the Play Room and Office, so the riser carries the whole floor's load while only two rooms have an opening for it. That is the design, not a discrepancy — but it means both registers pass more than their own room's share, and the schedule never said so.

| Register | Own room | Carries | Face | fpm |
|---|---:|---:|:-:|---:|
| Play Room — south | 115 | **139** | 5x10 | 535 |
| Office — two floor registers | 113 | **137** | 4x10 each | 328 |

Both stay inside the 500–750 band, and still do on the re-derived 301 (583 and 358 fpm). **The transfer path is what has to be checked, not the sizes** — the bath and hallway only get their air if the doors are undercut and the return pulls through them.

| Duct | CFM | Round | Rectangular |
|---|---:|:-:|:-:|
| Supply riser — as scheduled | 276 | 9″ | 5×16 |
| Supply riser — re-derived | **301** | **10″** | 6×16 |
| Return riser | 281 | 9″ | 9×9 |

The return riser is sized at 281 — Office 113 plus Play Room 168 — rather than the 228 mass balance requires, so the cross-flow split between the two rooms can be set by damper rather than by re-ducting.

Round is unnecessary anywhere inside the chase or under the stairs — it is all concealed, so rectangular wins on fit. Round is worth reserving for anywhere the duct is seen.

### Basement — the binding case

Just over **40″ of wall × ~16″ deep**, between the staircase door and the chimney, with the ceiling cut by the stair diagonal at 45° (36″ of headroom at the north end falling to 3″ at the south).

Two 15″ stud bays, and both are constrained:

- **North bay** — tall, but the chimney sits ~1″ behind the wall face and blocks roughly half its width.
- **South bay** — full width, but a triangle. Only about 9–10″ of its length has 10″ or more of clearance, so it is somewhere to **cross**, not to run.

**Arrangement:** two ducts through the north bay, one through the south — favouring whichever dimension is least constrained at each point. Two 9×9s will pass the tall space and one 9×9 the low space; 6×10 is the more conservative fit and still gives 8.4″ equivalent round at a quiet 492 fpm.

**Pair them by consequence, not by convenience:** the supply gets the better path. With an elevated horizontal air handler this falls out naturally — supply leaves at mid-height into the tall space, and the low triangle takes a duct running *under* the unit.

### Why a horizontal air handler, elevated

Not because a vertical one would not fit in the space — it would. Because of where the connections land:

- A **vertical upflow** unit exits through the **top**, straight into the stair soffit where there is least room.
- A **horizontal** unit exits **sideways at mid-height**, supply one end and return the other, both where they can turn into the under-stair space.

Elevating it a foot or two adds duct routing space beneath, **condensate fall** — a horizontal drain pan needs slope to a drain, and elevation is the cheapest way to buy it — and side service access.

### Main floor

Open space; not a constraint. The cabinet here passes the two risers through and is the natural place to take **the office supply straight up through the floor**, keeping that room's supply out of the attic entirely. The office is **100 CFM unbiased — 42% of the second floor's 238** — so this solves the largest single room with the shortest and safest run. (The figure was 87 CFM on an earlier model state; the percentage happens to be unchanged.)

**On the schedule's biased basis the ranking flips**: Office 113 against Play Room 115. That does not mean the Play Room is the bigger load — it is the deliberate choice to size the Play Room's new south duct for the *whole* room rather than half, because its existing east duct is unmeasured. Unbiased, the office is larger by 100 to 86.

### Second floor

Three shapes were considered, and **the preference has moved to C**:

| | Approach | Verdict |
|---|---|---|
| A | Straight cabinet wall from the chimney | **Rejected** — lands mid-latch on the attic access |
| B | Diagonal cabinet from the chimney to the corner | Viable — puts the attic access *inside* the cabinet, at the cost of floor area on the level with least to spare |
| C | **Ducts leaning diagonally through the main floor, emerging beyond the knee wall** | **Preferred** — no second-floor cabinet needed |

C avoids building on the second floor at all, and what it puts in the knee-wall attic is mostly **return** — which the governing principle at the top of this document permits, and which is the whole reason that principle is stated first.

Two supplies are the exceptions, and both are deliberate:

- **The office supply goes straight up through the office floor**, never entering the attic. It is the largest single room on the level, so the shortest and safest run serves the biggest load.
- **The play room takes a short attic run** for its extra supply. Short is the mitigation: a few feet of insulated supply in a buffer space is a different proposition from a trunk crossing it.

A small duct-only enclosure on the second floor stays available if the diagonal proves awkward to frame. B keeps one quiet advantage worth recording: a diagonal face is a better place to turn a duct than a square corner, and a 45° transition carries roughly half the equivalent length of two 90s.

**The attic is used deliberately, for returns only.** One return riser comes up and splits in two, running to the far corners of both rooms; supply arrives short and central. That is the governing principle applied.

---

## Room-by-room notes

**The two old second-floor ducts are load-bearing, not supplementary.** Both measure about **3 × 10**, which is 5.74″ equivalent round and carries roughly **84 CFM** at design friction — a quiet 403 fpm.

| | Needs | One 3×10 gives |
|---|---:|---:|
| Play Room (west) | 72 | 84 ✓ |
| Office (east, by the window) | 83 | 84 ✓ |

Together **168 CFM — 90% of the 186 those two rooms need unbiased** (Office 100, Play Room 86). That flips the framing: the old ducts are the *base* and the chase riser is the *margin*, which is a cheaper build than the other way round. Worth confirming both are clear and intact end to end, especially the one currently dead-ending under the floor near the east window — at those numbers it is carrying real load, not a nice-to-have.

**Office** — primary supply up through the floor from the main-floor cabinet, keeping it out of the attic entirely. The old duct near the window adds perimeter supply, which is what keeps this floor from being purely central-supply.

**Kids room (west)** — the second old duct, also inside conditioned space.

**Kitchen** — 153 CFM, the second-largest room, and its northern half sits over the crawlspace rather than the basement. Solved by the same principle: a **return** runs from behind the basement bathroom straight through the plank atop the cinder block — where old drain-pipe holes can be widened — out to a register under the kitchen sink. Buffer space, but return only.

The existing supply register sits diagonally across the room from there, which is the best case rather than a compromise: **supply and return at diagonal corners** gives the longest mixing path across a room and is exactly what you would design if free to choose.

---

## Where the design is knowingly unconventional

**Central supply with perimeter return inverts normal practice.** Convention puts supply at the perimeter — under windows, against exterior walls, where the load is and where you want to break the cold-surface draft — and returns centrally. This scheme does the reverse on the second floor.

The trade matters more in an old house with mixed glazing than in a tight new one. Two things make it acceptable:

1. The plan already includes **secondary perimeter supply** via the old window-adjacent duct in the office. The scheme is *primary central + secondary perimeter*, a recognised retrofit compromise rather than a straight inversion.
2. There is **room to add supply later** — including a north run — if internal room balance turns out poor. The chase is sized with margin and the risers are not the constraint.

**The assumption to check is throw.** Whether a central register at **100 CFM** reaches the office's far wall is Manual T territory. A typical floor register at that flow throws 8–12 ft against a room around 14–15 ft, so a central position needs ~7 ft — plausible with margin. It remains a catalogue lookup at register selection rather than something to take on faith.

**This assumes the central register carries the whole 100 CFM.** The office also has the existing perimeter duct, and if that stays in service the central register carries less and throws shorter. Either specify the central register for the full load and treat the perimeter duct as recovered capacity — the same call already made for the Play Room — or size both and check the throw at the reduced figure. **What must not happen is sizing for the full load and then quietly splitting it.**

---

## One air handler or two

The company suggests a **second ducted air handler** — two handlers with ducts, rather than a head per room with none. Described as "internal", which sounded like conditioned space and would have removed the strongest objection outright. **It is not.** The proposed location is the **north knee-wall attic**, accessed through the wall at the top of the stairs.

That puts it back where the standard objection lives, and adds a second one that is harder to fix.

### It is attic equipment, and this attic is hot

The knee-wall attics here are insulated at the floor and wall planes, so the space itself sits outside the thermal envelope. Our own load model estimates **summer attic air at about 133°F** — the sol-air figure Eldr derives from outdoor design plus roof gain. A heat-pump air handler, its coil, its cabinet leakage and every foot of its supply duct would live in that.

That is the whole reason retrofit attic equipment loses 20–30%, and it applies here in full. It also brings a condensate pan over a finished ceiling, and service access — filter changes included — through a knee-wall hatch at the top of the stairs.

### The placement problem, which is worse

**A unit in the north knee-wall attic can reach the north side of those rooms and not the south.** That is not a detail to solve later; it decides what the scheme can deliver. The south side of the second floor carries load that the conservative numbers here already show, and they *understate* it: a third of that ceiling area is not drawn yet.

The suggested remedy is a duct run in a channel along the east side of the office, into the small east knee-wall attic. **A channel along a finished wall is a chase.** If building a chase is acceptable, the objection to this design — which is built around a chase — was never about chases but about *which* one.

The two compared:

| | This design's chase | The proposed channel |
|---|---|---|
| Location | Three-level chase alongside the chimney | A box along a finished office wall |
| Serves | All three floors, supply and return | One register |
| Inside the envelope | Yes | Partly — it ends in an unconditioned knee-wall attic |
| Visible | No | Yes, in a room people use |
| Has to exist anyway | **Yes** — the main floor needs it | No |

The second unit is meant to *avoid* building a chase. Needing one anyway, in a worse place, to reach a corner the first unit was going to reach through the chase already planned, is the argument turning back on itself.

### What two handlers buy

- **Real zoning, which one unit cannot have here.** The strongest point in its favour, and the analysis here supports it: neither the basement (167 CFM, 14% of total) nor the second floor alone can be a hard zone on a single unit this size without starving the blower. Smart throttling of individual branches works, hard per-floor zoning does not. **Two handlers make per-floor zoning real instead of approximate** — and there are already three thermostats in this house expecting exactly that.
- **Much shorter duct runs, and therefore lower static pressure.** Static pressure is the thing most likely to defeat the single-unit scheme, and a second handler attacks it directly rather than arguing about it.
- **Independent part-load behaviour**, and no single point of failure for the whole house.

### What it costs

- A second indoor unit, a second filter, a second condensate path, a second service point, and a second maintenance schedule for as long as the house stands.
- **Somewhere inside conditioned space to put it**, which on the second floor of this house is not obvious. The knee-wall attic is what makes the space available, and putting the unit there is precisely what the internal framing rules out.
- Equipment and installation cost against a riser that has to exist anyway — the main floor needs the chase regardless.

### Where the single-unit case still stands

1. **The load is modest.** 238 CFM to the second floor against 751 to the main floor. The second floor is a geometry problem, not a capacity problem — and a second handler is a capacity answer to a geometry question.
2. **Both supply and return reach it.** A second handler solves the *return* problem by putting the blower where the air is, which is the usual reason "you can't duct a second floor" holds in retrofits. The chase has measured room for both, so the single unit is not relying on the return problem going away.
3. **The chase is conditioned.** Ducts stay inside the envelope for their whole run, which is the same benefit the internal-handler proposal is reaching for, obtained a different way.
4. **The numbers are conservative.** See the ceiling-area caveat above.

### The decision criterion

**Static pressure decides whether one unit is enough.** If it can move 1,245 CFM through this layout at an acceptable external static pressure, one unit is the better buy — everything inside the envelope, half the equipment, one filter to change. That is a question the fitting counts settle, and a contractor is better placed to supply them than this model is. Ask for the counts rather than for an opinion.

**But placement decides whether two units would even help.** A second handler in the north knee-wall attic does not serve the south side of those rooms, and no amount of static-pressure headroom changes that. So the two questions are independent, and they should be asked in this order:

1. *Where would the second unit sit, and which registers can it reach?* If the answer is "north only, plus a channel along the office wall", the proposal has not solved the problem it was brought in to solve.
2. *Only if it reaches everything:* does one unit hit its static-pressure limit?

A second handler somewhere central and inside the envelope would be an alternative worth pricing, and would buy the per-floor zoning a single unit cannot have here. **The north knee-wall attic is not that location**, and choosing it converts the strongest argument for two units into an argument about where to put a chase.

**Where to be careful.** Eldr's Manual D uses a flat 1.5× fitting factor, not true fitting equivalent lengths. Real elbows, tees and boots on a three-storey run add 50–150 ft of equivalent length, so any static-pressure figure computed with the default is optimistic. Either raise the factor to something defensible (2.5–3) and say so, or count fittings by hand for the contested run. **Do not hand over a number that flatters the case on a modelling shortcut** — it is the one thing that would cost the credibility everything else earns.

The current HVAC company specialises in insulation, so envelope work is likely already in their plan. A tighter envelope lowers the load the ducts have to carry, so the two efforts work together.

---

## The maintenance wall — front door to primary bedroom

The wall the upstairs-east risers pass through, and the trickiest build in the scheme. It is currently **one stud space deep**, with room for exactly one more inside the bedroom — a quirk of the doubled/offset wall created when the bedroom was extended south. Breaking in from the bedroom side showed **2–3 studs and an old conduit hole through to the basement**.

**The conduit hole is the datum.** It is a single point piercing both the basement and the wall cavity, so it registers the two coordinate frames against each other — the same shared-anchor trick the joists provide. Measure the studs relative to it and reference every riser to it, and "I cannot tell where the studs are versus where the ducts come up" becomes exact offsets from one known hole.

**Rectangular, not round.** The depth budget is roughly two stud bays back to back (~7″), and a bay gives about 14.5″ clear. Three round 5–6″ ducts side by side need 15–18″ and fight the studs. Residential **wall-stack duct** — 3.25x10 or 3.25x12, purpose-made to run vertically between studs in a 2x4 wall — puts the shallow dimension across the wall depth and solves the problem directly. Oval is the fallback. Prefer running each duct *within* a bay so no stud needs notching; if a riser must cross one, verify the partition is non-load-bearing first, because the south-extension quirk muddies that.

**The face comes off.** The built-in over it is designed as a removable panel on a French cleat, so the risers stay reachable without demolition — which is why this scheme runs fewer ducts through the wall rather than over-provisioning so it never has to be opened.

## Constraints from the rest of the basement

**The SW utility corner is spoken for.** It is being prepped for a Powerwall — a 45″ × 30″ unit on plywood, with a 40″ × 14″ electrical panel to its left and network gear to the right. Relocating the air handler under the stairs is partly what frees that corner, so **duct routing must stay clear of it**; it is not spare wall.

**Cost intuition for spiral:** roughly *diameter × 2 × length* in dollars — a 6″ run at 5 ft lands near $60, so about $12/ft. Order of magnitude only, useful for judging whether a routing change is worth arguing about.

---

## Open questions

- **Which dimension constrains the basement ducts** — stud-bay width after the chimney, or the 16″ closet depth. Changes duct proportions, not position.
- **The two old ducts** — sizes, and whether the office one can be rescued from its dead end.
- **The knee-wall attic itself** — not yet entered. Estimated ~32″ deep from the 56.5″ reading.
- **The chimney's absolute position** carries a 2″ disagreement with its own tape chain; fine for layout, not for cutting.
- **The second floor's interior geometry** lags the east–west registration applied to the perimeter, so per-room figures on that level are stale until it catches up.

## Equipment

Sized on the larger of heating and cooling, which here is heating: **40,331 BTU/hr = 3.4 tons** on current geometry, rising to roughly **3.8 tons** once `basement_wall` takes the professionals' measured U-value. So the target is **3.5–4 tons**, and 4 is the safer read.

### Bosch IDS Ultra — the leading candidate

The cold-climate member of the IDS family, and the relevant one here: NJ's 99% design temperature is 15°F, and the Ultra delivers **100% heating capacity down to 5°F**, continuing to initiate heating to −13°F. DOE Cold Climate Heat Pump Challenge approved and ENERGY STAR V6.1 Cold Climate certified, tested at Oak Ridge. Uses **R-454B**, an A2L low-GWP refrigerant.

Two-part system: **BOVA** outdoor condenser, **BIVA** indoor air handler.

| Component | Model | W × H × D (in) |
|---|---|---|
| Indoor air handler, 4 ton | BIVA-48MCB-M19X | **22.0 × 54.5 × 24.0** |
| Indoor air handler, 5 ton | BIVA-60MCB-M19X | 22.0 × 54.5 × 24.0 |
| Outdoor condenser, 5 ton | BOVA-60MTB-M19E | 29.125 × 43.3125 × 29.125 |

The 4-ton and 5-ton air handlers share a cabinet. Verified from Bosch's own IDS Ultra spec sheet; the 3-ton system exists per Bosch's product literature but its dimensions are not on the sheet consulted.

**What it means for the basement.** In upflow the unit is 54.5″ tall on a 22 × 24 footprint. Converted to horizontal it lies down: roughly **22–24″ tall** (depending on which face it rests on) on a **54.5 × 24** footprint. Against the ~40″ of headroom at the tall end of the stair wedge, a horizontal unit leaves **16–18″ beneath it** for elevation and a duct — which is the configuration this plan assumes.

In the open part of the bar area either orientation fits: the basement's 84″ to joist bottoms clears an upflow cabinet with 29.5″ to spare. The reason to prefer horizontal is not the unit's height but **where its connections land** — sideways at mid-height, matching the wedge, rather than out of the top into the stair soffit.

Electric heat kits (EHK-05B through EHK-20B, 5–20 kW) fit the cabinet without modification, which is the backup-heat path if the cold-climate performance ever needs supplementing.

### Air handler orientation

**Most residential air handlers are multi-position** — the same cabinet is sold for upflow, downflow, horizontal-left and horizontal-right. The Bosch BVA line ships configured for *upflow or horizontal-right* and is field-convertible to *horizontal-left or downflow*. The IDS Ultra air handler's drain pan is explicitly described as offering "flexibility for VT or HZ applications."

**The drain pan is the part that changes.** Condensate has to fall toward a drain in whatever orientation the coil ends up, so conversion is usually a matter of repositioning the pan and sometimes fitting a kit. Ask specifically whether the horizontal conversion needs a part, and confirm the drain fall — a horizontal pan with insufficient slope is a recurring source of overflow.

### The controls trade-off

The requirement here is variable speed **and** open control rather than a locked ecosystem. The two pull against each other:

| | Conventional 24V | Bosch communicating |
|---|---|---|
| Thermostat | any — ecobee, Home Assistant, anything | Bosch's own |
| Modulation | **staged**, not continuous | full compressor range |
| Openness | complete | closed |

A Bosch variable-speed unit **can** run on a third-party 24V thermostat, because the modulation logic lives in the unit rather than the stat. The IDS Ultra's remote monitoring is documented as working "even without a communicating thermostat." A two-stage-capable smart thermostat is the practical minimum.

The cost is granularity. The Ultra's compressor modulates **35% to 138% in 1% increments**, and a conventional thermostat can only ask for stages, so most of that resolution goes unused. A communicating thermostat unlocks it and closes the system.

**Worth establishing before committing:** whether local telemetry is available, or whether monitoring only goes through Bosch's EasyAir cloud app. The house already runs an LGTM stack, so a local data path is worth more here than in a typical install.

## Future options, deliberately deferred

- **Garage mudroom conversion.** Split the return off the kitchen run at one end, bring supply across the *conditioned* basement, and enter at the opposite end. The governing principle holds, and supply and return land diagonally opposite — the arrangement you would choose freely.
- **A north supply run** if room balance proves poor.
- **More second-floor supply** beyond the central pair and the two old ducts.
- **Manual T** — register throw and spread — which turns "should reach the far corner" into a calculation.
- **Grade line and second-floor ceiling geometry**, the two largest remaining Manual J gaps, both parked while the duct layout takes shape.
