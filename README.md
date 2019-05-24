# Project Proteim

Find the most optimal folded proteins

## Getting Started

### Statespace
The upper bound of the statespace is 4 * 3<sup>(n-1)</sup>, where n is the number of amino acids in a protein.
The first amino had four placement options and the following ones all have three.
These placement options difference of the first animo is why the formula has a times 4 and a to the (n-1)th power.

This statespace can be reduced by placing the first two amino acids. This will remove the rotational symmetry
and results in a formula of 3<sup>(n-2)</sup>.

We have also removed the mirror symmetry in the proteins, by always removing the left placement option if all the
previously placed amino acids are laying in a straight line. This reduces the statespace by a third,
giving us a reduced upper bound of 3<sup>(n-2)</sup> * 2/3.

More information and an illustration of this statespace reduction can be found in the powerpoint (slide 5-7, Presentatie folder).

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
* Local beam search     (to run: beam_search)
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

python main.py branch_and_bound protein_b1 3d
```

##### beam_search
When you want to run beam search, you can chose for one with a random factor or not.
The non-random beam search always picks the first proteins for the length of the beam.
The beam search with a random factor makes a list of best proteins. When this list
is bigger than the beam, this beam search picks randomly the best proteins out of this
list. To run a beam search for protein_a1 in 2d with a random factor, see example below.

```
python main.py beam_search protein 2d/3d true/false

python main.py beam_search protein_a1 2d true
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
