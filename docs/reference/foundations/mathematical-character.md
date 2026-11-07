# Mathematical character: hyperbolic, parabolic, elliptic

<div class="page-meta" markdown>
**Slot:** Track 0.1 governing equations · **Depth:** [deep] · **Taught in:** [Lesson 0.1](../../course/track-0/0-1-governing-equations.md)
</div>

## What it is

The compressible Navier–Stokes equations combine two kinds of mathematics. The inviscid part is **hyperbolic**: information travels as waves at finite speeds, and discontinuities can form and persist. The viscous part is **parabolic** in time (diffusion), and its steady version is **elliptic**. Which character dominates where decides how a solver must be built: which terms get upwinded, which time-step limits apply, and whether a steady problem can be marched in space.

## The problem it solves

Knowing the character tells you what a discretization must respect. Upwind [flux functions](../spatial/riemann-solvers.md) exist because the inviscid part has directional wave propagation; [viscous fluxes](../spatial/viscous-fluxes.md) are central because diffusion has no preferred direction; [time-step limits](../time/time-step-limits.md) come in two kinds because the two characters impose different stability conditions; and [space marching](../special/space-marching.md) works only where the steady problem is hyperbolic in the marching direction.

## How it works

### Hyperbolic

A first-order system $\partial_t U + A(U)\,\partial_x U = 0$ is hyperbolic when the **flux Jacobian** $A = \partial F/\partial U$ has real eigenvalues and a complete set of eigenvectors. The eigenvalues are the wave speeds; the eigenvectors say what each wave carries. For the 1D Euler equations,

$$
\lambda = u - a,\quad u,\quad u + a :
$$

two acoustic waves and one entropy (contact) wave. Information at a point comes only from inside the region bounded by the fastest characteristics (the domain of dependence).

For a reacting multi-temperature mixture, each species equation and the vibrational-energy equation add another copy of $\lambda = u$. These quantities are passively convected, so the wave structure is unchanged: two acoustic waves plus a contact, with species and $e_v$ riding the contact. This is good news. The system stays hyperbolic, the CFL limit is unchanged, and solvers like [HLLC](../spatial/riemann-solvers.md#hllc) extend trivially.

The sound speed in these eigenvalues is the **frozen** sound speed: on acoustic time scales, chemistry and any modes not equilibrated with $T$ can't respond. For a two-temperature model,

$$
a_f^2 = \gamma_f\,\frac{p}{\rho},\qquad \gamma_f = 1 + \frac{R_{mix}}{c_{v,tr}},
$$

with $c_{v,tr}$ the translational–rotational heat capacity per unit mass (in a one-temperature model the vibrational heat capacity is included). The equilibrium sound speed, relevant only when relaxation is much faster than the wave, is lower.

### Parabolic

Diffusion, $\partial_t u = \nu\,\partial_x^2 u$, has no finite propagation speed: a disturbance is felt everywhere instantly, with exponentially small amplitude far away. It smooths everything, so no discontinuity survives. The viscous stresses, heat conduction and species diffusion in [the governing equations](governing-equations.md) are all of this type.

Compressible Navier–Stokes is technically **incompletely parabolic**, since the continuity equation has no diffusion term. With viscosity a real shock isn't a discontinuity: it is a few mean free paths thick. That is far thinner than any continuum CFD cell, so on the grid it still looks like a discontinuity, which is why Navier–Stokes codes still need shock capturing.

### Elliptic

Steady diffusion is Laplace's or Poisson's equation: every point influences every other point, and there's no direction in which a solution can be marched. In steady compressible flow, ellipticity also appears without viscosity: wherever the flow is **subsonic**, pressure disturbances propagate upstream as well as downstream.

### Mixed character around a blunt body

The steady problem around a capsule is mixed. Behind the bow shock, the stagnation region is subsonic, so the steady equations there are elliptic. Beyond the sonic line the shock layer is supersonic, and the steady inviscid equations are hyperbolic in the flow direction: information only travels downstream.

<figure markdown>
![Blunt body regions](../../assets/figures/blunt_body_regions.svg)
<figcaption>The subsonic pocket between the bow shock and the nose is elliptic in the steady sense; past the sonic line, the shock layer is supersonic. Shock shape from Billig's perfect-gas correlation; the sonic line is schematic.</figcaption>
</figure>

Historically this made the steady **blunt-body problem** notoriously hard: no single steady method suited both regions. The breakthrough was to solve the *unsteady* equations instead, which are hyperbolic in time everywhere regardless of local Mach number, and march them to steady state (Moretti and Abbett, 1966). Every modern code still does this, in physical or pseudo-time.

The solver "knows" each region locally, at every face, through the signs of the eigenvalues. In supersonic regions all eigenvalues across a face have the same sign, and an upwind flux such as [Steger–Warming](../spatial/flux-vector-splitting.md#steger-warming) automatically takes only the upstream contribution. In subsonic regions it mixes both sides. Relaxation solvers exploit the same fact: Gauss–Seidel sweeps aligned with a supersonic flow converge almost in one pass (see [relaxation methods](../time/relaxation-methods.md)).

## Implications

| Lens | Effect |
|---|---|
| Time step and cost | Two explicit stability limits: convective ($\Delta x/(|u|+a)$) and viscous ($\Delta x^2/2\nu$). See [time-step limits](../time/time-step-limits.md). |
| Steady vs unsteady | Steady problems with subsonic regions must be solved globally (time marching or iteration); purely supersonic regions can be [space-marched](../special/space-marching.md). |
| Accuracy | Upwinding the hyperbolic part and centring the parabolic part is what each term's character demands. |
| Robustness | Wrong upwinding (taking information from downstream in a supersonic region) is unstable. |
| Physics captured or lost | Hyperbolic structure permits shocks and contacts; diffusion sets boundary layers and the wall heat flux. |
| Hardware / parallel fit | Elliptic coupling is global and needs many iterations or global solves; hyperbolic coupling is local. |

## In a run

You see the character in convergence behaviour: the subsonic stagnation region usually converges last in a steady blunt-body run, while supersonic regions settle quickly. Space-marching codes refuse to march, or produce "departure solutions," when the marching plane contains too much subsonic or reversed flow.

## Which codes

Universal; this is mathematics, not a code choice. What differs between codes is how they exploit it (upwind flux type, sweep directions, line-solve directions).

## See also

[Governing equations](governing-equations.md) · [Riemann solvers](../spatial/riemann-solvers.md) · [Time-step limits](../time/time-step-limits.md) · [Space marching](../special/space-marching.md) · [Entry flow anatomy](../physics/entry-flow-anatomy.md)

## References

Hirsch, *Numerical Computation of Internal and External Flows*; LeVeque, *Finite Volume Methods for Hyperbolic Problems*; Anderson, *Hypersonic and High-Temperature Gas Dynamics*; Moretti & Abbett (1966); Billig (1967). See the [bibliography](../../references.md).
