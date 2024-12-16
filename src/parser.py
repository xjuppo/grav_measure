import csv

def read_from_file(path: str, delimiter=";") -> dict:
    '''
        Reads values from a csv file and tries to parse them
        to float values

        Args:
            path (str): path of the csv file

        Optional Args:
            delimiter: csv delimiter, default: ";"

        Returns:
         dict(str, list(float)) where:
            - key is the header contained in the csv file
            - value is the values under that header
    '''
    file = open(path, "r", newline="")
    reader = csv.reader(file, delimiter=";")
    header: list = next(reader)
    
    values_to_parse = [line for line in reader]
    parsed_values = []
    for to_parse in values_to_parse:
        parsed = [float(e.replace(",", ".")) for e in to_parse]
        parsed_values.append(parsed)
    
    res: dict = {}

    for i in range(len(header)):
        res[header[i]] = []
    
    for parsed in parsed_values:
        for i in range(len(parsed)):
            res[header[i]].append(parsed[i])

    return res