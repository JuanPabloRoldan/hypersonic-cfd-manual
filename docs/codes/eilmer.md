---
status: outline
---

# Eilmer

Open-source compressible-flow code from the University of Queensland, used alongside expansion-tube experiments.

## Track 0 choices

| Slot | Choice | Reference |
|---|---|---|
| Discretization | Structured multiblock finite volume (unstructured also supported) | [Discretization families](../reference/spatial/discretization-families.md) |
| Inviscid flux | Several options | [Riemann solvers](../reference/spatial/riemann-solvers.md) |
| Time advancement | Explicit, or Newton–Krylov for steady state | [Explicit vs implicit](../reference/time/explicit-vs-implicit.md) |
| Other | Shock fitting; conjugate heat transfer; multi-temperature thermochemistry | |

## What's cool

Both ends of the time-integration trade-off in one code, and shock fitting as an alternative to capturing.

!!! warning "Calibration"
    Outline only; to be filled from Eilmer documentation.

## References

See the [bibliography](../references.md).
