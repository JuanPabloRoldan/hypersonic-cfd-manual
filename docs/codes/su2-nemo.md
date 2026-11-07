---
status: outline
---

# SU2-NEMO

The nonequilibrium (NEMO) solver of the open-source SU2 suite (Stanford origin, community-developed).

## Purpose

Open-source reacting, two-temperature hypersonic flows on unstructured grids; a practical code for running small cases yourself.

## Track 0 choices

| Slot | Choice | Reference |
|---|---|---|
| Discretization | Unstructured vertex-based finite volume | [Discretization families](../reference/spatial/discretization-families.md) |
| Inviscid flux | Roe, AUSM family and others | [Flux-vector splitting](../reference/spatial/flux-vector-splitting.md#ausm-family) |
| Thermochemistry | Two-temperature; built-in models or Mutation++ | [Mutation++](mutationpp.md) |
| Other | Adjoint inherited from SU2; open-source coupling with PATO | |

## What's cool

Open source end to end, so every choice can be read in the code and changed.

!!! warning "Calibration"
    Outline only; to be filled from SU2 documentation.

## References

See the [bibliography](../references.md).
