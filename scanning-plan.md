# 3D scanning → agent-usable house data — options & plan

Distilled from the 2026-06 discussion. Raw scanner notes were in `scanning.txt` (now folded in here). House ground truth: `HISTORY.md`.

## Why scan at all

The schematic was assembled without accurate ground truth: the floor plan is explicitly "not to scale", and the survey is a blurry JPEG good only for the footprint envelope. Because the levels are registered to each other, an error in the basement propagates through the whole house. A scan would give an independent geometric reference — something to trace against and overlay-check, rather than a replacement for the schematic. It does not replace the model — it becomes a *reference* you trace against and overlay-check: a tool does the math, a vision-capable agent does the interpretation.

## Structured output vs. mesh

Forget "which scanner" first. The real fork is **what the output IS**, because it changes the whole downstream pipeline:

| | **Structured** (Apple RoomPlan) | **Mesh / point cloud** (every dedicated scanner) |
|---|---|---|
| Output | walls/doors/windows as **parametric data + dimensions** | a blob of triangles / points (`.obj`/`.ply`/`.e57`) |
| Agent-usable | **immediately** — maps near-directly onto editable walls | needs an extraction step first |
| App use | could generate walls ~directly | place as a **mock-up** to trace, or slice to a floor plan |
| The catch | **simplifies everything to rectangles** (see Accuracy) | richer geometry, but "walls" must be inferred |

The irony to internalize: the cheaper dedicated scanners give better geometry but less agent-ready structure; the phone/tablet gives weaker geometry but instant structure. The "scan a house, then ask the agent questions" dream is specifically the RoomPlan path. For this house right now, mesh is plenty, because the survey plus a small extraction step already supply the "walls" understanding.

**A third category — photo-based (photogrammetry).** Most Android 3D-scan apps (and any phone without a LiDAR sensor) reconstruct geometry from ordinary photos rather than a depth sensor. They're the most accessible option — any camera works — but they produce an *unscaled* mesh: there is no metric reference, so scale must be set by hand from a known dimension, and fidelity trails both LiDAR and dedicated scanners, especially on blank/featureless walls. Useful for rough massing or a textured visual to eyeball, not for trustworthy wall dimensions. The clean way to place the three: **RoomPlan = scaled structure**, **LiDAR / dedicated scanners = scaled geometry**, **photogrammetry = unscaled geometry**. For our pipeline, a photogrammetry mesh can still be dropped in as a rough mock-up, but a survey/known-dimension scale step is mandatory before any measurement is trusted.

## Accuracy

- **iPad/iPhone LiDAR:** ~±1–3 cm horizontal in good conditions, but peer-reviewed testing shows most points land ~10 cm off the reference on *dynamic* (walking) scans, and accuracy degrades as the area grows and pose changes accumulate. Great for one small room held still; shaky as one coherent whole-house capture.
- **RoomPlan specifically** reduces the room to rectangles — sloped/non-flat walls become primitive boxes, ceilings and height variation are ignored, and it does not give wall thickness. So the 2nd floor is out (angled knee-wall/roof geometry is exactly what it can't represent), and wall thickness you'd still tape-measure (easy, and already being done).
- **Reflective surfaces** (mirrors, glass) distort LiDAR badly — mind the bathroom.
- **Dedicated structured-light (Einstar/Revopoint)** give higher raw fidelity and open meshes, but are optimized for *objects*; whole-*room* coherence depends on good tracking over featureless walls — verify room-scale tracking before trusting a big sweep.

## Scanner options — updated 2026 prices, openness, reputation

| Option | Cost (2026) | Output | Openness | Standalone? | Notes |
|---|---|---|---|---|---|
| **iPad Pro 2020 (refurb)** | **~$450** | RoomPlan **structured** + `.obj` cloud | High (instant OBJ/USDZ) | n/a (a tablet) | Cheapest path to the structured/agent dream; ±3 cm, rectangles-only, 2nd floor out. No Apple gear owned yet, so this is a real $450, not "$0." |
| **Einstar Vega** | **~$759 (seen $499 on sale)** | mesh `.obj/.stl/.ply` | High (open formats) | **Yes** (onboard 2K screen, wireless) | Plot twist: undercuts the iPad and is standalone + open. But mesh, *not* structured RoomPlan walls. Verify room-scale tracking. |
| **Revopoint Miraco** | **~$1,599** ($1,300–1,919) | mesh `.obj/.stl/.ply/…` | High (drag-and-drop, no cloud gate) | **Yes** | "Go-to prosumer standalone" reputation in 2026; handles mixed scales. The openness/scriptability sweet spot if this becomes a business. |
| **Einstar (original)** | **<$1,000** | mesh | High (OBJ/STL/PLY) | No — **tethered to a Windows PC** | Cheap, but a desktop software step sits in the loop. |
| **Leica BLK360 G1 (used)** | ~$6–8k | point cloud (e57/ptx) + obj | Medium (needs Cyclone to register, then free export) | Tripod | Survey-grade; the "if it's a business / whole-house coherent" tier. |
| **Faro Focus (used)** | ~$13k | point cloud, industry-standard | High (open formats, easy 3rd-party) | Tripod | Pro open alternative; bigger/heavier than the Leica. |

(Prices move; treat as ballpark and re-check at purchase time. Sources at bottom.)

## The agent pipeline

A scan becomes agent-usable through one small step: ingest the scan with a point-cloud library (Open3D in Python; CloudCompare for interactive cleanup), then turn it into something the model can act on. Three uses, cheapest-first:

1. **Slice → traceable floor plan.** Cut the point cloud at ~1.2 m height to get a true-to-scale 2D plan image, then drop it into the tracing workflow as a background, replacing the not-to-scale floor plan. Highest value, lowest effort — this is an established research pipeline (slice → iterative-RANSAC line detection → floor plan, >90% line accuracy).
2. **Plane-fit → wall coordinates.** RANSAC plane-fit the vertical surfaces to get exact wall positions, then overlay-check the model against reality and flag where it diverges.
3. **Structured scan → walls directly.** RoomPlan output becomes walls with minimal translation. Powerful but rectangle-limited; best for clean single-story rooms.

This is the literal substrate for the "scan a house with a tablet, then ask the agent questions" idea: the scan is the perception input, a deterministic script does the geometry, and the agent reasons over the result.

## Recommendation

**For this house, right now:** don't buy anything on the critical path. The survey already anchors the footprint core, and room-by-room is enough — the only unmeasurable spot left is the crawlspace under the kitchen (a deferred TODO).

- **If anyone can borrow a RoomPlan-capable Apple device for an afternoon:** scan just the crawlspace, export both the structured model and a point cloud/`.obj`. Then build the ingest→slice→plane-fit tool and prove the whole pipeline on the one area that can't be tape-measured. Best ROI, zero spend, unblocks a real TODO.
- **If nobody has Apple gear:** the crawlspace is tape-measurable with patience, so no purchase blocks this house. Don't buy a $450 iPad for one crawlspace.

**For the "scan-a-house-and-ask-the-agent" idea:** this is the RoomPlan path (structured output is the magic), so an Apple device is on that roadmap — but pair it with the extraction pipeline to escape RoomPlan's rectangle/no-thickness limits. If it grows toward whole-house coherent scans, that's where a Revopoint Miraco (open, standalone, ~$1.6k) or a used Faro/BLK360 earns its keep. Make "open formats" a hard requirement evaluated per-vendor, not a nice-to-have.

**The surprise to weigh:** the Einstar Vega at ~$500–759 undercuts the refurb iPad and is open + standalone — so if the goal is "best open geometry per dollar" rather than "RoomPlan's structured walls," it may be the better first hardware buy. The question deciding iPad-vs-Vega is structured-output (agent-ready walls) vs. best-open-mesh-per-dollar.

## Open questions

- Does the friend already own a RoomPlan-capable Apple device? (Changes the right-now answer entirely — borrow beats buy.)
- Is whole-house coherence needed soon, or is room-by-room fine for the foreseeable future? (Forks "phone/Vega is fine" vs. "tripod LiDAR.")
- Is "open formats" a hard requirement for the business, or negotiable? (Rules vendors in/out — especially the Leica's Cyclone-register step.)
- Android: still no mainstream phone with comparable LiDAR plus a RoomPlan-equivalent — worth a periodic re-check, but not a 2026 option. The photogrammetry apps (above) are the Android fallback: accessible but unscaled and lower-fidelity, so they don't change the recommendation.

## Sources

- Revopoint Miraco — [3DTechValley review](https://www.3dtechvalley.com/revopoint-miraco-review/), [3DSourced](https://www.3dsourced.com/3d-scanner-reviews/revopoint-miraco-review/), [Digital Camera World](https://www.digitalcameraworld.com/tech/scanners/revopoint-miraco-review-this-all-in-one-handheld-3d-scanner-makes-light-work-of-big-jobs)
- Einstar Vega — [3DTechValley review](https://www.3dtechvalley.com/einstar-vega-3d-scanner-review/), [Dynamism](https://www.dynamism.com/shining-3d/einstar-vega-3d-scanner.html), [3DPrinting.com sale](https://3dprinting.com/news/einstar-may-sales-for-makers-2026/); Einstar lineup — [3DTechValley Einstar 2](https://www.3dtechvalley.com/einstar-2-wireless-3d-scanner-review/)
- Apple RoomPlan limits — [Volpis overview](https://volpis.com/blog/apple-roomplan-overview/), [it-jim "Awful and Great"](https://www.it-jim.com/blog/roomplan-framework-by-apple/), [ScanManifold](https://www.scanmanifold.com/blog-posts/roomplan-scan-contractors)
- iPad Pro LiDAR accuracy — [ScienceDirect indoor-mapping eval](https://www.sciencedirect.com/science/article/pii/S2666165923000510), [MDPI vs industrial scanner](https://www.mdpi.com/2227-7080/9/2/25), [Tandfonline vs TLS](https://www.tandfonline.com/doi/full/10.1080/16874048.2024.2408839)
- Point-cloud → floor-plan pipeline — [ScienceDirect iterative-RANSAC](https://www.sciencedirect.com/science/article/abs/pii/S2352710224008064), [MDPI auto-2D-CAD](https://www.mdpi.com/2076-3417/10/8/2817), [HPI 2D/3D floor plans](https://hpi.de/doellner/publications/Document/matthias.trapp/GRAPP_2019_3_CR.pdf/8a3c70939dbca92c61b576331d3cfd56.html)
- Leica BLK360 G1 used — [Machinio listings](https://www.machinio.com/model/leica-blk360-g1)
