import sys
import copy
sys.path.append('../Classes')
from Protein import Protein
sys.path.append('../')
from helpers import save_best_protein

def breadth_first(protein_filename):
    """
    Constructive algorithm that finds solutions by going breadth first through
    the whole statespace.
    """
    protein = Protein(protein_filename)
    amino_acids = protein.get_amino_acids()
    best_proteins, queue = ([] for i in range(2))

    # place first two amino acids
    protein.place_first_two()

    # put start protein in the queue
    queue.append(protein)

    while queue != []:
        # pick the child in front off the queue
        protein = queue.pop(0)

        # if next amino exists
        next_parent_amino = protein.get_next_amino()

        if next_parent_amino:
            # get all the possible places to put the next amino
            all_children = protein.get_kids()

            # put the children in the back of the queue
            for protein_child in all_children:
                queue.append(protein_child)

        # when protein is completed
        else:
            protein.update_stability()

            # save best protein
            best_proteins = save_best_protein(best_proteins, protein)
