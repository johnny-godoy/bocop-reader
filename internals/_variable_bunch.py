"""Implement the VariableBunch class, which stores variables of the same type."""

from __future__ import annotations

import pandas as pd
import scipy.ndimage

from ._utilities import subplots, PiecewiseConstantInterpolator
from ._variable import _Variable


class _VariableBunch:
    """Base class to stores many variables of the same type (eg: only states).

    Attributes
    ----------
    dataframe: pd.DataFrame
        A dataframe with the values of each variable stored, indexed by time.
    variables: dict[str, Variable]
        A dictionary storing each variable, with their names as keys.
    working_directory_filename: str
        The file which stores the exported solution."""
    def __init__(self, solution: BOCOPSolution, variable_list: list[str]):
        """
        Parameters
        ----------
        solution: BOCOPSolution
            An instance of the class that stores all the solution information.
        variable_list: list[str]
            A list with each variable named."""
        self.variables = {name: _Variable(solution, name) for name in variable_list}
        self.working_directory_filename = solution.working_directory_filename
        self.dataframe = pd.DataFrame({name: variable.series
                                       for name, variable in self.variables.items()})
        # Setting an attribute for each variable with a valid name:
        for name, variable in self.variables.items():
            if not hasattr(self, name):
                setattr(self, name, variable)
        # Processing all series for step interpolation in their dataframe
        processed_dataframe = self.dataframe.apply(lambda column: scipy.ndimage.median_filter(column, size=1))
        processed_dataframe = (processed_dataframe - processed_dataframe.min())/(processed_dataframe.max() - processed_dataframe.min())
        # Creating the step interpolator for each variable
        for variable, (_, processed_series) in zip(self.variables.values(), processed_dataframe.iteritems()):
            variable.step_interpolator = PiecewiseConstantInterpolator(variable.series, processed_series)

    def __repr__(self):
        return f"{self.__class__.__name__}({self.working_directory_filename}, variables={list(self.variables.values())})"

    def __getitem__(self, name):
        """Get the variable object given the name."""
        return self.variables[name]

    def __iter__(self):
        """Iterate over the variables in the bunch."""
        return iter(self.variables.values())

    def __len__(self):
        """Return the number of variables in the bunch."""
        return len(self.variables)

    def size(self):
        """Return the number of elements in the bunch."""
        return self.dataframe.size

    def plot(self, n_cols: int = 0, n_rows: int = 0, **kwargs) -> tuple[Figure, Axes | np.array[Axes]]:
        """Plot all variables in the bunch as subplots of a single plot object.
         Returns the figure and axes of the plot.

        Parameters
        ----------
        n_cols: int, optional
            The number of columns for the plot. Defaults to the bunch size.
        n_rows: int, optional
            The number of rows for the plot. Defaults to 1.
        kwargs: optional
            Keyword arguments passed to plt.subplot.

        Raises
        ------
        ValueError:
            If the product of the rows and columns (the amount of subplots) doesn't match the
            size of the bunch.

        Returns
        -------
        fig: matplotlib.figure.Figure
            The figure corresponding to all axes for the subplots of each variable.
        ax: np.array[matplotlib.axes._subplots.AxesSubplot]|matplotlib.axes._subplots.AxesSubplot
            An array of every axis, each one plotting a variable.
            If there is only one variable, then it only returns the single axis."""
        if 0 in {n_cols, n_rows}:
            n_cols = 1
            n_rows = len(self.variables)
        size = n_cols * n_rows
        if size != len(self.variables):
            raise ValueError(f"The given shape ({n_cols}, {n_rows}) is of size={size}, " +
                             f"should be {len(self.variables)}")
        fig, axes = subplots(n_rows, n_cols)
        try:
            for variable, ax in zip(self.variables.values(), axes.flatten()):
                variable.plot(ax, **kwargs)
        except AttributeError:
            list(self.variables.values())[0].plot(axes, **kwargs)
        fig.suptitle(self.__class__.__name__)
        return fig, axes
