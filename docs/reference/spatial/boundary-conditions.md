---
status: outline
---

# Boundary conditions

<div class="page-meta" markdown>
**Slot:** Track 0.7 · **Depth:** [deep]
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

Supersonic outflow needs no physical condition (extrapolate). Subsonic outflow needs one, and imposing a fixed pressure reflects acoustic waves back into the domain. **Non-reflective (characteristic) conditions** in the Poinsot–Lele/NSCBC style instead set the amplitude of the incoming acoustic wave to relax the pressure towards a target, $\mathcal L_{\text{in}} = \sigma\,(1 - M^2)\,\dfrac{c}{L}\,(p - p_\infty)$, with a relaxation coefficient $\sigma$: zero is perfectly non-reflecting but lets the mean pressure drift; large values pin the pressure but reflect. $\sigma \approx 0.58$ (an optimum attributed to Rudy & Strikwerda) and 0.25 are common choices. *(To be written.)*
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
