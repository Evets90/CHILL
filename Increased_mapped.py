import pandas as pd
import os

def increase_mapped(map, mapped, per, mode="per", info="off", seed=None):
    """
    This takes two .pcs files, one being the 'map' and the other being the 'mapped' as per the
    mapping function, checks residue number-atom pairs in the map that are not present in the mapped
    and add a specified amount of them to the original mapped. The amount can be based on a
    percentage or an integer value.
    This function is used to maintain the original "mapping" procedure but increase it by a certain
    amount.
    The seed can be specified for reproducibility, if left empty the seed is randomized.
           """
    # read map
    with open(map) as f:
        if f.readline().strip()[:8] == "#Sample " or f.readline().strip()[:8] == "# Sample":
            kheader = 1
    if kheader == 1:
        mydfmap = pd.read_csv(map, sep="\s+", header=2,
                              names=["Residue_Number", "Rest", "Atom", "PCS", "Error", "Weight", "Sample"])
    else:
        mydfmap = pd.read_csv(map, sep="\s+",
                              names=["Residue_Number", "Rest", "Atom", "PCS", "Error", "Weight", "Sample"])
    # read mapped
    with open(mapped) as f:
        if f.readline().strip()[:8] == "#Sample " or f.readline().strip()[:8] == "# Sample":
            mheader = 1
    if mheader == 1:
        mydfmapped = pd.read_csv(mapped, sep="\s+", header=2,
                              names=["Residue_Number", "Rest", "Atom", "PCS", "Error", "Weight", "Sample"])
    else:
        mydfmapped = pd.read_csv(mapped, sep="\s+",
                              names=["Residue_Number", "Rest", "Atom", "PCS", "Error", "Weight", "Sample"])
    # concatenate and drop all duplicates to find missing in mapped
    global fraction
    merged = pd.concat([mydfmap, mydfmapped])
    merged.drop_duplicates(inplace=True, keep=False)
    merged = merged.round(3)
    # deletion of the selected percentage/number
    if mode == "Percentage":
        if seed:
            fraction = merged.sample(frac=per/100, random_state=seed)
        else:
            fraction = merged.sample(frac=per/100)
    elif mode == "Integer":
        if seed:
            fraction = merged.sample(n=per, random_state=seed)
        else:
            fraction = merged.sample(n=per)
    # concatenate and polish
    frames = [mydfmapped, fraction]
    conc = pd.concat(frames)
    conc.sort_values(["Sample", "Residue_Number"], ascending=True, inplace=True)
    conc = conc.round(3)
    # internal tests
    def test1(initial, result):
        """Simple function to check if the deletion in the first step worked fine"""
        initial_dictionary = {}
        result_dictionary = {}
        counter = 0
        for index1, row1 in initial.iterrows():
            initial_dictionary[row1['Residue_Number']] = (row1['Atom'], row1['Sample'])
        for index2, row2 in result.iterrows():
            result_dictionary[row2['Residue_Number']] = (row2['Atom'], row2['Sample'])
        for x in initial_dictionary:
            for y in result_dictionary:
                if x == y:
                    if initial_dictionary[x] == result_dictionary[y]:
                        counter += 1
                        if counter == 1:
                            print("WARNING! Internal Test Faied.")
                        print(f"Residue number {x} in mapped file with atom and sample {initial_dictionary[x]} is still found in the resulting DataFrame with residue number {y} and atom/sample {result_dictionary[y]}")
        if counter == 0:
            pass
            #print("Internal test was SUCCESSFUL.")
    test1(mydfmapped, merged)
    # more info
    #if info == "on":
    #    print(f"Mapped file {mapped} was increased with the following pcs:")
    #    print("Residue Number | Residue Type | Atom | PCS | Sample")
    #    for index, row in fraction.iterrows():
    #        print(row['Residue_Number'], row['Residue_Type'], row['Atom'], row['PCS'], row['Sample'])
    #    print(f"Total elements added: {len(fraction)}")
    newname = os.path.splitext(map)[0] + "_increased" + str(per) + ".pcs"
    conc.to_csv(newname, sep="\t", index=False, float_format='%.3f', header=None)
    return newname, conc