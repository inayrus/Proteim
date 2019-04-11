import matplotlib.pyplot as plt
import numpy as np


def visualize(all_coordinates):

    # putting the coordinates in an x and an y list
    x_list = []
    y_list = []
    scat_hx_list = []
    scat_hy_list = []
    scat_px_list = []
    scat_py_list = []

    # unpack the values in the dict
    for index in range(len(all_coordinates)):
        amino, coordinates = all_coordinates[index]
        x, y = coordinates
        x_list.append(x)
        y_list.append(y)

        print(amino)
        amino = str(amino)
        if 'P' in amino:
            scat_px_list.append(x)
            scat_py_list.append(y)
            plt.scatter(scat_px_list, scat_py_list, color='red', zorder=2)

        if 'H' in amino:
            scat_hx_list.append(x)
            scat_hy_list.append(y)
            plt.scatter(scat_hx_list, scat_hy_list, color='blue', zorder=2)

        # add a new line when there are two points, then pop one longest in list
        if len(x_list) == 2:
            plt.plot(x_list, y_list, color='black', marker='o', linestyle='solid', zorder=1)
            # print(x_list, y_list)
            x_list.pop(0)
            y_list.pop(0)




    plt.axis([-5, 5, -5, 5])
    plt.show()


    # 1) How to plot stuff and draw a line in it
    # https://stackoverflow.com/questions/16930328/vertical-horizontal-lines-in-matplotlib
    # plt.plot((x1, x2), (y1, y2), 'k-')
    #   --> Could use this to plot every amino and draw a covalent bond between them
    #       BUT: is it possible to plot multiple things over each other?
    #       --> ye: https://stackoverflow.com/questions/21254472/multiple-plot-in-one-figure-in-python
    #               https://stackoverflow.com/questions/22276066/how-to-plot-multiple-functions-on-the-same-figure-in-matplotlib
