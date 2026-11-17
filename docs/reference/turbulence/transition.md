---
status: outline
---

# Laminar–turbulent transition: mechanisms and prediction

<div class="page-meta" markdown>
**Chapter:** 4 Turbulence · **Depth:** [deep]
</div>

## What it is

How a laminar boundary layer becomes turbulent at hypersonic speed, and the tools used to predict where it happens: correlations, linear stability theory with the $e^N$ method, parabolized stability equations (PSE), transport-equation transition models inside RANS, and DNS of the transition process.

## The problem it solves

Turbulent heating is several times laminar heating ([model selection](../model-selection.md)), so where transition happens on a heatshield or backshell can decide the TPS material and thickness. No RANS model predicts transition by itself ([hypersonic page](../physics/turbulence-modeling.md#transition)); it has to be prescribed or modelled separately. Transition inside separated interactions also sets the reattachment heating ([SWBLI](../physics/shock-boundary-layer-interaction.md#laminar-transitional-and-turbulent-interactions)).

## How it works

*(Outline. Planned sections, with what each will establish.)*

### Receptivity and the paths to turbulence

- Receptivity (how free-stream disturbances, roughness and noise enter the boundary layer), linear growth of instability waves, nonlinear breakdown; bypass paths when disturbances are large.
- Noisy vs quiet wind tunnels, and why ground-test transition locations don't carry over to flight.

### Instability mechanisms at hypersonic speed

- **First mode** (viscous, oblique; the compressible form of Tollmien–Schlichting waves) and **second (Mack) mode** (acoustic waves trapped between the wall and the relative-sonic line; frequency scales with $U_e/\delta$; dominant above roughly Mach 4) (Mack 1984; Fedorov 2011).
- Wall cooling: stabilizes the first mode, destabilizes the second. Real-gas effects on second-mode growth.
- **Crossflow** on yawed or 3D bodies and capsules at angle of attack; attachment-line instability; entropy-layer instabilities on blunt bodies.
- **Roughness-induced transition**, the dominant path on capsule heatshields (ablated or tiled surfaces, protrusions): roughness Reynolds number correlations (Reda 2002; Schneider 2008).

### Correlations

- Momentum-thickness Reynolds number thresholds, $Re_\theta/M_e$ criteria, roughness correlations; their scatter and the data they came from.

### Linear stability theory and the e^N method

- Normal-mode analysis of the compressible boundary-layer profile (the compressible counterpart of the Orr–Sommerfeld problem), spatial growth rates, the N factor $N = \int \sigma\,dx$ and the calibrated $N$ at transition (quiet vs noisy environments).
- Worked example to build: N-factor envelope on a cone from a computed mean flow.

### Parabolized stability equations

- Non-parallel and nonlinear effects by marching the disturbance equations; PSE with chemistry for high enthalpy (Johnson & Candler 2005); tools (STABL, LASTRAC), calibrated.

### Transition models inside RANS

- Prescribed transition (switching production on), intermittency.
- Transport-equation models: $\gamma$–$Re_{\theta t}$ (Langtry & Menter 2009) and its hypersonic extensions; amplification-factor transport (Coder & Maughmer 2014) that imports $e^N$ ideas into RANS.

### DNS of transition

- Forced disturbances on cones and elliptic cones; what DNS adds (breakdown mechanisms, heating overshoot during transition) ([scale-resolving methods](scale-resolving.md#direct-numerical-simulation)).

## Variants

### Correlation-based prediction

See above.

### e^N with linear stability or PSE

See above.

### Transport-equation transition models

See above.

### Transition DNS

See above.

## Typical values

To be sourced: second-mode frequencies and N factors from flight and quiet-tunnel experiments (Fedorov 2011; Schneider 2004); roughness Reynolds numbers at transition on capsule heatshields (Reda 2002); transitional heating overshoot relative to turbulent levels.

## Trade-offs

To be written: correlation (instant, narrow validity) vs $e^N$/PSE (physics-based, needs a calibrated $N$ and a separate tool) vs transport models (inside the CFD run, calibration-dependent) vs DNS (mechanism-resolving, research cost).

## Effects on stability and robustness

To be written: mean-flow accuracy needed for stability analysis (grid and dissipation affect growth rates); robustness of transport transition models.

## Implications

| Lens | Effect |
|---|---|
| Time step and cost | Correlations free; stability analysis a post-process; transport models add one or two equations; DNS very expensive. |
| Steady vs unsteady | Stability analysis works on a steady mean flow; transition itself is unsteady. |
| Accuracy (heat flux, pressure) | Transition location is often the largest single uncertainty in turbulent heating. |
| Robustness | — |
| Physics captured or lost | Correlations and RANS models carry no mechanism; $e^N$ needs the dominant mechanism identified. |
| Hardware / parallel fit | Stability tools are small serial post-processes; DNS is the GPU-scale case. |

## In a run

Planned: laminar and fully turbulent runs as a bracket; prescribing transition onset; extracting a mean flow good enough for stability analysis (wall-normal resolution, low dissipation in the boundary layer).

## Which codes

To be filled: stability tools (STABL, LASTRAC) and which CFD codes they post-process; transport transition models in SU2, FUN3D and commercial codes.

!!! warning "Calibration"
    Tool and code capabilities to be confirmed from their documentation.

## See also

[Turbulence fundamentals](fundamentals.md) · [RANS models](rans-models.md) · [Scale-resolving methods](scale-resolving.md) · [Hypersonic boundary layers](../physics/turbulence-modeling.md) · [Entry flow anatomy](../physics/entry-flow-anatomy.md) · [Shock/boundary-layer interaction](../physics/shock-boundary-layer-interaction.md)

## References

Mack (1984); Fedorov (2011); Schneider (2004, 2008); Reda (2002); Langtry & Menter (2009); Coder & Maughmer (2014); Johnson & Candler (2005); Chang (2004), LASTRAC manual. See the [bibliography](../../references.md).
