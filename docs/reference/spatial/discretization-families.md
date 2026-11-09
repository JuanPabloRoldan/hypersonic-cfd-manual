---
status: draft
---

# Discretization families

<div class="page-meta" markdown>
**Slot:** Track 0.2 spatial discretization · **Depth:** [deep]
</div>

## What it is

The ways of turning the continuous PDE into a finite set of unknowns: finite differences, finite volumes, finite elements and discontinuous Galerkin, and particle methods (DSMC); on structured multiblock or unstructured grids; cell-centred or vertex-based.

## The problem it solves

Each family makes different trade-offs between conservation, geometric flexibility, order of accuracy and cost. The choice constrains everything downstream: how reconstruction works, which relaxation directions exist, and how heat flux behaves near walls.

## How it works

*(Outline, to be written.)*

## Variants

### Finite difference
### Finite volume, cell-centred
### Finite volume, vertex-based (dual mesh)
### Finite element and discontinuous Galerkin
### Structured multiblock vs unstructured grids {#structured-vs-unstructured}

For decades aeroheating codes (DPLR, LAURA) used structured multiblock grids, and the reasons are numerical rather than historical. Three things favour ordered hexahedral cells near the vehicle:

- **Heat flux needs a clean wall-normal stencil.** Second-order reconstruction and viscous gradients are most accurate when the cell pair across a face lines up with the face normal. Extruded hexahedra or prisms give that; stretched tetrahedra do not, and their gradients degrade.
- **Line relaxation needs lines.** [DPLR](../time/relaxation-methods.md#dplr) solves exactly along wall-normal lines; those exist naturally in an $(i,j,k)$ grid and in extruded layers, but not in a tetrahedral mesh.
- **Shocks need alignment** (next section).

The cost is grid generation. For complex geometry a structured grid can take longer to build than the solution takes to run, and may force poor cells or wasted points. The modern answer, introduced by Nompelis, Drayna & Candler (2004) and carried into US3D, is a **hybrid unstructured** grid built to look structured where it matters:

1. pave the surface with quadrilaterals and/or triangles;
2. extrude the surface mesh normal to the wall, giving layers of hexahedra or prisms through the boundary layer, which also provide solution lines;
3. fill the remaining volume with tetrahedra where geometry demands it, keeping hexahedra around the bow shock;
4. solve along the extruded lines with line relaxation and use point relaxation elsewhere.

US3D treats even a pure multiblock hexahedral grid as unstructured: it partitions blocks like any other cells, so there is no limit on the number of blocks. That makes it practical to use **three- and five-point singularities** in the grid topology (points where three or five blocks meet instead of four) and many small embedded-refinement blocks, which Candler, Subbareddy & Nompelis (2015) found relieve many of the compromises of conventional multiblock design.

Implementation follows from this: an unstructured cell-centred solver loops over **faces** to compute fluxes and scatter them to the two adjacent cells, then over **cells** to update. A pre-processor supplies the face-to-cell connectivity (with a consistent normal direction), the extra neighbours needed for second-order reconstruction, and the line structure for the implicit solver.

```text
for each face f with left cell L and right cell R:
    F = flux(face states of L and R, normal of f)
    dU[L] -= F * area(f);  dU[R] += F * area(f)
for each cell c:
    U[c] += dt / vol(c) * dU[c]
```

### Element types at strong shocks {#element-types-at-strong-shocks}

Tetrahedra at a strong shock are the single largest source of avoidable error in hypersonic unstructured simulations.

**Mechanism.** When a strong shock crosses a tetrahedron obliquely, the momentum fluxes through its faces don't balance the way they do on a cell aligned with the shock. The imbalance produces spurious vorticity and entropy at the shock, even with a first-order flux (Candler, Subbareddy & Nompelis 2015). Once created, that vorticity convects downstream and cannot be removed by any added dissipation. It ends up in the subsonic stagnation region and the entropy layer, which is exactly where the wall heat flux is set. Rotated flux evaluation has reduced the error on some grids but is not a general fix.

**Evidence.** Nompelis et al. (2004) computed a perfect-gas cylinder at 5 km/s ($\rho_\infty = 10^{-3}$ kg/m³, $T_\infty = 200$ K) on four grids:

| Grid | Near wall | Near the bow shock | Result |
|---|---|---|---|
| S | hexahedra | hexahedra | smooth shock and entropy layer; line relaxation converged to machine zero in about 800 iterations |
| H1 | hexahedra | hexahedra (shock region), tetrahedra elsewhere | indistinguishable from S |
| H2 | hexahedra | tetrahedra clustered at the shock | rougher shock, errors in the entropy layer |
| H3 | hexahedra | isotropic tetrahedra | visible errors in temperature, pressure and entropy; poor heat flux; residual never reached machine zero |

Their conclusion: even with a high-quality surface grid, tetrahedra near the bow shock spoil the heat-flux prediction, and an approximately shock-aligned region of hexahedra fixes it. Good grid design remains essential on unstructured grids.

### Shock alignment ("tailoring") {#shock-alignment}

Even on hexahedral grids, a strong shock that crosses the grid obliquely generates spurious post-shock vorticity and entropy. DPLR, LAURA and US3D therefore all provide grid-adaptation utilities that move the outer grid to follow the bow shock. The procedure in US3D (Candler et al. 2015):

1. converge on an initial grid whose lines run from the wall to the free-stream boundary;
2. detect the bow shock along each line;
3. rescale the points on each line so the shock sits a fixed number of cells from the wall (and the outer boundary just outside it);
4. reconverge; repeat once more if needed.

A more general approach under development in 2015 deforms the grid gradually until it is shock-aligned.

### Particle methods (DSMC)

*(Outline.)*

## Typical values and trade-offs

- **Hexahedra vs tetrahedra at the shock:** hexahedra (shock-aligned) give a smooth entropy layer and correct heat flux; tetrahedra generate vorticity that no dissipation removes.
- **Hybrid line/point convergence:** about 2× slower than pure line relaxation on a fully hexahedral grid, much faster than pure point relaxation (Nompelis et al. 2004).
- **Gridding time vs solve time:** structured grids for complex shapes can take longer to build than the run; hybrid grids cut that, at a modest convergence cost.
- **Shock tailoring:** typically one or two rounds of align-and-reconverge.

## Implications

| Lens | Effect |
|---|---|
| Time step and cost | Unstructured face loops cost more memory traffic per cell than structured sweeps; hybrid grids converge about 2× slower than pure line relaxation. |
| Steady vs unsteady | Shock tailoring is a steady-state tool; moving shocks need adaptation or deformation. |
| Accuracy (heat flux, pressure) | Element type and alignment at the bow shock control entropy-layer error and so stagnation heat flux; wall-normal extruded layers control the heat-flux gradient. |
| Robustness | A shock sitting in tetrahedra keeps the residual oscillating; aligned hexahedra converge to machine zero. |
| Physics captured or lost | Spurious vorticity from tetrahedra contaminates the entropy layer and any downstream boundary layer. |
| Hardware / parallel fit | Unstructured connectivity partitions freely (thousands of blocks); line-aware partitioning keeps implicit lines on one processor. |

## In a run

- Look at the shock in the converged solution: if it zigzags across cells or the entropy contours ripple downstream, check element type and alignment there before blaming the flux function.
- On unstructured grids, check that the extruded layers reach beyond the boundary layer and that implicit lines actually formed.
- Run shock tailoring once the shock position has settled, then reconverge.

## Which codes

Structured cell-centred FV: DPLR, LAURA, Eilmer, MFC. Unstructured cell-centred FV: US3D. Vertex-based FV: FUN3D, SU2. DSMC: SPARTA. See [codes](../../codes/index.md).

## See also

[The finite-volume pipeline](finite-volume-pipeline.md) · [Point and line relaxation](../time/relaxation-methods.md) · [Reconstruction](reconstruction.md#multidimensional-and-unstructured-reconstruction) · [Shock instabilities](shock-instabilities.md)

## References

Hirsch; Blazek; Bird; Nompelis, Drayna & Candler (2004); Candler, Subbareddy & Nompelis (2015, chapter); Candler et al. (2015, US3D). See the [bibliography](../../references.md).
