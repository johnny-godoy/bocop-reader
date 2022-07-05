"""Implement utility functions and classes."""

from __future__ import annotations

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def subplots(n_rows: int, n_cols: int, **kwargs) -> tuple[Figure, Axes]:
    """Create a rectangular plot with n_rows and n_columns of subplots. Like plt.subplots, but each subplot has the current figsize.

    Parameters
    ----------
    n_cols: int
        The number of columns for the plot.
    n_rows: int
        The number of rows for the plot.
    kwargs: optional
        Keyword arguments passed to plt.subplot."""
    return plt.subplots(nrows=n_rows, ncols=n_cols, constrained_layout=True, **kwargs,
                        figsize=np.array((n_rows, n_cols)) * plt.rcParams["figure.figsize"])


def not_close_to_zero(z: pd.Series) -> pd.Series:
    """Return True in the positions where the element of the series is not close to 0, (with absolute tolerance 1e-08)."""
    return np.logical_or(np.isnan(z), z > 1e-08)


class PiecewiseConstantInterpolator:
    """0-order spline fit to a given time series with N entries.

    Attributes:
    ----------
    intervals: np.ndarray of size 2xN
        A 2D array of intervals (length 2 arrays) in which the function is constant.
    value_per_interval: np.ndarray of size N
        A 1D array of the constant value per each interval."""
    __slots__ = "_right_times", "intervals", "name", "value_per_interval"

    def __init__(self, original_series: pd.Series, processed_series: pd.Series):
        """
        Parameters
        ----------
        original_series: pd.Series
            The series to fit.
        processed_series: pd.Series
            A denoised and normalized version of the original series."""
        self.name = original_series.name
        # Finding the cutting times
        left_times = processed_series[not_close_to_zero(processed_series.diff().abs())].index
        self._right_times = np.append(left_times[1:], original_series.index[-1])
        self.intervals = np.column_stack((left_times, self._right_times))
        # Finding the constant value for each time
        self.value_per_interval = np.array([original_series[a:b].median() for a, b in self.intervals])

    def __call__(self, times: np.ndarray) -> np.ndarray:
        """Evaluate the spline at each time.

        Parameters
        ----------
        times: np.ndarray
            Times at which to evaluate the spline.

        Returns
        -------
        values: np.ndarray
            Array of the same size as times, which the evaluation of the spline at each time."""
        indexes = np.searchsorted(self._right_times, times, side='right')
        values = self.value_per_interval[indexes]
        return values

    def __repr__(self):
        """String with the code for the LaTeX representation of the spline."""
        lines = [fr"{self.name}(t) \approx \begin{{cases}}"] + \
                [fr"{val} &\text{{ if }} t\in [{a}, {b}) \\" for (a, b), val in zip(self.intervals, self.value_per_interval)] + \
                [r"\end{cases}"]
        return "\n".join(lines)

    def _repr_html_(self):
        """LaTeX representation of the spline that is displayed in a Jupyter Notebook."""
        return f"${repr(self)}$"
