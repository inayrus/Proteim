import sys
from Amino import Amino

class Protein(object):
    """Representation of a protein"""

    def __init__(self, file):
        """initializes a protein"""
        self.stability= 0
        self.amino_acids = self.load_protein("ProteinData/protein_{}.txt".format(file))
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
                # erase the \n
                seq = line.strip()
                for index, letter in enumerate(seq):
                    # turn each letter into an Amino
                    new_amino = Amino(index, letter)

                    if index > 0:
                        prev_amino = amino_acids[index - 1]
                        # add previous amino to connections
                        new_amino.set_connections(prev_amino)
                        # add current amino to the prev amino's connections
                        prev_amino.set_connections(new_amino)
                        print(prev_amino.conn)

                    amino_acids.append(new_amino)
        return amino_acids


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("add one protein to the command line (ex. a1 or c4)")

    Protein(sys.argv[1])
