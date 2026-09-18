# Refrhus — Sweet Home 3D house data

A 1950s house in West Orange, NJ, modelled in Sweet Home 3D and tracked **exploded** so git can diff the geometry. The site built from this repository is at **<https://siliconsaga.github.io/refrhus/>**.

`main` holds current best knowledge of the house, including planned work. Proposed objects are named `Ducting:` and `Register:`, so the proposal is separable from the as-built by name rather than by branch. The duct design was merged as `proposal/ducts-v1`; `git diff proposal/ducts-v1^ proposal/ducts-v1` is that proposal as a single change.

## Layout

| Path | What it is |
|---|---|
| `sh3d-internals/` | The exploded `.sh3d` (a ZIP). `Home.xml` is the diffable truth — walls, rooms, levels, furniture. **Commit changes here.** |
| `Refrhus.sh3d` | The packed file you open in Sweet Home 3D. Generated, gitignored. |
| `eldr-sidecar.yaml` | Thermal assumptions [Eldr](https://github.com/SiliconSaga/eldr) reads alongside the geometry: assemblies, design conditions, infiltration. Live input. |
| `hvac/` | The professional Manual J reports and the current Eldr run. See [`hvac/index.md`](hvac/index.md). |
| `tools/` | Generators. `partslist.py` rebuilds `ducting-parts-list.md` from the model. |
| `_config.yml`, `_layouts/`, `_includes/`, `_sass/`, `_data/`, `assets/` | Jekyll site scaffolding. The documents themselves stay plain markdown. |

### The duct design

| | |
|---|---|
| [`ducting-scheme.md`](ducting-scheme.md) | **Start here.** The scheme, why it is shaped that way, the one-unit-versus-two comparison, and build details |
| [`ducting-register-schedule.md`](ducting-register-schedule.md) | Per-register airflow, duct size and face size. Hand-edited |
| [`ducting-parts-list.md`](ducting-parts-list.md) | **Generated** — run `tools/partslist.py`, do not edit |
| [`ducting-handover-plan.md`](ducting-handover-plan.md) | Modelling conventions and what remains open |
| [`ducting-model-audit.md`](ducting-model-audit.md) | What is drawn, checked against the schedule |

### The house

[`HISTORY.md`](HISTORY.md) is construction ground truth — read it before moving a wall. Measurement records are `basement-joists.md`, `basement-structure.md`, `basement-measure-sheet.md`, `chimney-measure-sheet.md` and `basement-post-details.html`. [`schematic-hitlist.md`](schematic-hitlist.md) ranks what still needs measuring by load impact. [`scanning-plan.md`](scanning-plan.md) is a parked evaluation of 3D scanning.

**Source images**, kept because the model was traced against them: `OriginalFloorPlan.png` (explicitly *not to scale*, hence the hand measuring), `OriginalPlanHVAC.png` and `LargerFloorplanMudroomHvacV2.png` (earlier HVAC concepts, superseded), and `SurveyAlone.png` (the footprint anchor).

## Pack / unpack

Scripts live in `realms/realm-siliconsaga/sweethome3d/`; run from the workspace root:

```bash
# rebuild the openable .sh3d from the exploded tree
bash realms/realm-siliconsaga/sweethome3d/pack.sh   hoards/refrhus/sh3d-internals hoards/refrhus/Refrhus.sh3d

# after editing in SH3D, re-explode and commit the diff
bash realms/realm-siliconsaga/sweethome3d/unpack.sh hoards/refrhus/Refrhus.sh3d   hoards/refrhus/sh3d-internals
```

`Home.xml` is the meaningful diff target. **A no-op open→save→unpack must diff to nothing** — `normalize.sh` enforces that by stripping volatile view state. If no-op saves start churning, a new view-state surface appeared: extend `normalize.sh` rather than hand-editing `Home.xml`.

## Regenerating

```bash
# the load report
PYTHONPATH=components/eldr components/eldr/.venv/bin/python -m eldr.cli \
  hoards/refrhus/sh3d-internals/Home.xml hoards/refrhus/eldr-sidecar.yaml

# the parts list and cost estimate
components/eldr/.venv/bin/python hoards/refrhus/tools/partslist.py
```

CI does both for you.

| Workflow | When | What |
|---|---|---|
| `loads.yml` | PR touching the model or side-car | Runs the engine on base and head, comments what moved |
| `regenerate.yml` | Push to `main` | Rebuilds the report and parts list, commits if they drifted |
| `deploy.yml` | Push to `main` | Builds the site and publishes to `gh-pages` |
| `pr-preview.yml` | Every PR | Publishes a browsable preview and a visual diff against `main` |

The load comparison is `eldr --diff`, which lives in the engine and is unit-tested there; `loads.yml` only fetches, runs and posts. **Eldr is deliberately unpinned and checked out once**, so both sides of a comparison run on the same engine — an engine change moves both sides identically and cancels out, leaving only model changes visible. Eldr has no packaging metadata yet, so it is reached via `PYTHONPATH` rather than pip-installed.

The two site workflows call reusable ones in [volundr](https://github.com/SiliconSaga/volundr), the same pair MTL Soccer uses. They replace GitHub's built-in Jekyll build, which fails silently by email; building here means a broken stylesheet fails a check on the pull request that introduced it.

## Building the site locally

CI runs Ruby 3.3, so match it:

```bash
brew install ruby@3.3
cd hoards/refrhus
PATH="/opt/homebrew/opt/ruby@3.3/bin:$PATH" bundle install
PATH="/opt/homebrew/opt/ruby@3.3/bin:$PATH" bundle exec jekyll serve
```

`Gemfile.lock` is committed, so a local build resolves to the same versions CI does. Gems vendor into `vendor/bundle` and the output lands in `_site`; both are gitignored.

**The three plugins in `_config.yml` are load-bearing.** GitHub's legacy Pages build injects `jekyll-optional-front-matter`, `jekyll-relative-links` and `jekyll-titles-from-headings` automatically; `bundle exec jekyll build` does not — the `github-pages` gem ships them but leaves them off. Without them declared, every document that has no front matter is copied out as a raw `.md` file rather than rendered, `.md` links stay unrewritten, and pages lose their titles. That is the whole site, since only `index.md` carries front matter.
