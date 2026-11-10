---
status: outline
---

# Shock-layer radiation

<div class="page-meta" markdown>
**Chapter:** 13 Shock-layer radiation · **Depth:** [feel], with the scaling and coupling arguments [deep]
</div>

## What it is

Heating of the surface by light emitted from the hot gas between the bow shock and the body. Excited atoms and molecules in the shock layer emit photons; some are absorbed again on the way, the rest reach the wall. A radiation model computes how much is emitted at each point, how it travels through the layer, and how much arrives.

## The problem it solves

Convective heating comes from the thin boundary layer. Radiative heating comes from the whole volume of hot gas, and it behaves differently in three ways that drive design:

- It rises far more steeply with entry speed than convective heating does.
- It **increases** with nose radius (a blunter body has a thicker radiating layer), where convective heating decreases ([stagnation-point heating](../physics/stagnation-point-heating.md#radiative-heating)).
- It can be large on the afterbody, where convective heating is small.

When to include it, by speed and atmosphere, is tabulated in [choosing physical models](../model-selection.md#table-3-by-what-you-want-to-predict): negligible at low-Earth-orbit return speeds, a secondary contribution at lunar return (about 11 km/s), comparable to or larger than convection above about 12 km/s, and significant from about 7 km/s in a CO₂ atmosphere.

## How it works

*(Outline. Planned sections, with what each will establish.)*

### What radiates

Atomic lines and continua of N and O, molecular bands (N₂, N₂⁺, NO, and CN and C₂ where carbon is present, CO and CO₂ at Mars); why emission depends on the populations of excited electronic states, and so on the electron temperature and density ([ionization, electrons and plasma](../thermo/ionization-and-electrons.md)).

### Transport: the equation of radiative transfer

Emission and absorption coefficients; intensity along a line of sight; optically thin and optically thick limits. The **tangent-slab** approximation (treat the shock layer as an infinite slab normal to the wall and integrate along the wall normal) against full three-dimensional ray tracing.

### Spectral models

Line-by-line (resolve every line: accurate and expensive), band and smeared-band models (average over spectral intervals: cheap enough to couple).

### Nonequilibrium radiation

Behind the shock the excited-state populations are not in a Boltzmann distribution at any temperature. Quasi-steady-state models compute them from the rates of the populating and depopulating processes. This is where radiation prediction is most uncertain.

### Coupling: radiative cooling and the Goulard number

Energy radiated away cools the shock layer, which lowers the emission. The Goulard number compares the radiative flux leaving the layer with the kinetic energy flux entering it and says when the flow and the radiation must be solved together. Coupling alone lowered radiative heating by 30–60% for Apollo 4 (10.24 km/s) and for a 15.24 km/s Mars-return case (Johnston, Gnoffo & Sutton 2009).

### Ablation products

Carbon-bearing species from an ablating heat shield absorb radiation in the boundary layer and emit their own: 20% blowing lowered the radiative flux by about 40% in the same study.

### Engineering correlations

The radiative counterparts of Sutton–Graves (Tauber & Sutton 1991), with their ranges of validity.

## Variants

Uncoupled (post-processed on a converged flow solution) and coupled; tangent-slab and ray-tracing; line-by-line and band models; equilibrium and nonequilibrium populations.

## Typical values

- Onset speeds: above about 10 km/s for Earth entry, about 7 km/s for Mars entry ([choosing physical models](../model-selection.md)).
- Reduction from coupling: 30–60% (Apollo 4 and a Mars-return case; Johnston, Gnoffo & Sutton 2009).
- Reduction from 20% ablation blowing: about 40% (same source).
- Correlation coefficients and Goulard-number thresholds: to be added from the sources below.

## Trade-offs

To be written: spectral resolution against cost; uncoupled against coupled; tangent-slab against ray tracing on afterbodies.

## Effects on stability and robustness

To be written: the radiative source term in the energy equations and how coupled codes under-relax it.

## Implications

| Lens | Effect |
|---|---|
| Time step and cost | A line-by-line calculation along one line of sight can cost as much as the flow solution; coupled runs repeat it every few hundred flow iterations. |
| Steady vs unsteady | Treated as quasi-steady at each trajectory point. |
| Accuracy (heat flux, pressure) | A separate heat-flux contribution with larger uncertainty than the convective one, dominated by nonequilibrium populations. Pressure is unaffected. |
| Robustness | Coupling needs under-relaxation. |
| Physics captured or lost | Leaving it out under-predicts heating at high speed: one of the few unsafe omissions ([choosing physical models](../model-selection.md#what-goes-wrong-if-you-leave-it-out)). |
| Hardware / parallel fit | Lines of sight are independent, so the transport calculation parallelizes trivially. |

## In a run

To be written. Starting point: radiation is usually computed along the stagnation line first, uncoupled, to decide whether a coupled calculation is warranted.

## Which codes

NEQAIR (line-by-line, post-processing flow solutions, typically from DPLR), HARA (band model, coupled inside LAURA) and NERO (in the Ares framework with US3D): see [radiation solvers](../../codes/index.md#radiation-solvers).

!!! warning "Calibration"
    The pairings are the usual ones described in NASA entry-vehicle papers; the codes are not tied to each other in principle. This page will be written from the NEQAIR documentation and Johnston's HARA papers.

## See also

[Stagnation-point heating](../physics/stagnation-point-heating.md) · [Ionization, electrons and plasma](../thermo/ionization-and-electrons.md) · [Thermal nonequilibrium](../thermo/thermal-nonequilibrium.md) · [Surface energy balance](../walls/surface-energy-balance.md) · [Choosing physical models](../model-selection.md)

## References

Goulard (1961); Tauber & Sutton (1991); Johnston, Hollis & Sutton (2008); Johnston, Gnoffo & Sutton (2009); Park, *Nonequilibrium Hypersonic Aerothermodynamics*, ch. 7–8; Anderson, *Hypersonic and High-Temperature Gas Dynamics*, ch. 18. See the [bibliography](../../references.md).
