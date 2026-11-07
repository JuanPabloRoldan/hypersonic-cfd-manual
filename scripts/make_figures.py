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


if __name__ == "__main__":
    burgers_demo()
    timestep_limits()
    minmod_reconstruction()
    cost_crossover()
    morse_well()
    arrhenius_switch()
    blunt_body()
    vib_energy()
