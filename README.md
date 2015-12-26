# nanonispy

A small library written in python 3 to parse Nanonis binary and ascii files. 

## Requirements

Currently written and 'tested' with python 3.5, fairly sure this won't work with version of python < 3.0

- numpy (>1.10)

Will continue making tests that are actually useful and maybe will make this a conda/pip build.

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
If you have the nose module installed, it's as simple as 
```python
nosetests
```
.

You can also see coverage of the tests as well as ignore the test discovery of numpy core packages (don't quite understand why it does this) with
```python
nosetests --with-coverage --cover-branches --cover-package=nanonispy
```
.

*I don't know how to turn tests without nose...*

## To do
- homogenize grid and scan header keys, right now header formats are pretty different and I'm to lazy to do it myself.

