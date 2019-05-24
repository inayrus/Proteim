import sys
import copy
sys.path.append('../')
sys.path.append('../Classes')
from Protein import Protein
from helpers import save_best_protein

def depth_first(protein_filename):
    """
    Constructive algorithm that finds solutions by going depth first through
    the whole statespace.
    """
    protein = Protein(protein_filename)
    amino_acids = protein.get_amino_acids()
    best_proteins, stack = ([] for i in range(2))

    # place first two amino acids, bc their placing doesn't matter
    protein.place_first_two()

    # put start protein in the stack
    stack.append(protein)

    iterations = 0

    # --> start loop
    while stack != []:
        # pick the last child off the stack (pop function)
        protein = stack.pop()
        iterations += 1
        print("number of iterations: {}".format(iterations))

        # if next amino exists,
        next_parent_amino = protein.get_next_amino()

        if next_parent_amino:
            # get all the possible places to put the next amino
            all_children = protein.get_kids()

            # put the children on the stack
            for protein_child in all_children:
                stack.append(protein_child)

        # when protein is completed
        else:
            # update stability
            protein.update_stability()

            # call save_best_protein function
            best_proteins = save_best_protein(best_proteins, protein)
