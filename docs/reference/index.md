# Theory manual

The theory manual is ordered the way a solver is built: first the equations being solved and the physical models that close them, then how the equations are discretized in space, how the fluxes and sources are evaluated, and how the discrete system is advanced to a solution. Every page follows the same template (what it is, the problem it solves, how it works, variants, typical values, trade-offs, effects on stability, implications, in a run, which codes; see [how to use this manual](../how-to-use.md#page-anatomy)) and can be read cold.

Pages marked with a hollow circle in the sidebar are outlines; half-filled circles are drafts.

## Contents

**Implications matrix.** [Every method on the six lenses, side by side](implications-matrix.md).

**1 Fundamental equations.** What every solver is trying to solve.
[1.1 Governing equations](foundations/governing-equations.md) ·
[1.2 Conservation form and weak solutions](foundations/conservation-and-weak-solutions.md) ·
[1.3 Mathematical character](foundations/mathematical-character.md) ·
[1.4 Closing the system](foundations/closing-the-system.md)

**2 Entry flow physics.** The flows the equations describe.
[2.1 Entry flow anatomy](physics/entry-flow-anatomy.md) ·
[2.2 Hypersonic shock relations and Newtonian theory](physics/hypersonic-shock-relations.md) ·
[2.3 Stagnation-point heating](physics/stagnation-point-heating.md) ·
[2.4 Shock/boundary-layer interaction](physics/shock-boundary-layer-interaction.md) ·
[2.5 Shock–shock interactions](physics/shock-shock-interactions.md)

**3 Gas models and thermochemistry.** The closures that make it a reentry code.
[3.1 Gas models](thermo/gas-models.md) ·
[3.2 Energy modes and thermodynamics](thermo/energy-modes.md) ·
[3.3 Thermal nonequilibrium](thermo/thermal-nonequilibrium.md) ·
[3.4 Finite-rate chemistry](thermo/finite-rate-chemistry.md) ·
[3.5 Transport and diffusion](thermo/transport-and-diffusion.md) ·
[3.6 Ionization, electrons and plasma](thermo/ionization-and-electrons.md)

**4 Turbulence.**
[4.1 Turbulence modeling for hypersonic boundary layers](physics/turbulence-modeling.md)

**5 Boundary conditions and walls.**
[5.1 Boundary conditions](spatial/boundary-conditions.md) ·
[5.2 Wall boundary conditions](walls/wall-boundary-conditions.md) ·
[5.3 Surface energy balance](walls/surface-energy-balance.md)

**6 Spatial discretization.** Turning the PDEs into a residual.
[6.1 The finite-volume method](spatial/finite-volume-pipeline.md) ·
[6.2 Discretization families](spatial/discretization-families.md) ·
[6.3 Reconstruction and limiters](spatial/reconstruction.md) ·
[6.4 ENO, WENO and TENO](spatial/weno.md) ·
[6.5 Viscous fluxes and gradients](spatial/viscous-fluxes.md)

**7 Inviscid flux functions.** Turning two face states into one flux.
[7.1 Riemann solvers](spatial/riemann-solvers.md) ·
[7.2 Flux-vector splitting](spatial/flux-vector-splitting.md) ·
[7.3 Central schemes and dissipation](spatial/central-schemes.md) ·
[7.4 Low-Mach corrections](spatial/low-mach-corrections.md) ·
[7.5 Shock instabilities](spatial/shock-instabilities.md)

**8 Source terms.**
[8.1 Stiff source terms](sources/stiff-sources.md)

**9 Time integration and solvers.** Driving the residual to zero, or through time.
[9.1 Time-step limits](time/time-step-limits.md) ·
[9.2 Explicit methods](time/explicit-methods.md) ·
[9.3 Implicit methods and Jacobians](time/implicit-methods.md) ·
[9.4 Point and line relaxation](time/relaxation-methods.md) ·
[9.5 Local time stepping](time/local-time-stepping.md) ·
[9.6 Dual time stepping](time/dual-time-stepping.md) ·
[9.7 Explicit vs implicit](time/explicit-vs-implicit.md)

**10 Reduced equations and engineering methods.**
[10.1 Space marching (PNS)](special/space-marching.md) ·
[10.2 Approximate and engineering methods](special/engineering-methods.md)

**11 Rarefied flow and particle methods.** Where the continuum model ends.
[11.1 Rarefaction and continuum breakdown](rarefied/continuum-breakdown.md) ·
[11.2 DSMC](rarefied/dsmc.md) ·
[11.3 Free-molecular flow](rarefied/free-molecular-flow.md)

**12 Verification and diagnosis.**
[12.1 Convergence diagnostics](time/convergence-diagnostics.md) ·
[12.2 Engineering checks on a solution](verification/engineering-checks.md)

**13 Shock-layer radiation.** Heating by light from the shock layer.
[13.1 Shock-layer radiation](radiation/shock-layer-radiation.md)

**Appendix.** [A Codes at a glance](../codes/index.md): each production code's choice in each slot, with primary sources. [B Choosing physical models](model-selection.md): when each gas model, species set, temperature model, radiation and rarefaction treatment is needed, by speed, altitude and output.

## Chapters still to come

Outlines exist for shock/boundary-layer interaction (2.4), shock–shock interactions (2.5) and shock-layer radiation (13). Still to be added: material response and ablation, and further entry-flow physics (entropy layers and viscous interaction, transition, wake flow).
