"""Implement the BOCOPSolution class, which stores all the information of BOCOP solution file."""

import os
import warnings

import numpy as np
import pandas as pd

from models._bunches import _AdjointStates, _Controls, _States

warnings.filterwarnings("error", category=UserWarning)
__CONSTANT_NAMES: tuple[str, str, str] = ("discretization_times", "stage_times", "parameters")


class BOCOPSolution:
    """Class that stores the solution of an optimal control problem solved by BOCOP.

    Attributes
    ----------
    adjoint_states: AdjointStates
        The container for all adjoint state variables.
    controls: Controls
        The container for all control variables.
    dataframe: pd.DataFrame
        A dataframe storing the value of all state and control variables, indexed by their discretization time.
    discretization_times: 1-D np.ndarray of length N
        The times at which the variables are evaluated.
    parameters: np.ndarray
    stage_times: 1-D np.ndarray of length N - 1
    states: States
        The container for all state variables.
    working_directory_filename: str
        Name of the folder which contains the solution files."""
    __slots__ = "adjoint_states", "controls", "dataframe", "discretization_times", "parameters", "stage_times", "states",\
                "working_directory_filename"

    def __init__(self, working_directory_filename: str):
        """
        Parameters
        ----------
        working_directory_filename: str
            Name of the folder which contains the solution files."""
        self.working_directory_filename = working_directory_filename
        for name in __CONSTANT_NAMES:
            setattr(self, name, self.file_to_array(name))
        files = []
        for file in os.listdir(working_directory_filename):
            filename = os.fsdecode(file)
            prefix, suffix = filename.split(".")
            if suffix == "export" and prefix not in __CONSTANT_NAMES:
                files.append(prefix)
        states = [file for file in files if f"{file}_adjoint_state" in files]
        controls = [file for file in files if f"stage_{file}" in files]
        self.adjoint_states = _AdjointStates(self, states)
        self.states = _States(self, states)
        self.controls = _Controls(self, controls)
        self.dataframe = pd.concat([self.states.dataframe, self.controls.dataframe], axis=1)

    def __repr__(self):
        return f"{self.__class__.__name__}({self.working_directory_filename})"

    def _file_to_array(self, filename: str) -> np.ndarray:
        """Read a file in the directory, and return it's contents as a numpy array.

        Parameters
        ----------
        filename: str
            Name of the file within the directory name.

        Returns
        -------
        array: np.ndarray
            The array with the values stored in the file. If the file is empty, then it is an empty array."""
        try:
            array = np.genfromtxt(f"{self.working_directory_filename}/{filename}.export")
        except UserWarning:
            array = np.empty(1)
        return array


if __name__ == "__main__":
    bs = BOCOPSolution("data/bocop_sample")
    print(bs.states.biomass.adjoint)
