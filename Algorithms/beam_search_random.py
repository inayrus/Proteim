import sys
import copy
sys.path.append('../Classes')
from Protein import Protein
sys.path.append('../')
from helpers import save_best_protein
from operator import itemgetter
import random

def beam_search_random(protein_filename):
    """
    Algorithm that finds solutions by going breadth first through
    the statespace with a certain beam. The beam is selected out of the lowest
    stabilities when this number is bigger than the beam, they are randomly selected
    """
    protein = Protein(protein_filename)
    amino_acids = protein.get_amino_acids()
    best_proteins, queue, child_stabilities, beamsearch, beam_random = ([] for i in range(5))
    beam = 100

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

            # if queue is empty al kids are made
            if queue == []:
                # if beam is bigger than the lengt of beamsearch add beamsearch to queue
                if len(beamsearch) < beam:
                    queue.extend(beamsearch)

                else:
                    # get all low stability children
                    while (len(beam_random) + len(queue)) < beam:
                        queue.extend(beam_random)
                        beam_random = []
                        lowest = min(beamsearch)


                        while beamsearch[0].get_stability() == lowest.get_stability() and ((len(beam_random) + len(queue)) < beam):
                            beam_random.append(beamsearch.pop(0))

                    # to add is the nummber of kids that still has to be added to the queue
                    to_add = beam - len(queue)
                    # pick random the to_add and add those to the queue
                    sampling = random.choices(beam_random, k=to_add)
                    queue.extend(sampling)

                    beamsearch, beam_random  = ([] for i in range(2))

        # when protein is completed
        else:
            # call save_best_protein function
            best_proteins = save_best_protein(best_proteins, protein)
