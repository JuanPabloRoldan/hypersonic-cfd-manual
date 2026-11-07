---
status: draft
---

# Flux-vector splitting

<div class="page-meta" markdown>
**Slot:** Track 0.4 flux functions · **Depth:** [deep] · **Taught in:** [Lesson 0.4](../../course/track-0/0-4-flux-functions.md) (pending); reentry use in [Track 2.3](../../course/track-2.md)
</div>

## What it is

Instead of solving a [Riemann problem](riemann-solvers.md) at the face, **flux-vector splitting** (FVS) splits the flux of each state into a part carried by right-running waves and a part carried by left-running waves, and upwinds each part separately:

$$
\hat{\mathbf F}(\mathbf U_L, \mathbf U_R) = \mathbf F^+(\mathbf U_L) + \mathbf F^-(\mathbf U_R).
$$

## The problem it solves

It gives upwinding with very little logic and, importantly for implicit codes, simple and robust flux Jacobians $\partial\mathbf F^\pm/\partial\mathbf U$. Classic FVS is also naturally resistant to the [carbuncle](shock-instabilities.md), which is part of why it became the backbone of DPLR and US3D.

## How it works

### Steger–Warming {#steger-warming}

The Euler flux is homogeneous of degree one, $\mathbf F = \mathbf A\mathbf U$ with $\mathbf A = \partial\mathbf F/\partial\mathbf U$. Split the eigenvalues by sign, $\lambda^\pm = \tfrac12(\lambda \pm |\lambda|)$, and rebuild:

$$
\mathbf A^\pm = \mathbf R\,\boldsymbol\Lambda^\pm\,\mathbf L,\qquad \mathbf F^\pm = \mathbf A^\pm\mathbf U .
$$

In supersonic flow all eigenvalues share a sign and the flux is fully upwinded. Weaknesses: $|\lambda|$ is not differentiable where an eigenvalue changes sign (sonic points, stagnation regions), producing small glitches; and the scheme is **very dissipative across contacts and shear layers**, so boundary layers are badly smeared unless the grid is very fine. That would ruin heat flux on its own.

### Modified Steger–Warming {#modified-steger-warming}

The fix used in reentry codes evaluates the split Jacobians at an averaged state between the two sides wherever the flow is smooth, which makes the scheme much less dissipative in boundary layers, and reverts to the true Steger–Warming evaluation near shocks, detected by a pressure-gradient sensor. The result keeps the robustness of FVS at shocks while recovering acceptable boundary-layer accuracy.

!!! warning "Calibration"
    The averaging and switching details follow MacCormack & Candler (1989) and the DPLR/US3D literature; exact weights and sensor forms differ between codes and versions. To be pinned down from primary sources in Lesson 0.4 / Track 2.3.

### van Leer

Splits the flux with polynomials in the local Mach number, chosen so $\mathbf F^\pm$ are continuously differentiable through sonic points (removing Steger–Warming's glitches). Still dissipative across contacts and shear layers.

### AUSM family

Liou's Advection Upstream Splitting Method splits the flux into a convective part (a mass flux upwinded with an interface Mach number) and a pressure part (split separately). Variants (AUSM+, AUSM+-up, AUSMPW+, ...) add low-dissipation behaviour in boundary layers, all-speed preconditioning and shock-stability fixes. Contacts are resolved well. Widely used in SU2 and commercial codes. *(Details to be written in Lesson 0.4.)*

## Implications

| Lens | Effect |
|---|---|
| Time step and cost | Cheap; Jacobians of split fluxes are well suited to [implicit relaxation](../time/relaxation-methods.md), a big reason DPLR uses them. |
| Steady vs unsteady | Usable for both; robust steady convergence is the traditional strength. |
| Accuracy | Raw Steger–Warming and van Leer smear boundary layers and heat flux; modified SW and AUSM variants fix much of this. |
| Robustness | Carbuncle-resistant (classic FVS); robust at very strong shocks. |
| Physics captured or lost | Dissipative variants damp contacts, shear layers and instability waves; not a choice for transition DNS without a low-dissipation alternative (see [central schemes](central-schemes.md)). |
| Hardware / parallel fit | Face-local; fine on GPUs. |

## In a run

Knobs: scheme selection; for modified Steger–Warming, the pressure-switch sensitivity. Symptoms: heat flux that keeps changing with wall-normal refinement (too much dissipation); small glitches at sonic lines.

## Which codes

DPLR and US3D use modified Steger–Warming as their base upwind flux (US3D adds low-dissipation KEC options, see [central schemes](central-schemes.md#kinetic-energy-consistent-fluxes)); SU2 and STAR-CCM+ offer AUSM-family schemes.

## See also

[Riemann solvers](riemann-solvers.md) · [Central schemes](central-schemes.md) · [Shock instabilities](shock-instabilities.md) · [DPLR](../../codes/dplr.md) · [US3D](../../codes/us3d.md)

## References

Steger & Warming (1981); van Leer (1982); MacCormack & Candler (1989); Liou & Steffen (1993); Liou (1996, 2006). See the [bibliography](../../references.md).
