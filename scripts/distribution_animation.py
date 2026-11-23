"""Animate population distributions over fixed growth rates from 3.820 to 3.860."""

import argparse
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
from matplotlib.animation import FuncAnimation, PillowWriter
import matplotlib.pyplot as plt
import numpy as np

from bifurcation import INITIAL_POPULATION, sample_attractor
from population_distribution import BIN_EDGES, STEPS


R_MIN = 3.820
R_MAX = 3.860
FRAME_COUNT = 201
FPS = 12
DEFAULT_OUTPUT = Path(__file__).resolve().parents[1] / "docs/graphs/population_distribution_sweep.gif"


def distribution_frames():
    rates = np.round(np.linspace(R_MIN, R_MAX, FRAME_COUNT), 4)
    populations = sample_attractor(rates, burn_in=0, iterations=STEPS)
    frequencies = np.array([
        np.histogram(populations[:, column], bins=BIN_EDGES)[0]
        for column in range(rates.size)
    ]) * (100 / STEPS)
    return rates, frequencies


def plot_animation(output=DEFAULT_OUTPUT):
    rates, frequencies = distribution_frames()
    fig, (ax, progress) = plt.subplots(
        2, 1, figsize=(10, 6), layout="constrained",
        gridspec_kw={"height_ratios": [6, 1]},
    )
    bars = ax.bar(
        BIN_EDGES[:-1], frequencies[0], width=np.diff(BIN_EDGES), align="edge",
        color="#555555", edgecolor="white", linewidth=0.4,
    )
    ax.set(
        xlabel="Population x", ylabel="Sampled steps per bin (%)", xlim=(0, 1),
        ylim=(0, np.ceil(frequencies.max() / 5) * 5),
    )
    ax.grid(axis="y", alpha=0.2)
    ax.set_axisbelow(True)
    title = ax.set_title(f"r = {rates[0]:.4f}")
    fig.suptitle(
        "Population distribution across growth rates\n"
        f"Independent fixed-r runs · steps 1–{STEPS:,} · x₀ = {INITIAL_POPULATION}",
        fontsize=12,
    )
    progress.set(xlim=(R_MIN, R_MAX), ylim=(0, 1), xlabel="Growth rate r")
    progress.set_yticks([])
    ticks = np.linspace(R_MIN, R_MAX, 5)
    progress.set_xticks(ticks, [f"{r:.3f}" for r in ticks])
    for r, label in (
        (1 + np.sqrt(8), "3-cycle onset"),
        (3.8414990075, "3 → 6"),
        (3.8568, "Interior crisis"),
    ):
        progress.axvline(r, color="#999999", lw=0.7, ls="--")
        progress.text(r, 0.85, label, ha="center", va="center", fontsize=8)
    cursor = progress.axvline(rates[0], ymax=0.6, color="#b15b24", lw=2)

    def update(frame):
        for bar, frequency in zip(bars, frequencies[frame]):
            bar.set_height(frequency)
        title.set_text(f"r = {rates[frame]:.4f}")
        cursor.set_xdata([rates[frame], rates[frame]])
        return (*bars, title, cursor)

    output = Path(output)
    output.parent.mkdir(parents=True, exist_ok=True)
    animation = FuncAnimation(fig, update, frames=rates.size, interval=1000 / FPS)
    animation.save(output, writer=PillowWriter(fps=FPS), dpi=100)
    plt.close(fig)
    return output


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    print(plot_animation(args.output))


if __name__ == "__main__":
    main()
