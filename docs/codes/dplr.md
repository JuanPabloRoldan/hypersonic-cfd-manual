---
status: draft
---

# DPLR

**Data-Parallel Line Relaxation** code, NASA Ames Research Center. The workhorse for Orion, MSL and Mars 2020 aerothermal environments.

## Purpose

Steady (and time-accurate) reacting Navier–Stokes solutions for entry vehicles, built for heat-flux accuracy on design trajectories.

## Track 0 choices

| Slot | Choice | Reference |
|---|---|---|
| Governing equations | Reacting, two-temperature Navier–Stokes | [Governing equations](../reference/foundations/governing-equations.md) |
| Discretization | Structured multiblock finite volume; grids tailored to the shock | [Discretization families](../reference/spatial/discretization-families.md) |
| Reconstruction | Second-order MUSCL-type | [Reconstruction](../reference/spatial/reconstruction.md) |
| Inviscid flux | Modified Steger–Warming flux-vector splitting | [Flux-vector splitting](../reference/spatial/flux-vector-splitting.md#modified-steger-warming) |
| Time advancement | Implicit data-parallel line relaxation along wall-normal lines | [Relaxation](../reference/time/relaxation-methods.md#line-relaxation) |
| Sources | Implicit | [Stiff sources](../reference/sources/stiff-sources.md) |
| Walls | Catalytic walls, surface energy balance, blowing BC for coupling with PATO | [Wall BCs](../reference/walls/wall-boundary-conditions.md) |

## What's cool

The name is the method. Its signature feature, line relaxation, is a basic idea from linear algebra (solve the stiffest coupling exactly, relax the rest), aimed precisely at the stiffness of aeroheating grids: the tiny wall-normal cells. Doing the line solves with Jacobi-type coupling between lines makes them independent within a sweep, so they parallelize cleanly.

## Implications

Excellent steady convergence on structured, wall-aligned grids; robust shocks from flux-vector splitting with acceptable boundary-layer dissipation from the modification; the line structure ties it to grids that have wall-normal lines, and the sequential Thomas solves are awkward on GPUs ([Track 3.8](../course/track-3.md)).

## Pipeline role

Loosely coupled to NEQAIR (radiation) and FIAT (material response) in design practice; blowing boundary condition for iteration with PATO. See [Track 9](../course/track-9.md).

!!! warning "Calibration"
    Reconstruction and limiter details to be verified against Wright, Candler & Bose (1998) and DPLR documentation.

## References

Wright, Candler & Bose (1998); Wright et al. on MSL and Orion aerothermal environments (NTRS). See the [bibliography](../references.md).
