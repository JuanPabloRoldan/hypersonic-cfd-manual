---
status: outline
---

# Lesson 0.8: Verification and diagnosis

<div class="page-meta" markdown>
**Slot:** verification and diagnosis · **Depth:** [deep] · **Reference pages:** [convergence diagnostics](../../reference/time/convergence-diagnostics.md)
</div>

## Planned content

1. Order of accuracy and the method of manufactured solutions.
2. Grid convergence and Richardson extrapolation; why heat flux converges more slowly than pressure.
3. Conservation checks.
4. Residual vs functional convergence; limit cycles; "converged" solutions that are still wrong.
5. Signs a run is lying: carbuncle, standoff out of the expected range, heat flux that depends on the flux scheme.

## Checkpoint (planned themes)

Given residual and heat-flux histories, decide whether a run is converged and whether to trust it.

## Track 0 exit test

Given a DPLR or US3D methods paragraph and an MFC input file, place every choice in its slot and explain, through the implications lens, why each code chose differently.
