---
status: outline
---

# Lesson 0.4: Flux functions

<div class="page-meta" markdown>
**Slot:** inviscid flux function · **Depth:** [deep] · **Reference pages:** [Riemann solvers](../../reference/spatial/riemann-solvers.md), [flux-vector splitting](../../reference/spatial/flux-vector-splitting.md), [central schemes](../../reference/spatial/central-schemes.md), [shock instabilities](../../reference/spatial/shock-instabilities.md)
</div>

## Planned content

1. The Riemann problem and its wave structure; the exact (Godunov) solver.
2. Every approximate flux as "central minus dissipation": Roe (and entropy fixes), HLL/HLLE, HLLC, Rusanov.
3. Flux-vector splitting: Steger–Warming, van Leer, modified Steger–Warming (DPLR, US3D), AUSM family.
4. Central schemes with artificial dissipation (JST); a first look at kinetic-energy-consistent fluxes.
5. The central trade-off: the dissipation that smears boundary layers is the dissipation that suppresses the carbuncle.
6. Flux Jacobians for implicit codes: why splitting fluxes are convenient.
7. MFC contrast: HLLC with WENO; IGR as a replacement for the whole reconstruction-plus-Riemann slot.

## Checkpoint (planned themes)

Which solver would you expect to give the best heat flux on a fixed grid, and which the most robust shock; why DPLR chose modified Steger–Warming; what the entropy fix does to stagnation heating.
