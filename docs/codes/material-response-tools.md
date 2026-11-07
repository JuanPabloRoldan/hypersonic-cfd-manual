---
status: outline
---

# Material response tools: FIAT, CHAR, Icarus, PATO, PuMA

| Tool | Approach | What it buys |
|---|---|---|
| **FIAT** (NASA Ames) | 1D implicit ablation and thermal response; quasi-steady pyrolysis gas; surface energy balance with B′ tables | The design workhorse; fast enough for Monte Carlo sizing |
| **CHAR** (NASA JSC) | Multi-dimensional finite-element material response | Multi-D conduction and recession (shoulders, gaps) |
| **Icarus** | Material response in the Ares framework | Coupling with US3D and NERO |
| **PATO** (NASA Ames, open, OpenFOAM-based) | Volume-averaged porous medium: Darcy flow of pyrolysis gases, Mutation++ chemistry | Pyrolysis-gas flow and in-depth chemistry, loose coupling with DPLR or SU2-NEMO |
| **PuMA** (NASA Ames, open) | Microstructure from X-ray tomography to effective properties | Multiscale link from fibres to continuum models |

Details in [Track 7](../course/track-7.md); pipeline role in [Track 9](../course/track-9.md); the boundary condition that couples them to CFD is the [surface energy balance](../reference/walls/surface-energy-balance.md).

!!! warning "Calibration"
    Outline only; to be filled from primary sources.

## References

Lachaud & Mansour (2014) on PATO. See the [bibliography](../references.md).
