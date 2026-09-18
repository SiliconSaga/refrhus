# Basement structure — forensic map

The basement is the house's only hard-measured level, so it's the datum everything else
re-registers to (see `HISTORY.md`). But it is **not a uniform box** — it grew in phases,
so framing, edge conditions, and the post/beam lines **stagger** by zone. Companion to
`basement-joists.md` (the joist grid + the E–W width).

## Working strategy — interior-first

Duct routing and air-handler clearances care about **interior clear space**, not the
exterior envelope. So: build the model **from the cinder inner faces inward**, nail the
**interior N–S dimension** (measured to the raw cinder face where exposed — the
east/utility side has the most bare block), and leave the exterior/edge detailing
(sill/rim/parge nuances, exact outer faces) for later or the scan. That's enough to
place ducts + size the air-handler space, and to firm up the Main floor and above.

## Three zones (west → east)

```
  N ↑         west/den        │stairs│      east/utility
   ┌────────────────────────────────────────────────────────┐
   │ ●────────●────────●  north girder ─────────●NE ↑turns N │  3 N posts, W-wall→NE
   │                                  chimney●══════●E(pocket)│  cross-beam, E side
   │     ●SW─────●s-mid  (→ stairs)                           │  SW beam, further S
   └────────────────────────────────────────────────────────┘
      W wall              ‖jst-12       ‖jst-15         E wall
                        (N-S zone-edge beams = stair sides)
```

- **West / den (carpet):** garage to the west, **kitchen crawlspace** to the north.
  **Rim joist alone** — no visible sill (paneling hides it; "doesn't feel like wood
  below").
- **Center / stairs:** **bathroom** (≈stair-width) at the **north** end, **stairs** to
  the south, **bar** under/behind mid. A **void with the main drain stack** behind the
  bathroom (NE, at the east end of the kitchen crawlspace); drain + supply penetrate the
  rim into the extended kitchen. No sill plank, but the **rim is ~2× thick** (likely
  doubled when the extension was added).
- **East / utility:** **bare foundation** floor; **electrical panel + sump in the SE
  corner**; air handler, water heater, dead furnace, laundry. **Heavy timber sill + rim**.
  **Bedroom crawlspace** to the south (tight). An **interior wall** runs under the east
  zone-edge beam.

## Perimeter framing (varies by wall / zone)

- **East/utility:** a heavy **timber sill** (~5.5″ — a 6× or built-up member, "beyond a
  4×4") on a ~2″ sloped **parge** bed, with the **rim (~1.5″) on its outer edge** and a
  small lip inboard. Heavy timber sills are normal in the *original* section of an old
  foundation.
- **West/den:** **rim alone**, no visible sill (paneling).
- **Center:** no sill plank; **rim ~2× thick** (doubled at the extension).
- **Consequence:** there is **no single block-face ↔ joist-end offset**. Measure the
  interior clear span **per zone / to the cinder face directly**. The earlier `interior =
  L − 13″` shortcut only holds where a plain 1.5″ rim/sill applies.

## Beams & posts (staggered — the phased-build signature)

- **North girder:** 3 posts, **W wall → NE post**, then **turns north** (does not reach
  the E wall).
- **East cross-beam:** **chimney → E wall**, seated in a **cinder pocket**; the east
  zone-edge beam (`joist-15`) passes **behind the chimney without bearing on it**, and
  the utility "middle joist" **dead-ends against this cross-beam**.
- **SW beam:** **SW + south-middle posts**, **stairs → W wall**, sitting **further south**
  than the east cross-beam — the two do **not** form one line.
- **Zone-edge beams (N–S, ~3.5″):** `joist-12` = den|stairs edge; `joist-15` =
  stairs|utility edge (interior wall beneath it).
- 6 posts total; exact beam-line latitudes and the 6th post still to pin.

## Open questions / scan targets

- **North-center corner** — bathroom + drain-stack void + doubled rim (pipes penetrate
  the rim into the extended kitchen). The odd part; leave loose for now.
- **Bedroom crawlspace** (S of utility) — un-enterable, peephole only; infer from the
  south-extension footprint + the single AC duct route until scanned.
- Confirm **actual joist / rim thickness** (old lumber may exceed 1.5″).
- Exact **beam-line latitudes** and the identity of the **6th post**.
- Whether the **west/den** hides a sill under the paneling.
