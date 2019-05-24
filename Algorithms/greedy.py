import sys
import copy
sys.path.append('../')
from helpers import save_best_protein
sys.path.append('Classes/')
from Protein import Protein
import random

def greedy_loop(protein_filename):
    """
    A loop function where proteins are folded with greedy.
    Best proteins are saved in a csv.
    """
    # list variable for the most stable folded proteins
    best_proteins = []

    # fold the protein in a loop
    for i in range(1500):
        # fold a protein
        protein, is_completed = greedy(protein_filename)

        # only save completed proteins (ones without dead endings)
        if is_completed:
            # update the best protein list and save the best protein in a csv
            best_proteins = save_best_protein(best_proteins, protein)

def greedy(protein_filename):
    """
    Constructive algorithm that finds solutions by placing amino acids in a greedy manner.
    """
    protein = Protein(protein_filename)
    amino_acids = protein.get_amino_acids()
    child_list = []

    # place first two amino acids
    protein.place_first_two()

    # put start protein in the queue
    child_list.append(protein)

    while child_list != []:
        # pick the child in front off the queue
        protein = child_list[0]

        # if next amino exists
        next_parent_amino = protein.get_next_amino()

        if next_parent_amino:
            # GEt al possible children
            child_list = protein.get_kids()

            # if child folds into itself retun false
            if child_list == []:
                return protein, False

            # start greedy children selection
            stabilities = []
            # get every child
            for child in child_list:
                child.update_stability()
                stabilities.append(child.get_stability())

            # if more than 1 child
            if len(stabilities) > 1:
                # get indices of best children
                best_indices = [index for index, stability in enumerate(stabilities)
                                if stability == min(stabilities)]
                # Choose best child
                chosen_index = random.choice(best_indices)
                child_list = [child_list[chosen_index]]

        # if no more next_amino
        else:
            return protein, True
