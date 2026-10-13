"""Library and CLI tools for interacting with buienradar."""

from codecs import open
from os import path
from subprocess import check_output

from setuptools import find_packages, setup

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()


def version_from_git():
    """Acquire package version from current git tag."""
    return check_output(['git', 'describe', '--tags', '--abbrev=0'],
                        universal_newlines=True)


setup(
    name='buienradar',

    version='1.0.10',
    python_requires='>=3.11',

    description=__doc__,
    long_description_content_type='text/x-rst',
    long_description=long_description,

    # The project's main homepage.
    url='https://github.com/mjj4791/python-buienradar',

    # Author details
    author='mjj4791',
    author_email='',

    # Choose your license
    license='MIT',

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 5 - Production/Stable',

        # Indicate who your project is intended for
        'Intended Audience :: Developers',

        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: MIT License',

        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Programming Language :: Python :: 3.13',
        'Programming Language :: Python :: 3.14',
        'Programming Language :: Python :: 3.15'
    ],

    keywords='buienradar weather',

    packages=find_packages(exclude=['contrib', 'docs', 'tests']),

    install_requires=[
        'docopt',
        'pytz',
        'requests',
        'xmltodict',
        'vincenty',
    ],

    # # List additional groups of dependencies here (e.g. development
    # # dependencies). You can install these using the following syntax,
    # # for example:
    # # $ pip install -e .[dev,test]
    # extras_require={
    #     'dev': ['check-manifest'],
    #     'test': ['coverage'],
    # },

    # # If there are data files included in your packages that need to be
    # # installed, specify them here.
    # package_data={
    #     'sample': ['package_data.dat'],
    # },

    # # Although 'package_data' is the preferred approach, in some case you may
    # # need to place data files outside of your packages. See:
    # # https://setuptools.pypa.io/en/latest/userguide/datafiles.html
    # # In this case, 'data_file' will be installed into '<sys.prefix>/my_data'
    # data_files=[('my_data', ['data/data_file'])],

    # To provide executable scripts, use entry points in preference to the
    # "scripts" keyword. Entry points provide cross-platform support and allow
    # pip to create the appropriate form of executable for the target platform.
    entry_points={
        'console_scripts': [
            'buienradar=buienradar.__main__:main',
        ],
    },
)
