---
status: outline
---

# Central schemes and dissipation

<div class="page-meta" markdown>
**Slot:** Track 0.4 flux functions; Track 2.5–2.6 · **Depth:** [deep] · **Taught in:** [Lesson 0.4](../../course/track-0/0-4-flux-functions.md), [Track 2](../../course/track-2.md) (pending)
</div>

## What it is

Central schemes evaluate the face flux from a symmetric average of the two sides and add dissipation explicitly, rather than getting it implicitly from upwinding. The amount and placement of that dissipation is the whole design.

## The problem it solves

Upwind fluxes add dissipation everywhere, including in smooth regions where it damps turbulence and instability waves. Central schemes can be made nearly dissipation-free in smooth flow and add dissipation only where it's needed, at shocks.

## How it works

*(Outline, to be written in Lesson 0.4 and Track 2.)*

## Variants

### JST

Jameson–Schmidt–Turkel: a central flux plus a blend of second-difference dissipation (switched on near shocks by a pressure sensor) and fourth-difference background dissipation.

### Kinetic-energy-consistent fluxes

Fluxes designed so the discrete scheme conserves (or does not spuriously produce) kinetic energy, giving very low dissipation for LES and DNS. The US3D approach (Subbareddy & Candler, 2009) pairs a kinetic-energy-consistent central flux with upwind dissipation switched on only near shocks by a shock sensor (Ducros-type).

### Shock sensors

Ducros, pressure-based and other sensors that decide where dissipation is added.

### Shock regularization (IGR)

A different route, used in MFC: instead of capturing shocks with limiters and Riemann solvers, modify the equations with an "entropic pressure" obtained from an elliptic solve each step, so shocks are spread over a controlled width and simple central fluxes can be used. It is still explicit and CFL-limited. See [MFC](../../codes/mfc.md#information-geometric-regularization-igr).

## Implications

*(To be filled: dissipation vs heat-flux accuracy; sensor robustness; suitability for transition and SWBLI unsteadiness.)*

## In a run

*(To be filled.)*

## Which codes

US3D (KEC + shock-switched dissipation); many aerospace codes (JST); MFC (IGR).

## See also

[Riemann solvers](riemann-solvers.md) · [Flux-vector splitting](flux-vector-splitting.md) · [Shock instabilities](shock-instabilities.md)

## References

Jameson, Schmidt & Turkel (1981); Ducros et al. (1999); Subbareddy & Candler (2009); Pirozzoli (2011). See the [bibliography](../../references.md).
