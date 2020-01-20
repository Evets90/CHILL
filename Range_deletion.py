import pandas as pd
import os


def pcs_range_deletion(file, min, max, column, inverse="off", header=0):
    """
    DESCRIPTION
    This takes a .pcs file and deletes all the values in a specified numeric column (residue number, PCS or
    sample) in a specified range. Indicated boundaries are included in the deletion. If the inverse mode is selected,
    the range is maintained and everything else is removed.
        """
    # read dataframes
    if header == 1:
        df = pd.read_csv(file, sep="\s+", header=2,names=["Residue Number", "Rest", "Atom", "PCS", "Error", "Weight", "Sample"])
    else:
        df = pd.read_csv(file, sep="\s+",names=["Residue Number", "Rest", "Atom", "PCS", "Error", "Weight", "Sample"])
    # deleting
    if inverse == "on":
        deleted = df.drop(df[(df[column] < min) | (df[column] > max)].index)
    else:
        deleted = df.drop(df[(df[column] >= min) & (df[column] <= max)].index)
    deleted = deleted.round(3)
    # internal test
    def test(initialdf, finaldf):
        if inverse == "on":
            toremove = initialdf[(initialdf[column] < min) | (initialdf[column] > max)].index
        else:
            toremove = initialdf[(initialdf[column] >= min) & (initialdf[column] <= max)].index
        if len(initialdf)-len(toremove) == len(finaldf):
            #print("Internal test SUCCESFUL.")
            pass
        else:
            print(f"Internal test FAILED for file {file}")
            exit(1)
    test(df, deleted)
    # finalizing
    newname = os.path.splitext(file)[0] + "_" + str(min) + "-" + str(max) + ".pcs"
    deleted.to_csv(newname, sep="\t", index=False, float_format='%.3f', header=None)
    return newname, deleted
