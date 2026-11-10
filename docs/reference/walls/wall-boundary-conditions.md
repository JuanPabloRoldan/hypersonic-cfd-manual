---
status: outline
---

# Wall boundary conditions

<div class="page-meta" markdown>
**Chapter:** 5 Boundary conditions and walls · **Depth:** [deep]
</div>

## What it is

The conditions imposed on velocity, temperature(s) and composition at a solid surface.

## The problem it solves

The wall is where the heat flux is measured, and the thermal and chemical conditions there change it substantially.

## How it works

*(Outline.)*

## Variants

### Thermal: isothermal, adiabatic, radiative equilibrium
### Catalytic: non-, partially, fully and super-catalytic

How each changes the diffusive enthalpy term $\sum_s h_s J_s$ in the [wall heat flux](../thermo/transport-and-diffusion.md).

### Slip and temperature-jump walls (rarefied flow)

In the slip regime ($10^{-3} \lesssim Kn \lesssim 10^{-1}$, [continuum breakdown](../rarefied/continuum-breakdown.md)) the gas next to the wall has had too few collisions with it to take on its velocity and temperature. The Navier–Stokes equations still hold in the interior, so the fix is a boundary condition: the wall values are replaced by a slip velocity and a jumped temperature proportional to the mean free path times the local gradient.

**Maxwell velocity slip** (neglecting thermal creep):

$$
u_s = \frac{2 - \sigma}{\sigma}\,\lambda\,\left.\frac{\partial u}{\partial n}\right|_w ,
$$

**Smoluchowski temperature jump:**

$$
T_s - T_w = \frac{2 - \alpha}{\alpha}\,\frac{2\gamma}{\gamma + 1}\,\frac{\lambda}{Pr}\,\left.\frac{\partial T}{\partial n}\right|_w ,
$$

with $\sigma$ the tangential-momentum accommodation coefficient, $\alpha$ the thermal accommodation coefficient (both 1 for a fully diffuse, fully accommodating wall), and $n$ the wall normal. Both reduce to no-slip and $T_s = T_w$ as $\lambda \to 0$. The effect is to lower skin friction and heat flux relative to no-slip, by an amount that grows with $Kn$. Multi-species, multi-temperature extensions exist (for example Gökçen & MacCormack 1989). Beyond $Kn \sim 0.1$ slip conditions are no longer enough and [DSMC](../rarefied/dsmc.md) is needed.

## Implications

*(To be filled.)*

## In a run

*(To be filled.)*

## Which codes

*(To be filled.)*

## See also

[Surface energy balance](surface-energy-balance.md) · [Transport and diffusion](../thermo/transport-and-diffusion.md) · [Boundary conditions](../spatial/boundary-conditions.md) · [Stagnation-point heating](../physics/stagnation-point-heating.md) · [Continuum breakdown](../rarefied/continuum-breakdown.md)

## References

Maxwell (1879); Smoluchowski (1898); Bird, *Molecular Gas Dynamics and the Direct Simulation of Gas Flows*; Gökçen & MacCormack (1989).
