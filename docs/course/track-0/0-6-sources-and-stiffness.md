---
status: outline
---

# Lesson 0.6: Source terms and stiffness

<div class="page-meta" markdown>
**Slot:** source terms · **Depth:** [deep] · **Reference pages:** [stiff source terms](../../reference/sources/stiff-sources.md), [finite-rate chemistry](../../reference/thermo/finite-rate-chemistry.md)
</div>

## Planned content

1. What stiffness is: eigenvalues of the source Jacobian, time-scale separation, Damköhler numbers.
2. Why explicit treatment of chemistry fails behind a strong shock.
3. Point-implicit sources; operator splitting (Lie, Strang) with stiff ODE integrators; IMEX; reduction methods.
4. The steady-state splitting error, and why reentry codes prefer point-implicit treatment.
5. Startup strategies: frozen chemistry first.

## Already previewed

Cell-by-cell (not reaction-by-reaction) treatment, splitting with sub-stepping, IMEX and reduction methods were introduced in Lesson 0.1's follow-ups.

## Checkpoint (planned themes)

Estimate a Damköhler number behind a bow shock; explain why a split scheme's steady state can depend on $\Delta t$.
