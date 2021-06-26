from setuptools import setup
from Cython.Build import cythonize
import numpy

setup(
    name='Qlatgir library for replacing null values!',
    ext_modules=cythonize("qalatgir.pyx"),
    include_dirs=[numpy.get_include()],
    zip_safe=False,
)
