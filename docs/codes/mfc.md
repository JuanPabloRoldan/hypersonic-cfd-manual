---
status: draft
---

# MFC (the contrast case)

**Multi-component Flow Code**: open-source, GPU-first solver for compressible multiphase flows. Not a reentry code, which is exactly why it's here: it makes nearly the opposite choice from production aeroheating codes in almost every slot, and each contrast explains why both are right for their problems.

## Track 0 choices, against a production reentry code

| Slot | MFC | Typical reentry code (DPLR/LAURA-class) | Why they differ |
|---|---|---|---|
| Governing equations | Multiphase five- or six-equation models; nonconservative volume-fraction equation | Single-phase reacting multi-temperature Navier–Stokes, fully conservative | Different physics; see [nonconservative systems](../reference/foundations/conservation-and-weak-solutions.md#nonconservative-systems) |
| Closures | Stiffened-gas EOS per phase, mixture rules | Thermally perfect mixture, finite-rate chemistry, two temperatures | [Closing the system](../reference/foundations/closing-the-system.md) |
| Discretization | Structured, near-uniform grids | Structured or unstructured, extremely stretched at the wall | Heat flux needs wall-resolved cells |
| Reconstruction | WENO (high order) on primitive variables | Second-order MUSCL | [WENO](../reference/spatial/weno.md) keeps waves; production codes value robustness and steady convergence |
| Inviscid flux | HLLC (also HLL, exact); or IGR | Modified Steger–Warming or Roe | Contacts and interfaces vs robust strong shocks |
| Time advancement | Explicit SSP-RK | Implicit relaxation | [Cost model](../reference/time/explicit-vs-implicit.md): acoustics are MFC's physics; steady heating wants unbounded steps |
| Hardware | GPU-first | CPU-first (historically) | Explicit maps naturally to GPUs |

## Information geometric regularization (IGR)

An alternative to shock capturing that MFC supports: rather than reconstructing with limiters and solving Riemann problems, the equations are modified with an additional "entropic pressure," obtained from an elliptic solve each step, which spreads shocks over a controlled width. That allows simple, low-memory central fluxes and made very large GPU runs possible. It replaces the reconstruction-plus-flux slot; it is still explicit and CFL-limited, so it does **not** change the [time-step constraint](../reference/time/explicit-vs-implicit.md#shock-regularization-is-not-a-time-step-loophole).

!!! warning "Calibration"
    Summary of the published idea (Cao & Schäfer) and its use in MFC; check the papers and MFC documentation for the exact formulation and current options.

## References

MFC documentation and papers (Bryngelson et al.; Wilfong et al.); Cao & Schäfer on IGR. See the [bibliography](../references.md).
