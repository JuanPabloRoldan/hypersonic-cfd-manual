# Local time stepping

<div class="page-meta" markdown>
**Chapter:** 9 Time integration and solvers · **Depth:** [deep]
</div>

## What it is

Letting different cells advance with different time steps. For **steady** problems, each cell simply uses its own largest stable step, and time accuracy is abandoned. For **unsteady** problems, special schemes let cells or refinement levels take different steps and resynchronize at shared time levels while keeping the solution time-accurate and conservative.

## The problem it solves

With a single global step, the smallest cell in the domain (a wall cell, typically) dictates the step everywhere. Local time stepping (LTS) lets large cells move at their own pace.

## How it works

### Steady-state LTS

For a steady problem only the final state $\mathbf R(\mathbf U) = 0$ matters, so time is a pseudo-time and any path to the solution is acceptable. Each cell takes

$$
\Delta t_i = \text{CFL}\cdot\frac{V_i}{\sum_{\text{faces}}\big(|u_n| + a\big)A_f + \text{viscous term}},
$$

its own local stability limit. This is standard in essentially every steady solver, explicit or implicit.

### Why it doesn't remove the stiffness

LTS removes the "smallest cell sets the global step" problem, but not the conditioning problem. A wall cell might have aspect ratio $\Delta x/\Delta y \sim 10^3$–$10^4$, and its local step is set by its small dimension $\Delta y$. A signal travelling along the wall then needs thousands of iterations to cross that one cell in the streamwise direction. In linear-algebra terms the discrete system is badly conditioned: the fastest and slowest error modes differ by orders of magnitude, and explicit iterations damp the slow ones very slowly. Stiff chemistry adds its own fast scales on top.

Explicit schemes with LTS and **multigrid** (Jameson-style) work well for aircraft aerodynamics, but struggle on stretched, reacting hypersonic grids. Implicit methods, and in particular [line relaxation](relaxation-methods.md#line-relaxation) along the stiff direction, attack the conditioning directly. See [explicit vs implicit](explicit-vs-implicit.md).

### Time-accurate LTS and subcycling

Naive LTS (every cell at its own step, never synchronized) destroys time accuracy, because neighbouring cells end up at different physical times. But time-accurate local stepping does exist:

- **AMR subcycling** (Berger–Oliger, Berger–Colella): each refinement level takes steps sized for its own cells; fine levels take several steps per coarse step and synchronize at coarse time levels, with **refluxing** (correcting the coarse cell by the accumulated fine-face fluxes) to keep exact conservation.
- **Multirate and ADER local time stepping**: schemes (common in DG codes) where each element advances with its own step and exchanges time-integrated fluxes with neighbours.
- **Sub-stepped local ODEs**: a cell-local subsystem (stiff chemistry, or a sub-grid bubble's Rayleigh–Plesset/Keller–Miksis equation in a Lagrangian bubble model) is integrated with many adaptive substeps inside one flow step and rejoins the flow at the shared time level. This is time-accurate to the order of the coupling. Adaptive sub-stepping of bubble ODEs in multiphase codes (MFC's bubble models offer this; check its documentation for the current options) is one example, and [operator-split chemistry](../sources/stiff-sources.md#operator-splitting-with-sub-stepped-chemistry) is the reacting-flow version.

!!! warning "Calibration"
    As far as is known here, production reentry codes rarely use time-accurate LTS for unsteady runs; they rely on implicit [dual time stepping](dual-time-stepping.md) instead. To be checked against code documentation.

## Implications

| Lens | Effect |
|---|---|
| Time step and cost | Steady: large speed-up over a global step; doesn't cure aspect-ratio stiffness. Unsteady: subcycling saves work when only a small region needs small steps. |
| Steady vs unsteady | Steady LTS is a pure convergence accelerator. Time-accurate LTS needs synchronization and conservative flux bookkeeping. |
| Accuracy | Steady: none (only the converged state matters). Unsteady: synchronization errors if done naively. |
| Robustness | Steady LTS behaves like a local CFL; too aggressive a local CFL in thin wall cells can destabilize. |
| Physics captured or lost | Steady LTS has no physical transient at all; its intermediate states are meaningless. |
| Hardware / parallel fit | Steady LTS is free; subcycling adds load-balancing and synchronization complexity. |

## In a run

Knobs: "local time stepping on/off," CFL, multigrid levels; for AMR codes, subcycling ratio. Symptoms: an explicit steady run whose residual drops quickly in the shock layer but crawls in the boundary layer (aspect-ratio stiffness).

## Which codes

Steady LTS: essentially all steady solvers (DPLR, LAURA, US3D, FUN3D, SU2). AMR subcycling: block-structured AMR frameworks (Chombo/AMReX-type codes). Sub-stepped local ODEs: MFC's Lagrangian bubbles, operator-split reacting codes.

## See also

[Time-step limits](time-step-limits.md) · [Explicit vs implicit](explicit-vs-implicit.md) · [Relaxation methods](relaxation-methods.md) · [Stiff sources](../sources/stiff-sources.md)

## References

Jameson, Schmidt & Turkel (1981); Berger & Oliger (1984); Berger & Colella (1989); Blazek. See the [bibliography](../../references.md).
