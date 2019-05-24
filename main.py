import sys
sys.path.append('Algorithms/')
sys.path.append('Results/')
sys.path.append('Classes/')
sys.path.append('MeansData/')
sys.path.append('Algorithms/')

import time
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
import calculate_stats

def main(action, protein, algorithm=None, dimension=None, size=None):
    """
    Calls the wanted function from a dict and runs it.
    """

    actions_dict = get_actions()

    # run visualize
    if action == "visualize":
        actions_dict[action](algorithm, protein, dimension, size)
    # run algorithm
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
                    'beam_search_random': beam_search_random.beam_search_random,
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
        protein = sys.argv[3]
        dimension = sys.argv[4].lower()
    elif action != "visualize":
        # variable casting for running algorithms
        if len_args == 4:
            protein = sys.argv[2]
            dimension = sys.argv[3].lower()
        # variable casting for getting statistics
        elif len_args == 3 and action == "calculate_stats":
            protein = sys.argv[2]
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
    if action != "calculate_stats" and dimension != "2d" and dimension != "3d":
        print("please choose either 2d or 3d as dimension")
        exit(1)

    # ensure subplot size is a positive int, if specified
    if len_args == 6:
        size = sys.argv[5]
        if not size.isdigit():
            print("please pick a subplot size that is a positive int")
            exit(1)
        if int(size) < 1:
            print("please pick a subplot size that is a positive int")
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
    elif len_args == 5:
        # visualize
        main(action, protein, algorithm, dimension)
        # statistics
    elif len_args == 3:
        main(action, protein)
        # visualize with defined subplot size
    else:
        main(action, protein, algorithm, dimension, size)

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
