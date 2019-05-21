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
* Random algorithm
* Depth first search
* Breadth first search
* Local beam search
* Branch and bound
* Greedy algorithm

The MeansData folder has csv files with the stability of all proteins after 1000 iterations with the random algorithm.
The mean of these stabilities can be calculated with the "calculate_mean" script.

The ProteinsData folder contains text files with amino acid orders of the tested proteins.

The Results folder contains the results of the algorithms, where they are sorted in a seperate folder for every algorithm.
It also has a function to visualize a results file.


### Running code

To run the code with a standard configuration (for example by using brute-force) use the following intstructions:

If you want to run an algorithm. First you see a general example
and than an example than an example to run  branch_and_bound for protein_b1 in 3d

```
python main.py name_algorithm protein 2d/3d

python main.py branch_and_bound protein_b1 3d
```

If you want to visualize the result of a protein. First you see a general example
and than an example if you want to visualize branch_and_bound for protein_b1 in 3d:

```
python main.py visualize name_algorithm protein 2d/3d

python main.py branch_and_bound protein_b1 3d
```

If you choose for a 2d visualisation you can also choose to visualize mutiple Proteins
in one plot. You can do this by adding a dimension. First you see an general example
than an example to visualize the branch and bound of protein_a1 2x2.


```
python main.py visualize name_algorithm protein 2d number_of_proteins

python main.py visualize branch_and_bound protein_a1 2d 2
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
