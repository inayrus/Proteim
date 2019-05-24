# Project Proteim

Find the most optimal folded proteins

## Getting Started

### Prerequisites

This codebase is completely written in Python [Python3.6.3](https://www.python.org/downloads/). In requirements.txt are alle necessary packages to run the code successfully. These packages can be easily installed with pip through the following instruction:

```
pip install -r requirements.txt
```

### Structure

The Algorithms folder consists of all written algorithms. It specifically contains:
* Random algorithm      (to run the algorithm, use random_fold)
* Depth first search    (to run: depth_first)
* Breadth first search  (to run: breadth_first)
* Local beam search     (to run: beam_search or beam_search_random)
* Branch and bound      (to run: branch_and_bound)
* Greedy algorithm      (to run: greedy)

The MeansData folder has csv files with the stability of all proteins after 1000 iterations with the random algorithm.
In this folder is also a script to calculate a csv data's mean and mode, and plot the data distribution in a histogram.

The ProteinsData folder contains 9 text files with amino acid orders of the tested proteins:
* protein_a1
* protein_b1 - protein_b4
* protein_c1 - protein_c4

The Results folder contains the results of the algorithms, where they are firstly seperated dimension folders and then seperated in  algorithm folders.
It also has a function to visualize a results file.


### Running code

To run the code, see the following intstructions and apply them to the algorithms and
protein names described above.

If you want to run an algorithm. First you see a general example
and than an example than an example to run  branch_and_bound for protein_b1 in 3d.
The exact algorithm names

```
python main.py name_algorithm protein 2d/3d

python main.py branch_and_bound protein_b1 3d
```

If you want to visualize the result of a protein. First you see a general example
and than an example if you want to visualize branch_and_bound for protein_b1 in 3d:

```
python main.py visualize name_algorithm protein 2d/3d

python main.py visualize branch_and_bound protein_b1 3d
```

If you choose for a 2d visualisation you can also choose to visualize multiple Proteins
in one plot. You can do this by adding a dimension. First you see an general example
than an example to visualize the branch and bound of protein_a1 2x2.


```
python main.py visualize name_algorithm protein 2d number_of_proteins

python main.py visualize branch_and_bound protein_a1 2d 2
```

If you wish to get the statistics (mean, mode, data distribution) for a protein.
First you see a general example and than an example for protein_c3.


```
python main.py calculate_stats protein

python main.py calculate_stats protein_c3
```


## Authors
Machiel Cligge,
Valerie Sawirja &
Amber Mayenburg

## Acknowledgments
* Minor Programmeren van de UvA
* Bas Terwijn
* Bram van den Heuvel
* Daan van den Berg
