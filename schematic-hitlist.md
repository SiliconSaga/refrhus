# Schematic hit-list

What still has to change in `Refrhus.sh3d`, who does each piece, and what each is worth. Ranked by BTU/hr impact within each section.

Current run: **40,331** heating against the professionals' **54,260** — a gap of **13,929 BTU/hr**. That gap has moved both ways as corrections landed — wider when the basement was measured and found smaller and better-sealed than the estimate it replaced, narrower again when the design station was corrected from Sweet Home 3D's default to Newark. **Neither movement is progress or regression on its own.** What matters is that the remaining difference is now concentrated in things that can be named — the grade line and the undrawn second-floor roof — rather than spread thinly across assumptions nobody had checked.

After the assembly true-up, almost all of what remains is *geometry* rather than assumptions. Above-grade walls, windows, the slab and occupants are settled against measured values. What is left is drawing and measuring — and item 1.1 alone accounts for roughly a third of the gap.

**The per-BTU figures below predate the basement work and are indicative, not current.** Re-derive from a fresh run before using one to decide what to do next.

**Still valuable, and still the right ranking.** Items 1.1 and 1.2 — the grade line and the second-floor roof — remain the two largest, and between them account for most of the gap. What has changed since this list was written is that the *tooling* side is done: Eldr resolves a U-value per surface, and `tag.py` writes the tags. Items 1.4 and 1.5 are now blocked only on knowing which physical sections are which.

---

## 1. Needs you in the house (measuring or looking)

### 1.1 Grade line — how far below grade does each basement wall sit? — **4,901 BTU/hr**

The single largest remaining item, and it blocks a second one. The professionals split each basement wall at grade: 774 ft² counted below grade at 3–4 ft average depth, the remainder counted among their above-grade walls. Eldr has no grade-line concept and classes the whole wall below grade — 1,135 ft².

That is why `basement_wall` is held at 0.07 instead of their area-weighted 0.196. Their U on our area gives 12,236 BTU/hr against their 9,271 — a 32% overshoot replacing today's 53% undershoot, which is trading one error for another rather than fixing anything.

**What to measure:** the exposed height of each of the four perimeter wall runs — how much wall stands proud of the soil, from grade to the underside of the sill. One number per run is enough; note where a run varies (a walk-out or a window well changes it).

**Then:** the wall gets drawn as two segments, or `basement_wall` gets an area-weighted U. Either way the number can finally be set honestly.

### 1.2 The 2nd floor — knee-wall attic and sloped roof — **3,458 BTU/hr**

Our ceiling area is **984 ft² against their 1,547** — a 563 ft² shortfall that is almost certainly the sloped roof and knee-wall surfaces on the still-incomplete 2nd floor, plus the unmodelled attic volume above the centre.

Note this is *entirely* area. The ceiling U-value already matches theirs (0.057, area-weighted from their construction page), and the unvented attic is deliberate and correct — see [`hvac/index.md`](hvac/index.md). Nothing here is a thermal assumption to argue about; it is surface that is not drawn yet.

**What to measure:** roof angles from the 2nd-floor door onto the garage roof, including the original-versus-kitchen-extension slope change that mildens the pitch toward the backyard. Knee-wall height and the run from knee wall to ridge on each side.

This is also exactly where the insulation work would happen, so the measuring is not wasted effort even if the model never catches up.

### 1.3 Confirm the window inventory — **needed for per-room accuracy, not the total**

The professionals' sheet and your recollection **do not agree**, and the difference is instructive rather than alarming.

Theirs — four single-pane units, 27.2 ft², all on the north half:

| Orientation | Qty | Area | U | Their description |
|---|---:|---:|---:|---|
| Northeast | 2 | 8.3 ft² combined (~4.2 each) | 0.900 | Clear single pane, operable |
| Northwest | 1 | 9.8 ft² | 0.900 | Clear single pane, operable window/door |
| Northwest | 1 | 9.1 ft² | 0.570 | Clear single pane **with storm** |

Yours — the tiny southwest window upstairs (same room as the unidentified door), the garage window, the deck glass door and window, and three basement windows.

Three of the differences are explainable, and two of them are things the model should get right anyway:

- **The garage window is correctly excluded from both.** It sits on unconditioned space, so it contributes nothing to the envelope. You were right to flag it as counting differently.
- **The bricked-in basement window is not a window.** It is opaque wall between basement and crawlspace now.
- **The window-well one is still a window** thermally — a well does not insulate — but gets essentially no solar gain.

What that leaves unexplained is your **tiny southwest upstairs window**: they list no southwest single-pane at all. Either they missed it or their compass differs from the model's.

**What to check:** walk the house and confirm which units are still original glass. The falsifiable version of their claim is *"the only unreplaced glazing is 2 northeast + 2 northwest, one with a storm"* — since the survey puts your front facing roughly southwest, that means all of it is at the back.

Two count discrepancies to keep in mind while you look: Eldr finds **14 windows / 146 ft²** against their 17 units / 152.5 ft², so about three small ones are missing from the model.

### 1.4 Which wall sections are the uninsulated ones — **enables per-room accuracy**

Their four above-grade wall assemblies imply the house has different constructions in different sections:

| Area | U | Assembly |
|---:|---:|---|
| 247.9 ft² | 0.240 | 2x4 stucco/siding, **R-0 cavity, R-0 board — uninsulated** |
| 942.3 ft² | 0.097 | 2x4, R-11 cavity |
| 222.0 ft² | 0.097 | **garage partition**, R-11 cavity |
| 130.5 ft² | 0.091 | 2x4, R-13 cavity |

U-0.240 is essentially a bare stud wall; the 0.09x rows are insulated. Which physical sections are which is house knowledge you have and I cannot derive — most likely the original construction versus the later extensions.

**What to tell me:** which walls or which parts of the house are the uninsulated 248 ft². Then I tag them.

### 1.5 Which rooms sit under which ceiling insulation

Their ceilings are three assemblies: 40.4 ft² at R-11, 541.2 ft² at R-13, 965.7 ft² at R-19. Eldr resolves ceilings per room, so this is expressible once you can say which rooms fall under which.

Worth combining with 1.2 — you will be up there anyway.

---

## 2. Decisions I need from you — then I do the edit

**Several of these may already be resolved** by the basement and duct work — the Garage room naming in particular. Worth a status pass against the current model before treating any of them as outstanding.

These are all model changes I can make, but each needs a judgement call that is yours.

### 2.1 The phantom doors — **−675 BTU/hr (we are currently over)**

Eldr counts **7 doors totalling 132 ft²**; the professionals count 3 totalling 82.3 ft². Your inventory says the envelope should hold **4**: front door, porch glass door, the unidentified upstairs door, and the garage↔kitchen buffer door.

What Eldr currently finds:

| Area | Plausibly |
|---:|---|
| 33.3 ft² | the porch glass door? (theirs is 43.4 ft² — if so we have it undersized) |
| 22.8 ft² | ? |
| 20.5 ft² × 3 | standard doors — but only two should be on the envelope |
| 8.1 ft² | **not door-sized** |
| 6.4 ft² | **not door-sized** |

**Decide:** which of these are real envelope doors. The two small ones are almost certainly errors. Interior doors do not belong on the envelope at all.

Also worth settling: their two opaque doors are 21.5 ft² wood-with-storm (clearly your front door) and 17.4 ft² metal/fibreglass. Is that second one the upstairs door or the garage buffer door? They only counted two, and you have three non-glass exterior-ish doors.

### 2.2 The bricked-in basement window

If it is still drawn as glass, it is overstating loss. **Decide:** delete it, or leave it drawn and I tag it so it reads as wall.

### 2.3 The three duplicate Garage rooms — *no load impact, confusing*

`tag.py list` shows three rooms of exactly 442.8 ft² on the Garage level — two unnamed, one named `Garage`. **Decide:** delete the two unnamed ones.

### 2.4 Driveway, Porch, Walkway, Driveway Extended drawn as rooms — *reads as nonsense*

These four are outdoor paving drawn as rooms on the Garage level (986.8 / 53.2 / 49.5 / 230.1 ft²). They now show up in the per-room cooling table, which is meaningless.

**Decide:** keep them as site context and move them to a level marked `role: ignore`, or drop them from the model.

### 2.5 The three basement wall stubs with implausible heights

Heights of 0.08 ft, 0.17 ft and 3.00 ft. **Decide:** real features or leftovers.

---

## 3. Things I can do alone once 1 and 2 are answered

- **Draw the crawlspace under the Main Bed extension** — the current run reports **113.0 ft²** of conditioned floor with no level drawn beneath it, all of it Main Bed, modelled as an *assumption* rather than seen as geometry. (An earlier figure of 149.5 ft² also counted a Living room void that the report no longer flags.) Drawing it makes the *Schematic gaps* warning shrink, which is the signal it is working.
- **Draw the rest of the basement floor as rooms** — rooms cover 678 ft² of a 761 ft² footprint, so ~83 ft² is undrawn, and walls bordering undrawn space read as facing outdoors. That pulls roughly 14 interior partition segments into the envelope and inflates the wall area.
- **The two main-floor void walls** (the kitchen/bathroom void).
- **Declare the assembly variants** in `eldr-sidecar.yaml` — `exterior_wall/r0: 0.240`, `window/single: 0.900`, `window/storm: 0.570`, `ceiling/r11: 0.081`, `ceiling/r13: 0.070`, `ceiling/r19: 0.049`, `buffer_wall: 0.097`.
- **Tag the walls and rooms** with `tag.py`, once you have told me which are which.

---

## How the tagging works

Both halves of this now exist: Eldr resolves a U-value per surface, and `tag.py` writes the wall and room properties. Items 1.4 and 1.5 are blocked only on house knowledge, not on tooling.

Windows and doors you can do yourself in Sweet Home 3D — rename them in the furniture list:

```
Bedroom window [window/single]
```

A bracketed token counts only if it contains `/` and its prefix is a real category, so your ordinary naming is untouched. This is better than tooling because you can see which window you are naming.

Walls and rooms need the tool, because Sweet Home 3D's UI cannot edit custom properties and a wall has no name to type into:

```bash
python3 realms/realm-siliconsaga/sweethome3d/tag.py list hoards/refrhus/sh3d-internals
python3 realms/realm-siliconsaga/sweethome3d/tag.py set  hoards/refrhus/sh3d-internals \
    wall 7 exterior_wall/r0
python3 realms/realm-siliconsaga/sweethome3d/tag.py set  hoards/refrhus/sh3d-internals \
    room 17 ceiling/r19
```

Tags survive Sweet Home 3D's own save and `normalize.sh`. They do **not** survive redrawing the object — a redrawn wall is a new id with no properties. Eldr's *Assembly coverage* report block is the detector: if a variant's area shrinks between two runs, a tag was lost.

---

## What the remaining work buys

Per-room CFM. The whole-house total is close enough that equipment sizing barely moves now. What the remaining work buys is *per-room* accuracy — and per-room CFM is the input to Manual T, which is the argument that the far corner of the office can actually be reached, and that the south side of the 2nd floor has a load whether or not it is convenient to duct.

**The duct design does not depend on this list.** The scheme, the register schedule and the parts list are built on per-room figures good enough to size ducts, and the items above would move them by less than the biases applied on purpose. Finishing the list sharpens the *argument*; it does not unblock the *build*.
