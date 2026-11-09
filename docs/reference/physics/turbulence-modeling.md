---
status: draft
---

# Turbulence modeling for hypersonic boundary layers

<div class="page-meta" markdown>
**Slot:** Track 1.7 (closures for the Reynolds-averaged equations) · **Depth:** [feel]
</div>

## What it is

The models that close the Reynolds- (Favre-) averaged Navier–Stokes equations for turbulent boundary layers at hypersonic Mach numbers: an eddy-viscosity model for the Reynolds stresses, and a model for the turbulent heat flux $\overline{\rho h'' u_i''}$. In entry analysis they matter wherever the boundary layer has transitioned: lunar-return and Mars capsules late in the heat pulse, large heatshields, backshells, and slender vehicles.

## The problem it solves

Turbulent heating can be several times laminar heating, and TPS is sized on it. RANS models were calibrated on incompressible, near-adiabatic flows. Entry boundary layers are the opposite: high Mach number and a **cold wall** (wall temperature far below the recovery temperature, because the TPS reradiates and conducts heat away; wall-to-recovery ratios of 0.2 or below are typical). Strong near-wall gradients of density, viscosity and temperature break the assumptions behind standard models.

## How it works

### Morkovin's hypothesis and its limits

Morkovin's hypothesis says compressible turbulence statistics are essentially incompressible ones once mean density and viscosity variations are accounted for; compressibility transformations (van Driest, Trettel–Larsson, and strong Reynolds analogies) map compressible profiles onto incompressible ones. DNS at Mach 11 and 14 with a cold wall ($T_w/T_r \approx 0.2$; Huang et al.) found these transformations working well over friction Reynolds numbers up to about 1200, supporting the hypothesis in that range. But putting $\rho$ and $\mu$ "inside the derivatives" of a RANS model is not enough for the model to inherit this: Danis & Durbin note that coordinate scaling near the wall is an extra assumption that standard two-equation models don't satisfy.

### Compressibility corrections to two-equation models

Classical corrections (Sarkar, Zeman, Wilcox) add dilatation-dissipation or pressure-dilatation terms to the $k$ equation. Reviews find they don't significantly improve heat transfer in cold-wall hypersonic boundary layers. Danis & Durbin (2022) found instead that $k$–$\omega$ models **over-predict near-wall eddy viscosity as the wall is cooled**, giving low mean velocity and wrong heat transfer. Their correction leaves the $k$ equation alone (it comes from exact kinetic-energy transport) and multiplies the production and destruction terms of the $\omega$ equation (a modeling construct) by a function $f(M, M_\tau, B_q)$ of the local Mach number, a local friction Mach number and a local heat-flux parameter. It tends to 1 as $M \to 0$ and $T_w/T_r \to 1$, is fully local (no wall-distance quantities), applies to any $k$–$\omega$ model, and, tested on DNS for $2.5 \le M \le 14$ and $0.18 \le T_w/T_r \le 1$, collapsed eddy-viscosity profiles and improved velocity, temperature, skin friction and heat-transfer predictions. Because it depends on local Mach number it is not Galilean invariant; $M$ is understood in the frame of the nearest wall.

### Turbulent heat flux: constant Prandtl number vs algebraic energy flux

The standard closure is gradient diffusion with a **constant turbulent Prandtl number**,

$$
\overline{\rho h'' u_i''} \approx -\frac{c_p\,\mu_t}{Pr_t}\frac{\partial \tilde T}{\partial x_i},\qquad Pr_t \approx 0.85\text{–}0.9 .
$$

The Mach 11/14 cold-wall DNS found $Pr_t \approx 0.9$ fits the outer layer ($0.2 < z/\delta < 0.8$), but the assumption fails near the wall, where $Pr_t$ overshoots and even changes sign where the wall-normal turbulent heat flux crosses zero.

The **algebraic energy flux (AEF)** model of Bowersox derives the heat flux vector from a truncated transport equation for the energy flux, so it depends on the Reynolds stresses and both temperature and velocity gradients rather than on one eddy diffusivity. Against data from Mach 0.02 to 11.8 it improved temperature predictions by up to 20% in the $10 < y^+ < 200$ region, and its near-wall behaviour suggested a damped $Pr_t$ (a constant near 0.75 divided by a van Driest-like damping function) for the wall-normal component. In the Mach 11/14 DNS assessment, AEF predicted the **streamwise** turbulent heat flux much better than constant $Pr_t$ and improved a posteriori temperature profiles, while both models did well for the **wall-normal** component, which is the one that sets wall heating. Bowersox & North also derived extensions for vibrational nonequilibrium, which changes the decay of turbulence, and noted pressure-gradient terms that may matter in high-speed flows.

### Validation anchors

The Huang et al. DNS reproduce CUBRC's Mach 11.1 flat-plate experiment (wall shear stress very well; heat transfer well over part of the plate, over-predicted far downstream) and agree closely with Baldwin–Lomax RANS for the same case, and include AEDC Tunnel 9 Mach 14 conditions. These databases are now standard for assessing RANS models in cold-wall conditions.

!!! note "Settled vs active"
    That standard RANS models and constant $Pr_t$ have known deficiencies for cold-wall hypersonic boundary layers is well documented. The specific corrections here are recent single-group proposals validated mainly on flat-plate DNS; their behaviour on capsule geometries, with pressure gradients, separation and reacting flow, is an open question.

## Variants

*(To be written: Spalart–Allmaras, SST and $k$–$\omega$ variants used in reentry codes; wall functions and why they fail with strong wall heat transfer; LES/DNS for transition and SWBLI.)*

## Implications

| Lens | Effect |
|---|---|
| Time step and cost | Two extra equations for two-equation models; stiff near-wall source terms. Corrections like Danis–Durbin are free (local, no wall variables). |
| Steady vs unsteady | RANS is a steady-state tool; unsteady SWBLI and transition need LES/DNS. |
| Accuracy | Directly sets turbulent heat flux; cold-wall errors in eddy viscosity and $Pr_t$ propagate to heating. |
| Robustness | Turbulence-model source terms add stiffness; positivity of $k$ and $\omega$ must be guarded. |
| Physics captured or lost | RANS loses unsteadiness and transition physics by construction; heat flux depends on the heat-flux closure, not just the eddy viscosity. |
| Hardware / parallel fit | Pointwise sources; same fit as the flow solver. |

## In a run

Knobs: turbulence model, compressibility correction, $Pr_t$ or heat-flux model, transition location (often prescribed). Symptoms: turbulent heating that is too high on cold walls; velocity profiles that don't collapse under van Driest scaling.

## Which codes

*(To be written.)* Production reentry codes use one- and two-equation RANS models (Baldwin–Lomax historically, SA and SST more recently) with constant $Pr_t$ by default.

## See also

[Viscous fluxes](../spatial/viscous-fluxes.md) · [Central schemes](../spatial/central-schemes.md) (low-dissipation numerics for LES/DNS) · [Entry flow anatomy](entry-flow-anatomy.md)

## References

Bowersox & North (2010); Huang, Nicholson, Duan, Choudhari & Bowersox (2020); Danis & Durbin (2022). See the [bibliography](../../references.md).
