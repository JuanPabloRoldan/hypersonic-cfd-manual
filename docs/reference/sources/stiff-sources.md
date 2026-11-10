---
status: draft
---

# Stiff source terms

<div class="page-meta" markdown>
**Chapter:** 8 Source terms · **Depth:** [deep]
</div>

## What it is

How a solver integrates the chemistry production rates $\dot\omega_s$ and the vibrational energy exchange $Q_{T\text{-}v}$ when their time scales are many orders of magnitude shorter than the flow's. A source is **stiff** when its fastest time scale is much shorter than the time step you'd like to take.

## The problem it solves

Reaction rates switch on exponentially with temperature ([finite-rate chemistry](../thermo/finite-rate-chemistry.md#how-it-knows-when-to-react)): behind a strong shock some reactions equilibrate in nanoseconds while the flow evolves over milliseconds. Integrating such sources explicitly would force $\Delta t$ below the fastest chemical time scale everywhere, a limit often far more severe than the [flow limits](../time/time-step-limits.md#source-term-limit).

The ratio of flow time to chemical time is the **Damköhler number**, $Da = \tau_{\text{flow}}/\tau_{\text{chem}}$. $Da \ll 1$: chemistry effectively frozen. $Da \gg 1$: chemistry effectively in equilibrium. $Da \sim 1$: genuine nonequilibrium. A reentry flow contains all three regimes at once, which is exactly what makes it stiff.

## How it works

Reactions can't be stepped one at a time: they share species, so they are tightly coupled through the concentrations. All practical approaches work **cell by cell**, treating the full source vector of each cell together.

### Point-implicit {#point-implicit}

Treat the source implicitly in each cell. For an otherwise explicit update,

$$
\left(\frac{V}{\Delta t}\,\mathbf I - V\,\frac{\partial\mathbf S}{\partial\mathbf U}\right)\Delta\mathbf U = -\mathbf R(\mathbf U^n),
$$

one dense $n\times n$ solve per cell. This removes the chemical stability limit entirely. In a fully implicit code, $\partial\mathbf S/\partial\mathbf U$ simply joins the diagonal blocks of the [residual Jacobian](../time/implicit-methods.md#two-different-jacobians). This is the norm in reentry codes.

### Operator splitting with sub-stepped chemistry {#operator-splitting-with-sub-stepped-chemistry}

Advance the flow (fluxes only) by $\Delta t$, then integrate each cell's chemistry ODE system $d\mathbf U/dt = \mathbf S(\mathbf U)$ over the same $\Delta t$ with a stiff adaptive integrator (BDF-type, CVODE-style), taking as many internal substeps as that cell needs. Strang splitting (half-step chemistry, full-step flow, half-step chemistry) gives second-order accuracy in time.

A caveat matters for steady aeroheating: with simple (Lie) splitting, the converged steady state can depend on $\Delta t$, because the split operators don't balance exactly at steady state. That makes splitting awkward for steady problems and is part of why point-implicit treatment won there. Splitting is common in unsteady combustion codes.

### IMEX

Implicit–explicit Runge–Kutta schemes: explicit stages for the fluxes, implicit stages for the sources, combined in one consistent time-accurate scheme without splitting error at steady state.

### Reduction methods

Eliminate the fastest modes analytically so they never need resolving: quasi-steady-state approximation (QSSA) for fast intermediate species, partial equilibrium for fast reactions, and computational singular perturbation (CSP) or intrinsic low-dimensional manifolds for systematic reduction. More common in combustion than in reentry.

## Implications

| Lens | Effect |
|---|---|
| Time step and cost | Point-implicit: a dense $n\times n$ solve per cell, removes the chemical limit. Splitting: cost scales with local stiffness (many substeps only where chemistry is fast). |
| Steady vs unsteady | Point-implicit works for both; Lie splitting has a $\Delta t$-dependent steady state; Strang and IMEX are time-accurate. |
| Accuracy | Large implicit steps are fine for steady state; for unsteady chemistry, time accuracy needs care (splitting order, subiterations). |
| Robustness | Implicit sources prevent the explosive overshoot of explicit chemistry; negative species densities still need clipping or positivity-preserving updates. |
| Physics captured or lost | Reduction methods discard fast transients by design; fine if those are not of interest. |
| Hardware / parallel fit | Cell-local and parallel, but adaptive substepping gives uneven work per cell, which hurts GPU load balance. |

## In a run

Knobs: source treatment (point-implicit, split), chemistry startup (frozen chemistry first, then switch on), sometimes a cap on reaction rates during startup. Symptoms: blow-up the moment chemistry is switched on; negative species densities near shocks; convergence slowdown when going from 5 to 11 species.


- **Start-up:** ramp all chemical sources from zero to full strength over the early iterations, and prefer a two-temperature model behind strong shocks, where it is less stiff than a one-temperature model because $T_v$ starts low (Park 1990, §5.5). Electron-impact ionization is the stiffest reaction class; see [avalanche ionization](../thermo/ionization-and-electrons.md#effects-on-stability-and-robustness).
## Which codes

!!! warning "Calibration"
    Production reentry codes (DPLR, LAURA, US3D) treat sources implicitly as part of their implicit systems. Operator splitting with stiff ODE integrators is more common in unsteady combustion and in some research codes. Code-specific details to be filled.

## See also

[Finite-rate chemistry](../thermo/finite-rate-chemistry.md) · [Thermal nonequilibrium](../thermo/thermal-nonequilibrium.md) · [Implicit methods](../time/implicit-methods.md) · [Local time stepping](../time/local-time-stepping.md)

## References

Bussing & Murman (1988) on point-implicit sources; Strang (1968); Hindmarsh et al. (2005) on CVODE/SUNDIALS; Lam & Goussis (1994) on CSP. See the [bibliography](../../references.md).
