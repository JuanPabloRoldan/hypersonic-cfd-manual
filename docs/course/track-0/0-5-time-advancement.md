---
status: outline
---

# Lesson 0.5: Time advancement and iteration

<div class="page-meta" markdown>
**Slot:** time advancement · **Depth:** [deep] · **Reference pages:** [time-step limits](../../reference/time/time-step-limits.md), [explicit methods](../../reference/time/explicit-methods.md), [implicit methods](../../reference/time/implicit-methods.md), [relaxation](../../reference/time/relaxation-methods.md), [local time stepping](../../reference/time/local-time-stepping.md), [explicit vs implicit](../../reference/time/explicit-vs-implicit.md), [dual time stepping](../../reference/time/dual-time-stepping.md)
</div>

## Planned content

1. Explicit: forward Euler, SSP Runge–Kutta, stability limits (von Neumann), CFL.
2. Implicit: backward Euler, linearization, residual Jacobians; steady state as pseudo-time; Newton as $\Delta t \to \infty$; defect correction.
3. Approximate linear solvers: point relaxation (Jacobi, Gauss–Seidel), line relaxation, LU-SGS, Newton–Krylov and JFNK, preconditioning.
4. Local time stepping for steady state; dual time stepping for unsteady.
5. The explicit-vs-implicit cost model, made quantitative.
6. MFC contrast: explicit SSP-RK on GPUs.

## Already previewed

The two Jacobians, the time-step limits and cell Reynolds number, local time stepping (steady and time-accurate), relaxation, and the cost model were all covered in Lesson 0.1's follow-ups. This lesson consolidates them and goes deeper; Track 3 goes deeper still.

## Checkpoint (planned themes)

Why the converged steady answer doesn't depend on the implicit left-hand side; why CFL is ramped; what local time stepping does and doesn't fix.
