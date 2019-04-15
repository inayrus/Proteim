import sys
import pathlib
import csv

def save_best_protein(best_proteins, new_protein):
    """
    A function that saves the protein with the lowest stability.
    Returns a list with the best proteins objects.
    """
    # remember the stabilities in variables
    new_protein.set_bonds()
    new_stability = new_protein.set_stability()

    # create a variable for the best stability
    if best_proteins == []:
        # take the stabilty of protein in csv file for comparison
        # if no csv, best_stability = 0
        file = get_file()
        if not file.exists():
            best_stability = 0
        else:
            with file.open(mode='r') as f:
                for line in f:
                    protein_data = line.split(',')
                    best_stability = int(protein_data[0])
                    break
    else:
        best_stability = best_proteins[0].get_stability()

    # if the stabilities are the same and protein is not yet in list, append
    if best_stability == new_stability:
        if new_protein not in best_proteins:
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
