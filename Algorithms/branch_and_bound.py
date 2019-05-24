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

    # place first two amino acids
    protein.place_first_two()

    # put start protein in the stack
    stack.append(protein)

    while stack != []:
        # pick the last child off the stack
        protein = stack.pop()
        next_parent_amino = protein.get_next_amino()

        # if next amino exists
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
                    mean = calculate_mean(total_depth_children, sum)

                    # same or better stability:
                    if child_stability <= best_stabilities[depth]:
                        stack.append(protein_child)
                        # update this depth's best stability
                        best_stabilities[depth] = child_stability
                    # worse than mean stability:
                    elif child_stability > mean:
                        stack = prune_branches(stack, protein_child, "worse")
                    # better than average, worse than best:
                    elif child_stability < mean and child_stability > best_stabilities[depth]:
                        stack = prune_branches(stack, protein_child, "between")

                    # update the average stabilities
                    mean_stabilities[depth] = [sum + child_stability, total_depth_children + 1]

                # all branches of a P amino are kept
                else:
                    stack.append(protein_child)

        # when protein is completed
        else:
            counter += 1
            protein.update_stability()

            # save best protein
            best_proteins = save_best_protein(best_proteins, protein)

def calculate_mean(total_depth_children, sum):
    """
    Calculate mean stability at a certain depth.
    """
    if sum != 0:
        mean = sum / total_depth_children
    else:
        mean = 0

    return mean

def prune_branches(stack, protein_child, prune):
    """
    This function decides of a child is pruned or appended to the stack.
    Returns the stack.
    """
    # initialize prune probabilities
    p_worse = 0.8
    p_between = 0.5

    if prune == "worse":
        chance = p_worse
    else:
        chance = p_between

    # draw random number 0-1
    ran_num = random.uniform(0, 1)
    if ran_num > chance:
        stack.append(protein_child)

    return stack
