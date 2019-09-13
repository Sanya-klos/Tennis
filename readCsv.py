import csv


def start(name):
    # better if use pandas :)
    r = 0  # from which row begin reading
    data = []
    with open(name, 'r') as csvFile:
        reader = csv.reader(csvFile)
        i = 0
        for row in reader:
            if i < r:
                i += 1
                continue
            data.append(row)

    csvFile.close()
    return data
