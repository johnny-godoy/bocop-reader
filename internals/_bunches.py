"""Implement the types of bunches which are stored in a BOCOPSolution class."""

from __future__ import annotations

from ._variable_bunch import _VariableBunch
from ._phase_plotter import _PhasePlotter


class _AdjointStates(_PhasePlotter):
    """Container for adjoint states."""
    def __init__(self, solution: BOCOPSolution, variable_list: list[str]):
        super().__init__(solution, [f"{variable}_adjoint_state" for variable in variable_list])


class _Controls(_VariableBunch):
    """Container for control variables."""
    pass


class _States(_PhasePlotter):
    """Container for states."""
    def __init__(self, solution: BOCOPSolution, variable_list: list[str]):
        super().__init__(solution, variable_list)
        # adjoints = solution.adjoint_states
        # Relating every variable to its adjoint
        # for name, variable in self.variables.items():
        #     variable.adjoint = adjoints[f"{name}_adjoint_state"]
