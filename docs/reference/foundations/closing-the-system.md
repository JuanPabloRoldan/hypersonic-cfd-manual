# Closing the system

<div class="page-meta" markdown>
**Chapter:** 1 Fundamental equations · **Depth:** [deep] for the structure, details in chapter 3
</div>

## What it is

The PDEs give one equation per conserved variable, but their fluxes and sources need quantities that aren't in $\mathbf U$: pressure, temperatures, transport coefficients, reaction rates and energy-exchange rates. **Closing the system** means supplying a model that expresses each of these as a function of $\mathbf U$ and its gradients.

## The problem it solves

Without closures the equations can't be evaluated. With them, the PDEs plus closures form a complete system. The PDEs themselves are only conservation and carry essentially no uncertainty; almost all the physical uncertainty in an aeroheating prediction lives in the closures. That is why the main uncertainty sources in aeroheating predictions are mostly closure models.

## How it works

A reentry code needs four kinds of closure.

### 1. Thermal equation of state

$p = \sum_s \rho_s R_s T$ (Dalton's law for a mixture of thermally perfect gases). Free electrons, if present, use $T_v$ in a two-temperature model. At entry shock-layer densities the gas is ideal to excellent accuracy; non-ideal ([dense-gas](../thermo/gas-models.md#dense-gases)) corrections need far higher densities.

### 2. Caloric relations and the temperature inversion

The energies as functions of temperatures and composition, $e_s(T, T_v)$, from statistical mechanics or polynomial fits (see [energy modes](../thermo/energy-modes.md)). Every residual evaluation needs the temperatures from the conserved energies, which means inverting these relations in every cell.

In a **two-temperature** model the inversion is partly explicit. $T_v$ needs a Newton iteration on

$$
\rho e_v = \sum_s \rho_s\, e_{v,s}(T_v),
$$

because $e_v$ is nonlinear in $T_v$. Once $T_v$ is known, $T$ follows directly, since translation and rotation are fully excited and their energy is linear in $T$:

$$
\Big(\sum_s \rho_s c_{v,tr,s}\Big)\,T = \rho E - \tfrac12\rho|\mathbf u|^2 - \rho e_v - \sum_s \rho_s h_s^0 .
$$

In a **one-temperature** model, $T$ itself needs the Newton iteration. Either way the inversion is a common crash site: a bad update gives a negative or unphysical energy, the iteration fails, and the code aborts with a "temperature not found" error.

The physics: this is how energy is partitioned among modes. Dissociation absorbs a large amount of energy (about 9.8 eV per N₂ molecule), so the real post-shock temperature is several times lower than a perfect-gas prediction, the shock layer is denser, and the standoff is thinner (see [entry flow anatomy](../physics/entry-flow-anatomy.md#post-shock-density-and-standoff)).

### 3. Transport properties

Newtonian stress, Fourier conduction for each energy mode, and a diffusion model, with coefficients from mixing rules or kinetic theory. See [transport and diffusion](../thermo/transport-and-diffusion.md). These directly set the wall heat flux,

$$
q_w = \kappa\,\frac{\partial T}{\partial n} + \kappa_v\,\frac{\partial T_v}{\partial n} + \sum_s h_s J_{s,n},
$$

where the last term is chemical enthalpy carried to the wall by diffusing atoms, which recombine there if the wall is catalytic ([wall boundary conditions](../walls/wall-boundary-conditions.md)).

### 4. Kinetics

Arrhenius reaction rates (with Park's controlling temperature for dissociation) for $\dot\omega_s$, and Landau–Teller relaxation with Millikan–White times for $Q_{T\text{-}v}$. See [finite-rate chemistry](../thermo/finite-rate-chemistry.md) and [thermal nonequilibrium](../thermo/thermal-nonequilibrium.md). They decide whether dissociation keeps up with the flow.

### Cost per cell

With $n_s$ species, $n_r$ reactions and $k$ Newton iterations:

| Closure | Cost per cell per evaluation | Notes |
|---|---|---|
| Equation of state | $O(n_s)$ | Trivial. |
| Temperature inversion | $O(k\,n_s)$, times the number of electronic levels if summed | Moderate, but runs everywhere, every evaluation. |
| Transport (mixing rules) | $O(n_s^2)$ | Pairwise interaction terms. |
| Transport (full Stefan–Maxwell) | $O(n_s^3)$ | A linear solve per cell. |
| Kinetics | $O(n_r)$ rate evaluations | Each has an `exp` and a power; plus $O(n_s^2)$ T–V pairs. |
| Source Jacobian (implicit only) | dense $n\times n$ block per cell | Needed for [point-implicit](../sources/stiff-sources.md#point-implicit) treatment. |

!!! warning "Calibration"
    In reacting codes, thermochemistry is commonly a large share of runtime, sometimes the majority. For implicit codes the $O(n^3)$ block linear algebra usually dominates at these system sizes. The split varies a lot between codes and cases; don't quote a percentage without a profile of the specific code.

## Variants

The closures differ by [gas model](../thermo/gas-models.md): a perfect gas needs only $p = (\gamma-1)\rho e$; equilibrium air replaces kinetics with a table lookup $p(\rho, e)$, $T(\rho, e)$; finite-rate multi-temperature models need all four. Libraries such as [Mutation++](../../codes/index.md#mutationpp) package the thermodynamic, transport and kinetic closures for several codes.

## Implications

| Lens | Effect |
|---|---|
| Time step and cost | Closure evaluation scales with species and reactions; source stiffness from kinetics adds iterations or forces implicit treatment. |
| Steady vs unsteady | Neutral. |
| Accuracy | Dominates physical accuracy: transport sets heat flux, kinetics set composition and temperature profiles, thermodynamics sets standoff. |
| Robustness | Temperature inversion failures and negative species densities are the classic reacting-flow crashes. |
| Physics captured or lost | Everything high-temperature lives here: dissociation, ionization, nonequilibrium lag, catalysis. |
| Hardware / parallel fit | Pointwise and embarrassingly parallel, but branchy (Newton iterations, table lookups), which costs efficiency on GPUs. |

## In a run

Knobs: gas model, species and reaction set, rate source (Park, Dunn–Kang, ...), transport model, diffusion model. Symptoms: temperature-inversion aborts early in a run, negative species densities near shocks, and large changes in heat flux when switching the transport or diffusion model.

## Which codes

DPLR, LAURA and US3D use built-in thermochemistry with similar model families; SU2-NEMO can use [Mutation++](../../codes/index.md#mutationpp). See the [code pages](../../codes/index.md).

## See also

[Governing equations](governing-equations.md) · [Gas models](../thermo/gas-models.md) · [Energy modes](../thermo/energy-modes.md) · [The finite-volume pipeline](../spatial/finite-volume-pipeline.md#1-decode)

## References

Anderson, *Hypersonic and High-Temperature Gas Dynamics*; Park, *Nonequilibrium Hypersonic Aerodynamics*; Gnoffo, Gupta & Shinn (1989), NASA TP-2867. See the [bibliography](../../references.md).
