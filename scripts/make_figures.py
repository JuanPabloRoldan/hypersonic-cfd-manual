"""Generate every figure used by the manual.

Run from the repository root:

    python scripts/make_figures.py

Writes SVG files into docs/assets/figures/. Each function is self-contained so a
figure can be regenerated or edited without touching the others. Values marked
"illustrative" are order-of-magnitude choices for teaching, not design data.
"""

import os
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

OUT = Path(__file__).resolve().parents[1] / "docs" / "assets" / "figures"
OUT.mkdir(parents=True, exist_ok=True)

plt.rcParams.update(
    {
        "font.size": 10,
        "axes.spines.top": False,
        "axes.spines.right": False,
        "axes.grid": True,
        "grid.alpha": 0.25,
        "figure.dpi": 110,
        "savefig.bbox": "tight",
        "svg.fonttype": "path",
    }
)
C0, C1, C2, C3, GREY = "#3949ab", "#e65100", "#2e7d32", "#8e24aa", "#757575"


def save(fig, name):
    fig.savefig(OUT / f"{name}.svg")
    preview = os.environ.get("FIG_PREVIEW_DIR")  # optional PNG copies for quick inspection
    if preview:
        Path(preview).mkdir(parents=True, exist_ok=True)
        fig.savefig(Path(preview) / f"{name}.png")
    plt.close(fig)
    print("wrote", name)


# ---------------------------------------------------------------------------
# 1. Burgers: conservative vs nonconservative upwind, and the two "conservative"
#    forms that are equivalent for smooth flow but not at a shock.
# ---------------------------------------------------------------------------
def burgers_demo():
    uL, uR, t_end = 1.0, 0.2, 1.0
    s_true = 0.5 * (uL + uR)  # from (u^2/2)_x
    s_alt = (2.0 / 3.0) * (uL**2 + uL * uR + uR**2) / (uL + uR)  # from (u^3/3)_x

    def run(N, conservative):
        x = np.linspace(-1, 2, N, endpoint=False) + 1.5 / N
        dx = 3.0 / N
        u = np.where(x < 0, uL, uR)
        dt = 0.4 * dx / uL
        t = 0.0
        while t < t_end - 1e-12:
            h = min(dt, t_end - t)
            lam = h / dx
            um = np.concatenate(([uL], u[:-1]))  # upwind neighbour (u > 0 everywhere)
            if conservative:
                u = u - lam * (0.5 * u**2 - 0.5 * um**2)
            else:
                u = u - lam * u * (u - um)
            t += h
        return x, u

    def shock_pos(x, u):
        mid = 0.5 * (uL + uR)
        i = np.argmax(u < mid)
        return x[i]

    fig, axes = plt.subplots(1, 2, figsize=(10, 3.6))
    ax = axes[0]
    xe = np.linspace(-1, 2, 2000)
    ax.plot(xe, np.where(xe < s_true * t_end, uL, uR), color="k", lw=1.2, label=f"exact weak solution (s = {s_true:.2f})")
    for N, ls in [(150, "--"), (1200, "-")]:
        x, u = run(N, True)
        ax.plot(x, u, ls, color=C0, lw=1.4, label=f"conservative upwind, N={N}")
        x, u = run(N, False)
        ax.plot(x, u, ls, color=C1, lw=1.4, label=f"nonconservative upwind, N={N}")
    ax.axvline(s_alt * t_end, color=C3, lw=1, ls=":", label=f"shock from $(u^3/3)_x$ form (s = {s_alt:.2f})")
    ax.set(xlabel="x", ylabel="u at t = 1", xlim=(-0.2, 1.2), title="Burgers shock, $u_L=1$, $u_R=0.2$")
    ax.legend(fontsize=7.5, loc="lower left")

    ax = axes[1]
    Ns = np.array([100, 200, 400, 800, 1600, 3200])
    for cons, col, lab in [(True, C0, "conservative"), (False, C1, "nonconservative")]:
        err = [abs(shock_pos(*run(N, cons)) - s_true * t_end) for N in Ns]
        ax.loglog(Ns, err, "o-", color=col, label=lab)
    ax.set(xlabel="number of cells N", ylabel="|shock position error|", title="Refinement does not fix the wrong form")
    ax.legend(fontsize=8)
    save(fig, "burgers_conservative_vs_nonconservative")


# ---------------------------------------------------------------------------
# 2. Explicit time-step limits vs cell size (illustrative shock-layer values)
# ---------------------------------------------------------------------------
def timestep_limits():
    c = 1000.0  # |u| + a near the wall, m/s (illustrative)
    nu = 3e-3  # kinematic viscosity, m^2/s (illustrative, low-density shock layer)
    dy = np.logspace(-7, -2, 200)
    dt_conv = dy / c
    dt_visc = dy**2 / (2 * nu)
    dt_comb = 1.0 / (1.0 / dt_conv + 1.0 / dt_visc)
    fig, ax = plt.subplots(figsize=(6.4, 4))
    ax.loglog(dy, dt_conv, color=C0, label=r"convective: $\Delta y/(|u|+a)$")
    ax.loglog(dy, dt_visc, color=C1, label=r"viscous: $\Delta y^2/(2\nu)$")
    ax.loglog(dy, dt_comb, color="k", lw=2, alpha=0.6, label="combined explicit limit")
    dyc = 2 * nu / c
    ax.axvline(dyc, color=GREY, ls=":")
    ax.text(dyc * 1.15, 1e-4, r"$Re_\Delta = 2$" + "\n(curves cross)", fontsize=8, color=GREY)
    ax.axvspan(5e-7, 2e-6, color=C1, alpha=0.08)
    ax.text(5.5e-7, 3e-13, "wall-resolved\nheating cells", fontsize=8, color=C1)
    ax.axvspan(3e-4, 3e-3, color=C0, alpha=0.08)
    ax.text(3.3e-4, 3e-13, "shock-layer\ncore cells", fontsize=8, color=C0)
    ax.set(xlabel=r"cell size $\Delta y$ (m)", ylabel=r"max stable $\Delta t$ (s)", ylim=(1e-13, 1e-3),
           title="Explicit limits: the viscous limit binds once $Re_\\Delta \\lesssim 2$\n(illustrative: $|u|+a$ = 1000 m/s, $\\nu$ = 3e-3 m²/s)")
    ax.legend(fontsize=8, loc="upper left")
    save(fig, "timestep_limits")


# ---------------------------------------------------------------------------
# 3. MUSCL reconstruction with minmod: smooth data vs a local extremum
# ---------------------------------------------------------------------------
def minmod(a, b):
    return np.where(a * b > 0, np.sign(a) * np.minimum(abs(a), abs(b)), 0.0)


def minmod_reconstruction():
    cases = [("Monotone data: limited slopes", np.array([0.5, 1.0, 2.0, 4.0, 5.0])),
             ("Local extremum: slope clipped to zero", np.array([0.5, 1.0, 3.0, 2.0, 1.5]))]
    fig, axes = plt.subplots(1, 2, figsize=(10, 3.4), sharey=True)
    for ax, (title, q) in zip(axes, cases):
        n = len(q)
        for i in range(n):
            ax.fill_between([i - 0.5, i + 0.5], 0, q[i], color=C0, alpha=0.12, step=None)
            ax.plot([i - 0.5, i + 0.5], [q[i], q[i]], color=C0, lw=1, alpha=0.6)
        for i in range(1, n - 1):
            s = float(minmod(q[i] - q[i - 1], q[i + 1] - q[i]))
            xs = np.array([i - 0.5, i + 0.5])
            ax.plot(xs, q[i] + s * (xs - i), color=C1, lw=2)
            ax.plot([i + 0.5], [q[i] + 0.5 * s], "o", color=C1, ms=5)
            ax.plot([i - 0.5], [q[i] - 0.5 * s], "o", mfc="white", color=C1, ms=5)
            sc = 0.5 * (q[i + 1] - q[i - 1])
            ax.plot(xs, q[i] + sc * (xs - i), color=GREY, lw=1, ls="--")
        ax.set(title=title, xlabel="cell index i", xticks=range(n))
    axes[0].set_ylabel("q")
    axes[0].plot([], [], color=C0, alpha=0.6, label="cell average")
    axes[0].plot([], [], color=C1, lw=2, label="minmod-limited slope")
    axes[0].plot([], [], color=GREY, ls="--", label="unlimited central slope")
    axes[0].plot([], [], "o", color=C1, label="face values ($q^L$ ●, $q^R$ ○)", mfc="white")
    axes[0].legend(fontsize=7.5, loc="upper left")
    save(fig, "minmod_reconstruction")


# ---------------------------------------------------------------------------
# 4. Explicit vs implicit: the cost-model crossover
# ---------------------------------------------------------------------------
def cost_crossover():
    r = np.logspace(0, 8, 300)
    fig, ax = plt.subplots(figsize=(6.6, 4))
    for C, col, lab in [(10, C2, "C = 10"), (50, C0, "C = 50"), (300, C1, "C = 300 (implicit on a GPU, say)")]:
        ax.loglog(r, r / C, color=col, label=lab)
    ax.axhline(1, color="k", lw=1)
    ax.text(1.3, 1.25, "break-even", fontsize=8)
    ax.fill_between(r, 1e-3, 1, color=C1, alpha=0.06)
    ax.fill_between(r, 1, 1e8, color=C0, alpha=0.05)
    ax.text(1.5e3, 3e-2, "explicit wins", fontsize=9, color=C1)
    ax.text(2e5, 3e7, "implicit wins", fontsize=9, color=C0)
    for x, lab in [(2, "DNS / shock–droplet\n(acoustics are the physics)"), (1e5, "capsule wake\nunsteadiness")]:
        ax.axvline(x, color=GREY, ls=":")
        ax.text(x * 1.2, 3e-3 if x < 10 else 3e-3, lab, fontsize=7.5, color=GREY)
    ax.annotate("steady heating:\nwanted Δt is unbounded →", xy=(1e8, 3e3), xytext=(3e5, 5e1),
                fontsize=7.5, color=GREY, arrowprops=dict(arrowstyle="->", color=GREY))
    ax.set(xlabel=r"$\Delta t_{wanted} / \Delta t_{allowed}$", ylabel="implicit speed-up over explicit",
           ylim=(1e-3, 1e8), title="Implicit wins when the step you could use exceeds\nthe step you're allowed by more than the overhead C")
    ax.legend(fontsize=8, loc="upper left")
    save(fig, "cost_crossover")


# ---------------------------------------------------------------------------
# 5. Morse potential well for N2 with vibrational levels (illustrative)
# ---------------------------------------------------------------------------
def morse_well():
    hc = 1.986445857e-23  # J per cm^-1
    De_eV = 9.9
    De = De_eV * 1.602176634e-19
    we = 2358.6  # cm^-1
    mu = 14.003074 / 2 * 1.66053907e-27
    re = 1.098  # Angstrom
    omega = 2 * np.pi * 2.99792458e10 * we
    a = omega * np.sqrt(mu / (2 * De)) * 1e-10  # 1/Angstrom
    r = np.linspace(0.8, 4.0, 800)
    V = De_eV * (1 - np.exp(-a * (r - re))) ** 2
    De_cm = De / hc
    wexe = we**2 / (4 * De_cm)
    vmax = int(we / (2 * wexe) - 0.5)
    fig, ax = plt.subplots(figsize=(6.4, 4.2))
    ax.plot(r, V, color="k", lw=1.6)
    for v in range(0, vmax + 1):
        G = we * (v + 0.5) - wexe * (v + 0.5) ** 2
        E = G * hc / 1.602176634e-19
        if E >= De_eV:
            break
        x = 1 - np.sqrt(E / De_eV)
        r1 = re - np.log(1 + np.sqrt(E / De_eV)) / a
        r2 = re - np.log(x) / a
        lw = 1.0 if v % 10 == 0 else 0.4
        ax.plot([r1, r2], [E, E], color=C0, lw=lw, alpha=0.9)
    ax.axhline(De_eV, color=C1, ls="--", lw=1)
    ax.text(3.0, De_eV + 0.2, "dissociation limit (N + N)", color=C1, fontsize=8)
    ax.annotate("", xy=(re, 0), xytext=(re, De_eV), arrowprops=dict(arrowstyle="<->", color=C1))
    ax.text(re + 0.05, De_eV / 2, r"$D_e \approx$ 9.9 eV", color=C1, fontsize=8)
    ax.text(1.55, 1.0, "v = 0, 10, 20, ... (bold)\nlevels crowd together\nnear the top (anharmonic)", fontsize=8, color=C0)
    ax.set(xlabel="internuclear distance r (Å)", ylabel="potential energy (eV)", ylim=(-0.3, 11.5), xlim=(0.8, 4.0),
           title="N$_2$ ground state, Morse approximation (illustrative)")
    save(fig, "morse_well_n2")


# ---------------------------------------------------------------------------
# 6. The Arrhenius switch: exp(-theta/T)
# ---------------------------------------------------------------------------
def arrhenius_switch():
    T = np.logspace(np.log10(300), np.log10(25000), 400)
    fig, ax = plt.subplots(figsize=(6.4, 4))
    for theta, col, lab in [(113200, C0, r"N$_2$ dissociation, $\theta \approx$ 113,200 K"),
                            (59500, C1, r"O$_2$ dissociation, $\theta \approx$ 59,500 K"),
                            (38400, C2, r"N$_2$ + O → NO + N, $\theta \approx$ 38,400 K")]:
        ax.semilogy(T, np.exp(-theta / T), color=col, label=lab)
    ax.axvspan(6000, 15000, color=GREY, alpha=0.1)
    ax.text(6300, 1e-75, "typical\nshock-layer\ntemperatures", fontsize=8, color=GREY)
    ax.set_yticks([10.0**(-k) for k in range(0, 170, 20)])
    ax.axvline(300, color=GREY, ls=":")
    ax.set_xscale("log")
    ax.set(xlabel="temperature T (K)", ylabel=r"$e^{-\theta/T}$", ylim=(1e-170, 2),
           title="Why reactions 'switch on' behind the shock\n(activation temperatures approximate, Park-type rates)")
    ax.legend(fontsize=8, loc="lower right")
    save(fig, "arrhenius_switch")


# ---------------------------------------------------------------------------
# 7. Blunt body: bow shock (Billig correlation), subsonic and supersonic regions
# ---------------------------------------------------------------------------
def blunt_body():
    M, g = 20.0, 1.4
    R = 1.0
    delta = 0.143 * np.exp(3.24 / M**2) * R
    Rc = 1.143 * np.exp(0.54 / (M - 1) ** 1.2) * R
    beta = np.arcsin(1 / M)

    def shock_x(y):  # x measured upstream from sphere centre
        return R + delta - Rc / np.tan(beta) ** 2 * (np.sqrt(1 + (y * np.tan(beta) / Rc) ** 2) - 1)

    # wave angle at which the post-shock flow is exactly sonic
    def m2_after(sig):
        m1n = M * np.sin(sig)
        m2n = np.sqrt((1 + 0.5 * (g - 1) * m1n**2) / (g * m1n**2 - 0.5 * (g - 1)))
        th = np.arctan(2 / np.tan(sig) * (m1n**2 - 1) / (M**2 * (g + np.cos(2 * sig)) + 2))
        return m2n / np.sin(sig - th)

    sig = np.linspace(np.radians(50), np.radians(89.9), 4000)
    sig_sonic = sig[np.argmin(abs(np.array([m2_after(s) for s in sig]) - 1))]
    ys = np.linspace(0, 3, 3000)
    xs = shock_x(ys)
    slope = np.gradient(xs, ys)  # dx/dy (x upstream)
    local = np.arctan2(1, -slope)  # angle of shock relative to freestream direction
    j = np.argmin(abs(local - sig_sonic))
    ysh, xsh = ys[j], xs[j]
    phi_b = np.radians(42)  # body sonic point, approximate for a sphere
    xb, yb = R * np.cos(phi_b), R * np.sin(phi_b)

    fig, ax = plt.subplots(figsize=(7.0, 6.0))
    th = np.linspace(-np.pi / 2, np.pi / 2, 300)
    ysp = np.linspace(0, 1.6, 600)
    for sgn in (1, -1):
        ax.plot(-shock_x(ysp), sgn * ysp, color=C1, lw=2)
    ax.fill(np.concatenate([-R * np.cos(th), [0, 0]]), np.concatenate([R * np.sin(th), [R, -R]]), color="#cfd8dc")
    ax.plot(-R * np.cos(th), R * np.sin(th), color="k", lw=1.5)
    # subsonic pocket: shock (-ysh..ysh) -> sonic line -> body (yb..-yb) -> sonic line
    tt = np.linspace(0, 1, 30)
    y_sh = np.linspace(-ysh, ysh, 80)
    y_bd = np.linspace(yb, -yb, 80)
    px = np.concatenate([-shock_x(abs(y_sh)), -(xsh + (xb - xsh) * tt), -np.sqrt(R**2 - y_bd**2), -(xb + (xsh - xb) * tt)])
    py = np.concatenate([y_sh, ysh + (yb - ysh) * tt, y_bd, -(yb + (ysh - yb) * tt)])
    ax.fill(px, py, color=C0, alpha=0.18, lw=0)
    for sgn in (1, -1):
        ax.plot(-(xsh + (xb - xsh) * tt), sgn * (ysh + (yb - ysh) * tt), color=C0, ls="--", lw=1.6)
    ax.annotate("subsonic pocket\n(steady problem: elliptic;\nevery point feels every other)", xy=(-1.04, -0.15),
                xytext=(-1.75, -0.95), fontsize=8.5, color=C0, arrowprops=dict(arrowstyle="->", color=C0))
    ax.annotate("sonic line", xy=(-(xsh + xb) / 2, (ysh + yb) / 2), xytext=(-1.6, 0.95), fontsize=8.5, color=C0,
                arrowprops=dict(arrowstyle="->", color=C0))
    ax.text(-0.40, 1.12, "supersonic shock layer\n(steady problem: hyperbolic\nin the flow direction)", fontsize=8.5)
    ax.annotate("bow shock", xy=(-shock_x(0.3), 0.3), xytext=(-1.75, 0.4), fontsize=8.5, color=C1,
                arrowprops=dict(arrowstyle="->", color=C1))
    ax.annotate("", xy=(-1.25, -1.35), xytext=(-1.8, -1.35), arrowprops=dict(arrowstyle="->"))
    ax.text(-1.8, -1.28, f"M = {M:.0f}", fontsize=9)
    ax.annotate("", xy=(-R, 0.0), xytext=(-R - delta, 0.0), arrowprops=dict(arrowstyle="<->", color="k", lw=0.8))
    ax.text(-R - delta / 2, 0.04, r"$\Delta$", fontsize=9, ha="center")
    ax.set_aspect("equal")
    ax.set(xlim=(-1.85, 0.25), ylim=(-1.5, 1.55), xticks=[], yticks=[],
           title="Blunt body at M = 20: mixed character of the steady problem\n(shock shape: Billig correlation, perfect gas; sonic line schematic)")
    ax.grid(False)
    for s in ax.spines.values():
        s.set_visible(False)
    save(fig, "blunt_body_regions")


# ---------------------------------------------------------------------------
# 8. Harmonic-oscillator vibrational energy
# ---------------------------------------------------------------------------
def vib_energy():
    x = np.linspace(0.02, 4, 400)  # T/theta_v
    ev = 1 / (np.exp(1 / x) - 1)  # e_v / (R theta_v)
    fig, ax = plt.subplots(figsize=(6.0, 3.8))
    ax.plot(x, ev, color=C0, lw=2, label=r"harmonic oscillator: $e_v/(R\theta_v) = 1/(e^{\theta_v/T}-1)$")
    ax.plot(x, x - 0.5, color=GREY, ls="--", label=r"fully excited limit: $T/\theta_v - 1/2$")
    ax.set(xlabel=r"$T_v/\theta_v$", ylabel=r"$e_v/(R\theta_v)$", ylim=(0, 3.6),
           title=r"Vibration is frozen out below $\theta_v$ and switches on above it" + "\n" +
                 r"($\theta_v \approx$ 3390 K for N$_2$, 2270 K for O$_2$)")
    ax.legend(fontsize=8, loc="upper left")
    save(fig, "vibrational_energy")


# ---------------------------------------------------------------------------
# 9. Flux limiters on Sweby's diagram
# ---------------------------------------------------------------------------
def sweby_limiters():
    r = np.linspace(0, 4, 400)
    lim = {
        "minmod": np.minimum(1, r),
        "van Leer": (r + abs(r)) / (1 + abs(r)),
        "van Albada": (r**2 + r) / (r**2 + 1),
        "MC": np.minimum(np.minimum(2 * r, 0.5 * (1 + r)), 2),
        "superbee": np.maximum(np.minimum(2 * r, 1), np.minimum(r, 2)),
        "Koren": np.minimum(np.minimum(2 * r, (1 + 2 * r) / 3), 2),
    }
    fig, ax = plt.subplots(figsize=(6.6, 4.2))
    lo = np.minimum(1, r)
    hi = np.maximum(np.minimum(2 * r, 1), np.minimum(r, 2))
    ax.fill_between(r, lo, hi, color=GREY, alpha=0.15, label="second-order TVD region")
    cols = [C0, C1, C2, C3, "k", "#00838f"]
    styles = ["-", "-", "--", "-.", ":", "--"]
    for (name, phi), c, ls in zip(lim.items(), cols, styles):
        ax.plot(r, phi, color=c, ls=ls, lw=1.6, label=name)
    ax.set(xlabel=r"$r = \Delta^-/\Delta^+$", ylabel=r"$\phi(r)$", xlim=(0, 4), ylim=(0, 2.3),
           title="Slope limiters on Sweby's diagram\n(minmod is the lower edge, superbee the upper edge)")
    ax.legend(fontsize=8, loc="lower right", ncol=2)
    save(fig, "sweby_limiters")


# ---------------------------------------------------------------------------
# 10. DPLR: wall-normal lines on a blunt-body grid and the matrix they produce.
#     Geometry is illustrative; the matrix structure is exact for the ordering shown.
# ---------------------------------------------------------------------------
def dplr_lines():
    fig, (ax, bx) = plt.subplots(1, 2, figsize=(10.5, 4.6), gridspec_kw={"width_ratios": [1.15, 1]})

    # body-fitted grid around a circular forebody, j from wall (0) to shock (1)
    ni, nj = 25, 12
    th = np.linspace(-0.45 * np.pi, 0.45 * np.pi, ni)
    eta = np.linspace(0, 1, nj) ** 2.0  # clustered toward the wall
    R = 1.0
    standoff = 0.22 + 0.45 * (th / (0.5 * np.pi)) ** 2  # shock moves away on the flanks
    X = np.empty((ni, nj)); Y = np.empty((ni, nj))
    for i in range(ni):
        r = R + eta * standoff[i]
        X[i] = -r * np.cos(th[i]); Y[i] = r * np.sin(th[i])
    for j in range(nj):
        ax.plot(X[:, j], Y[:, j], color=GREY, lw=0.45)
    for i in range(ni):
        ax.plot(X[i], Y[i], color=GREY, lw=0.45)
    tb = np.linspace(-0.45 * np.pi, 0.45 * np.pi, 200)
    ax.fill(np.r_[-np.cos(tb), 0.25, 0.25], np.r_[np.sin(tb), np.sin(tb[-1]), np.sin(tb[0])],
            color="#cfd8dc", zorder=3)
    ax.plot(X[:, -1], Y[:, -1], color=C1, lw=2.2, label="bow shock (outer boundary)")
    for k, i in enumerate([4, 12, 20]):
        ax.plot(X[i], Y[i], color=C0, lw=3.0, solid_capstyle="round", zorder=4,
                label="line $i$: all $j$ cells solved together (block-tridiagonal)" if k == 0 else None)
    i, j = 12, 6
    ax.annotate("", xy=(X[i + 1, j], Y[i + 1, j]), xytext=(X[i - 1, j], Y[i - 1, j]),
                arrowprops=dict(arrowstyle="<->", color=C2, lw=1.8), zorder=5)
    ax.annotate("coupling to lines $i\\pm1$:\nlagged one relaxation step,\nrepeated $k_{max}$ times",
                xy=(X[i - 1, j] - 0.02, Y[i - 1, j]), xytext=(-2.35, -0.55), color=C2, fontsize=8.5,
                arrowprops=dict(arrowstyle="->", color=C2, lw=0.9), zorder=6)
    ax.text(-0.93, 0.02, "wall", fontsize=8.5, ha="left", zorder=6)
    for yy in (0.55, 0.2, -0.15):
        ax.annotate("", xy=(-1.55, yy + 0.4), xytext=(-2.3, yy + 0.4),
                    arrowprops=dict(arrowstyle="->", color="k", lw=0.9))
    ax.text(-2.3, 1.08, "freestream", fontsize=8.5)
    ax.set_aspect("equal"); ax.set_xlim(-2.4, 0.3); ax.set_ylim(-1.25, 1.25)
    ax.set_xticks([]); ax.set_yticks([]); ax.grid(False)
    for sp in ax.spines.values():
        sp.set_visible(False)
    ax.legend(fontsize=8, loc="lower left", bbox_to_anchor=(0.0, -0.14), frameon=False)
    ax.set_title("Wall-normal lines (j direction) on a capsule forebody", fontsize=10)

    # matrix: i lines of nj cells, j fastest
    nl, nc = 5, 6
    N = nl * nc
    M = np.zeros((N, N))
    for L in range(nl):
        for c in range(nc):
            r = L * nc + c
            M[r, r] = 3
            if c > 0: M[r, r - 1] = 2
            if c < nc - 1: M[r, r + 1] = 2
            if L > 0: M[r, r - nc] = 1
            if L < nl - 1: M[r, r + nc] = 1
    from matplotlib.colors import ListedColormap
    cmap = ListedColormap(["white", "#a5d6a7", "#7986cb", "#283593"])
    bx.imshow(M, cmap=cmap, vmin=0, vmax=3, interpolation="nearest")
    for L in range(1, nl):
        bx.axhline(L * nc - 0.5, color=GREY, lw=0.5); bx.axvline(L * nc - 0.5, color=GREY, lw=0.5)
    bx.set_xticks([]); bx.set_yticks([]); bx.grid(False)
    bx.set_title("Implicit operator, ordered line by line\n(each square is an $n_e\\times n_e$ block)", fontsize=10)
    from matplotlib.patches import Patch
    bx.legend(handles=[Patch(color="#283593", label=r"diagonal block $\hat A$"),
                       Patch(color="#7986cb", label=r"on-line neighbours $\hat B,\hat C$: kept on the left"),
                       Patch(color="#a5d6a7", label=r"off-line neighbours $\hat D,\hat E$: moved to the right")],
              fontsize=7.8, loc="upper center", bbox_to_anchor=(0.5, -0.02), frameon=False)
    fig.tight_layout()
    save(fig, "dplr_lines")


# ---------------------------------------------------------------------------
# 11. DPLR vs DP-LUR: numbers reported by Wright, Candler & Bose (1998), M=15
#     cylinder-wedge, 128x128 grid, y+=1, 8-processor Cray T3E-900.
# ---------------------------------------------------------------------------
def dplr_vs_dplur():
    names = ["DPLR\n(line)", "DP-LUR\nfull matrix", "DP-LUR\ndiagonal"]
    cols = [C0, C1, GREY]
    iters = [300, 2300, 6200]
    cpu = [35, 235, 359]
    growth = [1, 6, 7]
    fig, axs = plt.subplots(1, 3, figsize=(10.5, 3.4))
    data = [(iters, "Iterations to 10 orders\n(Re = 3e4)", ["< 300", "2300", "6200"]),
            (cpu, "CPU seconds to 10 orders\n(Re = 3e4, 8 PEs)", ["35", "235", "359"]),
            (growth, "CPU growth, Re 3e4 to 3e8\n(max cell aspect ratio 35 to 125,000)", ["x1", "x6", "x7"])]
    for ax, (vals, title, labels) in zip(axs, data):
        bars = ax.bar(names, vals, color=cols, width=0.6)
        for b, lab in zip(bars, labels):
            ax.text(b.get_x() + b.get_width() / 2, b.get_height(), lab, ha="center", va="bottom", fontsize=9)
        ax.set_title(title, fontsize=9.5); ax.tick_params(axis="x", labelsize=8.5)
        ax.set_ylim(0, max(vals) * 1.18); ax.grid(axis="x", visible=False)
    fig.suptitle("DPLR against its point-relaxation predecessors (data from Wright, Candler & Bose 1998)",
                 fontsize=10, y=1.03)
    fig.tight_layout()
    save(fig, "dplr_vs_dplur")


# ---------------------------------------------------------------------------
# 12. Modified Steger-Warming pressure weight w(dp) (Candler et al. 2015 chapter)
# ---------------------------------------------------------------------------
def msw_pressure_weight():
    dp = np.linspace(0, 2.0, 400)
    fig, ax = plt.subplots(figsize=(6.4, 3.8))
    for g, c, ls in [(0.5, C2, "--"), (1.0, C0, "-"), (5.0, C1, "-.")]:
        w = 1 - 0.5 / ((g * dp) ** 2 + 1)
        ax.plot(dp, w, color=c, ls=ls, lw=1.8, label=f"g = {g:g}")
    ax.axhline(0.5, color=GREY, lw=0.8, ls=":"); ax.axhline(1.0, color=GREY, lw=0.8, ls=":")
    ax.text(1.98, 0.52, "w = 1/2: Jacobians from the face average\n(low dissipation, Roe-like)", ha="right", fontsize=8)
    ax.text(1.98, 0.955, "w = 1: Jacobians fully upwind (original Steger-Warming)", ha="right", va="top", fontsize=8)
    ax.set(xlabel=r"$\delta p = |p_{i+1}-p_i| / \min(p_i,p_{i+1})$", ylabel=r"weight $w_{i+1/2}$",
           ylim=(0.45, 1.03), xlim=(0, 2),
           title="Pressure weighting in modified Steger-Warming\n(larger g switches to the dissipative flux at weaker jumps)")
    ax.legend(fontsize=8.5, loc="center right")
    save(fig, "msw_pressure_weight")


# ---------------------------------------------------------------------------
# 13. Eigenvalue limiting: effective dissipation coefficient sqrt(l^2 + eps^2)
# ---------------------------------------------------------------------------
def eigenvalue_limiter():
    lam = np.linspace(-1.0, 1.0, 401)  # eigenvalue / sound speed
    fig, ax = plt.subplots(figsize=(6.4, 3.8))
    ax.plot(lam, np.abs(lam), color="k", lw=1.6, label=r"$|\lambda|$ (no limiting)")
    for e0, c, ls in [(0.1, C0, "-"), (0.3, C1, "--")]:
        ax.plot(lam, np.sqrt(lam ** 2 + e0 ** 2), color=c, ls=ls, lw=1.8,
                label=rf"$\sqrt{{\lambda^2+\varepsilon^2}}$, $\varepsilon_0={e0}$")
    ax.axvspan(-0.08, 0.08, color=GREY, alpha=0.12)
    ax.text(0.0, 0.62, "stagnation point:\n$\\lambda = u'$ goes to zero", ha="center", fontsize=8)
    ax.set(xlabel=r"eigenvalue $\lambda / a$", ylabel=r"dissipation coefficient $(\lambda^+ - \lambda^-)/a$",
           xlim=(-1, 1), ylim=(0, 1.05),
           title="Eigenvalue limiting keeps a floor of dissipation where $u'\\to 0$\n($\\varepsilon = \\varepsilon_0 a$, typically $0.1 \\leq \\varepsilon_0 \\leq 0.3$)")
    ax.legend(fontsize=8.5, loc="lower right")
    save(fig, "eigenvalue_limiter")


# ---------------------------------------------------------------------------
# 14. Unstructured MUSCL: virtual upwind point (Darwish & Moukalled), as used
#     in US3D (Candler et al. 2015 chapter). Geometry is schematic.
# ---------------------------------------------------------------------------
def virtual_upwind_point():
    fig, ax = plt.subplots(figsize=(6.4, 3.6))
    C = np.array([0.0, 0.0]); D = np.array([1.6, 0.45])
    P = 2 * C - D
    tri_C = np.array([[-0.7, -0.75], [0.85, -0.35], [0.25, 0.95]])
    tri_D = np.array([[0.85, -0.35], [2.3, 0.15], [0.25, 0.95]])
    for tri, c in [(tri_C, "#e8eaf6"), (tri_D, "#fff3e0")]:
        ax.fill(tri[:, 0], tri[:, 1], color=c, ec=GREY, lw=1.0)
    f0, f1 = tri_C[1], tri_C[2]
    ax.plot([f0[0], f1[0]], [f0[1], f1[1]], color="k", lw=2.4)
    fm = 0.5 * (f0 + f1)
    ax.text(fm[0] + 0.07, fm[1] + 0.15, "face $f$", fontsize=9)
    ax.plot([P[0], D[0]], [P[1], D[1]], color=GREY, ls="--", lw=1)
    for pt, lab, col in [(C, "C (upwind cell)", C0), (D, "D (downwind cell)", C1), (P, "P (virtual upwind point)", C2)]:
        ax.plot(*pt, "o", color=col, ms=7, zorder=5)
    ax.annotate("C", C, xytext=(-14, -14), textcoords="offset points", color=C0, fontsize=10)
    ax.annotate("D", D, xytext=(6, 6), textcoords="offset points", color=C1, fontsize=10)
    ax.annotate("P", P, xytext=(-14, -14), textcoords="offset points", color=C2, fontsize=10)
    ax.annotate("", xy=D, xytext=C, arrowprops=dict(arrowstyle="->", color=C1, lw=1.4))
    ax.text(0.95, 0.05, r"$\vec r_{CD}$", color=C1, fontsize=10)
    ax.text(-1.75, -1.05, r"$U_P = U_D - 2\,\nabla U_C\cdot\vec r_{CD}$" "\n"
            r"$U_{f,L} = U_C + \frac{1}{2}\,\mathrm{limit}\!\left(2\nabla U_C\cdot\vec r_{CD} - (U_D-U_C),\; U_D - U_C\right)$",
            fontsize=9, va="top")
    ax.set_aspect("equal"); ax.set_xlim(-1.8, 2.5); ax.set_ylim(-1.75, 1.05)
    ax.axis("off")
    ax.set_title("Second-order face state on an unstructured grid: build the missing upwind point", fontsize=10)
    save(fig, "virtual_upwind_point")


# ---------------------------------------------------------------------------
# 15. Double-cone flow: schematic of the features (25/55 deg, 10.16 cm faces).
#     Shock positions are schematic, not a computed solution.
# ---------------------------------------------------------------------------
def double_cone_schematic():
    fig, ax = plt.subplots(figsize=(8.2, 5.0))
    L = 10.16
    a1, a2 = np.radians(25), np.radians(55)
    x1, y1 = L * np.cos(a1), L * np.sin(a1)
    x2, y2 = x1 + L * np.cos(a2), y1 + L * np.sin(a2)
    ax.fill([0, x1, x2, x2 + 4, x2 + 4, 0], [0, y1, y2, y2, -1.5, -1.5], color="#cfd8dc", ec="k", lw=1.2)
    S = np.array([4.5, 4.5 * np.tan(a1)])                    # separation point (first cone)
    R = np.array([x1 + 2.4 * np.cos(a2), y1 + 2.4 * np.sin(a2)])  # reattachment (second cone)
    I = np.array([8.0, 4.62])                                 # shock-shock interaction
    Q = np.array([8.4, 4.4])
    t = np.linspace(0, 1, 60)[:, None]
    bub = (1 - t) ** 2 * S + 2 * (1 - t) * t * Q + t ** 2 * R
    ax.fill(np.r_[bub[:, 0], x1], np.r_[bub[:, 1], y1], color="#ffcc80", ec=C1, lw=1.2)
    ax.plot([0, I[0]], [0, I[1]], color=C0, lw=1.8)            # attached leading-edge shock
    ax.plot([S[0], I[0]], [S[1], I[1]], color=C3, lw=1.6)      # separation shock
    yy = np.linspace(I[1], 16.5, 60)
    xx = (yy + 6.86) / 1.428 - 0.012 * (yy - I[1]) ** 2
    ax.plot(xx, yy, color=C1, lw=1.8)                          # bow shock
    ax.plot([I[0], R[0]], [I[1], R[1]], color=GREY, lw=1.2, ls="--")  # transmitted shock
    ax.plot(*I, "*", color="k", ms=11, zorder=5)
    ax.plot(*S, "o", color="k", ms=4); ax.plot(*R, "o", color="k", ms=4)
    kw = dict(fontsize=8.5, arrowprops=dict(arrowstyle="->", lw=0.8, color="k"))
    ax.annotate("attached leading-edge shock", xy=(3.0, 3.0 * I[1] / I[0]), xytext=(-4.2, 5.2), color=C0, **kw)
    ax.annotate("separation shock", xy=(6.2, S[1] + 1.7 * (I[1] - S[1]) / (I[0] - S[0])), xytext=(-1.5, 8.2), color=C3, **kw)
    ax.annotate("shock-shock interaction", xy=I, xytext=(0.5, 11.0), **kw)
    ax.annotate("bow shock", xy=(xx[40], yy[40]), xytext=(5.0, 15.0), color=C1, **kw)
    ax.annotate("separation zone", xy=(7.9, 3.95), xytext=(10.5, 1.2), color=C1, **kw)
    ax.annotate("reattachment:\npeak heat flux", xy=R, xytext=(13.2, 4.6), **kw)
    ax.annotate("", xy=(-0.6, 2.0), xytext=(-4.4, 2.0), arrowprops=dict(arrowstyle="->", lw=1.2))
    ax.text(-4.4, 2.4, "Mach 11.3", fontsize=8.5)
    ax.text(3.2, 0.55, r"25$^\circ$", fontsize=8.5)
    ax.text(12.9, 7.6, r"55$^\circ$", fontsize=8.5)
    yd = -2.6
    for xv in (S[0], R[0]):
        ax.plot([xv, xv], [yd - 0.2, -1.5], color="k", lw=0.6, ls=":")
    ax.annotate("", xy=(R[0], yd), xytext=(S[0], yd), arrowprops=dict(arrowstyle="<->", lw=1))
    ax.text(0.5 * (S[0] + R[0]), yd - 1.0, r"$L_s$: axial separation length", ha="center", fontsize=9)
    ax.set_aspect("equal"); ax.set_xlim(-4.6, 21); ax.set_ylim(-4.2, 17)
    ax.axis("off")
    ax.set_title("Double-cone flow (schematic, not to scale)", fontsize=10)
    save(fig, "double_cone_schematic")



# ---------------------------------------------------------------------------
# 16. The Riemann problem at a face: cells, reconstructed states, x-t wave fan.
#     Schematic.
# ---------------------------------------------------------------------------
def riemann_face_and_fan():
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(10.5, 3.9), gridspec_kw={"width_ratios": [1.15, 1]})
    # left: cell averages and piecewise-linear reconstruction
    xc = np.arange(4) + 0.5
    ubar = np.array([1.0, 0.92, 0.45, 0.38])
    slopes = np.array([-0.06, -0.10, -0.08, -0.05])
    for i, (x0, ub, sl) in enumerate(zip(xc, ubar, slopes)):
        a1.plot([x0 - 0.5, x0 + 0.5], [ub, ub], color=GREY, lw=1, ls=":")
        a1.plot([x0 - 0.5, x0 + 0.5], [ub - 0.5 * sl, ub + 0.5 * sl], color=C0, lw=2)
    for xf in range(5):
        a1.axvline(xf, color="#bdbdbd", lw=0.8)
    a1.axvline(2, color=C1, lw=2)
    uL = ubar[1] + 0.5 * slopes[1]
    uR = ubar[2] - 0.5 * slopes[2]
    a1.plot([2], [uL], "o", color=C0)
    a1.plot([2], [uR], "o", color=C0)
    a1.annotate(r"$\mathbf{U}_L$ (from cell $i$)", xy=(2, uL), xytext=(0.35, 0.72), fontsize=9,
                arrowprops=dict(arrowstyle="->", color=C0))
    a1.annotate(r"$\mathbf{U}_R$ (from cell $i+1$)", xy=(2, uR), xytext=(2.35, 0.72), fontsize=9,
                arrowprops=dict(arrowstyle="->", color=C0))
    for i, lab in enumerate(["$i-1$", "$i$", "$i+1$", "$i+2$"]):
        a1.text(xc[i], 0.22, lab, ha="center", fontsize=9)
    a1.text(2, 1.12, r"face $i+\frac{1}{2}$", ha="center", color=C1, fontsize=9)
    a1.set(xlim=(0, 4), ylim=(0.15, 1.2), xticks=[], yticks=[], xlabel="x",
           title="1. Reconstruct: two states meet at each face\n(dotted: cell averages; solid: reconstructed profile)")
    a1.grid(False)
    # right: x-t diagram at that face
    t = np.linspace(0, 1, 2)
    for sp in np.linspace(-1.3, -0.75, 6):  # left rarefaction fan
        a2.plot(sp * t, t, color=C0, lw=1)
    a2.plot(0.35 * t, t, color=C2, lw=1.8, ls="--")  # contact
    a2.plot(1.15 * t, t, color=C3, lw=2.2)  # right shock
    a2.axvline(0, color=C1, lw=2)
    a2.text(-1.45, 0.25, r"$\mathbf{U}_L$", fontsize=11)
    a2.text(1.25, 0.25, r"$\mathbf{U}_R$", fontsize=11)
    a2.text(-0.45, 0.82, r"$\mathbf{U}_{*L}$", fontsize=11)
    a2.text(0.62, 0.82, r"$\mathbf{U}_{*R}$", fontsize=11)
    a2.text(-1.55, 1.04, "rarefaction\n(left acoustic, $u-a$)", fontsize=8, color=C0)
    a2.text(0.12, 1.04, "contact ($u$)", fontsize=8, color=C2)
    a2.text(0.95, 1.04, "shock\n($u+a$)", fontsize=8, color=C3)
    a2.annotate("flux is evaluated on this line:\n" + r"$\hat{\mathbf{F}} = \mathbf{F}(\mathbf{U}(x/t = 0))$",
                xy=(0, 0.5), xytext=(0.25, 0.42), fontsize=8.5, color=C1, arrowprops=dict(arrowstyle="->", color=C1))
    a2.set(xlim=(-1.6, 1.6), ylim=(0, 1.25), xticks=[0], xticklabels=[r"face"], yticks=[], xlabel="x", ylabel="t",
           title="2. Solve the Riemann problem there\n(one possible wave pattern; schematic)")
    a2.grid(False)
    save(fig, "riemann_face_and_fan")


# ---------------------------------------------------------------------------
# 17. Exact vs HLL vs HLLC wave models in the x-t plane. Schematic.
# ---------------------------------------------------------------------------
def riemann_fans_compare():
    fig, axes = plt.subplots(1, 3, figsize=(11, 3.6), sharey=True)
    t = np.array([0, 1.0])
    titles = ["Exact (Godunov)\nall waves, true shapes",
              "HLL\ntwo waves, one averaged state",
              "HLLC\nthree waves, two star states"]
    for ax, ttl in zip(axes, titles):
        ax.axvline(0, color=C1, lw=1.6)
        ax.set(xlim=(-1.5, 1.5), ylim=(0, 1.2), xticks=[], yticks=[], title=ttl)
        ax.grid(False)
        ax.text(-1.4, 0.15, r"$\mathbf{U}_L$", fontsize=11)
        ax.text(1.12, 0.15, r"$\mathbf{U}_R$", fontsize=11)
    a = axes[0]
    for sp in np.linspace(-1.2, -0.7, 6):
        a.plot(sp * t, t, color=C0, lw=1)
    a.plot(0.3 * t, t, color=C2, ls="--", lw=1.8)
    a.plot(1.05 * t, t, color=C3, lw=2.2)
    a.text(-0.42, 0.85, r"$\mathbf{U}_{*L}$", fontsize=10)
    a.text(0.5, 0.85, r"$\mathbf{U}_{*R}$", fontsize=10)
    a = axes[1]
    a.plot(-1.25 * t, t, color=C3, lw=2)
    a.plot(1.15 * t, t, color=C3, lw=2)
    a.fill([0, -1.25, 1.15], [0, 1, 1], color=C0, alpha=0.10, lw=0)
    a.text(-0.35, 0.8, r"$\mathbf{U}_{\mathrm{HLL}}$", fontsize=11)
    a.text(-1.45, 1.03, r"$S_L$", color=C3)
    a.text(1.08, 1.03, r"$S_R$", color=C3)
    a.text(-0.95, 0.45, "contact lost:\naveraged away", fontsize=7.5, color=GREY)
    a = axes[2]
    a.plot(-1.25 * t, t, color=C3, lw=2)
    a.plot(1.15 * t, t, color=C3, lw=2)
    a.plot(0.3 * t, t, color=C2, ls="--", lw=1.8)
    a.text(-0.55, 0.8, r"$\mathbf{U}_{*L}$", fontsize=10)
    a.text(0.45, 0.8, r"$\mathbf{U}_{*R}$", fontsize=10)
    a.text(-1.45, 1.03, r"$S_L$", color=C3)
    a.text(0.22, 1.03, r"$S_*$", color=C2)
    a.text(1.08, 1.03, r"$S_R$", color=C3)
    save(fig, "riemann_fans_compare")


# ---------------------------------------------------------------------------
# 18. Entropy fix demo on Burgers' equation: a transonic rarefaction
#     (uL < 0 < uR). Roe keeps an expansion shock; Harten's fix, HLL,
#     Rusanov and Godunov produce the fan. Computed here, first order.
# ---------------------------------------------------------------------------
def entropy_fix_burgers():
    uL0, uR0, t_end, N = -0.5, 1.0, 1.0, 400
    x = np.linspace(-2, 2, N, endpoint=False) + 2.0 / N
    dx = 4.0 / N
    f = lambda u: 0.5 * u ** 2

    def flux(name, ul, ur):
        a = 0.5 * (ul + ur)  # Roe speed for Burgers
        if name == "Roe":
            return 0.5 * (f(ul) + f(ur)) - 0.5 * np.abs(a) * (ur - ul)
        if name == "Roe + Harten fix":
            d = 0.5
            aa = np.where(np.abs(a) < d, (a ** 2 + d ** 2) / (2 * d), np.abs(a))
            return 0.5 * (f(ul) + f(ur)) - 0.5 * aa * (ur - ul)
        if name == "HLL (Einfeldt speeds)":
            sl = np.minimum(np.minimum(ul, ur), a)
            sr = np.maximum(np.maximum(ul, ur), a)
            fh = (sr * f(ul) - sl * f(ur) + sl * sr * (ur - ul)) / np.where(sr - sl > 1e-14, sr - sl, 1.0)
            return np.where(sl >= 0, f(ul), np.where(sr <= 0, f(ur), fh))
        if name == "Godunov (exact)":
            shock = ul > ur
            s = 0.5 * (ul + ur)
            fs = np.where(s > 0, f(ul), f(ur))
            fr = np.where(ul > 0, f(ul), np.where(ur < 0, f(ur), 0.0))
            return np.where(shock, fs, fr)

    names = ["Roe", "Roe + Harten fix", "HLL (Einfeldt speeds)", "Godunov (exact)"]
    styles = [(C1, "-", 2.0), (C0, "--", 1.6), (C2, "-.", 1.6), (C3, ":", 2.0)]
    fig, ax = plt.subplots(figsize=(7.2, 4.0))
    xe = np.linspace(-2, 2, 800)
    ue = np.where(xe < uL0 * t_end, uL0, np.where(xe > uR0 * t_end, uR0, xe / t_end))
    ax.plot(xe, ue, color="k", lw=3, alpha=0.25, label="exact: rarefaction fan")
    for name, (c, ls, lw) in zip(names, styles):
        u = np.where(x < 0, uL0, uR0)
        dt = 0.4 * dx / max(abs(uL0), abs(uR0))
        t = 0.0
        while t < t_end - 1e-12:
            h = min(dt, t_end - t)
            ue_ = np.concatenate(([uL0], u, [uR0]))
            F = flux(name, ue_[:-1], ue_[1:])
            u = u - h / dx * (F[1:] - F[:-1])
            t += h
        ax.plot(x, u, color=c, ls=ls, lw=lw, label=name)
    ax.annotate("Roe: the jump survives as an\nexpansion shock moving at " + r"$\tilde a = (u_L+u_R)/2$",
                xy=(0.25, 0.25), xytext=(-1.9, 0.62), fontsize=8.5, color=C1,
                arrowprops=dict(arrowstyle="->", color=C1))
    ax.set(xlabel="x", ylabel="u", xlim=(-2, 2), ylim=(-0.65, 1.1),
           title="Burgers, transonic rarefaction ($u_L=-0.5$, $u_R=1$), t = 1, 400 cells, first order\n(computed in scripts/make_figures.py; Harten $\\delta = 0.5$)")
    ax.legend(fontsize=8, loc="lower right")
    save(fig, "entropy_fix_burgers")


# ---------------------------------------------------------------------------
# 19. Capsule flow-field anatomy, forebody to wake. Schematic, not to scale.
# ---------------------------------------------------------------------------
def capsule_anatomy():
    fig, ax = plt.subplots(figsize=(11, 6.2))
    # capsule: shallow spherical heat shield (left), rounded shoulder, conical backshell
    Rb, Rn = 1.0, 2.4  # base radius, nose radius
    th = np.linspace(-np.arcsin(Rb / Rn), np.arcsin(Rb / Rn), 200)
    hx = -(Rn * np.cos(th) - Rn * np.cos(th[0]))  # heat shield, apex at x<0
    hy = Rn * np.sin(th)
    hx = hx - hx.max()  # apex at negative x, rim at x=0
    bx = np.array([0.0, 0.08, 1.05, 1.15])
    by = np.array([1.0, 1.03, 0.42, 0.38])
    upper = np.concatenate([hx[hy >= 0][::-1], bx])
    uy = np.concatenate([hy[hy >= 0][::-1], by])
    outline_x = np.concatenate([upper, [1.15], upper[::-1]])
    outline_y = np.concatenate([uy, [-0.38], -uy[::-1]])
    ax.fill(outline_x, outline_y, color="#cfd8dc", zorder=3)
    ax.plot(outline_x, outline_y, color="k", lw=1.4, zorder=4)
    apex = hx.min()
    # bow shock
    ys = np.linspace(-2.6, 2.6, 300)
    xs = apex - 0.28 - 0.42 * (np.sqrt(1 + (ys / 0.75) ** 2) - 1)
    ax.plot(xs, ys, color=C1, lw=2.2)
    # boundary layer (thin band along heat shield and around shoulder)
    for sgn in (1, -1):
        yy = np.linspace(0, 1.0, 50)
        xx = np.interp(yy, hy[hy >= 0], hx[hy >= 0])
        ax.plot(xx - 0.06 - 0.06 * yy, sgn * yy, color=C2, lw=1.2)
    # shoulder expansion fan
    for ang in np.radians([10, 25, 40, 55]):
        ax.plot([0.04, 0.04 + 0.9 * np.cos(ang)], [1.03, 1.03 + 0.9 * np.sin(ang)], color=C0, lw=0.8)
        ax.plot([0.04, 0.04 + 0.9 * np.cos(ang)], [-1.03, -1.03 - 0.9 * np.sin(ang)], color=C0, lw=0.8)
    # free shear layers from shoulder to neck
    xn = 3.3
    sx = np.linspace(0.08, xn, 100)
    sy = 1.03 - (1.03 - 0.12) * ((sx - 0.08) / (xn - 0.08)) ** 1.3
    for sgn in (1, -1):
        ax.plot(sx, sgn * sy, color=C3, lw=1.6)
        ax.plot(sx, sgn * (sy + 0.04 * np.sin(9 * sx) * (sx / xn)), color=C3, lw=0.8, alpha=0.5)
    # recirculation zone
    ax.fill(np.concatenate([sx, sx[::-1]]), np.concatenate([sy, -sy[::-1]]) * 0.96, color=C3, alpha=0.07)
    for cy, d in [(0.42, 1), (-0.42, -1)]:
        e = np.linspace(0, 2 * np.pi * 0.85, 60)
        ax.plot(2.0 + 0.55 * np.cos(e), cy + 0.22 * d * np.sin(e), color=C3, lw=0.9)
        ax.annotate("", xy=(2.0 + 0.55 * np.cos(e[-1]), cy + 0.22 * d * np.sin(e[-1])),
                    xytext=(2.0 + 0.55 * np.cos(e[-3]), cy + 0.22 * d * np.sin(e[-3])),
                    arrowprops=dict(arrowstyle="->", color=C3, lw=0.9))
    # recompression shocks and wake
    for sgn in (1, -1):
        ax.plot([xn - 0.2, xn + 1.4], [sgn * 0.15, sgn * 1.25], color=C1, lw=1.5)
    wx = np.linspace(xn, 6.2, 100)
    for sgn in (1, -1):
        ax.plot(wx, sgn * (0.12 + 0.08 * (wx - xn)), color=GREY, lw=1, ls="--")
    # labels
    L = dict(fontsize=8.5)
    def lab(n, xy, xt, txt, c="k"):
        ax.annotate(f"({n}) {txt}", xy=xy, xytext=xt, color=c, arrowprops=dict(arrowstyle="->", color=c, lw=0.8), **L)
    lab(1, (xs[150] , 0.0), (-3.9, -0.35), "bow shock\n(near-normal on axis)", C1)
    lab(2, (apex - 0.15, 0.25), (-3.9, 0.65), "shock layer / stagnation region\n(subsonic, reacting, nonequilibrium\njust behind the shock)")
    lab(3, (0.55, -1.2), (-3.9, -1.9), "entropy layer\n(high-entropy gas from the near-normal\npart of the shock, wrapping the body)")
    lab(4, (-0.12, -0.55), (-2.6, -2.65), "boundary layer\n(laminar on most forebodies)", C2)
    lab(5, (0.35, 1.45), (-0.4, 2.45), "shoulder expansion\n(p, T fall fast; chemistry freezes)", C0)
    lab(6, (1.6, 0.75), (1.4, 2.0), "free shear layer\n(transitions, unsteady)", C3)
    lab(7, (2.0, -0.3), (2.0, -2.25), "recirculation zone / base flow\n(low speed, low density, reversed)", C3)
    lab(8, (xn, 0.0), (4.3, -1.2), "neck: shear layers converge,\nrear stagnation point", "k")
    lab(9, (xn + 0.7, 0.68), (4.3, 1.6), "recompression shock", C1)
    lab(10, (5.5, 0.3), (5.0, 0.8), "far wake", GREY)
    ax.annotate("", xy=(-3.2, 1.5), xytext=(-4.0, 1.5), arrowprops=dict(arrowstyle="->", lw=1.3))
    ax.text(-4.0, 1.6, r"$M_\infty \gg 1$", fontsize=9)
    ax.set_aspect("equal")
    ax.set(xlim=(-4.1, 6.3), ylim=(-2.85, 2.85), xticks=[], yticks=[],
           title="Flow around an entry capsule, forebody to wake (schematic, not to scale; zero angle of attack)")
    ax.grid(False)
    for s in ax.spines.values():
        s.set_visible(False)
    save(fig, "capsule_anatomy")


# ---------------------------------------------------------------------------
# 20. Sutton-Graves stagnation heating, Earth: q = k sqrt(rho/R_n) V^3,
#     k = 1.7415e-4 (SI). Computed from the correlation.
# ---------------------------------------------------------------------------
def sutton_graves_map():
    k = 1.7415e-4
    V = np.linspace(4e3, 13e3, 200)
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(10.5, 3.9))
    for rho, c in zip([1e-4, 3e-4, 1e-3], [C0, C1, C2]):
        a1.plot(V / 1e3, k * np.sqrt(rho / 1.0) * V ** 3 / 1e4, color=c, lw=2, label=rf"$\rho_\infty$ = {rho:g} kg/m³")
    a1.set(yscale="log", xlabel="entry velocity $V_\\infty$ (km/s)", ylabel="$q_s$ (W/cm²)",
           title="Sutton–Graves convective stagnation heating, Earth\n$R_n$ = 1 m")
    a1.legend(fontsize=8)
    Rn = np.logspace(-2, 1, 200)
    for Vk, c in zip([7.5, 11.0], [C0, C1]):
        a2.plot(Rn, k * np.sqrt(3e-4 / Rn) * (Vk * 1e3) ** 3 / 1e4, color=c, lw=2, label=f"V = {Vk} km/s")
    a2.set(xscale="log", yscale="log", xlabel="nose radius $R_n$ (m)", ylabel="$q_s$ (W/cm²)",
           title="Effect of nose radius ($\\rho_\\infty$ = 3×10⁻⁴ kg/m³)\nslope −1/2: blunter is cooler (convective only)")
    a2.legend(fontsize=8)
    save(fig, "sutton_graves_map")


# ---------------------------------------------------------------------------
# 21. Hypersonic shock limits and Newtonian pressure. Computed from the
#     perfect-gas relations, gamma = 1.4.
# ---------------------------------------------------------------------------
def shock_limits_newtonian():
    g = 1.4
    M = np.linspace(1.01, 25, 400)
    rr = (g + 1) * M ** 2 / ((g - 1) * M ** 2 + 2)
    pr = 1 + 2 * g / (g + 1) * (M ** 2 - 1)
    def cpmax(M):
        a = ((g + 1) ** 2 * M ** 2 / (4 * g * M ** 2 - 2 * (g - 1))) ** (g / (g - 1))
        b = (1 - g + 2 * g * M ** 2) / (g + 1)
        return 2 / (g * M ** 2) * (a * b - 1)
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(10.5, 3.9))
    a1.plot(M, rr, color=C0, lw=2, label=r"$\rho_2/\rho_1$")
    a1.axhline((g + 1) / (g - 1), color=C0, ls=":", lw=1)
    a1.text(14, 6.15, r"limit $(\gamma+1)/(\gamma-1) = 6$", color=C0, fontsize=8.5)
    a1.plot(M, cpmax(M), color=C1, lw=2, label=r"$C_{p,\max}$ (stagnation, behind normal shock)")
    a1.axhline(1.839, color=C1, ls=":", lw=1)
    a1.text(14, 2.05, r"limit 1.839", color=C1, fontsize=8.5)
    a1.plot(M, pr / M ** 2, color=C2, lw=1.6, ls="--", label=r"$(p_2/p_1)/M_1^2$, limit $2\gamma/(\gamma+1) = 1.17$")
    a1.set(xlabel=r"$M_1$", ylim=(0, 7), title="Normal shock, perfect gas γ = 1.4:\nratios freeze as M grows (Mach-number independence)")
    a1.legend(fontsize=8, loc="center right")
    phi = np.linspace(0, 90, 200)
    for Mi, c in zip([5, 20], [C0, C1]):
        a2.plot(phi, cpmax(Mi) * np.cos(np.radians(phi)) ** 2, color=c, lw=2, label=f"modified Newtonian, M = {Mi}")
    a2.plot(phi, 2 * np.cos(np.radians(phi)) ** 2, color=GREY, ls="--", lw=1.4, label="Newtonian, $C_p = 2\\sin^2\\theta$")
    a2.set(xlabel=r"angle from stagnation point on a sphere, $\phi$ (deg)", ylabel=r"$C_p$",
           title="Newtonian pressure on a sphere:\n" + r"$C_p = C_{p,\max}\cos^2\phi$ (computed)")
    a2.legend(fontsize=8)
    save(fig, "shock_limits_newtonian")


# ---------------------------------------------------------------------------
# 22. Rarefaction regimes vs Knudsen number. Schematic (indicative bounds).
# ---------------------------------------------------------------------------
def knudsen_regimes():
    fig, ax = plt.subplots(figsize=(9.5, 3.2))
    rows = [("Euler", 1e-6, 1e-3, C0), ("Navier–Stokes (no slip)", 1e-6, 1e-3, C0),
            ("Navier–Stokes + slip / jump walls", 1e-3, 1e-1, C2),
            ("DSMC / Boltzmann", 1e-3, 1e3, C1), ("Free-molecular (collisionless)", 10, 1e3, C3)]
    for i, (lab, a, b, c) in enumerate(rows):
        ax.barh(i, np.log10(b) - np.log10(a), left=np.log10(a), color=c, alpha=0.75, height=0.6)
        ax.text(np.log10(a) + 0.08, i, lab, va="center", fontsize=8.5, color="k")
    for x in [-3, -1, 1]:
        ax.axvline(x, color=GREY, lw=0.8, ls=":")
    for xc, t in [(-4.5, "continuum"), (-2, "slip"), (0, "transitional"), (2, "free-molecular")]:
        ax.text(xc, len(rows) - 0.3, t, ha="center", fontsize=9, color=GREY)
    ax.set_yticks([])
    ax.set_xticks(range(-6, 4))
    ax.set_xticklabels([f"$10^{{{k}}}$" for k in range(-6, 4)])
    ax.set(xlim=(-6, 3), ylim=(-0.6, len(rows) + 0.1), xlabel=r"Knudsen number $Kn = \lambda/L$",
           title="Where each model is valid (schematic; bounds are indicative, after Bird 1994)")
    ax.invert_yaxis()
    ax.grid(False)
    save(fig, "knudsen_regimes")


# ---------------------------------------------------------------------------
# 23. Plasma frequency vs electron density, with communication bands.
#     Computed: f_p = 8.98 sqrt(n_e) Hz, n_e in m^-3.
# ---------------------------------------------------------------------------
def plasma_frequency_bands():
    ne = np.logspace(14, 20, 300)
    fp = 8.98 * np.sqrt(ne)
    fig, ax = plt.subplots(figsize=(7.4, 4.0))
    ax.plot(ne, fp / 1e9, color=C0, lw=2.2, label=r"plasma frequency $f_p = 8.98\sqrt{n_e}$")
    bands = [("VHF voice (~0.3 GHz)", 0.3e9, GREY), ("GPS L1 (1.58 GHz)", 1.575e9, C2),
             ("S-band (2.3 GHz)", 2.3e9, C1), ("X-band (8.4 GHz)", 8.4e9, C3), ("Ka-band (32 GHz)", 32e9, "#6a3d9a")]
    for lab, f, c in bands:
        nc = (f / 8.98) ** 2
        ax.axhline(f / 1e9, color=c, ls=":", lw=1)
        ax.plot([nc], [f / 1e9], "o", color=c)
        yoff = 0.72 if "GPS" in lab else 1.1
        ax.text(1.3e14, f / 1e9 * yoff, f"{lab}: blacked out above $n_e$ ≈ {nc:.1e} m⁻³", fontsize=7.5, color=c)
    ax.set(xscale="log", yscale="log", xlabel=r"electron number density $n_e$ (m$^{-3}$)", ylabel="frequency (GHz)",
           title="Signals below the local plasma frequency are reflected (computed;\ncollisions add attenuation below this cutoff too)")
    ax.legend(fontsize=8, loc="lower right")
    save(fig, "plasma_frequency_bands")


# ---------------------------------------------------------------------------
# 24. Physics ladder vs Earth entry velocity. Schematic, indicative onsets
#     (stagnation region of a metre-scale blunt body).
# ---------------------------------------------------------------------------
def physics_ladder():
    rows = [
        ("Vibrational excitation", 1.0, 16, C0),
        ("O₂ dissociation", 2.5, 16, C0),
        ("N₂ dissociation", 5.0, 16, C0),
        ("Ionization (NO⁺ first, then N⁺, O⁺)", 7.0, 16, C1),
        ("Radiative heating: secondary", 10.0, 12.0, C3),
        ("Radiative heating: comparable / dominant", 12.0, 16, C3),
    ]
    fig, ax = plt.subplots(figsize=(9.5, 4.2))
    for i, (lab, a, b, c) in enumerate(rows):
        ax.barh(i, b - a, left=a, color=c, alpha=0.75, height=0.55)
        ax.text(a + 0.12, i, lab, va="center", fontsize=8.5)
    for v, lab in [(7.8, "LEO return\n~7.8"), (11.0, "lunar return\n(Apollo, Orion) ~11"), (12.9, "Stardust\n12.9")]:
        ax.axvline(v, color=GREY, ls="--", lw=1)
        ax.text(v, len(rows) + 0.25, lab, ha="center", va="center", fontsize=7.5, color=GREY)
    sec = ax.secondary_xaxis("top", functions=(lambda x: x / 0.315, lambda m: m * 0.315))
    sec.set_xlabel("approximate Mach number at ~60 km altitude (a ≈ 315 m/s)")
    ax.set(xlim=(0, 16), ylim=(-0.6, len(rows) + 0.75), yticks=[], xlabel="flight velocity (km/s), Earth atmosphere",
           title="What turns on as entry speed rises (schematic; onsets indicative, see text)")
    ax.invert_yaxis()
    ax.grid(axis="y", visible=False)
    save(fig, "physics_ladder")


# ---------------------------------------------------------------------------
# Boundary conditions: how many characteristics enter at each boundary type.
# ---------------------------------------------------------------------------
def bc_characteristics():
    fig, axes = plt.subplots(1, 4, figsize=(11.5, 3.1), sharey=True)
    cases = [
        ("Supersonic inflow\n(free stream)", 2.0, "left"),
        ("Subsonic inflow", 0.5, "left"),
        ("Subsonic outflow", 0.5, "right"),
        ("Supersonic outflow", 2.0, "right"),
    ]
    labels = [r"$u_n - a$", r"$u_n$", r"$u_n + a$"]
    for ax, (title, M, side) in zip(axes, cases):
        speeds = [M - 1.0, M, M + 1.0]  # in units of a, flow left to right
        xb = 0.0
        ax.axvline(xb, color="k", lw=2)
        if side == "left":
            ax.axvspan(xb, 1.2, color=C0, alpha=0.06)
            ax.text(0.6, 0.06, "domain", ha="center", color=C0, fontsize=9)
        else:
            ax.axvspan(-1.2, xb, color=C0, alpha=0.06)
            ax.text(-0.6, 0.06, "domain", ha="center", color=C0, fontsize=9)
        n_in = 0
        for s, lab in zip(speeds, labels):
            # a characteristic through the boundary point at t = 0.5
            t = np.linspace(0, 1, 2)
            x = s * (t - 0.5) * 0.9
            entering = (s > 0) if side == "left" else (s < 0)
            n_in += entering
            col = C1 if entering else GREY
            ax.plot(x, t, color=col, lw=2.2 if entering else 1.4, ls="-" if entering else "--")
            ax.annotate(
                "", xy=(x[1], t[1]), xytext=(x[1] - 0.12 * s, t[1] - 0.12 / 0.9),
                arrowprops=dict(arrowstyle="->", color=col, lw=1.6),
            )
            ax.text(x[1], 1.03, lab, ha="center", va="bottom", fontsize=8, color=col)
        ax.set_title(title, fontsize=10)
        ax.text(
            0.5, -0.2, f"specify {n_in} of 3 wave families\nextrapolate {3 - n_in}",
            transform=ax.transAxes, ha="center", va="top", fontsize=9,
        )
        ax.set_xlim(-1.2, 1.2)
        ax.set_ylim(0, 1.18)
        ax.set_xticks([])
        ax.set_yticks([])
        ax.grid(False)
        for sp in ax.spines.values():
            sp.set_visible(False)
    axes[0].set_ylabel("time")
    fig.suptitle("Characteristics through a boundary point (flow left to right; solid orange = entering the domain)", fontsize=10, y=1.16)
    save(fig, "bc_characteristics")


# ---------------------------------------------------------------------------
# Wall BCs: radiative-equilibrium wall temperature, and what a catalytic wall
# does to the atom profile (schematic).
# ---------------------------------------------------------------------------
def wall_bc_thermal_catalytic():
    fig, axes = plt.subplots(1, 2, figsize=(10.5, 3.7))
    ax = axes[0]
    sigma = 5.670e-8
    q = np.logspace(0, 3.2, 200)  # W/cm^2
    for eps, col in ((0.6, C2), (0.85, C0), (1.0, GREY)):
        ax.semilogx(q, (q * 1e4 / (eps * sigma)) ** 0.25, color=col, label=rf"$\varepsilon = {eps}$")
    for qq in (10, 100, 1000):
        T = (qq * 1e4 / (0.85 * sigma)) ** 0.25
        ax.plot(qq, T, "o", color=C0)
        ax.annotate(f"{T:.0f} K", (qq, T), textcoords="offset points", xytext=(-8, 8), ha="right", fontsize=9)
    ax.set_xlabel(r"heat flux into the wall, $q_w$ (W/cm$^2$)")
    ax.set_ylabel(r"radiative-equilibrium $T_w$ (K)")
    ax.set_title(r"$q_w = \varepsilon\sigma T_w^4$ (computed)", fontsize=10)
    ax.legend(frameon=False)

    ax = axes[1]
    y = np.linspace(0, 1, 200)
    edge = 0.6
    nc = edge * np.ones_like(y)
    fc = edge * (1 - np.exp(-y / 0.22)) / (1 - np.exp(-1 / 0.22))
    pc = 0.45 * nc + 0.55 * fc
    ax.plot(nc, y, color=C2, label=r"non-catalytic: $\partial Y_a/\partial n = 0$")
    ax.plot(pc, y, color=C0, label=r"partially catalytic: finite $\gamma$")
    ax.plot(fc, y, color=C1, label="fully catalytic: atoms recombine at the wall")
    ax.axhline(0, color="k", lw=3)
    ax.text(0.7, 0.03, "wall", ha="center", va="bottom", fontsize=9)
    ax.annotate("steeper gradient here\n= larger diffusive heating", xy=(0.12, 0.04), xytext=(0.2, 0.42),
                arrowprops=dict(arrowstyle="->", color=C1), color=C1, fontsize=9)
    ax.set_xlabel(r"atom mass fraction $Y_a$")
    ax.set_ylabel("distance from wall / boundary-layer thickness")
    ax.set_xlim(0, 0.75)
    ax.set_ylim(-0.02, 1)
    ax.set_title("Atom profile in a frozen boundary layer (schematic)", fontsize=10)
    ax.legend(frameon=False, fontsize=8, loc="upper left")
    save(fig, "wall_bc_thermal_catalytic")


# ---------------------------------------------------------------------------
# Surface energy balance: the control surface (schematic) and the blowing
# reduction of the heat-transfer coefficient (computed).
# ---------------------------------------------------------------------------
def surface_energy_balance():
    fig, axes = plt.subplots(1, 2, figsize=(11, 3.9), gridspec_kw={"width_ratios": [1.35, 1]})
    ax = axes[0]
    ax.axhspan(-1, 0, color="#bcaaa4", alpha=0.6)
    ax.axhline(0, color="k", lw=2)
    ax.text(-0.02, -0.5, "material\n(char, then virgin)", ha="left", va="center", fontsize=9)
    ax.text(-0.02, 0.12, "gas", ha="left", va="center", fontsize=9)

    def arrow(x, y0, y1, col, text, ty, ha="center"):
        ax.annotate("", xy=(x, y1), xytext=(x, y0), arrowprops=dict(arrowstyle="-|>", color=col, lw=2.2))
        ax.text(x, ty, text, ha=ha, va="center", fontsize=8.5, color=col)

    arrow(0.16, 0.62, 0.04, C1, "conduction +\nspecies diffusion\n" + r"$\rho_e u_e C_H(H_r - h_w)$", 0.78)
    arrow(0.40, 0.62, 0.04, C1, "absorbed\nradiation\n" + r"$\alpha\,q_{rad}$", 0.78)
    arrow(0.60, 0.04, 0.62, C0, "reradiation\n" + r"$\varepsilon\sigma T_w^4$", 0.76)
    arrow(0.86, 0.04, 0.62, C0, "blown gas\nleaves\n" + r"$(\dot m_g + \dot m_c)\,h_w$", 0.80)
    arrow(0.30, -0.04, -0.62, C0, "conduction\ninto solid\n" + r"$q_{cond}$", -0.8)
    arrow(0.56, -0.62, -0.04, C1, "pyrolysis gas\narrives\n" + r"$\dot m_g h_g$", -0.8)
    arrow(0.80, -0.62, -0.04, C1, "char consumed\n" + r"$\dot m_c h_c$", -0.8)
    ax.set_xlim(-0.05, 1.02)
    ax.set_ylim(-1, 1)
    ax.axis("off")
    ax.set_title("Energy crossing the surface (schematic; orange = in, blue = out)", fontsize=10)

    ax = axes[1]
    B = np.linspace(1e-3, 5, 300)
    for lam, col, lab in ((0.5, C0, r"laminar, $\lambda = 0.5$"), (0.4, C2, r"turbulent, $\lambda = 0.4$")):
        phi = 2 * lam * B
        ax.plot(B, phi / np.expm1(phi), color=col, label=lab)
    ax.plot(1, 1 / np.expm1(1.0), "o", color=C0)
    ax.annotate("0.58", (1, 1 / np.expm1(1.0)), textcoords="offset points", xytext=(8, 6), fontsize=9)
    ax.set_xlabel(r"$B'_0 = \dot m / (\rho_e u_e C_{H0})$")
    ax.set_ylabel(r"$C_H / C_{H0}$")
    ax.set_title(r"Blowing correction $\varphi/(e^{\varphi}-1)$, $\varphi = 2\lambda B'_0$ (computed)", fontsize=10)
    ax.set_ylim(0, 1.02)
    ax.legend(frameon=False)
    save(fig, "surface_energy_balance")


# ---------------------------------------------------------------------------
# Explicit methods: linear stability regions of Runge-Kutta schemes, with the
# eigenvalues of typical spatial operators.
# ---------------------------------------------------------------------------
def rk_stability_regions():
    import math

    fig, axes = plt.subplots(1, 2, figsize=(10.5, 4.2))
    x = np.linspace(-3.4, 0.8, 500)
    y = np.linspace(-3.3, 3.3, 600)
    X, Y = np.meshgrid(x, y)
    Z = X + 1j * Y
    ax = axes[0]
    handles = []
    for s, col, name in ((1, GREY, "forward Euler"), (2, C2, "RK2 (SSP-RK2)"), (3, C0, "RK3 (SSP-RK3)"), (4, C1, "RK4")):
        G = sum(Z**k / math.factorial(k) for k in range(s + 1))
        ax.contour(X, Y, np.abs(G), levels=[1.0], colors=[col], linewidths=1.8)
        handles.append(plt.Line2D([], [], color=col, lw=1.8, label=name))
    ax.axhline(0, color="k", lw=0.6)
    ax.axvline(0, color="k", lw=0.6)
    ax.set_aspect("equal")
    ax.set_xlabel(r"Re($\lambda\Delta t$)")
    ax.set_ylabel(r"Im($\lambda\Delta t$)")
    ax.set_title(r"Stable where $|G(\lambda\Delta t)| \leq 1$ (inside each curve)", fontsize=10)
    ax.legend(handles=handles, frameon=False, fontsize=8, loc="upper left")

    ax = axes[1]
    G3 = sum(Z**k / math.factorial(k) for k in range(4))
    ax.contourf(X, Y, np.abs(G3), levels=[0, 1.0], colors=[C0], alpha=0.12)
    ax.contour(X, Y, np.abs(G3), levels=[1.0], colors=[C0], linewidths=1.8)
    th = np.linspace(0, 2 * np.pi, 41)
    c = 1.0
    ax.plot(-c * (1 - np.cos(th)), -c * np.sin(th), "o", ms=3.5, color=C1, label="first-order upwind convection, CFL = 1")
    ax.plot(0 * th, 1.5 * np.sin(th), "s", ms=3.5, color=C2, label="central convection, CFL = 1.5")
    r = 0.5
    ax.plot(-2 * r * (1 - np.cos(th)), 0 * th, "^", ms=3.5, color=C3, label=r"central diffusion, $\nu\Delta t/\Delta x^2 = 0.5$")
    ax.axhline(0, color="k", lw=0.6)
    ax.axvline(0, color="k", lw=0.6)
    ax.set_aspect("equal")
    ax.set_xlabel(r"Re($\lambda\Delta t$)")
    ax.set_title("Where spatial operators put their eigenvalues\n(shaded: RK3 region)", fontsize=10)
    ax.legend(frameon=False, fontsize=8, loc="upper left")
    save(fig, "rk_stability_regions")


# ---------------------------------------------------------------------------
# Dual time stepping: subiteration sawtooth (schematic) and what the physical
# time step does to a resolved oscillation (computed).
# ---------------------------------------------------------------------------
def dual_time_stepping():
    fig, axes = plt.subplots(1, 2, figsize=(10.5, 3.7))
    ax = axes[0]
    k = np.arange(0, 13)
    for n in range(4):
        res = 10.0 ** (-0.28 * k) * (1.0 if n else 3.0)
        ax.semilogy(n * 12 + k, res, color=C0)
        ax.axvline(n * 12, color=GREY, lw=0.8, ls=":")
        ax.text(n * 12 + 6, 6.0, rf"step $n{'+' + str(n) if n else ''}$", ha="center", fontsize=9)
    ax.axhline(10.0**-3, color=C1, ls="--", lw=1)
    ax.text(47, 10.0**-2.85, "subiteration tolerance", color=C1, ha="right", fontsize=9)
    ax.set_ylim(1e-4, 20)
    ax.set_xlabel(r"pseudo-time iterations (all physical steps)")
    ax.set_ylabel(r"unsteady residual $\|\mathbf{R}^*\|$")
    ax.set_title("Each physical step is a small steady-state problem (schematic)", fontsize=10)

    ax = axes[1]
    N = np.arange(8, 201)

    def amp1(n):
        z = 2j * np.pi / n
        return abs(1 / (1 - z)) ** n

    def amp2(n):
        z = 2j * np.pi / n
        r = np.roots([1.5 - z, -2, 0.5])
        return max(abs(r)) ** n

    ax.semilogx(N, [amp1(n) for n in N], color=GREY, label="BDF1 (backward Euler)")
    ax.semilogx(N, [amp2(n) for n in N], color=C0, label="BDF2")
    for n in (20, 50):
        a = amp2(n)
        ax.plot(n, a, "o", color=C0)
        ax.annotate(f"{a:.3f}", (n, a), textcoords="offset points", xytext=(6, -14), fontsize=9)
    ax.set_xlabel("physical time steps per period of the oscillation")
    ax.set_ylabel("amplitude left after one period")
    ax.set_ylim(0, 1.05)
    ax.set_title(r"Numerical damping of $u' = i\omega u$ (computed)", fontsize=10)
    ax.legend(frameon=False, loc="lower right")
    save(fig, "dual_time_stepping")


# ---------------------------------------------------------------------------
# Convergence diagnostics: residual vs heat-flux history (schematic) and a
# three-grid Richardson extrapolation (illustrative numbers).
# ---------------------------------------------------------------------------
def convergence_histories():
    fig, axes = plt.subplots(1, 3, figsize=(12.5, 3.6))
    it = np.linspace(0, 3000, 600)
    ax = axes[0]
    res = 10 ** (-it / 380.0)
    res = np.maximum(res, 1e-8)
    ax.semilogy(it, res, color=C0)
    ax.set_xlabel("iteration")
    ax.set_ylabel("density residual (relative)", color=C0)
    ax2 = ax.twinx()
    ax2.spines["right"].set_visible(True)
    q = 50 + 14 * np.exp(-it / 900.0) * np.cos(it / 260.0) + 6 * np.exp(-it / 1400.0)
    ax2.plot(it, q, color=C1)
    ax2.set_ylabel(r"stagnation heat flux (W/cm$^2$)", color=C1)
    ax2.grid(False)
    ax.axvline(1750, color=GREY, ls=":")
    ax.text(1780, 1e-1, "residual down\n5 orders;\n$q_w$ still moving", fontsize=8, color=GREY)
    ax.set_title("Residual converges before heat flux", fontsize=10)

    ax = axes[1]
    res2 = 10 ** (-np.minimum(it, 900) / 300.0) * (1 + 0.5 * np.sin(it / 9.0) * (it > 900))
    ax.semilogy(it, res2, color=C0)
    ax.set_xlabel("iteration")
    ax.set_ylabel("density residual (relative)")
    ax.text(1500, 4e-3, "stall after 3 orders:\nlimiter chatter or\nunsteady flow", fontsize=8, color=GREY)
    ax.set_ylim(1e-8, 2)
    ax.set_title("A limit cycle", fontsize=10)

    ax = axes[2]
    h = np.array([4.0, 2.0, 1.0])
    f = np.array([52.0, 50.8, 50.4])
    p = np.log((f[0] - f[1]) / (f[1] - f[2])) / np.log(2.0)
    fext = f[2] + (f[2] - f[1]) / (2.0**p - 1)
    hh = np.linspace(0, 4.2, 100)
    C = (f[2] - fext) / 1.0**p
    ax.plot(hh, fext + C * hh**p, color=GREY, lw=1)
    ax.plot(h, f, "o", color=C0, label="three grids")
    ax.plot(0, fext, "s", color=C1, label=f"Richardson: {fext:.1f}")
    ax.set_xlabel("relative grid spacing $h$ (fine = 1)")
    ax.set_ylabel(r"stagnation heat flux (W/cm$^2$)")
    ax.set_title(f"Grid convergence, observed order p = {p:.2f}\n(illustrative numbers)", fontsize=10)
    ax.legend(frameon=False)
    for a in (axes[0], axes[1]):
        a.text(0.02, 0.03, "schematic", transform=a.transAxes, fontsize=8, color=GREY)
    fig.tight_layout()
    save(fig, "convergence_histories")


# ---------------------------------------------------------------------------
# Finite-volume pipeline in 1-D: cell averages, limited reconstruction, the two
# states at a face and the single flux they produce.
# ---------------------------------------------------------------------------
def fv_stencil():
    q = np.array([1.0, 1.2, 2.0, 4.0, 4.4, 4.5])
    n = len(q)
    fig, ax = plt.subplots(figsize=(9.5, 3.9))
    slopes = np.zeros(n)
    for i in range(1, n - 1):
        slopes[i] = minmod(q[i] - q[i - 1], q[i + 1] - q[i])
    for i in range(n):
        ax.plot([i, i + 1], [q[i], q[i]], color=GREY, lw=1, ls=":")
        ax.plot([i, i + 1], [q[i] - 0.5 * slopes[i], q[i] + 0.5 * slopes[i]], color=C0, lw=2.2)
        ax.plot(i + 0.5, q[i], "o", color="k", ms=4)
        ax.axvline(i, color=GREY, lw=0.6)
    ax.axvline(n, color=GREY, lw=0.6)
    f = 3  # face between cells 2 and 3
    qL = q[f - 1] + 0.5 * slopes[f - 1]
    qR = q[f] - 0.5 * slopes[f]
    ax.axvline(f, color=C1, lw=1.6)
    ax.plot(f, qL, "s", color=C1, ms=7)
    ax.plot(f, qR, "s", color=C1, ms=7)
    ax.annotate(rf"$q_L = {qL:.1f}$", (f, qL), textcoords="offset points", xytext=(-12, 8), ha="right", color=C1)
    ax.annotate(rf"$q_R = {qR:.1f}$", (f, qR), textcoords="offset points", xytext=(12, -16), ha="left", color=C1)
    ax.annotate("", xy=(f + 0.45, 0.45), xytext=(f - 0.45, 0.45), arrowprops=dict(arrowstyle="-|>", color=C1, lw=2))
    ax.text(f, 0.15, r"one flux $\hat F(q_L, q_R)$: leaves cell $i$, enters cell $i{+}1$", ha="center", color=C1, fontsize=9)
    names = [r"$i-2$", r"$i-1$", r"$i$", r"$i+1$", r"$i+2$", r"$i+3$"]
    for i in range(n):
        ax.text(i + 0.5, 5.15, names[i], ha="center", fontsize=9)
    ax.text(f + 0.06, 4.75, r"face $i+\frac{1}{2}$", ha="left", color=C1, fontsize=9)
    ax.plot([], [], "o", color="k", ms=4, label="cell average (what is stored)")
    ax.plot([], [], color=C0, lw=2.2, label="limited linear reconstruction (minmod)")
    ax.plot([], [], "s", color=C1, ms=7, label="left and right states at the face")
    ax.legend(frameon=False, fontsize=8, loc="upper left", bbox_to_anchor=(0.0, 0.9))
    ax.set_xlim(0, n)
    ax.set_ylim(0, 5.5)
    ax.set_xticks([])
    ax.set_ylabel("a primitive variable $q$")
    ax.grid(False)
    save(fig, "fv_stencil")


# ---------------------------------------------------------------------------
# Discretization families: cell-centred vs vertex-based control volumes, and a
# hybrid grid with extruded wall layers (schematic).
# ---------------------------------------------------------------------------
def discretization_families():
    import matplotlib.tri as mtri
    from matplotlib.patches import Polygon

    rng = np.random.default_rng(4)
    xs, ys = np.meshgrid(np.arange(5.0), np.arange(5.0))
    xs = xs + 0.5 * (np.arange(5)[:, None] % 2)
    pts = np.c_[xs.ravel(), ys.ravel() * 0.87]
    pts += rng.normal(0, 0.06, pts.shape)
    tri = mtri.Triangulation(pts[:, 0], pts[:, 1])
    cent = pts[tri.triangles].mean(axis=1)

    fig, axes = plt.subplots(1, 3, figsize=(12, 3.9))
    for ax, title in zip(axes[:2], ("Cell-centred: the cell is the control volume", "Vertex-based: a dual cell around each node")):
        ax.triplot(tri, color=GREY, lw=0.8)
        ax.set_aspect("equal")
        ax.axis("off")
        ax.set_title(title, fontsize=10)
        ax.set_xlim(0.6, 4.0)
        ax.set_ylim(0.0, 3.1)
    ax = axes[0]
    target = np.argmin(np.hypot(cent[:, 0] - 2.4, cent[:, 1] - 1.6))
    ax.add_patch(Polygon(pts[tri.triangles[target]], fc=C0, alpha=0.3, ec=C0, lw=2))
    ax.plot(cent[:, 0], cent[:, 1], "o", color=C0, ms=4)
    ax.text(2.3, 0.12, "unknowns at cell centroids\none flux per mesh face", ha="center", fontsize=9, color=C0, bbox=dict(fc="white", ec="none", pad=3))
    ax = axes[1]
    node = np.argmin(np.hypot(pts[:, 0] - 2.4, pts[:, 1] - 1.75))
    around = [t for t in range(len(tri.triangles)) if node in tri.triangles[t]]
    ang = np.arctan2(cent[around, 1] - pts[node, 1], cent[around, 0] - pts[node, 0])
    around = [around[k] for k in np.argsort(ang)]
    poly = []
    for a, b in zip(around, around[1:] + around[:1]):
        poly.append(cent[a])
        shared = (set(tri.triangles[a]) & set(tri.triangles[b])) - {node}
        if shared:
            other = shared.pop()
            poly.append(0.5 * (pts[node] + pts[other]))
    ax.add_patch(Polygon(np.array(poly), fc=C1, alpha=0.3, ec=C1, lw=2))
    ax.plot(pts[:, 0], pts[:, 1], "o", color=C1, ms=4)
    ax.text(2.3, 0.12, "unknowns at nodes\none flux per mesh edge", ha="center", fontsize=9, color=C1, bbox=dict(fc="white", ec="none", pad=3))

    ax = axes[2]
    xw = np.linspace(0, 4, 13)
    wall = 0.25 * np.sin(xw * 0.8)
    heights = np.cumsum(0.07 * 1.45 ** np.arange(7))
    for h in np.r_[0, heights]:
        ax.plot(xw, wall + h, color=C0, lw=0.8)
    for k in range(len(xw)):
        ax.plot([xw[k], xw[k]], [wall[k], wall[k] + heights[-1]], color=C0, lw=0.8)
    ax.plot([xw[6], xw[6]], [wall[6], wall[6] + heights[-1]], color=C1, lw=2.6)
    ax.text(xw[6] + 0.08, wall[6] + heights[-1] * 0.5, "implicit line", color=C1, fontsize=9, rotation=90, va="center")
    top = np.c_[xw, wall + heights[-1]]
    outer = np.c_[np.linspace(0, 4, 9), np.full(9, 2.9)]
    mid = np.c_[np.linspace(0.2, 3.8, 8), np.full(8, 2.25) + rng.normal(0, 0.05, 8)]
    allp = np.vstack([top, mid, outer])
    t2 = mtri.Triangulation(allp[:, 0], allp[:, 1])
    mask = allp[t2.triangles][:, :, 1].mean(axis=1) < (0.25 * np.sin(allp[t2.triangles][:, :, 0].mean(axis=1) * 0.8) + heights[-1])
    t2.set_mask(mask)
    ax.triplot(t2, color=GREY, lw=0.8)
    ax.fill_between(xw, wall - 0.3, wall, color="#bcaaa4")
    ax.text(2, -0.42, "wall", ha="center", fontsize=9)
    ax.set_xlim(0, 4)
    ax.set_ylim(-0.6, 2.95)
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_title("Hybrid grid: extruded layers at the wall,\ntetrahedra (triangles here) away from it", fontsize=10)
    fig.text(0.5, 0.0, "schematic, 2-D", ha="center", fontsize=8, color=GREY)
    save(fig, "discretization_families")


# ---------------------------------------------------------------------------
# Viscous face gradient on a skewed cell pair: direct difference along the
# centroid line plus the tangential part of the averaged gradient (schematic).
# ---------------------------------------------------------------------------
def viscous_face_gradient():
    from matplotlib.patches import Polygon

    fig, axes = plt.subplots(1, 2, figsize=(10.5, 3.7), gridspec_kw={"width_ratios": [1.25, 1]})
    ax = axes[0]
    Lc = np.array([[0, 0], [2.0, 0.2], [2.3, 1.5], [0.2, 1.3]])
    Rc = np.array([[2.0, 0.2], [4.3, 0.7], [4.5, 2.1], [2.3, 1.5]])
    ax.add_patch(Polygon(Lc, fc=C0, alpha=0.12, ec=GREY))
    ax.add_patch(Polygon(Rc, fc=C2, alpha=0.12, ec=GREY))
    cL, cR = Lc.mean(axis=0), Rc.mean(axis=0)
    fm = 0.5 * (Lc[1] + Lc[2])
    tvec = (Lc[2] - Lc[1]) / np.linalg.norm(Lc[2] - Lc[1])
    nvec = np.array([tvec[1], -tvec[0]])
    ax.plot(*np.c_[Lc[1], Lc[2]], color="k", lw=2.5)
    ax.plot(*cL, "o", color=C0)
    ax.plot(*cR, "o", color=C2)
    ax.text(cL[0] - 0.1, cL[1] - 0.22, r"$\phi_L$", color=C0, ha="right")
    ax.text(cR[0] + 0.1, cR[1] + 0.12, r"$\phi_R$", color=C2)
    ax.annotate("", xy=cR, xytext=cL, arrowprops=dict(arrowstyle="-|>", color=C1, lw=2))
    ax.text(0.5 * (cL[0] + cR[0]) - 0.75, 0.5 * (cL[1] + cR[1]) + 0.12, r"$\hat{\mathbf{e}}$, length $\Delta\ell$", color=C1)
    ax.annotate("", xy=fm + 0.9 * nvec, xytext=fm, arrowprops=dict(arrowstyle="-|>", color="k", lw=2))
    ax.text(*(fm + 0.98 * nvec + [0.0, -0.18]), r"$\hat{\mathbf{n}}$")
    ax.annotate("", xy=fm + 0.7 * tvec, xytext=fm, arrowprops=dict(arrowstyle="-|>", color=C3, lw=2))
    ax.text(*(fm + 0.75 * tvec + [0.08, 0.0]), "tangential part:\nfrom averaged\ncell gradients", color=C3, fontsize=8, va="center")
    ax.text(1.2, -0.35, r"normal part: direct difference $(\phi_R - \phi_L)/\Delta\ell$", color=C1, fontsize=9, ha="left")
    ax.set_xlim(-0.2, 5.4)
    ax.set_ylim(-0.6, 2.5)
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_title("Face gradient on a skewed cell pair (schematic)", fontsize=10)

    ax = axes[1]
    y = np.linspace(0, 1, 300)
    T = 300 + 5700 * (1 - np.exp(-y / 0.12))
    ax.plot(T, y, color=C0)
    for dn, col, lab in ((0.30, C1, "coarse first cell"), (0.04, C2, "fine first cell")):
        Tc = 300 + 5700 * (1 - np.exp(-(dn / 2) / 0.12))
        ax.plot([300, Tc], [0, dn / 2], "o-", color=col, ms=4, label=f"{lab}: slope {((Tc - 300) / (dn / 2)) / (5700 / 0.12):.2f} of exact")
        ax.axhline(dn, color=col, lw=0.6, ls=":")
    ax.axhline(0, color="k", lw=3)
    ax.set_xlabel("temperature (K)")
    ax.set_ylabel("distance from wall / boundary-layer thickness")
    ax.set_ylim(-0.01, 0.45)
    ax.set_title("One-sided wall gradient vs first-cell height\n(illustrative exponential profile)", fontsize=10)
    ax.legend(frameon=False, fontsize=8, loc="lower right")
    save(fig, "viscous_face_gradient")


# ---------------------------------------------------------------------------
# WENO5: the three candidate stencils for one face, and the nonlinear weights
# near a discontinuity (computed with the Jiang-Shu weights).
# ---------------------------------------------------------------------------
def weno_stencils():
    fig, axes = plt.subplots(1, 2, figsize=(11, 3.8), gridspec_kw={"width_ratios": [1, 1.15]})
    ax = axes[0]
    names = [r"$i-2$", r"$i-1$", r"$i$", r"$i+1$", r"$i+2$"]
    for k, nm in enumerate(names):
        ax.add_patch(plt.Rectangle((k, 0), 1, 0.5, fc="white", ec=GREY))
        ax.text(k + 0.5, 0.25, nm, ha="center", va="center", fontsize=9)
    ax.axvline(3, ymin=0.0, ymax=0.95, color=C1, lw=2)
    ax.text(3.1, 2.55, r"face $i+\frac{1}{2}$", ha="left", color=C1, fontsize=9)
    for s, (a, b), col, d in zip(range(3), ((0, 3), (1, 4), (2, 5)), (C0, C2, C3), ("0.1", "0.6", "0.3")):
        yb = 0.8 + 0.5 * s
        ax.plot([a + 0.1, b - 0.1], [yb, yb], color=col, lw=6, solid_capstyle="butt", alpha=0.8)
        ax.text(b + 0.05 if b < 5 else a - 0.05, yb, rf"$S_{s}$, ideal weight {d}", color=col, va="center", ha="left" if b < 5 else "right", fontsize=9)
    ax.set_xlim(-2.2, 6.6)
    ax.set_ylim(-0.1, 2.8)
    ax.axis("off")
    ax.set_title("Three 3-cell stencils, each giving a value at the face", fontsize=10)

    ax = axes[1]
    N = 24
    x = np.arange(N) + 0.5
    q = np.where(x < 12, 1.0, 0.0) + 0.15 * np.sin(2 * np.pi * x / N)
    eps = 1e-6
    d = np.array([0.1, 0.6, 0.3])
    W = np.full((N, 3), np.nan)
    for i in range(2, N - 2):
        a, b, c, dd, e = q[i - 2 : i + 3]
        beta = np.array([
            13 / 12 * (a - 2 * b + c) ** 2 + 0.25 * (a - 4 * b + 3 * c) ** 2,
            13 / 12 * (b - 2 * c + dd) ** 2 + 0.25 * (b - dd) ** 2,
            13 / 12 * (c - 2 * dd + e) ** 2 + 0.25 * (3 * c - 4 * dd + e) ** 2,
        ])
        al = d / (eps + beta) ** 2
        W[i] = al / al.sum()
    for s, col in zip(range(3), (C0, C2, C3)):
        ax.plot(x, W[:, s], "o-", color=col, ms=3.5, label=rf"$\omega_{s}$")
        ax.axhline(d[s], color=col, lw=0.7, ls=":")
    ax2 = ax.twinx()
    ax2.step(np.arange(N + 1), np.r_[q, q[-1]], where="post", color=GREY, lw=1)
    ax2.set_ylabel("cell averages", color=GREY)
    ax2.grid(False)
    ax2.spines["right"].set_visible(True)
    ax.set_xlabel("cell index")
    ax.set_ylabel("nonlinear weight")
    ax.set_ylim(-0.03, 1.03)
    ax.set_title("Weights go to the ideal values in smooth data and\ndrop stencils that cross the jump (computed, WENO-JS)", fontsize=10)
    ax.legend(frameon=False, fontsize=8, loc="center left")
    save(fig, "weno_stencils")


# ---------------------------------------------------------------------------
# Central schemes: the JST pressure sensor on a 1-D profile, and the Ducros
# sensor as a function of vorticity over dilatation (both computed).
# ---------------------------------------------------------------------------
def jst_ducros_sensors():
    fig, axes = plt.subplots(1, 2, figsize=(11, 3.7))
    ax = axes[0]
    N = 80
    x = (np.arange(N) + 0.5) / N
    p = 1 + 0.08 * np.sin(2 * np.pi * x * 3) * (x < 0.55) + 4.0 * 0.5 * (1 + np.tanh((x - 0.7) / 0.012))
    nu = np.zeros(N)
    nu[1:-1] = np.abs(p[2:] - 2 * p[1:-1] + p[:-2]) / (p[2:] + 2 * p[1:-1] + p[:-2])
    k2, k4 = 0.5, 1 / 64
    numax = np.maximum(nu, np.maximum(np.roll(nu, 1), np.roll(nu, -1)))
    e2 = k2 * numax
    e4 = np.maximum(0, k4 - e2)
    ax.plot(x, p, color=GREY, lw=1.2)
    ax.set_ylabel("pressure (arbitrary units)", color=GREY)
    ax.set_xlabel("x")
    ax2 = ax.twinx()
    ax2.spines["right"].set_visible(True)
    ax2.semilogy(x, np.maximum(e2, 1e-5), color=C1, label=r"$\varepsilon^{(2)}$ (second difference)")
    ax2.semilogy(x, np.maximum(e4, 1e-5), color=C0, label=r"$\varepsilon^{(4)}$ (fourth difference)")
    ax2.set_ylim(1e-5, 1)
    ax2.set_ylabel("dissipation coefficient")
    ax2.grid(False)
    ax2.legend(frameon=False, fontsize=8, loc="upper left")
    ax.set_title(r"JST switch, $k^{(2)} = 1/2$, $k^{(4)} = 1/64$ (computed)", fontsize=10)

    ax = axes[1]
    r = np.logspace(-2, 2, 300)
    ax.semilogx(r, 1 / (1 + r**2), color=C0)
    ax.axvspan(1e-2, 0.2, color=C1, alpha=0.08)
    ax.axvspan(5, 1e2, color=C2, alpha=0.08)
    ax.text(0.045, 0.45, "shock:\ndilatation\ndominates,\ndissipation on", ha="center", fontsize=9, color=C1)
    ax.text(22, 0.45, "vortex or\nshear layer:\ndissipation off", ha="center", fontsize=9, color=C2)
    ax.set_xlabel(r"vorticity / dilatation, $|\nabla\times\mathbf{u}|\,/\,|\nabla\cdot\mathbf{u}|$")
    ax.set_ylabel(r"Ducros sensor $\alpha_{diss}$")
    ax.set_title("Ducros sensor (computed from its definition)", fontsize=10)
    fig.tight_layout()
    save(fig, "jst_ducros_sensors")


# ---------------------------------------------------------------------------
# Low-Mach corrections: the factor each correction applies to the acoustic
# dissipation, against local face-normal Mach number (computed).
# ---------------------------------------------------------------------------
def low_mach_scaling():
    fig, axes = plt.subplots(1, 2, figsize=(10.5, 3.7))
    M = np.logspace(-3, 0.3, 400)
    ax = axes[0]
    ax.loglog(M, 1 / M, color=GREY, label="uncorrected upwind flux")
    ax.loglog(M, np.minimum(5.0, 1 / M), color=C0, label=r"Roe-M, $\phi = 5$")
    ax.set_xlabel("local face-normal Mach number")
    ax.set_ylabel("acoustic dissipation / advective dissipation")
    ax.set_title(r"The imbalance: $c/|u| = 1/M$", fontsize=10)
    ax.legend(frameon=False, fontsize=8)

    ax = axes[1]
    ax.semilogx(M, np.ones_like(M), color=GREY, label="uncorrected")
    ax.semilogx(M, np.minimum(5 * M, 1), color=C0, label=r"Roe-M: $\min(\phi M, 1)$, $\phi = 5$")
    ax.semilogx(M, np.sin(np.minimum(1, M / 0.1) * np.pi / 2), color=C1, label=r"HLLC-LM: $\sin(\min(1, M/0.1)\,\pi/2)$")
    ax.semilogx(M, np.minimum(M, 1), color=C2, label=r"Thornber: $z = \min(M, 1)$")
    ax.set_xlabel("local face-normal Mach number")
    ax.set_ylabel("factor on the acoustic dissipation")
    ax.set_title("What each correction does to it", fontsize=10)
    ax.legend(frameon=False, fontsize=8, loc="center left")
    save(fig, "low_mach_scaling")


# ---------------------------------------------------------------------------
# The carbuncle (schematic).
# ---------------------------------------------------------------------------
def carbuncle_schematic():
    fig, axes = plt.subplots(1, 2, figsize=(9.5, 4.0))
    th = np.linspace(-np.pi / 2, np.pi / 2, 200)
    for ax, bad in zip(axes, (False, True)):
        ax.fill(np.cos(np.pi - th) * 1.0, np.sin(np.pi - th) * 1.0, color="#bcaaa4")
        ax.fill_betweenx([-1, 1], 0, 0.8, color="#bcaaa4")
        y = np.linspace(-1.9, 1.9, 400)
        xs = -1.38 - 0.0 * y + 0.33 * y**2
        if bad:
            xs = xs - 0.55 * np.exp(-((y / 0.22) ** 2))
        ax.plot(xs, y, color=C0, lw=2.2)
        for yy in np.linspace(-1.7, 1.7, 9):
            ax.annotate("", xy=(-2.25, yy), xytext=(-2.9, yy), arrowprops=dict(arrowstyle="->", color=GREY, lw=1))
        ax.plot([-2.9, -1.0], [0, 0], color=GREY, lw=0.8, ls=":")
        if bad:
            t = np.linspace(0, 2 * np.pi, 60)
            for s in (1, -1):
                ax.plot(-1.45 + 0.2 * np.cos(t), s * 0.17 + 0.11 * np.sin(t), color=C1, lw=1)
            ax.annotate("spurious protrusion\non the stagnation line", xy=(-1.9, 0.05), xytext=(-2.9, 1.25),
                        arrowprops=dict(arrowstyle="->", color=C1), color=C1, fontsize=9)
            ax.text(-1.45, -0.5, "spurious\nrecirculation", color=C1, fontsize=8, ha="center", va="top")
            ax.set_title("Carbuncle: converged, plausible, wrong", fontsize=10)
        else:
            ax.text(-2.1, 1.75, "bow shock", color=C0, fontsize=9)
            ax.set_title("Correct solution", fontsize=10)
        ax.set_xlim(-3.0, 0.6)
        ax.set_ylim(-2, 2)
        ax.set_aspect("equal")
        ax.axis("off")
    fig.text(0.5, 0.02, "schematic, not to scale", ha="center", fontsize=8, color=GREY)
    save(fig, "carbuncle_schematic")


# ---------------------------------------------------------------------------
# Stiff sources: explicit vs implicit Euler on a relaxation equation (computed).
# ---------------------------------------------------------------------------
def stiff_relaxation():
    fig, axes = plt.subplots(1, 2, figsize=(10.5, 3.7))
    ax = axes[0]
    t = np.linspace(0, 8, 400)
    ax.plot(t, np.exp(-t), color="k", lw=1.2, label="exact")
    for r, col in ((0.5, C2), (1.5, C0), (2.5, C1)):
        n = int(8 / r) + 1
        tt = np.arange(n + 1) * r
        y = (1 - r) ** np.arange(n + 1)
        ax.plot(tt, y, "o-", color=col, ms=3.5, label=rf"explicit, $\Delta t/\tau = {r}$")
    ax.set_ylim(-3, 3)
    ax.set_xlim(0, 8)
    ax.set_xlabel(r"time / $\tau$")
    ax.set_ylabel(r"$(y - y_{eq})/(y_0 - y_{eq})$")
    ax.set_title("Explicit Euler: oscillates above 1, diverges above 2", fontsize=10)
    ax.legend(frameon=False, fontsize=8, loc="lower left")

    ax = axes[1]
    ax.plot(t, np.exp(-t), color="k", lw=1.2, label="exact")
    for r, col in ((0.5, C2), (2.5, C1), (8.0, C3)):
        n = int(8 / r) + 1
        tt = np.arange(n + 1) * r
        y = (1 / (1 + r)) ** np.arange(n + 1)
        ax.plot(tt, y, "o-", color=col, ms=3.5, label=rf"implicit, $\Delta t/\tau = {r}$")
    ax.set_ylim(-0.1, 1.05)
    ax.set_xlim(0, 8)
    ax.set_xlabel(r"time / $\tau$")
    ax.set_title("Implicit Euler: stable at any step, relaxes to equilibrium", fontsize=10)
    ax.legend(frameon=False, fontsize=8)
    fig.suptitle(r"Model source term $dy/dt = -(y - y_{eq})/\tau$ (computed)", fontsize=10, y=1.02)
    save(fig, "stiff_relaxation")


# ---------------------------------------------------------------------------
# Implicit methods: block sparsity of the Jacobian on a small structured grid,
# ordered along wall-normal lines (computed pattern).
# ---------------------------------------------------------------------------
def implicit_sparsity():
    ni, nj = 5, 6  # i along the wall, j wall-normal; unknown index = i*nj + j
    n = ni * nj
    A = np.zeros((n, n))
    for i in range(ni):
        for j in range(nj):
            k = i * nj + j
            A[k, k] = 3
            if j > 0:
                A[k, k - 1] = 2
            if j < nj - 1:
                A[k, k + 1] = 2
            if i > 0:
                A[k, k - nj] = 1
            if i < ni - 1:
                A[k, k + nj] = 1
    from matplotlib.colors import ListedColormap

    fig, axes = plt.subplots(1, 2, figsize=(10.5, 4.3), gridspec_kw={"width_ratios": [1.15, 1]})
    ax = axes[0]
    ax.imshow(A, cmap=ListedColormap(["white", C2, C0, "k"]), interpolation="nearest")
    for i in range(1, ni):
        ax.axhline(i * nj - 0.5, color=GREY, lw=0.5)
        ax.axvline(i * nj - 0.5, color=GREY, lw=0.5)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.grid(False)
    ax.set_title(f"Jacobian of a {ni}×{nj} grid: each square is an $n_e\\times n_e$ block", fontsize=10)
    ax.plot([], [], "s", color="k", label="diagonal block (cell itself, sources)")
    ax.plot([], [], "s", color=C0, label="wall-normal neighbours: kept by line relaxation")
    ax.plot([], [], "s", color=C2, label="neighbouring lines: moved to the right-hand side")
    ax.legend(frameon=False, fontsize=8, loc="upper center", bbox_to_anchor=(0.5, -0.02))

    ax = axes[1]
    ne = np.arange(5, 21)
    ax.plot(ne, (ne / 5.0) ** 2, "o-", color=C0, ms=3.5, label=r"storage per block, $n_e^2$")
    ax.plot(ne, (ne / 5.0) ** 3, "o-", color=C1, ms=3.5, label=r"block factorization, $n_e^3$")
    ax.plot(ne, ne / 5.0, "o-", color=GREY, ms=3.5, label=r"explicit residual, $\sim n_e$")
    ax.axvline(16, color=GREY, ls=":")
    ax.text(16.2, 48, "11-species\n2T air", fontsize=8, color=GREY)
    ax.annotate("33×", (16, (16 / 5) ** 3), textcoords="offset points", xytext=(-26, 2), color=C1, fontsize=9)
    ax.annotate("10×", (16, (16 / 5) ** 2), textcoords="offset points", xytext=(-26, 2), color=C0, fontsize=9)
    ax.set_xlabel(r"equations per cell, $n_e$")
    ax.set_ylabel("cost relative to a 5-equation perfect gas")
    ax.set_title("Cost growth with the gas model (computed)", fontsize=10)
    ax.legend(frameon=False, fontsize=8)
    save(fig, "implicit_sparsity")


# ---------------------------------------------------------------------------
# Local time stepping: the local step across a stretched wall-normal grid.
# ---------------------------------------------------------------------------
def local_time_steps():
    fig, ax = plt.subplots(figsize=(7.2, 3.8))
    n = 60
    dy = 1e-6 * 1.2 ** np.arange(n)
    y = np.cumsum(dy) - dy / 2
    a, nu = 1.0e3, 3.0e-3  # illustrative |u|+a and kinematic viscosity
    dt = 1.0 / (a / dy + 2 * nu / dy**2)
    ax.loglog(y, dt, color=C0, label="local time step of each cell")
    ax.axhline(dt.min(), color=C1, ls="--", label="global step = smallest local step")
    ax.fill_between(y, dt.min(), dt, color=C0, alpha=0.08)
    ax.annotate(f"ratio {dt.max() / dt.min():.0e}", (y[-1], dt[-1]), textcoords="offset points", xytext=(-70, -6), fontsize=9, color=C0)
    ax.set_xlabel("distance from wall (m)")
    ax.set_ylabel("allowed explicit time step (s)")
    ax.set_title("Wall-normal line of 60 cells, first cell 1 µm, growth 1.2\n(illustrative shock-layer values)", fontsize=10)
    ax.legend(frameon=False, fontsize=8, loc="upper left")
    save(fig, "local_time_steps")


if __name__ == "__main__":
    burgers_demo()
    timestep_limits()
    minmod_reconstruction()
    cost_crossover()
    morse_well()
    arrhenius_switch()
    blunt_body()
    vib_energy()
    sweby_limiters()
    dplr_lines()
    dplr_vs_dplur()
    msw_pressure_weight()
    eigenvalue_limiter()
    virtual_upwind_point()
    double_cone_schematic()
    riemann_face_and_fan()
    riemann_fans_compare()
    entropy_fix_burgers()
    capsule_anatomy()
    sutton_graves_map()
    shock_limits_newtonian()
    knudsen_regimes()
    plasma_frequency_bands()
    physics_ladder()
    bc_characteristics()
    wall_bc_thermal_catalytic()
    surface_energy_balance()
    rk_stability_regions()
    dual_time_stepping()
    convergence_histories()
    fv_stencil()
    discretization_families()
    viscous_face_gradient()
    weno_stencils()
    jst_ducros_sensors()
    low_mach_scaling()
    carbuncle_schematic()
    stiff_relaxation()
    implicit_sparsity()
    local_time_steps()
