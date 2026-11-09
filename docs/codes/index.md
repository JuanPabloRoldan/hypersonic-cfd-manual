# A. Codes at a glance

This appendix answers one question: which choice does each code make in each solver slot? The explanations live in the theory chapters; every method page ends with a **Which codes** section saying who uses it. This page just puts the production reentry codes side by side and points to their primary sources.

!!! warning "Calibration"
    DPLR, LAURA, US3D and FIAT are not open source; entries are only as good as the cited manuals and papers. Defaults and options change between versions.

## The production codes, slot by slot

| Code | Grid and discretization | Inviscid flux | Time advancement | Thermochemistry and coupling |
|---|---|---|---|---|
| <a id="dplr"></a>**DPLR** (NASA Ames) | Structured multiblock finite volume; grids tailored to the shock | [Modified Steger–Warming](../reference/spatial/flux-vector-splitting.md#modified-steger-warming) | Implicit [data-parallel line relaxation](../reference/time/relaxation-methods.md#line-relaxation) | 2T finite-rate; catalytic walls; loosely coupled to NEQAIR and FIAT, blowing BC for PATO |
| <a id="laura"></a>**LAURA** (NASA Langley) | Structured multiblock finite volume; shock alignment | [Roe](../reference/spatial/riemann-solvers.md#roe) with Yee-type TVD limiting and entropy fix | [Point-implicit relaxation](../reference/time/relaxation-methods.md#point-relaxation) | 2T finite-rate; coupled radiation (HARA) and ablating walls; shares gas-physics modules with FUN3D |
| <a id="us3d"></a>**US3D** (Univ. of Minnesota / VirtusAero) | Unstructured cell-centred finite volume | Modified Steger–Warming; [KEC central flux with Ducros-switched dissipation](../reference/spatial/central-schemes.md#kinetic-energy-consistent-fluxes) for low-dissipation work | Implicit line and full-matrix point relaxation; BDF2 with subiterations | 2T finite-rate; gas–surface interaction; flow solver of the Ares framework |
| <a id="fun3d"></a>**FUN3D** (NASA Langley) | Unstructured vertex-based finite volume | Upwind options | Implicit point/line relaxation; BDF2 with subiterations | Reacting path (HEFSS); adjoint-based adaptation |
| <a id="su2-nemo"></a>**SU2-NEMO** (open) | Unstructured vertex-based finite volume | Roe, AUSM family and others | Implicit | 2T, built-in or via Mutation++; adjoint |
| <a id="eilmer"></a>**Eilmer** (Univ. of Queensland, open) | Structured multiblock (unstructured supported) | Several, incl. AUSMDV and HLLC | Explicit or Newton–Krylov | Multi-temperature; shock fitting; conjugate heat transfer |
| <a id="sparta"></a>**SPARTA** (Sandia, open) | DSMC particles on hierarchical Cartesian grid with cut cells | (particles) | (particles) | Collision-based chemistry; Kokkos GPU |
| <a id="star-ccm"></a>**STAR-CCM+** (commercial) | Unstructured finite volume | Roe, AUSM+ | Coupled implicit, with preconditioning and AMG | 2T in recent versions |

## Supporting tools {#supporting-tools}

<a id="radiation-solvers"></a>**Radiation**: NEQAIR (NASA Ames; line-by-line, post-processed on CFD solutions, usually along lines of sight), HARA (NASA Langley; band model, coupled inside LAURA), NERO (radiation in the Ares framework). To be expanded in [Track 6](../course/track-6.md).

<a id="material-response-tools"></a>**Material response**: FIAT (1D implicit ablation and thermal response with B′ tables; the design workhorse), CHAR (multi-D finite element), Icarus (Ares framework), PATO (open, OpenFOAM-based porous-medium model with Darcy flow and Mutation++), PuMA (microstructure to effective properties). To be expanded in [Track 7](../course/track-7.md).

<a id="mutationpp"></a>**Mutation++**: open VKI library for thermodynamics, transport (including Stefan–Maxwell diffusion), kinetics and gas–surface interaction, shared by SU2-NEMO, PATO and others; see [closing the system](../reference/foundations/closing-the-system.md).

## Contrast codes {#contrast-codes}

Two explicit, high-order research codes appear on method pages as alternatives, because they make nearly the opposite choice in every slot: <a id="mfc"></a>**MFC** (explicit SSP-RK, WENO with HLLC or [IGR shock regularization](../reference/spatial/central-schemes.md#shock-regularization-igr), GPU-first, multiphase) and <a id="alpaca"></a>**ALPACA / JAX-Fluids** (TU Munich; explicit, WENO/TENO, HLLC-LM, multiresolution AMR). Their input decks are useful for practising placing knobs in slots; the reasons both families are right for their own problems are on the [explicit vs implicit](../reference/time/explicit-vs-implicit.md) page.

## Primary sources

- DPLR: Wright, Candler & Bose (1998), the algorithm; Wright, White & Mangini (2009), *DPLR Code User Manual, Acadia v4.01.1*, NASA/TM-2009-215388 (free on NTRS).
- LAURA: Gnoffo (1990), NASA TP-2953, the algorithm; Thompson et al. (2020), *LAURA Users Manual 5.6*, NASA/TM-2020-220566 (NTRS).
- US3D: Nompelis, Drayna & Candler (2004), origins; Subbareddy & Candler (2009), low-dissipation fluxes; Candler, Subbareddy & Nompelis (2013), decoupled implicit method; Candler et al. (2015), code overview.

Full citations in the [bibliography](../references.md#codes).
