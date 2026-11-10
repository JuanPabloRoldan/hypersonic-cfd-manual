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
