import pandas as pd
import os

def pcs_subset(file, subset, mode, seed=None):
    """
    This takes a .pcs file and retains a certain subset of those pcs. The subset value can be
    based on a percentage or a integer number depending on the mode. The seed can be specified for
    reproducibility, if left empty the seed is randomized.
       """
    # read dataframes
    with open(file) as f:
        if f.readline().strip()[:8] == "#Sample " or f.readline().strip()[:8] == "# Sample":
            header = 1
    if header == 1:
        f_read = pd.read_csv(file, sep="\s+", header=2, names=["Residue Number", "Rest", "Atom", "PCS", "Error", "Weight", "Sample"])
    else:
        f_read= pd.read_csv(file, sep="\s+", names=["Residue Number", "Rest", "Atom", "PCS", "Error", "Weight", "Sample"])
        # deletion of the selected percentage
    if mode == "Percentage":
        fraction = subset/100
        if seed:
            sub = f_read.sample(frac=fraction, random_state=seed)
        else:
            sub = f_read.sample(frac=fraction)
    elif mode == "Integer":
        if seed:
            sub = f_read.sample(n=subset, random_state=seed)
        else:
            sub = f_read.sample(n=subset)
    else:
        print("Error, no correct mode selected")
        exit(1)
    # polish
    sub.sort_values(["Sample", "Residue Number"], ascending=True, inplace=True)
    sub = sub.round(3)
    def test(result):
        if mode == "Percentage":
            removed = len(f_read) * (1 - fraction)
            left = round(len(f_read) - removed)
        elif mode == "Integer":
            removed = round(len(f_read) - subset)
            left = len(f_read) - removed
        else:
            print("Error, no correct mode selected")
            exit(1)
        if left == len(result):
            pass
            #print("Internal Test SUCESSFUL.")
        else:
            print(f"Internal test Failed: expected {left} elements and found {len(result)}")
    test(sub)
    newname = os.path.splitext(file)[0] + "_" + str(subset) + "_subset.pcs"
    sub.to_csv(newname, sep="\t", index=False, float_format='%.3f', header=None)
    return newname, sub