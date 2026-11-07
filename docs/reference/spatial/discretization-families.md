---
status: outline
---

# Discretization families

<div class="page-meta" markdown>
**Slot:** Track 0.2 spatial discretization · **Depth:** [deep] · **Taught in:** [Lesson 0.2](../../course/track-0/0-2-spatial-discretization.md) (pending)
</div>

## What it is

The ways of turning the continuous PDE into a finite set of unknowns: finite differences, finite volumes, finite elements and discontinuous Galerkin, and particle methods (DSMC); on structured multiblock or unstructured grids; cell-centred or vertex-based.

## The problem it solves

Each family makes different trade-offs between conservation, geometric flexibility, order of accuracy and cost. The choice constrains everything downstream: how reconstruction works, which relaxation directions exist, and how heat flux behaves near walls.

## How it works

*(Outline, to be written in Lesson 0.2.)*

## Variants

### Finite difference
### Finite volume, cell-centred
### Finite volume, vertex-based (dual mesh)
### Finite element and discontinuous Galerkin
### Particle methods (DSMC)
### Structured multiblock vs unstructured grids

Why structured, shock-aligned grids dominated aeroheating, and what unstructured codes do instead (prism layers, line structures). See [Track 2.9](../../course/track-2.md).

## Implications

*(To be filled.)*

## In a run

*(To be filled.)*

## Which codes

Structured cell-centred FV: DPLR, LAURA, Eilmer, MFC. Unstructured cell-centred FV: US3D. Vertex-based FV: FUN3D, SU2. DSMC: SPARTA. See [codes](../../codes/index.md).

## See also

[The finite-volume pipeline](finite-volume-pipeline.md)

## References

Hirsch; Blazek; Bird. See the [bibliography](../../references.md).
