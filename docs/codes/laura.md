---
status: draft
---

# LAURA

**Langley Aerothermodynamic Upwind Relaxation Algorithm**, NASA Langley Research Center.

## Purpose

Structured-grid reacting Navier–Stokes aeroheating, with strong coupling to radiation and ablation.

## Track 0 choices

| Slot | Choice | Reference |
|---|---|---|
| Governing equations | Reacting, two-temperature Navier–Stokes | [Governing equations](../reference/foundations/governing-equations.md) |
| Discretization | Structured finite volume; shock-aligned grids | [Discretization families](../reference/spatial/discretization-families.md) |
| Inviscid flux | Roe's flux-difference splitting with Yee-type TVD limiting and an entropy fix | [Riemann solvers](../reference/spatial/riemann-solvers.md#roe) |
| Time advancement | Point-implicit relaxation | [Relaxation](../reference/time/relaxation-methods.md#point-relaxation) |
| Coupling | Radiation via HARA; ablating-wall boundary conditions | [Radiation solvers](radiation-tools.md) |

## What's cool

Tight in-code coupling of radiation and ablation, which matters at high entry speeds where radiation and ablation interact. Newer versions share infrastructure with FUN3D.

## Implications

Roe's contact resolution gives good boundary layers; the entropy fix and shock alignment manage the carbuncle risk. Point relaxation is simple and robust, with slower convergence than line relaxation on very stretched grids.

!!! warning "Calibration"
    Whether current versions offer line-implicit relaxation, and details of the entropy fix, to be checked against the LAURA user manual.

## References

Gnoffo (1990); Mazaheri et al., LAURA users manual (NTRS). See the [bibliography](../references.md).
