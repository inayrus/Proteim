import sys
sys.path.append('Algorithms/')
sys.path.append('Results/')
sys.path.append('Classes/')

from Protein import Protein
# import all the algorithm files
import beam_search_random
import beam_search
import branch_and_bound
import breadth_first
import depth_first
import greedy
import random_fold
import visualize_csv

def main():

    # link the argv's to the right variables
    action = sys.argv[1]

    # variable casting for visualizing
    if action == "visualize" and len(sys.argv) == 6:
        size == sys.argv[5]
    if action == "visualize" and len(sys.argv) >= 5:
        algorithm = sys.argv[2]
        protein = sys.argv[3]
        dimension = sys.argv[4].lower()
        size = 1

    # variable casting for running algorithms
    elif action != "visualize" and len(sys.argv) == 4:
        protein = sys.argv[2]
        dimension = sys.argv[3].lower()
    # argv check
    else:
        print("two usage options \n"
              "running an algorithm: python main.py algorithm protein dimension\n"
              "visualizing a result: python main.py visualize algorithm protein dimension [2d_subplot_size]\n")
        exit(1)

    if action == "beam_search_random":
        beam_search_random.beam_search_random(protein)
    elif action == "beam_search":
        beam_search.beam_search(protein)
    elif action == "branch_and_bound":
        branch_and_bound.branch_and_bound(protein)
    elif action == "breadth_first":
        breadth_first.breadth_first(protein)
    elif action == "depth_first":
        depth_first.depth_first(protein)
    elif action == "greedy":
        greedy.greedy_loop(protein)
    elif action == "random_fold":
        random_fold.random_loop(protein)
    elif action == "visualize":
        visualize_csv.visualize_dimension(algorithm, protein, dimension, size)


if __name__ == "__main__":
    main()
