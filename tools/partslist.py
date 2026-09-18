#!/usr/bin/env python3
"""Generate the duct parts list from the model.

Run membership comes from the object names — stem plus ordinal — never from
geometry, so this needs no junction resolution. Round vs rectangular comes from
the catalogue id rather than from guessing at near-square sections.

Usage: partslist.py [Home.xml] [out.md]   (defaults are relative to this file)

Requires `defusedxml` (the only third-party dependency):
    python3 -m pip install defusedxml
or use the Eldr virtualenv, which already has it:
    components/eldr/.venv/bin/python hoards/refrhus/tools/partslist.py
"""
import math
import os
import re
import sys
from collections import defaultdict

try:
    import defusedxml.ElementTree as DET
except ImportError:
    sys.exit("partslist.py needs defusedxml: python3 -m pip install defusedxml")

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HOME = sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, "sh3d-internals", "Home.xml")
OUT = sys.argv[2] if len(sys.argv) > 2 else os.path.join(ROOT, "ducting-parts-list.md")
def IN(cm):
    """Sweet Home 3D stores every length in centimetres; this house thinks in inches."""
    return cm / 2.54

DEFAULT_MATERIAL = {"round": "dwspiral", "rect": "rect"}

root = DET.parse(HOME).getroot()
levels = {l.get("id"): l.get("name") for l in root.findall("level")}


def axis_of(f):
    """Which world axis the piece's longest in-plan dimension runs along."""
    w = IN(float(f.get("widthInPlan") or f.get("width")))
    dp = IN(float(f.get("depthInPlan") or f.get("depth")))
    h = IN(float(f.get("heightInPlan") or f.get("height")))
    ang = float(f.get("angle") or 0)
    cs, sn = abs(math.cos(ang)), abs(math.sin(ang))
    ex, ey = w * cs + dp * sn, w * sn + dp * cs
    return max((("x", ex), ("y", ey), ("z", h)), key=lambda t: t[1])[0]


ducts, regs = [], []
for f in root.iter("pieceOfFurniture"):
    nm = f.get("name") or ""
    low = nm.lower()
    is_reg = low.startswith("register:")
    if not is_reg and "duct" not in low:
        continue
    full = nm.split(":", 1)[-1].strip()
    m = re.search(r"\[(\w+)\]", full)
    tag = m.group(1) if m else None
    bare = re.sub(r"\s*\[\w+\]\s*", " ", full).strip()
    # RAW dimensions, not the in-plan box. The in-plan values are an axis-aligned
    # envelope — correct for adjacency, but for anything tilted off a right angle
    # they overstate the section (a 12in cylinder rolled 15deg reports 15in wide).
    # width/depth/height are the true part sizes whatever the rotation.
    dims = sorted((IN(float(f.get("width"))),
                   IN(float(f.get("depth"))),
                   IN(float(f.get("height")))))
    shape = "round" if "Cylinder" in (f.get("catalogId") or "") else "rect"
    lvl = levels.get(f.get("level"), "?")
    # Only an explicit FUTURE prefix counts. The `description` field carries
    # "Future possibility" on plenums and trunks that are plainly core scope,
    # and a lowercase "future" appears mid-name in runs that serve a future
    # space alongside a live one.
    future = bare.startswith("FUTURE")
    if is_reg:
        regs.append(dict(name=bare, level=lvl, face=(dims[1], dims[2]),
                         style="circular" if tag == "circular" else "louvred",
                         side="return" if "return" in bare.lower() else "supply",
                         future=future))
    else:
        # Longest dimension is the run direction; the other two are the section.
        ducts.append(dict(name=bare, stem=re.sub(r"\s+\d+$", "", bare), level=lvl,
                          shape=shape, length=dims[2], section=(dims[0], dims[1]),
                          material=tag or DEFAULT_MATERIAL[shape],
                          axis=axis_of(f), future=future,
                          ordinal=int(re.search(r"(\d+)$", bare).group(1))
                          if re.search(r"(\d+)$", bare) else 1))

# Names carry run membership AND segment order, so a collision is not cosmetic:
# two segments sharing an ordinal sort arbitrarily against each other, and the
# bend count silently loses a direction change. Fail rather than emit a
# plausible wrong number.
dupes = defaultdict(list)
for d in ducts + regs:
    dupes[d["name"]].append(d["level"])
dupes = {n: lv for n, lv in dupes.items() if len(lv) > 1}
if dupes:
    for name, lv in sorted(dupes.items()):
        print(f"  duplicate name: {name!r} on {', '.join(lv)}", file=sys.stderr)
    sys.exit(f"{len(dupes)} duplicate object name(s) — renumber before generating.")

runs = defaultdict(list)
for d in ducts:
    runs[d["stem"]].append(d)

rows = []
for stem, members in runs.items():
    members.sort(key=lambda d: d["ordinal"])
    total = sum(m["length"] for m in members)
    bends = sum(1 for a, b in zip(members, members[1:]) if a["axis"] != b["axis"])
    secs, mats, lvls = [], [], []
    for m in members:
        s = (f'{m["section"][1]:.0f}″ round' if m["shape"] == "round"
             else f'{m["section"][0]:.0f}x{m["section"][1]:.0f}')
        if s not in secs:
            secs.append(s)
        if m["material"] not in mats:
            mats.append(m["material"])
        if m["level"] not in lvls:
            lvls.append(m["level"])
    rows.append(dict(stem=stem, n=len(members), total=total, bends=bends,
                     secs=secs, mats=mats, lvls=lvls,
                     side="return" if "return" in stem.lower() else "supply",
                     future=all(m["future"] for m in members)))

# Linear feet by section + material, future excluded from the buy.
tally = defaultdict(float)
for d in ducts:
    if d["future"]:
        continue
    s = (f'{d["section"][1]:.0f}″ round' if d["shape"] == "round"
         else f'{d["section"][0]:.0f}x{d["section"][1]:.0f}')
    tally[(s, d["material"])] += d["length"]

L = []
w = L.append
w("# Duct parts list")
w("")
w("**Generated from the model.** Every figure below is read from the drawn objects — "
  "run membership from the object names, lengths and sections from the geometry, "
  "register faces from the frame objects. Regenerate it rather than editing it.")
w("")
w("**Fittings are not in this list.** No elbows, tees, takeoffs, boots, transitions or "
  "hangers are modelled, and the bend counts below are inferred from segment-to-segment "
  "direction changes rather than drawn. A parts list that silently omitted fittings would "
  "read as complete when it is not — **treat this as the straight-duct schedule and the "
  "fitting count as the contractor's to supply.** That is work they are better placed to "
  "do anyway, and asking for it is how the effective-length question gets answered.")
w("")
w("Lengths are centre-line and **do not deduct for fittings**, so they run long at every "
  "junction. Runs marked *future* are drawn but out of scope, and are excluded from the "
  "material totals.")
w("")

for side in ("supply", "return"):
    w(f"## {side.title()} runs")
    w("")
    w("| Run | Levels | Segs | Section | Material | Length | Bends |")
    w("|---|---|:-:|:-:|:-:|---:|:-:|")
    for r in sorted(rows, key=lambda r: (r["future"], r["stem"])):
        if r["side"] != side:
            continue
        fut = " *(future)*" if r["future"] else ""
        w(f'| {r["stem"]}{fut} | {", ".join(r["lvls"])} | {r["n"]} | '
          f'{" / ".join(r["secs"])} | {" / ".join(r["mats"])} | '
          f'{r["total"] / 12:.1f} ft | {r["bends"]} |')
    w("")

w("## Registers and grilles")
w("")
w("| Register | Level | Face | Style |")
w("|---|---|:-:|:-:|")
for r in sorted(regs, key=lambda r: (r["future"], r["side"], r["name"])):
    fut = " *(future)*" if r["future"] else ""
    w(f'| {r["name"]}{fut} | {r["level"]} | {r["face"][0]:.0f}x{r["face"][1]:.0f} | {r["style"]} |')
w("")

w("## Materials summary")
w("")
w("Future runs excluded. Round sizes are **airway** — confirm whether a supplier quotes "
  "inner or outer diameter on double-wall before ordering, because getting it backwards "
  "costs two inches of diameter on every round run at once.")
w("")
w("### Where the round duct comes from")
w("")
w("Double-wall spiral is fabricator-made rather than a stocked wholesale item, and "
  "two shops within reach of the house make it. Both confirmed from their own "
  "published pages; neither has been quoted.")
w("")
w("| | Location | Round capability |")
w("|---|---|---|")
w("| **[Universal Fabricating & Supply](https://www.ductfabricating.com/)** | "
  "[25 Just Rd, Fairfield NJ](https://www.google.com/maps/search/?api=1&query="
  "25+Just+Rd%2C+Fairfield%2C+NJ+07004) — roughly 8 miles | "
  "Single and double-wall spiral **3″–54″**, custom lengths to 20 ft |")
w("| **[Airside Sheet Metal](https://www.airsidesheetmetal.com/)** | "
  "[246 Brighton Rd, Andover NJ](https://www.google.com/maps/search/?api=1&query="
  "246+Brighton+Rd%2C+Andover%2C+NJ+07821) — roughly 30 miles | "
  "**4″–60″**, stocked 4″–26″, 60,000 ft² shop |")
w("")
w("Fairfield is the near one and covers every size on this job. Andover is the "
  "larger shop and the one more likely to have odd sizes on the floor.")
w("")
w("**The question to settle on the first call is inner versus outer diameter.** "
  "Everything above is sized by *airway*, and on double-wall the insulation sits "
  "inside the shell — so a supplier quoting outer diameter delivers roughly two "
  "inches less airway than the schedule assumes, on every round run at once.")
w("")
w("Two smaller things worth raising at the same time: this job totals under 100 ft "
  "of round across four diameters, which is a small order for a commercial shop and "
  "may run into a minimum; and **9″ is the least common of the four sizes** here, so "
  "it is the one most likely to be a special run rather than something on the rack.")
w("")
w("**An `oval` section is the box it must fit inside, not its airway.** A flat oval "
  "turns each corner into a semicircular end, so a run listed 14x18 carries about "
  "210 in² against the 252 the two numbers multiply to — roughly 20% less on every "
  "oval run here. The box is what is printed because the box is what has to clear the "
  "framing; size the airflow off the airway.")
w("")
w("| Section | Material | Linear feet |")
w("|---|---|---:|")
for (s, mat), ln in sorted(tally.items(), key=lambda kv: -kv[1]):
    w(f"| {s} | {mat} | {ln / 12:.1f} |")
w(f'| **Total** | | **{sum(tally.values()) / 12:.1f}** |')
w("")

live_regs = [r for r in regs if not r["future"]]
branches = [r for r in rows if "branch" in r["stem"].lower() and not r["future"]]

# --- Cost, planning grade -------------------------------------------------
# Installed $/ft bands. Broad on purpose: fabrication, access and region move
# these more than size does, and a single figure would imply precision we do
# not have. Round is double-wall insulated spiral at 5-9in; rect is shop-
# fabricated galvanised, with the large trunk sections sitting at the top.
BANDS = {"round": (12, 30), "rect": (10, 25)}
round_ft = sum(d["length"] for d in ducts if d["shape"] == "round" and not d["future"]) / 12
rect_ft = sum(d["length"] for d in ducts if d["shape"] != "round" and not d["future"]) / 12
n_sup = sum(1 for r in live_regs if r["side"] == "supply")
n_ret = sum(1 for r in live_regs if r["side"] == "return")

duct_rows = [
    ("Round duct, double-wall spiral", f"{round_ft:.0f} ft",
     round_ft * BANDS["round"][0], round_ft * BANDS["round"][1]),
    ("Rectangular and oval, fabricated", f"{rect_ft:.0f} ft",
     rect_ft * BANDS["rect"][0], rect_ft * BANDS["rect"][1]),
]
trim_rows = [
    ("Supply registers", f"{n_sup}", n_sup * 15, n_sup * 60),
    ("Return grilles", f"{n_ret}", n_ret * 25, n_ret * 100),
    ("Balancing dampers", f"{len(branches)}", len(branches) * 25, len(branches) * 60),
]
cost = duct_rows + trim_rows
# Fittings scale with the DUCT line only. Registers, grilles and dampers are
# counted items with no fittings of their own, so folding them into the base
# would inflate the allowance by whatever the trim happens to cost.
duct_lo = sum(c[2] for c in duct_rows)
duct_hi = sum(c[3] for c in duct_rows)
lo = sum(c[2] for c in cost)
hi = sum(c[3] for c in cost)

w("## Cost — planning grade only")
w("")
w("**Every figure here is a band, and the bands are wide on purpose.** Fabrication, "
  "access and region move installed duct pricing more than size does, so a single "
  "number would imply a precision this does not have. Use it to compare options "
  "against each other, not to budget.")
w("")
w("| Item | Quantity | Low | High |")
w("|---|---:|---:|---:|")
for label, qty, a, b in cost:
    w(f"| {label} | {qty} | ${a:,.0f} | ${b:,.0f} |")
w(f"| Duct only | | ${duct_lo:,.0f} | ${duct_hi:,.0f} |")
w(f"| **Subtotal — duct, trim and dampers** | | **${lo:,.0f}** | **${hi:,.0f}** |")
w("")
w("**All figures are pre-incentive.** No rebate, tax credit or utility programme is "
  "netted off anywhere in this document. Incentives change by year, by model and by "
  "jurisdiction, and a quote that quietly assumes one is a quote that cannot be "
  "compared against another.")
w("")
w("**Fittings are missing from that subtotal and they are not a rounding error.** "
  "Elbows, tees, takeoffs, boots and transitions commonly run **30–50% of a duct "
  "job's material cost**, and none of them are modelled here — so treat the straight-"
  "duct figure as roughly two thirds of the real material story.")
w("")
w("### Labour is already inside those bands")
w("")
w("The $/ft figures above are *installed*, not material-only, so labour is not a line "
  "to add — it is most of what the band's width represents. For sanity-checking a "
  "quote that separates them: duct labour alone runs roughly **$5–15 per linear foot**, "
  "and HVAC labour is **$75–150 per hour per technician**.")
w("")
w("Published estimates of labour's *share* of a duct job disagree sharply — one puts it "
  "near 22% of a whole-house replacement, another at 60%. **That spread is a signal, "
  "not noise:** it is the difference between duct run through open basement joists and "
  "duct fished through finished walls. This house is both, which is why the "
  "bands here are wide and why a walkthrough quote will beat any figure on this page.")
w("")
w("### Ducted extras, priced separately")
w("")
w("| Option | Installed | Note |")
w("|---|---|---|")
w("| Media air cleaner | **$400–1,000** | A deep pleated filter in the return. The "
  "default choice, and the one with no downside beyond filter changes |")
w("| UV treatment | **$400–800**, up to $3,500 | Coil-sterilising lamps at the low end; "
  "in-duct air treatment at the high end. Effectiveness claims vary far more than price does |")
w("| Whole-house humidifier | **$400–1,200**, up to $2,500 | Bypass or steam. Steam "
  "costs more and holds a setpoint |")
w("")
w("**A media cleaner has a real interaction with this design and the others do not.** "
  "A deep filter adds static pressure to the return side, and the return side is "
  "already this system's constraint — see the main-floor return path above. Size the "
  "filter cabinet generously and account for its pressure drop in the same breath as "
  "the return trunk, rather than adding it afterwards. **The others are additions to "
  "the system; filtration is a change to it.**")
w("")
w("### Equipment, and why the number to quote is 4 tons")
w("")
w("Manual S on the current model recommends **3.5 tons** — 40,331 BTU/hr is 3.4 "
  "tons of load. The figure worth quoting against is **4.0**, and the reason is "
  "the state of the model rather than a preference for headroom.")
w("")
w("The load calculation runs against geometry that is knowingly incomplete, and **every "
  "gap in it points the same way**:")
w("")
w("- **No grade line.** Basement walls are classed below-grade over their whole height. "
  "Taking the professionals' measured U-value alone moves the load to roughly "
  "45,600 BTU/hr — 3.8 tons.")
w("- **The second-floor roof is not drawn.** Ceiling area is modelled at 984 ft² against "
  "a professional report's 1,547 — a third of that surface is missing, and it is the "
  "hot side of the house.")
w("- **Corrections to the model have tended to raise the load, not lower it**, and "
  "every gap still open points the same way. Today's figure reads as a floor rather "
  "than a midpoint.")
w("")
w("**The sizing verdict is one to hold loosely.** 3.5 tons "
  "is what today's model says; 3.8 is what one known-missing input alone would make it; "
  "and the remaining gaps have not been priced at all. Rounding to the next tier is the "
  "cheap direction to be wrong in — an oversized heat pump with inverter turndown "
  "short-cycles far less than a single-stage unit would, while an undersized one has no "
  "remedy short of replacement.")
w("")
w("| | Installed, pre-incentive |")
w("|---|---:|")
w("| 3.5-ton cold-climate heat pump, this class | $5,000–9,000 |")
w("| **4.0-ton — the tier to quote** | **$5,500–10,500** |")
w("")
w("The Bosch IDS Ultra is the candidate on file. Treat both rows as placeholders until "
  "a dealer quotes the specific model: published pricing for this equipment comes "
  "largely from aggregator sites rather than distributors.")
w("")

# Fittings add both parts and the labour to hang them; 25-40% on the installed
# duct line is the working allowance, not the 30-50%-of-material figure.
fit_lo, fit_hi = duct_lo * 0.25, duct_hi * 0.40
eq_lo, eq_hi = 5500, 10500
ex_lo, ex_hi = 1200, 3000
tot_lo = lo + fit_lo + eq_lo + ex_lo
tot_hi = hi + fit_hi + eq_hi + ex_hi

w("## Whole-job estimate")
w("")
w("| | Low | High |")
w("|---|---:|---:|")
w(f"| Ductwork, straight runs | ${duct_lo:,.0f} | ${duct_hi:,.0f} |")
w(f"| Fittings allowance (25–40% of duct) | ${fit_lo:,.0f} | ${fit_hi:,.0f} |")
w(f"| Registers, grilles, dampers | ${lo - duct_lo:,.0f} | ${hi - duct_hi:,.0f} |")
w(f"| Equipment, 4-ton | ${eq_lo:,.0f} | ${eq_hi:,.0f} |")
w(f"| Filtration, UV, humidity | ${ex_lo:,.0f} | ${ex_hi:,.0f} |")
w(f"| **Total, pre-incentive** | **${tot_lo:,.0f}** | **${tot_hi:,.0f}** |")
w("")
w(f"**Centre of mass is around ${(tot_lo + tot_hi) / 2:,.0f}**, and the upper band is "
  "what you get if every constrained thing turns out to be the hard version — duct "
  "fished through finished walls rather than run through open joists, the kitchen "
  "cabinetry modified rather than worked around, the high-end UV rather than coil "
  "lamps. A realistic landing spot sits below the top of the range rather than at it.")
w("")
w("**Pre-incentive throughout.** Nothing here is netted against a rebate, credit or "
  "utility programme, so it can be compared against a quote line for line — and "
  "whatever incentives apply come off afterwards rather than being baked into a number "
  "nobody can reconcile.")
w("")
w("One caveat on the whole table: **the fittings allowance is the weakest number "
  "in it.** It is a percentage standing in for a count not yet made, on the one "
  "quantity this model explicitly cannot derive. It is also, not coincidentally, the "
  "same count that settles the one-unit-versus-two question — so asking for it buys an "
  "answer twice.")
w("")
w("### What this is for: one air handler or two")
w("")
w("The number that matters is not the total, it is **the delta between one unit and "
  "two**. The proposal is a second ducted handler in the **north knee-wall attic**, "
  "reached through the wall at the top of the stairs — so it is attic equipment, in a "
  "space our own model puts near 133°F on a summer design day. It is argued with on its "
  "merits in [`ducting-scheme.md`](ducting-scheme.md).")
w("")
w("On cost alone, the delta is a second indoor unit, a second filter, a second "
  "condensate path — over a finished ceiling — a second service point reached through a "
  "knee-wall hatch, and a second maintenance schedule for as long as the house stands. "
  "Against a riser that **has to be built anyway** for the main floor.")
w("")
w("**But cost is not what decides it, and neither is static pressure alone.** A north "
  "knee-wall unit does not reach the south side of those rooms, and the suggested "
  "remedy — a duct channel along the office wall — is itself a chase. Ask which "
  "registers the second unit can reach *before* asking whether one unit runs "
  "out of static pressure. The fitting counts settle the second question; only a site "
  "visit settles the first.")
w("")
w("## Counts")
w("")
w("| Item | Count |")
w("|---|---:|")
w(f'| Supply registers | {sum(1 for r in live_regs if r["side"] == "supply")} |')
w(f'| Return grilles | {sum(1 for r in live_regs if r["side"] == "return")} |')
w(f'| — of which circular | {sum(1 for r in live_regs if r["style"] == "circular")} |')
w(f"| Branch runs (one balancing damper each) | {len(branches)} |")
w(f'| Inferred direction changes | {sum(r["bends"] for r in rows if not r["future"])} |')
w("")
w("**Every takeoff wants a balancing damper, whatever the balance calculation says.** A branch "
  "without one cannot be adjusted after the fact, and the first season in a house is when "
  "the balance is discovered.")
w("")

open(OUT, "w", encoding="utf-8").write("\n".join(L) + "\n")
print(f"wrote {OUT}  ({len(rows)} runs, {len(regs)} registers, "
      f"{sum(tally.values()) / 12:.0f} ft of duct)")
