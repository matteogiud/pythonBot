def parse_list(filename, delimiter=';', no_first=0) -> list:
    import csv

    data = []
    with open(filename, mode='r', encoding="utf8") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=delimiter)

        for riga in csv_reader:
            if no_first > 0:
                no_first -= 1
                continue
            data.append(riga)

        return data


def parse_dict(filename, delimiter=';', no_first=0) -> list:
    import csv

    data = []
    with open(filename, mode='r', encoding="utf8") as csv_file:
        while (no_first > 0):
            next(csv_file)
            no_first -= 1
            # se devo skippare la prima riga

        csv_reader = csv.DictReader(csv_file, delimiter=delimiter)

        for riga in csv_reader:
            data.append(riga)

        return data


open("pippo.txt", mode="w").write(
    str(parse_dict("py\\anagrafica_impianti_attivi.csv", no_first=1)))
