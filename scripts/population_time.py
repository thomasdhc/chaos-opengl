"""Compare initial and long-run logistic-map populations at three constant rates."""

import argparse
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from bifurcation import INITIAL_POPULATION, sample_attractor


EXPERIMENTS = (
    (3.828, "Chaos near the three-cycle onset", "#555555"),
    (3.830, "Period 3", "#286a9b"),
    (3.845, "Period 6", "#b15b24"),
)
INITIAL_STEPS = 120
SETTLING_STEPS = 20000
LONG_RUN_STEPS = 60
DEFAULT_OUTPUT_DIRECTORY = Path(__file__).resolve().parents[1] / "docs/graphs"


def plot_time_views(output_directory=DEFAULT_OUTPUT_DIRECTORY):
    rates = np.array([r for r, _, _ in EXPERIMENTS])
    # One continuous trajectory per rate, including the shared initial population.
    populations = np.vstack((
        np.full((1, rates.size), INITIAL_POPULATION),
        sample_attractor(rates, burn_in=0, iterations=SETTLING_STEPS + LONG_RUN_STEPS),
    ))
    output_directory = Path(output_directory)
    output_directory.mkdir(parents=True, exist_ok=True)
    outputs = []
    views = (
        (0, INITIAL_STEPS, "Initial population evolution", "population_initial.png"),
        (SETTLING_STEPS, LONG_RUN_STEPS, "Long-run population evolution", "population_long_run.png"),
    )
    for start, steps, title, filename in views:
        fig, axes = plt.subplots(3, 1, figsize=(12, 8), sharex=True, layout="constrained")
        times = np.arange(start, start + steps + 1)
        for column, (ax, (r, behavior, color)) in enumerate(zip(axes, EXPERIMENTS)):
            ax.plot(times, populations[times, column], "o-", color=color, ms=3, lw=0.8)
            ax.set(title=f"r = {r:.3f} · {behavior}", ylabel="Population x", ylim=(0, 1))
            ax.set_xlim(times[0], times[-1])
            ax.grid(alpha=0.2)
        axes[-1].set_xlabel("Time step n")
        # Keep absolute step numbers visible in the long-run view.
        axes[-1].ticklabel_format(axis="x", style="plain", useOffset=False)
        fig.suptitle(f"{title}\nConstant r · shared x₀ = {INITIAL_POPULATION}", fontsize=14)
        output = output_directory / filename
        fig.savefig(output, dpi=200)
        plt.close(fig)
        outputs.append(output)
    return outputs


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-directory", type=Path, default=DEFAULT_OUTPUT_DIRECTORY)
    args = parser.parse_args()
    for output in plot_time_views(args.output_directory):
        print(output)


if __name__ == "__main__":
    main()
