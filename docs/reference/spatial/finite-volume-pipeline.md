# The finite-volume pipeline

<div class="page-meta" markdown>
**Chapter:** 6 Spatial discretization · **Depth:** [deep]
</div>

## What it is

The sequence of operations a cell-centred finite-volume code performs to turn the stored cell averages $\bar{\mathbf U}_i$ into a residual $\mathbf R_i$ and then an update. This page is the hub: each step links to the page that covers it in depth.

## The problem it solves

It connects every slot of the solver. Knowing the order of operations tells you where a given method acts, what it receives as input, and which other choices it interacts with.

## How it works

```mermaid
flowchart TD
    A["Cell averages Ū (conserved)"] -->|"1. decode: EOS + caloric inversion"| B["Primitives W = (ρ_s, u, p, T, T_v)"]
    B -->|"2. reconstruct: slopes + limiter"| C["Face states W_L, W_R"]
    C -->|"3. inviscid numerical flux"| D["F*_inv at each face"]
    B -->|"4. face gradients + transport"| E["F_visc at each face"]
    B -->|"5. kinetics + T–V exchange"| F["Sources S_i"]
    D --> G(["Residual R_i = Σ faces (F*_inv − F_visc)·A − S_i V_i"])
    E --> G
    F --> G
    G -->|"6. update (explicit or implicit)"| A
```

Each cell stores $\bar{\mathbf U}_i$, the average of the conserved variables over its volume. Primitives are never the state; they are a derived view recomputed every evaluation, because the fluxes and sources are written in them. The update itself is always a conservative flux difference ([why that matters](../foundations/conservation-and-weak-solutions.md)).

### 1. Decode

Convert $\bar{\mathbf U}_i \to \mathbf W_i$. This is where the [closures](../foundations/closing-the-system.md) are applied.

For a calorically perfect gas it is closed-form: $u = (\rho u)/\rho$, $p = (\gamma-1)(\rho E - \tfrac12\rho u^2)$. For a two-temperature mixture, species densities come straight from $\mathbf U$, $T_v$ needs a Newton solve, and $T$ then follows directly ([details](../foundations/closing-the-system.md#2-caloric-relations-and-the-temperature-inversion)).

### 2. Reconstruct

Build face states $\mathbf W_L$, $\mathbf W_R$ on each side of every face. First order uses the cell values themselves; second order builds a limited slope in each cell from its neighbours and evaluates it at the faces; WENO blends several candidate polynomials. See [reconstruction and limiters](reconstruction.md) and [WENO](weno.md).

A worked example with the minmod limiter, for any primitive $q$ in 1D:

$$
\begin{gathered}
\Delta^- = q_i - q_{i-1},\qquad \Delta^+ = q_{i+1} - q_i,\qquad \sigma_i = \operatorname{minmod}(\Delta^-,\Delta^+),\\[1ex]
q^L_{i+1/2} = q_i + \tfrac12\sigma_i,\qquad q^R_{i-1/2} = q_i - \tfrac12\sigma_i .
\end{gathered}
$$

With $q = 1, 2, 4$ in cells $i-1, i, i+1$: $\Delta^- = 1$, $\Delta^+ = 2$, so $\sigma_i = 1$ and $q^L_{i+1/2} = 2.5$ (an unlimited central slope would give 2.75). At an extremum, $q = 1, 3, 2$, the slopes have opposite signs, $\sigma_i = 0$, and the cell goes flat (locally first order).

<figure markdown>
![Cell averages, reconstruction and the face flux](../../assets/figures/fv_stencil.svg)
<figcaption markdown="span">Steps 2 and 3 in one dimension. Black dots are the stored cell averages (1, 1.2, 2, 4, 4.4, 4.5). Blue lines are the minmod-limited linear reconstructions inside each cell. At face $i+\tfrac12$ the two reconstructions disagree: the left state is $2 + \tfrac12(0.8) = 2.4$ and the right state is $4 - \tfrac12(0.4) = 3.8$. The flux function turns that pair into a single flux, which is subtracted from cell $i$ and added to cell $i+1$. Computed from the minmod formula above.</figcaption>
</figure>

The jump between $q_L$ and $q_R$ at a face is not an error to be removed. It is the scheme's measure of how under-resolved the solution is there, and the flux function's dissipation is proportional to it. In smooth, well-resolved flow the two states nearly coincide and every flux function gives nearly the same answer; at a shock they differ by the full jump and the choice of flux function matters most.

### 3. Inviscid flux

Evaluate a numerical flux function $\hat{\mathbf F}(\mathbf W_L, \mathbf W_R)$ at each face. There is always a flux function; a Riemann solver is one family of them:

- [Riemann solvers](riemann-solvers.md): exact (Godunov), Roe, HLL, HLLC, Rusanov.
- [Flux-vector splitting](flux-vector-splitting.md): Steger–Warming, van Leer, AUSM family. These split the flux by the signs of the eigenvalues instead of solving a Riemann problem.
- [Central schemes](central-schemes.md): central differencing plus artificial dissipation (JST), kinetic-energy-consistent fluxes with shock-switched dissipation; and shock regularization (IGR) as a different route.

All of them need $p$, $a$ and $u_n$ on each side, which are primitive quantities.

### 4. Viscous flux

Face gradients of $\mathbf u$, $T$, $T_v$ and mass fractions from neighbouring cells, face-averaged transport coefficients, then stresses, heat fluxes and diffusion fluxes. Always central-type. See [viscous fluxes](viscous-fluxes.md).

### 5. Sources

Evaluate $\dot\omega_s$ and $Q_{T\text{-}v}$ at the cell centre from $\mathbf W_i$. An explicit code adds them to the residual; a point-implicit or fully implicit code also puts $\partial\mathbf S/\partial\mathbf U$ into its left-hand matrix, which removes the chemistry stability limit. See [stiff source terms](../sources/stiff-sources.md).

### 6. Update

Inviscid and viscous fluxes are computed separately but **summed into one residual**; they are not solved separately:

$$
\mathbf R_i = \sum_{\text{faces}}\big(\hat{\mathbf F}_{\text{inv}} - \mathbf F_{\text{visc}}\big)\cdot\mathbf A_f - \mathbf S_i V_i .
$$

Explicit: $\bar{\mathbf U}_i \leftarrow \bar{\mathbf U}_i - \frac{\Delta t}{V_i}\mathbf R_i$, with a Runge–Kutta scheme repeating steps 1–5 once per stage ([explicit methods](../time/explicit-methods.md)). Implicit: assemble $(\mathbf I\,V/\Delta t + \partial\mathbf R/\partial\mathbf U)\,\Delta\mathbf U = -\mathbf R$ and solve it approximately ([implicit methods](../time/implicit-methods.md), [relaxation](../time/relaxation-methods.md)). Boundary conditions enter as fluxes or ghost-cell states at boundary faces ([boundary conditions](boundary-conditions.md)).

## Typical values

- Stencil width per face: 2 cells (first order), 4 cells (MUSCL, second order), 6 cells (fifth-order WENO). That is also the number of ghost or halo layers needed on each side: 1, 2, 3.
- Evaluations per explicit time step: one pass of steps 1–5 per Runge–Kutta stage, so three passes for SSP-RK3.
- Share of cost: for a perfect gas the inviscid flux and reconstruction dominate. With finite-rate chemistry, the decode (temperature inversion), transport properties and source terms often cost more than the fluxes ([closing the system](../foundations/closing-the-system.md)).
- Unknowns per cell: 5 for a 3-D perfect gas, 16 for 11-species two-temperature air ([governing equations](../foundations/governing-equations.md)).

## Trade-offs

- **Store conserved, compute with primitives.** Conservation is guaranteed by the flux-difference update; the price is a decode in every cell at every evaluation.
- **One residual for everything.** Inviscid, viscous and source contributions each get the discretization that suits them, then are summed. The alternative, operator splitting (advance each piece separately), is simpler for stiff chemistry but leaves a splitting error at steady state ([stiff source terms](../sources/stiff-sources.md)).
- **Higher-order reconstruction.** Less dissipation per cell, but a wider stencil, more work per face and more ways to produce an unphysical face state.

## Effects on stability and robustness

- **Decode** fails when the conserved state is unphysical: negative internal energy after subtracting kinetic energy, or a temperature iteration that doesn't converge. This is the most common place for a run to abort.
- **Reconstruct** can overshoot to a negative density or pressure at a face even when both cells are fine. Limiters, primitive-variable reconstruction and first-order fallback are the defences ([reconstruction](reconstruction.md#which-variables-to-reconstruct)).
- **Inviscid flux** decides shock behaviour: too little dissipation and the shock can go unstable ([shock instabilities](shock-instabilities.md)); too much and the boundary layer is smeared.
- **Sources** bring stiffness, which an explicit update can't handle at a flow-sized time step.

## Implications

| Lens | Effect |
|---|---|
| Time step and cost | Explicit cost is one pipeline pass per RK stage; implicit adds Jacobian assembly and a linear solve per iteration. |
| Steady vs unsteady | The same residual serves both; only step 6 changes. |
| Accuracy | Set by reconstruction order, flux dissipation and gradient quality; heat flux is especially sensitive to steps 3 and 4 near the wall. |
| Robustness | Steps 1 and 2 are where positivity is won or lost. |
| Physics captured or lost | Each step can smear physics: limiters clip peaks, dissipative fluxes smear contacts and boundary layers. |
| Hardware / parallel fit | Steps 1–5 are local and map well to GPUs; step 6 is where implicit methods introduce global data dependencies. |

## In a run

Every input deck selects something in each step: reconstruction order and limiter (step 2), flux scheme and entropy fix (step 3), gradient method (step 4), source treatment (step 5), time integrator and CFL (step 6).

## Which codes

All cell-centred finite-volume codes follow this structure (DPLR, LAURA, US3D, Eilmer, MFC). Vertex-based codes (FUN3D, SU2) do the same on a dual mesh around each node. See [discretization families](discretization-families.md).

## See also

[Reconstruction](reconstruction.md) · [Riemann solvers](riemann-solvers.md) · [Viscous fluxes](viscous-fluxes.md) · [Stiff sources](../sources/stiff-sources.md) · [Implicit methods](../time/implicit-methods.md)

## References

Blazek, *Computational Fluid Dynamics: Principles and Applications*; Hirsch, *Numerical Computation of Internal and External Flows*; LeVeque, *Finite Volume Methods for Hyperbolic Problems*. See the [bibliography](../../references.md).
