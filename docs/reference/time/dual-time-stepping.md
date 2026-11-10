---
status: outline
---

# Dual time stepping

<div class="page-meta" markdown>
**Chapter:** 9 Time integration and solvers · **Depth:** [deep]
</div>

## What it is

A time-accurate implicit method: discretize physical time with a backward difference (typically second-order BDF2), and at each physical step converge the resulting nonlinear system by iterating in a fictitious pseudo-time, with all the steady-state accelerators (local pseudo-time steps, relaxation, multigrid).

## The problem it solves

It lets an implicit steady-state solver do unsteady problems with a physical step chosen for the physics, not for stability. See the [cost model](explicit-vs-implicit.md).

## How it works

*(Outline.)*

$$
V\,\frac{3\mathbf U^{n+1} - 4\mathbf U^n + \mathbf U^{n-1}}{2\Delta t} + \mathbf R(\mathbf U^{n+1}) = 0,
$$

solved for $\mathbf U^{n+1}$ by subiterations in pseudo-time $\tau$.

## Variants

*(To be filled.)*

## Implications

*(To be filled: subiteration count vs accuracy; what's needed for SWBLI unsteadiness and wake dynamics.)*

## In a run

*(To be filled.)*

## Which codes

*(To be filled.)*

## See also

[Implicit methods](implicit-methods.md) · [Explicit vs implicit](explicit-vs-implicit.md) · [Local time stepping](local-time-stepping.md)

## References

Jameson (1991). See the [bibliography](../../references.md).
