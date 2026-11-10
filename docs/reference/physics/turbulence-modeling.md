---
status: draft
---

# Turbulence modeling for hypersonic boundary layers

<div class="page-meta" markdown>
**Chapter:** 4 Turbulence · **Depth:** [feel]
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

### RANS model families

| Family | Extra equations | How the eddy viscosity is set | Strengths | Weak points for entry flows |
|---|---|---|---|---|
| Algebraic (Baldwin–Lomax, Cebeci–Smith) | 0 | from the mean velocity profile and wall distance | cheap, robust for attached boundary layers | needs an identifiable boundary-layer edge; poor in separation and wakes |
| Spalart–Allmaras | 1 | a transport equation for the eddy viscosity itself | robust, easy to converge | needs wall distance; compressible variants change the answer |
| $k$–$\omega$ and SST | 2 | from turbulent kinetic energy $k$ and specific dissipation rate $\omega$ | better in pressure gradients and mild separation | cold-wall eddy-viscosity errors (above); over-production of $k$ at shocks |

All of them are eddy-viscosity models: the turbulent stress is assumed proportional to the mean strain rate. Two consequences matter at hypersonic speed. A shock is a region of enormous strain rate, so an eddy-viscosity model produces turbulent kinetic energy there far faster than real turbulence responds, and codes limit production at shocks. And the heat flux inherits whatever error the eddy viscosity has, through the turbulent Prandtl number.

### Wall functions

A wall function replaces the near-wall grid with an assumed velocity and temperature profile (the log law), so the first cell can be far thicker. The assumed profile comes from incompressible, near-adiabatic boundary layers in equilibrium. With a cold wall and large property variation across the layer it doesn't hold in untransformed variables, and the wall heat flux is exactly the quantity the assumed profile dictates. Aeroheating runs therefore resolve the wall, with the first cell at $y^+$ of order one.

### Transition

RANS models don't predict where the boundary layer becomes turbulent. Entry analyses usually prescribe the transition location, or run fully laminar and fully turbulent solutions as a bracket. The location comes from correlations (a momentum-thickness Reynolds number, sometimes divided by edge Mach number, exceeding a threshold of a few hundred; roughness-based criteria on ablated heatshields) or from stability analysis.

### Scale-resolving methods

LES and DNS resolve the turbulence instead of modelling it, and need the low-dissipation numerics of [central schemes](../spatial/central-schemes.md) and time-accurate integration. They are used for transition mechanisms, shock/boundary-layer interaction unsteadiness and to build the databases RANS models are judged against. Hybrid RANS/LES (detached-eddy simulation) is used for capsule wakes, where the separated flow is unsteady at large scale.

## Typical values

- Turbulent Prandtl number: 0.85–0.9; about 0.9 fits the outer layer in Mach 11 and 14 cold-wall DNS (Huang et al. 2020).
- Wall-to-recovery temperature ratio in entry: 0.2 or below.
- Algebraic energy flux model: up to 20% better temperature in $10 < y^+ < 200$ against data from Mach 0.02 to 11.8 (Bowersox & North 2010).
- Danis–Durbin correction: tested for $2.5 \le M \le 14$ and $0.18 \le T_w/T_r \le 1$ (Danis & Durbin 2022).
- First-cell height for wall-resolved heating: $y^+$ of order one.
- Turbulent over laminar heating at the same location: commonly a factor of several.

## Trade-offs

- **Algebraic vs transport-equation models.** Algebraic models add no equations and no stiffness but only work where a boundary layer is clearly defined; one- and two-equation models work in separated regions and cost extra unknowns per cell.
- **Laminar/turbulent bracket vs transition prediction.** The bracket is cheap and safe (fully turbulent is the conservative end) but can over-size the TPS; transition prediction removes conservatism and adds a large uncertainty of its own.
- **RANS vs scale-resolving.** RANS gives steady heating at design cost; LES and DNS give the physics at a cost that restricts them to small domains and research.
- **Constant $Pr_t$ vs a heat-flux model.** Constant $Pr_t$ does well for the wall-normal heat flux that sets heating; better models mainly improve the temperature profile and streamwise flux.

## Effects on stability and robustness

- Turbulence-model source terms are stiff near the wall and are treated implicitly; $k$, $\omega$ and the SA variable must be kept positive.
- Unlimited production of $k$ at a strong shock can flood the shock layer with eddy viscosity, which shows up as unphysically high heating downstream.
- Switching the model on over an established laminar solution is a standard start-up strategy.
- A RANS solution of a flow that is really unsteady (wake, separated interaction) may not converge ([convergence diagnostics](../time/convergence-diagnostics.md#stalls-and-limit-cycles)).

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

Production reentry codes use algebraic models (Baldwin–Lomax, Cebeci–Smith) historically, and Spalart–Allmaras and SST more recently, with constant $Pr_t$ by default. [US3D](../../codes/index.md#us3d) adds hybrid RANS/LES and low-dissipation fluxes for scale-resolving work.

!!! warning "Calibration"
    The model lists are from the codes' manuals and methods papers at a general level. Which compressibility corrections and shock production limiters are applied by default is version-specific.

## See also

[Viscous fluxes](../spatial/viscous-fluxes.md) · [Central schemes](../spatial/central-schemes.md) (low-dissipation numerics for LES/DNS) · [Entry flow anatomy](entry-flow-anatomy.md)

## References

Bowersox & North (2010); Huang, Nicholson, Duan, Choudhari & Bowersox (2020); Danis & Durbin (2022). See the [bibliography](../../references.md).
