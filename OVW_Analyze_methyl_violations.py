import pandas as pd
import os
import re


def violations_upl_metprot(file, viol_type, what, mode, info="on", remaining="off"):
    """Take an .ovw overview file produced by cyana and check how many violations are between a selected
    group of atoms. The user has to load the file, select a type of violation (upl, vdw, ...), select a
    group of atoms to monitor and then a mode.
    As the page name suggests, current available group of atoms are all involved in the methyl group. The
    mode defines whether to track violations between a select atom an something else ('single') or between
    two selected atoms ('double'). If the option 'inverse' is checked, the remaining violations are
    printed.

    """
    res = pd.DataFrame()
    # Read DataFrame
    r = open(file, 'r')
    file2 = os.path.splitext(file)[0] + "tmp.txt"
    w = open(file2, 'w+')
    for line in r:
        if viol_type == "Upper":
            if "Upper" in line:
                end = line.find(re.findall('\d+.\d+', line)[-1]) + len(re.findall('\d+.\d+', line)[-1])
                w.write(line[:end] + "\n")
        elif viol_type == "VdW":
            if "VdW" in line:
                end = line.find(re.findall('\d+.\d+', line)[-1]) + len(re.findall('\d+.\d+', line)[-1])
                w.write(line[:end] + "\n")
    dt = pd.read_csv(file2, sep="\s+",
                     names=['Type', '1_atom', '1_rest', '1_resn', '-', '2_atom', '2_rest', '2_resn', 'upl', '#', 'mean',
                            'max'], header=None)
    met_prot = ['HG21', 'HG22', 'HG23', 'HB1', 'HB2', 'HB3', 'HG21', 'HG22', 'HG23', 'HG11', 'HG12', 'HG13', 'HD11',
                'HD12', 'HD13', 'HD21', 'HD22', 'HD23', 'HD11', 'HD12', 'HD13', 'HG21', 'HG22', 'HG23', 'HE1', 'HE2',
                'HE3']
    HB = ['HB2', 'HB3']
    HG = ['HG2', 'HG3']
    HD = ['HD2', 'HD3']
    HB_HG_HD = ['HB2', 'HB3', 'HG2', 'HG3', 'HD2', 'HD3']
    HA_HB_HG_HD_HE_CG_CD = ['HA1', 'HA2', 'HB2', 'HB3', 'HG2', 'HG3', 'HD2', 'HD3', 'HD21', 'HD22', 'HG11', 'HG12',
                            'HG13', 'HG21', 'HG22', 'HG23', 'HE1', 'HE2', 'HE3', 'CG1', 'CG2', 'CD1', 'CD2']
    if what == "All methyl protons":
        if mode == "double":
            res = dt.loc[dt['1_atom'].isin(met_prot) & dt['2_atom'].isin(met_prot)]
        elif mode == "single":
            res = dt.loc[dt['1_atom'].isin(met_prot) | dt['2_atom'].isin(met_prot)]
        else:
            print("Incorrect mode selected.")
            exit(1)
    elif what == "HB":
        if mode == "double":
            res = dt.loc[dt['1_atom'].isin(HB) & dt['2_atom'].isin(HB)]
        elif mode == "single":
            res = dt.loc[dt['1_atom'].isin(HB) | dt['2_atom'].isin(HB)]
        else:
            print("Incorrect mode selected.")
            exit(1)
    elif what == "HG":
        if mode == "double":
            res = dt.loc[dt['1_atom'].isin(HG) & dt['2_atom'].isin(HG)]
        elif mode == "single":
            res = dt.loc[dt['1_atom'].isin(HG) | dt['2_atom'].isin(HG)]
        else:
            print("Incorrect mode selected.")
            exit(1)
    elif what == "HD":
        if mode == "double":
            res = dt.loc[dt['1_atom'].isin(HD) & dt['2_atom'].isin(HD)]
        elif mode == "single":
            res = dt.loc[dt['1_atom'].isin(HD) | dt['2_atom'].isin(HD)]
        else:
            print("Incorrect mode selected.")
            exit(1)
    elif what == "HB_HG_HD":
        if mode == "double":
            res = dt.loc[dt['1_atom'].isin(HB_HG_HD) & dt['2_atom'].isin(HB_HG_HD)]
        elif mode == "single":
            res = dt.loc[dt['1_atom'].isin(HB_HG_HD) | dt['2_atom'].isin(HB_HG_HD)]
        else:
            print("Incorrect mode selected.")
            exit(1)
    elif what == "HA_HB_HG_HD_HE_CG_CD":
        if mode == "double":
            res = dt.loc[dt['1_atom'].isin(HA_HB_HG_HD_HE_CG_CD) & dt['2_atom'].isin(HA_HB_HG_HD_HE_CG_CD)]
        elif mode == "single":
            res = dt.loc[dt['1_atom'].isin(HA_HB_HG_HD_HE_CG_CD) | dt['2_atom'].isin(HA_HB_HG_HD_HE_CG_CD)]
        else:
            print("Incorrect mode selected.")
            exit(1)
    else:
        print(
            "Incorrect 'what' selected. Currently supported options are 'met_prot', 'HB', 'HG', 'HD', 'HB_HG_HD', 'HA_HB_HG_HD_HE_CG_CD'.")
        exit(1)
    if info == "on":
        print(f"Starting file: {file}.")
        print(f"checked for {mode} {viol_type} violations of the {what} atoms:")
        if what == "met_prot":
            print(*met_prot)
        elif what == "HB":
            print(*HB)
        elif what == "HG":
            print(*HG)
        elif what == "HD":
            print(*HD)
        elif what == "HB_HG_HD":
            print(*HB_HG_HD)
        elif what == "HA_HB_HG_HD_HE_CG_CD":
            print(*HA_HB_HG_HD_HE_CG_CD)
        print(f"Initial violations analyzed: {len(dt)}.")
        print(f"Selected violations found: {len(res)} ({round((len(res) * 100) / len(dt), 2)}%)\n\n")

    def get_remaining(result, initial):
        pull = pd.concat([initial, result])
        pull = pull.drop_duplicates(keep=False)
        print(f"Total non selected violations {len(pull)}. List:")
        return pull

    newname = os.path.splitext(file)[0] + "_methyl.txt"
    os.remove(file2)
    if remaining == "on":
        pull = get_remaining(res, dt)
        pull.to_csv(newname, sep=" ", index=False, float_format='%.3f', header=None)
        return newname, pull
    else:
        res.to_csv(newname, sep=" ", index=False, float_format='%.3f', header=None)
        return newname, res

