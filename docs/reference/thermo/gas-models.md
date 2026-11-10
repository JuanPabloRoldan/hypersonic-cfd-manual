# Gas models

<div class="page-meta" markdown>
**Chapter:** 3 Gas models and thermochemistry · **Depth:** [deep] for the structure
</div>

## What it is

The set of assumptions that decides which quantities are carried as conserved variables and which are supplied by the closure. The key idea: **$\mathbf U$ contains exactly the quantities you refuse to assume are in equilibrium.** Everything assumed equilibrated moves out of the PDEs and into the closure.

## The problem it solves

Entry flows span frozen, nonequilibrium and equilibrium regimes. A model that is too simple gives badly wrong temperatures and standoff; a model that is too detailed is unaffordable or lacks the rate data to justify it. Choosing the rung of the ladder is one of the first decisions of any run.

## How it works

### Terminology

"Real gas" in hypersonics usually means *high-temperature effects*, not van der Waals behaviour.

- **Calorically perfect**: $p = \rho RT$ with constant $c_v$ and $\gamma$.
- **Thermally perfect**: still $p = \rho RT$, but $e(T)$ is nonlinear because internal modes (vibration, electronic) switch on with temperature.
- **Equilibrium reacting**: composition is whatever chemical equilibrium dictates at the local $(\rho, e)$.
- **Nonequilibrium**: composition and/or internal energies lag behind equilibrium.

### Two independent axes

Gas models differ along two separate axes, the thermal state of the energy modes and the chemical state of the composition:

| Chemistry → / Modes ↓ | Frozen | Equilibrium | Finite-rate |
|---|---|---|---|
| Fixed (constant γ) | Calorically perfect | — | — |
| Equilibrium at one T | Thermally perfect | Equilibrium air | Finite-rate 1T |
| Nonequilibrium | Vibrational relaxation in frozen-chemistry expansions (nozzles, wakes) | — (chemical equilibrium implies thermal) | 2T, 3T, multi-vib, state-to-state |

### The ladder, with implications

For *when* each rung is needed (by speed, altitude and output), see [choosing physical models](../model-selection.md).

Counts are for 3D with 11-species air; costs are qualitative and case-dependent.

| Model | Unknowns per cell | Closure work per cell | Implicit block | Captures | Loses | Typical use |
|---|---|---|---|---|---|---|
| Calorically perfect | 5 | Closed-form $p$ | 5×5 | Shock and wave structure, cold-flow aero | All high-T effects: post-shock T badly overpredicted, standoff too large | Cold hypersonic tunnels, method testing |
| Thermally perfect | 5 | Newton for $T$ on $e(T)$ | 5×5 | Vibrational excitation below dissociation | Dissociation | Moderate-enthalpy tunnels, nozzles below ~2500 K |
| Equilibrium air | 5 | Table or curve-fit lookup | 5×5 | Correct T, ρ, standoff when $Da \gg 1$ | Relaxation zones, overshoot, freezing in expansions and wakes, finite catalysis | Low altitude, large bodies, quick estimates |
| Finite-rate 1T | 15 | Newton for $T$; $n_r$ Arrhenius rates; $O(n_s^2)$ transport | 15×15 | Chemical lag, recombination freezing, catalytic-wall effects | Vibrational lag: T overshoot, vibration–dissociation coupling | Lower-speed entry, some design work |
| Finite-rate 2T (Park) | 16 | Newton for $T_v$ ($T$ then direct); T–V relaxation pairs | 16×16 | Post-shock overshoot; vibration–dissociation coupling via $T_c$ | Separate electron temperature, per-species vibration, non-Boltzmann populations | Standard Earth/Mars entry design |
| Multi-temperature | 17+ | More inversions and relaxation pairs | grows | Electron-temperature effects, per-species vibration (CO₂ modes), rotational lag | Limited by rate-data quality | Research, high-speed and ionized flows, Mars, rarefied regimes |
| State-to-state | $10^2$–$10^4$ | Huge rate tables | infeasible implicitly in 3D | True level populations | (cost) | 0D/1D studies that inform reduced models |

Equilibrium air has the same five unknowns as a perfect gas: all the chemistry is hidden inside a nonlinear table lookup $p(\rho, e)$, $T(\rho, e)$ (Tannehill–Mugge-type curve fits, or Gibbs minimization).

The magnitude of the perfect-gas error is large. At Mach 25 a calorically perfect gas predicts post-shock temperatures of order 30,000 K; real air dissociates and lands several times lower. See [entry flow anatomy](../physics/entry-flow-anatomy.md#post-shock-density-and-standoff) for what this does to density and standoff.

### Species sets

5-species air (N₂, O₂, NO, N, O) is adequate below roughly 8–9 km/s. 11-species air adds N₂⁺, O₂⁺, NO⁺, N⁺, O⁺ and e⁻, needed above roughly 9–10 km/s (lunar return and faster) or when communications blackout matters. Mars entry needs a CO₂–N₂ mechanism; Titan entry N₂–CH₄ (with CN, a strong radiator).

### Dense gases {#dense-gases}

A **dense gas** is one where molecules are close enough that intermolecular forces and finite molecular volume matter, so $p \ne \rho RT$ and the compressibility factor $Z = p/(\rho RT)$ departs from 1. This happens near the critical point and at high pressure: supercritical rocket chambers, organic Rankine cycle turbines. It needs real-fluid equations of state (van der Waals, Peng–Robinson, Span–Wagner); $\mathbf U$ is unchanged and only the closure changes. Entry shock layers sit at a fraction of an atmosphere and thousands of kelvin, so $Z\approx 1$. A curiosity: in certain heavy fluids (BZT fluids, with negative fundamental derivative $\Gamma < 0$), expansion shocks become physically admissible, because the [entropy condition](../foundations/conservation-and-weak-solutions.md#nonuniqueness-and-the-entropy-condition) selects different weak solutions in that regime.

## Implications

| Lens | Effect |
|---|---|
| Time step and cost | Explicit cost grows roughly linearly with equations plus closure cost; implicit cost as $n^2$ memory and $n^3$ block operations; stiff chemistry adds iterations. |
| Steady vs unsteady | Neutral, but nonequilibrium models add stiff relaxation that implicit or point-implicit treatment must handle. |
| Accuracy | Decisive: standoff, post-shock temperature, composition at the wall and therefore heat flux all depend on the model. |
| Robustness | Each rung adds failure modes (temperature inversion, negative species); standard practice is to start perfect-gas or frozen and switch chemistry on later. |
| Physics captured or lost | See the table. |
| Hardware / parallel fit | More unknowns per cell means more memory per cell, which hits GPUs and implicit methods hardest. |

## In a run

Knobs: gas model, species set, number of temperatures, reaction mechanism. Symptoms: abrupt cost increase when chemistry is switched on; standoff that changes noticeably between models; temperature-inversion aborts at startup.

## Which codes

DPLR, LAURA and US3D run finite-rate 2T air and Mars mechanisms as standard; equilibrium and perfect-gas options are typical for quick runs. SU2-NEMO and Eilmer offer similar ladders (SU2-NEMO through Mutation++ or built-in models).

## See also

[Closing the system](../foundations/closing-the-system.md) · [Energy modes](energy-modes.md) · [Thermal nonequilibrium](thermal-nonequilibrium.md) · [Finite-rate chemistry](finite-rate-chemistry.md)

## References

Anderson, *Hypersonic and High-Temperature Gas Dynamics*; Park, *Nonequilibrium Hypersonic Aerodynamics*; Gnoffo, Gupta & Shinn (1989); Tannehill & Mugge (1974). See the [bibliography](../../references.md).
