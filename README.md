# BOCOP Reader

This project implements the ``BOCOPSolution`` [Python](https://www.python.org/) class, which reads a [BOCOP](https://www.bocop.org/) solution directory for ease of use in scientific and engineering applications.

For example, it implements:

* Grouping states/adjoint states/control variables together in ``VariableBunch`` classes.
* Representing variables in common types for scientific Python, such as [NumPy](https://numpy.org/) ``ndarray`` and [Pandas](https://pandas.pydata.org/) ``DataFrame``.
* Improved plotting with the [matplotlib](https://matplotlib.org/) library, easily plotting variables over time as well as phase diagrams between states with full customization capabilities.
* Variable interpolation with cubic splines, allowing for easy differentiation and integration.
* Variable interpolation with piecewise constants, numerically detecting bang-bang controls and returning their [LaTeX](https://www.latex-project.org/) representation.

# Installation and use

For local  or [Google Colab](https://colab.research.google.com/) installation, just use the command:

``
pip install git+https://github.com/johnny-godoy/bocop-reader.git
``

The main object that stores all solution files is the ``BOCOPSolution`` class, which can be imported like such:

``
from bocop_solution import BOCOPSolution
``

# Contact
For bug reports and user help, I recommend you to use the GitHub Issues feature, but you may also contact the author at johnny.godoy@ing.uchile.cl.
