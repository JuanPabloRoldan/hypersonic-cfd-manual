# Authoring conventions for this repository

This repo is a MkDocs (Material) site that serves two purposes at once:

1. **A theory manual** (`docs/reference/`, shown as the "Theory manual" tab): one page per method or model family, written so it can be read cold, organized like a commercial code's theory guide (the STAR-CCM+ theory guide is the model). Chapters are numbered in the order a solver is built: 1 fundamental equations, 2 entry flow physics, 3 gas models and thermochemistry, 4 turbulence, 5 boundary conditions and walls, 6 spatial discretization, 7 inviscid flux functions, 8 source terms, 9 time integration and solvers, 10 reduced equations, 11 verification and diagnosis, then appendices. Numbers live in the `nav` labels in `mkdocs.yml` (and in `docs/reference/index.md`), not in file names, so URLs stay stable. New chapters (radiation, material response, Track 1 physics topics) are inserted where they belong in that order and the later numbers shifted.
2. **A course** (`docs/course/`): the teaching sequence, Tracks 0–9, with lessons that explain, connect and end in checkpoint questions.

Plus `docs/glossary.md`, `docs/references.md`, and one appendix page, `docs/codes/index.md` ("Codes at a glance"), which compares the production codes slot by slot and lists their primary sources.

Lessons teach and link out. Theory pages hold the durable explanation. When a lesson explains something at length, the theory page should hold the full version and the lesson should summarize it and link to it.

**Codes are not organized as separate pages.** What a code does is recorded on the method pages, in each page's "Which codes" section, and summarized in the appendix table. Research and contrast codes (MFC, ALPACA/JAX-Fluids) appear only as alternatives or sources of extra numerics on method pages, not as subjects of their own. Link to a code with `codes/index.md#<code>` (anchors: `dplr`, `laura`, `us3d`, `fun3d`, `su2-nemo`, `eilmer`, `sparta`, `star-ccm`, `radiation-solvers`, `material-response-tools`, `mutationpp`, `mfc`, `alpaca`).

## Linking rule (the most important convention)

The first time a page mentions a method, model, term or code that has (or should have) its own page, link it with a relative link to the `.md` file, for example `[HLLC](../spatial/riemann-solvers.md#hllc)`.

If the target page doesn't exist yet, create it as an outline stub (front matter `status: outline`), give it the standard sections, and add it to `nav` in `mkdocs.yml`. One page may cover a whole family: all Riemann solvers live on `reference/spatial/riemann-solvers.md`, with one `##` section per solver so anchors work.

`mkdocs build --strict` must pass before every push; it fails on broken links and missing nav entries.

## Page status

Set in front matter and shown as an icon in the sidebar:

- no status: written and taught.
- `status: draft`: partly written (formulas or key facts in place), lesson still pending.
- `status: outline`: section headings and pointers only.

Every reference page starts with a `page-meta` block:

```markdown
<div class="page-meta" markdown>
**Slot:** Track 0.4 flux functions · **Depth:** [deep] · **Taught in:** [Lesson 0.4](../../course/track-0/0-4-flux-functions.md)
</div>
```

## Theory page template

```markdown
# <Method or model family>

<div class="page-meta" markdown> ... </div>

## What it is
## The problem it solves
## How it works            (equations, derivations where the derivation is the understanding)
## Variants                (one ## or ### per variant, so they are linkable)
## Typical values          (explicit bullets: parameter ranges, measured costs, convergence numbers, physical values; each with its source)
## Trade-offs              (explicit bullets: what you gain, what you pay)
## Effects on stability and robustness   (explicit bullets)
## Implications            (the six-lens table, below)
## In a run                (input knobs, symptoms, what to check)
## Which codes             (who uses it and how they differ; calibrated)
## See also
## References
```

The six-lens implications table:

| Lens | Effect |
|---|---|
| Time step and cost | |
| Steady vs unsteady | |
| Accuracy (heat flux, pressure) | |
| Robustness | |
| Physics captured or lost | |
| Hardware / parallel fit | |

## Lesson template

Lessons live in `docs/course/`. Each has: the slot it anchors to, the narrative explanation (prose, with equations), links into reference pages, a contrast with MFC where it clarifies a choice, and **Checkpoint** questions. Model answers go inside collapsed `??? success "Model answer"` blocks so the page works for self-testing. Record the learner's checkpoint outcome in `docs/course/session-log.md`.

## Calibration

Separate settled results from active debate or one group's preference. Many production codes (DPLR, LAURA, US3D, FIAT) are not open, so code-specific claims get a `!!! warning "Calibration"` admonition unless backed by a cited primary source (NTRS papers, AIAA/JCP papers, user manuals). Never state a code detail more confidently than the source allows.

## Style

- Explanations ("How it works") are prose, carried by equations and drawn figures, in the spirit of the STAR-CCM+ theory guide: write the governing discrete equation, define every symbol, then explain what each term does. Derive when the derivation is the understanding.
- Practical content is **explicit bullets**, not buried in prose: typical parameter values and ranges, measured costs and convergence numbers, physical values (free-stream conditions, Mach numbers, aspect ratios), trade-offs, effects on stability and robustness, effects on run time, symptoms in a run. Each number carries its source and test case ("10 orders in under 300 iterations, Mach 15 cylinder-wedge, Wright et al. 1998").
- Every major method gets at least one figure: a schematic of the algorithm or stencil, a plot of a key function (limiter, switch, weight), or a chart of published numbers. Plots of published numbers say whose numbers they are in the caption or title.
- Examples centre on planetary entry, capsules, sample return and human spaceflight.
- Write in your own words; cite books and papers in `docs/references.md`, never reproduce their text.
- Abbreviations get hover tooltips from `includes/abbreviations.md`; add new ones there.

## Figures

Figures are generated by `scripts/make_figures.py` into `docs/assets/figures/` (SVG). Edit the script and rerun it rather than hand-editing images. Mermaid diagrams go inline in Markdown fences. Mark schematic geometry as schematic ("not to scale") and keep plotted data exactly as published. Set `FIG_PREVIEW_DIR=/some/dir` to also write PNG previews for checking.

When writing Markdown from Python, use raw strings (`r"""..."""`) so LaTeX such as `\times` and `\approx` is not turned into control characters.

## Glossary

`docs/glossary.md` uses this entry format, alphabetical. Entries whose checkpoint is still open are marked *provisional*.

```
### <Term> (also: <aliases>)
Depth: [deep] or [feel]
Slot: <Track 0 slot, physics topic, or pipeline stage>
What it is:
Problem it solves:
Implications:
In a run:
Which codes:
See also:
```

## Build locally

```bash
pip install -r requirements.txt
python scripts/make_figures.py   # only if figures changed; needs numpy + matplotlib
mkdocs serve                      # http://127.0.0.1:8000
mkdocs build --strict             # what CI runs
```
