from setuptools import setup
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md')) as f:
    long_description = f.read()

setup(
    name='nanonispy',

    # Versions should comply with PEP440.  For a discussion on single-sourcing
    # the version across setup.py and the project code, see
    # https://packaging.python.org/en/latest/single_source_version.html
    version='1.0',

    description='Library to parse Nanonis files.',
    long_description=long_description,

    # The project's main homepage.
    url='https://github.com/underchemist/nanonispy',

    # Download url
    # download_url = 'https://github.com/underchemist/nanonispy/tarball/master',

    # Author details
    author='Yann-Sebastien Tremblay-Johnston',
    author_email='yanns.tremblay@gmail.com',

    # Choose your license
    license='MIT',

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',

        # Indicate who your project is intended for
        'Intended Audience :: Developers',
        'Topic :: Scientific/Engineering :: Physics',

        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: MIT License',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5'
    ],

    # What does your project relate to?
    keywords='data science numpy binary file parse',

    # You can just specify the packages manually here if your project is
    # simple. Or you can use find_packages().
    packages=['nanonispy', 'nanonispy.tests'],

    # If there are data files included in your packages that need to be
    # installed, specify them here.  If using Python 2.6 or less, then these
    # have to be included in MANIFEST.in as well.
    package_data={
        'nanonispy': ['LICENSE', 'README.md'],
    },

    install_requires=[
          'numpy',
      ],

    tests_require = ['nose', 'coverage'],
)
