import os

def cyana_test(file):
    """This takes a cyana batch run file and automatically creates a .cya macro to test if all the input
    files (aco, upl, ...) are present and if any parameter is rising an error. This can be used to quickly
    check before a large heterogeneous batch run if anything is amiss. If anything is wrong/missing, the
    macro will stop at the error.
    The macro is stored in the working folder under the name 'test.cya'. To activate it, navigate to that
    folder, start cyana and type 'test'.
    """
    # intro
    r = open(file, 'r')
    newfile = os.path.dirname(file) + "/test.cya"
    w = open(newfile, 'w+')
    keywords = ["read seq", 'read aco', 'read lol', 'read upl', 'read pcs', 'read rdc', 'seed', 'nproc', 'weight_', 'info:=']
    counter = 0
    # generate .cya script
    for line in r:
        if "/cyana" in line:
            counter += 1
        elif any(a in line for a in keywords):
            w.write(line)
    return newfile, counter