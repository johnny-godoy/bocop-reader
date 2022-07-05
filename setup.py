import setuptools

setuptools.setup(name="bocop_solution",
                 version="0.0.1",
                 description="Reader for BOCOP solution files",
                 license="MIT",
                 author="Johnny Godoy",
                 author_email="johnny.godoy@ing.uchile.cl",
                 url="https://github.com/johnny-godoy/bocop-reader",
                 install_requires=["numpy", "pandas"],
                 extra_require=["matplotlib", "scipy"],
                 py_modules=["bocop_solution"]
                 )