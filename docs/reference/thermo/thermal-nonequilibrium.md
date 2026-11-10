---
status: draft
---

# Thermal nonequilibrium models

<div class="page-meta" markdown>
**Chapter:** 3 Gas models and thermochemistry · **Depth:** [deep]
</div>

## What it is

The family of models that let internal energy modes lag behind translation. Each extra temperature is an extra conserved energy equation plus a relaxation source. The hierarchy runs from one temperature (all modes equilibrated) through Park's two-temperature model to multi-temperature and state-to-state descriptions.

## The problem it solves

Right behind a strong shock, energy lands first in translation. Vibration needs $10^3$–$10^5$ collisions to catch up ([equilibration rates](energy-modes.md#equilibration-rates)), so the translational temperature overshoots, then relaxes as vibration absorbs energy and dissociation proceeds. That overshoot and lag affect standoff, the chemistry behind the shock, nonequilibrium radiation and heating. A one-temperature model can't represent any of it.

## How it works

Each lagging mode gets an energy equation (see the vibrational energy equation in [governing equations](../foundations/governing-equations.md#reacting-two-temperature-mixture)) with a relaxation source. The standard translational–vibrational exchange is the **Landau–Teller** form

$$
Q_{T\text{-}v} = \sum_s \rho_s\,\frac{e_{v,s}(T) - e_{v,s}(T_v)}{\tau_s},
$$

driving each species' vibrational energy towards its value at the translational temperature, with relaxation times $\tau_s$ from the **Millikan–White** correlation (plus Park's high-temperature collision-limited correction). Vibration–dissociation coupling enters through the energy removed with dissociating molecules ($\sum_s\dot\omega_s e_{v,s}$ in the $e_v$ equation) and through the [controlling temperature](finite-rate-chemistry.md#parks-controlling-temperature) in the rates.

*(Derivations, Millikan–White coefficients and the high-temperature correction: to be written.)*

## Variants

### One temperature (1T)

All internal modes in equilibrium at $T$; chemistry may still be finite-rate. Valid when vibrational relaxation is fast compared with the flow (dense flows, low speeds).

### Two temperature (Park 2T)

$T$ for translation and rotation (both fast); $T_v$ for vibration, electronic excitation and free-electron translation. The last two are lumped with vibration mainly because of strong electron–vibration coupling in N₂, and partly for convenience. Codes carry total energy plus vibrational energy (rather than separate translational and vibrational energies) because total energy is exactly conserved. The standard model for Earth and Mars entry design.

### Three temperature (3T)

A separate electron temperature $T_e$. Matters in strongly ionized flows and for radiation.

### Multi-vibrational

One vibrational temperature per molecule ($T_{v,\mathrm{N_2}}$, $T_{v,\mathrm{O_2}}$, $T_{v,\mathrm{NO}}$), or per vibrational mode of polyatomic molecules (CO₂ has three modes, relevant for Mars entry and backshell radiation).

### Rotational nonequilibrium

A separate rotational temperature. Rotation is fast, so this matters only in very rarefied flow (high altitude, small bodies) and inside the shock front itself.

### State-to-state {#state-to-state}

Every vibrational (and possibly electronic) level of every molecule is treated as its own pseudo-species with its own rate equations: hundreds to thousands of equations. Coarse-grained variants group levels into bins. These models show that the vibrational populations behind a shock are **not Boltzmann** at all, so "a temperature $T_v$" is itself a modeling assumption. That reaches directly into nonequilibrium radiation and into how dissociation rates should be modeled. Rate data come increasingly from ab initio potential surfaces and quasi-classical trajectory (QCT) calculations.

## Implications

| Lens | Effect |
|---|---|
| Time step and cost | Each extra temperature adds an equation (implicit block grows), a temperature inversion and relaxation pairs; state-to-state is unaffordable in 3D implicit codes. |
| Steady vs unsteady | Relaxation sources are stiff and need [implicit treatment](../sources/stiff-sources.md#point-implicit). |
| Accuracy | 2T captures the dominant effect for most Earth/Mars entries; weak spots are very high speeds (above about 10 km/s), nonequilibrium radiation, and the somewhat ad hoc controlling temperature. |
| Robustness | $T_v$ inversion failures and $T_v$ overshoot at startup. |
| Physics captured or lost | Overshoot and relaxation zone (2T); electron effects (3T); per-species lag (multi-vib); non-Boltzmann distributions (state-to-state only). |
| Hardware / parallel fit | Pointwise; more state per cell. |

!!! note "Settled vs active"
    Park's 2T model is settled practice for design. Whether its controlling temperature and relaxation correlations are adequate at high speeds, and how to build reduced models from state-to-state and QCT data, is an active research area.

## In a run

Knobs: number of temperatures, relaxation-time correlations, controlling-temperature exponent. Symptoms: post-shock $T$ overshoot (expected in 2T, absent in 1T); differences in standoff and radiation between 1T and 2T runs.

## Which codes

DPLR, LAURA, US3D, SU2-NEMO and Eilmer all run 2T as standard; multi-temperature and state-to-state are research options (often in 0D/1D tools).

## See also

[Energy modes](energy-modes.md) · [Finite-rate chemistry](finite-rate-chemistry.md) · [Gas models](gas-models.md) · [Stiff sources](../sources/stiff-sources.md)

## References

Park, *Nonequilibrium Hypersonic Aerodynamics*; Park (1993); Millikan & White (1963); Candler (2019). See the [bibliography](../../references.md).
