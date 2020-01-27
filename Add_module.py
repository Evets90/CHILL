import pandas as pd
import os

def add_module(key, map, module, Test1=0):
    """
        Follow-up of the "Mapping" function.
        This takes two .pcs files, one a being the 'map' and the other the 'key' (as per the
        mapping function), and add all the missing pcs from the map in a specific module/cap
        to the 'key'.
        If the option 'Check sequence integrity' is ticked, the system will check if any residue is
        missing in the assignment of the selected module in the 'map' file.
           """
    global deleted
    # read key
    with open(key) as f:
        if f.readline().strip()[:8] == "#Sample " or f.readline().strip()[:8] == "# Sample":
            kheader = 1
    if kheader == 1:
        mydfkey = pd.read_csv(key, sep="\s+", header=2,
                              names=["Residue_Number", "Rest", "Atom", "PCS", "Error", "Weight", "Sample"])
    else:
        mydfkey = pd.read_csv(key, sep="\s+",
                              names=["Residue_Number", "Rest", "Atom", "PCS", "Error", "Weight", "Sample"])
    # read map
    with open(map) as f:
        if f.readline().strip()[:8] == "#Sample " or f.readline().strip()[:8] == "# Sample":
            mheader = 1
    if mheader == 1:
        mydfmap = pd.read_csv(map, sep="\s+", header=2,
                              names=["Residue_Number", "Rest", "Atom", "PCS", "Error", "Weight", "Sample"])
    else:
        mydfmap = pd.read_csv(map, sep="\s+",
                              names=["Residue_Number", "Rest", "Atom", "PCS", "Error", "Weight", "Sample"])
    # look in the map for the selected modules
    if module == "Y":
        deleted = mydfmap.drop(mydfmap[mydfmap['Residue_Number'] > 32].index)
    elif module == "M1":
        deleted = mydfmap.drop(mydfmap[(mydfmap['Residue_Number'] < 33) | (mydfmap['Residue_Number'] > 74)].index)
    elif module == "M2":
        deleted = mydfmap.drop(mydfmap[(mydfmap['Residue_Number'] < 75) | (mydfmap['Residue_Number'] > 116)].index)
    elif module == "M3":
        deleted = mydfmap.drop(mydfmap[(mydfmap['Residue_Number'] < 117) | (mydfmap['Residue_Number'] > 158)].index)
    elif module == "M4":
        deleted = mydfmap.drop(mydfmap[(mydfmap['Residue_Number'] < 159) | (mydfmap['Residue_Number'] > 200)].index)
    elif module == "A":
        deleted = mydfmap.drop(mydfmap[mydfmap['Residue_Number'] < 201].index)
    else:
        print("Error selecting the module.")
    # concatenate, delete duplicates and polish
    frames = [mydfkey, deleted]
    conc = pd.concat(frames)
    dupp = conc.duplicated(keep='first')
    conc.drop_duplicates(inplace=True)
    conc.sort_values(["Sample", "Residue_Number"], ascending=True, inplace=True)
    conc = conc.round(3)
    # internal tests
    def test1(result, module):
        """Quick test to check if the final DataFrame contains entirely the residue number range for the selected module"""
        select = result['Residue_Number']
        select = select.sort_values()
        select.drop_duplicates(inplace=True)
        inlist = select.tolist()
        outlist = []
        if module == "Y":
            mymin = 1
            mymax = 32
        elif module == "M1":
            mymin = 33
            mymax = 74
        elif module == "M2":
            mymin = 75
            mymax = 116
        elif module == "M3":
            mymin = 117
            mymax = 158
        elif module == "M4":
            mymin = 159
            mymax = 200
        elif module == "A":
            mymin = 201
            mymax = 239
        else:
            print("Incorrect module selected.")
            exit(1)
        for x in range(mymin, mymax+1):
            outlist.append(x)
        missing = 0
        for element in outlist:
            if element not in inlist:
                print(f"{element} is missing.")
                missing += 1
        if missing == 0:
            pass
            #print("Internal test 1 SUCCESSFUL")
        else:
            print(f"Internal test 1 FAILED. Total missing elements in the sequence: {missing}")
    def test2(result, initial):
        """Small test to check if putting together the result and the intial and removing the non-duplicates returns the initial"""
        pull = pd.concat([initial, result])
        dup = pull.duplicated(subset=["Residue_Number","Atom","Sample"], keep='first')
        dup = dup[dup == True].index
        if len(initial) == len(dup):
            pass
            #print("Internal test 2 SUCESSFUL")
        else:
            print("Internal test 2 FAILED")
    if Test1==1:
        test1(conc, module)
    test2(conc, mydfkey)
    newname = os.path.splitext(key)[0] + "_PlusModule" + str(module) + ".pcs"
    conc.to_csv(newname, sep="\t", index=False, float_format='%.3f', header=None)
    return newname, conc
