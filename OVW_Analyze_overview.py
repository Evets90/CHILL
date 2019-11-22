import os

def general_docstring():
    """In this page you can select multiple cyana overview files (e.g. from a batch run) and extract very fast all the target function, RMSD or number of violations.
    """
    # just to a have a general docstring
    pass

def get_tf(read):
    f = open(read, 'r')
    name = os.path.basename(read)
    for line in f:
        if "Ave " in line.strip()[:4]:
            print(name + ": " + line.strip()[5:12] + " " + u"\u00B1", end="")
        if "+/-" in line.strip()[:3]:
            print(line.strip()[3:12])

def get_rmsd(read):
    f = open(read, 'r')
    name = os.path.basename(read)
    for line in f:
        if "Average backbone" in line:
            print(name + ": " + line.strip()[:52])

def get_violations(read):
    f = open(read, 'r')
    name = os.path.basename(read)
    counter = 0
    for line in f:
        if "violated" in line and "." in line:
            counter += 1
            if counter == 1:
                print(name + ":", end=" ")
            split = line.split()
            for element in split:
                if element.isdigit() == True:
                    print(element, end=" ")
            if counter == 4:
                print("\n", end="")
