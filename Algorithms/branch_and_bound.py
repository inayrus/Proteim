import sys
import copy
import random
sys.path.append('../')
from helpers import save_best_protein
from Protein import Protein
import time

def branch_and_bound(protein_filename):
    """
    An algorithm that goes depth first through the statespace and prunes branches
    that seem unlikely to produce the optimal score with a certain probability.
    """
    protein = Protein(protein_filename)
    amino_acids = protein.get_amino_acids()
    best_proteins = []
    stack = []

    # initialize a mean stability and best stability as a list of zeroes
    len_protein = len(amino_acids)
    best_stabilities = [0] * len_protein
    mean_stabilities = [[0, 0]] * len_protein

    # initialize prune probabilities
    p_worse = 0.8
    p_between = 0.5

    # place first two amino acids, bc their placing doesn't matter
    protein.place_amino([0, 0], 0)
    protein.place_amino([0, 1], 1)

    # put start protein in the stack
    stack.append(protein)

    while stack != []:
        # pick the last child off the stack (pop function)
        protein = stack.pop()

        # if next amino exists,
        next_parent_amino = protein.get_next_amino()

        if next_parent_amino:
            # get all the possible places to put the next amino
            all_places = protein.get_place_options(protein.get_rearmost_amino())

            # only continue if protein hasn't folded into itself
            if all_places != []:
                # remember the current amino depth
                depth = len(protein.get_all_coordinates())

                # for every possible place, copy the current protein and create a child
                for place in all_places:
                    protein_child = copy.deepcopy(protein)

                    # get the new child amino
                    next_child_amino = protein_child.get_next_amino()
                    kind = next_child_amino.get_kind()

                    # pseudo-place amino and update the stability
                    protein_child.place_amino(place, next_child_amino.get_id())
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

                        # UPDATE THE AVERAGE STABILITIES
                        mean_stabilities[depth] = [sum + child_stability, total_depth_children + 1]

                    # all branches of a P amino are kept
                    else:
                        stack.append(protein_child)

        # when protein is completed
        else:
            # update bonds for every new child
            protein.update_bonds()
            # update stability
            protein.update_stability()

            # call save_best_protein function
            best_proteins = save_best_protein(best_proteins, protein)

if __name__ == "__main__":
    start = time.time()
    branch_and_bound(sys.argv[1])
    end = time. time()
    print(end - start)
