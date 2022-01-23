from setuptools import setup, find_packages

with open("README.md", "r") as readme_file:
    readme = readme_file.read()

requirements = [
    "Pillow"
]

setup(
    name="binfmtspec",
    version="0.0.1",
    author="Leonhard Pfob",
    author_email="l.pfob@3-klicks.de",
    description="A package for defining and visualizing binary format specifications.",
    long_description=readme,
    long_description_content_type="text/markdown",
    url="",
    packages=[ "binfmtspec" ],
    install_requires=requirements,
    classifiers=[
        "Programming Language :: Python :: 3.7",
    ],
)