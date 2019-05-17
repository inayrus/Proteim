import sys
import statistics
import pathlib
import csv
import matplotlib.pyplot as plt

def calculate_mean(protein_name):
    """Function that takes data from a csv and returns the mean."""
    data = []

    file = pathlib.Path("{}_1000.csv".format(protein_name))

    # read the csvfile
    with file.open('r') as csv_file:
        csv_reader = csv.reader(csv_file)

        # append the stabilities to a list
        for row in csv_reader:
            if row != []:
                for elem in row:
                    data.append(int(elem))

    # calculate mean
    average = statistics.mean(data)
    mode = statistics.mode(data)
    print("average: {}".format(average))
    print("mode: {}".format(mode))


def plot_distribution(protein_name):
    data = []

    file = pathlib.Path("{}_1000.csv".format(protein_name))

    # read the csvfile
    with file.open('r') as csv_file:
        csv_reader = csv.reader(csv_file)

        # append the stabilities to a list
        for row in csv_reader:
            if row != []:
                for elem in row:
                    data.append(int(elem))

    plt.hist(data, density=1, bins=20)
    plt.show()


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("type the protein you want the mean of in the command line")
    calculate_mean(sys.argv[1])
    plot_distribution(sys.argv[1])
