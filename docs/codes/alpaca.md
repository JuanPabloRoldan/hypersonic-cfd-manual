---
status: draft
---

# ALPACA (contrast, and a knob-to-slot exercise)

Open-source compressible solver from TU Munich (Adams group), built around high-order shock capturing, multiresolution adaptive grids and sharp-interface (level-set) multiphase methods. Like [MFC](mfc.md), it is not a reentry code: it is explicit, Cartesian and designed for unsteady shock-dominated flows, and much of its option list concerns multiphase interfaces. It is here because its input deck exposes, as named knobs, almost every flux and reconstruction choice discussed in this manual, which makes it a good place to practise placing each setting in its slot. Its sibling, JAX-Fluids, is a differentiable JAX re-implementation with a similar option set.

## Knobs, by slot

Only the single-phase options relevant to hypersonics are listed; level-set, interface and diffuse-interface settings are omitted.

| Slot | ALPACA knob and options | Reference page |
|---|---|---|
| Governing equations | Equation set: Euler, Navier–Stokes (plus isentropic and multiphase models) | [Governing equations](../reference/foundations/governing-equations.md) |
| Flux function, finite-volume form | Riemann solver: HLLC, HLL, Rusanov | [Riemann solvers](../reference/spatial/riemann-solvers.md) |
| Flux function, finite-difference form | Flux splitting: Roe, local and global Lax–Friedrichs, and low-Mach Roe-M / LLF-M with limit factor $\phi = 5$ | [Flux-vector splitting](../reference/spatial/flux-vector-splitting.md#flux-splitting-for-finite-difference-weno) |
| Wave speeds | Einfeldt, Davis, Toro (pressure-based), arithmetic average | [Wave-speed estimates](../reference/spatial/riemann-solvers.md#wave-speed-estimates) |
| Low-Mach / shock stability | HLLC low-Mach fix (HLLC-LM) with limit Mach 0.1 and sine or linear activation, optionally gated by a shock sensor | [Low-Mach corrections](../reference/spatial/low-mach-corrections.md#hllc-lm), [shock instabilities](../reference/spatial/shock-instabilities.md) |
| Reconstruction variables | Conservative, primitive, characteristic, characteristic-primitive; consistent primitive reconstruction with temperature or pressure as the dependent state | [Which variables to reconstruct](../reference/spatial/reconstruction.md#which-variables-to-reconstruct) |
| Reconstruction stencil | First order, central 2nd/4th order; WENO3, WENO5 (JS, Z, mapped and others), WENO-AO(5,3), WENO-CU6, TENO5, WENO7, WENO9 | [ENO, WENO and TENO](../reference/spatial/weno.md) |
| Limiters (MUSCL) | minmod, Koren, MC ("MUSCL"), superbee, van Albada, van Leer, OSPRE, HCUS, SMART | [Limiters](../reference/spatial/reconstruction.md#limiters) |
| Viscous terms | Fourth-order central differences at cell centres and faces | [Viscous fluxes](../reference/spatial/viscous-fluxes.md) |
| Positivity | Positivity check, a-posteriori check, density and pressure floors ($10^{-7}$), positivity fallback flux for flux splitting | [Positivity safeguards](../reference/spatial/riemann-solvers.md#positivity-safeguards) |
| Time advancement | Explicit SSP Runge–Kutta (RK2, RK3), CFL typically 0.25–0.5 | [Explicit methods](../reference/time/explicit-methods.md) |
| Grid | Multiresolution (wavelet-based) adaptive refinement: refinement threshold, maximum level, prediction-stencil order, blocks of 16 cells with 4 halo cells | [Discretization families](../reference/spatial/discretization-families.md) |
| Boundary conditions | Non-reflective outflow with relaxation coefficient $\sigma = 0.58$ | [Boundary conditions](../reference/spatial/boundary-conditions.md) |

## Through the implications lens

Every choice points the same way as MFC's: explicit, high-order, low-dissipation, wave-resolving, with a large menu of shock-stability and positivity fixes because those schemes are less forgiving at strong shocks. Several of the fixes now in this manual (HLLC-LM, Roe-M, TENO, WENO-CU6) come from the same group. A production aeroheating code makes the opposite choices for steady heating on wall-resolved grids; see the [cost model](../reference/time/explicit-vs-implicit.md).

!!! warning "Calibration"
    Option names are from an ALPACA input deck supplied by the user (a newer version than the public repository, which offers a subset, e.g. Einfeldt, Davis, Toro and arithmetic wave speeds). Defaults are set per run. Check the ALPACA and JAX-Fluids documentation for the current lists.

## References

Hoppe et al. on ALPACA; Bezgin, Buhendwa & Adams (2023) on JAX-Fluids; Fleischmann, Adami & Adams (2020). See the [bibliography](../references.md).
