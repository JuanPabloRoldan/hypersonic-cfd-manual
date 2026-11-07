---
status: outline
---

# Lesson 0.2: Spatial discretization

<div class="page-meta" markdown>
**Slot:** spatial discretization · **Depth:** [deep] · **Reference pages:** [discretization families](../../reference/spatial/discretization-families.md), [the finite-volume pipeline](../../reference/spatial/finite-volume-pipeline.md), [viscous fluxes](../../reference/spatial/viscous-fluxes.md)
</div>

## Planned content

1. Finite difference vs finite volume vs finite element and discontinuous Galerkin vs particle methods (DSMC): what each discretizes, what each conserves, and what each costs.
2. Structured multiblock vs unstructured grids; cell-centred vs vertex-based (dual mesh) finite volumes.
3. Why structured, shock-aligned grids dominated aeroheating, and what unstructured codes do instead (prism layers, wall-normal line structures).
4. Face gradients for viscous fluxes on general grids: Green–Gauss, least squares, and the face-normal correction.
5. MFC contrast: uniform-ish structured grids, high-order finite differences of fluxes vs finite-volume averages.

## Already previewed

The six-step residual evaluation was walked through in Lesson 0.1's follow-ups; see [the finite-volume pipeline](../../reference/spatial/finite-volume-pipeline.md).

## Checkpoint (planned themes)

Why a vertex-based code's "cell" is not a grid cell; why tetrahedral near-wall grids give noisy heat flux; what a structured grid buys an implicit line solver.
