import sys
import pathlib
import random
import matplotlib.pyplot as plt
from Amino import Amino

class Protein(object):
    """Representation of a protein"""

    def __init__(self, file):
        """initializes a protein"""
        self.stability = 0
        self.amino_acids = self.load_protein("ProteinData/{}.txt".format(file))
        self.bonds = []
        self.all_coordinates = []
        self.amino_places = {}

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

    def brute_force_search(self):
        """
        A function that makes all proteins and saves the protein with the lowest stability
        """
        # TODO make a proteins
        # if folded in on itself skip this one move on to new protein
        # if list empty, Save that protein to list
        # if current stability>stability in x_list delete list and append
        # if smaller do nothing
        # if not empty: check stability
        # if same, check coordinates
        # if same do nothing

    def ribosome_fold(self):
        """
        A function that folds the protein by placing its amino acids
        one by one on a grid
        """
        for index, amino in enumerate(self.amino_acids):
            # initializes list of all possible plces for new aminoacid
            all_places = []

            # place the first amino in location 0,0.
            if index == 0:
                self.all_coordinates += [[0, 0]]
                amino.set_location([0, 0])
                self.amino_places["[0, 0]"] = amino

            # for the other aminos:
            # 1) loop through the spaces around amino
            else:
                coordinates = self.all_coordinates[index - 1]
                all_places = self.get_neighbors(coordinates)

                # 2) check the Protein attribute what places are empty
                for xy in self.all_coordinates:
                    if xy in all_places:
                        all_places.remove(xy)

                # when no places around last amino available, break
                if all_places == []:
                    # TODO
                    # Breadth of depth first search implementeren
                    # Tegen doodlopen
                    print("Whoops folded in on myself")
                    exit(1)

                # 3) pick one location to place the amino in
                picked_place = random.choice(all_places)

                # 4) update amino location & location Protein attribute
                self.all_coordinates += [picked_place]
                amino.set_location(picked_place)

                self.amino_places["{}".format(picked_place)] = amino
            # TODO
            # when all aminos should have been placed:
            # 1) if doodgelopen/ not all amino's placed, do not save
            # 2) if placed without issue:
            #    2a) check bonds of new Protein vs saved Protein.
            #    2b) save location attribute of most stable Protein

            #  return coordinates of the amino's in the protein

        return self.all_coordinates


    def set_bonds(self, coordinates):
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

                    # # check if other H not in amino's own connections
                    # amino.is_connected(neighbor_amino)

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
        x_list, y_list, scat_hx_list, scat_hy_list, scat_px_list, scat_py_list, scat_cx_list, scat_cy_list = ([] for list in range(8))

        for index, coordinates in enumerate(self.all_coordinates):
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
    all_bonds = protein.set_bonds(all_coordinates)
    stability = protein.set_stability()

    # Visualize the protein
    protein.visualize()
