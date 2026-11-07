---
status: outline
---

# Lesson 0.3: Reconstruction

<div class="page-meta" markdown>
**Slot:** reconstruction · **Depth:** [deep] · **Reference pages:** [reconstruction and limiters](../../reference/spatial/reconstruction.md), [WENO](../../reference/spatial/weno.md)
</div>

## Planned content

1. Why face states are needed and what first order costs in accuracy.
2. Godunov's theorem: why high order without oscillations must be nonlinear.
3. MUSCL and slope limiters (minmod, van Leer, MC, superbee); TVD; extremum clipping at the stagnation point and its effect on heating.
4. WENO: candidate stencils, smoothness indicators, nonlinear weights; JS vs Z; why production aeroheating codes stayed second order (link to Track 2.7).
5. Which variables to reconstruct (conservative, primitive, characteristic) and positivity at Mach 25.
6. Unstructured reconstruction and limiters (Barth–Jespersen, Venkatakrishnan); limiter chatter and steady convergence.
7. MFC contrast: WENO on primitives, explicit time stepping, GPU-friendly stencils.

## Already previewed

Minmod numbers and the extremum case (Lesson 0.1 follow-ups); why primitives and when characteristic variables help. See [reconstruction](../../reference/spatial/reconstruction.md).

## Checkpoint (planned themes)

Predict what a limiter does at a stagnation-point temperature peak; why reconstructing $\rho E$ can give negative pressure; what changes in a run if you switch minmod to superbee.
