import setuptools

from bocop_solution import __version__

setuptools.setup(name="bocop_solution",
                 version=__version__,
                 description="Reader for BOCOP solution files",
                 license="MIT",
                 author="Johnny Godoy",
                 author_email="johnny.godoy@ing.uchile.cl",
                 url="https://github.com/johnny-godoy/bocop-reader",
                 install_requires=["matplotlib>=3.2.2", "numpy>=1.21.6", "pandas>=1.3.5", "scipy>=1.4.1"],
                 py_modules=["bocop_solution"],
                 packages=["internals"]
                 )
