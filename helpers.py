import sys
import pathlib
import csv
import ast
from Protein import Protein

def save_best_protein(best_proteins, new_protein):
    """
    A function that saves the protein with the lowest stability.
    Returns a list with the best proteins objects.
    """
    # remember the stabilities in variables
    new_protein.update_bonds()
    new_stability = new_protein.update_stability()

    # create a variable for the best stability
    if best_proteins == []:
        # take the stabilty of protein in csv file for comparison
        file = get_file()
        if not file.exists():
            best_stability = 0
        else:
            # load all the proteins that are saved in csv
            best_proteins = load_from_csv(file)
            best_stability = best_proteins[0].get_stability()
    else:
        best_stability = best_proteins[0].get_stability()

    # only append proteins with same stabilities if they're folded differently
    if best_stability == new_stability:
        if not is_duplicate(best_proteins, new_protein):
                best_proteins.append(new_protein)
                save_in_csv(new_protein, "append")

    # overwrite list if there is a lower protein stabilty
    elif best_stability > new_stability:
        best_proteins = [new_protein]
        save_in_csv(new_protein, "write")

    print("new stability: ","{}".format(new_stability))
    print("best stability: ","{}".format(best_stability))

    return best_proteins


def save_in_csv(protein, write_or_append):
    """
    A function that writes a protein to a csv file.
    The protein is saved in the Results folder, under the name:
    'algorithm_protein_filename.csv'
    """
    file = get_file()

    print(write_or_append)
    amino_places = protein.get_amino_places()
    bonds = protein.get_bonds()

    # objects can't be saved in a csv:
    # change the values in amino_places from amino Object to 'H'/'C'/'P'
    for key, amino in amino_places.items():
        kind = amino.get_kind()
        amino_places[key] = kind

    # store the coordinates in bonds variable instead of amino Objects
    for index, bonded_aminos in enumerate(bonds):
        # get the coordinates of the aminos
        amino_1, amino_2 = bonded_aminos
        coordinates = [amino_1.get_location(), amino_2.get_location()]
        # rewrite the list with the coordinates
        bonds[index] = coordinates

    # the data to save
    data = [protein.get_stability(), protein.get_all_coordinates(),
            amino_places, bonds]

    #  write data if file doesn't exist or it got a write argument
    if not file.exists() or write_or_append == "write":
        with file.open(mode='w') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow(data)
    # append data if it got an append argument
    else:
        with file.open(mode='a') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow(data)

    return protein.get_stability()


def load_from_csv(file, protein_name=sys.argv[1]):
    """
    Recreates a protein object from a csvfile.
    protein_name arg is optional, but its default is sys.argv[1].
    This default is used when running a algorithms,
    but it's specified when visualizing a protein (visualize_csv)

    Returns the protein object.
    """
    best_proteins = []

    # read the csvfile
    with file.open('r') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=",")

        # split the data in each row
        for row in csv_reader:
            if row != []:
                # create new protein object
                protein = Protein(protein_name)

                # read the data into the original data structures
                stability = int(row[0])
                all_coordinates = ast.literal_eval(row[1])
                amino_places = ast.literal_eval(row[2])
                bonds = ast.literal_eval(row[3])

                # set the data as protein attributes
                protein.set_stability(stability)
                protein.set_all_coordinates(all_coordinates)
                protein.set_amino_places(amino_places)
                protein.set_bonds(bonds)

                # append the protein to the best proteins list
                best_proteins.append(protein)
    return best_proteins


def is_duplicate(best_proteins, new_protein):
    """
    Checks if a certain protein folding has been made before.
    Returns a bool.
    """
    # loop over all the best proteins
    for best in best_proteins:
        best_coordinates = best.get_all_coordinates()
        new_coordinates = new_protein.get_all_coordinates()
        same = 0
        past_proteins = 0

        # check if the coordinates match
        for index, best_coordinate in enumerate(best_coordinates):
            if best_coordinate == new_coordinates[index]:
                same += 1

        # if all coordinates are similar, the new protein is a duplicate
        if same == len(best_coordinates):
            return True
    # only no duplicates when looped through all existing proteins
    return False


def get_file():
    """
    Function that returns a path for a results csv file.
    Values will be retrieved from the command line,
    assuming the usage: "python algorithm.py protein_name".
    """
    # construct csv filename from commandline args
    algorithm_split = sys.argv[0].split(".")
    algrm = algorithm_split[0]
    protein_name = sys.argv[1]

    # create path
    file = pathlib.Path("../Results/{}/{}_{}.csv".format(algrm, algrm, protein_name))

    return file
