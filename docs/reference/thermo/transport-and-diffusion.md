---
status: draft
---

# Transport and diffusion

<div class="page-meta" markdown>
**Slot:** Track 0.1 closures; Track 4.6 · **Depth:** [feel], with the diffusion hierarchy at [deep]
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

Species properties come from collision integrals (Chapman–Enskog kinetic theory) or curve fits; mixture values from mixing rules such as Wilke's, or from the Gupta–Yos formulation. Mixing rules need pairwise interaction terms, so they cost $O(n_s^2)$ per cell.

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

### Libraries

Mutation++ (VKI) provides transport, thermodynamics and chemistry to several codes. *(See [Mutation++](../../codes/index.md#mutationpp).)*

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

*(To be written.)*

## See also

[Viscous fluxes](../spatial/viscous-fluxes.md) · [Wall boundary conditions](../walls/wall-boundary-conditions.md) · [Closing the system](../foundations/closing-the-system.md)

## References

Gupta, Yos, Thompson & Lee (1990); Wilke (1950); Ramshaw (1990) on SCEBD; Hirschfelder, Curtiss & Bird, *Molecular Theory of Gases and Liquids*. See the [bibliography](../../references.md).
