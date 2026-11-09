---
status: draft
---

# Space marching: thin-layer and parabolized Navier–Stokes

<div class="page-meta" markdown>
**Slot:** Track 2.10 (governing-equation reductions) · **Depth:** [feel], with the math
</div>

## What it is

Reduced forms of the Navier–Stokes equations that drop the viscous derivatives along the main flow direction. The **thin-layer** equations keep time and are solved by ordinary time marching. The **parabolized Navier–Stokes** (PNS) equations also drop time and are solved by marching in the flow direction, plane by plane, as if that coordinate were time.

## The problem it solves

For a slender vehicle in supersonic flow, a full 3D steady solve is expensive. If information only travels downstream, the solution can be built one cross-sectional plane at a time: a 2D problem per station instead of a global 3D iteration, which was historically decisive for slender bodies and the Shuttle windward side.

## How it works

### Order-of-magnitude reduction {#thin-layer-navier-stokes}

Write the steady 3D equations as $\partial_x\mathbf E + \partial_y\mathbf F + \partial_z\mathbf G = 0$, each flux including its viscous part, with $x$ along the body and $y$ normal to it. In a boundary layer of thickness $\delta$ on a body of length $L$,

$$
\partial_y \sim \frac1\delta,\qquad \partial_x \sim \frac1L,\qquad \frac{\delta}{L} \sim Re_L^{-1/2}.
$$

A streamwise viscous term such as $\mu\,\partial_x^2 u$ is smaller than $\mu\,\partial_y^2 u$ by $(\delta/L)^2 \sim 1/Re_L$. Dropping all $x$-derivatives inside the viscous fluxes gives the **thin-layer** approximation (time kept). PNS also drops the time derivative:

$$
\partial_x\mathbf E_{\text{inv}}(\mathbf U) = -\partial_y\big(\mathbf F - \mathbf F_v\big) - \partial_z\big(\mathbf G - \mathbf G_v\big),
$$

where the viscous fluxes now contain only cross-plane derivatives.

### Marching

Treat $x$ like time and march implicitly, for example

$$
\frac{\mathbf E^{k+1} - \mathbf E^k}{\Delta x} = -\,\text{RHS}(\mathbf U^{k+1}),
$$

solving a nonlinear 2D problem (by Newton iteration) at each station $k+1$. The march starts from an initial data plane, typically extracted from a full Navier–Stokes solution of the blunt nose where the flow has become supersonic.

### Well-posedness and the subsonic sublayer

Marching in $x$ is well-posed only if information travels only in $+x$: all eigenvalues of $\partial\mathbf E/\partial\mathbf U$ (relative to the $x$-direction) must be positive, roughly the condition $u > a$. Outside the boundary layer that holds. In the subsonic sublayer near the wall, the streamwise pressure gradient carries information upstream (an eigenvalue $u - a < 0$), and a naive march blows up into **departure solutions**.

**Vigneron's** fix splits the streamwise pressure in $\mathbf E$: keep a fraction $\omega p$ in the marched flux, with

$$
\omega = \min\!\left(1,\ \frac{\sigma\,\gamma M_x^2}{1 + (\gamma - 1)M_x^2}\right),
$$

$\sigma < 1$ a safety factor and $M_x$ the local streamwise Mach number, and neglect or lag the remaining $(1-\omega)\,\partial_x p$. The march becomes stable at the cost of a small approximation in the sublayer.

### Where it fails

Reversed flow (separation at a flare, ramp or body-flap) sends information upstream through the whole layer, so PNS cannot march through a separated SWBLI; the region must be solved globally. Subsonic regions (blunt noses) can't be marched at all. The analyst sets up the split: full Navier–Stokes where the flow is elliptic, PNS from a supersonic starting plane onward.

## Variants

### Thin-layer Navier–Stokes {#thin-layer-variant}

Time-marched; used as an option in some codes to save viscous-flux work on attached flows.

### Iterative (global) PNS

Multiple marching sweeps with the lagged pressure updated each sweep, allowing limited upstream influence.

## Implications

| Lens | Effect |
|---|---|
| Time step and cost | One 2D solve per station instead of a global 3D iteration: very cheap for slender bodies. |
| Steady vs unsteady | Steady only. |
| Accuracy | Good for attached, supersonic flows; Vigneron splitting introduces a small sublayer approximation. |
| Robustness | Fails with departure solutions where the march isn't well-posed. |
| Physics captured or lost | Loses all upstream influence: no separation, no subsonic regions. |
| Hardware / parallel fit | Sequential in $x$; parallel within each plane. |

## In a run

Knobs: starting plane, marching step, Vigneron safety factor. Symptoms: departure solutions, march failure at separation.

## Which codes

!!! warning "Calibration"
    PNS codes were prominent in NASA and industry for slender vehicles (e.g. UPS at Langley); some general codes offer thin-layer options. Specific current availability to be checked.

## See also

[Mathematical character](../foundations/mathematical-character.md) · [Governing equations](../foundations/governing-equations.md#thin-layer-and-parabolized-navier-stokes) · [Viscous fluxes](../spatial/viscous-fluxes.md)

## References

Vigneron, Rakich & Tannehill (1978); Tannehill, Anderson & Pletcher, *Computational Fluid Mechanics and Heat Transfer*; Anderson, *Hypersonic and High-Temperature Gas Dynamics*. See the [bibliography](../../references.md).
