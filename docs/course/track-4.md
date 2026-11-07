---
status: outline
---

# Track 4: Thermochemistry and nonequilibrium

Reference table: the [gas-model ladder](../reference/thermo/gas-models.md).

| # | Topic | Depth | Reference |
|---|---|---|---|
| 4.1 | High-temperature gas thermodynamics: internal energy modes, partition functions, electronic levels and potential-energy curves, NASA polynomials, equilibrium vs frozen vs nonequilibrium; why dissociation lowers post-shock temperature and raises density; dense-gas EOS only as contrast. | [deep] | [Energy modes](../reference/thermo/energy-modes.md) |
| 4.2 | **Thermal nonequilibrium and the model hierarchy**: 1T, Park 2T, 3T, multi-vibrational (per species, CO₂ modes), rotational nonequilibrium, state-to-state and coarse-grained. For each: physics captured (post-shock overshoot, vibration–dissociation coupling, non-Boltzmann populations), cost, data needs, when justified. Landau–Teller relaxation, Millikan–White. | [deep] | [Thermal nonequilibrium](../reference/thermo/thermal-nonequilibrium.md) |
| 4.3 | Finite-rate chemistry: 5- and 11-species air, CO₂ mechanisms, Arrhenius rates, equilibrium constants and backward rates, third bodies, Park's controlling temperature, vibration–dissociation coupling, ionization and charge neutrality. | [deep] | [Finite-rate chemistry](../reference/thermo/finite-rate-chemistry.md) |
| 4.4 | **Stiffness of chemical sources**: Damköhler numbers, point-implicit treatment, operator splitting with sub-stepped stiff ODE integration, IMEX, splitting error at steady state, reduction methods (QSSA, CSP). | [deep] | [Stiff sources](../reference/sources/stiff-sources.md) |
| 4.5 | Ionization and electrons: weakly ionized flows, ambipolar diffusion, communications blackout. | [feel] | [Transport](../reference/thermo/transport-and-diffusion.md#ambipolar-diffusion) |
| 4.6 | Transport properties: Gupta–Yos, Wilke mixing, Chapman–Enskog; diffusion models (Fick/mixture-averaged, SCEBD, full Stefan–Maxwell) and when cross-diffusion matters; libraries like Mutation++. | [feel] | [Transport and diffusion](../reference/thermo/transport-and-diffusion.md), [Mutation++](../codes/mutationpp.md) |
| 4.7 | State-to-state and ab initio (QCT) rate data: where the field is moving and why. | [feel, may go deep] | [Thermal nonequilibrium](../reference/thermo/thermal-nonequilibrium.md#state-to-state) |
