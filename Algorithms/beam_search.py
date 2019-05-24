import sys
import copy
sys.path.append('../Classes')
from Protein import Protein
sys.path.append('../')
from helpers import save_best_protein
from operator import itemgetter
import random

def beam_search(protein_filename, random):
    """
    Algorithm that finds solutions by going breadth first through
    the statespace with a certain beam. The beam is selected out of the lowest
    stabilities when this number is bigger than the beam, they are randomly selected
    """
    protein = Protein(protein_filename)
    amino_acids = protein.get_amino_acids()
    best_proteins, queue, child_stabilities, beamsearch, beam_random = ([] for i in range(5))
    beam = 50

    # place first two amino acids, bc their placing doesn't matter
    protein.place_first_two()

    # put start protein in the queue
    queue.append(protein)

    while queue != []:
        # pick the child in front off the queue
        protein = queue.pop(0)

        # if next amino exists,
        next_parent_amino = protein.get_next_amino()

        # make a list with all proteins and their stabilities
        if next_parent_amino:
                        # get all the possible places to put the next amino
            new_children = protein.get_kids()

            # append the new child to the pre-beam list
            for child in new_children:
                child.update_stability()
                beamsearch.append(child)

            beamsearch.sort()

            # if queue is empty al kids are made
            if queue == []:

                # if beam is bigger than the lengt of beamsearch add beamsearch to queue
                if len(beamsearch) < beam:
                    queue.extend(beamsearch)

                # else pick randomly pick children with best stability
                else:
                    pick_children(beam_random, queue, beamsearch, beam, random)

                    # empty the beamsearch and beam_random list
                    beamsearch, beam_random  = ([] for i in range(2))

        # when protein is completed
        else:
            # save best protein
            best_proteins = save_best_protein(best_proteins, protein)

def pick_children(beam_random, queue, beamsearch, beam, random):
    """
    This functon picks the best children.
    If random = true beam_search with a random factor makes a list of best proteins. 
    This beam search picks randomly the best proteins out of this list.
    If random = false beam_search always picks the first proteins for the length of the beam.
    """
    if random == "true":
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
    else:
        for i in range(beam):
            queue.append(beamsearch[i])
