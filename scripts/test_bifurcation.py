import tempfile
import unittest
from pathlib import Path

import numpy as np

from bifurcation import R_INFINITY, distance_coordinate, plot_diagram, sample_attractor


class BifurcationTests(unittest.TestCase):
    def test_vectorized_iterations_match_scalar_map(self):
        rates = np.array([3.5, 3.55, 3.6])
        actual = sample_attractor(rates, burn_in=50, iterations=8)
        for column, r in enumerate(rates):
            x = 0.123456789
            for _ in range(50):
                x = r * x * (1 - x)
            for row in range(8):
                x = r * x * (1 - x)
                self.assertEqual(actual[row, column], x)

    def test_settled_period_doubling(self):
        rates = np.array([3.5, 3.55, 3.566, 3.569, 3.5698])
        populations = sample_attractor(rates)
        for column, period in enumerate([4, 8, 16, 32, 64]):
            self.assertEqual(np.unique(populations[:, column].round(9)).size, period)
        self.assertTrue(np.all((populations >= 0) & (populations <= 1)))

    def test_log_distance_expands_each_decade_equally(self):
        rates = R_INFINITY - np.array([1e-2, 1e-3, 1e-4, 1e-5])
        np.testing.assert_allclose(distance_coordinate(rates), [2, 3, 4, 5])
        for rate in [R_INFINITY, 3.6]:
            with self.assertRaises(ValueError):
                distance_coordinate(rate)

    def test_invalid_sampling_arguments(self):
        for rates in [[4.1], [-0.1], [float("nan")], [[3.5]]]:
            with self.assertRaises(ValueError):
                sample_attractor(rates)
        for burn_in, iterations in [(-1, 8), (20, 0)]:
            with self.assertRaises(ValueError):
                sample_attractor([3.5], burn_in, iterations)
        with self.assertRaises(ValueError):
            plot_diagram(samples=1)

    def test_headless_png_output(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "graphs" / "test.png"
            self.assertEqual(plot_diagram(output, 30, 20, 8), output)
            self.assertEqual(output.read_bytes()[:8], b"\x89PNG\r\n\x1a\n")


if __name__ == "__main__":
    unittest.main()
