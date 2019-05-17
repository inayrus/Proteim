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

def main():
    action = sys.argv[1]
    protein = sys.argv[2]
    dimension = sys.argv[3]

    if action == "greedy":
        greedy.greedy_loop(protein)
    elif action == "random_fold":
        random_fold.random_loop(protein)


    # # ask if the user wants to run an algorithm or visualize
    # while True:
    #     action = input("choose an action: \n"
    #                    "1) running an algorithm \n"
    #                    "2) visualizing a protein \n")
    #     if action == '1' or action == '2':
    #         break

    # send the user to the right function

# # running algorithms
# def algorithms():
#
# # visualizing, 2d/ 3d
# def visualizing():

# protein options


if __name__ == "__main__":
    main()

    # input control --> argv needs to be at least 4 long
