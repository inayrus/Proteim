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
        self.coordinates = []

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
                self.coordinates += [[amino, [0, 0]]]
                amino.set_location([0, 0])

            # for the other aminos:
            # 1) loop through the spaces around amino
            else:
                prev_amino, coordinates = self.coordinates[index - 1]
                all_places = self.get_neightbors(coordinates)

                # 2) check the Protein attribute what places are empty
                for prev_aminos, xy in self.coordinates:
                    if xy in all_places:
                        all_places.remove(xy)

                # 3) pick one location to place the amino in
                picked_place = random.choice(all_places)

                # when no places around last amino available, break
                if all_places == []:
                    return []

                # 4) update amino location & location Protein attribute
                self.coordinates += [[amino, picked_place]]
                amino.set_location(picked_place)

            # when all aminos should have been placed:
            # 1) if doodgelopen/ not all amino's placed, do not save
            # 2) if placed without issue:
            #    2a) check bonds of new Protein vs saved Protein.
            #    2b) save location attribute of most stable Protein

            #  return coordinates of the amino's in the protein

        return self.coordinates


    def set_bonds(self, coordinates):
        """function to store the bonds H's or C's made in the protein"""

        # loop through the aminos in the protein
        for amino in self.amino_acids:
            amino_kind = amino.get_kind()
            # print(amino_kind)

            # for H's and C's, get neighboring locations
            if amino_kind != 'P':
                amino_location = amino.get_location()
                neightboring_locations = self.get_neightbors(amino_location)

                # remove location if neighboring amino is in amino's own connections
                connected_aminos = amino.get_conn()
                for conn_amino in connected_aminos:
                    conn_amino_location = conn_amino.get_location()
                    if conn_amino_location in neightboring_locations:
                        neightboring_locations.remove(conn_amino_location)

                # check if amino is neighboring a non-covalent H or C
                for another_amino, coordinates in self.coordinates:
                    if coordinates in neightboring_locations and another_amino.get_kind() != 'P':
                        bonded_amino = another_amino

                        # check if current bond is already stored
                        if self.bonds == []:
                            self.bonds += [[amino, bonded_amino]]

                        # for bond in self.bonds:
                        if [amino, bonded_amino] not in self.bonds and [bonded_amino, amino] not in self.bonds:
                            # if not, add bond to attribute
                            self.bonds += [[amino, bonded_amino]]


        print("bonds: {}".format(self.bonds))
        return self.bonds

                    # # check if other H not in amino's own connections
                    # amino.is_connected(neighbor_amino)


    def get_neightbors(self, coordinates):
        """
        a function that returns a list of all coordinates around a certain
        grid point
        """
        x, y = coordinates
        return [[x, y + 1], [x, y - 1], [x + 1, y], [x - 1, y]]


    def visualize(all_coordinates, bonds):
        # putting the coordinates in an x and an y list
        x_list = []
        y_list = []
        scat_hx_list = []
        scat_hy_list = []
        scat_px_list = []
        scat_py_list = []

        for index in range(len(all_coordinates)):
            # unpack the coordinate values
            amino, coordinates = all_coordinates[index]
            x, y = coordinates
            x_list.append(x)
            y_list.append(y)

            # group the coordinates of the same amino kinds
            amino_kind = amino.get_kind()
            if amino_kind == 'P':
                scat_px_list.append(x)
                scat_py_list.append(y)
            elif amino_kind == 'H':
                scat_hx_list.append(x)
                scat_hy_list.append(y)

        # Plot cavalent line
        plt.plot(x_list, y_list, color='black', linestyle='solid', zorder=1)

        # use different colours to visualize the amino kind groups
        plt.scatter(scat_px_list, scat_py_list, color='red', zorder=2)
        plt.scatter(scat_hx_list, scat_hy_list, color='blue', zorder=2)

        # unpack the bonds neightboring_locations
        for bond in bonds:
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
    visualize(all_coordinates, all_bonds)
