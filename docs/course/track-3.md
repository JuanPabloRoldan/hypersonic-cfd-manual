---
status: outline
---

# Track 3: Time integration, convergence and cost

The implications track: how the time-advancement choice shapes what you can compute and what it costs. **Depth:** [deep] unless marked.

| # | Topic | Depth | Reference |
|---|---|---|---|
| 3.1 | Explicit methods: CFL constraint from the smallest cells, convective vs viscous limits and the cell Reynolds number, why explicit is impractical for steady aeroheating but natural for unsteady/DNS and GPUs. | [deep] | [Time-step limits](../reference/time/time-step-limits.md), [explicit methods](../reference/time/explicit-methods.md) |
| 3.2 | Stiffness sources in reentry: wall-normal stretching and high aspect ratio, chemistry, vibrational relaxation. Why they all point toward implicit methods. | [deep] | [Stiff sources](../reference/sources/stiff-sources.md) |
| 3.3 | **DPLR's data-parallel line relaxation** in detail: exact block-tridiagonal solves along wall-normal lines, relaxation sweeps elsewhere, why it kills the dominant stiffness and parallelizes on CPUs; its limits on unstructured grids and GPUs. | [deep] | [Relaxation](../reference/time/relaxation-methods.md#line-relaxation), [DPLR](../codes/dplr.md) |
| 3.4 | Point relaxation (LAURA) and line relaxation explained mechanically; LU-SGS; Gauss–Seidel vs Jacobi; sweep direction in supersonic regions; Newton–Krylov/JFNK and preconditioning; memory, robustness and convergence-rate trade-offs. | [deep] | [Relaxation](../reference/time/relaxation-methods.md), [implicit methods](../reference/time/implicit-methods.md) |
| 3.5 | CFL ramping; **local time stepping** in depth (why it's legal for steady state, why it degrades on high-aspect-ratio grids, explicit LTS + multigrid vs implicit); startup strategies (first order → second order, frozen chemistry first); convergence stalls. | [deep] | [Local time stepping](../reference/time/local-time-stepping.md) |
| 3.6 | Unsteady problems: dual time stepping, time-accurate implicit vs explicit, what's needed for SWBLI unsteadiness, wake dynamics and transition. **Time-accurate LTS and subcycling** (AMR with refluxing, multirate/ADER, sub-stepped local ODEs) and why production reentry codes rarely use them. **The explicit-vs-implicit crossover as a cost model.** | [deep] | [Dual time stepping](../reference/time/dual-time-stepping.md), [explicit vs implicit](../reference/time/explicit-vs-implicit.md) |
| 3.7 | Convergence diagnostics: residuals vs integrated quantities (heat flux, forces); limit cycles; when a converged solution is still wrong. | [deep] | [Convergence diagnostics](../reference/time/convergence-diagnostics.md) |
| 3.8 | GPU porting of reentry codes: why implicit line solves and complex chemistry are hard on GPUs; current directions. Links to the separate CUDA/PMPP course. | [feel] | |
