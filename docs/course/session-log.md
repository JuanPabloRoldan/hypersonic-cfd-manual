# Session log

One entry per session: date, topic, what clicked, what's still shaky.

## 2026-11-07: Lesson 0.1, governing equations

**Covered:** the reacting two-temperature system; conservative vs primitive variables; weak solutions, Rankine–Hugoniot and the Lax–Wendroff theorem; hyperbolic, parabolic and elliptic character; the two explicit time-step limits; closing the system. Follow-ups: the finite-volume pipeline step by step; characteristic vs primitive reconstruction; dense gases; electronic levels and the potential well; why dissociation raises shock-layer density and shrinks standoff; Stefan–Maxwell diffusion; the two axes of gas models; the thermal-nonequilibrium hierarchy; stiff chemistry treatments; local time stepping (steady and time-accurate); line and point relaxation; the explicit-vs-implicit cost model; PNS.

**Corrections made during the session:** a handful of thin wall cells set the *global* time step only in time-accurate runs (steady runs use local time stepping, whose real limitation is aspect-ratio stiffness); naive local time stepping, not all local time stepping, breaks time accuracy; at an isolated contact, primitive reconstruction is already fine, and characteristic reconstruction pays off where waves overlap.

**Checkpoint:**

| Q | Topic | Outcome |
|---|---|---|
| 1 | Conservation with primitive reconstruction | Solid (minor: reconstruction serves the flux, closures are applied in decode; say "wrong jump conditions") |
| 2 | Which explicit limit binds at the wall | Half right: parameter is the cell Reynolds number, not Damköhler; viscous limit binds when $Re_\Delta \lesssim 2$ |
| 3 | Why 5 → 16 equations hurts implicit more | Solid |
| 4 | Why marching works on a cone but not a nose | Half right: missing that the stagnation region is subsonic, hence elliptic (upstream influence) |
| 5 | Burgers: why forms disagree, which is right | Half right: chain-rule failure at discontinuities; the entropy condition is a separate job |

**Still shaky:** questions 2, 4 and 5; rework before moving to Lesson 0.2.
