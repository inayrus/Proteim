# Project Proteim

Find the most optimal folded proteins

## Getting Started

### Prerequisites

This codebase is completely written in Python [Python3.6.3](https://www.python.org/downloads/). In requirements.txt are all necessary packages to run the code successfully. These packages can be easily installed with pip through the following instruction:

```
pip install -r requirements.txt
```

### Structure

#### The Algorithms folder
Consists of all written algorithms. It specifically contains:
* Random algorithm      (to run the algorithm, use random_fold)
* Depth first search    (to run: depth_first)
* Breadth first search  (to run: breadth_first)
* Local beam search     (to run: beam_search or beam_search_random)
* Branch and bound      (to run: branch_and_bound)
* Greedy algorithm      (to run: greedy)

#### The MeansData folder
This folder has csv files with the stability of all proteins after 1000 iterations with the random algorithm.
In this folder is also a script to calculate a csv data's mean and mode, and plot the data distribution in a histogram.

#### The ProteinsData folder
This folder contains 9 text files with amino acid orders of the tested proteins:
* protein_a1
* protein_b1 - protein_b4
* protein_c1 - protein_c4

#### The Results folder
In this folder are the results of the algorithms, where they are firstly separated dimension folders and then separated in  algorithm folders.
It also has a function to visualize a results file.


### Running code

To run the code with a standard configuration:

#### Running algorithms
First you see a general example and then an example to run branch and bound for protein_b1 in 3d.

```
python main.py name_algorithm protein 2d/3d
+
python main.py branch_and_bound protein_b1 3d
```

#### Visualizing a result
First you see a general example and than an example to visualize branch and bound for protein_b1 in 3d:

```
python main.py visualize name_algorithm protein 2d/3d

python main.py branch_and_bound protein_b1 3d
```

##### 2d visualisation
If you choose for a 2d visualisation you can also choose to visualize multiple Proteins
in one plot. You can do this by adding a dimension. First you see an general example
than an example to visualize the branch and bound of protein_a1 2x2.


```
python main.py visualize name_algorithm protein 2d number_of_proteins

python main.py visualize branch_and_bound protein_a1 2d 2
```

#### Retrieving statistics
If you wish to get mean, mode and data distribution for a protein.
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
