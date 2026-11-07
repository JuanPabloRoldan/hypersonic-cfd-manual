---
status: draft
---

# WENO reconstruction

<div class="page-meta" markdown>
**Slot:** Track 0.3 reconstruction · **Depth:** [deep] · **Taught in:** [Lesson 0.3](../../course/track-0/0-3-reconstruction.md) (pending)
</div>

## What it is

Weighted essentially non-oscillatory (WENO) reconstruction builds the face value as a weighted blend of several lower-order candidate polynomials, each on a different stencil. In smooth regions the weights reproduce a single high-order stencil; near a discontinuity, stencils that cross it get almost zero weight. It is the nonlinear, high-order cousin of [MUSCL with limiters](reconstruction.md).

## The problem it solves

MUSCL limiters are at most second order and clip smooth extrema. WENO reaches fifth order (or higher) in smooth flow, degrades gracefully at shocks, and doesn't flatten smooth peaks the way TVD limiters do. That matters for problems where small-amplitude waves must survive: transition, acoustics, turbulence, and multiphase interfaces.

## How it works

### WENO5 (Jiang–Shu)

For the left state at face $i+\tfrac12$, use three 3-cell stencils, $\{i-2,i-1,i\}$, $\{i-1,i,i+1\}$ and $\{i,i+1,i+2\}$, each giving a third-order candidate:

$$
\begin{aligned}
q^{(0)} &= \tfrac16\left(2q_{i-2} - 7q_{i-1} + 11q_i\right),\\
q^{(1)} &= \tfrac16\left(-q_{i-1} + 5q_i + 2q_{i+1}\right),\\
q^{(2)} &= \tfrac16\left(2q_i + 5q_{i+1} - q_{i+2}\right).
\end{aligned}
$$

The **linear weights** $d_0 = \tfrac1{10}$, $d_1 = \tfrac6{10}$, $d_2 = \tfrac3{10}$ combine them into the fifth-order upwind-biased value on the full 5-cell stencil.

**Smoothness indicators** measure how much each candidate varies:

$$
\begin{aligned}
\beta_0 &= \tfrac{13}{12}(q_{i-2} - 2q_{i-1} + q_i)^2 + \tfrac14(q_{i-2} - 4q_{i-1} + 3q_i)^2,\\
\beta_1 &= \tfrac{13}{12}(q_{i-1} - 2q_i + q_{i+1})^2 + \tfrac14(q_{i-1} - q_{i+1})^2,\\
\beta_2 &= \tfrac{13}{12}(q_i - 2q_{i+1} + q_{i+2})^2 + \tfrac14(3q_i - 4q_{i+1} + q_{i+2})^2.
\end{aligned}
$$

**Nonlinear weights** penalize rough stencils:

$$
\alpha_k = \frac{d_k}{(\varepsilon + \beta_k)^2},\qquad \omega_k = \frac{\alpha_k}{\sum_j\alpha_j},\qquad q^L_{i+1/2} = \sum_k \omega_k\, q^{(k)},
$$

with a small $\varepsilon$ (often $10^{-6}$ or smaller, or scaled with the data) to avoid division by zero. In smooth regions all $\beta_k$ are similar, $\omega_k \to d_k$, and the result is fifth order. If a stencil crosses a shock, its $\beta_k$ is large and its weight collapses.

The right state at the same face is the mirror image, using stencils biased the other way.

## Variants

### WENO-JS

The original Jiang–Shu weights above. Known to lose accuracy at smooth critical points (where the first derivative vanishes), which is precisely the kind of point a stagnation region contains.

### WENO-M and WENO-Z

Modified weights that restore the design order at critical points. WENO-Z (Borges et al.) uses a global smoothness measure $\tau_5 = |\beta_0 - \beta_2|$:

$$
\alpha_k = d_k\left(1 + \left(\frac{\tau_5}{\beta_k + \varepsilon}\right)^p\right),
$$

typically with $p = 1$ or $2$. It is less dissipative than WENO-JS for the same stencil.

### Characteristic-wise WENO

Apply the reconstruction to characteristic variables (projected with the left eigenvectors at the face), then project back. More expensive, but much cleaner near strong shocks. See [which variables to reconstruct](reconstruction.md#which-variables-to-reconstruct).

### Higher orders and targeted variants

WENO7, WENO9 and targeted ENO (TENO) schemes extend the idea with sharper stencil selection. *(Outline: to be expanded.)*

## Implications

| Lens | Effect |
|---|---|
| Time step and cost | More arithmetic per face than MUSCL, plus characteristic projection if used; usually paired with explicit SSP-RK time stepping. |
| Steady vs unsteady | Built for unsteady, wave-resolving work; nonlinear weights flicker and can stall implicit steady convergence. |
| Accuracy | High order in smooth flow and low dissipation, but still has to be paired with a dissipative-enough flux at strong shocks; near-wall heat flux on stretched grids is not automatically better than a well-resolved second-order result. |
| Robustness | Not strictly positivity-preserving without extra limiting; strong hypersonic shocks need care (positivity limiters, characteristic projection). |
| Physics captured or lost | Preserves small-amplitude waves (instability modes, acoustics) that MUSCL limiters damp. |
| Hardware / parallel fit | Wide but regular stencil; excellent on GPUs with structured data (as in MFC). Halo width grows with order. |

## In a run

Knobs: WENO order, weight variant (JS, M, Z), $\varepsilon$, variable set (primitive or characteristic), and often a fallback to lower order near walls or in low-quality cells. Symptoms: oscillations behind strong shocks (try characteristic projection or a more dissipative flux); excessive dissipation of small waves (try WENO-Z).

## Which codes

MFC uses WENO (several orders, with JS/M/Z-type variants) on primitive variables, with HLLC fluxes and explicit SSP-RK time stepping. US3D and other research codes use high-order or low-dissipation options for DNS of transition; production aeroheating codes (DPLR, LAURA) stay second order. Why they stay there is a [Track 2.7](../../course/track-2.md) topic.

!!! warning "Calibration"
    MFC's option list should be checked against its current documentation; the US3D statement refers to its published DNS/LES work rather than a specific WENO option.

## See also

[Reconstruction and limiters](reconstruction.md) · [Riemann solvers](riemann-solvers.md) · [Central schemes](central-schemes.md) · [MFC](../../codes/mfc.md)

## References

Jiang & Shu (1996); Borges, Carmona, Costa & Don (2008); Shu (1998) lecture notes on ENO/WENO; Pirozzoli (2011). See the [bibliography](../../references.md).
