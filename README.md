# NB-DEA: Differential Expression Analyzer

Installation:

```
pip install git+https://github.com/vharnathka/NB-DEA.git
```


Usage:

Insert two files:

- File A has the filenames of the samples/replicates of your first condition
- File B has the filenames of the samples/replicates of your second condition
- Use `-f` to filter for a low count
- Samples should be in RSEM format

Testing:

1. Download the testing files separately by downloading this as a zip file and using the files in `testing`:
2. navigate to this folder and input the files `conditionA` and `conditionB` into the `nb-dea` input.
