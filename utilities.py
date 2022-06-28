"""
Implements utility functions and classes.
"""

from __future__ import annotations

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def subplots(n_rows: int, n_cols: int, **kwargs) -> tuple[Figure, Axes]:
    """Creates a rectangular plot with n_rows and n_columns of subplots. Unlike plt.subplots, each subplot has the current figsize.

    Parameters
    ----------
    n_cols: int
        The number of columns for the plot.
    n_rows: int
        The number of rows for the plot.
    kwargs: optional
        Keyword arguments passed to plt.subplot.

    Returns
    -------
        Just as plt.subplots.
    """
    return plt.subplots(nrows=n_rows, ncols=n_cols, constrained_layout=True, **kwargs,
                        figsize=np.array((n_rows, n_cols)) * plt.rcParams["figure.figsize"])


class PiecewiseConstantInterpolator:
    """0-order spline fit to a given time series with N entries.

    Attributes:
    ----------
    intervals: np.ndarray of size 2xN
        A 2D array of intervals (length 2 arrays) in which the function is constant.
    value_per_interval: np.ndarray of size N
        A 1D array of the constant value per each interval.
    """
    def __init__(self, series: pd.Series):
        normalized_series = (series - series.min())/(series.max() - series.min())
        left_times = normalized_series[~np.isclose(normalized_series.diff(), 0.)].index
        self._right_times = np.append(left_times[1:], series.index[-1])
        self.intervals = np.column_stack((left_times, self._right_times))
        self.value_per_interval = np.array([series[a:b].median() for a, b in self.intervals])

    def __call__(self, times: np.ndarray) -> np.ndarray:
        """Evaluates the spline at each time.

        Parameters
        ----------
        times: np.ndarray
            Times at which to evaluate the spline

        Returns
        -------
        values: np.ndarray
            Array of the same size as times, which the evaluation of the spline at each time.
        """
        indexes = np.searchsorted(self._right_times, times, side='right')
        values = self.value_per_interval[indexes]
        return values

    def __repr__(self):
        """LaTeX representation of the spline."""
        lines = [r"\begin{cases}"] + list(fr"{val} &\text{{ if }} x\in [{a}, {b}) \\"
                                          for (a, b), val in zip(self.intervals, self.value_per_interval)) + [r"\end{cases}"]
        return "\n".join(lines)

