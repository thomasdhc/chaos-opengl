"""Plot logistic-map period doubling and periodic windows within chaos."""

import argparse
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np


R_INFINITY = 3.569945672  # Approximation; do not resolve distances near its precision.
SPLITS = (
    (3.5440903596, "4 → 8"),
    (3.5644072661, "8 → 16"),
    (3.5687594195, "16 → 32"),
    (3.5696916098, "32 → 64"),
    (3.5698912580, "64 → 128"),
)
DEFAULT_OUTPUT = Path(__file__).resolve().parents[1] / "docs/graphs/bifurcation_zooms.png"


def distance_coordinate(r):
    """Increase rightwards as r approaches R_INFINITY from below."""
    r = np.asarray(r, dtype=float)
    if np.any(r >= R_INFINITY):
        raise ValueError("The log-distance view requires r < R_INFINITY")
    return -np.log10(R_INFINITY - r)


def sample_attractor(r, burn_in=20000, iterations=512):
    """Discard transients independently at each r, then retain orbit samples."""
    r = np.asarray(r, dtype=float)
    if r.ndim != 1 or not np.all(np.isfinite(r)) or np.any((r < 0) | (r > 4)):
        raise ValueError("r must be a finite one-dimensional array in [0, 4]")
    if burn_in < 0 or iterations < 1:
        raise ValueError("burn_in must be nonnegative and iterations positive")
    x = np.full(r.shape, 0.123456789, dtype=float)
    for _ in range(burn_in):
        x = r * x * (1 - x)
    populations = np.empty((iterations, r.size))
    for i in range(iterations):
        x = r * x * (1 - x)
        populations[i] = x
    return populations


def plot_diagram(output=DEFAULT_OUTPUT, samples=6000, burn_in=20000, iterations=512):
    if samples < 2:
        raise ValueError("samples must be at least 2")
    fig, axes = plt.subplots(2, 2, figsize=(15, 11), layout="constrained")
    axes = axes.ravel()
    linear_r = np.linspace(3.5, 3.6, samples)
    # Uniform screen-space sampling supplies increasing r resolution near chaos.
    distances = np.geomspace(R_INFINITY - 3.5, 1e-5, samples)
    log_r = R_INFINITY - distances
    log_positions = distance_coordinate(log_r)

    chaotic_r = np.linspace(3.6, 4.0, samples)
    window_r = np.linspace(3.82, 3.86, samples)

    for ax, r, positions in zip(
        axes,
        (linear_r, log_r, chaotic_r, window_r),
        (linear_r, log_positions, chaotic_r, window_r),
    ):
        populations = sample_attractor(r, burn_in, iterations)
        ax.scatter(
            np.tile(positions, iterations), populations.ravel(),
            s=0.06, color="black", alpha=0.25, linewidths=0, rasterized=True,
        )
        ax.set_ylabel("Long-run population x")
        ax.grid(alpha=0.15)
        ax.set_axisbelow(True)
        ax.set_xlim(positions[0], positions[-1])

    axes[0].set(
        title="Linear r: period doubling into chaos",
        xlabel="Growth rate r", ylim=(0.3, 0.92),
    )
    axes[1].set(
        title="Log distance to chaos: lowest population branch",
        xlabel="Growth rate r (position = −log₁₀(r∞ − r))", ylim=(0.34, 0.39),
    )
    ticks = np.array([3.5, 3.54, 3.56, 3.568, 3.5695, 3.5699, 3.56993])
    axes[1].set_xticks(distance_coordinate(ticks), [f"{r:g}" for r in ticks])
    axes[1].tick_params(axis="x", labelsize=9, rotation=30)
    for r, label in SPLITS:
        for ax, position in zip(axes, (r, distance_coordinate(r))):
            ax.axvline(position, color="#286a9b", lw=0.7, alpha=0.5)
        axes[1].text(
            distance_coordinate(r), 1.01, label, transform=axes[1].get_xaxis_transform(),
            ha="center", va="bottom", fontsize=8, color="#286a9b",
        )
    axes[1].set_title(axes[1].get_title(), pad=25)
    axes[2].set(
        title="Periodic windows within chaos (shaded region enlarged at right)",
        xlabel="Growth rate r", ylim=(0, 1),
    )
    axes[2].axvspan(3.82, 3.86, color="#286a9b", alpha=0.12)
    axes[3].set(
        title="Period-3 window and its period-doubling cascade",
        xlabel="Growth rate r", ylim=(0, 1),
    )
    axes[3].set_title(axes[3].get_title(), pad=25)
    for r, label in ((1 + np.sqrt(8), "3-cycle begins"), (3.8414990075, "3 → 6")):
        axes[3].axvline(r, color="#286a9b", lw=0.8, ls="--")
        axes[3].text(
            r, 1.01, label, transform=axes[3].get_xaxis_transform(),
            ha="center", va="bottom", fontsize=8, color="#286a9b",
        )
    fig.suptitle(
        "Logistic map · xₙ₊₁ = r xₙ (1 − xₙ)\n"
        f"r∞ ≈ {R_INFINITY} · {burn_in:,} settling steps + {iterations:,} retained per r",
        fontsize=13,
    )
    output = Path(output)
    output.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output, dpi=200)
    plt.close(fig)
    return output


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--samples", type=int, default=6000, help="r samples per panel")
    parser.add_argument("--burn-in", type=int, default=20000)
    parser.add_argument("--iterations", type=int, default=512)
    args = parser.parse_args()
    print(plot_diagram(args.output, args.samples, args.burn_in, args.iterations))


if __name__ == "__main__":
    main()
