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

- **A computed laminar case (Candler 2011, §7.2.3).** Holden's Run 43: Mach 13.94 over a cylinder of 3.81 cm radius, free-stream unit Reynolds number 42,600/m (low enough that the interaction stays laminar), shock from a 10° wedge generator. Sweeping the impingement point through the six types on a $1200\times800$ grid around the half-cylinder, the worst case gave a peak pressure about **16 times** and a peak heat flux about **22 times** the undisturbed stagnation-point values. The worst case was a jet striking the surface obliquely, which heated more than the jet striking it normally.
- **Peak width:** about the size of the terminal shock in the jet; its spread comes mainly from the thermal boundary layer, so higher Reynolds numbers give even narrower peaks (Candler 2011, §7.2.3).
- **Agreement with experiment:** laminar computations over-predicted measured peak pressure and heating by about 30%; accounting for finite gauge size and varying surface temperature improved the agreement (D'Ambrosio 2002, as summarized by Candler 2011, §7.2.3).
- **High enthalpy:** dissociation caused by the interaction changes the shock strengths and typically **reduces** the peak heating (Sanderson, Hornung & Sturtevant 2004).
- Measured amplification factors at Mach 6 and 8 for types III–V: to be added from Wieting & Holden (1989) and Holden et al. (1998).

!!! warning "Calibration"
    The 16× and 22× factors are from one laminar computation at one condition, not a design rule. Transitional and turbulent interactions, and three-dimensional ones, have different peaks; Holden (2011, §6.4) gives correlations of measured shock–shock heating that this page will draw on.

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

Edney (1968); Wieting & Holden (1989); Holden et al. (1998); D'Ambrosio (2002); Sanderson, Hornung & Sturtevant (2004); Anderson, *Hypersonic and High-Temperature Gas Dynamics*; Babinsky & Harvey (eds.) (2011): Délery, ch. 2, §2.2.3 (Edney classification with shock polars), Holden, ch. 6, §6.4 (shock–shock experiments and correlations), Candler, ch. 7, §7.2.3 (computed cylinder interactions). See the [bibliography](../../references.md).
