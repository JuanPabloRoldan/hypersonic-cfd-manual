---
status: outline
---

# Track 2: Numerics for hypersonic flows

**Depth:** [deep] unless marked. Builds directly on [Track 0](track-0/index.md).

| # | Topic | Depth | Reference |
|---|---|---|---|
| 2.1 | Shock capturing vs shock fitting; **shock alignment and grid tailoring** (DPLR, LAURA); outer-boundary adaptation. | [deep] | |
| 2.2 | **Shock instabilities: the carbuncle**, odd–even decoupling; why Roe/HLLC are prone and HLL/Steger–Warming aren't; entropy fixes, hybrid and rotated fluxes. | [deep] | [Shock instabilities](../reference/spatial/shock-instabilities.md), [low-Mach corrections](../reference/spatial/low-mach-corrections.md) |
| 2.3 | **Flux choices in reentry codes**: modified Steger–Warming (DPLR, US3D), Roe + Yee TVD (LAURA), AUSM family (SU2, commercial). Dissipation vs heat-flux accuracy. | [deep] | [Riemann solvers](../reference/spatial/riemann-solvers.md), [flux-vector splitting](../reference/spatial/flux-vector-splitting.md) |
| 2.4 | **Heat-flux accuracy**: grid and scheme sensitivity of stagnation heating; cell Reynolds number; wall-normal spacing; grid alignment; how flux dissipation contaminates heating; why converged residuals don't mean converged heating. | [deep] | [Viscous fluxes](../reference/spatial/viscous-fluxes.md#near-the-wall) |
| 2.5 | **Artificial dissipation and shock sensors**: JST, Ducros, hybrid central/upwind switching. | [deep] | [Central schemes](../reference/spatial/central-schemes.md) |
| 2.6 | **Kinetic-energy-consistent fluxes**: low dissipation for LES/DNS of transition and SWBLI unsteadiness; US3D-style dissipation added only at shocks. | [deep] | [Central schemes](../reference/spatial/central-schemes.md#kinetic-energy-consistent-fluxes) |
| 2.7 | **High-order methods** (WENO, DG) in hypersonics: what they buy and why production codes stayed second order. Contrast: shock regularization instead of capturing (IGR in MFC). | [deep] | [ENO, WENO and TENO](../reference/spatial/weno.md) |
| 2.8 | Mesh adaptation: metric-based anisotropic adaptation, adjoint-based adaptation (link to Dragonfly-type Titan entry work). | [feel] | |
| 2.9 | Unstructured vs structured for aeroheating: prisms and hexes near walls, why tetrahedral heating is notoriously noisy. | [feel] | [Discretization families](../reference/spatial/discretization-families.md) |
| 2.10 | **Space marching and reduced equations**: thin-layer and parabolized Navier–Stokes, the order-of-magnitude derivation, marching in $x$, Vigneron splitting, why marching fails in subsonic and separated regions; time marching as the blunt-body breakthrough. | [feel, with the math] | [Space marching](../reference/special/space-marching.md) |
