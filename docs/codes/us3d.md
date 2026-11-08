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
| Reconstruction | Second-order TVD-MUSCL (minmod in the published double-cone case) | [Reconstruction](../reference/spatial/reconstruction.md#limiters) |
| Inviscid flux | Modified Steger–Warming (face-averaged split Jacobians, eigenvalues smoothed with $\delta \approx 0.1$–0.2); low-dissipation option: kinetic-energy-consistent central flux plus the modified Steger–Warming dissipation term scaled by a Ducros shock sensor | [Flux-vector splitting](../reference/spatial/flux-vector-splitting.md#modified-steger-warming), [central schemes](../reference/spatial/central-schemes.md#kinetic-energy-consistent-fluxes) |
| Time advancement | Implicit: BDF2 with subiterations for time-accurate runs; full-matrix point relaxation (FMPR) for the linear systems; DPLR-type line relaxation heritage; CFL ramped to $10^5$ for steady runs | [Implicit methods](../reference/time/implicit-methods.md), [relaxation](../reference/time/relaxation-methods.md), [dual time stepping](../reference/time/dual-time-stepping.md) |
| Thermochemistry | Two-temperature finite-rate; gas–surface interaction | [Thermal nonequilibrium](../reference/thermo/thermal-nonequilibrium.md) |

## What's cool

One flux, two personalities. With the dissipation switch fully on, it is a robust upwind code for steady aeroheating; with the Ducros switch, the same code runs LES/DNS with dissipation only at shocks. And the signature upwind flux, modified Steger–Warming, turns out on inspection to be a Roe-type flux with face-averaged matrices: if the face average is the Roe average, the two are identical. The "distinctive" choice is really a basic solver idea in disguise.

The implicit low-dissipation combination is itself instructive: Subbareddy & Candler point out that the explicit step would be limited by $|u| + c$ while turbulence only needs steps set by $u$, a factor of order $1 + 1/M$ more steps in low-Mach regions, plus the high-aspect-ratio boundary-layer cells. That is the [cost-model](../reference/time/explicit-vs-implicit.md) argument for implicit LES.

## Validation highlighted in the source

The 25°–55° double cone at Mach 11.3 (CUBRC), whose separation size is sensitive to numerical dissipation: surface heating matched experiment once vibrational relaxation and chemistry were included in the forebody.

!!! warning "Calibration"
    Everything in the table except the code's general description is from Subbareddy & Candler (2009), a 2009 snapshot. The overall code architecture (including line relaxation on unstructured grids, thermochemistry options and current defaults) should be checked against Candler et al. (2015), "Development of the US3D code for advanced compressible and reacting flow simulations," AIAA 2015-1893, and Nompelis, Drayna & Candler (2004/2005) on the solver's origins.

## References

Subbareddy & Candler (2009); Candler et al. (2015); Nompelis, Drayna & Candler (2004). See the [bibliography](../references.md).
