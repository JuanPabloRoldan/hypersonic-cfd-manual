# Viscous fluxes and gradients

<div class="page-meta" markdown>
**Slot:** Track 0.2/0.4, the viscous part of the residual · **Depth:** [deep] · **Taught in:** [Lesson 0.1](../../course/track-0/0-1-governing-equations.md) (overview); details in Lesson 0.2
</div>

## What it is

The discretization of $\mathbf F_{\text{visc}}$: viscous stresses (momentum diffusion), heat conduction for each temperature, and species mass diffusion. Each is a transport coefficient times a gradient, so the work is computing **face gradients** and **face-averaged coefficients**.

## The problem it solves

Diffusion is what sets boundary layers, skin friction and, above all, the wall heat flux $q_w = \kappa\,\partial T/\partial n + \dots$ ([closures](../foundations/closing-the-system.md#3-transport-properties)). An inviscid flux function knows nothing about it.

## How it works

Diffusion is [parabolic](../foundations/mathematical-character.md#parabolic): it has no preferred direction, so there is nothing to upwind. Central-type approximations are both natural and stable. In 1D on a uniform grid,

$$
q_{i+1/2} = -\kappa_{i+1/2}\,\frac{T_{i+1} - T_i}{\Delta x},\qquad \kappa_{i+1/2} = \tfrac12(\kappa_i + \kappa_{i+1}).
$$

In multiple dimensions on general grids, face gradients are built from cell gradients (Green–Gauss or least-squares) averaged to the face, plus a **face-normal correction** that uses the direct difference across the face. Without that correction, averaged gradients decouple neighbouring cells and allow odd–even oscillations.

The inviscid and viscous fluxes are computed separately but summed into **one residual** at each face ([the pipeline](finite-volume-pipeline.md#6-update)): one equation, assembled from pieces that each get the discretization suited to their mathematical character.

### Near the wall

Heat flux is a gradient at the wall, so its accuracy depends on resolving the thermal boundary layer. The usual guideline is a wall **cell Reynolds number** of order one or below,

$$
Re_\Delta = \frac{\rho\,a\,\Delta n}{\mu} \lesssim 1\ \text{(order of magnitude)},
$$

an accepted practice supported by grid studies in the aeroheating literature rather than a theorem ([Track 2.4](../../course/track-2.md)). Those thin cells are also why the [viscous time-step limit](../time/time-step-limits.md) binds for explicit schemes.

## Variants

### Thin-layer approximation

Keep only viscous derivatives normal to the wall. Cheaper; appropriate for attached boundary layers on well-aligned grids. See [space marching](../special/space-marching.md#thin-layer-navier-stokes).

### Discontinuous Galerkin viscous treatments

DG needs special viscous discretizations (BR2, interior penalty, LDG), but these are still symmetric, not upwinded. *(Track 2.7.)*

## Implications

| Lens | Effect |
|---|---|
| Time step and cost | Adds the $\Delta x^2/(2\nu)$ explicit limit; gradient reconstruction costs about as much as an inviscid flux evaluation. |
| Steady vs unsteady | Neutral. |
| Accuracy | Gradient quality on stretched, skewed near-wall cells directly controls heat flux and skin friction. |
| Robustness | Poor face-normal correction on skewed grids gives odd–even noise in wall quantities. |
| Physics captured or lost | Sets boundary-layer structure; thin-layer variants drop streamwise diffusion (fine for attached layers, wrong in separation). |
| Hardware / parallel fit | Local stencil; GPU-friendly. |

## In a run

Knobs: gradient method, thin-layer vs full viscous terms, transport model. Symptoms: noisy wall heat flux on skewed or tetrahedral near-wall cells; heat flux that changes with wall spacing (wall $Re_\Delta$ too large).

## Which codes

All Navier–Stokes codes use central-type viscous discretizations; differences lie in gradient reconstruction on unstructured grids (FUN3D, US3D, SU2) vs straightforward differences on structured grids (DPLR, LAURA).

## See also

[Time-step limits](../time/time-step-limits.md) · [Transport and diffusion](../thermo/transport-and-diffusion.md) · [Wall boundary conditions](../walls/wall-boundary-conditions.md)

## References

Blazek, *Computational Fluid Dynamics: Principles and Applications*; Hirsch, *Numerical Computation of Internal and External Flows*. See the [bibliography](../../references.md).
