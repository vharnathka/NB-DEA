# NB-DEA: Differential Expression Analyzer

## Project Description

CSE 185 Final Project: Differential expression analyzer

## Installation:

### Prerequisites
- Python 3.8
- Required libraries: `requirements.txt`

### Setting up the environment

1. Clone the respository:

```
git clone https://github.com/vharnathka/NB-DEA.git
cd NB-DEA
```

2. Install the required libraries:
```
pip install pr requirements.txt
```

3. Install `nb_dea.py`
```
python setup.py install
```
If you do not have administrative rights on your system, add `--user` after that command and rerun.

4. Verify the installation
```
which nb_dea
nb_dea --help
```

## Usage:

Insert two files:

- File A has the filenames of the samples/replicates of your first condition
- File B has the filenames of the samples/replicates of your second condition
- Use `-f` to filter for a low count
- Samples should be in RSEM format

Testing:

1. Download the testing files separately by downloading this as a zip file and using the files in `testing`:
2. navigate to this folder and input the files `conditionA` and `conditionB` into the `nb-dea` input.
