---
status: draft
---

# Transport and diffusion

<div class="page-meta" markdown>
**Chapter:** 3 Gas models and thermochemistry · **Depth:** [feel], with the diffusion hierarchy at [deep]
</div>

## What it is

The models for viscosity $\mu$, thermal conductivities $\kappa$ (and $\kappa_v$ in multi-temperature models) and the species diffusion fluxes $\mathbf J_s$ that appear in the [viscous fluxes](../spatial/viscous-fluxes.md).

## The problem it solves

Transport directly sets the wall heat flux:

$$
q_w = \kappa\,\frac{\partial T}{\partial n} + \kappa_v\,\frac{\partial T_v}{\partial n} + \sum_s h_s J_{s,n}.
$$

The last term is chemical enthalpy carried to the wall by diffusing atoms, which release it if they recombine there (a catalytic wall). Getting diffusion wrong changes the heat flux even when the temperature gradient is right.

## How it works

### Viscosity and conductivity

Species properties come from collision integrals (Chapman–Enskog kinetic theory) or curve fits. Chapman–Enskog theory is also where the Navier–Stokes form itself comes from: it is the first-order correction to an equilibrium (Maxwellian) velocity distribution in powers of the Knudsen number, which is why these transport models and the Navier–Stokes equations fail together when the gas becomes rarefied ([continuum breakdown](../rarefied/continuum-breakdown.md#why-navier-stokes-fails-chapman-enskog)). Mixture values come from mixing rules such as Wilke's, or from the Gupta–Yos formulation. Mixing rules need pairwise interaction terms, so they cost $O(n_s^2)$ per cell.

### The diffusion hierarchy

**Fick's law with one coefficient per species** (mixture-averaged, or a constant Lewis or Schmidt number):

$$
\mathbf J_s = -\rho D_s\nabla Y_s .
$$

Cheap, but does not automatically satisfy $\sum_s\mathbf J_s = 0$, so a correction velocity is usually added.

**SCEBD (self-consistent effective binary diffusion)** builds effective coefficients so that mass conservation holds consistently. A common upgrade in reentry codes.

**Full Stefan–Maxwell** couples every pair of species:

$$
\nabla X_s = \sum_k \frac{X_s X_k}{\mathcal D_{sk}}\,(\mathbf V_k - \mathbf V_s)\quad(+\ \text{thermal and pressure diffusion}),
$$

which requires solving an $n_s\times n_s$ linear system per cell, $O(n_s^3)$. What it buys is **cross-diffusion**: one species' flux driven by the gradients of others, including reverse diffusion and diffusion barriers, with exact mass conservation and no correction velocity.

### When the difference matters

Cross-diffusion matters when molecular masses differ a lot: H₂/He atmospheres (gas giants), ablation products (H, C and their compounds) mixing with air, and ionized flows with light electrons. For neutral air, where N, O, N₂ and O₂ have similar masses, SCEBD is usually close to Stefan–Maxwell.

!!! warning "Calibration"
    The size of the heat-flux difference between diffusion models for catalytic walls in air is generally reported as modest, but should be quoted only from a specific study.

### Ambipolar diffusion {#ambipolar-diffusion}

In an ionized gas, electrons diffuse far faster than ions, but any separation creates an electric field that pulls them back. The net effect is that ions and electrons diffuse together, with ion diffusion coefficients roughly doubled. Codes enforce this instead of resolving the field.

## Variants

### Viscosity and conductivity models

| Model | What it is | Range | Cost |
|---|---|---|---|
| Sutherland | one-line fit of air viscosity against temperature | non-reacting air, up to roughly 2000 K | negligible |
| Blottner fits + Wilke mixing + Eucken conductivity | curve-fitted species viscosities, mixed with Wilke's rule; conductivity from viscosity and heat capacities | neutral, weakly ionized air, up to roughly 10,000 K | $O(n_s^2)$ |
| Gupta–Yos (collision integrals) | mixture properties built from binary collision integrals | ionized air to 30,000 K (Gupta et al. 1990) | $O(n_s^2)$, larger constant |
| Full Chapman–Enskog | solve the kinetic-theory linear systems | reference accuracy | $O(n_s^3)$ |

### Diffusion models

Constant Lewis or Schmidt number; mixture-averaged Fick with a correction velocity; SCEBD; full Stefan–Maxwell (section above). Ambipolar treatment is added to any of them when ions are present.

### Libraries

[Mutation++](../../codes/index.md#mutationpp) (VKI) provides transport, thermodynamics and chemistry to several codes.

## Typical values

- Prandtl number of air: about 0.7. Lewis number used by Fay & Riddell for dissociated air: 1.4. Schmidt numbers assumed in constant-Schmidt models: 0.5–0.7.
- Ambipolar diffusion coefficient: $D_a = D_i(1 + T_e/T_i)$, so twice the ion coefficient when electron and ion temperatures are equal.
- Cost per cell: $O(n_s^2)$ for mixing rules (121 pair terms for 11 species), $O(n_s^3)$ for Stefan–Maxwell.
- Validity limits in the table above are approximate; the 30,000 K figure is the stated range of the Gupta et al. (1990) data.

## Trade-offs

- **Wilke/Blottner vs collision integrals.** The simple route is cheap and adequate for neutral air; it degrades as ionization rises, because charged-particle collisions are long-range and don't follow the fitted trends.
- **Fick vs SCEBD vs Stefan–Maxwell.** Each step is more consistent with mass conservation and costs more; the gain is small for neutral air and large when species masses differ widely.
- **Constant Lewis number.** One number instead of a diffusion model, which is why it appears in correlations and in the film-coefficient [surface energy balance](../walls/surface-energy-balance.md); it can't represent species separating from each other.

## Effects on stability and robustness

- Fick's law with independent coefficients doesn't sum to zero mass flux. Without a correction velocity, total mass is not conserved near walls where gradients are large.
- Mass fractions pushed slightly negative by diffusion near a catalytic wall need limiting.
- Transport coefficients are smooth and positive, so they don't destabilize a run; their effect is on accuracy and on the viscous time-step limit through $\nu$.

## Implications

| Lens | Effect |
|---|---|
| Time step and cost | $O(n_s^2)$ per cell for mixing rules; $O(n_s^3)$ for Stefan–Maxwell. |
| Steady vs unsteady | Neutral. |
| Accuracy | Directly sets heat flux and skin friction; diffusion model matters most for catalytic walls and ablating surfaces. |
| Robustness | Correction velocities and mass-fraction bounds need care near walls. |
| Physics captured or lost | Simplified diffusion loses cross-diffusion and separation of light species. |
| Hardware / parallel fit | Pointwise; per-cell linear solves for Stefan–Maxwell. |

## In a run

Knobs: transport model, diffusion model, Lewis/Schmidt numbers if constant. Symptoms: heat flux that shifts when changing the diffusion model on a catalytic wall.

## Which codes

The production entry codes use collision-integral transport (Gupta–Yos type mixing) for ionized air and offer simpler curve-fit options; for diffusion, SCEBD or an approximate multicomponent (Stefan–Maxwell) treatment is typical. [SU2-NEMO](../../codes/index.md#su2-nemo) can take all of these from Mutation++.

!!! warning "Calibration"
    Which transport and diffusion model each of DPLR, LAURA and US3D uses by default is in their user manuals and varies with version; this page has not been checked against them line by line.

## See also

[Viscous fluxes](../spatial/viscous-fluxes.md) · [Wall boundary conditions](../walls/wall-boundary-conditions.md) · [Closing the system](../foundations/closing-the-system.md)

## References

Gupta, Yos, Thompson & Lee (1990); Wilke (1950); Ramshaw (1990) on SCEBD; Hirschfelder, Curtiss & Bird, *Molecular Theory of Gases and Liquids*. See the [bibliography](../../references.md).
