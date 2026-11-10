---
status: outline
---

# Explicit methods

<div class="page-meta" markdown>
**Chapter:** 9 Time integration and solvers · **Depth:** [deep]
</div>

## What it is

The new state is computed directly from the residual of known states: $\mathbf U^{n+1} = \mathbf U^n - \frac{\Delta t}{V}\mathbf R(\mathbf U^n)$ for forward Euler, or a sequence of such stages in a Runge–Kutta scheme. No linear system is solved.

## The problem it solves

Cheap, simple, local and time-accurate. The natural choice when the physics itself needs small steps (acoustics, shocks moving through the domain, turbulence) and on GPUs.

## How it works

*(Outline.)* Each stage is one pass of the [finite-volume pipeline](../spatial/finite-volume-pipeline.md). Stability is governed by the [time-step limits](time-step-limits.md).

## Variants

### Forward Euler
### SSP Runge–Kutta (TVD-RK)

Strong-stability-preserving Runge–Kutta schemes (Shu–Osher RK3 is the classic) keep the non-oscillatory property of the spatial scheme. MFC uses SSP-RK.

### Low-storage Runge–Kutta
### Explicit with multigrid and local time stepping (steady state)

See [local time stepping](local-time-stepping.md).

## Implications

*(To be filled.)* Preview: cost per step is lowest of all methods, number of steps is the issue; see [explicit vs implicit](explicit-vs-implicit.md).

## In a run

*(To be filled.)*

## Which codes

MFC (SSP-RK), Eilmer (explicit option), most DNS codes.

## See also

[Time-step limits](time-step-limits.md) · [Explicit vs implicit](explicit-vs-implicit.md)

## References

Shu & Osher (1988); Gottlieb, Shu & Tadmor (2001). See the [bibliography](../../references.md).
