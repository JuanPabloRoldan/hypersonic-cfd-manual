---
status: draft
---

# Engineering checks on a solution

<div class="page-meta" markdown>
**Chapter:** 12 Verification and diagnosis · **Depth:** [deep]
</div>

## What it is

A short list of closed-form or correlation-based numbers that any entry-flow CFD solution can be compared with in minutes: free-stream and post-shock states, stagnation pressure, forebody pressure distribution, shock standoff, stagnation heating, and the frozen and equilibrium limits behind the shock.

## The problem it solves

Residuals going down only says that the discrete equations are being solved ([convergence diagnostics](../time/convergence-diagnostics.md)). It says nothing about whether the setup, gas model, grid or flux are right. These checks catch the common gross errors (wrong free-stream units, wrong gas model, unresolved boundary layer, misaligned shock) before anyone looks at detailed results.

## How it works

Each check compares one CFD quantity with an independent estimate; the expected agreement is part of the check.

| Check | CFD quantity | Independent estimate | Expect | If it fails, suspect |
|---|---|---|---|---|
| Post-shock state on the stagnation line | $p$, $\rho$, $T$ just behind the shock | Normal-shock relations: perfect gas, frozen, or equilibrium ([shock relations](../physics/hypersonic-shock-relations.md#equilibrium-and-nonequilibrium-normal-shocks)) | Between frozen and equilibrium | free-stream setup, gas model, shock smeared over too many cells |
| Stagnation pressure | wall $p$ at the stagnation point | $p_\infty + C_{p,\max}\tfrac12\rho_\infty V_\infty^2$ | within a few percent | free stream, shock capturing |
| Forebody pressure | $C_p$ along the heat shield | modified Newtonian | within a few percent away from the shoulder | geometry, angle of attack, setup |
| Shock standoff | standoff on the axis | density-ratio correlation ([standoff](../physics/entry-flow-anatomy.md#post-shock-density-and-standoff)) | perfect gas > nonequilibrium > equilibrium | gas model, grid at the shock |
| Stagnation heat flux | wall $q$ at the stagnation point | Fay–Riddell or Sutton–Graves, same wall assumption ([stagnation heating](../physics/stagnation-point-heating.md)) | roughly 10–20% | wall-normal resolution, flux dissipation in the BL, shock alignment, catalysis setting |
| Relaxation behind the shock | $T$, $T_v$, composition on the stagnation line | frozen state at the shock, equilibrium state downstream | $T$ jumps at the shock, then falls as $T_v$ rises to meet it and the gas dissociates | thermal-nonequilibrium coupling, rates |
| Conservation | mass flux in vs out; total enthalpy on inviscid streamlines | exact | to round-off or truncation | boundary conditions, non-conservative terms |

## Variants

Checks against **published solutions** (code-to-code comparisons, validation cases such as the double cone) belong to validation rather than this page (a validation chapter is planned).

## Typical values

- Fay–Riddell and Sutton–Graves agreement with laminar, fully catalytic CFD: typically 10–20% (see the calibration note on [stagnation heating](../physics/stagnation-point-heating.md#typical-values)).
- Modified Newtonian forebody pressure: a few percent on blunt forebodies.

## Trade-offs

- Gain: catches gross errors cheaply; builds intuition for what a solution should look like.
- Pay: only checks the simple parts of the flow (forebody, stagnation line). Wake, interactions and transition need validation data.

## Effects on stability and robustness

None directly; a failed check often explains a later robustness problem (a badly resolved shock that later carbuncles, a free stream in the wrong units).

## Implications

| Lens | Effect |
|---|---|
| Time step and cost | Minutes per solution. |
| Steady vs unsteady | Steady forebody quantities. |
| Accuracy (heat flux, pressure) | The first line of defence for both. |
| Robustness | Indirect. |
| Physics captured or lost | Forebody and stagnation line only. |
| Hardware / parallel fit | n/a |

## In a run

Run the checks at the first converged solution of every new configuration and after every change of gas model, wall condition or grid family.

## Which codes

Independent of the code.

## See also

[Convergence diagnostics](../time/convergence-diagnostics.md) · [Hypersonic shock relations and Newtonian theory](../physics/hypersonic-shock-relations.md) · [Stagnation-point heating](../physics/stagnation-point-heating.md) · [Engineering methods](../special/engineering-methods.md)

## References

Anderson, *Hypersonic and High-Temperature Gas Dynamics*; Fay & Riddell (1958); Sutton & Graves (1971).
