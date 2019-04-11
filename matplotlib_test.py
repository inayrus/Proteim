# from Protein import Protein
import matplotlib.pyplot as plt
import numpy as np

x1 = 0
y1 = 0
x2 = 0
y2 = 1

# a dictionalry with the coordinates
test_dict = {'0': ["amino_1", [x1, y1]]}
test_dict['1'] = ["amino_2", [x2, y2]]
test_dict['2'] = ["amino_3", [0, 2]]
test_dict['3'] = ["amino_4", [0, 3]]
test_dict['4'] = ["amino_5", [1, 3]]

# putting the coordinates in an x and an y list
x_list = []
y_list = []

# unpack the values in the dict
for index in range(len(test_dict)):
# for element in test_dict.values():
    amino, coordinates = test_dict[str(index)]
    print(coordinates)
    # amino, coordinates = element
    x, y = coordinates
    x_list.append(x)
    y_list.append(y)
    # add a new line when there are two points, then pop the first one
    if len(x_list) == 2:
        plt.plot(x_list, y_list, color='green', marker='o', linestyle='solid')
        print(x_list, y_list)
        x_list.pop(0)
        y_list.pop(0)


#  make a plot with the coordinates
# plt.plot(x_list, y_list, color='green', marker='o')
plt.show()


# 1) How to plot stuff and draw a line in it
# https://stackoverflow.com/questions/16930328/vertical-horizontal-lines-in-matplotlib
# plt.plot((x1, x2), (y1, y2), 'k-')
#   --> Could use this to plot every amino and draw a covalent bond between them
#       BUT: is it possible to plot multiple things over each other?
#       --> ye: https://stackoverflow.com/questions/21254472/multiple-plot-in-one-figure-in-python
#               https://stackoverflow.com/questions/22276066/how-to-plot-multiple-functions-on-the-same-figure-in-matplotlib

# 2) Possible to give a dict with the coordinates {'id': [x, y]},
#    and unpack the coordinates and put them in two lists: X and Y.
