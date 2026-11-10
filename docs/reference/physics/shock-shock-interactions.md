---
status: outline
---

# Shock–shock interactions

<div class="page-meta" markdown>
**Chapter:** 2 Entry flow physics · **Depth:** [deep]
</div>

## What it is

What happens when a shock from elsewhere (another body, a strut, a flap, an attachment fitting) crosses the bow shock of a blunt body. The two shocks meet, and the pattern of transmitted shocks, shear layers and jets that leaves the meeting point can strike the surface. Edney (1968) sorted the possibilities into six types according to where on the bow shock the incoming shock arrives.

## The problem it solves

This page describes a flow feature, not a method. It matters because some of these patterns concentrate the flow's energy onto a very small area of the surface, giving local heating and pressure far above the undisturbed stagnation values. Any vehicle with struts, protuberances, or neighbouring bodies in its shock layer has to be checked for it.

## How it works

*(Outline. Planned sections, with what each will establish.)*

### The six Edney types

A figure of the bow shock with the six impingement locations, and for each type the resulting pattern and what reaches the wall: a shock, a shear layer, a supersonic jet or an expansion.

| Type | What reaches the surface | Severity |
|---|---|---|
| I, II | a transmitted shock, which then interacts with the boundary layer | moderate; behaves like a [shock/boundary-layer interaction](shock-boundary-layer-interaction.md) |
| III | a shear layer that attaches to the surface | high |
| IV | a supersonic jet embedded in the subsonic shock layer, striking the surface nearly head-on | the most severe |
| V | a thin jet and transmitted shock near the upper sonic region | moderate |
| VI | an expansion fan | heating reduced |

The table is the orientation level; the mechanisms and the conditions separating the types are to be written from Edney's report.

### Type IV jet impingement

Why a supersonic jet forms inside the subsonic region, why its stagnation pressure is higher than that behind a single normal shock (the gas has been compressed through several weaker shocks instead), and why the peak is so narrow.

### Unsteadiness and sensitivity

The Type IV jet can oscillate; the peak location and level are sensitive to the impingement position and to the gas model.

## Variants

Two-dimensional (cylinder) and three-dimensional (sphere, fin leading edge) interactions; perfect-gas and high-enthalpy.

## Typical values

To be added from Edney (1968) and Wieting & Holden (1989), who measured interference heating on a cylinder at Mach 6 and 8. Peak heating in Type IV interactions is commonly quoted as an order of magnitude above the undisturbed stagnation value.

!!! warning "Calibration"
    The order-of-magnitude statement is the commonly cited level, not a figure taken from a specific table; the page will quote measured amplification factors with their test conditions when it is written.

## Trade-offs

To be written: resolving the jet (a feature far thinner than the shock layer) against the cost of the grid, and grid adaptation as the practical route.

## Effects on stability and robustness

- The jet and its bounding shear layers are thin, so the predicted peak rises with resolution until they are resolved; an under-resolved solution under-predicts the peak.
- Unsteady Type IV interactions don't converge with a steady solver.

## Implications

| Lens | Effect |
|---|---|
| Time step and cost | Local refinement around the jet dominates the cost. |
| Steady vs unsteady | Types I–III and V–VI are usually steady; Type IV may not be. |
| Accuracy (heat flux, pressure) | Peak values are grid-limited and sensitive to impingement location. |
| Robustness | Strong shocks crossing the grid at arbitrary angles; [shock instabilities](../spatial/shock-instabilities.md) and misaligned-grid errors apply. |
| Physics captured or lost | Dissipative schemes smear the jet and lower the peak. |
| Hardware / parallel fit | Suits adaptive, unstructured grids ([discretization families](../spatial/discretization-families.md)). |

## In a run

To be written. Starting point: a heating spike that grows with every grid refinement near a shock intersection is the signature of an unresolved jet.

## Which codes

To be written from validation papers.

## See also

[Entry flow anatomy](entry-flow-anatomy.md#interactions) · [Shock/boundary-layer interaction](shock-boundary-layer-interaction.md) · [Hypersonic shock relations](hypersonic-shock-relations.md)

## References

Edney (1968); Wieting & Holden (1989); Anderson, *Hypersonic and High-Temperature Gas Dynamics*. See the [bibliography](../../references.md).
