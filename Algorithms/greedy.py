sys.path.append('../')
from Protein import Protein
from helpers import save_best_protein
import random

def greedy(protein_filename):
    """
    Constructive algorithm that finds solutions by placing amino acids in a greedy manner.
    """
    protein = Protein(protein_filename)
    amino_acids = protein.get_amino_acids()

    # place first two amino acids, bc their placing doesn't matter
    protein.place_amino([0, 0], 0)
    protein.place_amino([0, 1], 1)

    # put start protein in the queue
    queue.append(protein)

    # --> start loop
    while queue != []:
        # pick the child in front off the queue (pop function)
        protein = queue.pop(0)

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
                    queue.append(protein_child)

            # Start greedy children selection
            # When all children added, pop all - update and compare stability - put best child back
            if queue.length() == 2:
                child_1 = queue.pop(0)
                child_2 = queu.pop(1)

                # Update bonds for children
                child_1.update_bonds()
                child_2.update_bonds()
                # update stability
                child_1.update_stability()
                child_2.update_stability()

                if child_1.get_stability() > child_2.get_stability():
                    queue.append(child_1)
                elif child_2.get_stability() > child_1.get_stability():
                    queue.append(child_2)
                else:
                    # Pick a random child
                    all_children = [child_1, child_2]
                    chosen_child = random.choice(all_children)
                    queue.append(chosen_child)
            elif queue.lenght() == 3:
                child_1 = queue.pop(0)
                child_2 = queue.pop(1)
                child_3 = queue.pop(2)

                # Update bonds for children
                child_1.update_bonds()
                child_2.update_bonds()
                child_3.update_bonds()
                # update stability
                child_1.update_stability()
                child_2.update_stability()
                child_3.update_stability()

                if child_1.get_stability() > child_2.get_stability() and child_1.get_stability() > child_3.get_stability():
                    queue.append(child_1)
                elif child_2.get_stability() > child_1.get_stability() and child_2.get_stability() > child_3.get_stability():
                    queue.append(child_2)
                elif child_3.get_stability() > child_1.get_stability() and child_3.get_stability() > child_2.get_stability():
                    queue.append(child_3)
                else:
                    # Pick a random child
                    all_children = [child_1, child_2, child_3]
                    chosen_child = random.choice(all_children)
                    queue.append(chosen_child)

        # when protein is completed
        else:
        # call save_best_protein function
        best_proteins = save_best_protein(best_proteins, protein)

if __name__ == "__main__":
    greedy(sys.argv[1])
