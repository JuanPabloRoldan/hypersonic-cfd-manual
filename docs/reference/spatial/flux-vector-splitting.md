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

The fix used in DPLR and US3D evaluates the split Jacobians not at each side's own state but at a state averaged between the two sides. In the first-order form given by Subbareddy & Candler (2009),

$$
\hat{\mathbf F}_f = \big(\mathbf R\boldsymbol\Lambda^+\mathbf R^{-1}\big)_f\,\mathbf U_i + \big(\mathbf R\boldsymbol\Lambda^-\mathbf R^{-1}\big)_f\,\mathbf U_{nbr}
= \big(\mathbf R\boldsymbol\Lambda\mathbf R^{-1}\big)_f\,\frac{\mathbf U_i + \mathbf U_{nbr}}{2} - \frac12\big(\mathbf R|\boldsymbol\Lambda|\mathbf R^{-1}\big)_f\,(\mathbf U_{nbr} - \mathbf U_i),
$$

with all matrices evaluated at face-averaged values. That expansion is the key insight: a symmetric (central) part plus a dissipation term $\tfrac12\mathbf R|\boldsymbol\Lambda|\mathbf R^{-1}\Delta\mathbf U$. **If the face average is the Roe average, this is exactly the Roe flux.** The signature flux of DPLR and US3D is, in disguise, a Roe-type upwind flux with a different averaging. In practice $\mathbf U_i$, $\mathbf U_{nbr}$ are replaced by MUSCL face states, and the eigenvalues are smoothed near sonic and stagnation points,

$$
\lambda_k^{\pm} = \tfrac12\Big(\lambda_k \pm \sqrt{\lambda_k^2 + \delta c^2}\Big),\qquad \delta \approx 0.1\text{–}0.2,
$$

an entropy-fix-like modification that keeps the dissipation from vanishing where an eigenvalue crosses zero. The original MacCormack & Candler (1989) form also blends towards true (side-by-side) Steger–Warming near shocks using a pressure-gradient weight, recovering FVS robustness where it matters while keeping boundary-layer dissipation low elsewhere.

US3D's low-dissipation option keeps this dissipation term but multiplies it by a shock-sensor switch and replaces the central part with a [kinetic-energy-consistent flux](central-schemes.md#kinetic-energy-consistent-fluxes).

!!! warning "Calibration"
    The face-averaged form, the expansion and the eigenvalue modification are from Subbareddy & Candler (2009). Exact averaging, the pressure-switch form and default $\delta$ in current DPLR and US3D versions should be checked against code documentation in Track 2.3.

### van Leer

Splits the flux with polynomials in the local Mach number, chosen so $\mathbf F^\pm$ are continuously differentiable through sonic points (removing Steger–Warming's glitches). Still dissipative across contacts and shear layers.

### AUSM family

Liou's Advection Upstream Splitting Method splits the flux into a convective part (a mass flux upwinded with an interface Mach number) and a pressure part (split separately). Variants (AUSM+, AUSM+-up, AUSMPW+, ...) add low-dissipation behaviour in boundary layers, all-speed preconditioning and shock-stability fixes. Contacts are resolved well. Widely used in SU2 and commercial codes. *(Details to be written in Lesson 0.4.)*

### Flux splitting for finite-difference WENO

High-order finite-difference codes (the Shu–Osher approach, as in ALPACA's and JAX-Fluids' "flux splitting" solver type) reconstruct *fluxes* rather than states. The flux at each point is split, $f^\pm = \tfrac12(f \pm \alpha u)$, usually in characteristic variables, and $f^+$ and $f^-$ are reconstructed with left- and right-biased WENO stencils. The choice of $\alpha$ names the scheme:

- **Global Lax–Friedrichs (GLF):** $\alpha$ = the maximum wave speed over the whole domain (per characteristic field). Most dissipative, most robust, and smooth in the data (good for formal accuracy).
- **Local Lax–Friedrichs (LLF):** $\alpha$ = the maximum over the local stencil. Less dissipative.
- **Roe-type splitting:** $\alpha = |\lambda|$ of each characteristic field, upwinding each field by its own speed, with a fallback to LLF where the eigenvalue changes sign (entropy fix).
- **Low-Mach variants (Roe-M, LLF-M):** limit the acoustic $\alpha$ to $\phi\,|u|$ at low face-normal Mach number, which cures grid-aligned shock instabilities; see [low-Mach corrections](low-mach-corrections.md#roe-m).

Codes using this approach often add a positivity-preserving fallback flux (an HLLC or HLL flux computed from first-order states) where the high-order split flux would produce negative density or pressure; see [positivity safeguards](riemann-solvers.md#positivity-safeguards).

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

[Riemann solvers](riemann-solvers.md) · [Central schemes](central-schemes.md) · [Shock instabilities](shock-instabilities.md) · [DPLR](../../codes/index.md#dplr) · [US3D](../../codes/index.md#us3d)

## References

Steger & Warming (1981); van Leer (1982); MacCormack & Candler (1989); Subbareddy & Candler (2009); Shu & Osher (1988); Liou & Steffen (1993); Liou (1996, 2006). See the [bibliography](../../references.md).
