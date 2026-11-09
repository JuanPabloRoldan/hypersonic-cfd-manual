---
status: draft
---

# Riemann solvers

<div class="page-meta" markdown>
**Slot:** Track 0.4 flux functions · **Depth:** [deep] · **Taught in:** [Lesson 0.4](../../course/track-0/0-4-flux-functions.md) (pending)
</div>

## What it is

A **numerical flux function** turns the two reconstructed face states $\mathbf U_L$, $\mathbf U_R$ into one flux $\hat{\mathbf F}(\mathbf U_L, \mathbf U_R)$ for the [conservative update](../foundations/conservation-and-weak-solutions.md#the-lax-wendroff-theorem). **Riemann solvers** are the family that does this by solving, exactly or approximately, the **Riemann problem**: the evolution of an initial discontinuity between two constant states. Other families split the flux by eigenvalue sign ([flux-vector splitting](flux-vector-splitting.md)) or use central differences plus dissipation ([central schemes](central-schemes.md)).

## The problem it solves

At a face, the two sides disagree. Physics resolves the disagreement by waves: for the Euler equations, a left acoustic wave, a contact (entropy and shear) wave, and a right acoustic wave, separating four constant states. Using that wave structure to decide the face flux gives upwinding that respects the [hyperbolic character](../foundations/mathematical-character.md#hyperbolic) of the equations, which is what makes shock capturing stable.

## How it works

All the approximate solvers below can be read as "central flux minus dissipation":

$$
\hat{\mathbf F} = \tfrac12\big(\mathbf F_L + \mathbf F_R\big) - \tfrac12\,\mathbf D\,(\mathbf U_R - \mathbf U_L),
$$

and they differ in the dissipation matrix $\mathbf D$: how much each wave family is damped. That single difference explains most of their behaviour: contact resolution, boundary-layer smearing, positivity and carbuncle susceptibility.

## Variants

### Exact (Godunov)

Solve the full nonlinear Riemann problem (an iteration for the star-region pressure) and evaluate the flux at the face. The reference standard; expensive and awkward for real-gas mixtures, so rarely used in production reentry codes.

### Roe

Linearize around a special average state so the linear problem is exact for isolated discontinuities:

$$
\hat{\mathbf F}_{\text{Roe}} = \tfrac12(\mathbf F_L + \mathbf F_R) - \tfrac12\sum_k |\tilde\lambda_k|\,\tilde\alpha_k\,\tilde{\mathbf r}_k ,
$$

with eigenvalues $\tilde\lambda_k$, eigenvectors $\tilde{\mathbf r}_k$ and wave strengths $\tilde\alpha_k$ evaluated at Roe averages, for a perfect gas

$$
\tilde u = \frac{\sqrt{\rho_L}u_L + \sqrt{\rho_R}u_R}{\sqrt{\rho_L} + \sqrt{\rho_R}},\qquad \tilde H = \frac{\sqrt{\rho_L}H_L + \sqrt{\rho_R}H_R}{\sqrt{\rho_L} + \sqrt{\rho_R}},\qquad \tilde a^2 = (\gamma - 1)\big(\tilde H - \tfrac12\tilde u^2\big).
$$

Reacting mixtures need a generalized Roe average (the pressure derivatives depend on composition).

**Strengths:** resolves stationary contacts and shear layers exactly, so boundary layers suffer little numerical dissipation. **Weaknesses:** admits expansion shocks at sonic points (needs an **entropy fix**, e.g. Harten's, which replaces $|\lambda|$ by $(\lambda^2 + \delta^2)/2\delta$ when $|\lambda| < \delta$); not positivity-preserving in strong expansions; prone to the [carbuncle](shock-instabilities.md). The entropy-fix parameter $\delta$ is a real knob in hypersonic runs, and it affects heating.

### HLL

Assume only two waves with speeds $S_L < S_R$ and one averaged state between them:

$$
\hat{\mathbf F}_{\text{HLL}} = \frac{S_R\,\mathbf F_L - S_L\,\mathbf F_R + S_L S_R\,(\mathbf U_R - \mathbf U_L)}{S_R - S_L}
$$

for $S_L < 0 < S_R$ (otherwise take the upwind flux). The result depends on how $S_L$ and $S_R$ are estimated; see [wave-speed estimates](#wave-speed-estimates).

**Strengths:** positivity-preserving with suitable wave speeds; carbuncle-resistant; simple and robust. **Weaknesses:** the contact and shear waves are lost inside the averaged state, so contacts and **boundary layers are smeared**, which degrades heat flux on practical grids.

### HLLE

HLL with Einfeldt's wave-speed estimates (the Roe-averaged bounds above), chosen so the scheme is positivity-preserving.

### HLLC

Restore the missing **C**ontact: three waves $S_L < S_* < S_R$ and two star states. The contact speed is

$$
S_* = \frac{p_R - p_L + \rho_L u_L(S_L - u_L) - \rho_R u_R(S_R - u_R)}{\rho_L(S_L - u_L) - \rho_R(S_R - u_R)},
$$

and each star state is

$$
\mathbf U_{*K} = \rho_K\,\frac{S_K - u_K}{S_K - S_*}
\begin{bmatrix} 1 \\ S_* \\ v_K \\ w_K \\ \dfrac{E_K}{\rho_K} + (S_* - u_K)\left(S_* + \dfrac{p_K}{\rho_K(S_K - u_K)}\right)\end{bmatrix},\qquad K = L, R,
$$

with species densities scaled by the same factor (mass fractions are carried through the contact unchanged). The flux is $\mathbf F_K + S_K(\mathbf U_{*K} - \mathbf U_K)$ in the star region on side $K$.

**Strengths:** resolves contacts and shear layers like Roe, but positivity-preserving with suitable wave speeds and needs no entropy fix; species and extra scalars ride the contact trivially. **Weaknesses:** like Roe, prone to the carbuncle at strong shocks aligned with the grid.

### HLLC-LM

A shock-stable, *lower*-dissipation HLLC (Fleischmann, Adami & Adams, 2020). HLLC is rewritten in an equivalent central form whose dissipation splits into acoustic and contact parts; the acoustic wave speeds are then scaled down smoothly where the face-normal Mach number is below 0.1. Because the transverse faces at a grid-aligned shock are exactly such faces, this removes the carbuncle without adding dissipation. Full formulas on [low-Mach corrections](low-mach-corrections.md#hllc-lm).

### Rusanov (local Lax–Friedrichs)

One wave speed $S = \max(|u_L| + a_L,\ |u_R| + a_R)$ for everything:

$$
\hat{\mathbf F} = \tfrac12(\mathbf F_L + \mathbf F_R) - \tfrac12 S\,(\mathbf U_R - \mathbf U_L).
$$

Most dissipative, very robust, cheapest. Often used as a fallback in difficult cells.

### Summary

| Solver | Contacts and shear | Positivity | Entropy fix needed | Carbuncle | Cost |
|---|---|---|---|---|---|
| Exact | exact | yes | no | prone | high |
| Roe | exact | no | yes | prone | medium |
| HLL / HLLE | smeared | yes (HLLE) | no | resistant | low |
| HLLC | resolved | yes (suitable speeds) | no | prone (worse in 3D) | low–medium |
| HLLC-LM | resolved | as HLLC | no | resistant | low–medium |
| Rusanov | heavily smeared | yes | no | resistant | lowest |

The pattern is the classical trade-off of hypersonic flux design: **the dissipation that smears contacts and boundary layers is the same dissipation that suppresses the carbuncle.** Hybrid and rotated solvers, and dissipation applied only at shocks, try to get both. A newer line of work argues the trade-off is partly false: the carbuncle is driven by *mis-scaled* acoustic dissipation at low face-normal Mach numbers, so it can be cured by reducing dissipation there ([HLLC-LM](#hllc-lm), [low-Mach corrections](low-mach-corrections.md)). See [shock instabilities](shock-instabilities.md) and [Track 2.2–2.3](../../course/track-2.md).

## Wave-speed estimates

HLL-family solvers (HLL, HLLE, HLLC, HLLC-LM) need estimates $S_L$, $S_R$ of the fastest left- and right-running signals. Too small and the scheme loses positivity or stability, because a real wave falls outside the fan; too large and it adds dissipation. The common choices, with $c$ the sound speed:

| Estimate | $S_L$, $S_R$ | Notes |
|---|---|---|
| Rusanov | $\mp\max(\lvert u_L\rvert  + c_L,\ \lvert u_R\rvert  + c_R)$ | Symmetric and largest; most dissipative. |
| Davis (1988) | $S_L = \min(u_L - c_L,\ u_R - c_R)$, $S_R = \max(u_L + c_L,\ u_R + c_R)$ | Simple and cheap. A cruder variant uses $u_L - c_L$ and $u_R + c_R$ only. |
| Einfeldt (1988) | $S_L = \min(u_L - c_L,\ \hat u - \hat c)$, $S_R = \max(u_R + c_R,\ \hat u + \hat c)$, with Roe-averaged $\hat u$ and $\hat c^2 = \dfrac{\sqrt{\rho_L}c_L^2 + \sqrt{\rho_R}c_R^2}{\sqrt{\rho_L} + \sqrt{\rho_R}} + \dfrac12\dfrac{\sqrt{\rho_L\rho_R}}{(\sqrt{\rho_L} + \sqrt{\rho_R})^2}(u_R - u_L)^2$ | The HLLE choice; makes HLL positivity-preserving for the Euler equations. The usual default. |
| Arithmetic (Coralic & Colonius 2014) | as Einfeldt, with arithmetic averages $\bar u$, $\bar c$ instead of Roe averages | Used in multiphase codes, where Roe averages are awkward. |
| Toro, pressure-based (Toro et al. 1994) | $S_L = u_L - c_L q_L$, $S_R = u_R + c_R q_R$, with $q_K = \sqrt{1 + \tfrac{\gamma + 1}{2\gamma}(p_*/p_K - 1)}$ if $p_* > p_K$ (a shock on that side), else 1 | Estimates the star pressure $p_*$ first (e.g. two-rarefaction or linearized solvers). Tighter bounds and less dissipation, but tied to a $\gamma$-law EOS; needs an effective $\gamma$ for reacting mixtures. |

For HLLC, the contact speed $S_*$ then follows from the Batten et al. (1997) formula in the [HLLC section](#hllc). For reacting multi-temperature air, the sound speed in all of these is the [frozen sound speed](../foundations/mathematical-character.md#hyperbolic).

## Positivity safeguards

Strong expansions (capsule shoulders and wakes, near-vacuum regions) and strong shocks can drive density, pressure or temperature negative at a face or in an update even when the flux function itself is positivity-preserving, because high-order reconstruction can produce non-physical face states. Codes guard against this at three levels:

- **At the face states.** Check reconstructed $\rho$, $p$ (and species densities, $T$, $T_v$) and fall back to lower-order reconstruction where they are non-physical, or scale the reconstruction towards the cell average (Zhang–Shu-type limiting).
- **At the flux.** A *positivity-preserving flux limiter* blends the high-order flux with a first-order positive flux (HLL/HLLC with Einfeldt speeds, or Rusanov) just enough to keep the updated cell positive (Hu, Adams & Shu, 2013). ALPACA's "Riemann solver for positivity under flux splitting" is this fallback flux.
- **After the update (a posteriori).** If a cell ends up non-physical, recompute it with a lower-order, more robust scheme (MOOD-type detection).

Density and pressure floors (for example $10^{-7}$ in ALPACA) are the last line of defence, not a fix. Frequent triggering usually signals a resolution or startup problem.

## Implications

| Lens | Effect |
|---|---|
| Time step and cost | All are explicit-CFL-compatible; implicit codes also need the flux Jacobian, which is simpler for some solvers (and often approximated). |
| Steady vs unsteady | All usable for both; entropy fixes and wave-speed switches can cause limit cycles in steady convergence. |
| Accuracy | Contact-resolving solvers (Roe, HLLC) give much better boundary layers and heat flux on a given grid than HLL/Rusanov. |
| Robustness | HLL-family is positivity-preserving and carbuncle-resistant; Roe needs fixes. |
| Physics captured or lost | HLL loses the contact and shear waves; Roe and HLLC keep them. |
| Hardware / parallel fit | Face-local, branch-light; all map well to GPUs. |

## In a run

Knobs: flux scheme, entropy-fix coefficient, wave-speed estimate. Symptoms: carbuncle (a spurious protrusion of the bow shock at the stagnation line), expansion shocks at sonic points, negative pressure in strong expansions (wake), and heat flux that changes noticeably with the flux choice on the same grid.

## Which codes

LAURA uses Roe's scheme with Yee-type TVD limiting and an entropy fix; MFC defaults to HLLC (HLL and an exact solver are available); [ALPACA](../../codes/index.md#alpaca) offers HLLC, HLLC-LM, HLL and Rusanov with a choice of wave-speed estimates; STAR-CCM+ offers Roe and AUSM+ options. DPLR and US3D use [modified Steger–Warming](flux-vector-splitting.md#modified-steger-warming) rather than a Riemann solver.

!!! warning "Calibration"
    These assignments follow the codes' published descriptions; defaults and options change between versions. Verify against current user manuals before relying on them.

## See also

[Flux-vector splitting](flux-vector-splitting.md) · [Central schemes](central-schemes.md) · [Shock instabilities](shock-instabilities.md) · [Reconstruction](reconstruction.md) · [The finite-volume pipeline](finite-volume-pipeline.md#3-inviscid-flux)

## References

Toro, *Riemann Solvers and Numerical Methods for Fluid Dynamics* (the standard reference for all of the above); Roe (1981); Harten, Lax & van Leer (1983); Davis (1988); Einfeldt (1988); Toro, Spruce & Speares (1994); Batten et al. (1997); Quirk (1994); Coralic & Colonius (2014); Hu, Adams & Shu (2013); Fleischmann, Adami & Adams (2020). See the [bibliography](../../references.md).
