"""Implement the PhasePlotter class, extending variable bunches that require phase plot diagrams."""

from __future__ import annotations

import matplotlib.collections
import matplotlib.pyplot as plt
import numpy as np

from ._variable_bunch import _VariableBunch


class _PhasePlotter(_VariableBunch):
    """Base class for a variable bunch that implements the phase_space_plot method."""
    def phase_space_plot(self, state_x: str, state_y: str, fig_ax: tuple[Figure, Axes] = None) -> tuple[Figure, Axes]:
        """Plot the phase space of two variables. Return the figure and axes of the plot.

        Parameters
        ----------
        state_x: str
            Name of the variable in the x axis.
        state_y: str
            Name of the variable in the x axis.
        fig_ax: tuple[Figure, Axes], optional
            Figure and axis of the plot in a tuple. If None, new ones will be created.

        Returns
        -------
        fig: matplotlib.figure.Figure
            The figure of the plot.
        ax: matplotlib.axes._subplots.AxesSubplot
            The axis of the plot."""
        # Setting the figure and axis
        if fig_ax is None:
            fig, ax = plt.subplots(1, 1)
        else:
            fig, ax = fig_ax
        # Creating the phase plot, colored by time
        values_state_x = self.variables[state_x].values
        values_state_y = self.variables[state_y].values
        points = np.column_stack((values_state_x, values_state_y)).reshape((-1, 1, 2))
        lc = matplotlib.collections.LineCollection(np.concatenate([points[:-1], points[1:]], axis=1),
                                                   norm=plt.Normalize(self.discretization_times[0],
                                                                      self.discretization_times[-1]))
        lc.set_array(self.discretization_times)
        # Plot configurations
        fig.colorbar(ax.add_collection(lc), ax=ax, label="time")
        ax.set_xlabel(state_x)
        ax.set_ylabel(state_y)
        ax.set_xlim(values_state_x.min(), values_state_x.max())
        ax.set_ylim(values_state_y.min(), values_state_y.max())
        return fig, ax
