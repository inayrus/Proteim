import sys
import copy
sys.path.append('../Classes')
from Protein import Protein
sys.path.append('../')
from helpers import save_best_protein
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

    # place first two amino acids, bc their placing doesn't matter
    protein.place_first_two()

    # put start protein in the queue
    child_list.append(protein)

    # --> start loop
    while child_list != []:
        # pick the child in front off the queue (pop function)
        protein = child_list[0]

        # if next amino exists,
        next_parent_amino = protein.get_next_amino()

        if next_parent_amino:
            # get all the possible places to put the next amino
            all_places = protein.get_place_options(protein.get_rearmost_amino())

            # only continue if protein hasn't folded into itself
            if all_places != []:
                # for every possible place, copy the current protein and create a child
                for place in all_places:
                    protein_child = copy.deepcopy(protein)

                    # place new amino
                    next_child_amino = protein_child.get_next_amino()
                    protein_child.place_amino(place, next_child_amino.get_id())

                    # put the children in the back of the queue
                    child_list.append(protein_child)
            else:
                return protein, False

            # Start greedy children selection
            stabilities = []
            # Get every child
            for child in child_list:
                # Get child stability
                child.update_bonds()
                child.update_stability()
                stabilities.append(child.get_stability())

            # If more than 1 child
            if len(stabilities) > 1:
                # Get indices of best children
                best_indices = [index for index, stability in enumerate(stabilities)
                                if stability == min(stabilities)]
                # Choose best child or
                chosen_index = random.choice(best_indices)
                child_list = [child_list[chosen_index]]

        # if no more next_amino
        else:
            return protein, True

if __name__ == "__main__":
    greedy_loop(sys.argv[1])
