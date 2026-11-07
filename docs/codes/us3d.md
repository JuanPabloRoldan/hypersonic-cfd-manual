---
status: draft
---

# US3D

Unstructured implicit hypersonic solver, University of Minnesota (Candler group) and VirtusAero. Flow solver inside the Ares framework.

## Purpose

Reacting hypersonic flows on unstructured grids, from steady aeroheating to DNS/LES of transition and shock–boundary-layer interaction.

## Track 0 choices

| Slot | Choice | Reference |
|---|---|---|
| Discretization | Unstructured cell-centred finite volume | [Discretization families](../reference/spatial/discretization-families.md) |
| Inviscid flux | Modified Steger–Warming; kinetic-energy-consistent central flux with shock-sensor-switched upwind dissipation for low-dissipation work | [Flux-vector splitting](../reference/spatial/flux-vector-splitting.md), [central schemes](../reference/spatial/central-schemes.md#kinetic-energy-consistent-fluxes) |
| Time advancement | Implicit, DPLR heritage; implicit second-order time stepping for unsteady work | [Implicit methods](../reference/time/implicit-methods.md) |
| Thermochemistry | Two-temperature finite-rate; gas–surface interaction | [Thermal nonequilibrium](../reference/thermo/thermal-nonequilibrium.md) |

## What's cool

The KEC flux with dissipation switched on only at shocks: one code that can do robust steady aeroheating and low-dissipation simulations of instability waves. The signature idea (central where smooth, upwind where shocked) is the same trade-off every flux function makes, made explicit and local.

!!! warning "Calibration"
    Details of the dissipation switch and implicit options to be checked against Subbareddy & Candler (2009) and US3D documentation.

## References

Subbareddy & Candler (2009); Candler et al. on US3D development (AIAA). See the [bibliography](../references.md).
