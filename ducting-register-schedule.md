# Register schedule — working document

**This file is meant to be edited directly.** It is the per-register duct schedule for the proposed scheme, generated 2026-09-02 and hand-tuned as the layout firms up. Sizes come from Eldr's equal-friction math at 0.08 in.wc/100 ft; the reasoning behind the airflow lives in [`ducting-scheme.md`](ducting-scheme.md).

Airflow is biased on purpose — **second floor ×1.35**, **basement ×0.70**, main floor unchanged — and computed on a **30°F supply-air rise**, the heat-pump figure. (A 50°F rise is a gas furnace and undersizes every heating-driven duct by 1.67×.)

**Every size below is per individual duct**, not per room. A room with two supplies gets two ducts of the size shown.

---

## Schedule

| Level | Room | Room CFM | Sup | CFM ea | Round | Rect | fpm | Ret | CFM ea | Round | Rect | fpm | New? | Comment |
|---|---|---:|:-:|---:|:-:|:-:|---:|:-:|---:|:-:|:-:|---:|---:|---:|
| Basement | Future Media Room | 85 | 1 | 85 | 6″ | 3x10 | 435 | 1 | 84 | 6″ | 3x10 | 430 | 2 | Own ceiling return |
| Basement | Utility Room | 82 | 1 | 82 | 6″ | 3x10 | 415 | 1 | 83 | 6″ | 3x10 | 425 | 2 | Own ceiling return |
| Main | Kitchen | 251 | 2 | 126 | 7″ | 4x10 | 470 | 1 | 251 | 9″ | 5x14 | 569 | 2 | One tricky |
| Main | Main Bed | 227 | 2 | 113 | 7″ | 4x10 | 424 | 1 | 227 | 9″ | 5x14 | 513 | 1 | Return narrow? |
| Main | Living room | 143 | 2 | 71 | 6″ | 3x10 | 363 | 1 | 143 | 7″ | 4x12 | 534 | | |
| Main | Kids Room | 64 | 1 | 64 | 6″ | 3x8 | 324 | 1 | 64 | **8″** | 4x12 | 421 | | Grille carries 64; the **duct** is sized 8″ for the **147** it shares with the utility return, which is where 421 fpm comes from |
| Main | Main Bath | 36 | 1 | 36 | 5″ | 3x6 | 263 | — | — | — | — | — | | |
| Main | Main Closet | 17 | 1 | 17 | 4″ | 3x6 | 191 | — | — | — | — | — | 1 | Tiny split from orphan |
| 2nd | Play Room | 115 | 2 | 115 / ? | 7″ | 4x10 | 429 | 1 | **168** | 8″ | 4x14 | 481 | 1 | The **new south** duct alone is sized for the whole 115; the existing east register contributes an unknown amount on top — not a second 115 |
| 2nd | Office | 113 | 2 | 56 | 5″ | 3x8 | 413 | 1 | 113 | 7″ | 4x10 | 423 | 2.5 | Rescue orphan counts half |
| 2nd | Upper Bath | 28 | — | — | — | — | — | — | — | — | — | — | | No supply — wants electric heat |
| 2nd | Upstairs Hallway | 20 | — | — | — | — | — | — | — | — | — | — | | Swept by transit only |

Rectangular sizes are the shallowest option holding an **aspect ratio at or under 4:1**. Flatter than that costs friction and makes fittings awkward, so a 3x20 is not a substitute for a 4x14 even though the areas are similar.

**Two return decisions are baked into the table above.**

*The Utility Room return joins the Kids Room branch rather than a basement trunk.* That branch passes through the basement ceiling on its way down, so tapping it is the short path — but it means the branch carries **147 CFM, not 64**. It is drawn at 8″, which runs 421 fpm and is fine; the 6″ the schedule originally called for would have run 747 and been a mistake. **A shared branch is sized for the sum, and the room name on it stops being the whole story.**

*The basement runs two ceiling returns rather than one midline.* The earlier plan collapsed both rooms onto a single 167 CFM midline grille, which was the cheaper build — three new ducts instead of five. Drawing it settled the question the other way: the two rooms are separated by the stair and utility walls, so a single midline grille would have pulled almost entirely from whichever room it sat in, and the other would have had to give its air up through a doorway. Each room now returns where it is supplied, at **84 and 83 CFM**, the same total split two ways.

*The Play Room gets two supplies, and the new one is sized as though it were the only one.* The existing east-wall duct is small enough to be suspect, so the new south-wall register is sized for the room's full 115 CFM rather than for half of it. If the east duct turns out to carry its share, the room is comfortably over-served and the damper takes it back; if it carries nothing, the room is still right. **Sizing the new duct for half would have made the room hostage to a duct nobody has measured.** Treat the east register as recovered capacity, not as a design assumption — it is the one supply in this house whose contribution is unknown.

*The second-floor returns are sized for the cross-flow split, not for their own rooms.* The Play Room's is sized at **168** rather than its own 115, so the option to drag air across from the Office exists without re-ducting. Their combined capacity is 281 against the 228 the floor actually needs — **the dampers set the real split**, and sizing for the larger case costs a nominal size, not a redesign.

Room-name mapping, since the model and conversation differ: the 2nd-floor "kids room" is **Play Room**; the main-floor "small kids room" is **Kids Room**; "bathroom" with supply only is **Main Bath**. The two basement supplies are named by position in the model and by room here — **"west basement" is Future Media Room**, **"basement east" is Utility Room**.

---

## Register and grille faces

Sized on face velocity only. **Supplies assume 75% free area** — the generous end for a louvred face, so a grille with heavier blades runs faster than shown, never slower. Returns are computed on gross area.

Targets: supplies **500–750 fpm** is the normal band and 600 is where this document starts objecting; returns **300–500 fpm**, with the sizes below aimed at the quiet end. That aim is a choice, and an expensive one — **a return sized at 300 fpm is two-thirds larger than the same airflow at 500.** Treat 500 as the requirement and the rest as comfort.

**This is not Manual T.** Throw, spread, drop and NC need the room's dimensions against a specific manufacturer's catalogue, and the choice of *where* on the wall or floor matters as much as the size. Treat the faces below as the starting schedule a contractor prices, not as a selection.

Faces below are **as drawn in the model**, sized against available space, with the resulting velocity computed. Every face is now inside its band.

| Level | Register | CFM | Face | fpm | Verdict |
|---|---|---:|:-:|---:|---|
| Basement | Future Media — NW ceiling `[circular]` | 85 | 5x10 | 326 | ok |
| Basement | Utility — SE ceiling `[circular]` | 82 | 5x10 | 315 | ok |
| Main | Kitchen — SW | 126 | 6x11 | 367 | ok |
| Main | Kitchen — SE | 126 | 4x15 | 403 | ok |
| Main | Main Bed — NE | 113 | 6x11 | 329 | ok |
| Main | Main Bed — W | 113 | 6x11 | 329 | ok |
| Main | Living room — NW | 71 | 5x10 | 273 | ok |
| Main | Living room — NE | 71 | 6x10 | 227 | ok |
| Main | Kids Room | 64 | 6x12 | 171 | Generous; throw will be weak |
| Main | Main Bath | 36 | 5x8 | 173 | ok |
| Main | Main Closet | 17 | 4x8 | 102 | ok |
| 2nd | Play Room — south | 115 | 5x10 | 442 | ok |
| 2nd | Play Room — east | — | 4x8 | — | Existing; contribution unknown |
| 2nd | Office — NE floor | 56 | 4x10 | 269 | ok |
| 2nd | Office — W floor | 56 | 4x10 | 269 | ok |
| | **Supply registers** | | | | **15** |
| Basement | Future Media — SW ceiling `[circular]` | 84 | 5x12 | 202 | ok |
| Basement | Utility — NE ceiling `[circular]` | 83 | 5x12 | 199 | ok |
| Main | Kitchen | 251 | 8x14 | 323 | ok |
| Main | Main Bed | 227 | 5x9 | 726 | Matches its duct — see below |
| Main | Living room | 143 | 6x12 | 286 | ok |
| Main | Kids Room | 64 | 4x10 | 230 | ok |
| 2nd | Play Room — SW | 168 | 6x12 | 336 | ok |
| 2nd | Office — SW | 113 | 6x8 | 339 | ok |
| | **Return grilles** | | | | **8** |

### The two kitchen faces, now settled

Both were constrained by cabinetry and both have been redrawn at the size this schedule asked for:

| Register | Was | fpm | Now | fpm |
|---|:-:|---:|:-:|---:|
| Kitchen — SE supply | 2x15 | 806 | **4x15** | 403 |
| Kitchen return | 3x20 | 602 | **8x14** | 323 |

**The kitchen SE register was the one worth building around.** At 2″ of height under the cabinetry it ran 806 fpm — not marginal, audible, and in a kitchen where people stand. The 4″ height halves it to 403. **Getting that height is still a construction decision** — one cabinet moves over, or the cabinet is modified — so the drawn 4x15 records the decision rather than removing the work. Note that 403 fpm assumes a generous 75% free area; a heavier louvred face runs faster.

**The kitchen return was about area, not length.** 251 CFM needs roughly 120 in² at 300 fpm, and the 3x20 gave 60. What it did *not* need was to stay 20″ long: preserving the drawn dimension and growing only the other gives 6x20, a 3.3:1 grille nobody stocks.

| Target | Area | Sensible face |
|---|---:|:-:|
| 300 fpm — quiet | 120 in² | 10x12 |
| 350 fpm | 103 in² | **8x14** |
| 500 fpm — the ceiling | 72 in² | 6x12 |

**8x14 is the pick** — a stock size at 323 fpm, and what the model now carries. 6x12 is defensible if space is tight, at the cost of a return you can hear.

If the 3″ height is fixed by cabinetry, no single grille solves it — 3x40 would be needed, and the answer is two openings rather than one enormous one.

*Already corrected in the model:* Main Bed W supply 4x8 → **6x11**, matching its NE twin at the same 113 CFM, and Office SW return 4x8 → **6x8**. Neither had a space constraint; both were simply drawn small.

**The Main Bed W register may also want to point east** rather than the way it is drawn — a throw question, and throw is Manual T's business rather than something the plan view can settle.

### The main-floor return path is the real bottleneck

It was a single 4x8 running 30 ft with three returns hanging off it — Main Bed 227, Kids Room 64, and the Utility Room's 83 via the Kids Room tap. That is 374 CFM through 32 in², about **1,680 fpm**.

**The run is now split at the point where it stops being buried**, which is the remedy this section used to argue for:

| Segment | Serves | CFM | Section | fpm |
|---|---|---:|:-:|---:|
| `Return branch for kids room and basement NE`, 8.9 ft | Kids Room + Utility | 147 | **6x10** | 353 |
| `Return branch for main bedroom`, 21 ft | Main Bed | 227 | 4x8 | 1,022 |

**The two rooms behind the pinch are out from behind it.** The Kids Room and Utility Room now return through 60 in² at a quiet 353 fpm, where before they shared a duct running four times over.

**The main bedroom segment still reads 1,022 fpm, and that number is notional.** It is the existing duct through the inaccessible crawlspace, drawn at the size it actually is. At the ~91 CFM it is believed to pass it runs 410 fpm and is quiet — the duct is not undersized for what goes through it, it is undersized for what the room wants. That gap is a capacity problem to solve at the grille or with a transfer path, not a duct to re-size in the model.

The split still rests on drawn adjacency. **Verify the topology on site before pricing anything** — specifically that the open basement run really does extend as far as the model puts the split.

**The Main Bed return is not in that list, though its number is the worst.** 726 fpm assumes 227 CFM actually arrives, and it cannot: behind that grille is the existing 7.5x4 through the inaccessible crawlspace, good for roughly 91 CFM. At 91 the 5x9 face runs 291 fpm and is perfectly quiet. **The grille is correctly sized for the duct; the duct is the problem**, and the plan of record remains a transfer grille over the bedroom door first.

The Kids Room supply is the opposite case — 6x12 for 64 CFM is generous enough that throw suffers. Harmless in a small room, and worth leaving if the opening is already cut.

---

## How trunks are sized

The duct system is a hierarchy, and each level is sized by **the air passing through that particular segment** — not by anything upstream or downstream:

| Term | What it is | How it is sized |
|---|---|---|
| **Plenum** | The sheet-metal box bolted straight onto the air handler — one on the supply outlet, one on the return inlet | By the unit's opening, not by CFM. Its job is transition. |
| **Trunk** | The main duct leaving the plenum, carrying the bulk of the air | By total CFM passing through it |
| **Sub-trunk** | A trunk serving one zone or floor, fed from the main trunk or straight off the plenum | By that zone's total CFM |
| **Branch / runout** | The duct serving a single register | By that register's CFM |

**Anything serving more than one register is a trunk.** So yes — the large duct going up to the second floor is a trunk, and so is the return coming back down from it. Both carry 276 CFM and serve four registers before splitting.

**A trunk shrinks as branches leave it.** Two standard ways to handle that:

- **Reducing trunk** — step it down after each takeoff. Keeps velocity roughly constant, uses less metal, needs more fittings.
- **Extended plenum** — hold one size for most of the run and reduce once near the end. Simpler, slightly more material, and much the more common choice in residential work.

### The main trunk may not need to exist

| Segment | CFM | Round | Rectangular |
|---|---:|:-:|:-:|
| Basement sub-trunk | 167 | 8″ | 4x14 |
| Main sub-trunk | 737 | 14″ | 8x20 |
| 2nd floor sub-trunk | 276 | 9″ | 5x16 |
| *Main trunk at the unit* | *1,179* | *16″* | *10x22* |

That 16″ figure assumes **one** duct leaves the plenum and splits later. It does not have to be built that way, and in this basement it probably should not be — a 16″ round plus insulation hanging under joists at 84″ is a real intrusion.

**If the plenum carries takeoffs directly, the 16″ duct never exists.** Splitting the main floor into two sub-trunks makes the largest single duct in the house a **10″**:

| Off the plenum | Serves | CFM | Round |
|---|---|---:|:-:|
| Basement | Future Media, Utility | 167 | 8″ |
| Main — south | Main Bed 227, Living room 143 | 370 | **10″** |
| Main — north | Kitchen 251, Kids Room 64, Main Bath 36, Main Closet 17 | 368 | **10″** |
| 2nd floor riser | Office, Play Room, Upper Bath, Hallway | 276 | 9″ |

Four takeoffs, nothing above 10″, and the south/north split happens to follow the routing already planned — south through the stairs, north through the basement bathroom and west along the girder. The cost is a larger plenum with room for four connections, and enough spacing between them that they do not rob one another.

---

## Returns are not a mirror of the supply side

Total return must equal total supply. But the return side is **a smaller number of larger openings**:

- **Fewer.** Rooms without their own return give their air up through door undercuts or transfer grilles. Here that is Main Bath, Main Closet, Upper Bath and Upstairs Hallway.
- **Larger per CFM.** Returns are designed at lower velocity — roughly 400–600 fpm against a supply branch's 600–900 — so the same airflow wants a bigger duct.
- **Much larger at the grille.** A supply register is limited by throw and noise to roughly **100–150 CFM**. A return grille does not throw, so one can comfortably take **300–500 CFM**. That asymmetry is why one return serves what needed two supplies.

### Balance per level

With the Upper Bath and Upstairs Hallway carrying no supply:

| Level | Total supply | Return registers | Together they must carry | Sized for |
|---|---:|:-:|---:|---:|
| Basement | 167 | 1 | 167 | 167 |
| Main | 737 | 4 | 737 | 737 |
| 2nd floor | **228** | 2 | **228** | 281 — deliberately generous |

### Using return placement to balance the second floor

Oversizing the Play Room's return to drag air across from the Office is a standard technique, and the numbers work. The only constraint is that the floor's two returns sum to 228.

| | Supply | Return | Net |
|---|---:|---:|---|
| Office | 113 | 60 | 53 CFM leaves |
| Play Room | 115 | 168 | 53 CFM arrives |
| Upper Bath | — | — | swept by transit |
| Upstairs Hallway | — | — | swept by transit |
| | **228** | **228** | balanced |

That drives 53 CFM through the bath and hallway on its way to the Play Room. Shrink the Office return further to pull harder; the pair just has to keep summing to 228.

**The mechanism only works if the air has a path.** Door undercuts of ¾″ or transfer grilles between office, bathroom and play room are what make this real rather than theoretical — without them the rooms pressurise and the flow stops.

### Transit air sweeps a room; it does not heat one

This is the trap in leaving the Upper Bath unsupplied. Air arriving from the Office is at room temperature and has no heat to give up. Steady-state estimate for the bath, on a UA of about 16.5 BTU/hr·°F:

| Transit air through it | Design-day temperature |
|---:|---:|
| 53 CFM | ~58°F |
| 100 CFM | ~63°F |

Conduction from adjacent rooms through interior walls is ignored, so reality is warmer — but no plausible transit rate reaches 70°F, because the air has nothing to deliver.

**A bathroom wants its own heat.** Three ways out, and the middle one is usually best here:

1. Supply it from the riser and accept the register landing over the stairs.
2. **Electric resistance — a toe-kick heater or heated floor.** Standard for exactly this case, cheap to run for a room this size, independent of the duct layout, and it makes the bathroom warmer than ducting would. It also avoids forcing the north run through the main-floor bathroom and kitchen void.
3. Accept roughly 60°F on design days.

The Upstairs Hallway needs no such treatment — it is transit space, tolerates being cool, and borrows heat from the rooms it connects.

---

## Zoning — air is not water

The house already runs three heating zones, so three zones feels like the obvious carry-over. It is not, and the reason is worth being blunt about:

> **Zoning water is easy. Zoning air is hard.** A zone valve closes and the boiler simply makes less hot water. A zone damper closes and the air has to go *somewhere* — the blower is still turning.

The arithmetic here is unfriendly. Against a whole-house design of ~1,180 CFM, and a 3.5–4 ton air handler whose minimum airflow is roughly 40% of nominal (**550–640 CFM**):

| Zone calling alone | CFM | Versus minimum |
|---|---:|---|
| Basement | 167 | **14% — far below** |
| 2nd floor | 228 | **19% — far below** |
| Main | 737 | fine |
| Basement + Main | 904 | fine |

**Neither the basement nor the second floor can be its own hard zone** on a single unit this size. Either alone starves the blower and drives static pressure up.

What works, roughly in order of preference:

- **Manual balancing dampers and no zoning.** A modulating compressor running long low-output cycles does much of what zoning promises, because the classic reason to zone is a single-stage unit blasting and shutting off. Simplest, cheapest, and reversible.
- **Modulating zone dampers** that throttle rather than shut, so every zone keeps some flow. Avoids the minimum-airflow cliff entirely.
- **A dump zone** — usually the basement, damper never fully closing, so minimum flow is always available.
- **A zone panel that reduces blower speed to match the open zones.** Correct in principle, but see the caution below.
- **A bypass damper.** The old answer and the bad one: it recirculates supply air to the return, degrading dehumidification, and can freeze the coil in cooling or overheat it in heating. Avoid.

**The caution that links back to controls:** a zone panel able to stage the blower generally has to *communicate* with the unit, and zone panels are frequently where the open-controls option quietly disappears. Zoning and third-party thermostats pull against each other, the same tension as modulation and open control.

**Recommendation: manual dampers now, zoning later if the balance disappoints.** The stack effect is real and does not care about modulation, so this may not be the final answer — but it is the cheap experiment, and the ductwork for it is identical either way.

### Throttling is not zoning, and the distinction matters

Everything above concerns **hard zone dampers**, where a whole floor's damper shuts. Smart-home *throttling* of individual branches is a different and much safer thing, because **throttling redistributes air rather than removing it** — a partly-closed damper raises static slightly and the air leaves through the other branches. The system only starves when most of it closes.

| Action | CFM affected | Share of 1,180 |
|---|---:|---:|
| One basement branch throttled by half | ~28 | **2.4%** |
| Whole basement throttled hard | 167 | 14% |
| Basement + 2nd floor together | 395 | 33% |

A single motorised branch damper reacting to a local sensor — the computer rack under the NW basement supply, for instance — is a balancing damper that moves by itself. It is not a system-level risk.

**Compressor turndown and blower minimum are separate constraints.** The unit modulates capacity to roughly a third; the blower minimum exists to keep enough air over the coil, above freezing in cooling and below the high limit in heating. That minimum **scales with output**, so at a third capacity the required airflow falls too and demand tracks requirement. The failure mode is not low flow — it is **dampers throttling while the compressor stays at full**, which is precisely what two independent control systems can do to each other.

**The architecture that works:** the unit's own thermostat decides *whether* the system runs and at what capacity; the smart-home dampers decide *where* the air goes within that. Clean separation, and it sidesteps the communicating-thermostat trap entirely, because the dampers are just motorised balancing dampers the unit never needs to know about.

**The rule that keeps them from fighting:** never throttle more than ~30–40% of total design airflow at once, and never fully close a damper. Give the smart-home logic a hard floor it cannot cross regardless of what the sensors say.

And if nothing calls, the system is simply off — the minimum-airflow problem only exists while it is running. For a basement that holds temperature unconditioned, letting it drift when it is the only caller uses thermal mass the house already has rather than conceding anything.

## Duct materials

| Option | Where it fits | Watch |
|---|---|---|
| **Rectangular sheet metal** | Joist bays, trunks | Most size-flexible — any dimension |
| **Spiral round** | Exposed runs | Standard increments only; low friction, strong |
| **Double-wall spiral** | Exposed where insulation is wanted | Confirm ID vs OD; confirm the liner is cooling-rated |
| **Flat oval** | **Shallow spaces, joist bays, above a soffit** | Round-like friction at a much shallower profile |
| **Snaplock round** | Concealed round runs | Cheaper than spiral, less handsome |
| **Flex** | Final 3–6 ft to a register only | 2–3× the friction of rigid; sags and crushes |
| **Ductboard** | — | Fibres, poor durability, hard to clean. Skip. |

**Flat oval deserves consideration here.** Spiral-formed then flattened, it keeps most of round's low friction in a profile that fits where round will not, which suits a house whose recurring constraint is headroom. Available double-wall.

**Flex is fine and widely abused.** Pulled tight and under about six feet it is a legitimate final connection and kills vibration. Sagging through a joist bay for twenty feet it is the commonest cause of a system that underperforms its design — and it is invisible once the ceiling closes.

**Trunks cannot be resized decently.** The practical hedge is not oversizing — a too-large trunk runs slow, and slow is what makes near takeoffs steal from far ones — but **adding a parallel duct later**, which is a further argument for the four-way plenum split: four modest ducts leave room beside them, one 16″ artery does not.

## Notes for editing

- **Splitting a room's supply does not change its total** — two registers at half the CFM each, and each duct drops about one nominal size.
- **Velocities above ~700 fpm on a branch start to be audible.** Everything here is well under.
- **Under 10 CFM, do not run a duct.** Closets, chimney voids, the bar area and the stair void are served by transfer.
- **Future work is out of scope here.** The garage mudroom conversion is deliberately absent; see the future-options section of `ducting-scheme.md`.
