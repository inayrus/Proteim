import sys
import copy
sys.path.append('../')
from helpers import save_best_protein
from Protein import Protein
from operator import itemgetter
import random
import time


def beam_search_random(protein_filename):
    """
    Constructive algorithm that finds solutions by going breadth first through
    the whole statespace.
    """
    protein = Protein(protein_filename)
    amino_acids = protein.get_amino_acids()
    best_proteins = []
    queue = []
    child_stabilities = []
    beamsearch = []
    beam_random  = []

    beam = 50
    # place first two amino acids, bc their placing doesn't matter
    protein.place_amino([0, 0], 0)
    protein.place_amino([0, 1], 1)

    # put start protein in the queue
    queue.append(protein)

    # --> start loop
    while queue != []:
        # pick the child in front off the queue (pop function)
        protein = queue.pop(0)
        # print("lengte queue: {}".format(len(queue)))

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


            if queue == []:
                if len(beamsearch) < beam:
                    for i in range(len(beamsearch)):
                        queue.append(beamsearch[i])
                else:

                    # get all low stability children
                    while (len(beam_random) + len(queue)) < beam:
                        queue.extend(beam_random)
                        beam_random = []
                        lowest = min(beamsearch)

                        while beamsearch[0].get_stability() == lowest.get_stability() and ((len(beam_random) + len(queue)) < beam):
                            beam_random.append(beamsearch.pop(0))



                    to_add = beam - len(queue)

                    for i in range(to_add):

                        index_to_choose = list(range(0, len(beam_random)))
                        chosen = random.choice(index_to_choose)
                        queue.append(beam_random[chosen])
                    beamsearch = []
                    beam_random = []



        # when protein is completed
        else:
            # call save_best_protein function
            best_proteins = save_best_protein(best_proteins, protein)




if __name__ == "__main__":
    start = time.time ()
    beam_search_random(sys.argv[1])
    end = time. time()
    print(end - start)
