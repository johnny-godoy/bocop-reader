# BOCOP Reader

This project implements the ``BOCOPSolution`` [Python](https://www.python.org/) class, which reads a [BOCOP](https://www.bocop.org/) solution directory for ease of use for scientists and engineers.

For example, it implements:

* Grouping states/adjoint states/control variables together in ``VariableBunch`` classes.
* Representing variables in common types for scientific Python, such as [NumPy](https://numpy.org/) ``ndarray`` and [Pandas](https://pandas.pydata.org/) ``DataFrame``.
* Improved plotting with the [matplotlib](https://matplotlib.org/) library, easily plotting variables over time as well as phase diagrams between states with full customization capabilities.
* Variable interpolation with cubic splines, allowing for easy differentiation and integration.
* Variable interpolation with piecewise constants, numerically detecting bang-bang controls and returning their [LaTeX](https://www.latex-project.org/) representation.

# TO DO

* Set up the project for easy installation.
* Write thorough testing with all the BOCOP example problems.
* Create example [Jupyter](https://jupyter.org/) Notebooks, acting as a User Guide.