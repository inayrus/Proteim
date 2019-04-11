from tkinter import *

root = Tk()

# we zouden hier overheen kunnen loopen zodat het het juiste aminozuur is
# https://www.youtube.com/watch?v=-nmzq3xiZ6I
label_1 = Label(root, text= Protein.amino_acids)
label_2 = Label(root, text=Protein.amino_acids)


# dan print hij het hier als het goed is uit. We moeten dan nog bepalen
# hoe dit x_coordinate en y_coordinate echt noemen
entry_1.grid(row = Protein.x_coordinate, column = Protein.y_coordinate)
entry_2.grid(row = Protein.x_coordinate, column = Protein.y_coordinate)
