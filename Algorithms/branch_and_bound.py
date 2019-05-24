import sys
import copy
import random
sys.path.append('../Classes')
from Protein import Protein
sys.path.append('../')
from helpers import save_best_protein

def branch_and_bound(protein_filename):
    """
    An algorithm that goes depth first through the statespace and prunes branches
    that seem unlikely to produce the optimal score with a certain probability.
    """
    protein = Protein(protein_filename)
    amino_acids = protein.get_amino_acids()
    best_proteins, stack= ([] for i in range(2))

    counter = 0

    # initialize a mean stability and best stability as a list of zeroes
    len_protein = len(amino_acids)
    best_stabilities = [0] * len_protein
    mean_stabilities = [[0, 0]] * len_protein

    # initialize prune probabilities
    p_worse = 0.8
    p_between = 0.5

    # place first two amino acids
    protein.place_first_two()

    # put start protein in the stack
    stack.append(protein)

    while stack != []:
        # pick the last child off the stack
        protein = stack.pop()

        # if next amino exists,
        next_parent_amino = protein.get_next_amino()

        if next_parent_amino:

            # remember the current amino depth
            depth = len(protein.get_all_coordinates())

            # get all the possible places to put the next amino
            all_children = protein.get_kids()

            # get the new child amino
            for protein_child in all_children:
                next_child_amino = protein_child.get_rearmost_amino()

                kind = next_child_amino.get_kind()

                # pseudo-place amino and update the stability
                child_stability = protein_child.update_stability()

                # pruning only applicable when a H or C is to be placed.
                if kind != 'P':
                    # calculate mean stability
                    sum, total_depth_children = mean_stabilities[depth]
                    if sum != 0:
                        mean = sum / total_depth_children
                    else:
                        mean = 0

                    # same or better stability: put child on stack
                    if child_stability <= best_stabilities[depth]:
                        stack.append(protein_child)
                        # update this depth's best stability
                        best_stabilities[depth] = child_stability
                    # worse than mean stability: prune with probability
                    elif child_stability > mean:
                        # draw random number 0-1
                        ran_num = random.uniform(0, 1)
                        if ran_num > p_worse:
                            stack.append(protein_child)
                    # better than average, worse than best: prune with p
                    elif child_stability < mean and child_stability > best_stabilities[depth]:
                        # draw random number 0-1
                        ran_num = random.uniform(0, 1)
                        if ran_num > p_between:
                            stack.append(protein_child)

                    # update the average stabilities
                    mean_stabilities[depth] = [sum + child_stability, total_depth_children + 1]

                # all branches of a P amino are kept
                else:
                    stack.append(protein_child)

        # when protein is completed
        else:
            # increase counter
            counter += 1

            # update stability
            protein.update_stability()

            # call save_best_protein function
            best_proteins = save_best_protein(best_proteins, protein)
