---
status: outline
---

# Scale-resolving methods: DNS, LES and hybrid RANS/LES

<div class="page-meta" markdown>
**Chapter:** 4 Turbulence · **Depth:** [feel]
</div>

## What it is

The methods that compute the turbulent motion itself rather than its average. **DNS** (direct numerical simulation) resolves every scale down to the dissipative one. **LES** (large-eddy simulation) resolves the energy-containing eddies and models the small ones with a subgrid-scale (SGS) model, either explicitly or implicitly through the numerical dissipation (**implicit LES**). **Hybrid RANS/LES** (the detached-eddy family: DES, DDES, IDDES) uses RANS near walls and LES away from them. **Wall-modelled LES** resolves the outer boundary layer and models the near-wall layer.

## The problem it solves

RANS can't represent unsteadiness, transition, or flows where the turbulence is far from equilibrium. On entry vehicles that means capsule wakes and backshell heating, the low-frequency motion of separated [shock/boundary-layer interactions](../physics/shock-boundary-layer-interaction.md#low-frequency-unsteadiness), supersonic retropropulsion plumes, transition mechanisms, and the reference databases that RANS models are judged against. These methods trade cost for physics; the page sets out how much cost, for how much physics.

## How it works

*(Outline. Planned sections, with what each will establish.)*

### Resolution requirements

- What must be resolved for DNS (Kolmogorov scale; near walls, the viscous sublayer), wall-resolved LES (near-wall streaks), and wall-modelled LES (the outer layer only), expressed as spacings in wall units ([fundamentals](fundamentals.md#wall-turbulence-in-wall-units)).
- Grid-point scaling with Reynolds number for a flat-plate boundary layer: DNS $\sim Re^{37/14}$, wall-resolved LES $\sim Re^{13/7}$, wall-modelled LES $\sim Re$ (Choi & Moin 2012). Figure to draw: the three scalings, with a capsule heat-pulse Reynolds number marked.
- Time step from the smallest resolved cell and acoustics; total time from flow-throughs or low-frequency periods (worked example on [SWBLI](../physics/shock-boundary-layer-interaction.md#worked-example-the-cost-of-resolving-unsteadiness-illustrative)).

### Direct numerical simulation

- No model; numerics must be low-dissipation and high-order or kinetic-energy-consistent ([central schemes](../spatial/central-schemes.md)), with shock capturing confined to shocks.
- Hypersonic DNS in practice: temporal and spatially developing boundary layers, cold walls (Duan, Beekman & Martin; Huang et al. 2020), transition on cones and elliptic cones (the HIFiRE-5 example on [central schemes](../spatial/central-schemes.md#typical-values)).
- Inflow turbulence for spatially developing boundary layers: recycling–rescaling and synthetic (digital-filter) methods, and the development length they cost.

### Large-eddy simulation

- Filtering: Favre-filtered equations, SGS stress and SGS heat flux; compressible SGS terms usually neglected and when that's justified (Garnier, Adams & Sagaut 2009).
- SGS models: Smagorinsky (constant, wall damping), dynamic procedure (Germano et al.), WALE (correct near-wall scaling), Vreman and $\sigma$ models; scale-similarity and mixed models as neighbours.
- Interaction with shock capturing: SGS dissipation vs numerical dissipation, shock sensors (Ducros), why upwind schemes can swamp the SGS model.
- Wall-resolved vs wall-modelled LES. Wall models: equilibrium (ODE) models, the exchange location, and the wall heat flux they return; why cold walls and pressure gradients strain equilibrium wall models (Kawai & Larsson 2012; Larsson et al. 2016).

### Implicit LES

- Letting the numerical dissipation of a shock-capturing scheme play the role of the SGS model (MILES, ILES; Boris et al. 1992; Grinstein, Margolin & Rider 2007).
- Why it is common in hypersonics (WENO and TENO codes, MFC among them as the contrast case) and what it costs in rigour: the effective SGS dissipation depends on grid, scheme and limiter, not on physics; grid convergence means approaching DNS.
- Neighbours told apart: ILES vs under-resolved DNS vs explicit LES on a dissipative scheme.

### Hybrid RANS/LES

- **DES (DES97):** Spalart–Allmaras with the wall distance replaced by $\min(d, C_{DES}\Delta)$, so the model acts as RANS near walls and as an SGS model where the grid is fine. Failure modes: modelled-stress depletion and grid-induced separation when the grid is refined inside the boundary layer.
- **DDES:** a shielding function $f_d$ that keeps attached boundary layers in RANS regardless of the grid (Spalart et al. 2006).
- **IDDES:** adds a wall-modelled LES branch so that, with inflow turbulence, the method acts as WMLES inside the boundary layer (Shur et al. 2008).
- The **grey area**: delay in generating resolved turbulence where RANS hands over to LES (separated shear layers); remedies (vorticity-based length scales, synthetic turbulence, zonal DES (Deck 2012)).
- Neighbours: URANS vs DES vs LES; SST-based DES variants; scale-adaptive simulation as a related idea.
- Entry use: capsule wakes and backshell, base flows, retropropulsion plumes.

### Time integration and statistics

- Explicit low-storage RK for DNS/LES on GPUs vs implicit [dual time stepping](../time/dual-time-stepping.md) for hybrid methods on stretched wall grids ([explicit vs implicit](../time/explicit-vs-implicit.md)).
- Averaging times, statistical convergence, spectra; the transient to discard.

## Variants

### Direct numerical simulation

See above.

### Wall-resolved LES

See above.

### Wall-modelled LES

See above.

### Implicit LES

See above.

### Detached-eddy simulation

DES97, DDES, IDDES, zonal DES.

Comparison table to build: what is modelled, near-wall grid requirement, grid-point scaling, typical entry application, main failure mode.

## Typical values

To be sourced: wall-unit spacings for DNS and wall-resolved LES (Georgiadis, Rizzetta & Fureby 2010; Pope 2000, ch. 13); the Choi & Moin constants behind the scalings above; $C_{DES}$; hypersonic DNS grid sizes and costs from published runs.

## Trade-offs

To be written: physics captured vs cost for each method; explicit SGS model vs ILES; hybrid methods' dependence on the grid and on where the interface falls.

## Effects on stability and robustness

To be written: kinetic-energy-preserving numerics and aliasing; shock sensors; positivity in strong expansions; the hybrid interface; inflow-generation transients.

## Implications

| Lens | Effect |
|---|---|
| Time step and cost | Orders of magnitude above RANS; scales steeply with Reynolds number except for wall-modelled LES. |
| Steady vs unsteady | Inherently unsteady; statistics need long records. |
| Accuracy (heat flux, pressure) | Wall-resolved methods get heat flux from resolved gradients; wall-modelled and hybrid methods inherit the wall model's or RANS model's heat flux. |
| Robustness | Low-dissipation numerics near shocks; grid-sensitive hybrid interfaces. |
| Physics captured or lost | Unsteadiness, large-scale structures, (DNS) transition; subgrid effects modelled or left to numerics. |
| Hardware / parallel fit | Explicit, high-arithmetic-intensity methods map well to GPUs ([explicit vs implicit](../time/explicit-vs-implicit.md)). |

## In a run

Planned: choosing the method from the Reynolds number and what output is needed; grid design in wall units; inflow turbulence; how long to run and what to average; signs of an under-resolved LES (spectra, energy pile-up) and of a DES grey area.

## Which codes

To be filled from methods papers. At the general level: [US3D](../../codes/index.md#us3d) runs DNS, LES and hybrid RANS/LES with low-dissipation fluxes ([central schemes](../spatial/central-schemes.md)); explicit high-order research codes (MFC, ALPACA/JAX-Fluids) are ILES-style contrasts.

!!! warning "Calibration"
    Which hybrid variants and SGS models each production code offers is version-specific; the page will cite each code's documentation.

## See also

[Turbulence fundamentals](fundamentals.md) · [RANS models](rans-models.md) · [Hypersonic boundary layers](../physics/turbulence-modeling.md) · [Transition](transition.md) · [Central schemes](../spatial/central-schemes.md) · [Dual time stepping](../time/dual-time-stepping.md) · [Shock/boundary-layer interaction](../physics/shock-boundary-layer-interaction.md)

## References

Pope (2000), chs. 9, 13; Garnier, Adams & Sagaut (2009); Choi & Moin (2012); Georgiadis, Rizzetta & Fureby (2010); Smagorinsky (1963); Germano et al. (1991); Nicoud & Ducros (1999); Boris et al. (1992); Grinstein, Margolin & Rider (2007); Kawai & Larsson (2012); Larsson et al. (2016); Spalart et al. (1997); Spalart et al. (2006); Shur et al. (2008); Spalart (2009); Deck (2012); Duan, Beekman & Martin (2010, 2011); Huang et al. (2020); Knight & Zheltovodov, chs. 4–5 in Babinsky & Harvey (2011). See the [bibliography](../../references.md).
