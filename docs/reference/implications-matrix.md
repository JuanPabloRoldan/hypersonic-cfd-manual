# Implications matrix

Every method covered so far, judged on the six lenses side by side. Each row links to its reference page, where the full table and the reasoning live. Rows are added as new methods are written up.

**Legend:** ✓ strength · ✗ weakness · ~ depends or mixed. Short phrases, not verdicts; read the reference page before relying on a cell.

## Reconstruction

| Method | Time step and cost | Steady vs unsteady | Accuracy | Robustness | Physics captured or lost | Hardware fit |
|---|---|---|---|---|---|---|
| [First order](spatial/reconstruction.md#first-order) | ✓ cheapest | ✓ converges easily (startup) | ✗ very dissipative, poor heat flux | ✓ most robust | ✗ smears everything | ✓ |
| [MUSCL + limiter](spatial/reconstruction.md#muscl-with-limiters) | ✓ cheap | ~ limiter chatter can stall steady runs | ~ 2nd order, clips extrema (stagnation point) | ~ depends on limiter and variables | ~ dissipative limiters smear shear layers | ✓ local stencil |
| [WENO](spatial/weno.md#weno-jiang-shu) | ~ more per face | ~ built for unsteady; weights can stall implicit steady | ✓ high order in smooth flow | ~ needs positivity care at strong shocks | ✓ keeps small waves | ✓ structured GPU; wide halos |
| [TENO](spatial/weno.md#teno) | ~ as WENO | ~ hard switch can stall steady runs | ✓ optimal linear scheme in smooth flow, least dissipative | ~ needs care at strong shocks | ✓ keeps small waves | ✓ structured GPU; wide halos |

## Inviscid flux functions

| Method | Time step and cost | Steady vs unsteady | Accuracy | Robustness | Physics captured or lost | Hardware fit |
|---|---|---|---|---|---|---|
| [Roe](spatial/riemann-solvers.md#roe) | ~ medium | ~ entropy fix can cause limit cycles | ✓ resolves contacts, boundary layers | ✗ entropy fix needed; not positivity-preserving; carbuncle | ✓ contacts and shear | ✓ |
| [HLL / HLLE](spatial/riemann-solvers.md#hll) | ✓ cheap | ✓ | ✗ smears contacts and boundary layers | ✓ positive, carbuncle-resistant | ✗ loses contact and shear waves | ✓ |
| [HLLC](spatial/riemann-solvers.md#hllc) | ✓ cheap | ✓ | ✓ resolves contacts | ~ positive with suitable speeds; carbuncle-prone | ✓ contacts, species ride the contact | ✓ |
| [HLLC-LM](spatial/low-mach-corrections.md#hllc-lm) | ✓ cheap | ✓ smooth activation | ✓ less dissipative than HLLC | ✓ shock-stable incl. 3D | ✓ contacts, low-Mach features | ✓ |
| [KEC + Ducros dissipation](spatial/central-schemes.md#kinetic-energy-consistent-fluxes) | ✓ cheap fluxes | ✓ built for LES/DNS, implicit capable | ✓ minimal dissipation away from shocks | ~ depends on sensor | ✓ turbulence, separation dynamics | ✓ |
| [Rusanov](spatial/riemann-solvers.md#rusanov-local-laxfriedrichs) | ✓ cheapest | ✓ | ✗ most dissipative | ✓ very robust | ✗ smears heavily | ✓ |
| [Steger–Warming](spatial/flux-vector-splitting.md#steger-warming) | ✓ cheap, simple Jacobians | ✓ robust steady convergence | ✗ smears boundary layers | ✓ carbuncle-resistant | ✗ damps contacts and shear | ✓ |
| [Modified Steger–Warming](spatial/flux-vector-splitting.md#modified-steger-warming) | ✓ cheap, simple Jacobians | ✓ | ~ much better boundary layers | ✓ FVS robustness at shocks | ~ | ✓ |
| [AUSM family](spatial/flux-vector-splitting.md#ausm-family) | ✓ cheap | ✓ | ✓ resolves contacts | ~ variant-dependent | ✓ | ✓ |

## Time integration

| Method | Time step and cost | Steady vs unsteady | Accuracy | Robustness | Physics captured or lost | Hardware fit |
|---|---|---|---|---|---|---|
| [Explicit RK](time/explicit-methods.md) | ✗ CFL and viscous limits; ✓ cheapest step | ✓ time-accurate; ✗ slow to steady state on stiff grids | ✓ resolves fast transients | ✓ fails cleanly | ✓ wave-resolving | ✓ ideal for GPUs |
| [Implicit + point relaxation](time/relaxation-methods.md#point-relaxation) | ✓ no stability limit; ✗ $n^2$ memory, $n^3$ blocks | ✓ steady; unsteady via dual time | ✓ converged answer independent of LHS | ~ CFL ramping needed | ✗ filters fast transients | ✗ sequential sweeps |
| [Implicit + line relaxation](time/relaxation-methods.md#line-relaxation) | ✓ kills wall-normal stiffness | ✓ steady; unsteady via dual time | ✓ | ✓ on stretched grids | ✗ filters fast transients | ~ parallel across lines, sequential along |
| [Steady local time stepping](time/local-time-stepping.md) | ✓ removes global smallest-cell limit; ✗ not aspect-ratio stiffness | steady only | n/a | ~ | n/a | ✓ free |
| [Dual time stepping](time/dual-time-stepping.md) | ~ physics-sized steps, subiterations each | ✓ time-accurate implicit | ~ needs subiteration convergence | ~ | ~ resolves what the step resolves | ✗ as implicit |

## Source treatment

| Method | Time step and cost | Steady vs unsteady | Accuracy | Robustness | Physics captured or lost | Hardware fit |
|---|---|---|---|---|---|---|
| [Point-implicit](sources/stiff-sources.md#point-implicit) | ✓ removes chemical limit; dense block per cell | ✓ both | ✓ | ✓ | ✓ | ✓ cell-local |
| [Operator splitting + stiff ODE](sources/stiff-sources.md#operator-splitting-with-sub-stepped-chemistry) | ~ work scales with local stiffness | ✗ Lie splitting: $\Delta t$-dependent steady state | ~ Strang is 2nd order | ✓ | ✓ | ✗ uneven work per cell |

## Gas models

| Model | Time step and cost | Steady vs unsteady | Accuracy | Robustness | Physics captured or lost | Hardware fit |
|---|---|---|---|---|---|---|
| [Calorically perfect](thermo/gas-models.md#the-ladder-with-implications) | ✓ 5 eq | n/a | ✗ wrong T and standoff for entry | ✓ | ✗ all high-T effects | ✓ |
| [Equilibrium air](thermo/gas-models.md#the-ladder-with-implications) | ✓ 5 eq + lookup | n/a | ✓ if $Da \gg 1$ | ✓ | ✗ relaxation, freezing, finite catalysis | ~ lookups |
| [Finite-rate 1T](thermo/gas-models.md#the-ladder-with-implications) | ~ 15 eq, stiff | stiff sources | ~ | ~ | ✗ vibrational lag | ~ |
| [Finite-rate 2T](thermo/gas-models.md#the-ladder-with-implications) | ✗ 16 eq, stiff | stiff sources | ✓ design standard | ~ $T_v$ inversion | ~ no electron T, Boltzmann assumed | ~ |
