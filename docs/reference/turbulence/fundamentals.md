---
status: outline
---

# Turbulence fundamentals and averaging

<div class="page-meta" markdown>
**Chapter:** 4 Turbulence · **Depth:** [feel]
</div>

## What it is

The vocabulary and the exact equations that every turbulence model and every scale-resolving simulation starts from: the range of scales in a turbulent flow and how energy moves between them, the averaged equations (Reynolds and Favre) with the unclosed terms they leave behind, the turbulent kinetic energy budget including its compressible terms, and the structure of a turbulent boundary layer in wall units.

## The problem it solves

Without this page, the other turbulence pages can't say precisely what a model is modelling or what a simulation must resolve. It defines the terms that [RANS models](rans-models.md) close, the scales that [DNS and LES](scale-resolving.md) must resolve, and the hypotheses ([Morkovin](../physics/turbulence-modeling.md#morkovins-hypothesis-and-its-limits)) that let incompressible results be carried over to hypersonic boundary layers.

## How it works

*(Outline. Planned sections, with what each will establish.)*

### Scales and the energy cascade

- Large, energy-containing eddies of size $\ell$ (of order the boundary-layer thickness $\delta$) receive energy from the mean shear; energy passes to smaller eddies until viscosity dissipates it at the Kolmogorov scale $\eta = (\nu^3/\varepsilon)^{1/4}$, with $\nu$ the kinematic viscosity and $\varepsilon$ the dissipation rate.
- The scale ratio $\ell/\eta \sim Re_\ell^{3/4}$ and its consequence for grid size in 3D (the origin of DNS cost, carried to [DNS](scale-resolving.md#direct-numerical-simulation)).
- Kolmogorov's hypotheses and the inertial range; the $k^{-5/3}$ spectrum as a check on LES spectra.
- Figure to draw: energy spectrum with the production, inertial and dissipation ranges, marking what RANS, LES and DNS each resolve.

### Reynolds and Favre averaging

- Reynolds decomposition $u = \bar u + u'$ and the Reynolds stress $-\rho\overline{u_i'u_j'}$ it leaves in the momentum equation.
- Why variable-density flow uses **Favre** (density-weighted) averaging, $\tilde u = \overline{\rho u}/\bar\rho$, $u = \tilde u + u''$: it removes density–velocity correlations from the continuity and convective terms, so the averaged equations look like the laminar ones plus a few unclosed terms. Show the averaged continuity and momentum equations side by side in both forms.
- The full list of unclosed terms in the Favre-averaged energy equation (turbulent heat flux, turbulent diffusion of kinetic energy, pressure–velocity and viscous correlations) and which ones codes keep.
- Misconception to meet: Favre averaging doesn't make compressibility effects disappear; it moves them into terms that are usually neglected.

### The turbulent kinetic energy budget

- Transport equation for $k = \tfrac12\widetilde{u_i''u_i''}$: production, dissipation, turbulent and viscous diffusion, pressure diffusion.
- Compressible additions: pressure–dilatation, dilatational dissipation, and the mass-flux term $\overline{u_i''}\,\partial\bar p/\partial x_i$. Where they matter (high turbulent Mach number $M_t = \sqrt{2k}/\bar a$, shock–turbulence interaction) and where they don't (attached boundary layers), with values from hypersonic boundary-layer DNS (Duan, Beekman & Martin 2010, 2011).
- Why production at a shock is the weak point of every eddy-viscosity model ([shock/boundary-layer interaction](../physics/shock-boundary-layer-interaction.md#trade-offs)).

### Wall turbulence in wall units

- Friction velocity $u_\tau = \sqrt{\tau_w/\rho_w}$, viscous length $\nu_w/u_\tau$, $y^+$, $u^+$; viscous sublayer, buffer layer, log layer, wake region.
- Grid spacings in wall units ($\Delta x^+$, $y^+_1$, $\Delta z^+$) as the common language of RANS, LES and DNS resolution requirements ([scale-resolving methods](scale-resolving.md#resolution-requirements)).
- Compressible transformations (van Driest, Trettel–Larsson) that map hypersonic profiles onto the incompressible law of the wall; how cold walls stretch them ([hypersonic modeling](../physics/turbulence-modeling.md#morkovins-hypothesis-and-its-limits)).

### Compressibility: Morkovin and the strong Reynolds analogy

- Morkovin's hypothesis stated with its range of validity in terms of $M_t$ and fluctuating Mach number.
- The strong Reynolds analogy linking temperature and velocity fluctuations, and its modified forms for cold walls (Huang, Coleman & Bradshaw 1995).
- Turbulent heat flux and the turbulent Prandtl number as its closure; the Reynolds analogy factor $2St/C_f$ that links heating to skin friction.

## Variants

Not a method with variants. Neighbouring concepts to tell apart on the page: Reynolds vs Favre averaging; ensemble vs time averaging (and why a statistically steady RANS is not a time average of an unsteady flow); filtering (LES) vs averaging (RANS).

## Typical values

To be sourced: Kolmogorov and viscous length scales for a capsule boundary layer at peak heating (illustrative computation from free-stream conditions); $M_t$ and the relative size of compressible budget terms from Mach 3–12 DNS (Duan et al.); log-law constants and their scatter (Pope, ch. 7).

## Trade-offs

Not applicable at the level of this page; the trade-offs are in the choice of averaging or filtering, listed on [RANS models](rans-models.md#trade-offs) and [scale-resolving methods](scale-resolving.md#trade-offs).

## Effects on stability and robustness

Not applicable (no algorithm). The numerical consequences of each unclosed term are on the model pages.

## Implications

| Lens | Effect |
|---|---|
| Time step and cost | Scale ratio $\ell/\eta \sim Re^{3/4}$ sets the cost of resolving turbulence. |
| Steady vs unsteady | Averaging produces a steady problem; filtering does not. |
| Accuracy (heat flux, pressure) | Heat flux depends on the turbulent heat flux closure and on near-wall structure in wall units. |
| Robustness | — |
| Physics captured or lost | Averaging discards all fluctuation information except what the closure carries. |
| Hardware / parallel fit | — |

## In a run

Planned: computing $y^+_1$ for a wall-resolved heating grid from a laminar or RANS solution (worked example), and checking $M_t$ in a solution to decide whether compressible corrections could matter.

## Which codes

All finite-volume reentry codes solve the Favre-averaged equations when a turbulence model is on; see [RANS models](rans-models.md#which-codes).

## See also

[RANS models](rans-models.md) · [Scale-resolving methods](scale-resolving.md) · [Hypersonic boundary layers](../physics/turbulence-modeling.md) · [Transition](transition.md) · [Governing equations](../foundations/governing-equations.md)

## References

Pope, *Turbulent Flows* (2000), chs. 2–7; Wilcox, *Turbulence Modeling for CFD* (2006); Gatski & Bonnet (2013); Smits & Dussauge (2006); Favre (1965); Kolmogorov (1941); Morkovin (1962); Huang, Coleman & Bradshaw (1995); Duan, Beekman & Martin (2010, 2011); van Driest (1951); Trettel & Larsson (2016). See the [bibliography](../../references.md).
