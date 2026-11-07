---
status: outline
---

# Radiation solvers: NEQAIR, HARA, NERO

| Tool | Approach | Coupling | Trade-off |
|---|---|---|---|
| **NEQAIR** (NASA Ames) | Line-by-line spectral calculation, with nonequilibrium excited-state populations | Post-processed on CFD solutions (typically DPLR), usually along lines of sight (tangent slab) | Most detailed spectra; expensive; loosely coupled |
| **HARA** (NASA Langley) | Band (smeared-rotational) model | Coupled inside LAURA | Cheaper; allows coupled radiation–flowfield solutions |
| **NERO** | Radiation module of the Ares framework | Configurable coupling with US3D | Framework flexibility |

Details in [Track 6](../course/track-6.md).

!!! warning "Calibration"
    Outline only; to be filled from primary sources.

## References

See the [bibliography](../references.md).
