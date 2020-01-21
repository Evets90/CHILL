import pandas as pd
import os

def pcs_subset(file, subset, mode="per", iter="off", info="off", seed=None):
    """
    This takes a .pcs file and retains a certain subset of those pcs. The subset can be based on
    a percentage or a integer number.
       """
    # fail early
    if mode == "per" and not 0 < subset <= 1:
        print("Not a valid subset number. Please enter a float number between 0 and 1.")
        exit(1)
    elif mode == "int":
        if float(subset).is_integer() == False or subset < 1:
            print("Not a valid subset number. Please enter an integer (min 1).")
            exit(1)
    # read dataframes
    if iter == "on":
        f_read = pd.DataFrame(file)
    else:
        f_read = pd.read_csv(file, sep=' ',
                             names=["Residue_Number", "Residue_Type", "Atom", "PCS", "Error", "Weight", "Sample"],
                             skiprows=1)
    # deletion of the selected percentage
    if mode == "per":
        if seed:
            sub = f_read.sample(frac=subset, random_state=seed)
        else:
            sub = f_read.sample(frac=subset)
    elif mode == "int":
        if seed:
            sub = f_read.sample(n=subset, random_state=seed)
        else:
            sub = f_read.sample(n=subset)
    else:
        print("Error, no correct mode selected")
        exit(1)
    # polish
    sub.sort_values(["Sample", "Residue_Number"], ascending=True, inplace=True)
    sub = sub.round(3)

    def test(result):
        if mode == "per":
            removed = len(f_read) * (1 - subset)
            left = round(len(f_read) - removed)
        elif mode == "int":
            removed = round(len(f_read) - subset)
            left = len(f_read) - removed
        else:
            print("Error, no correct mode selected")
            exit(1)
        if left == len(result):
            print("Internal Test SUCESSFUL.")
        else:
            print(f"Internal test Failed: expected {left} elements and found {len(result)}")

    test(sub)
    if info == "on":
        if mode == "per":
            print(f"Initial number of pcs: {len(f_read)}.")
            print(f"Deleting {100 - (subset * 100)}% with seed {seed}.")
            print(f"Remaining number of pcs: {len(sub)}\n")
        elif mode == "int":
            print(f"Initial number of pcs: {len(f_read)}.")
            print(f"Deleting {len(f_read) - subset} pcs with seed {seed}.")
            print(f"Remaining number of pcs: {len(sub)}\n")
    return sub