from setuptools import setup
from Cython.Build import cythonize

setup(
    name='Qlatgir library for replacing null values!',
    ext_modules=cythonize("qalatgir.pyx"),
    zip_safe=False,
)
