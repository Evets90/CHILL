import pandas as pd
import os

def randomization(file, per):
    """This page is to randomly delete a subset of PCS from a file to obtain a radonm subset.
    """
    df = pd.read_csv(file, delimiter='\s+',
                         names=["#Residue_Number", "Residue_Type", "Atom", "PCS", "Error", "Weight", "Sample"])
    df = df.sample(frac=per)
    df.sort_index(inplace=True)
    newname = os.path.splitext(file)[0] + "_randomized.pcs"
    df.to_csv(newname, header=None, index=False, float_format='%.3f', sep='\t')
    #print(df)
    return newname, df