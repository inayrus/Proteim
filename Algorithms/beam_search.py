import sys
import copy
sys.path.append('../')
from helpers import save_best_protein
from Protein import Protein
from operator import itemgetter

def breadth_first(protein_filename):
    """
    Constructive algorithm that finds solutions by going breadth first through
    the whole statespace.
    """
    protein = Protein(protein_filename)
    amino_acids = protein.get_amino_acids()
    best_proteins = []
    queue = []
    beam = 4

    # place first two amino acids, bc their placing doesn't matter
    protein.place_amino([0, 0], 0)
    protein.place_amino([0, 1], 1)

    # put start protein in the queue
    queue.append(protein)

    # --> start loop
    while queue != []:
        beamsearch = []
        # pick the child in front off the queue (pop function)
        protein = queue.pop(0)
        print(len(queue))

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

                    for i in range(len(queue)):
                        queue[i].update_bonds()
                        queue[i].update_stability()
                        beamsearch.append(queue[i])


                    # print("beamsearch before sort: {}".format(beamsearch))
                    #
                    # # sort the list
                    # beamsearch.sort()
                    # print("beamsearch after sort: {}".format(beamsearch))

                    # is the beam is bigger thand the list, the queue is the same as the beamsearch
                    if beam > len(beamsearch):
                        for i in range(beamsearch):
                            queue.append(beamsearch[i])
                    # else only append the most negative proteins to the queue
                    else:
                        for i in range(beam):
                            queue.append(beamsearch[i])



        # when protein is completed
        else:
            # update bonds for every new child
            protein.update_bonds()
            # update stability
            protein.update_stability()

            # call save_best_protein function
            best_proteins = save_best_protein(best_proteins, protein)




if __name__ == "__main__":
    breadth_first(sys.argv[1])
