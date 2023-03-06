#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import find_packages, setup

with open("README.rst") as readme_file:
    readme = readme_file.read()

requirements = ["scipy>=1.0.0", "textblob>=0.15.3", "pandas", "scipy", "matplotlib"]

setup(
    author="Lucas Shen YS",
    author_email="lucas@lucasshen.com",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    description="A small module to compute textual lexical richness (aka lexical diversity).",
    install_requires=requirements,
    license="MIT license",
    long_description_content_type="text/x-rst",
    long_description=readme,
    include_package_data=True,
    keywords=[
        "lexical diversity",
        "lexical richness",
        "vocabulary diversity",
        "lexical density",
        "lexical",
        "nlp",
        "data science",
        "natural language processing",
        "information retrieval",
        "data mining",
        "natural langauge",
        "lexical analysis",
        "api",
        "lexical analyzer",
        "linguistic analysis",
        "statistics",
    ],
    name="lexicalrichness",
    packages=find_packages(include=["lexicalrichness"]),
    url="https://github.com/LSYS/lexicalrichness",
    download_url="https://github.com/LSYS/LexicalRichness/archive/refs/tags/v0.5.0.tar.gz",
    version="0.5.0",
)
