---
status: outline
---

# FUN3D

NASA Langley's unstructured-grid solver; hypersonic and reacting capability through its HEFSS path.

## Purpose

General aerodynamics on unstructured grids, with adjoint-based adaptation and design; reacting hypersonics as an extension.

## Track 0 choices

| Slot | Choice | Reference |
|---|---|---|
| Discretization | Unstructured vertex-based (node-centred) finite volume | [Discretization families](../reference/spatial/discretization-families.md) |
| Time advancement | Implicit, with point- and line-implicit relaxation in boundary-layer prisms; BDF2 with subiterations for time-accurate runs | [Relaxation](../reference/time/relaxation-methods.md) |
| Adaptation | Adjoint-based and metric-based adaptation | [Track 2.8](../course/track-2.md) |

## What's cool

Adjoint machinery: error estimation and grid adaptation targeted at a chosen output (for example, heat flux at a point).

!!! warning "Calibration"
    Outline only; to be filled from FUN3D documentation.

## References

FUN3D manual (NTRS). See the [bibliography](../references.md).
