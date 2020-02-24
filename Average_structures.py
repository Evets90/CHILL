from biopandas.pdb import PandasPdb
import pandas as pd
import os

def general_docstring():
    """Here you can load a list of .pdb files and generate an average structure. The average structure
    will have average x, y and z coordinates for each atom. If the option "Only CA" is selected, only CA
    atoms are maintaned in the process. It is recomended to align the structures in PyMOL first to obtain
    an optimal result. More info here: https://pymolwiki.org/index.php/Align
    WARNING: this works only with pdb files that have exactly the same atoms and order of atoms (i.e. a
    bundle of structures from cyana). Anything with different atoms and/or different order will raise an
    error.
    """
    # Just to have a general docstring
    pass


def atom_number_test(list):
    """Test to check if the pdb files contain exactly the same atom numbering"""
    ppdb = PandasPdb()
    df = pd.DataFrame()
    counter = 0
    # Loop for extracting atom numbers
    for file in list:
        counter += 1
        ppdb.read_pdb(file)
        r = ppdb.df['ATOM']
        df[counter] = r['atom_number']
    # Remove rows with non identical values for each column
    dfx = df[df.apply(pd.Series.nunique, axis=1) == 1]
    if len(df) == len(dfx):
        return True
    else:
        return False


def set_key(dictionary, key, value):
    """Correctly genereate a dictionary with one key and multiple values."""
    if key not in dictionary:
        dictionary[key] = value
    elif type(dictionary[key]) == list:
        dictionary[key].append(value)
    else:
        dictionary[key] = [dictionary[key], value]


def get_dictionaries(list):
    """For each file in the list, generate three dictionaries linking atom number to x, y and z coordinates"""
    ppdb = PandasPdb()
    dictio_x = {}
    dictio_y = {}
    dictio_z = {}
    for file in list:
        ppdb.read_pdb(file)
        r = ppdb.df['ATOM']
        for index, row in r.iterrows():
            set_key(dictio_x, row['atom_number'], row['x_coord'])
            set_key(dictio_y, row['atom_number'], row['y_coord'])
            set_key(dictio_z, row['atom_number'], row['z_coord'])
    return dictio_x, dictio_y, dictio_z


def average_dict_values(dictionary):
    """Averages the values of each key in a dictionary"""
    ave = {}
    for key in dictionary:
        average = sum(dictionary[key]) / len(dictionary[key])
        ave[key] = round(average, 3)
    return ave


def map_dataframe(file, dx, dy, dz, remove_non_ca=0):
    """Construct the new pdb mapping x, y and z averaged coordinates"""
    ppdb = PandasPdb()
    ppdb.read_pdb(file)
    r = ppdb.df['ATOM']
    r.x_coord = r.atom_number.map(dx)
    r.y_coord = r.atom_number.map(dy)
    r.z_coord = r.atom_number.map(dz)
    if remove_non_ca == 0:
        newname = os.path.splitext(file)[0] + "_averaged.pdb"
        ppdb.to_pdb(newname)
        return newname, ppdb
    elif remove_non_ca == 1:
        r.drop(r[r['atom_name'] != "CA"].index, inplace=True)
        newname = os.path.splitext(file)[0] + "_averaged_CA.pdb"
        ppdb.to_pdb(newname)
        return newname, ppdb
    else:
        exit(1)


#f1 = "/Users/stefanocucuzza/Desktop/Stefano/CHILL/Test_files/Test_average_structures/File1.pdb"
#f1w = "/Users/stefanocucuzza/Desktop/Stefano/CHILL/Test_files/Test_average_structures/File1_wrong.pdb"
#f2 = "/Users/stefanocucuzza/Desktop/Stefano/CHILL/Test_files/Test_average_structures/File2.pdb"
#f3 = "/Users/stefanocucuzza/Desktop/Stefano/CHILL/Test_files/Test_average_structures/File3.pdb"
#
#dx, dy, dz = get_dictionaries([f1, f2])
#ax = average_dict_values(dx)
#ay = average_dict_values(dy)
#az = average_dict_values(dz)
#map_dataframe(f1, ax, ay, az, remove_non_ca=1)