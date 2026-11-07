---
status: outline
---

# STAR-CCM+

Commercial multiphysics CFD (Siemens). Its coupled density-based solver handles hypersonic flows, with Roe and AUSM+ flux options and two-temperature models in recent versions; it has been validated by the US Navy on cone-flare and double-cone cases.

## Why it's here

A good place to see how a GUI exposes, and hides, solver choices. Each option in its physics continuum maps to a slot in this manual: the flux option to [flux functions](../reference/spatial/riemann-solvers.md), the "coupled implicit" solver to [implicit methods](../reference/time/implicit-methods.md), the CFL setting to [time-step limits](../reference/time/time-step-limits.md), and its documentation's theory guide is the model for this manual's reference format.

!!! warning "Calibration"
    Outline only; option names and defaults to be checked against the current STAR-CCM+ documentation.

## References

See the [bibliography](../references.md).
