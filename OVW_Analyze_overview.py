import os

def general_docstring():
    """In this page you can select multiple cyana overview files (e.g. from a batch run) and extract very fast all the target function, RMSD or number of violations.
    """
    # just to a have a general docstring
    pass

def get_tf(read):
    f = open(read, 'r')
    write = os.path.dirname(read) + "/All_TF.txt"
    r = open(write, 'a')
    name = os.path.basename(read)
    for line in f:
        if "Ave" in line:
            if "Average" not in line:
                print(name + line[:18])
                r.write(name + line[:18]+"\n")

def get_rmsd(read):
    f = open(read, 'r')
    write = os.path.dirname(read) + "/All_RMSD.txt"
    r = open(write, 'a')
    name = os.path.basename(read)
    for line in f:
        if "Average backbone" in line:
             print(name + line[:57])
             r.write(name + line[:57]+"\n")

def get_violations(read):
    f = open(read, 'r')
    write = os.path.dirname(read) + "/All_VIOL.txt"
    r = open(write, 'a')
    name = os.path.basename(read)
    counter = 0
    for line in f:
        if "violated" in line and "." in line:
            counter += 1
            if counter == 1:
                print(name + ": ")
                r.write(name + ": ")
            split = line.split()
            for element in split:
                if element.isdigit() == True:
                    r.write(element + " ")
                    print(element + " ")
            if counter == 4:
                r.write("\n")
                print("\n")