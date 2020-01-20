import pandas as pd
import os

def mapping(key, map):
    """
    This takes two .pcs files, a "map" and a "key", and checks for every residue_number-atom
    combination in the map and maintains the same in the key. It is used to maintain the same
    assignments that you have in the "map" file while using the pcs, tolerance, weight and sample
    of the "key" file.
    NOTE: if the 'map' is not a perfect subset of 'key', the function will fail and raise an
    error. I might implement a solution in the future if required.
        """
    # read key
    with open(key) as f:
        if f.readline().strip()[:8] == "#Sample " or f.readline().strip()[:8] == "# Sample":
            kheader = 1
    if kheader == 1:
        mydfkey = pd.read_csv(key, sep="\s+", header=2,
                           names=["Residue Number", "Rest", "Atom", "PCS", "Error", "Weight", "Sample"])
    else:
        mydfkey = pd.read_csv(key, sep="\s+",
                           names=["Residue Number", "Rest", "Atom", "PCS", "Error", "Weight", "Sample"])
    # read map
    with open(map) as f:
        if f.readline().strip()[:8] == "#Sample " or f.readline().strip()[:8] == "# Sample":
            mheader = 1
    if mheader == 1:
        mydfmap = pd.read_csv(map, sep="\s+", header=2,
                           names=["Residue Number", "Rest", "Atom", "PCS", "Error", "Weight", "Sample"])
    else:
        mydfmap = pd.read_csv(map, sep="\s+",
                           names=["Residue Number", "Rest", "Atom", "PCS", "Error", "Weight", "Sample"])
    # merge on residue number
    merged = pd.merge(mydfkey, mydfmap, on='Residue Number', how='outer')
    merged = pd.DataFrame.dropna(merged)
    # keep only same atoms in the two dataframes
    merged = merged.drop(merged[merged['Atom_x']!=merged['Atom_y']].index)
    # drop unwanted columns, rename them and round up to three decimals
    merged = merged.drop(['Rest_y', 'Atom_y', 'PCS_y', 'Error_y', "Weight_y", 'Sample_y'], axis=1)
    merged.columns = ['Residue Number','Residue Type', 'Atom', 'PCS', 'Error', 'Weight', 'Sample']
    merged = merged.round(3)
    def test(result, map1):
        """Simple function to check if something went wrong in the processing by comparing the number of rows in the
        resulting file and in the map file. They should be the same, granted that the map is a subset on the key file.
        Always true in my particular case but not in all cases so potential errors are just stated and not stopped."""
        if len(result.index) == len(map1.index):
            #print(f"Internal test SUCCESSFUL, {map} mapped on {key}")
            pass
        else:
            print(f"Internal test FAILED. Attention! Total rows of the result does not match total rows of the map {map}. Check if {map} is a perfect subset of {key}.")
    test(merged, mydfmap)
    newname = os.path.splitext(key)[0] + "_mapped.pcs"
    merged.to_csv(newname, sep="\t", index=False, float_format='%.3f', header=None)
    return newname, merged