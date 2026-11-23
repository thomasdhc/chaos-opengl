"""Plot population frequencies over the first 20,060 steps at r = 3.828."""

import argparse
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from bifurcation import INITIAL_POPULATION, sample_attractor


GROWTH_RATE = 3.828
STEPS = 20060
BIN_EDGES = np.linspace(0, 1, 101)
DEFAULT_OUTPUT = Path(__file__).resolve().parents[1] / "docs/graphs/population_distribution_r3_828.png"


def plot_distribution(output=DEFAULT_OUTPUT):
    populations = sample_attractor(np.array([GROWTH_RATE]), burn_in=0, iterations=STEPS)[:, 0]
    fig, ax = plt.subplots(figsize=(10, 5), layout="constrained")
    ax.hist(
        populations, bins=BIN_EDGES, weights=np.full(STEPS, 100 / STEPS),
        color="#555555", edgecolor="white", linewidth=0.4,
    )
    ax.set(
        title=f"Population distribution · r = {GROWTH_RATE}\n"
              f"Steps 1–{STEPS:,} · x₀ = {INITIAL_POPULATION} · bin width 0.01",
        xlabel="Population x", ylabel="Sampled steps per bin (%)", xlim=(0, 1),
    )
    ax.grid(axis="y", alpha=0.2)
    ax.set_axisbelow(True)
    output = Path(output)
    output.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output, dpi=200)
    plt.close(fig)
    return output


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    print(plot_distribution(args.output))


if __name__ == "__main__":
    main()
