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
        # if no csv, best_stability = 0
        file = get_file()
        if not file.exists():
            best_stability = 0
        else:
            # load all the proteins that are saved in csv
            best_proteins = load_from_csv(file)
            # get the stability
            best_stability = best_proteins[0].get_stability()
    else:
        best_stability = best_proteins[0].get_stability()


    # if the stabilities are the same and protein is not yet in list, append
    if best_stability == new_stability:

        # loop over all the best proteins
        for best in best_proteins:
            best_coordinates = best.get_all_coordinates()
            new_coordinates = new_protein.get_all_coordinates()
            same = 0
            past_proteins = 0

            # check if the coordinates match
            for index, best_coordinate in enumerate(best_coordinates):
                print("in for loop 2")
                if best_coordinate == new_coordinates[index]:
                    same += 1

            # if the coordinates of a whole protein match, stop loop, don't save
            if same == len(best_coordinates):
                break
            # remember how many non matching proteins have passed
            else:
                past_proteins += 1

            # only save the new protein when looped through all best proteins
            if past_proteins == len(best_proteins):
                best_proteins.append(new_protein)
                save_in_csv(new_protein, "append")


    # overwrite list if there is a lower protein stabilty
    elif best_stability > new_stability:
        best_proteins = [new_protein]
        save_in_csv(best_proteins, "write")

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
    # data to write:
    data = []
    # for protein in proteins:
    data.append([protein.get_stability(), protein.get_all_coordinates(),
                     protein.get_amino_places(), protein.get_bonds()])

    #  write data if file doesn't exist or it got a write argument
    if not file.exists() or write_or_append == "write":
        with file.open(mode='w') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerows(data)
    # append data if it got an append argument
    else:
        with file.open(mode='a') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerows(data)

    return protein.get_stability()


def load_from_csv(file):
    """
    Recreates a protein object from a csvfile.
    Returns the protein object

    --> ISSUE: ast can't read the way the bonds are represented.
               might need to change the Amino __repr__
    """
    best_proteins = []
    protein_name = sys.argv[1]

    # create new protein object
    protein = Protein(protein_name)

    # read the csvfile
    with file.open('r') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=",")

        # split the data in each row
        for row in csv_reader:
            if row != []:
                stability = int(row[0])
                all_coordinates = ast.literal_eval(row[1])
                amino_places = ast.literal_eval(row[2])
                # bonds = ast.literal_eval(row[3])

                # set the data as protein attributes
                protein.set_stability(stability)
                protein.set_all_coordinates(all_coordinates)
                protein.set_amino_places(amino_places)
                # protein.set_bonds(bonds)

                # append the protein to the best proteins list
                best_proteins.append(protein)
    return best_proteins


def get_file():
    """
    Function that returns a path for a results csv file
    """
    # save algorithm name and protein name from args to create csv filename
    algorithm_split = sys.argv[0].split(".")
    algrm = algorithm_split[0]
    protein_name = sys.argv[1]

    # create path
    file = pathlib.Path("../Results/{}/{}_{}.csv".format(algrm, algrm, protein_name))

    return file


# if __name__ == "__main__":
#     algrm = "ribosome_fold"
#     protein_name = "protein_a1"
#     file = pathlib.Path("Results/{}/{}_{}.csv".format(algrm, algrm, protein_name))
#     best_proteins = load_from_csv(file)
#     print(best_proteins)
