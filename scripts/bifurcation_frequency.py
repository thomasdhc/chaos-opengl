"""Color the full bifurcation diagram by population-bin visitation frequency."""

import argparse
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
from matplotlib.colors import LogNorm
import matplotlib.pyplot as plt
import numpy as np

from bifurcation import INITIAL_POPULATION
from population_distribution import BIN_EDGES, STEPS


R_MIN = 2.4
R_MAX = 4.0
R_SAMPLES = 4000
BURN_IN = 20000
DISPLAY_BINS = 1000
DEFAULT_OUTPUT = Path(__file__).resolve().parents[1] / "docs/graphs/bifurcation_frequency.png"


def population_counts(rates, burn_in=BURN_IN, steps=STEPS):
    """Accumulate fine population bins while retaining a bounded history size."""
    rates = np.asarray(rates, dtype=float)
    x = np.full(rates.shape, INITIAL_POPULATION)
    for _ in range(burn_in):
        x = rates * x * (1 - x)
    counts = np.zeros((rates.size, DISPLAY_BINS), dtype=np.int32)
    columns = np.arange(rates.size)
    for _ in range(steps):
        x = rates * x * (1 - x)
        bins = np.minimum((x * DISPLAY_BINS).astype(int), DISPLAY_BINS - 1)
        counts[columns, bins] += 1
    return counts


def frequency_colors(counts, steps=STEPS):
    """Color occupied fine bins by the frequency of their enclosing 0.01 bin."""
    frequency_bins = BIN_EDGES.size - 1
    fine_bins_per_bin = DISPLAY_BINS // frequency_bins
    coarse = counts.reshape(counts.shape[0], frequency_bins, fine_bins_per_bin).sum(axis=2)
    percentages = coarse * (100 / steps)
    colors = np.repeat(percentages, fine_bins_per_bin, axis=1)
    return np.ma.masked_where(counts == 0, colors)


def plot_diagram(output=DEFAULT_OUTPUT):
    rates = np.linspace(R_MIN, R_MAX, R_SAMPLES)
    colors = frequency_colors(population_counts(rates))
    cmap = plt.colormaps["RdYlGn"].copy()
    cmap.set_bad("white")
    fig, ax = plt.subplots(figsize=(14, 7), layout="constrained")
    image = ax.imshow(
        colors.T, origin="lower", extent=(R_MIN, R_MAX, 0, 1), aspect="auto",
        interpolation="nearest", cmap=cmap, norm=LogNorm(vmin=100 / STEPS, vmax=100),
    )
    ax.set(
        title="Frequency-colored bifurcation diagram\n"
              f"{BURN_IN:,} settling steps + {STEPS:,} retained per r · x₀ = {INITIAL_POPULATION}",
        xlabel="Growth rate r", ylabel="Long-run population x",
    )
    colorbar = fig.colorbar(image, ax=ax, pad=0.02)
    colorbar.set_ticks([0.01, 0.1, 1, 10, 100], labels=["0.01%", "0.1%", "1%", "10%", "100%"])
    colorbar.set_label("Samples per 0.01-wide population bin (log color scale)")
    output = Path(output)
    output.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output, dpi=200)
    plt.close(fig)
    return output


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    print(plot_diagram(args.output))


if __name__ == "__main__":
    main()
