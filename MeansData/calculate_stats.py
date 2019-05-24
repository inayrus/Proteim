import sys
import statistics
import pathlib
import csv
import matplotlib.pyplot as plt

def calculate_stats(protein_name):
    """
    Prints the mean and the mode in the terminal.
    Also plots the data distribution in a histogram.
    """
    calculate_mean_mode(protein_name)
    plot_distribution(protein_name)


def calculate_mean_mode(protein_name):
    """
    Function that reads the data gotten from 1000 iterations with the random
    algorithm from a csv and returns the mean and mode.
    """
    data = []

    file = pathlib.Path("MeansData/{}_1000.csv".format(protein_name))

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

    file = pathlib.Path("MeansData/{}_1000.csv".format(protein_name))

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
    calculate_stats(sys.argv[1])
