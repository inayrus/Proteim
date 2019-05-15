import sys
import copy
sys.path.append('../')
from helpers import save_best_protein
from Protein import Protein
from operator import itemgetter
import time

def beam_search(protein_filename):
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
                    # print("len beamsearch : {}".format(len(beamsearch)))
                    # child_stabilities.append(protein_child.get_stability())

                beamsearch.sort()
                # print("beamsearch list : {}".format(beamsearch))
                # print("len beamsearch : {}".format(len(beamsearch)))

                #  list of protein stabilities
                # child_stabilities = [child.get_stability() for child in beamsearch

            if queue == []:
                # print("lengte: {}".format(len(beamsearch)))
                # while len(queue) != beam and child_stabilities != []:
                if len(beamsearch) < beam:
                    for i in range(len(beamsearch)):
                        queue.append(beamsearch[i])
                else:
                    for i in range(beam):
                        queue.append(beamsearch[i])
                beamsearch = []




                    #
                    # print("child stab: {}".format(child_stabilities))
                    #
                    # # get index of lowest child_stabilities
                    # minimum = min(child_stabilities)
                    # min_index = child_stabilities.index(minimum)
                    #
                    # # remove stability from list
                    # child_stabilities.pop(min_index)
                    #
                    # # get the protein child with this lowest stability
                    # low_child = beamsearch.pop(min_index)
                    #
                    # # append child to queue
                    # queue.append(low_child)
                    # print("queue: {}".format(queue))
                    # breakpoint()


        # when protein is completed
        else:
                    # call save_best_protein function
            best_proteins = save_best_protein(best_proteins, protein)




if __name__ == "__main__":
    start = time.time()
    beam_search(sys.argv[1])
    end = time. time()
    print(end - start)
