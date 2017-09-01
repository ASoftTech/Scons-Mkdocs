"""Setup file to package scons mkdocs tools"""
from setuptools import setup, find_packages
from codecs import open  # To use a consistent encoding
from os import path

VERSION = '0.0.1'

# Get the long description from the relevant file
here = path.abspath(path.dirname(__file__))
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name="scons-tools-grbd",

    version=VERSION,
    description='Scons tools for generating documentation and building source',
    long_description=long_description,

    url='https://github.com/ASoftTech/Scons-Tools-Grbd.git',
 
    author='Aperture Software Technologies Ltd.',
    author_email='garlicbready@googlemail.com',

    license='MIT',
    packages=find_packages("scons_tools_grbd"),
    keywords="pip package, mkdocs, scons",
    include_package_data=True,

    install_requires=[
        'mkdocs>=0.16.3',
        'mkdocs-pandoc>=0.2.6',
    ],

    entry_points={
        'scons.tools': [
            'scons_tools_grbd = scons_tools_grbd.Tools',
        ],
        'scons.tests': [
            'scons_tools_grbd = scons_tools_grbd.Tests',
        ],
    },

    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        "Programming Language :: Python :: Implementation :: CPython",
        'Topic :: Documentation',
        'Topic :: Text Processing',
    ],

    zip_safe=False,
)