---
status: outline
---

# Boundary conditions

<div class="page-meta" markdown>
**Slot:** Track 0.7 · **Depth:** [deep] · **Taught in:** [Lesson 0.7](../../course/track-0/0-7-boundary-conditions.md) (pending)
</div>

## What it is

How a solver supplies the information missing at the edges of the domain, as boundary-face fluxes or ghost-cell states.

## The problem it solves

A hyperbolic system needs exactly as many boundary conditions at a boundary as there are characteristics entering the domain; too many over-specifies the problem and reflects waves, too few leaves it ill-posed. Walls add viscous and thermochemical conditions.

## How it works

*(Outline.)* Count incoming characteristics from the signs of the eigenvalues normal to the boundary ([mathematical character](../foundations/mathematical-character.md#hyperbolic)).

## Variants

### Characteristic far-field and supersonic inflow
### Supersonic and subsonic outflow
### Symmetry planes and the axis of axisymmetric flow
### Walls

No-slip, thermal and catalytic conditions are covered on their own page: [wall boundary conditions](../walls/wall-boundary-conditions.md).

## Implications

*(To be filled.)*

## In a run

*(To be filled: reflections from outflow, axis singularities, shock interaction with the outer boundary.)*

## Which codes

*(To be filled.)*

## See also

[Wall boundary conditions](../walls/wall-boundary-conditions.md)

## References

Blazek; Hirsch. See the [bibliography](../../references.md).
