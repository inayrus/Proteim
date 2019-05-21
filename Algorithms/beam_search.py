import sys
import copy
sys.path.append('../Classes')
from Protein import Protein
sys.path.append('../')
from helpers import save_best_protein
from operator import itemgetter

def beam_search(protein_filename):
    """
    Algorithm that finds solutions by going breadth first through
    the statespace with a certain beam
    """
    protein = Protein(protein_filename)
    amino_acids = protein.get_amino_acids()
    best_proteins, queue, child_stabilities, beamsearch = ([] for i in range(4))
    beam = 1000
    # place first two amino acids, bc their placing doesn't matter
    protein.place_first_two()

    # put start protein in the queue
    queue.append(protein)

    # --> start loop
    while queue != []:
        # pick the child in front off the queue (pop function)
        protein = queue.pop(0)

        # if next amino exists,
        next_parent_amino = protein.get_next_amino()

        # make a list with all proteins and their stabilities
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

                    # append the new child to the pre-beam list
                    protein_child.update_stability()
                    beamsearch.append(protein_child)

                beamsearch.sort()

            # if queue is empty al kids are made, add the best kids (in rnage beam) to the queue
            if queue == []:
                if len(beamsearch) < beam:
                    for i in range(len(beamsearch)):
                        queue.append(beamsearch[i])

                else:
                    for i in range(beam):
                        queue.append(beamsearch[i])

                beamsearch = []

        # when protein is completed
        else:
            # call save_best_protein function
            best_proteins = save_best_protein(best_proteins, protein)
