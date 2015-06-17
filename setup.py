#!/usr/bin/python3
from os import path
from setuptools import setup


# https://github.com/pypa/sampleproject/blob/master/setup.py
here = path.abspath(path.dirname(__file__))

# Get the long description from the relevant file
with open(path.join(here, 'README'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='ManFuzzer',
    version='1.1',
    packages=['manparser', 'arguments', 'values', 'legacymanfuzzer'],
    include_package_data=True,
    license='Apache2.0',
    description='The ManFuzzer is a tool to create fuzzing inputs for command line programs using help options '
                'and man pages.',
    long_description=long_description,
    url='https://github.com/GroundPound/ManFuzzer',
    author='Peter Chapman & G.Grieco',
    author_email='peter@cmu.edu, gg@cifasis-conicet.gov.ar',
    scripts=['manfuzzer'],
    install_requires=[
    ],
)
