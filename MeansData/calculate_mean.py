import sys
import statistics
import pathlib
import csv

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
        print(average)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("type the protein you want the mean of in the command line")
    calculate_mean(sys.argv[1])
