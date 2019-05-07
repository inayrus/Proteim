import sys
import pathlib
import random
# line below ensures Protein.py can be reached: it exits the Algorithm folder
# and re-enters the Proteim dir, where Protein.py currently is
sys.path.append('../')
from Protein import Protein
from helpers import save_best_protein


def ribosome_loop(protein_filename):
    """
    A loop function where proteins are randomly folded.
    Best proteins are saved in a csv.
    """
    # list variable for the most stable folded proteins
    best_proteins = []

    # fold the protein in a loop
    while True:
        # fold a protein
        protein, is_completed = ribosome_fold(protein_filename)

        # only save completed proteins (ones without dead endings)
        if is_completed:
            # update the best protein list and save the best protein in a csv
            best_proteins = save_best_protein(best_proteins, protein)


def ribosome_fold(protein_filename):
    """
    A function that folds the protein by placing its amino acids
    one by one on a grid, randomly.
    Returns protein object, success boolean (False: protein folded in on itself)
    """
    # initialize a new protein object
    protein = Protein(protein_filename)
    amino_acids = protein.get_amino_acids()

    for index, amino in enumerate(amino_acids):
        # initializes list of all possible plces for new aminoacid
        all_places = []

        # place the first two aminos
        if index == 0:
            protein.place_amino([0, 0], index)
        elif index == 1:
            protein.place_amino([0, 1], index)

        # for the other aminos:
        else:
            # get the possible places for the next amino
            prev_amino = amino_acids[index - 1]
            all_places = protein.get_place_options(prev_amino)

            # stop if last amino is dead ending
            if all_places == []:
                print("Whoops folded in on myself")
                return protein, False

            # 3) pick one location to place the amino in
            picked_place = random.choice(all_places)

            # 4) update amino location & location Protein attribute
            protein.place_amino(picked_place, amino.get_id())

    return protein, True

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
    ribosome_loop(sys.argv[1])

    # for i in range(3**4):
    #     protein = ribosome_fold(sys.argv[1])

    # all_coordinates = protein.get_all_coordinates()
    # all_bonds = protein.update_bonds()
    # stability = protein.update_stability()

    # Visualize the protein
    # protein.visualize()
