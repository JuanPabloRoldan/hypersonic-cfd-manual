# Glossary

Key terms in a fixed format: what each is, the problem it solves, its implications and how it shows up in a run.

---

### Cell Reynolds number (also: wall cell Reynolds number, $Re_\Delta$)


- **Depth:** [deep] · **Topic:** time advancement; heat-flux accuracy
- **What it is:** $Re_\Delta = (|u| + a)\,\Delta x/\nu$, the ratio of convective to diffusive transport across one cell. At the wall it is usually written $\rho a\Delta n/\mu$.
- **Problem it solves:** tells you which explicit time-step limit binds (viscous when $Re_\Delta \lesssim 2$) and whether a wall grid resolves the thermal boundary layer (order 1 or below for heat flux).
- **Implications:** wall-resolved heating grids have $Re_\Delta \lesssim 1$, so explicit schemes are viscous-limited there and steady aeroheating goes implicit.
- **In a run:** heat flux that changes with wall spacing means $Re_\Delta$ is too large.
- **Which codes:** a grid-design guideline used across DPLR, LAURA, US3D practice.
- **See also:** [time-step limits](reference/time/time-step-limits.md), [viscous fluxes](reference/spatial/viscous-fluxes.md#near-the-wall), Damköhler number (the chemistry analog of a time-scale ratio, not this).

### Characteristic variables

- **Depth:** [deep] · **Topic:** reconstruction
- **What it is:** projections of the state jump onto the eigenvectors of the flux Jacobian, $\mathbf w = \mathbf L\,\Delta\mathbf U$: one amplitude per wave family.
- **Problem it solves:** lets a limiter treat each wave family by its own smoothness, avoiding oscillations where waves overlap (mainly at shocks).
- **Implications:** cleaner high-order shock capturing; costs an eigendecomposition per face; approximate because eigenvectors are frozen at the face.
- **In a run:** a "characteristic reconstruction" option in high-order codes.
- **Which codes:** common in WENO codes (an option in MFC); rare in second-order production codes.
- **See also:** [reconstruction](reference/spatial/reconstruction.md#which-variables-to-reconstruct), [WENO](reference/spatial/weno.md).

### Closure (also: closing the system)

- **Depth:** [deep] · **Topic:** governing equations
- **What it is:** the models that express quantities needed by the fluxes and sources but absent from $\mathbf U$ ($p$, $T$, $T_v$, transport coefficients, rates) as functions of $\mathbf U$ and its gradients: EOS, caloric relations, transport, kinetics.
- **Problem it solves:** without it the conservation laws can't be evaluated.
- **Implications:** carries almost all the physical uncertainty of an aeroheating prediction; costs scale with species and reactions; temperature inversion is a common crash site.
- **In a run:** gas model, species set, transport and diffusion model choices.
- **Which codes:** all; packaged as a library in Mutation++.
- **See also:** [closing the system](reference/foundations/closing-the-system.md), [gas models](reference/thermo/gas-models.md).

### Conservation form

- **Depth:** [deep] · **Topic:** governing equations
- **What it is:** writing the equations, and the numerical update, as divergences of fluxes of conserved quantities: $U_i^{n+1} = U_i^n - \tfrac{\Delta t}{\Delta x}(\hat F_{i+1/2} - \hat F_{i-1/2})$.
- **Problem it solves:** guarantees correct shock jump conditions (via the Lax–Wendroff theorem) and exact discrete conservation.
- **Implications:** decisive for shock position, standoff and post-shock state; reconstruction may still use primitive or characteristic variables.
- **In a run:** built in to production codes; global conservation checks catch violations.
- **Which codes:** all finite-volume reentry codes; multiphase codes like MFC also carry a nonconservative volume-fraction equation.
- **See also:** [conservation form and weak solutions](reference/foundations/conservation-and-weak-solutions.md).

### Controlling temperature (also: Park's $T_c$)

- **Depth:** [deep] · **Topic:** closures (kinetics)
- **What it is:** $T_c = T^a T_v^{1-a}$ ($a \approx 0.5$–0.7), the temperature at which dissociation rates are evaluated in a two-temperature model.
- **Problem it solves:** a simple model of vibration–dissociation coupling: vibrationally cold gas dissociates more slowly.
- **Implications:** empirical; one of the known weak points of the 2T model at high speed.
- **In a run:** the exponent $a$ is sometimes an input.
- **Which codes:** standard in 2T codes (DPLR, LAURA, US3D, SU2-NEMO).
- **See also:** [finite-rate chemistry](reference/thermo/finite-rate-chemistry.md#parks-controlling-temperature).

### Damköhler number

- **Depth:** [deep] · **Topic:** sources and stiffness
- **What it is:** $Da = \tau_{\text{flow}}/\tau_{\text{chem}}$.
- **Problem it solves:** classifies chemistry as frozen ($Da \ll 1$), nonequilibrium ($Da \sim 1$) or equilibrium ($Da \gg 1$).
- **Implications:** an entry flow contains all three regimes at once, which is what makes its chemistry stiff.
- **In a run:** decides whether an equilibrium or frozen model would be adequate in a region.
- **Which codes:** a concept, not an option.
- **See also:** [stiff source terms](reference/sources/stiff-sources.md), [gas models](reference/thermo/gas-models.md).

### Debye length (also: Debye shielding, quasi-neutrality)

- **Depth:** [feel] · **Topic:** ionization and electrons
- **What it is:** the distance over which a plasma screens a charge imbalance, $\lambda_D \approx 69\sqrt{T_e/n_e}$ m; about a micrometre in an entry shock layer.
- **Problem it solves:** justifies quasi-neutrality ($n_e = \sum n_{\text{ions}}$) in CFD, and makes the electron–ion Coulomb cross-section finite.
- **Implications:** no need to resolve charge separation; sheath physics at walls and probes is lost.
- **In a run:** invisible; electrons get no separate species equation.
- **Which codes:** all ionizing-flow CFD codes.
- **See also:** [ionization, electrons and plasma](reference/thermo/ionization-and-electrons.md#charge-neutrality-and-the-debye-length).

### Direct simulation Monte Carlo (also: DSMC)

- **Depth:** [feel] · **Topic:** rarefied flow; discretization families (particles)
- **What it is:** Bird's particle method for the Boltzmann equation: simulator particles move ballistically, then collide in cells with probabilities set by a collision model (VHS/VSS, Larsen–Borgnakke for internal energy).
- **Problem it solves:** transitional and rarefied flow ($Kn \gtrsim 0.1$), where Navier–Stokes is invalid.
- **Implications:** cells smaller than the mean free path and time steps smaller than the collision time, so cost grows steeply with density; outputs are statistically noisy, heat flux most.
- **In a run:** check cell size vs $\lambda$, time step vs collision time, particles per cell.
- **Which codes:** SPARTA (Kokkos GPU), DAC, MONACO.
- **See also:** [DSMC](reference/rarefied/dsmc.md), [continuum breakdown](reference/rarefied/continuum-breakdown.md).

### Entropy condition


- **Depth:** [deep] · **Topic:** governing equations; flux functions
- **What it is:** the extra condition (entropy must not decrease across a shock; characteristics run into it) that selects the physical weak solution.
- **Problem it solves:** weak solutions are not unique; without it, unphysical expansion shocks are admissible.
- **Implications:** separate from choosing the conservation form; numerically, why Roe's solver needs an entropy fix.
- **In a run:** the entropy-fix coefficient in Roe-type schemes; it affects stagnation heating.
- **Which codes:** LAURA (Roe with entropy fix) and any Roe-based code.
- **See also:** [conservation form and weak solutions](reference/foundations/conservation-and-weak-solutions.md#nonuniqueness-and-the-entropy-condition), [which schemes enforce it](reference/foundations/conservation-and-weak-solutions.md#which-schemes-enforce-the-entropy-condition), [entropy fix](#entropy-fix-also-harten-fix-eigenvalue-limiting).

### Entropy fix (also: Harten fix, eigenvalue limiting)

- **Depth:** [deep] · **Topic:** flux functions
- **What it is:** a floor on the dissipation coefficient of an upwind flux where an eigenvalue goes to zero, e.g. Harten's $|\lambda| \to (\lambda^2 + \delta^2)/2\delta$ for $|\lambda| < \delta$.
- **Problem it solves:** Roe's solver damps each wave by $|\tilde\lambda|$, so at a transonic rarefaction it keeps an unphysical expansion shock; the fix restores the fan. Also used against the carbuncle.
- **Implications:** adds dissipation wherever active, including boundary layers, so it is usually reduced near walls. HLL-family, Rusanov and exact solvers don't need it.
- **In a run:** the entropy-fix or eigenvalue-limiter coefficient; heat flux can depend on it.
- **Which codes:** Roe-based codes (LAURA); eigenvalue limiting in modified Steger–Warming (DPLR, US3D).
- **See also:** [entropy fixes: why Roe needs one](reference/spatial/riemann-solvers.md#entropy-fixes-why-roe-needs-one), [modified Steger–Warming](reference/spatial/flux-vector-splitting.md#modified-steger-warming).

### Flux Jacobian

- **Depth:** [deep] · **Topic:** governing equations; flux functions
- **What it is:** $\mathbf A = \partial\mathbf F/\partial\mathbf U$. Its eigenvalues are wave speeds; its eigenvectors are what each wave carries.
- **Problem it solves:** characterizes the hyperbolic system; used by Roe (linearization), HLL (wave-speed bounds), characteristic BCs and CFL.
- **Implications:** an analysis tool, not a solution method. Not to be confused with the residual Jacobian.
- **In a run:** invisible; underlies flux and BC choices.
- **Which codes:** all.
- **See also:** [implicit methods](reference/time/implicit-methods.md#two-different-jacobians), [mathematical character](reference/foundations/mathematical-character.md#hyperbolic).

### Frozen sound speed

- **Depth:** [deep] · **Topic:** governing equations
- **What it is:** the sound speed with chemistry and lagging internal modes held fixed: $a_f^2 = \gamma_f p/\rho$, $\gamma_f = 1 + R_{mix}/c_{v,tr}$ in a 2T model.
- **Problem it solves:** the correct wave speed on acoustic time scales, which the eigenvalues and flux functions use.
- **Implications:** higher than the equilibrium sound speed, because compression energy can only go into translation and rotation; the flux Jacobian never contains source terms, so a finite-rate code's eigenvalues always use it.
- **In a run:** inside every flux function of a reacting code.
- **Which codes:** all reacting codes.
- **See also:** [frozen and equilibrium sound speed](reference/foundations/mathematical-character.md#frozen-and-equilibrium-sound-speed).

### Knudsen number (also: $Kn$, gradient-length Knudsen number)

- **Depth:** [feel] · **Topic:** rarefied flow
- **What it is:** $Kn = \lambda/L$, mean free path over a flow length scale; the local version $Kn_{GL} = (\lambda/Q)|\nabla Q|$ uses the gradient length of a flow quantity.
- **Problem it solves:** says when the continuum (Navier–Stokes) model is valid: continuum below about $10^{-3}$, slip to about $10^{-1}$, transitional to about 10, free-molecular above; locally, continuum fails where $Kn_{GL} \gtrsim 0.05$ (Boyd, Chen & Candler 1995).
- **Implications:** decides between no-slip CFD, slip walls, and DSMC.
- **In a run:** post-process $Kn_{GL}$ from high-altitude solutions.
- **Which codes:** a criterion, not an option.
- **See also:** [continuum breakdown](reference/rarefied/continuum-breakdown.md).

### Lax–Wendroff theorem

- **Depth:** [deep] · **Topic:** governing equations
- **What it is:** if a consistent scheme in conservation form converges (boundedly, almost everywhere), its limit is a weak solution.
- **Problem it solves:** justifies conservative shock capturing: correct jump conditions without tracking shocks.
- **Implications:** doesn't guarantee convergence or the entropy solution; nonconservative schemes have no such guarantee.
- **In a run:** why production codes update conserved variables with flux differences.
- **Which codes:** all finite-volume codes rely on it.
- **See also:** [conservation form](reference/foundations/conservation-and-weak-solutions.md#the-lax-wendroff-theorem).

### Limiter (also: slope limiter)

- **Depth:** [deep] · **Topic:** reconstruction
- **What it is:** a nonlinear function of neighbouring differences that sets the slope in each cell so reconstruction creates no new extrema (minmod, van Leer, MC, superbee).
- **Problem it solves:** second order in smooth flow without oscillations at shocks (required by Godunov's theorem).
- **Implications:** clips smooth peaks (stagnation point) and can chatter, stalling steady convergence.
- **In a run:** limiter type; sometimes a limiter-freeze iteration.
- **Which codes:** all MUSCL-type codes.
- **See also:** [reconstruction](reference/spatial/reconstruction.md#limiters).

### Local time stepping

- **Depth:** [deep] · **Topic:** time advancement
- **What it is:** each cell advances with its own time step. Steady: each cell's own stability limit, time accuracy abandoned. Unsteady: special schemes (AMR subcycling, multirate) that resynchronize.
- **Problem it solves:** stops the smallest cell from setting everyone's step.
- **Implications:** standard for steady runs but doesn't cure aspect-ratio stiffness; naive LTS breaks time accuracy.
- **In a run:** "local time stepping" switch, CFL.
- **Which codes:** essentially all steady solvers; subcycling in AMR codes.
- **See also:** [local time stepping](reference/time/local-time-stepping.md).

### Modified Newtonian theory (also: Lees' modified Newtonian, Newtonian flow)

- **Depth:** [feel] · **Topic:** inviscid hypersonic theory; engineering checks
- **What it is:** $C_p = C_{p,\max}\sin^2\theta$ on surfaces facing the flow, with $C_{p,\max}$ the stagnation value behind a normal shock (1.839 for $\gamma = 1.4$ at high Mach); Newton's original has 2 in place of $C_{p,\max}$.
- **Problem it solves:** closed-form forebody pressure on blunt bodies, within a few percent.
- **Implications:** poor at shoulders and on shadowed surfaces; exact for free-molecular flow with diffuse cold walls (factor 2).
- **In a run:** check CFD forebody $C_p$ and stagnation pressure against it.
- **Which codes:** engineering aerodynamic tools.
- **See also:** [hypersonic shock relations and Newtonian theory](reference/physics/hypersonic-shock-relations.md), [engineering checks](reference/verification/engineering-checks.md).

### Numerical flux function

- **Depth:** [deep] · **Topic:** flux functions
- **What it is:** a function $\hat{\mathbf F}(\mathbf U_L, \mathbf U_R)$ giving the face flux from the two reconstructed states. Riemann solvers, flux-vector splitting and central schemes are all families of it.
- **Problem it solves:** turns two disagreeing face states into one conservative flux with the right upwinding.
- **Implications:** sets numerical dissipation, hence boundary-layer and heat-flux accuracy, positivity and carbuncle behaviour.
- **In a run:** flux scheme option.
- **Which codes:** DPLR/US3D modified Steger–Warming; LAURA Roe; MFC HLLC.
- **See also:** [Riemann solvers](reference/spatial/riemann-solvers.md), [flux-vector splitting](reference/spatial/flux-vector-splitting.md).

### Parabolized Navier–Stokes (also: PNS, space marching)

- **Depth:** [feel] · **Topic:** governing-equation reductions
- **What it is:** steady Navier–Stokes with streamwise viscous derivatives dropped, marched in the flow direction plane by plane.
- **Problem it solves:** cheap steady solutions for slender bodies in supersonic flow.
- **Implications:** needs supersonic flow (Vigneron splitting in the subsonic sublayer); fails in subsonic and separated regions.
- **In a run:** starting plane, marching step, Vigneron safety factor; departure solutions when the march is ill-posed.
- **Which codes:** dedicated PNS codes.
- **See also:** [space marching](reference/special/space-marching.md).

### Plasma frequency (also: communications blackout, critical electron density)

- **Depth:** [feel] · **Topic:** ionization and electrons
- **What it is:** $f_p \approx 8.98\sqrt{n_e}$ Hz; radio waves below it are reflected by the plasma.
- **Problem it solves:** predicts blackout: S-band (2.3 GHz) is cut off above about $7\times10^{16}$ m⁻³.
- **Implications:** blackout prediction needs electron densities near the antenna, often on the afterbody.
- **In a run:** post-process $n_e$; validate against RAM-C II.
- **Which codes:** any code with ionized species.
- **See also:** [communications blackout](reference/thermo/ionization-and-electrons.md#communications-blackout).

### Primitive variables

- **Depth:** [deep] · **Topic:** governing equations; reconstruction
- **What it is:** $(\rho_s, \mathbf u, p, T, T_v)$: the variables the physics, fluxes and boundary conditions are written in.
- **Problem it solves:** easier positivity control and clean contacts when reconstructed.
- **Implications:** a derived view recomputed every evaluation; never the stored state, never the update.
- **In a run:** the "reconstruction variables" choice.
- **Which codes:** common choice in reentry codes and in MFC.
- **See also:** [the finite-volume pipeline](reference/spatial/finite-volume-pipeline.md#1-decode).

### Rankine–Hugoniot conditions


- **Depth:** [deep] · **Topic:** governing equations
- **What it is:** $s\,[U] = [F(U)]$: the jump conditions across a discontinuity moving at speed $s$, from the integral form.
- **Problem it solves:** fixes shock speed and post-shock state.
- **Implications:** depend on which quantities are in $U$; the reason conservation form matters.
- **In a run:** standoff and post-shock state are their consequences.
- **Which codes:** physics, not an option.
- **See also:** [conservation form](reference/foundations/conservation-and-weak-solutions.md#rankine-hugoniot-conditions).

### Reconstruction (also: MUSCL extrapolation)

- **Depth:** [deep] · **Topic:** reconstruction
- **What it is:** building a polynomial in each cell from its neighbours and evaluating it at faces to get $\mathbf W_L$, $\mathbf W_R$.
- **Problem it solves:** higher than first-order accuracy for the face fluxes.
- **Implications:** sets order, dissipation and positivity; needs limiting or WENO weights at shocks.
- **In a run:** spatial order, limiter, variable set.
- **Which codes:** MUSCL in production codes; WENO in MFC.
- **See also:** [reconstruction](reference/spatial/reconstruction.md), [WENO](reference/spatial/weno.md).

### Residual Jacobian

- **Depth:** [deep] · **Topic:** time advancement
- **What it is:** $\partial\mathbf R/\partial\mathbf U$: the sparse block matrix in the implicit update $(V/\Delta t\,\mathbf I + \partial\mathbf R/\partial\mathbf U)\Delta\mathbf U = -\mathbf R$.
- **Problem it solves:** lets implicit methods take steps far beyond explicit limits; Newton's method as $\Delta t\to\infty$.
- **Implications:** $n\times n$ blocks: memory $\propto n^2$, factorization $\propto n^3$; often approximated (first order) without affecting the converged answer.
- **In a run:** Jacobian order, relaxation sweeps, CFL ramp.
- **Which codes:** DPLR, LAURA, US3D, FUN3D, SU2.
- **See also:** [implicit methods](reference/time/implicit-methods.md).

### Star region (also: star states, $\mathbf U_{*L}$, $\mathbf U_{*R}$)

- **Depth:** [deep] · **Topic:** flux functions
- **What it is:** in a Riemann problem, the region between the left and right acoustic waves. Pressure and normal velocity are uniform there ($p_*$, $u_*$); density, temperature, species and tangential velocity can jump at the contact, giving two states $\mathbf U_{*L}$ and $\mathbf U_{*R}$.
- **Problem it solves:** the vocabulary in which exact and HLLC solvers are written.
- **Implications:** HLL replaces both star states (and any fans) by one average; HLLC keeps two.
- **In a run:** invisible.
- **Which codes:** all Godunov-type codes.
- **See also:** [the Riemann problem at a face](reference/spatial/riemann-solvers.md#the-riemann-problem-at-a-face).

### Two-temperature model (also: Park 2T)

- **Depth:** [deep] · **Topic:** closures; thermal nonequilibrium
- **What it is:** $T$ for translation–rotation, $T_v$ for vibration–electronic–electron energy, with a separate vibrational energy equation and Landau–Teller relaxation.
- **Problem it solves:** captures post-shock temperature overshoot and vibrational lag.
- **Implications:** one extra equation and inversion; standard for design; weak spots at very high speed and for nonequilibrium radiation.
- **In a run:** number of temperatures; relaxation correlations.
- **Which codes:** DPLR, LAURA, US3D, SU2-NEMO, Eilmer.
- **See also:** [thermal nonequilibrium](reference/thermo/thermal-nonequilibrium.md).

### Weak solution


- **Depth:** [deep] · **Topic:** governing equations
- **What it is:** a function satisfying the integral form of a conservation law against every smooth test function; allowed to be discontinuous.
- **Problem it solves:** gives shocks a precise mathematical meaning.
- **Implications:** not unique without an entropy condition; conservative schemes converge to weak solutions (Lax–Wendroff).
- **In a run:** every shock in a CFD solution is an approximation to one.
- **Which codes:** all shock-capturing codes.
- **See also:** [conservation form and weak solutions](reference/foundations/conservation-and-weak-solutions.md#the-weak-form).
