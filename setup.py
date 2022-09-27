from setuptools import find_packages, setup

# Get requirements from file
with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="radfeat",
    version="0.1",
    install_requires=requirements,
    packages=find_packages(),
)
