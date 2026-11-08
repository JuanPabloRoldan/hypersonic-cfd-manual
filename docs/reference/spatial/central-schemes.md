---
status: draft
---

# Central schemes and dissipation

<div class="page-meta" markdown>
**Slot:** Track 0.4 flux functions; Track 2.5–2.6 · **Depth:** [deep] · **Taught in:** [Lesson 0.4](../../course/track-0/0-4-flux-functions.md), [Track 2](../../course/track-2.md) (pending)
</div>

## What it is

Central schemes compute the face flux from a symmetric average of the two sides and add dissipation explicitly, rather than getting it implicitly from upwinding. Any upwind flux can be written this way ("central minus dissipation", see [Riemann solvers](riemann-solvers.md#how-it-works)); central schemes make the split explicit so the dissipation can be switched off where it isn't needed.

## The problem it solves

Upwind fluxes dissipate everywhere, including in smooth regions where they damp turbulence, instability waves and acoustics. For LES and DNS of transition, SWBLI unsteadiness or turbulent heating, that numerical dissipation can swamp the physics (Subbareddy & Candler showed fully upwind fluxes visibly over-damp decaying turbulence). Central schemes can be nearly dissipation-free in smooth flow and add dissipation only at shocks.

## How it works

The flux at face $f$ is

$$
\hat{\mathbf F}_f = \mathbf F_{f,\text{sym}} + \alpha_{\text{diss}}\,\mathbf D_f ,
$$

a symmetric (non-dissipative) part, plus a dissipative part $\mathbf D_f$ (typically borrowed from an upwind scheme) multiplied by a **shock sensor** $0 \le \alpha_{\text{diss}} \le 1$ that is near zero in smooth or vortical regions and near one at shocks. Design choices: how the symmetric part is built (plain average, skew-symmetric, kinetic-energy consistent), where the dissipation comes from, and the sensor.

A naive central average is unstable for compressible turbulence even without shocks, because it produces kinetic energy spuriously through aliasing. That is what kinetic-energy-consistent and skew-symmetric forms fix.

## Variants

### JST

Jameson–Schmidt–Turkel (1981): a central flux plus a blend of second-difference dissipation, switched on near shocks by a normalized pressure second-difference sensor, and a small fourth-difference background dissipation that damps odd–even modes. The classic aerospace central scheme, typically paired with explicit Runge–Kutta, local time stepping and multigrid.

### Kinetic-energy-consistent fluxes

Subbareddy & Candler (2009), the basis of US3D's low-dissipation capability. The aim: the discrete convective fluxes should not create or destroy kinetic energy $\rho k = \tfrac12\rho|\mathbf u|^2$, which is transferred only through pressure work and viscous dissipation.

Deriving the kinetic-energy balance from the discrete mass and momentum fluxes shows this holds if the momentum flux is the mass flux times the **face-averaged velocity**:

$$
\mathbf F_f = (\rho u')_f \begin{bmatrix} 1 \\ \bar u \\ \bar v \\ \bar w \end{bmatrix}_f,\qquad \bar a_f = \tfrac12(a_i + a_{nbr}),
$$

with any symmetric choice of the face mass flux $(\rho u')_f$, and with the kinetic-energy flux in the total-energy equation chosen consistently (it involves $\tfrac12(u_iu_{nbr} + v_iv_{nbr} + w_iw_{nbr})$ times the mass flux). This is the compressible analog of the kinetic-energy-conserving fluxes used in incompressible LES codes, and similar to skew-symmetric forms. They also show the time discretization matters: a "fully discrete" form is needed to keep the property through the time step.

**Shock capturing** adds the dissipative part of the [modified Steger–Warming](flux-vector-splitting.md#modified-steger-warming) flux, $\mathbf D_f = -\tfrac12(\mathbf R|\boldsymbol\Lambda|\mathbf R^{-1})_f(\mathbf U_R - \mathbf U_L)$, with MUSCL face states, multiplied by the Ducros sensor (below), taking the larger of the two cell values at the face.

**Time integration** is implicit: BDF2 with subiterations solved by full-matrix point relaxation, with CFL up to $10^5$ for steady runs. A subtlety: if the implicit Jacobians include full dissipation while the residual uses switched dissipation, unconverged subiterations leave a small extra dissipation that accumulates over many steps; converging the subiterations removes it.

**Validation** in the paper includes the 25°–55° double cone at Mach 11.3 (Holden's CUBRC case), where the separation size is sensitive to numerical dissipation; with the low-dissipation fluxes (TVD-MUSCL with minmod plus the Ducros switch) the computed heat transfer matched experiment and reference simulations, once vibrational relaxation and chemistry were included in the forebody.

### Shock sensors

**Ducros:**

$$
\alpha_{\text{diss}} = \min\!\left(\frac{(\nabla\cdot\mathbf u)^2}{(\nabla\cdot\mathbf u)^2 + |\nabla\times\mathbf u|^2 + \epsilon},\ 1\right).
$$

Near one where dilatation dominates (shocks), near zero where vorticity dominates (turbulence), so shear layers and boundary-layer turbulence are left undamped. Undefined in 1D (no vorticity), where pressure- or density-gradient sensors are used instead. Other sensors use pressure or density second differences (as in JST) or the Mach-number jump across a face. No sensor is perfect: compressions and expansions in turbulence also trigger it, and a strong vortex near a shock can switch it off.

### Shock regularization (IGR)

A different route, used in MFC: rather than capturing shocks with limiters and Riemann solvers, modify the equations with an "entropic pressure" obtained from an elliptic solve each step, so shocks are spread over a controlled width and simple central fluxes can be used. It is still explicit and CFL-limited. See [MFC](../../codes/mfc.md#information-geometric-regularization-igr).

## Implications

| Lens | Effect |
|---|---|
| Time step and cost | Cheap fluxes; the sensor adds a gradient evaluation. Implicit treatment needs care with switched dissipation in the Jacobians. |
| Steady vs unsteady | Designed for unsteady LES/DNS; works for steady runs with the dissipation switched fully on or by sensor. |
| Accuracy | Minimal dissipation in smooth and vortical regions; quality at shocks depends on the sensor and the borrowed dissipation. |
| Robustness | Without dissipation, central schemes rely on kinetic-energy consistency for stability; sensor misfires at strong shocks are the main risk. |
| Physics captured or lost | Keeps turbulence, instability waves and separation-bubble dynamics (double-cone separation size is dissipation-sensitive). |
| Hardware / parallel fit | Compact and local; GPU-friendly. |

## In a run

Knobs: dissipation on/off/sensor, sensor type and threshold, reconstruction used in the dissipation term. Symptoms: oscillations near shocks (sensor too weak), over-damped turbulence or wrong separation size (sensor too strong or dissipation always on).

## Which codes

US3D (KEC plus Ducros-switched modified Steger–Warming dissipation); many aerospace codes (JST); MFC (IGR).

## See also

[Riemann solvers](riemann-solvers.md) · [Flux-vector splitting](flux-vector-splitting.md) · [Shock instabilities](shock-instabilities.md) · [US3D](../../codes/us3d.md)

## References

Jameson, Schmidt & Turkel (1981); Ducros et al. (1999); Subbareddy & Candler (2009); Pirozzoli (2011). See the [bibliography](../../references.md).
