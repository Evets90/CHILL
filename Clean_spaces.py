import re
import os

def clean_spaces(file):
    """This takes any file and for each line replaces multiple white spaces or other special
    character (tabs and so on) with a single with space.
    It is intended to be a pre-step for loading into Pandas dataframes.
    The output is "filename_clean.txt"
    """
    newfile = os.path.splitext(file)[0] + "_clean.txt"
    f2 = open(newfile, 'w+')
    res = []
    with open(file, 'r') as f:
        for line in f:
            goodline = re.sub(r'\s+', ' ', line).strip()
            f2.write(goodline + '\n')
            res.append(goodline+"\n")
    return res
