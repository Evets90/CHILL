import os


def plus_one_iteration(file, value, first, log, overview):
    """This takes a Cyana batch run file (see test files for an example) and assign an incremental value to
    each run, so that every log and overview file will be unique. The user can specify the value of the
    first run and the lines to iterate with (log and overview). If left blank, defaults will be used.
    DEFAULTS:
    -Starting run value: 1
    -First line of a new run: '/home/ubuntu/programs/cyana-3.98.'
    -Log line: 'Zoolander_OVW_1_log.txt'
    -Overview line: 'overview Zoolander_OVW_1.ovw structures=10 range=3-238 pdb'
    WARNING: this function is NOT optimized for the user, modify code directly.
    """
    r = open(file, 'r')
    newname = os.path.splitext(file)[0] + "_iterated.sh"
    w = open(newname, 'w+')
    counter = value-1
    for line in r:
        if first in line:
            counter += 1
        if log in line:
            logmod = "/home/ubuntu/programs/cyana-3.98.11/cyana << EOF > Zoolander_OVW_" + str(counter) + "_log.txt\n"
            w.write(logmod)
        elif overview in line:
            ovwmod = "overview Zoolander_OVW_" + str(counter) + ".ovw structures=10 range=3-238 pdb\n"
            w.write(ovwmod)
        else:
            w.write(line)
    return newname
