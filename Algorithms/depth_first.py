import sys
import copy
sys.path.append('../')
from helpers import save_best_protein
from Protein import Protein

def depth_first(protein_filename):
    """
    """
    protein = Protein(protein_filename)
    amino_acids = protein.get_amino_acids()
    best_proteins = []
    stack = []

    # place first two amino acids, bc their placing doesn't matter
    protein.place_amino([0, 0], amino_acids[0])
    protein.place_amino([0, 1], amino_acids[1])

    # put start protein in the stack
    stack.append(protein)

    # --> start loop
    while stack != []:
        # pick the last child off the stack (pop function)
        protein = stack.pop()
        print(len(stack))

        # if next amino exists,
        next_amino = protein.get_next_amino()

        if next_amino:
            # get all the possible places to put the next amino
            all_places = protein.get_place_options(protein.get_rearmost_amino())

            # only continue if protein hasn't folded into itself
            if all_places != []:
                # for every possible place, copy the current protein and create a child
                for place in all_places:
                    protein_child = copy.deepcopy(protein)
                    # place new amino
                    protein_child.place_amino(place, next_amino)

                    # update bonds for every new child
                    protein_child.update_bonds()
                    # update stability
                    protein_child.update_stability()

                    # put the children on the stack
                    stack.append(protein_child)

        # when protein is completed
        else:
            # call save_best_protein function
            best_proteins = save_best_protein(best_proteins, protein)

if __name__ == "__main__":
    depth_first(sys.argv[1])
