import pandas as pd

def check_series(file, column):
    """This checks if a specific column of a file contains a full sequence of numbers.
    It can be used for example to check if a .prot files contains all residues at least once.

    The file has to be in a comma separated format (csv), if needed to prepare the file use the basic function
    "Clean spaces".

    For now it only supports integers.

    It takes the minimum and maximum values in the column, creates a list of integers in that range
    and check if all these integers are present in the original column.
    Individual missing values are listed.

    Parameters:
        -Column: the column containing the series to be checked (index 1, normal).
    """
    dt = pd.read_csv(file, sep=' ', header=None)
    ndt = dt.sort_values(by=column-1)
    tocheck = ndt[column-1]
    inlist = tocheck.tolist()
    min = inlist[0]
    max = inlist[-1]
    outlist = []
    for number in range(min, max+1):
        outlist.append(number)
    missing = 0
    mlist = []
    for element in outlist:
        if element not in inlist:
            mlist.append("Missing: " + str(element) + "\n")
            missing += 1
    return missing, mlist