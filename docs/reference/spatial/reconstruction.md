---
status: draft
---

# Reconstruction and limiters

<div class="page-meta" markdown>
**Slot:** Track 0.3 reconstruction · **Depth:** [deep] · **Taught in:** [Lesson 0.3](../../course/track-0/0-3-reconstruction.md) (pending; basics previewed in Lesson 0.1)
</div>

## What it is

A finite-volume cell stores only an average. To evaluate a flux at a face you need the solution *at* the face, on each side. **Reconstruction** builds a polynomial inside each cell from the cell and its neighbours and evaluates it at the faces, producing the left and right states $\mathbf W_L$, $\mathbf W_R$ fed to the [flux function](riemann-solvers.md). "MUSCL extrapolation" and "reconstruction" are the same operation in different vocabularies. A **limiter** modifies the reconstruction near discontinuities so it doesn't create new maxima or minima.

## The problem it solves

Using cell averages directly as face states (first order) is robust but very dissipative: boundary layers and shear layers smear, and heat flux is poor. Higher-order polynomials are accurate in smooth regions but oscillate at shocks. Limiters give high order where the flow is smooth and fall back towards first order at discontinuities.

## How it works

### Godunov's theorem

No *linear* scheme (one whose coefficients don't depend on the solution) can be both monotonicity-preserving and better than first-order accurate. To get second order without oscillations, the scheme must be nonlinear: its stencil weights must depend on the data. Limiters and WENO weights are exactly that nonlinearity.

### MUSCL: piecewise-linear reconstruction

In 1D, give cell $i$ a slope $\sigma_i$ and evaluate it at the faces:

$$
q^L_{i+1/2} = q_i + \tfrac12\sigma_i,\qquad q^R_{i-1/2} = q_i - \tfrac12\sigma_i .
$$

The unlimited central slope $\sigma_i = \tfrac12(q_{i+1} - q_{i-1})$ is second order but oscillates at jumps. A limiter computes $\sigma_i$ from the one-sided differences $\Delta^- = q_i - q_{i-1}$ and $\Delta^+ = q_{i+1} - q_i$ instead.

<figure markdown>
![minmod reconstruction](../../assets/figures/minmod_reconstruction.svg)
<figcaption>Left: on monotone data minmod picks the smaller one-sided slope, keeping face values within the range of the neighbours. Right: at a local extremum the one-sided slopes have opposite signs, minmod returns zero, and the cell is flat (first order there).</figcaption>
</figure>

### Limiters

All of these return zero when $\Delta^-$ and $\Delta^+$ have opposite signs (a local extremum). When they share a sign:

| Limiter | Slope $\sigma_i$ | Character |
|---|---|---|
| minmod | the smaller of $\Delta^-$, $\Delta^+$ in magnitude | Most dissipative TVD limiter; very robust. |
| van Leer | $\dfrac{2\,\Delta^-\Delta^+}{\Delta^- + \Delta^+}$ (harmonic mean) | Smooth, a common default. |
| MC (monotonized central) | $\operatorname{minmod}\!\big(2\Delta^-,\ \tfrac12(\Delta^-+\Delta^+),\ 2\Delta^+\big)$ | Sharper; uses the central slope when allowed. |
| superbee | larger of $\operatorname{minmod}(2\Delta^-,\Delta^+)$ and $\operatorname{minmod}(\Delta^-,2\Delta^+)$ | Least dissipative TVD limiter; tends to square off smooth peaks. |

### Extremum clipping and the stagnation point

Because every TVD limiter returns zero slope at a local extremum, it clips genuine smooth peaks too. In a reentry flow, stagnation-point quantities (pressure, temperature behind the shock) sit at smooth extrema, so the limiter locally drops to first order exactly where heating is evaluated. This is one reason heat-flux accuracy is so sensitive to limiter choice and grid alignment ([Track 2.4](../../course/track-2.md)).

### Which variables to reconstruct

Reconstruction may act on conservative, primitive or characteristic variables. The update stays conservative in every case, so this choice affects oscillations and positivity, not the shock jump conditions.

**Conservative variables** ($\rho$, $\rho\mathbf u$, $\rho E$) are the simplest, but have a serious positivity problem at high Mach number. Internal energy is $\rho E - \tfrac12\rho|\mathbf u|^2$; at Mach 25 kinetic energy is about 99% of the total, so pressure is a small difference of two large numbers. Limiting each conserved variable independently can easily produce a face state with negative pressure or temperature.

**Primitive variables** ($\rho_s$, $\mathbf u$, $p$, $T$) make positivity much easier to enforce (limit $p$ and $T$ directly) and keep pressure and velocity exactly constant across an isolated contact discontinuity, avoiding spurious pressure oscillations there. This is the common choice in second-order reentry codes and in multiphase codes like MFC, where material interfaces are contacts.

**Characteristic variables** project the jump onto the eigenvectors of the flux Jacobian, $\mathbf w = \mathbf L\,\Delta\mathbf U$, giving one amplitude per wave family. Their advantage shows up where waves overlap: across a shock all primitives jump at once, and limiting each primitive separately treats a mixture of acoustic and entropy content with one slope, which seeds post-shock oscillations, especially at high order. Characteristic limiting limits each family by its own smoothness. The cost is an eigendecomposition per face, and the decoupling is only approximate because the eigenvectors are frozen at the face. High-order WENO codes often use it; second-order production codes usually don't.

## Variants

### First order

Face states equal cell averages. Robust, very dissipative. Standard as a **startup** strategy: run first order until the shock is established, then switch to second order ([Track 3.5](../../course/track-3.md)).

### MUSCL with limiters

Described above. Second order in smooth regions; the workhorse of production reentry codes.

### WENO

Higher order by blending several candidate stencils with smoothness-dependent weights. See [WENO](weno.md).

### Multidimensional and unstructured reconstruction

On unstructured grids, slopes come from least-squares or Green–Gauss gradients, limited by Barth–Jespersen or Venkatakrishnan limiters. *(To be written in Lesson 0.3.)*

## Implications

| Lens | Effect |
|---|---|
| Time step and cost | Cheap for MUSCL; WENO and characteristic projection cost more per face. Limiters that switch on and off can stall steady convergence (limiter "chatter"). |
| Steady vs unsteady | Limiter chatter matters most for steady convergence; some codes freeze the limiter late in a run. |
| Accuracy | Order in smooth regions, clipping at extrema (stagnation point), dissipation in boundary layers; directly affects heat flux. |
| Robustness | Variable choice and limiter strength decide positivity at strong shocks. |
| Physics captured or lost | Dissipative limiters smear shear layers, contacts and instability waves. |
| Hardware / parallel fit | Local, stencil-based; maps well to GPUs. Wider stencils (WENO) mean more halo exchange. |

## In a run

Knobs: spatial order, limiter type, the variable set limited, and sometimes a limiter-freezing iteration. Symptoms: residual stalling at a plateau with a limiter flickering near the shock; post-shock wiggles (too little limiting, or limiting in the wrong variables); smeared heating peaks (too much limiting).

## Which codes

!!! warning "Calibration"
    Code-specific reconstruction details (variable set, limiter defaults) for DPLR, LAURA and US3D are to be filled in from their primary references during Lesson 0.3. MFC reconstructs primitive (optionally characteristic) variables with WENO.

## See also

[The finite-volume pipeline](finite-volume-pipeline.md#2-reconstruct) · [WENO](weno.md) · [Riemann solvers](riemann-solvers.md) · [Conservation form](../foundations/conservation-and-weak-solutions.md)

## References

van Leer (1979); Toro, *Riemann Solvers and Numerical Methods for Fluid Dynamics*; LeVeque, *Finite Volume Methods for Hyperbolic Problems*; Blazek, *Computational Fluid Dynamics*. See the [bibliography](../../references.md).
