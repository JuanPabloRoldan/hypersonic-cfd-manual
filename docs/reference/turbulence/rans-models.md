---
status: outline
---

# RANS turbulence models

<div class="page-meta" markdown>
**Chapter:** 4 Turbulence · **Depth:** [feel]
</div>

## What it is

The family of closures for the Reynolds (Favre)-averaged equations used in steady and unsteady RANS: algebraic (zero-equation) models, one-equation models, two-equation models, and Reynolds-stress and explicit algebraic stress models. All but the last family use the **Boussinesq eddy-viscosity hypothesis**, $-\overline{\rho u_i''u_j''} = 2\mu_t\big(\tilde S_{ij} - \tfrac13\tilde S_{kk}\delta_{ij}\big) - \tfrac23\bar\rho k\,\delta_{ij}$, where $\mu_t$ is the eddy viscosity, $\tilde S_{ij}$ the mean strain-rate tensor and $k$ the turbulent kinetic energy; the models differ in how they compute $\mu_t$.

## The problem it solves

At flight Reynolds numbers, resolving the turbulence is unaffordable ([cost scaling](scale-resolving.md#resolution-requirements)), so turbulent heating and skin friction for TPS design come from RANS. This page builds the model families up one at a time so each one's assumptions, and therefore its failure modes on entry vehicles, are visible. The hypersonic-specific corrections (cold walls, compressibility, turbulent heat flux) are on [turbulence modeling for hypersonic boundary layers](../physics/turbulence-modeling.md).

## How it works

*(Outline. Planned sections, with what each will establish.)*

### The eddy-viscosity hypothesis and its limits

- Where Boussinesq comes from (analogy with molecular viscosity), what it assumes (stress aligned with strain, local equilibrium), and the flows where that fails: strong curvature and rotation, sudden strain (shocks), separation, secondary flows.
- Realizability: why $\mu_t$ from large strain can give negative normal stresses, and the limiters that prevent it.

### Algebraic (zero-equation) models

- Mixing length, Cebeci–Smith (two-layer, needs boundary-layer edge), Baldwin–Lomax (edge found from vorticity, no edge search).
- Why they were the historical workhorse of reentry codes, and why they fail in separated flows and entropy layers where an "edge" is ill defined.

### One-equation models

- Spalart–Allmaras: one transport equation for a working variable $\tilde\nu$ (production, destruction with wall distance, diffusion); trip terms.
- Variants relevant to hypersonics: negative-$\tilde\nu$ (SA-neg) for robustness, rotation/curvature correction, compressibility and density corrections (Catris–Aupoix), strain-adaptive formulation that limits production at shocks (Rung et al. 2003; see the flare example on [SWBLI](../physics/shock-boundary-layer-interaction.md#trade-offs)). Naming follows NASA's Turbulence Modeling Resource.
- Baldwin–Barth as a historical neighbour.

### Two-equation models

- $k$–$\varepsilon$ (Launder–Spalding): low-Reynolds-number damping functions needed to integrate to the wall; the **stagnation-point anomaly** (excess $k$ produced at a stagnation point) and its fixes (Kato–Launder, Durbin's realizability limit) — directly relevant to capsule forebodies.
- $k$–$\omega$ (Wilcox 1988, 2006/2008 with stress limiter and cross-diffusion): integrates to the wall without damping functions; sensitivity to free-stream $\omega$.
- Menter BSL and SST: blending $k$–$\omega$ near the wall with $k$–$\varepsilon$ away from it, the shear-stress limiter ($a_1$) that improves adverse-pressure-gradient behaviour; SST-2003 and vorticity-production variants.
- Wall and free-stream boundary conditions for $k$, $\omega$, $\varepsilon$ and $\tilde\nu$, and how turbulence quantities decay or jump across the bow shock.

### Reynolds-stress and algebraic stress models

- Second-moment closures (LRR, SSG, SSG/LRR-$\omega$): six stress equations plus a length-scale equation; what they capture (anisotropy, curvature, history) and what they cost (seven equations, stiffness, robustness).
- Explicit algebraic Reynolds-stress models (Wallin–Johansson): anisotropy at two-equation cost.
- Whether either has a track record on hypersonic heating (to be checked in Roy & Blottner 2006 and later assessments).

### Production at shocks

- Why strain-based production explodes across a captured shock; production limiters and shock-unsteadiness corrections (Sinha, Mahesh & Candler); link to the [SWBLI evidence](../physics/shock-boundary-layer-interaction.md#trade-offs).

### Numerics of RANS equations

- Stiff, nonlinear source terms; positivity of $k$, $\omega$, $\tilde\nu$; implicit treatment loosely or fully coupled with the flow equations; first-order upwinding of turbulence convection as common practice ([implicit methods](../time/implicit-methods.md), [stiff sources](../sources/stiff-sources.md)).

## Variants

### Algebraic models

Cebeci–Smith, Baldwin–Lomax (above).

### Spalart–Allmaras {#spalart-allmaras}

Baseline and the variants above.

### k–epsilon {#k-epsilon}

Standard, low-Reynolds-number, realizable.

### k–omega and SST {#k-omega-and-sst}

Wilcox 1988/2006, Menter BSL/SST, SST-2003.

### Reynolds-stress and EARSM

LRR, SSG, SSG/LRR-$\omega$, Wallin–Johansson EARSM.

Comparison table to build: equations solved, wall treatment, cost per cell, behaviour at stagnation points, shocks, separation, and cold walls.

## Typical values

To be sourced: model constants (from the original papers and NASA's Turbulence Modeling Resource); recommended free-stream values for $\tilde\nu$, $k$, $\omega$; first-cell $y^+$ needed for each model; published hypersonic heating errors by model (Roy & Blottner 2006).

## Trade-offs

To be written: algebraic (no extra equations, no separation) vs one-equation (robust, wall-distance dependent) vs two-equation (better in pressure gradients, more stiffness, stagnation anomaly) vs Reynolds-stress (anisotropy, cost and robustness).

## Effects on stability and robustness

To be written: positivity failures, stiffness of near-wall destruction terms, limit cycles in separated regions, sensitivity to free-stream turbulence values.

## Implications

| Lens | Effect |
|---|---|
| Time step and cost | 0, 1, 2 or 7 extra equations per cell; stiff sources favour implicit treatment. |
| Steady vs unsteady | Steady by construction; URANS only where the unsteadiness is far slower than the turbulence. |
| Accuracy (heat flux, pressure) | Sets turbulent heating; model spread on separated and cold-wall flows is large. |
| Robustness | Positivity and stiffness; production at shocks. |
| Physics captured or lost | No unsteadiness, no transition (unless coupled to a [transition model](transition.md)). |
| Hardware / parallel fit | Pointwise sources, same fit as the flow solver; wall distance is a global precomputation. |

## In a run

Planned: model choice, free-stream and wall values, wall spacing, production limiter switch, how to run two models as a bracket, symptoms of a bad free-stream $\omega$ or a stagnation anomaly.

## Which codes

To be filled from user manuals and methods papers. At the general level: production reentry codes offer algebraic models (historically), Spalart–Allmaras and SST ([hypersonic page](../physics/turbulence-modeling.md#which-codes)).

!!! warning "Calibration"
    Variant names and defaults differ between codes and versions; the page will cite each code's manual for its options.

## See also

[Turbulence fundamentals](fundamentals.md) · [Hypersonic boundary layers](../physics/turbulence-modeling.md) · [Scale-resolving methods](scale-resolving.md) · [Transition](transition.md) · [Shock/boundary-layer interaction](../physics/shock-boundary-layer-interaction.md)

## References

Wilcox, *Turbulence Modeling for CFD* (2006); Pope (2000), chs. 10–11; Cebeci & Smith (1974); Baldwin & Lomax (1978); Spalart & Allmaras (1992); Catris & Aupoix (2000); Rung et al. (2003); Launder & Spalding (1974); Durbin (1996); Wilcox (2008); Menter (1994); Menter, Kuntz & Langtry (2003); Launder, Reece & Rodi (1975); Speziale, Sarkar & Gatski (1991); Wallin & Johansson (2000); Roy & Blottner (2006); Sinha, Mahesh & Candler (2003); NASA Turbulence Modeling Resource. See the [bibliography](../../references.md).
