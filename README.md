# Project Proteim

Find the most optimal folded proteins

## Getting Started

### Prerequisites

This codebase is completely written in Python [Python3.6.3](https://www.python.org/downloads/). In requirements.txt are alle necessary packages to run the code sucessfully. These packages can be easily installed with pip through the following instruction:

```
pip install -r requirements.txt
```

### Structure

The Algorithms folder consists of all written algorithms. It specifically contains:
* Random algorithm (ribosome_fold)
* depth first search
* breadth first search
* local beam search
* branch and bound
* greedy algorithm

The MeansData folder has csv files with the stability of all proteins after 1000 iterations with the random algorithm.
The mean of these stabilities can be calculated with the "calculate_mean" script.

The ProteinsData folder contains text files with amino acid orders of the tested proteins.

The Results folder contains the results of the algorithms, where they are sorted in a seperate folder for every algorithm.
It also has a function to visualize a results file.


### Running code


Om de code te draaien met de standaardconfiguratie (bv. brute-force en voorbeeld.csv) gebruik de instructie:

```
python main.py
```

## Authors
Machiel Cligge,
Valerie Sawirja &
Amber Mayenburg

## Acknowledgments
* minor programmeren van de UvA
* Bas Terwijn
* Bram van den Heuvel
* Daan van den Berg
