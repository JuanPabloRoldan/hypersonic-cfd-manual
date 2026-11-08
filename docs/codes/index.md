# Codes

What makes DPLR "DPLR"? Each page answers that in the same format: purpose, distinctive features, the code's choice in every [Track 0 slot](../course/track-0/index.md), the implications of those choices, and what's cool about it, including when a code's signature feature is really a basic solver idea in disguise.

!!! warning "Calibration"
    Several production codes (DPLR, LAURA, US3D, FIAT) are not open, so these pages can only be as good as their published descriptions. Claims are drawn from the codes' papers and manuals as summarized in the course plan; each page will be checked against primary sources (NTRS papers, AIAA/JCP papers, user manuals) as it's taught. Defaults and options change between versions.

## Track 0 choices side by side

| Code | Discretization | Inviscid flux | Time advancement | Thermochemistry |
|---|---|---|---|---|
| [DPLR](dplr.md) | Structured multiblock FV, shock-tailored grids | Modified Steger–Warming | Implicit data-parallel line relaxation | 2T, finite-rate, catalytic walls |
| [LAURA](laura.md) | Structured FV, shock alignment | Roe + Yee TVD | Point-implicit relaxation | 2T, finite-rate; coupled radiation (HARA) and ablating walls |
| [US3D](us3d.md) | Unstructured cell-centred FV | Modified Steger–Warming; KEC + shock-switched dissipation | Implicit (DPLR heritage) | 2T, finite-rate, gas–surface interaction |
| [FUN3D](fun3d.md) | Unstructured vertex-based FV | Upwind (several options) | Implicit point/line relaxation | Reacting (HEFSS) |
| [SU2-NEMO](su2-nemo.md) | Unstructured vertex-based FV | Roe, AUSM family, others | Implicit | 2T via built-in models or Mutation++ |
| [Eilmer](eilmer.md) | Structured multiblock FV | Several (incl. AUSMDV, HLLC) | Explicit or Newton–Krylov | Multi-temperature, finite-rate |
| [SPARTA](sparta.md) | DSMC, hierarchical Cartesian grid with cut cells | (particles) | (particles) | Collision-based chemistry |
| [MFC](mfc.md) | Structured FV/FD, multiphase | HLLC (+ HLL, exact); or IGR | Explicit SSP-RK, GPU | Stiffened-gas multiphase (not a reentry code) |
| [ALPACA](alpaca.md) | Cartesian FV/FD with multiresolution AMR | HLLC, HLLC-LM, HLL, Rusanov; Roe/LF flux splitting | Explicit SSP-RK | Ideal gas and multiphase (not a reentry code) |
| [STAR-CCM+](star-ccm.md) | Unstructured FV (commercial) | Roe, AUSM+ | Coupled implicit density-based | 2T in recent versions |

## Supporting tools

[Radiation solvers](radiation-tools.md) (NEQAIR, HARA, NERO) · [Material response tools](material-response-tools.md) (FIAT, CHAR, Icarus, PATO, PuMA) · [Mutation++](mutationpp.md)
