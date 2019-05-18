import sys
sys.path.append('Algorithms/')
sys.path.append('Results/')
sys.path.append('Classes/')

import pathlib
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

    # a dict with all actions
    actions_dict = {
                    'beam_search_random': beam_search_random.beam_search_random,
                    'beam_search': beam_search.beam_search,
                    'branch_and_bound': branch_and_bound.branch_and_bound,
                    'breadth_first': breadth_first.breadth_first,
                    'depth_first': depth_first.depth_first,
                    'greedy': greedy.greedy_loop,
                    'random_fold': random_fold.random_loop,
                    'visualize': visualize_csv.visualize_dimension
    }

    action = sys.argv[1]
    len_args = len(sys.argv)

    # variable casting for visualizing
    if action == "visualize" and (len_args == 5 or len_args == 6):
        algorithm = sys.argv[2]
        protein = sys.argv[3]
        dimension = sys.argv[4].lower()
    # variable casting for running algorithms
    elif action != "visualize" and len_args == 4:
        protein = sys.argv[2]
        dimension = sys.argv[3].lower()
    # argv usage check
    else:
        print("two usage options \n"
              "running an algorithm: python main.py algorithm protein dimension\n"
              "visualizing a result: python main.py visualize algorithm protein dimension [2d_subplot_size]")
        exit(1)


    # ensure that the protein name exists in ProteinData
    file = pathlib.Path("ProteinData/{}.txt".format(protein))
    if not file.exists():
        print("please choose a protein from the ProteinData folder (ex. protein_a1)")
        exit(1)

    # ensure that the dimension is valid
    if dimension != "2d" and dimension != "3d":
        print("please choose either 2d or 3d as dimension")
        exit(1)

    # ensure subplot size is a positive int, if specified
    if len_args == 6:
        size == sys.argv[5]
        if size < 1 or not size.is_integer():
            print("please pick a subplot size that is a positive int")
            exit(1)

    # check if action exists in the dict
    if action in actions_dict:
        if action == "visualize":

            # ensure the algorithm to visualize exists
            if algorithm not in actions_dict:
                print("please pick an algorithm from the Algorithms folder to visualize.")
                exit(1)
            # if all is well, run visualize
            actions_dict[action](algorithm, protein, dimension, size)

        # if all is good, run algorithm
        else:
            actions_dict[action](protein)
    else:
        print("action does not exist. \n"
              "please choose to 'visualize' or pick an algorithm from the Algorithms folder.")
        exit(1)

if __name__ == "__main__":
    main()
