import sys
# sys.path.append('Algorithms/')
sys.path.append('Results/')
sys.path.append('Classes/')
sys.path.append('MeansData/')
sys.path.append('Algorithms/')

import time
import pathlib
from Protein import Protein
# import all the algorithm files
import beam_search
import branch_and_bound
import breadth_first
import depth_first
import greedy
import random_fold
import visualize_csv
import calculate_stats

def main(action, protein, algorithm=None, dimension=None, size=None, random=None):
    """
    Calls the wanted function from a dict and runs it.
    """

    actions_dict = get_actions()

    # run visualize
    if action == "visualize":
        if len(sys.argv) == 6:
            actions_dict[action](algorithm, protein, dimension, size)
        else:
            actions_dict[action](algorithm, protein, dimension)
    # run algorithm
    elif action == "beam_search":
        actions_dict[action](protein, random)
    elif action != "calculate_stats":
        print("running {} algorithm".format(action))
        actions_dict[action](protein)

    # calculate statistics
    else:
        actions_dict[action](protein)


def get_actions():
    """
    Returns a dict with all possible actions as keys and
    a function as their value.
    """
    # a dict with all actions
    actions_dict = {
                    'beam_search': beam_search.beam_search,
                    'branch_and_bound': branch_and_bound.branch_and_bound,
                    'breadth_first': breadth_first.breadth_first,
                    'depth_first': depth_first.depth_first,
                    'greedy': greedy.greedy_loop,
                    'random_fold': random_fold.random_loop,
                    'visualize': visualize_csv.visualize_dimension,
                    'calculate_stats': calculate_stats.calculate_stats
    }
    return actions_dict


def argv_validation():
    """
    Checks if the command line arguments are valid.
    """

    action = sys.argv[1]
    len_args = len(sys.argv)

    # usage and length check
    if action == "visualize" and (len_args == 5 or len_args == 6):
        # variable casting for visualizing
        algorithm = sys.argv[2]
        protein = sys.argv[3].lower()
        dimension = sys.argv[4].lower()
    elif action != "visualize":
        # variable casting for running algorithms
        if len_args == 4:
            protein = sys.argv[2].lower()
            dimension = sys.argv[3].lower()
        # variable casting for getting statistics
        elif len_args == 3 and action == "calculate_stats":
            protein = sys.argv[2]
        elif len_args == 5 and action == "beam_search":
            algorithm = sys.argv[1]
            protein = sys.argv[2].lower()
            dimension = sys.argv[3].lower()
            random = sys.argv[4].lower()
        else:
            print_main_usage()
    else:
        print_main_usage()

    # ensure that the protein name exists in ProteinData
    file = pathlib.Path("ProteinData/{}.txt".format(protein))
    if not file.exists():
        print("please choose a protein from the ProteinData folder (ex. protein_a1)")
        exit(1)

    # ensure that the dimension is valid
    elif action != "calculate_stats" and dimension != "2d" and dimension != "3d":
        print("please choose either 2d or 3d as dimension")
        exit(1)

    # ensure subplot size is a positive int, if specified
    elif len_args == 6:
        size = sys.argv[5]
        if not size.isdigit():
            print("please pick a subplot size that is a positive int")
            exit(1)
        if int(size) < 1:
            print("please pick a subplot size that is a positive int")
            exit(1)

    elif action == "beam_search" and len_args != 5:
        print("beam_search usage: python main.py beam_search protein dimension random")
        exit(1)
    elif action == "beam_search" and random != "true" and random != "false":
        print("The random argument in beam_search has to be true or false")
        exit(1)

    # check if action exists in the dict
    actions_dict = get_actions()
    if action in actions_dict:
        if action == "visualize":
            # ensure the algorithm to visualize exists
            if algorithm not in actions_dict:
                print("please pick an algorithm from the Algorithms folder to visualize.")
                exit(1)
    else:
        print("action does not exist. \n"
              "please choose to 'visualize' or pick an algorithm from the Algorithms folder.")
        exit(1)

    # if all is well, run main
    if len_args == 4:
        # run algorithm
        main(action, protein)
    elif action == "visualize":
        if len_args == 6:
            # visualize with defined subplot size
            main(action, protein, algorithm, dimension, size)
        else:
            main(action, protein, algorithm, dimension)
        # statistics
    elif len_args == 3:
        main(action, protein)
    else:
        # specifically for beam
        main(action, protein, algorithm, random)

def print_main_usage():
    print("three usage options \n"
          "running an algorithm: python main.py algorithm protein dimension\n"
          "visualizing a result: python main.py visualize algorithm protein dimension [2d_subplot_size]\n"
          "calculating statistics: python main.py calculate_stats protein")
    exit(1)

if __name__ == "__main__":
    start = time.time()
    argv_validation()
    end = time. time()
    print(end - start)
