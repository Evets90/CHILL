import pandas as pd

def general_docstring():
    """This page will allow you to choose a type of violation (Upper, VdW, ACO or PCS) and create automatically a .pml PyMOL macro to color the violating residues on the structure.
    """
    # just to a have a general docstring
    pass

colors = ["aquamarine","black","blue","bluewhite","br0","br1","br2","br3","br4","br5","br6","br7","br8","br9","brightorange","brown","carbon","chartreuse","chocolate","cyan","darksalmon","dash","deepblue","deepolive","deeppurple","deepsalmon","deepteal","density","dirtyviolet","firebrick","forest","gray","green","greencyan","grey","hotpink","hydrogen","lightblue","lightmagenta","lightorange","lightpink","lightteal","lime","limegreen","limon","magenta","marine","nitrogen","olive","orange","oxygen","palecyan","palegreen","paleyellow","pink","purple","purpleblue","raspberry","red","ruby","salmon","sand","skyblue","slate","smudge","splitpea","sulfur","teal","tv_blue","tv_green","tv_orange","tv_red","tv_yellow","violet","violetpurple","warmpink","wheat","white","yellow","yelloworange"]

modes = ['cartoon', 'lines','ribbon', 'sticks', 'spheres']

def get_type(file):
    # Determine violations portion of the file
    r = open(file, 'r')
    start = 0
    end = 0
    counter = 0
    for line in r:
        counter += 1
        if "Restraints violated" in line:
            start = counter
        if "RMSDs for residues" in line:
            end = counter
    # Read Dataframe
    df = pd.read_csv(file, skiprows=start+1, nrows=(end-start)-7, delim_whitespace=True, usecols=[0,1,2,3,4,5,6,7,8,9,10,11], header=None)
    types = []
    for x in df[0].unique():
        types.append(x)
    return types, df

def macro_violations(df, type, mode, color):
    if type=="Upper":
        df = df.drop(df[df[0] != type].index)
        firstuni = df.drop_duplicates(subset=3)
        seconduni = df.drop_duplicates(subset=7)
        firstlist = firstuni[3].to_list()
        secondlist = seconduni[7].to_list()
        print("select Violating, i. ", end="")
        for element in firstlist:
            print(round(element), end="+")
        for element in secondlist[:-1]:
            print(round(element), end="+")
        print(round(secondlist[-1]))
    elif type == "VdW":
        df = df.drop(df[df[0] != type].index)
        df = df.drop_duplicates(subset=3)
        print("select Violating, i. ", end="")
        for element in df[3].tolist()[:-1]:
            print(round(element), end="+")
        print(round(df[3].tolist()[-1]))
    elif type == "Angle":
        df = df.drop(df[df[0] != type].index)
        df = df.drop_duplicates(subset=3)
        print("select Violating, i. ", end="")
        for element in df[3].tolist()[:-1]:
            print(round(element), end="+")
        print(round(df[3].tolist()[-1]))
    elif type == "PCS":
        df = df.drop(df[df[0] != type].index)
        df = df.drop_duplicates(subset=3)
        print("select Violating, i. ", end="")
        for element in df[3].tolist()[:-1]:
            print(round(element), end="+")
        print(round(df[3].tolist()[-1]))
    else:
        print("Type not currently supported.")
    print("hide everything, Violating")
    print("show " + mode + ", Violating")
    print("color " + color + ", Violating")
