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
            # with file.open(mode='r') as f:
            #     for line in f:
            #         protein_data = line.split(',')
            #         best_stability = int(protein_data[0])
            #         break

            # load all the proteins that are saved in csv
            best_proteins = load_from_csv(file)
            # get the stability
            best_stability = best_proteins[0].get_stability()
    else:
        best_stability = best_proteins[0].get_stability()

    # if the stabilities are the same and protein is not yet in list, append
    
    if best_stability == new_stability:
        print("in if + {}".format(best_proteins))
        for best in best_proteins:
            print("in for loop 1")
            x= 0
            for i in range(len(new_protein.get_all_coordinates())):
                print("in for loop 2")
                print(best.get_all_coordinates()[i])
                if best.get_all_coordinates()[i] == new_protein.get_all_coordinates()[i]:
                    x = x + 1
            if x != len(new_protein.get_all_coordinates()):
                best_proteins.append(new_protein)
                save_in_csv(best_proteins, "append")

    # overwrite list if there is a lower protein stabilty
    elif best_stability > new_stability:
        best_proteins = [new_protein]
        save_in_csv(best_proteins, "write")

    print("new stability: ","{}".format(new_stability))
    print("best stability: ","{}".format(best_stability))

    return best_proteins


def save_in_csv(proteins, write_or_append):
    """
    A function that writes a protein to a csv file.
    The protein will be saved in the Results folder, under the name:
    'algorithm_protein_filename.csv'
    """
    file = get_file()

    print(write_or_append)
    # data to write:
    data = []
    for protein in proteins:
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

    return proteins[0].get_stability()


def load_from_csv(file):
    """
    Recreates a protein object from a csvfile.
    Returns the protein object
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
                stability = row[0]
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
