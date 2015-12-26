[![Build Status](https://travis-ci.org/underchemist/nanonispy.svg?branch=master)](https://travis-ci.org/underchemist/nanonispy)
[![Coverage Status](https://coveralls.io/repos/underchemist/nanonispy/badge.svg?branch=master&service=github)](https://coveralls.io/github/underchemist/nanonispy?branch=master)
[![Install with conda](https://anaconda.org/underchemist/nanonispy/badges/installer/conda.svg)](https://anaconda.org/underchemist/nanonispy/badges/installer/conda.svg)
# nanonispy

A small library written in python 3 to parse Nanonis binary and ascii files. 

## Requirements

Currently written and tested with 
- python 3.5
- python 3.4

Depends on 
- numpy

Will continue making tests that are actually useful and maybe will make this a conda/pip build.

## Install
### pip
```
pip install nanonispy
```

### conda
```
conda install --channel https://conda.anaconda.org/underchemist nanonispy
```

### github
Simply clone this repo and run
```
python setup.py install
```

## Basic usage

Once installed, you should be able to import it to any python script or ipython session.

```python
import nanonispy as nap
```

Then given a file,

```python
grid = nap.read.Grid('/path/to/datafile.3ds')
```

You can look at the attributes and methods to determine the information available. 

## Running tests
Similar to the install, except run
```
python setup.py test
```
.
If you have the nose module installed, it's as simple as 
```
nosetests
```
.

You can also see coverage of the tests as well as ignore the test discovery of numpy core packages (don't quite understand why it does this) with
```
nosetests --with-coverage --cover-branches --cover-package=nanonispy
```
.

*I don't know how to turn tests without nose...*

## To do
- homogenize grid and scan header keys, right now header formats are pretty different and I'm to lazy to do it myself.
- more relevant tests
- saving methods

