from setuptools import setup
from setuptools_rust import RustExtension


setup(
    name="rust-qalatgir",
    version="0.1.0",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python",
        "Programming Language :: Rust",
        "Operating System :: POSIX",
        "Operating System :: MacOS :: MacOS X",
    ],
    packages=["rust_qalatgir"],
    rust_extensions=[RustExtension("rust_qalatgir.rust_qalatgir", "Cargo.toml", debug=False)],
    include_package_data=True,
    zip_safe=False,
)