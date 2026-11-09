---
status: draft
---

# Entry flow anatomy

<div class="page-meta" markdown>
**Slot:** Track 1.1 · **Depth:** [deep]
</div>

## What it is

The structure of the flow around a blunt entry vehicle: bow shock, shock standoff, stagnation region and sonic line, shock layer, boundary layer, shoulder expansion, wake and backshell.

## The problem it solves

Every aerothermal quantity is tied to one of these regions, and each region stresses different parts of the solver: the stagnation region is subsonic and [elliptic](../foundations/mathematical-character.md#mixed-character-around-a-blunt-body), the shock layer is reacting and in nonequilibrium, the boundary layer sets heat flux, and the wake is separated and unsteady.

## How it works

<figure markdown>
![Blunt body regions](../../assets/figures/blunt_body_regions.svg)
<figcaption>Bow shock, standoff, subsonic stagnation pocket and supersonic shock layer around a sphere at M = 20 (Billig's perfect-gas shock-shape correlation; sonic line schematic).</figcaption>
</figure>

*(The full anatomy, region by region, is still to be written.)*

### Post-shock density and standoff

For a strong normal shock, the conservation laws ([Rankine–Hugoniot](../foundations/conservation-and-weak-solutions.md#rankine-hugoniot-conditions)) give

$$
\rho_1 u_1 = \rho_2 u_2,\qquad p_2 \approx \rho_1 u_1^2,\qquad h_2 \approx \tfrac12 u_1^2,
$$

where the approximations hold because $u_2 \ll u_1$. Post-shock **pressure and enthalpy are fixed by the freestream momentum and kinetic energy**, almost independently of the gas model. What the gas model decides is how that enthalpy is held. In a perfect gas it is all random thermal motion, so $T_2$ is huge. In dissociating air a large fraction goes into breaking bonds (chemical energy), so $T_2$ is several times lower.

The equation of state then gives $\rho_2 = p_2/(R_{mix}T_2)$. At essentially the same pressure but a much lower temperature, the density is higher. Dissociation also raises $R_{mix}$ (more particles per unit mass), which partly offsets this, but the temperature drop wins. "Denser" means denser at the same pressure; the shock-layer volume is not fixed in advance, it is the outcome.

The density ratio $\varepsilon^{-1} = \rho_2/\rho_1$ rises from the perfect-gas strong-shock limit $(\gamma+1)/(\gamma-1) = 6$ to roughly 10–15 or more in high-speed equilibrium air (indicative values; see the equilibrium normal-shock charts in Anderson). Continuity then says the post-shock gas also moves more slowly, $u_2 = \varepsilon u_1$.

**Standoff follows from mass balance.** The mass flux entering through the shock must leave sideways around the shoulder. Denser gas carries the same mass flux through a thinner layer, so the shock sits closer. Standoff is approximately proportional to the density ratio across the shock; a widely used approximation for a sphere is

$$
\frac{\Delta}{R_n} \approx 0.78\,\frac{\rho_1}{\rho_2}.
$$

In **nonequilibrium**, the composition right behind the shock is still frozen, so $T$ is high and the density ratio is close to the perfect-gas value; moving towards the body the gas relaxes, $T$ drops and the density climbs. Finite-rate standoff therefore falls between the perfect-gas and equilibrium values. This is one of the quickest sanity checks on a reacting solution.

## Variants

*(Outline: stagnation region, sonic line, shock layer, boundary layer, shoulder expansion, wake and backshell.)*

## Implications

*(To be written.)*

## In a run

Standoff is the first thing to check against expectations: perfect gas > nonequilibrium > equilibrium. A standoff outside that range points at the gas model, the shock capturing, or the grid at the shock.

## Which codes

Not code-specific.

## See also

[Mathematical character](../foundations/mathematical-character.md) · [Gas models](../thermo/gas-models.md) · [Energy modes](../thermo/energy-modes.md)

## References

Anderson, *Hypersonic and High-Temperature Gas Dynamics*; Billig (1967); Gnoffo (1999). See the [bibliography](../../references.md).
