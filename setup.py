"""
A setuptools based setup module.

Run using:
    $ python -m pip install -ve .

Explanation of arguments:
    -e, --editable <path/url>
        Install a project in editable mode (i.e. setuptools “develop mode”) from a local project path or a VCS url.

    -v, --verbose
        Give more output.
"""
# pylint: disable=invalid-name

from pathlib import Path
from setuptools import setup, find_packages

here = Path(__file__).parent.absolute()  # pylint: disable=no-member

# Get the long description from the README file
with open(here / "README.md", encoding="utf-8") as f:
    long_description = f.read()

with open(here / "requirements.txt", encoding="utf-8") as f:
    requirements = f.read().splitlines()

setup(
    name="qiskit_metal",
    version="0.0.2",
    description="Quantum VLSI and Sims",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Qiskit/qiskit-metal",
    author="Qiskit Development Team",
    author_email="qiskit@qiskit.org",
    license="Apache 2.0",
    classifiers=[
        "Environment :: Console",
        "License :: OSI Approved :: Apache Software License",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: MacOS",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Topic :: Scientific/Engineering",
    ],
    keywords="qiskit sdk quantum",
    packages=find_packages(),
    package_data={"": ["*.ui", "*.qrc", "_imgs/*.png", "_imgs/*.txt"]},
    python_requires=">=3.7, <=3.7.8",
    install_requires=requirements,
)
