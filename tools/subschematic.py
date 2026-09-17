#!/usr/bin/env python3
"""Generate cropped SVG sub-schematics from the model.

A sub-schematic is a close-up of one region — the plenum area, a trunk
junction, the utility cabinet — drawn from the same `Home.xml` the parts list
reads, so it cannot drift from the model the way a hand-drawn diagram does.

WHERE A VIEW'S BOUNDS COME FROM
-------------------------------
From an object drawn in Sweet Home 3D, named `View: <title> [<projection>]` —
the same naming convention `Ducting:` and `Register:` already use. Make it a
box, set it invisible, and drag it over the region you want. The crop then
follows the model: move the plenum and re-drag the box, and every diagram
re-cuts itself. Declaring coordinates in a YAML file would need hand
maintenance against geometry that moves, and would have to be edited blind.

    View: Plenum area [plan]
    View: Utility cabinet [section-ns]

The projection tag is optional and defaults to `plan`:

    plan         looking down   — x across, y down the page
    section-ns   looking west   — y across, z up the page
    section-ew   looking north  — x across, z up the page

HOW BIG TO DRAW THE BOX
-----------------------
**Roughly 6–10 ft across.** The plenum view below is 8.7 x 7.6 ft and holds 28
objects, which is the busy end of readable; under about 4 ft you have zoomed
past the context that makes the close-up worth having. Aim for one junction
and everything that lands on it.

**All three dimensions are read, in both projections.** The two the drawing
shows are the crop. The third is a slice: it decides what is near enough to
belong in the picture, and without it a section of the plenum collects every
duct anywhere along the house at the same height.

So for a **plan** box, the height picks the levels — sitting on the Basement
and stopping below the ceiling draws the basement alone, while drawing it up
through the slab picks up the transition level and the floor above. For a
**section** box, the depth is the slice thickness; 1–2 ft cuts a junction and
its takeoffs without the far side of the room piling up behind them. A section
box also has to be as *tall* as the elevation you want to show, which for the
three-level cabinet means a box that spans levels — set its height directly
rather than expecting the level to bound it.

Set the box invisible so it never renders in 3D. It is read out of `Home.xml`
either way.

`--around` is the escape hatch for a region with no box drawn yet: it derives
bounds from every object whose name contains the given text, plus padding.

Usage:
    subschematic.py                          # every View: object in the model
    subschematic.py --around "plenum" --title "Plenum area"
    subschematic.py --list                   # what the model defines

Requires `defusedxml`:
    components/eldr/.venv/bin/python hoards/refrhus/tools/subschematic.py
"""
import argparse
import math
import os
import re
import sys

try:
    import defusedxml.ElementTree as DET
except ImportError:
    sys.exit("subschematic.py needs defusedxml: python3 -m pip install defusedxml")

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HOME = os.path.join(ROOT, "sh3d-internals", "Home.xml")
OUTDIR = os.path.join(ROOT, "assets", "schematics")

PROJECTIONS = ("plan", "section-ns", "section-ew")

# Sweet Home 3D's own convention for this model: green supply, yellow return.
# These are only the fallback — a piece's `color` attribute wins, so a drawing
# matches what the owner sees on screen rather than a second scheme they have
# to learn. Both are bright enough to vanish against a white page, which is
# what the currentColor halo under every outline is for.
SUPPLY = "#28f200"
RETURN = "#fefb00"
FUTURE = "#8a8a8a"


def hexcolour(raw):
    """Sweet Home 3D stores colour as ARGB hex; SVG wants RGB."""
    if not raw:
        return None
    h = raw.strip().lstrip("#")
    if len(h) == 8:
        h = h[2:]
    return f"#{h.lower()}" if len(h) == 6 else None


def luma(hexstr):
    r, g, b = (int(hexstr[i:i + 2], 16) / 255 for i in (1, 3, 5))
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def IN(cm):
    """Sweet Home 3D stores every length in centimetres; this house thinks in inches."""
    return cm / 2.54


def fnum(el, attr, default=None):
    v = el.get(attr)
    return float(v) if v is not None else default


# ---------------------------------------------------------------- model read

def load(path):
    root = DET.parse(path).getroot()
    levels = {}
    for el in root.findall("level"):
        levels[el.get("id")] = {
            "name": el.get("name"),
            "elevation": IN(fnum(el, "elevation", 0.0)),
            "height": IN(fnum(el, "height", 0.0)),
        }
    return root, levels


def footprint(el):
    """The piece's in-plan rectangle as four (x, y) corners, in inches.

    widthInPlan/depthInPlan are Sweet Home 3D's own post-pitch/roll envelope
    and are only written when they differ from the raw dimensions, so falling
    back to width/depth is correct rather than approximate. `angle` then spins
    that envelope in plan, which is why the corners are computed rather than
    read off an axis-aligned box.
    """
    w = IN(fnum(el, "widthInPlan") or fnum(el, "width"))
    d = IN(fnum(el, "depthInPlan") or fnum(el, "depth"))
    cx, cy = IN(fnum(el, "x", 0.0)), IN(fnum(el, "y", 0.0))
    a = fnum(el, "angle", 0.0)
    cs, sn = math.cos(a), math.sin(a)
    return [(cx + ex * cs - ey * sn, cy + ex * sn + ey * cs)
            for ex, ey in ((-w / 2, -d / 2), (w / 2, -d / 2),
                           (w / 2, d / 2), (-w / 2, d / 2))]


def zrange(el, levels):
    """Absolute floor and ceiling of the piece, in inches above level zero.

    `elevation` is measured from its own level's floor to the bottom of the
    in-plan box — not to the bottom of the part — which is the same trap that
    made an earlier connectivity reader wrong by tens of inches.
    """
    h = IN(fnum(el, "heightInPlan") or fnum(el, "height"))
    base = levels.get(el.get("level"), {}).get("elevation", 0.0)
    z0 = base + IN(fnum(el, "elevation", 0.0))
    return z0, z0 + h


def pieces(root, levels):
    out = []
    for el in root.iter("pieceOfFurniture"):
        nm = (el.get("name") or "").strip()
        if not nm:
            continue
        low = nm.lower()
        if low.startswith("view:"):
            kind = "view"
        elif low.startswith("register:"):
            kind = "register"
        elif "duct" in low:
            kind = "duct"
        else:
            continue
        body = nm.split(":", 1)[-1].strip() if ":" in nm else nm
        m = re.search(r"\[([\w-]+)\]", body)
        tag = m.group(1) if m else None
        bare = re.sub(r"\s*\[[\w-]+\]\s*", " ", body).strip()
        z0, z1 = zrange(el, levels)
        side = "return" if "return" in bare.lower() else "supply"
        out.append({
            "kind": kind,
            "name": bare,
            "tag": tag,
            "level": levels.get(el.get("level"), {}).get("name", "?"),
            "corners": footprint(el),
            "z0": z0, "z1": z1,
            "future": bare.startswith("FUTURE"),
            "side": side,
            "colour": hexcolour(el.get("color")) or (RETURN if side == "return"
                                                     else SUPPLY),
        })
    return out


def walls(root, levels):
    out = []
    for el in root.iter("wall"):
        lvl = levels.get(el.get("level"), {})
        out.append({
            "level": lvl.get("name", "?"),
            "x0": IN(fnum(el, "xStart", 0.0)), "y0": IN(fnum(el, "yStart", 0.0)),
            "x1": IN(fnum(el, "xEnd", 0.0)), "y1": IN(fnum(el, "yEnd", 0.0)),
            "t": IN(fnum(el, "thickness", 10.0)),
            "z0": lvl.get("elevation", 0.0),
            "z1": lvl.get("elevation", 0.0) + IN(fnum(el, "height", 0.0)),
        })
    return out


# --------------------------------------------------------------- projection

def project(pt3, proj):
    x, y, z = pt3
    if proj == "plan":
        return x, y            # y already runs down the page in both frames
    if proj == "section-ns":
        return y, -z           # looking west: north to the left, up is up
    return x, -z               # section-ew, looking north


def box3_of(item):
    """Axis-aligned world extent, (x0, y0, z0, x1, y1, z1), in inches."""
    xs = [c[0] for c in item["corners"]]
    ys = [c[1] for c in item["corners"]]
    return (min(xs), min(ys), item["z0"], max(xs), max(ys), item["z1"])


def crop2(b3, proj):
    """The two drawn axes of a 3D box, in page coordinates."""
    x0, y0, z0, x1, y1, z1 = b3
    if proj == "plan":
        return x0, y0, x1, y1
    if proj == "section-ns":
        return y0, -z1, y1, -z0
    return x0, -z1, x1, -z0


def depth2(b3, proj):
    """The axis running into the page — the one the drawing cannot show.

    A section is a slice, not a projection of everything behind it. Without
    this the section of a plenum collects every duct anywhere along the house
    at the same height, which is how the first attempt came out as mush.
    """
    x0, y0, z0, x1, y1, z1 = b3
    if proj == "plan":
        return z0, z1
    if proj == "section-ns":
        return x0, x1
    return y0, y1


def box_of(item, proj):
    """Axis-aligned extent of one item in the chosen projection."""
    return crop2(box3_of(item), proj)


def poly_of(item, proj):
    """Drawable outline: the true rotated rectangle in plan, the box in section."""
    if proj == "plan":
        return list(item["corners"])
    a0, b0, a1, b1 = box_of(item, proj)
    return [(a0, b0), (a1, b0), (a1, b1), (a0, b1)]


def overlaps(box, crop):
    return not (box[2] < crop[0] or box[0] > crop[2]
                or box[3] < crop[1] or box[1] > crop[3])


# ------------------------------------------------------------------- render

def esc(s):
    return (s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))


def render(title, proj, crop, items, wall_segs, scale=3.2, pad=26):
    a0, b0, a1, b1 = crop
    W = (a1 - a0) * scale + pad * 2
    H = (b1 - b0) * scale + pad * 2 + 30

    def P(a, b):
        return (a - a0) * scale + pad, (b - b0) * scale + pad

    # Walls and ducts run past the crop by design — clip rather than let them
    # bleed into the margin, which would read as the drawing being wrong.
    fx, fy = pad - 4, pad - 4
    fw, fh = (a1 - a0) * scale + 8, (b1 - b0) * scale + 8
    cid = "crop-" + re.sub(r"[^a-z0-9]+", "", title.lower())[:16]

    L = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W:.0f} {H:.0f}" '
         f'role="img" aria-label="{esc(title)}" '
         f'style="max-width:100%;height:auto;color:currentColor">']
    L.append(f'<defs><clipPath id="{cid}"><rect x="{fx:.1f}" y="{fy:.1f}" '
             f'width="{fw:.1f}" height="{fh:.1f}"/></clipPath></defs>')
    L.append(f'<g clip-path="url(#{cid})" fill="none" stroke="currentColor" '
             f'stroke-linejoin="round">')

    # Walls first, so ductwork reads on top of them.
    for w in wall_segs:
        if proj == "plan":
            xa, ya = P(w["x0"], w["y0"])
            xb, yb = P(w["x1"], w["y1"])
            L.append(f'<line x1="{xa:.1f}" y1="{ya:.1f}" x2="{xb:.1f}" y2="{yb:.1f}" '
                     f'stroke-width="{max(1.5, w["t"] * scale):.1f}" opacity="0.18"/>')
        else:
            across = (w["y0"], w["y1"]) if proj == "section-ns" else (w["x0"], w["x1"])
            xa, ya = P(min(across), -w["z1"])
            xb, yb = P(max(across), -w["z0"])
            L.append(f'<rect x="{xa:.1f}" y="{ya:.1f}" width="{xb - xa:.1f}" '
                     f'height="{yb - ya:.1f}" opacity="0.12" fill="currentColor" '
                     f'stroke="none"/>')

    labels = []
    for it in items:
        pts = " ".join(f"{P(a, b)[0]:.1f},{P(a, b)[1]:.1f}" for a, b in poly_of(it, proj))
        if it["future"]:
            colour, dash, op = FUTURE, ' stroke-dasharray="4 3"', 0.10
        else:
            colour = it["colour"]
            dash, op = "", (0.62 if it["kind"] == "register" else 0.22)
        # Model colours are picked to stand out in Sweet Home 3D's own plan
        # view, which has a fixed pale ground. A halo of the page's own
        # foreground under each outline keeps a pure yellow duct visible on
        # white without repainting it into some other colour.
        L.append(f'<polygon points="{pts}" fill="none" stroke="currentColor" '
                 f'stroke-width="2.6" opacity="0.28"{dash}/>')
        L.append(f'<polygon points="{pts}" fill="{colour}" fill-opacity="{op}" '
                 f'stroke="{colour}" stroke-width="1.4"{dash}/>')
        bx = box_of(it, proj)
        ca, cb = P((bx[0] + bx[2]) / 2, (bx[1] + bx[3]) / 2)
        labels.append((ca, cb, it, colour))

    L.append("</g>")
    L.append(f'<rect x="{fx:.1f}" y="{fy:.1f}" width="{fw:.1f}" height="{fh:.1f}" '
             f'fill="none" stroke="currentColor" stroke-width="1" opacity="0.3"/>')

    # Labels last so nothing overdraws them, and numbered rather than named:
    # the names here run to sixty characters and the key carries them instead.
    # Two corrections before drawing: a piece that straddles the edge has its
    # centroid outside the frame, and a congested junction stacks several
    # centroids on the same point. Both produce a drawing that is technically
    # correct and unreadable.
    R = 7.5
    placed = []
    for ca, cb, it, colour in labels:
        ca = min(max(ca, fx + R), fx + fw - R)
        cb = min(max(cb, fy + R), fy + fh - R)
        for _ in range(60):
            clash = next((p for p in placed
                          if (p[0] - ca) ** 2 + (p[1] - cb) ** 2 < (2 * R + 1) ** 2),
                         None)
            if clash is None:
                break
            dx, dy = ca - clash[0], cb - clash[1]
            d = math.hypot(dx, dy) or 1.0
            if d < 0.01:            # exactly coincident — pick a direction
                dx, dy, d = 0.0, 1.0, 1.0
            ca += dx / d * (2 * R + 1 - d + 0.5)
            cb += dy / d * (2 * R + 1 - d + 0.5)
            ca = min(max(ca, fx + R), fx + fw - R)
            cb = min(max(cb, fy + R), fy + fh - R)
        placed.append((ca, cb))

    L.append('<g font-family="ui-sans-serif,system-ui,sans-serif" font-size="11" '
             'text-anchor="middle" fill="currentColor">')
    for i, ((ca, cb), (_, _, it, colour)) in enumerate(zip(placed, labels), 1):
        # The digit has to read on whatever the model painted the duct, and
        # the model's yellow takes black where its green takes white.
        ink = "#111" if luma(colour) > 0.55 else "#fff"
        L.append(f'<circle cx="{ca:.1f}" cy="{cb:.1f}" r="{R}" fill="{colour}" '
                 f'stroke="currentColor" stroke-width="1.2" stroke-opacity="0.55"/>')
        L.append(f'<text x="{ca:.1f}" y="{cb + 3.6:.1f}" fill="{ink}" '
                 f'font-size="10" font-weight="700">{i}</text>')

    # Scale bar, in whole feet, sized to roughly a fifth of the drawing.
    feet = max(1, round(((a1 - a0) / 12) / 5))
    barw = feet * 12 * scale
    bx, by = pad, H - 14
    L.append(f'<line x1="{bx:.1f}" y1="{by:.1f}" x2="{bx + barw:.1f}" y2="{by:.1f}" '
             f'stroke="currentColor" stroke-width="1.5"/>')
    L.append(f'<text x="{bx + barw / 2:.1f}" y="{by - 5:.1f}" font-size="10" '
             f'opacity="0.75">{feet} ft</text>')
    if proj == "plan":
        L.append(f'<text x="{W - pad:.1f}" y="{by:.1f}" font-size="10" '
                 f'text-anchor="end" opacity="0.75">north ↑</text>')
    L.append("</g></svg>")
    return "\n".join(L), labels


# --------------------------------------------------------------------- main

def collect(b3, all_items, all_walls, proj, keep_levels=None):
    """Everything inside the view box, tested in all three axes.

    Both drawn axes are cropped, and so is the axis running into the page —
    the box is a volume, not a window. In plan, level names do that third test
    better than raw elevations do, because a level is the unit a reader thinks
    in and a duct's z can straddle two of them.
    """
    crop = crop2(b3, proj)
    d0, d1 = depth2(b3, proj)

    items = []
    for it in all_items:
        if it["kind"] == "view":
            continue
        if not overlaps(box_of(it, proj), crop):
            continue
        if proj == "plan":
            if keep_levels and it["level"] not in keep_levels:
                continue
        else:
            e0, e1 = depth2(box3_of(it), proj)
            if e1 < d0 or e0 > d1:
                continue
        items.append(it)

    ws = []
    for w in all_walls:
        if proj == "plan":
            if keep_levels and w["level"] not in keep_levels:
                continue
            b = (min(w["x0"], w["x1"]), min(w["y0"], w["y1"]),
                 max(w["x0"], w["x1"]), max(w["y0"], w["y1"]))
        else:
            across = (w["y0"], w["y1"]) if proj == "section-ns" else (w["x0"], w["x1"])
            into = (w["x0"], w["x1"]) if proj == "section-ns" else (w["y0"], w["y1"])
            if max(into) < d0 or min(into) > d1:
                continue
            b = (min(across), -w["z1"], max(across), -w["z0"])
        if overlaps(b, crop):
            ws.append(w)
    return items, ws


def explain(view, all_items, all_walls, levels):
    """Say what a view box covers, in the terms the box is drawn in.

    A box in Sweet Home 3D is invisible by design and its extent is hard to
    judge on screen against ducts it overlaps, so the question "does this
    actually contain the junction?" is not answerable in the app. This answers
    it from the file, and reports the grow-by figures needed to hold the
    partially-caught objects whole.
    """
    b3 = box3_of(view)
    x0, y0, z0, x1, y1, z1 = b3
    proj = view["tag"] if view["tag"] in PROJECTIONS else "plan"

    print(f"View: {view['name']}  [{proj}]   drawn on {view['level']}")
    print(f"  {(x1 - x0) / 12:.1f} ft E-W  x  {(y1 - y0) / 12:.1f} ft N-S  x  "
          f"{(z1 - z0) / 12:.1f} ft tall")
    print(f"  x {x0:.0f}-{x1:.0f}in   y {y0:.0f}-{y1:.0f}in   z {z0:.0f}-{z1:.0f}in")

    spanned = [lv["name"] for lv in levels.values()
               if lv["elevation"] < z1 and lv["elevation"] + lv["height"] > z0]
    print(f"  levels in view: {', '.join(spanned) or '(none)'}")

    d0, d1 = depth2(b3, proj)
    axis = {"plan": "z", "section-ns": "x", "section-ew": "y"}[proj]
    print(f"  slice depth: {(d1 - d0) / 12:.1f} ft along {axis} "
          f"(the axis the drawing cannot show)")

    items, ws = collect(b3, all_items, all_walls, proj, spanned)
    print(f"  drawn: {len(items)} objects, {len(ws)} walls\n")

    if not items:
        print("  Nothing inside the box.\n")
        return

    # How much of each caught object is inside, and what it would take to hold
    # it whole. Reported per object because "grow it a bit" is not actionable.
    need = [0.0, 0.0, 0.0, 0.0]          # -x, -y, +x, +y, in inches
    whole = 0
    print(f"  {'':<4}{'object':<54}{'inside':>8}")
    for it in sorted(items, key=lambda i: i["name"]):
        e = box3_of(it)
        ox = max(0.0, min(e[3], x1) - max(e[0], x0))
        oy = max(0.0, min(e[4], y1) - max(e[1], y0))
        frac = min(ox / max(0.1, e[3] - e[0]), oy / max(0.1, e[4] - e[1]))
        if frac > 0.98:
            whole += 1
            mark = "full"
        else:
            mark = f"{frac * 100:.0f}%"
            need[0] = max(need[0], x0 - e[0])
            need[1] = max(need[1], y0 - e[1])
            need[2] = max(need[2], e[3] - x1)
            need[3] = max(need[3], e[4] - y1)
        print(f"  {'[' + it['side'][:3] + ']':<4}{it['name']:<54}{mark:>8}")

    print(f"\n  {whole} of {len(items)} drawn whole.")
    if any(n > 0.5 for n in need):
        print("  To hold every caught object whole, grow the box by:")
        for label, n in zip(("west (-x)", "north (-y)", "east (+x)", "south (+y)"),
                            need):
            if n > 0.5:
                print(f"    {label:<12} {n:6.0f} in  ({n / 12:.1f} ft)")
        print(f"  Which would make it {(x1 - x0 + need[0] + need[2]) / 12:.1f} x "
              f"{(y1 - y0 + need[1] + need[3]) / 12:.1f} ft.")
    print()


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--home", default=HOME)
    ap.add_argument("--outdir", default=OUTDIR)
    ap.add_argument("--around", help="derive bounds from objects matching this text")
    ap.add_argument("--title", help="title, required with --around")
    ap.add_argument("--projection", default="plan", choices=PROJECTIONS)
    ap.add_argument("--pad-in", type=float, default=18.0,
                    help="inches of margin around --around bounds")
    ap.add_argument("--levels", help="comma-separated level names to draw in plan; "
                                     "defaults to the levels the box's height spans")
    ap.add_argument("--list", action="store_true", help="list View: objects and exit")
    ap.add_argument("--explain", action="store_true",
                    help="report what each view covers — size, levels, and how "
                         "much of each object falls inside — and how far the box "
                         "would have to grow to hold them whole")
    args = ap.parse_args()

    root, levels = load(args.home)
    all_items = pieces(root, levels)
    all_walls = walls(root, levels)
    views = [it for it in all_items if it["kind"] == "view"]

    if args.list:
        if not views:
            print("No View: objects in the model.")
            print("Draw a box in Sweet Home 3D named e.g. 'View: Plenum area [plan]',")
            print("set it invisible, and drag it over the region you want.")
        for v in views:
            print(f"  {v['name']}  [{v['tag'] or 'plan'}]  on {v['level']}")
        return

    if args.explain:
        if not views:
            sys.exit("no View: objects in the model — nothing to explain")
        for v in views:
            explain(v, all_items, all_walls, levels)
        return

    jobs = []
    if args.around:
        if not args.title:
            sys.exit("--around needs --title")
        hits = [it for it in all_items
                if it["kind"] != "view" and args.around.lower() in it["name"].lower()]
        if not hits:
            sys.exit(f"nothing matches {args.around!r}")
        boxes = [box3_of(h) for h in hits]
        p = args.pad_in
        b3 = (min(b[0] for b in boxes) - p, min(b[1] for b in boxes) - p,
              min(b[2] for b in boxes) - p,
              max(b[3] for b in boxes) + p, max(b[4] for b in boxes) + p,
              max(b[5] for b in boxes) + p)
        jobs.append((args.title, hits[0]["level"], args.projection, b3))
        print(f"derived bounds from {len(hits)} object(s) matching {args.around!r}")
    else:
        if not views:
            sys.exit("no View: objects in the model — use --around, or see --list")
        for v in views:
            proj = v["tag"] if v["tag"] in PROJECTIONS else "plan"
            jobs.append((v["name"], v["level"], proj, box3_of(v)))

    explicit = [s.strip() for s in args.levels.split(",")] if args.levels else None

    def levels_spanned(b3, own):
        """Which levels a plan view should draw, from how tall the box is.

        A box sitting on the Basement and stopping below the ceiling draws the
        basement alone; one drawn up through the slab picks up the transition
        level and the floor above as well. That makes the box's height mean
        something in plan, not only in section, so there is one rule to
        explain rather than two.
        """
        z0, z1 = b3[2], b3[5]
        hit = [lv["name"] for lv in levels.values()
               if lv["elevation"] < z1 and lv["elevation"] + lv["height"] > z0]
        return hit or [own]

    os.makedirs(args.outdir, exist_ok=True)
    for title, level, proj, b3 in jobs:
        keep = explicit or levels_spanned(b3, level)
        items, ws = collect(b3, all_items, all_walls, proj, keep)
        if not items:
            print(f"  {title}: nothing inside the box — skipped")
            continue
        svg, labels = render(title, proj, crop2(b3, proj), items, ws)
        slug = re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")
        path = os.path.join(args.outdir, f"{slug}-{proj}.svg")
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(svg + "\n")
        # The numbers on the drawing are meaningless without this, so it is
        # written next to the SVG rather than left to be transcribed by hand.
        key = [f"| # | Run | Side | Level |", "|--:|---|:-:|---|"]
        for i, (_, _, it, _) in enumerate(labels, 1):
            side = "future" if it["future"] else it["side"]
            key.append(f"| {i} | {it['name']} | {side} | {it['level']} |")
        keypath = os.path.join(args.outdir, f"{slug}-{proj}.key.md")
        with open(keypath, "w", encoding="utf-8") as fh:
            fh.write("\n".join(key) + "\n")

        print(f"wrote {os.path.relpath(path, ROOT)}  "
              f"({len(items)} objects, {len(ws)} walls, {proj})")
        print(f"wrote {os.path.relpath(keypath, ROOT)}")


if __name__ == "__main__":
    main()
