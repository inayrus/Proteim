import sys
import pathlib
import random
import csv
import statistics
sys.path.append('../Classes')
from Protein import Protein
sys.path.append('../')
from helpers import save_best_protein


def random_loop(protein_filename):
    """
    A loop function where proteins are randomly folded.
    Best proteins are saved in a csv.
    """
    # list variable for the most stable folded proteins
    best_proteins = []

    # fold the protein in a loop
    while True:
        # fold a protein
        protein, is_completed = random_fold(protein_filename)

        # only save completed proteins (ones without dead endings)
        if is_completed:
            # update the best protein list and save the best protein in a csv
            best_proteins = save_best_protein(best_proteins, protein)


def random_fold(protein_filename):
    """
    A function that folds the protein by placing its amino acids
    one by one on a grid, randomly.
    Returns protein object, success boolean (False: protein folded in on itself)
    """
    # initialize a new protein object
    protein = Protein(protein_filename)
    amino_acids = protein.get_amino_acids()

    # place first 2 aminos
    protein.place_first_two()

    # for the other aminos:
    next_amino = protein.get_next_amino()

    while next_amino:
        # get all the possible places to put the next amino
        all_places = protein.get_place_options(protein.get_rearmost_amino())

        # stop if last amino is dead ending
        if all_places == []:
            return protein, False

        # pick one location to place the amino in
        picked_place = random.choice(all_places)

        # update amino location & location Protein attribute
        protein.place_amino(picked_place, next_amino.get_id())

        # get the next amino
        next_amino = protein.get_next_amino()

    return protein, True


def save_for_mean(protein, stabilities):
    """Saves the stability in a csv"""
    file = pathlib.Path("../MeansData/{}_1000.csv".format(sys.argv[1]))

    # the data to save
    data = [protein.get_stability()]

    #  write data if file doesn't exist
    if not file.exists():
        with file.open(mode='w') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow(data)
    else:
        with file.open(mode='a') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow(data)
            
    # append stability to list
    stabilities.append(protein.get_stability())
