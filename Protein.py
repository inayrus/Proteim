import sys
import pathlib
from Amino import Amino

class Protein(object):
    """Representation of a protein"""

    def __init__(self, file):
        """initializes a protein"""
        self.stability= 0
        self.amino_acids = self.load_protein("ProteinData/{}.txt".format(file))
        self.bonds = []

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
    Protein(sys.argv[1])
