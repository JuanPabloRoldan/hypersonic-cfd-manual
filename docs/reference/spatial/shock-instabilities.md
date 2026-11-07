---
status: outline
---

# Shock instabilities: the carbuncle

<div class="page-meta" markdown>
**Slot:** Track 2.2 · **Depth:** [deep] · **Taught in:** [Track 2](../../course/track-2.md) (pending)
</div>

## What it is

A family of purely numerical failures of shock-capturing schemes at strong shocks aligned with the grid: the **carbuncle** (a spurious protrusion of a bow shock along the stagnation line), odd–even decoupling along a planar shock, and kinked Mach stems.

## The problem it solves

This page is about a problem, not a method: knowing which flux functions are prone, why, and what fixes exist.

## How it works

*(Outline.)* Contact-resolving solvers ([Roe](riemann-solvers.md#roe), [HLLC](riemann-solvers.md#hllc)) put almost no dissipation on the shear and entropy waves; along a grid-aligned shock that lack of transverse damping lets perturbations grow. Dissipative solvers ([HLL](riemann-solvers.md#hll), [Steger–Warming](flux-vector-splitting.md#steger-warming)) damp them. The same dissipation that cures the carbuncle smears boundary layers.

## Variants

### Fixes

Entropy fixes with multidimensional dissipation, hybrid fluxes (HLLC away from shocks, HLL at shocks), rotated Riemann solvers, shock-aligned grids ([Track 2.1](../../course/track-2.md)).

## Implications

*(To be filled.)*

## In a run

A capsule solution whose bow shock develops a nose or a bulge at the stagnation line, with stagnation heating that depends on the flux scheme.

## Which codes

*(To be filled.)*

## See also

[Riemann solvers](riemann-solvers.md) · [Flux-vector splitting](flux-vector-splitting.md)

## References

Quirk (1994). See the [bibliography](../../references.md).
