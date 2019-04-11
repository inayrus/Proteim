import sys
import pathlib
import random
import matplotlib.pyplot as plt
from matplotlib_test import visualize
from Amino import Amino

class Protein(object):
    """Representation of a protein"""

    def __init__(self, file):
        """initializes a protein"""
        self.stability = 0
        self.amino_acids = self.load_protein("ProteinData/{}.txt".format(file))
        self.bonds = []
        self.coordinates = {}

    def load_protein(self, file):
        """
        Reads the protein in from a text file.
        Returns a list of Amino instances
        """
        # read in the file
        with open(file, "r") as f:
            amino_acids = []

            for line in f:
                # get rid of whitespace
                seq = line.strip()

                for index, letter in enumerate(seq):
                    # turn each letter into an Amino object
                    new_amino = Amino(index, letter)

                    # add the new and prev amino to each other's connections
                    if index > 0:
                        prev_amino = amino_acids[index - 1]
                        new_amino.set_connections(prev_amino)
                        prev_amino.set_connections(new_amino)
                        # print(prev_amino.conn)

                    # add the new amino to the list
                    amino_acids.append(new_amino)
        return amino_acids

    def ribosome_fold(self):
        """
        a function that folds the protein by placing its amino acids
        one by one on a grid
        """
        for index, amino in enumerate(self.amino_acids):

            all_places = []

            # place the first amino in location 0,0.
            if index == 0:
                self.coordinates[index] = [amino, [0, 0]]
                amino.set_location([0, 0])

            # for every other amino,
            # 1) loop through the spaces around amino
            else:
                prev_amino, coordinates = self.coordinates[index - 1]
                x, y = coordinates
                all_places = [[x, y + 1], [x, y - 1], [x + 1, y], [x - 1, y]]

                # 2) check the Protein attribute what places are empty
                for prev_aminos, xy in self.coordinates.values():
                    if xy in all_places:
                        all_places.remove(xy)

                # when no places around last amino available, break
                if all_places == []:
                    return []

                # 3) pick one location to place the amino in
                picked_place = random.choice(all_places)
                print(picked_place)

                # 4) update amino location & location Protein attribute
                self.coordinates[index] = [amino, picked_place]
                amino.set_location(picked_place)


            # when all aminos should have been placed:
            # 1) if doodgelopen/ not all amino's placed, do not save
            # 2) if placed without issue:
            #    2a) check bonds of new Protein vs saved Protein.
            #    2b) save location attribute of most stable Protein

            #  return coordinates of the amino's in the protein

        visualize(self.coordinates)
        return self.coordinates


if __name__ == "__main__":

    # ensure that a filename is added to the commandline
    if len(sys.argv) != 2:
        print("give one protein filename to the command line (ex. protein_a1)")
        exit(1)

    # ensure that the file exists in ProteinData
    file = pathlib.Path("ProteinData/{}.txt".format(sys.argv[1]))
    if not file.exists():
        print("please choose a filename that exist in the ProteinData folder")
        exit(1)

    # if all is good, create a protein object
    protein = Protein(sys.argv[1])
    protein.ribosome_fold()
