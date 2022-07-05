"""Implement the Variable class, which contains states, adjoint states or controls variables."""

from __future__ import annotations

import matplotlib.pyplot as plt
import pandas as pd
import scipy.interpolate
import scipy.optimize


class _Variable:
    """Class that stores a state, adjoint state or control variable.

    Attributes
    ----------
    discretization_times: np.ndarray
        The times at which the variable is evaluated.
    cubic_interpolator: scipy.interpolate.interpolate.interp1d
        An interpolator for the variable.
    name: str
        The name of the variable.
    series: pd.Series
        The values of the variable, indexed by the discretization times.
    step_interpolator: PiecewiseConstantInterpolator
        A piecewise constant interpolator for the variable.
    values: np.ndarray
        The values that are taken by the variable.
    adjoint: _Variable, optional
        If the variable represents a state, then this attribute references the adjoint variable."""
    __slots__ = "discretization_times", "cubic_interpolator", "name", "series", "step_interpolator", "values", "adjoint"

    def __init__(self, solution: BOCOPSolution, name: str):
        """
        Parameters
        ----------
        solution: BOCOPSolution
            An instance of the class that stores all the solution information.
        name: str
            The name of the variable."""
        self.name = name
        # Setting arrays and series
        self.values = solution._file_to_array(name)
        times = solution.stage_times if len(solution.stage_times) == len(self.values) else solution.discretization_times
        self.discretization_times = times
        self.series = pd.Series(self.values, index=self.discretization_times, name=name)
        # Creating the interpolator object
        self.cubic_interpolator = scipy.interpolate.InterpolatedUnivariateSpline(self.discretization_times, self.values)

    def __repr__(self):
        return f"{self.__class__.__name__}({self.name})"

    def __call__(self, evaluation_times: np.ndarray, **kwargs) -> np.ndarray:
        """Evaluate the interpolator fitted with the known values of the variable."""
        return self.cubic_interpolator(evaluation_times, **kwargs)

    def inverse(self, evaluation_values: np.ndarray, guess_times: list[float | NoneType] = None) -> np.ndarray:
        """Return times such that self(times) is close to evaluation_values, and times is close to guess_times. This inverts
        the interpolator, even if it is not an injective function.

        Parameters
        ----------
        evaluation_values: np.ndarray
            The values whose time we wish to find.
        guess_times: list[float | NoneType], optional
            A list of guess times which are close to the ones we want to find. If a value is None, then the guess will be the closest
            time in the series attribute. Giving a guess makes sure you can get different times for the same value in the case of non
            injectivity.

        Returns
        -------
        times: np.ndarray
            The times at which self(times) = evaluation_values"""
        if guess_times is None:
            guess_times = [None for _ in evaluation_values]
        # Filling up the times that where not given with the closest value in the series
        for i, (guess, value) in enumerate(zip(guess_times, evaluation_values)):
            if guess is None:
                guess_times[i] = (self.series - value).abs().argmin()
        # Inverting the function with root-finding
        times = scipy.optimize.root(lambda x: self(x) - evaluation_values,
                                    np.array(guess_times)).x
        return times

    def plot(self, ax: AxesSubplot = None, **kwargs) -> AxesSubplot:
        """Plot the variable over time, and return the resulting axis.

        Parameters
        ----------
        ax: matplotlib.axes._subplots.AxesSubplot, optional
            An axis to plot the variable. If None, a new axis will be created.
        kwargs: optional
            Keyword arguments passed to plt.subplot.

        Returns
        -------
        ax: matplotlib.axes._subplots.AxesSubplot
            The axis in which the plot is drawn."""
        if ax is None:
            ax = plt.subplots(1, 1)[1]
        ax.plot(self.discretization_times, self.values, **kwargs)
        ax.set_xlabel("time")
        ax.set_ylabel(self.name)
        return ax
