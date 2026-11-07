---
status: draft
---

# Point and line relaxation

<div class="page-meta" markdown>
**Slot:** Track 0.5 time advancement; Track 3.3–3.4 · **Depth:** [deep] · **Taught in:** [Track 3](../../course/track-3.md) (pending; previewed in Lesson 0.1)
</div>

## What it is

Iterative ways of approximately solving the implicit system $\big(\tfrac{V}{\Delta t}\mathbf I + \tfrac{\partial\mathbf R}{\partial\mathbf U}\big)\Delta\mathbf U = -\mathbf R$ ([implicit methods](implicit-methods.md)) by solving small pieces of it exactly and iterating over the pieces.

## The problem it solves

The full system is far too large to factor. Relaxation solves exactly the couplings that matter most (within a cell, or along a line of cells) and treats the rest by repeated sweeps. Choosing the right pieces is what makes it converge.

## How it works

### Point relaxation {#point-relaxation}

For each cell, solve its own $n\times n$ diagonal block exactly, moving the neighbour contributions to the right-hand side. Use the neighbours' latest values (**Gauss–Seidel**: sweep through the grid in order) or their old values (**Jacobi**: every cell independently, then update all). Repeat for several sweeps per iteration.

Gauss–Seidel converges faster, and the sweep direction matters: in a supersonic region a sweep aligned with the flow carries information downstream in a single pass, because information really does only travel downstream ([mathematical character](../foundations/mathematical-character.md#mixed-character-around-a-blunt-body)). Jacobi parallelizes trivially but converges more slowly.

### Line relaxation {#line-relaxation}

Take a whole line of cells, typically the wall-normal line from the body to the shock, and solve their coupled system exactly. Each cell couples only to its two neighbours on the line, so the system is **block-tridiagonal** and is solved by a block Thomas algorithm (forward elimination, back substitution) in $O(N_{\text{line}}\,n^3)$ operations. Couplings to cells off the line are lagged and handled by sweeps.

### Why wall-normal lines

The stiffness of an aeroheating grid is concentrated in the wall-normal direction: cells there are tiny ($\Delta n \sim 10^{-6}$ m) and diffusion and acoustics couple them strongly. Along the wall the cells are large and coupling is weak. Solving exactly along wall-normal lines removes the stiffest coupling, and the remaining directions converge well under cheap relaxation sweeps. This is the core idea of **data-parallel line relaxation** (DPLR, Wright, Candler & Bose 1998): within a sweep the lines are independent, so they parallelize cleanly across processors.

*(Track 3.3 covers the DPLR algorithm in detail: the sweep structure, the "data-parallel" choice of Jacobi-like coupling between lines, and its behaviour on unstructured grids and GPUs.)*

## Variants

### LU-SGS

Lower–upper symmetric Gauss–Seidel: an approximate factorization with forward and backward sweeps and a simplified (scalar) diagonal, so no block inversions are needed. Cheap per iteration, slower convergence. *(Track 3.4.)*

### Line-implicit on unstructured grids

Lines built from stacks of prism or hex cells in the boundary layer, with point relaxation elsewhere. Used in FUN3D and US3D.

## Implications

| Lens | Effect |
|---|---|
| Time step and cost | Point relaxation: one $n\times n$ inversion per cell per sweep. Line relaxation: one block-tridiagonal solve per line, with far better convergence on stretched grids. |
| Steady vs unsteady | Primarily steady-state accelerators; used as the inner solver in dual time stepping for unsteady runs. |
| Accuracy | None directly (the residual sets the answer). |
| Robustness | Line solves cure the stiffness of high-aspect-ratio wall cells; point relaxation alone converges slowly there. |
| Physics captured or lost | None directly. |
| Hardware / parallel fit | Gauss–Seidel sweeps and Thomas-algorithm line solves are sequential along their direction, which is awkward on GPUs; Jacobi coupling between lines (the "data-parallel" part) restores parallelism across lines. |

## In a run

Knobs: number of sweeps per iteration, line direction, Jacobi vs Gauss–Seidel coupling. Symptoms: slow convergence in boundary layers when lines are absent or misaligned; good convergence that degrades when the grid isn't line-structured near the wall.

## Which codes

!!! warning "Calibration"
    DPLR: data-parallel line relaxation along wall-normal lines. LAURA: historically point-implicit relaxation; newer versions may offer line-implicit options (check the LAURA user manual). FUN3D and US3D: point and line-implicit relaxation on unstructured grids, with lines in boundary-layer prism stacks. To be verified against primary sources in Track 3.

## See also

[Implicit methods](implicit-methods.md) · [Local time stepping](local-time-stepping.md) · [Explicit vs implicit](explicit-vs-implicit.md) · [DPLR](../../codes/dplr.md)

## References

Wright, Candler & Bose (1998); Gnoffo (1990) on LAURA's point-implicit relaxation; Blazek. See the [bibliography](../../references.md).
