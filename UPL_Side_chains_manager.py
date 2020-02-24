import pandas as pd
import os

def general_docstring():
    """In this page you can load a .upl upper limit restrains cyana file and manage the distances related
    to sidechains using one of three different functions.
    -Remove side chains: retains only distances between two backbone atoms.
    -Remove inter side chains: retains only distances between a side chain atom and another atom in the
    same residue (either backbone or side chain).
    -Remove inter side chains (backbone): retains distances between a side chain atom and another atom in
    the same residue (either backbone or side chain) AND distances between two backbone atoms.
    """
    pass
    # Just to have a general docstring

def remove_sidechains(file):
    """Take a .upl file and returns a Pandas Dataframe in which every distance which is not between two
    backbone atoms (C, CA, N, H and O) is deleted.
    """
    # read Dataframe
    dt = pd.read_csv(file, sep='\s+', header=None,
                     names=['1_resn', '1_rest', '1_atom', '2_resn', '2_rest', '2_atom', 'upl'])
    bckbone = ["C", "CA", "N", "H", "O"]
    res = dt.loc[dt['1_atom'].isin(bckbone) & dt['2_atom'].isin(bckbone)]
    newname = os.path.splitext(file)[0] + "_removed_side_chains.upl"
    res.to_csv(newname, sep="\t", index=False, float_format='%.3f', header=None)
    return newname, res

def remove_inter_sidechains(file):
    """Take a .upl file and returns a Pandas Dataframe in which only distances between a side chain
    and something else in the same residue are maintained.
    """
    # read DataFrame
    dt = pd.read_csv(file, sep='\s+', header=None, names=['1_resn', '1_rest', '1_atom', '2_resn', '2_rest', '2_atom', 'upl'])
    sideatoms = ['CB','HB','HA','HB1','HB2','HB3','CG','HG2','HG3','HE21','HE22','HD1','HD2','CD1','CD2','HD3','HE2','HE3','HG','HD','HE','NE2','ND2','NE1','QB','QG','OE1','OE2','QD1','QD2','QQD','QD','QE2','SD','QE','OD1','OG','OD2','NE','NH1','1HH1','2HH2','QH2','NZ','1HZ','2HZ','QZ','QA','3HZ','HH','QH1','NH2','ND1','CD','CE','CZ','HZ']
    # Check for at least one side chain atom
    sdc = dt[['1_atom', '2_atom']].isin(sideatoms).any(axis=1)
    # Check for same residue
    res = dt.where(dt[sdc]['1_resn']==dt[sdc]['2_resn'])
    res.dropna(inplace=True)
    res['1_resn'] = res['1_resn'].astype(int)
    res['2_resn'] = res['2_resn'].astype(int)
    newname = os.path.splitext(file)[0] + "_removed_inter_side_chains.upl"
    res.to_csv(newname, sep="\t", index=False, float_format='%.3f', header=None)
    return newname, res


def remove_inter_sidechains_with_backbone(file):
    """Takes a .upl upper limit restrain cyana file and remove all distances between sidechains of different residues. In other words, only backbone distances and distances between atoms in a sidechain of the same residue are maintained.
    """
    # read Dataframe
    dt = pd.read_csv(file, sep='\s+', header=None,
                     names=['1_resn', '1_rest', '1_atom', '2_resn', '2_rest', '2_atom', 'upl'])
    # lists
    bckbone = ["C", "CA", "N", "H", "O"]
    sideatoms = ['CB', 'HB', 'HA', 'HB1', 'HB2', 'HB3', 'CG', 'HG2', 'HG3', 'HE21', 'HE22', 'HD1', 'HD2', 'CD1', 'CD2',
                 'HD3', 'HE2', 'HE3', 'HG', 'HD', 'HE', 'NE2', 'ND2', 'NE1', 'QB', 'QG', 'OE1', 'OE2', 'QD1', 'QD2',
                 'QQD', 'QD', 'QE2', 'SD', 'QE', 'OD1', 'OG', 'OD2', 'NE', 'NH1', '1HH1', '2HH2', 'QH2', 'NZ', '1HZ',
                 '2HZ', 'QZ', 'QA', '3HZ', 'HH', 'QH1', 'NH2', 'ND1', 'CD', 'CE', 'CZ', 'HZ']
    # backbone
    resback = dt.loc[dt['1_atom'].isin(bckbone) & dt['2_atom'].isin(bckbone)]
    # sidechains
    sdc = dt[['1_atom', '2_atom']].isin(sideatoms).any(axis=1)
    resside = dt.where(dt[sdc]['1_resn'] == dt[sdc]['2_resn'])
    resside.dropna(inplace=True)
    # concatenate
    frames = [resback, resside]
    conc = pd.concat(frames)
    # polishing
    conc.sort_values("1_resn", ascending=True, inplace=True)
    conc['1_resn'] = conc['1_resn'].astype(int)
    conc['2_resn'] = conc['2_resn'].astype(int)
    newname = os.path.splitext(file)[0] + "_removed_inter_side_chains_backbone.upl"
    conc.to_csv(newname, sep="\t", index=False, float_format='%.3f', header=None)
    return newname, conc
