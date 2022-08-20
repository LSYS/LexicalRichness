#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()


requirements = ['scipy>=1.0.0', 'textblob>=0.15.3']

setup(
    author="Lucas Shen YS",
    author_email='lucas@lucasshen.com',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    description="A small module to compute textual lexical richness (aka lexical diversity).",
    install_requires=requirements,
    license="MIT license",
    long_description_content_type='text/x-rst',
    long_description=readme,
    include_package_data=True,
    keywords=['lexical diversity', 'lexical richness', 'vocabulary diversity', 'lexical density', 'lexical'],
    name='lexicalrichness',
    packages=find_packages(include=['lexicalrichness']),
    url='https://github.com/LSYS/lexicalrichness',
    download_url='https://github.com/LSYS/LexicalRichness/archive/refs/tags/v0.2.0.tar.gz',
    version='0.2.0'
)
