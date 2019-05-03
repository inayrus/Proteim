import sys
sys.path.append('../')
import pathlib
import random
import matplotlib.pyplot as plt
from Amino import Amino

class Protein(object):
    """Representation of a protein"""

    def __init__(self, file):
        """initializes a protein"""
        self.stability = 0
        self.amino_acids = self.load_protein(file)
        self.bonds = []
        self.all_coordinates = []
        self.amino_places = {}

    def load_protein(self, file):
        """
        Reads the protein in from a text file.
        Returns a list of Amino instances
        """
        # ensure the file can be found despite the directory that the user is in
        filepath = pathlib.Path("ProteinData/{}.txt".format(file))
        if not filepath.exists():
            p = pathlib.Path("../ProteinData/{}.txt".format(file))
            filepath = p.resolve()

        # read in the file
        with filepath.open('r') as f:
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

    def update_bonds(self):
        """
        Function to store the bonds H's or C's made in the protein
        """
        # loop through the aminos in the protein
        for amino in self.amino_acids:
            num_placed = len(self.all_coordinates)

        for index in range(num_placed - 1):
            amino = self.amino_acids[index]
            print(amino)

        for index in range(num_placed - 1):
            amino = self.amino_acids[index]
            print(amino)

            # for H's and C's, get neighboring locations
            if amino.get_kind() != 'P':
                surroundings = self.get_neighbors(amino)

                # remove location of connected amino's
                for conn_amino in amino.get_conn():
                    conn_location = conn_amino.get_location()
                    if conn_location in surroundings:
                        surroundings.remove(conn_location)

                for location in surroundings:
                    # check if location is in dict and the new amino is H or C
                    str_location = "{}".format(location)
                    if str_location in self.amino_places and \
                       self.amino_places[str_location].get_kind() != 'P':

                       # check if current bond is already stored
                        bonded_amino = self.amino_places[str_location]
                        if [amino, bonded_amino] not in self.bonds and \
                           [bonded_amino, amino] not in self.bonds:

                            # if not, add bond to attribute
                            self.bonds += [[amino, bonded_amino]]

        print("bonds: {}".format(self.bonds))
        return self.bonds

    def set_bonds(self, bonds):
        """
        Sets the bonds attribute to a certain value.
        """
        self.bonds = bonds

    def update_stability(self):
        """
        A function that sets the stability of the protein
        """
        # Check all bonds and get kinds of bonded amino's
        for bond in self.bonds:
            amino, other_amino = bond
            amino = amino.get_kind()
            other_amino = other_amino.get_kind()

            # Set stability to -1 of -5 depending on bond
            if amino == "H" or other_amino == "H":
                self.stability -= 1
            elif amino == "C" and other_amino == "C":
                self.stability -= 5

        print(self.stability)
        return self.stability

    def set_stability(self, stability):
        """
        Sets the stability attribute to a certain value.
        """
        self.stability = stability

    def add_coordinates(self, coordinate):
        """
        A function that adds a coordinate to the list of all used coordinates
        in the protein
        """
        self.all_coordinates += [coordinate]

    def remove_coordinates(self, coordinate):
        """
        A function that removes a coordinate from the list of all used coordinates
        in the protein
        """
        self.all_coordinates.remove(coordinate)

    def set_all_coordinates(self, coordinates):
        """
        Sets the coordinates attribute to a certain value.
        """
        self.all_coordinates = coordinates

    def add_amino_place(self, coordinate, amino):
        """
        A function that links an Amino to its coordinates
        {'coordinates': Amino}
        """
        self.amino_places["{}".format(coordinate)] = amino

    def remove_amino_place(self, coordinate):
        """
        A function that deletes a coordinate key from the dict
        Returns the removed amino
        """
        return self.amino_places.pop("{}".format(coordinate))

    def set_amino_places(self, amino_places):
        """
        Sets the amino places attribute to a certain value.
        """
        self.amino_places = amino_places

    def get_neighbors(self, amino):
        """
        A function that returns a list of all coordinates around a certain
        grid point
        """
        coordinates = amino.get_location()
        x, y = coordinates
        return [[x, y + 1], [x, y - 1], [x + 1, y], [x - 1, y]]

    def get_place_options(self, amino):
        """
        Returns a list with the optional coordinates to place next amino in
        """
        # 1) loop through the spaces around amino
        all_places = self.get_neighbors(amino)

        # 2) check the Protein attribute what places are empty
        for xy in self.get_all_coordinates():
            if xy in all_places:
                all_places.remove(xy)
        return all_places

    def get_next_amino(self):
        """
        Returns the first amino that's not yet placed
        """
        # get the number of placed amino's
        num_placed = len(self.all_coordinates)

        if num_placed < len(self.amino_acids):
            next_amino = self.amino_acids[num_placed]
            return next_amino
        # there is no next amino
        else:
            return None

    def get_rearmost_amino(self):
        """
        Returns the last placed amino.

        --> problem is dat there are 7 coordinates in the list, meaning there
        should be 7 placed amino's. however, the 7th amino's coor are empty.
        So where is that 7th coordinate in the list coming from?

        --> problem 2: the coordinates list doesn't make sense:
        [[0, 0], [0, 1], [-1, 1], [2, 1], [2, 0], [0, -1], [2, -2]]

        --> problem 3: the 6th amino's location doesn't even exist in the list
        """
        num_placed = len(self.all_coordinates)
        print("all_coordinates: {}".format(self.all_coordinates))
        amino = self.amino_acids[num_placed - 1]
        prev_amino = self.amino_acids[num_placed - 2]
        print("rearmost amino: {}".format(amino))
        print("rearmost amino coor: {}".format(amino.get_location()))
        print("prev amino coor: {}".format(prev_amino.get_location()))
        return amino

    def place_amino(self, coordinates, amino):
        """
        Places an amino on given coordinates.
        """
        self.add_coordinates(coordinates)
        self.add_amino_place(coordinates, amino)
        amino.set_location(coordinates)


    # some getters the algorithms are allowed to access
    def get_stability(self):
        """
        Returns the protein's stability (int)
        """
        return self.stability

    def get_amino_acids(self):
        """
        Returns a list with all Amino objects in this Protein
        """
        return self.amino_acids

    def get_bonds(self):
        """
        Returns a list with all bonds between H and C amino acids
        [Amino object 1, Amino object 2]
        """
        return self.bonds

    def get_all_coordinates(self):
        """
        Returns a list with all coordinates in this protein configuarion
        """
        return self.all_coordinates

    def get_amino_places(self):
        """
        Returns a dict for all locations of the amino acids
        {'coordinate': Amino object}
        """
        return self.amino_places


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
    all_coordinates = protein.ribosome_fold()
    all_bonds = protein.update_bonds()
    stability = protein.update_stability()
    brute_force_search = protein.brute_force_search()

    # Visualize the protein
    protein.visualize()
