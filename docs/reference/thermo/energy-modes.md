---
status: draft
---

# Energy modes and thermodynamics

<div class="page-meta" markdown>
**Chapter:** 3 Gas models and thermochemistry · **Depth:** [deep]
</div>

## What it is

A molecule stores energy in several **modes**: translation (motion of the molecule as a whole), rotation (tumbling), vibration (the atoms oscillating along their bond) and electronic excitation (electrons in higher-energy states). Free electrons carry their own translational energy. Statistical mechanics gives each mode's energy as a function of a temperature; the [caloric closure](../foundations/closing-the-system.md#2-caloric-relations-and-the-temperature-inversion) sums them.

## The problem it solves

Where the energy goes decides the temperature. In a shock layer, a large fraction of the kinetic energy of the oncoming gas ends up in vibration, dissociation and electronic excitation rather than in random thermal motion, which changes temperature, density, standoff and heating ([entry flow anatomy](../physics/entry-flow-anatomy.md#post-shock-density-and-standoff)).

## How it works

### Equilibration rates

The modes reach equilibrium with each other at very different rates. Translation equilibrates in a few collisions, rotation in about ten, vibration in roughly $10^3$–$10^5$ (strongly temperature-dependent), and dissociation on comparable or slower scales at high temperature. That gap is why vibration gets its own temperature in [multi-temperature models](thermal-nonequilibrium.md).

### Translation and rotation

Fully excited at any temperature of interest, so their energy is linear in $T$: $\tfrac32 RT$ per unit mass (in terms of the species gas constant) for translation, plus $RT$ for rotation of a linear molecule. This is why the [two-temperature inversion](../foundations/closing-the-system.md#2-caloric-relations-and-the-temperature-inversion) gets $T$ directly once $T_v$ is known.

### Vibration

Vibration is quantized. In the harmonic-oscillator approximation, per unit mass,

$$
e_v = \frac{R\,\theta_v}{e^{\theta_v/T_v} - 1},
$$

with characteristic temperatures $\theta_v \approx 3390$ K for N₂ and $\approx 2270$ K for O₂. Well below $\theta_v$, vibration is frozen out; well above, it approaches the fully excited value $R(T_v - \theta_v/2)$.

<figure markdown>
![vibrational energy](../../assets/figures/vibrational_energy.svg)
<figcaption>Harmonic-oscillator vibrational energy. Vibration contributes almost nothing below about 0.2 θ<sub>v</sub> and is essentially fully excited above about 2 θ<sub>v</sub>; shock-layer temperatures of 6,000–15,000 K are well into the excited regime for air molecules.</figcaption>
</figure>

### The potential-energy well

The harmonic oscillator is an approximation to the true interatomic potential. Plot the energy of a diatomic molecule against the separation of its two nuclei: the curve has a minimum at the bond length, and its depth is the dissociation energy. Vibrational levels sit inside that well, getting closer together near the top because the real oscillator is anharmonic. **Dissociation means climbing out of the well.** Each electronic state has its own potential curve and its own well.

<figure markdown>
![Morse well](../../assets/figures/morse_well_n2.svg)
<figcaption>The N<sub>2</sub> ground electronic state in the Morse approximation, with its vibrational levels (illustrative; the Morse fit is approximate near the top of the well). A molecule high in the well needs only a small push to dissociate: the picture behind vibration–dissociation coupling.</figcaption>
</figure>

This picture is the basis of **vibration–dissociation coupling**: a vibrationally excited molecule dissociates more easily, and dissociation preferentially removes high-lying (energetic) vibrational states. Park's [controlling temperature](finite-rate-chemistry.md#parks-controlling-temperature) is a crude model of the first effect; state-to-state models resolve both ([thermal nonequilibrium](thermal-nonequilibrium.md#state-to-state)).

### Electronic excitation

Electrons in an atom or molecule occupy quantized states; excited electronic states are higher-energy configurations. Each species has a table of levels from spectroscopy (for example the NIST Atomic Spectra Database), with characteristic temperatures $\theta_i$ and degeneracies $g_i$. The electronic energy is a Boltzmann average over that table:

$$
e_{el} = \frac{R\sum_i g_i\,\theta_i\,e^{-\theta_i/T_{el}}}{\sum_i g_i\,e^{-\theta_i/T_{el}}}.
$$

"Tabulated levels" means this sum runs over real levels rather than a fitted polynomial. CFD models usually truncate it to a few levels, up to a few dozen. In a two-temperature model $T_{el} = T_v$.

### Formation enthalpy

Each species carries a heat of formation $h_s^0$ (zero for N₂ and O₂ by convention; large and positive for N, O and NO). Including it in the total energy ([governing equations](../foundations/governing-equations.md#reacting-two-temperature-mixture)) is what makes chemical energy part of the conserved $E$, so the energy equation needs no chemistry source.

### Partition functions and polynomial fits

*(Outline.)* All of the above follow from the partition function of each mode. Production codes often use NASA polynomial fits for $c_p(T)$, $h(T)$ and $s(T)$ instead of explicit mode sums, which is simpler in a one-temperature model but needs care in multi-temperature models where modes have different temperatures.

## Variants

How codes evaluate the energies: closed-form expressions for each mode (rigid rotor, harmonic oscillator, a table of electronic levels), needed whenever $T \ne T_v$; or polynomial fits of $c_p(T)$ for each species (the NASA polynomials), which lump all the modes together and so assume a single temperature.

## Typical values

- Characteristic vibrational temperatures: about 3390 K (N₂), 2270 K (O₂), 2740 K (NO) (Anderson; other compilations differ by a percent or two).
- Characteristic rotational temperatures: about 2.9 K (N₂) and 2.1 K (O₂), which is why rotation is fully excited at any temperature of interest.
- Dissociation energies: 9.76 eV (N₂), 5.12 eV (O₂), 6.50 eV (NO); as characteristic temperatures, about 113,000 K, 59,500 K and 75,500 K.
- Ionization energies: 14.53 eV (N), 13.62 eV (O), 9.26 eV (NO). NO ionizes most easily, which is why NO⁺ supplies the first electrons.
- Collisions to equilibrate: a few (translation), about ten (rotation), $10^3$–$10^5$ (vibration).

## Trade-offs

- **Harmonic oscillator vs anharmonic levels.** The harmonic form is closed and cheap; it over-counts energy near the top of the well, where real levels crowd together and the molecule dissociates.
- **Truncating the electronic levels.** A few low-lying levels are enough for the energy below about 10,000 K; radiation needs many more.
- **Mode-by-mode expressions vs polynomial fits.** Fits are faster and are what most thermodynamic data sets provide; they can't be split between two temperatures.

## Effects on stability and robustness

- The vibrational energy is a steep, nonlinear function of $T_v$ at low temperature; the Newton inversion for $T_v$ needs a safeguarded start when $e_v$ is very small.
- Polynomial fits evaluated outside their fitted range are the usual source of unphysical heat capacities.
- None of the mode models is a source of instability in itself; their role in robustness is through the temperature inversion ([closing the system](../foundations/closing-the-system.md#2-caloric-relations-and-the-temperature-inversion)).

## Implications

| Lens | Effect |
|---|---|
| Time step and cost | Mode sums and electronic-level tables cost per cell per evaluation inside the temperature inversion. |
| Steady vs unsteady | Neutral. |
| Accuracy | Sets temperature for a given energy, hence chemistry rates, standoff and heating. |
| Robustness | Nonlinear $e(T)$ requires a Newton inversion that can fail with bad energies. |
| Physics captured or lost | Harmonic vs anharmonic, truncated electronic levels: small effects on temperature, larger on radiation and dissociation coupling. |
| Hardware / parallel fit | Pointwise; branchy iterations reduce GPU efficiency. |

## In a run

Knobs: thermodynamic database (mode sums vs polynomial fits), number of electronic levels. Symptoms: temperature-inversion failures; small differences in standoff between codes using different databases.

## Which codes

All reacting codes. Mutation++ provides mode-resolved thermodynamics to codes that use it.

## See also

[Gas models](gas-models.md) · [Thermal nonequilibrium](thermal-nonequilibrium.md) · [Finite-rate chemistry](finite-rate-chemistry.md) · [Closing the system](../foundations/closing-the-system.md)

## References

Anderson, *Hypersonic and High-Temperature Gas Dynamics* (statistical thermodynamics chapters); Vincenti & Kruger, *Introduction to Physical Gas Dynamics*; Park, *Nonequilibrium Hypersonic Aerothermodynamics*. See the [bibliography](../../references.md).
