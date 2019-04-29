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


    def set_bonds(self):
        """
        Function to store the bonds H's or C's made in the protein
        """
        # loop through the aminos in the protein
        for amino in self.amino_acids:

            # for H's and C's, get neighboring locations
            if amino.get_kind() != 'P':
                amino_location = amino.get_location()
                surroundings = self.get_neighbors(amino_location)

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

    def set_stability(self):
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

    def get_neighbors(self, coordinates):
        """
        A function that returns a list of all coordinates around a certain
        grid point
        """
        x, y = coordinates
        return [[x, y + 1], [x, y - 1], [x + 1, y], [x - 1, y]]


    def visualize(self):
        """
        A function that visualizes the folded protein using matplotlib
        """
        # putting the coordinates in an x and an y list
        x_list, y_list, scat_hx_list, scat_hy_list, scat_px_list, scat_py_list, \
        scat_cx_list, scat_cy_list = ([] for list in range(8))

        for coordinates in self.all_coordinates:
            # unpack the coordinate values
            x, y = coordinates
            x_list.append(x)
            y_list.append(y)

            # group the coordinates of the same amino kinds
            amino = self.amino_places["{}".format(coordinates)]
            amino_kind = amino.get_kind()
            if amino_kind == 'P':
                scat_px_list.append(x)
                scat_py_list.append(y)
            elif amino_kind == 'H':
                scat_hx_list.append(x)
                scat_hy_list.append(y)
            else:
                scat_cx_list.append(x)
                scat_cy_list.append(y)

        # Plot cavalent line
        plt.plot(x_list, y_list, color='black', linestyle='solid', zorder=1)

        # use different colours to visualize the amino kind groups
        plt.scatter(scat_px_list, scat_py_list, color='red', zorder=2)
        plt.scatter(scat_hx_list, scat_hy_list, color='blue', zorder=2)
        plt.scatter(scat_cx_list, scat_cy_list, color='gold', zorder=2)

        # unpack the bonds neighboring_locations
        for bond in self.bonds:
            bonds_x = []
            bonds_y = []
            for bonds_amino in bond:
                x, y = bonds_amino.get_location()
                bonds_x.append(x)
                bonds_y.append(y)

            # plot bond
            plt.plot(bonds_x, bonds_y, color='green', linestyle='--', zorder=1)

        #  set plot axis and show plot
        plt.axis([min(x_list) - 1, max(x_list) + 1, min(y_list) - 1, max(y_list) + 1])
        plt.show()


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
    all_bonds = protein.set_bonds()
    stability = protein.set_stability()
    brute_force_search = protein.brute_force_search()

    # Visualize the protein
    protein.visualize()
