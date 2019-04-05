class Amino(object):
    """ representation of an amino acid """

    def __init__(self, id, kind):
        """ initializes an amino acid """
        self.id = id
        self.kind = kind
        self.conn = []
        self.location = []
        self.bond_strength = self.set_bond_strength(kind)

    def get_conn(self):
        """ returns the amino's connections (a list) """
        return self.conn

    def get_location(self):
        """ return the amino's location (a list of x and y)"""
        return self.location

    def get_bond_strength(self):
        """ The added stability if this animo would bond with its own kind.
        Returns an int"""
        return self.bond_strength

    def set_location(self, location):
        """ sets the location of the amino: [x, y]"""
        self.location = location

    def set_bond_strength(self, kind):
        """ if kind is H or C, set bond_strength"""
        if self.kind == 'H':
            self.bond_strength = -1
        elif self.kind == 'C':
            self.bond_strength = -5
        else:
            self.bond_strength = 0

    def set_connections(self, connected_amino):
        """ a function to add a connected amino to self.conn"""
        self.conn += [connected_amino]

    def __repr__(self):
        return "{}: {}".format(self.id, self.kind)
