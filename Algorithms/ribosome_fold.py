import sys
import pathlib
import random
# line below ensures Protein.py can be reached: it exits the Algorithm folder
# and re-enters the Proteim dir, where Protein.py currently is
sys.path.append('../')
from Protein import Protein
from helpers import save_best_protein

def ribosome_fold(protein_filename):
    """
    A function that folds the protein by placing its amino acids
    one by one on a grid.
    Currently folds randomly.
    """
    # initialize a new protein object
    protein = Protein(protein_filename)
    amino_acids = protein.get_amino_acids()
    best_proteins = []

    for index, amino in enumerate(amino_acids):
        # initializes list of all possible plces for new aminoacid
        all_places = []

        # place the first amino in location 0,0.
        if index == 0:
            protein.add_coordinates([0, 0])
            protein.add_amino_place([0, 0], amino)
            amino.set_location([0, 0])

        # for the other aminos:
        else:
            # prevent the protein from folding in on itself
            while all_places == []:
                # 1) loop through the spaces around amino
                all_coordinates = protein.get_all_coordinates()
                coordinates = all_coordinates[index - 1]
                all_places = protein.get_neighbors(coordinates)

                # 2) check the Protein attribute what places are empty
                for xy in all_coordinates:
                    if xy in all_places:
                        all_places.remove(xy)

                # backtrack if last amino is dead ending (place last amino elsewhere)
                if all_places == []:
                    # get remaining places the last amino could have been placed
                    prev_coordinates = all_coordinates[index - 2]
                    remain_places = protein.get_neighbors(prev_coordinates)
                    remain_places.remove(coordinates)

                    # pick a random new place
                    new_place = random.choice(remain_places)

                    # erase the stuck-amino coordinates from datastructures
                    protein.remove_coordinates(coordinates)
                    prev_amino = protein.remove_amino_place(coordinates)

                    # set the new place of last amino in the protein Object
                    protein.add_coordinates(new_place)
                    protein.add_amino_place(new_place, prev_amino)
                    prev_amino.set_location(new_place)

                    # (beginning of loop) to get possible locations for curr amino
                    print("Whoops folded in on myself")

            # 3) pick one location to place the amino in
            picked_place = random.choice(all_places)

            # 4) update amino location & location Protein attribute
            protein.add_coordinates(picked_place)
            amino.set_location(picked_place)
            protein.add_amino_place(picked_place, amino)

        # TODO
        # when all aminos should have been placed:
        # 1) if doodgelopen/ not all amino's placed, do not save
        # 2) if placed without issue:
        #    2a) check bonds of new Protein vs saved Protein.
        #    2b) save location attribute of most stable Protein

        #  return coordinates of the amino's in the protein

    best_proteins = save_best_protein(best_proteins, protein)

    return protein


if __name__ == "__main__":

    # ensure that a filename is added to the commandline
    if len(sys.argv) != 2:
        print("give one protein filename to the command line (ex. protein_a1)")
        exit(1)

    # ensure that the file exists in ProteinData
    file = pathlib.Path("../ProteinData/{}.txt".format(sys.argv[1]))
    if not file.exists():
        print("please choose a filename that exist in the ProteinData folder")
        exit(1)

    # if all is good, run the algorithm
    for i in range(3**4):
        protein = ribosome_fold(sys.argv[1])
    # all_coordinates = protein.get_all_coordinates()
    # all_bonds = protein.set_bonds()
    # stability = protein.set_stability()

    # Visualize the protein
    # protein.visualize()
