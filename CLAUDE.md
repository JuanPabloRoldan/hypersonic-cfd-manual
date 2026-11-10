# Authoring conventions for this repository

This repo is a MkDocs (Material) site holding **a theory manual and nothing else**: one page per method or model family in `docs/reference/`, written so it can be read cold, organized like a commercial code's theory guide (the STAR-CCM+ theory guide is the model). Chapters are numbered in the order a solver is built: 1 fundamental equations, 2 entry flow physics, 3 gas models and thermochemistry, 4 turbulence, 5 boundary conditions and walls, 6 spatial discretization, 7 inviscid flux functions, 8 source terms, 9 time integration and solvers, 10 reduced equations and engineering methods, 11 rarefied flow and particle methods, 12 verification and diagnosis, 13 shock-layer radiation, then appendices. Numbers live in the `nav` labels in `mkdocs.yml` (and in `docs/reference/index.md`), not in file names, so URLs stay stable. New entry-flow physics pages join chapter 2. New chapters (material response and ablation next) are appended after the last numbered chapter, so that existing chapter numbers, which the owner's notes refer to, don't shift.

Plus `docs/glossary.md`, `docs/references.md`, the implications matrix, and one appendix page, `docs/codes/index.md` ("Codes at a glance"), which compares the production codes slot by slot and lists their primary sources.

**The course is not in this repo.** Lessons, checkpoint questions, answers, outcomes and the session log live privately in the owner's Claude project ("Reentry Numerics": `main.md`, `course/track-*.md`, `course/manual-review.md`). Don't add lesson pages, checkpoint outcomes, "taught in" links, learner progress or personal information to the site. When teaching produces a durable explanation, it goes into the theory page for that method. Don't reference course tracks ("Track 6" etc.) anywhere on the site; point to manual pages, or say "planned chapter".

**Codes are not organized as separate pages.** What a code does is recorded on the method pages, in each page's "Which codes" section, and summarized in the appendix table. Research and contrast codes (MFC, ALPACA/JAX-Fluids) appear only as alternatives or sources of extra numerics on method pages, not as subjects of their own. Link to a code with `codes/index.md#<code>` (anchors: `dplr`, `laura`, `us3d`, `fun3d`, `su2-nemo`, `eilmer`, `sparta`, `star-ccm`, `radiation-solvers`, `material-response-tools`, `mutationpp`, `mfc`, `alpaca`).

## Linking rule (the most important convention)

The first time a page mentions a method, model, term or code that has (or should have) its own page, link it with a relative link to the `.md` file, for example `[HLLC](../spatial/riemann-solvers.md#hllc)`.

If the target page doesn't exist yet, create it as an outline stub (front matter `status: outline`), give it the standard sections, and add it to `nav` in `mkdocs.yml`. One page may cover a whole family: all Riemann solvers live on `reference/spatial/riemann-solvers.md`, with one `##` section per solver so anchors work.

`mkdocs build --strict` must pass before every push; it fails on broken links and missing nav entries.

## Page status

Set in front matter and shown as an icon in the sidebar:

- no status: written.
- `status: draft`: key formulas and facts in place, some sections still to be written.
- `status: outline`: section headings and pointers only.

Whether the owner has reviewed a page is tracked in the project's `course/manual-review.md`, not on the site.

Every reference page starts with a `page-meta` block:

```markdown
<div class="page-meta" markdown>
**Chapter:** 7 Inviscid flux functions · **Depth:** [deep]
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

## Reader checks (run these on every page you add or change)

The reader has a working CFD background but reads each page cold, and stops at anything asserted without support. These twelve checks come from the questions and complaints raised in review so far; the example in brackets is the question that motivated each one. A page isn't done until it passes all that apply.

1. **Every term and symbol is defined where it first appears on the page**, in a clause, not by a link alone. ("Star states: I don't know what this means." "What is a dense gas?")
2. **Structural claims are shown, not stated.** If the text says something about eigenvalues, a Jacobian, a stencil or a limit, write the matrix, the stencil or the limit. ("How does adding species keep the eigenvalues? Show the matrices.")
3. **Every displayed equation is read back.** One sentence saying where it comes from (which balance, which assumption), then what each term does. Give a short derivation, with skipped steps named, when the derivation is the understanding.
4. **Neighbours are told apart.** When two methods, models or terms sound alike, say in one or two sentences what differs and when it matters, or give a comparison table. Text and tables must name the same set of things. ("HLL vs HLLE if both are positivity preserving?" "Why does only Roe need an entropy fix?" "The text names three models, the table has four.")
5. **"When do I need this?" has an answer**: a rule of thumb in terms of something easy to estimate (entry speed, Mach number, altitude, Knudsen, Damköhler or cell Reynolds number), plus what goes wrong, and in which direction, if it is left out.
6. **Physical results come with their causal chain**, one link per sentence, with numbers. ("Dissociation absorbs energy, so the gas is colder; at nearly the same pressure a colder gas is denser; the same mass flux then needs a thinner layer, so the standoff shrinks.")
7. **Likely misconceptions are met head on.** Where a statement collides with a reasonable prior belief, say so and resolve it. ("I thought explicit codes were faster in hypersonics." "CFL can be much greater than 1?")
8. **At least one worked example with numbers** on every method page (minmod slopes, a Roe average, a time step at a wall cell), and **costs in concrete terms** (operation counts, memory scaling, iterations to converge, with the source and test case).
9. **No dangling promises.** "Covered later" is not allowed. Link to the page and section that covers it; if none exists, create the outline stub.
10. **A figure wherever geometry, a stencil, a wave pattern, an algorithm's data flow or a trend carries the point.** If a paragraph describes a picture in words, draw the picture. Captions say what to look at.
11. **Alternatives and codes.** Each method page says what else could be used in its place and what the production codes actually do, calibrated.
12. **It renders.** No raw `$`, backslash commands or broken images on the built page; no course references ("Track 6", "lesson", "checkpoint").

Writing habits that follow from these: lead each section with the plain statement and put the formula second; one idea per paragraph; short declarative sentences; prefer a small table over a long sentence with four parallel items.

## Adding material

**A new fact, number or explanation.** Find the page that owns the topic and put it in the section the template gives it (a parameter range goes in Typical values, a failure mode in Effects on stability, a knob in In a run). Don't create a page for something that is a section of an existing family page. Then update whatever else repeats it: the six-lens table on that page, the implications matrix, the glossary entry, the codes appendix.

**A new page.** Use the template below in full. Place it in the chapter order, number it in `nav` and in `docs/reference/index.md`, and link to it from every page that already mentions the topic. Start it as `outline` (headings and pointers), move it to `draft` when How it works, one figure and one worked example are in, and remove the status when every template section is filled and the reader checks pass.

**A new figure.** Add a function to `scripts/make_figures.py`, call it from `__main__`, regenerate, and look at the PNG preview before committing. Schematics are labelled "schematic" or "not to scale". Computed curves say in the caption what was computed and from which formula. Published data are plotted exactly as published and credited in the caption.

**A number.** Give the value, the units, the source and the test case. Order-of-magnitude teaching values are labelled "illustrative". If the only source is paywalled or wasn't read in full, say what was read (abstract, table, conclusions).

**From a paper or book.** Paraphrase and cite; add the entry to `docs/references.md`. Put each result on the method page it belongs to, not on a page about the paper.

**Before pushing.** Run `mkdocs build --strict`, then `python scripts/check_render.py`. The script opens every page of the built `site/` in headless Chrome and fails on math errors, raw LaTeX, unrendered `$`, missing images, display equations wider than the text column, and course wording. It needs Playwright and Chrome; without internet access, point `LOCAL_NPM` at a directory where `npm install mathjax@3 mermaid@11` has been run (see the script's header). It is not part of CI. Look at a screenshot (`--shots DIR`) of any page with a new figure or Mermaid diagram. Commit one chapter or one topic at a time.

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

`docs/glossary.md` uses this entry format, alphabetical.

```
### <Term> (also: <aliases>)
Depth: [deep] or [feel]
Topic: <physics topic or pipeline stage>
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
python scripts/check_render.py    # rendered-page check; needs playwright + Chrome
```
