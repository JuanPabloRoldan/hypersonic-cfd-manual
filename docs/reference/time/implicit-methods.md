# Implicit methods and Jacobians

<div class="page-meta" markdown>
**Slot:** Track 0.5 time advancement; Track 3 · **Depth:** [deep] · **Taught in:** [Lesson 0.1](../../course/track-0/0-1-governing-equations.md) (preview), [Lesson 0.5](../../course/track-0/0-5-time-advancement.md) (pending)
</div>

## What it is

An implicit method evaluates the residual at the *new* state, so each step requires solving a (linearized) system of equations coupling all cells. In exchange, it can take time steps far beyond the explicit [stability limits](time-step-limits.md).

## The problem it solves

Steady aeroheating problems are stiff: tiny wall-normal cells, high aspect ratios, fast chemistry and vibrational relaxation all impose small explicit steps that have nothing to do with the physics of interest. Implicit methods remove those stability limits so the step can be chosen for convergence speed (steady) or for the physical time scale of interest (unsteady).

## How it works

### Two different Jacobians

Two matrices both get called "the Jacobian," and they do different jobs.

The **flux Jacobian** $\mathbf A = \partial\mathbf F/\partial\mathbf U$ is for analysis. It lets you write $\partial_t\mathbf U + \mathbf A\,\partial_x\mathbf U = 0$; its eigenvalues are the wave speeds and its eigenvectors what each wave carries ([mathematical character](../foundations/mathematical-character.md#hyperbolic)). It doesn't produce a solution. Flux functions exploit it: [Roe](../spatial/riemann-solvers.md#roe) linearizes around a Roe-averaged $\mathbf A$, [HLL](../spatial/riemann-solvers.md#hll) uses its extreme eigenvalues as wave-speed bounds, characteristic boundary conditions use its eigenvectors, and the CFL condition uses its largest eigenvalue.

The **residual Jacobian** $\partial\mathbf R/\partial\mathbf U$ is for the implicit update. It is a huge sparse matrix with one $n\times n$ block per cell-neighbour pair (built from neighbours' flux Jacobians and the viscous terms) plus a diagonal block that includes the source Jacobian $\partial\mathbf S/\partial\mathbf U$.

### Backward Euler and its linearization

Backward Euler for the semi-discrete system $V\,d\mathbf U/dt = -\mathbf R(\mathbf U)$ is

$$
V\,\frac{\mathbf U^{n+1} - \mathbf U^n}{\Delta t} = -\mathbf R(\mathbf U^{n+1}).
$$

Linearize $\mathbf R(\mathbf U^{n+1}) \approx \mathbf R(\mathbf U^n) + \frac{\partial\mathbf R}{\partial\mathbf U}\Delta\mathbf U$:

$$
\left(\frac{V}{\Delta t}\,\mathbf I + \frac{\partial\mathbf R}{\partial\mathbf U}\right)\Delta\mathbf U = -\mathbf R(\mathbf U^n).
$$

As $\Delta t\to\infty$ the left-hand matrix becomes $\partial\mathbf R/\partial\mathbf U$ and the update becomes **Newton's method** for $\mathbf R(\mathbf U) = 0$, which converges quadratically near the solution. That is why steady implicit solvers ramp the CFL number up as the solution settles. The $V/\Delta t$ term keeps early iterations stable while the solution is far from converged.

### Solving it approximately

Nobody solves this system exactly. The left-hand side is usually an approximation (often a first-order, more dissipative Jacobian even when the residual is second order: a **defect-correction** strategy), and the linear system is solved approximately by [point or line relaxation](relaxation-methods.md), LU-SGS, or a Krylov method (GMRES) with preconditioning. Because the right-hand side is the true residual, the converged steady solution is unaffected by these approximations; only the convergence rate is.

### Cost scaling with the number of equations

Each block is $n\times n$, with $n$ the number of conserved variables per cell. Memory goes as $n^2$ and block factorizations or inversions as $n^3$. Going from a perfect gas ($n = 5$) to 11-species two-temperature air ($n = 16$) multiplies block-operation cost by roughly $(16/5)^3 \approx 33$, before counting the extra source-Jacobian work. An explicit code pays roughly linearly in $n$. See [explicit vs implicit](explicit-vs-implicit.md).

## Variants

### Steady state via pseudo-time

March $\Delta t\to$ large with local time stepping; time accuracy is irrelevant. See [local time stepping](local-time-stepping.md).

### Time-accurate implicit and dual time stepping

Second-order backward differences in physical time, with inner pseudo-time iterations at each physical step. See [dual time stepping](dual-time-stepping.md).

### Point-implicit sources only

Treat only the sources implicitly and the fluxes explicitly. See [stiff source terms](../sources/stiff-sources.md#point-implicit).

### Newton–Krylov and JFNK

Krylov solvers that need only Jacobian–vector products, which can be approximated by finite differences of the residual (Jacobian-free). *(Track 3.4.)*

## Implications

| Lens | Effect |
|---|---|
| Time step and cost | Removes the stability limit; each iteration costs much more than an explicit step (Jacobian assembly, linear solve), with $n^2$ memory and $n^3$ block cost. |
| Steady vs unsteady | Natural steady-state accelerator; time-accurate with dual time stepping. |
| Accuracy | Converged steady solutions don't depend on the left-hand-side approximation; time-accurate runs need subiteration convergence. |
| Robustness | Large steps can drive the solution through unphysical states early on; CFL ramping and startup strategies matter. |
| Physics captured or lost | Large time steps filter out fast transients by design; fine for steady flow, wrong for wave-resolving physics. |
| Hardware / parallel fit | Global coupling and recursive solves (Gauss–Seidel, line solves) are harder on GPUs than explicit updates. See [Track 3.8](../../course/track-3.md). |

## In a run

Knobs: CFL start value and ramp, Jacobian order, number of relaxation sweeps or Krylov iterations, source treatment. Symptoms: divergence when CFL ramps too fast; stall at a plateau; quadratic convergence at the end when the Jacobian is accurate.

## Which codes

DPLR ([line relaxation](relaxation-methods.md#line-relaxation)), LAURA (point-implicit relaxation), US3D, FUN3D, SU2 and Eilmer (Newton–Krylov option) are all implicit for steady problems. MFC is explicit.

## See also

[Point and line relaxation](relaxation-methods.md) · [Explicit vs implicit](explicit-vs-implicit.md) · [Time-step limits](time-step-limits.md) · [Dual time stepping](dual-time-stepping.md)

## References

Blazek; Hirsch; Wright, Candler & Bose (1998); Knoll & Keyes (2004). See the [bibliography](../../references.md).
