"""Implements the types of bunches which are stored in a BOCOPSolution class."""

from __future__ import annotations

from variable_bunch import _VariableBunch
from phase_plotter import _PhasePlotter


class _States(_PhasePlotter):
    """Container for states. Every variable gets the adjoint attribute added, which relates it to its adjoint variable."""
    def __init__(self, solution: BOCOPSolution, variable_list: list[str]):
        super().__init__(solution, variable_list)
        adjoints = solution.adjoint_states
        for name, variable in self.variables.items():
            variable.adjoint = adjoints[f"{name}_adjoint_state"]


class _AdjointStates(_PhasePlotter):
    """Container for adjoint states."""
    def __init__(self, solution: BOCOPSolution, variable_list: list[str]):
        super().__init__(solution, [f"{variable}_adjoint_state" for variable in variable_list])


class _Controls(_VariableBunch):
    """Container for control variables."""
    pass
