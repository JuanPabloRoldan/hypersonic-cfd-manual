# Reference manual

One page per method or model family, organized by the solver slot it belongs to. Each page can be read cold and follows the same template (see [how to use this manual](../how-to-use.md#page-anatomy)). The [implications matrix](implications-matrix.md) puts the six-lens verdicts for every method side by side.

## By slot

**Foundations.** What every solver is trying to solve.
[Governing equations](foundations/governing-equations.md) ·
[Conservation form and weak solutions](foundations/conservation-and-weak-solutions.md) ·
[Mathematical character](foundations/mathematical-character.md) ·
[Closing the system](foundations/closing-the-system.md)

**Spatial discretization.** Turning the PDE into a residual.
[The finite-volume pipeline](spatial/finite-volume-pipeline.md) ·
[Discretization families](spatial/discretization-families.md) ·
[Reconstruction and limiters](spatial/reconstruction.md) ·
[WENO](spatial/weno.md) ·
[Riemann solvers](spatial/riemann-solvers.md) ·
[Flux-vector splitting](spatial/flux-vector-splitting.md) ·
[Central schemes and dissipation](spatial/central-schemes.md) ·
[Shock instabilities](spatial/shock-instabilities.md) ·
[Viscous fluxes and gradients](spatial/viscous-fluxes.md) ·
[Boundary conditions](spatial/boundary-conditions.md)

**Time integration and convergence.** Driving the residual to zero, or through time.
[Time-step limits](time/time-step-limits.md) ·
[Explicit methods](time/explicit-methods.md) ·
[Implicit methods and Jacobians](time/implicit-methods.md) ·
[Point and line relaxation](time/relaxation-methods.md) ·
[Local time stepping](time/local-time-stepping.md) ·
[Explicit vs implicit](time/explicit-vs-implicit.md) ·
[Dual time stepping](time/dual-time-stepping.md) ·
[Convergence diagnostics](time/convergence-diagnostics.md)

**Source terms.**
[Stiff source terms](sources/stiff-sources.md)

**Thermochemistry.** The closures that make it a reentry code.
[Gas models](thermo/gas-models.md) ·
[Energy modes and thermodynamics](thermo/energy-modes.md) ·
[Thermal nonequilibrium models](thermo/thermal-nonequilibrium.md) ·
[Finite-rate chemistry](thermo/finite-rate-chemistry.md) ·
[Transport and diffusion](thermo/transport-and-diffusion.md)

**Walls and surfaces.**
[Wall boundary conditions](walls/wall-boundary-conditions.md) ·
[Surface energy balance](walls/surface-energy-balance.md)

**Physics.**
[Entry flow anatomy](physics/entry-flow-anatomy.md)

**Special formulations.**
[Space marching (PNS)](special/space-marching.md)

Physics topics that haven't been taught yet (stagnation heating, SWBLI, shock–shock interactions, transition, rarefaction, radiation, material response) are outlined in the [course tracks](../course/index.md) and get reference pages as they're covered.
