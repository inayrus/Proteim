
import sys
from Amino import Amino

class Protein(object):
    """Representation of a protein"""

    def __init__(self, file):
        """initializes a protein"""
        self.stability= 0
        self.amino_acids = self.load_protein(f"ProteinData/protein_{file}.txt")
        self.bonds = []

    def load_protein(self, file):
        """
        Reads the protein in from a text file.
        Returns a list of Amino instances
        """
        with open(file, "r") as f:
            amino_acids = []
            for letter in f:
                amino = Amino(letter)
                amino_acids.append(amino)
        print(amino_acids)
        return amino_acids

if __name__ == "__main__":
    if len(sys.argv) != 2
        print("add one protein to the command line (ex. a1 or c4)")

    file = sys.argv[1]
