import pandas as pd
import os

def general_docstring():
    """The left part of this page is to convert a .npc file produced by NUMBAT into its respective .pcs file format. The .npc file is paired to a .seq file containing the sequence (three letter code, one amino acid per line).
    The right part of this page is to delete a subset of atoms from an already converted .pcs file.
    """
    # just to a have a general docstring
    pass

modes = ["N+NH", "N+NH+C+CA+CB", "Custom"]


def conversion(file, seq, tolerance, sample, weight):
    """This takes a .npc file produced by NUMBAT and turns into the format .pcs used by CYANA.
    .npc = ResNum / Atom / PCS / tolerance
    .pcs = ResNum / ResType / Atom / PCS / Tolerance / Weight / Sample
    """
    df = pd.read_csv(file, delimiter='\t', names=["Residue_Number", "Atom", "PCS", "Tolerance"])
    df["Sample"] = sample
    df["Tolerance"] = tolerance
    df["Weight"] = weight
    seq_df = pd.read_csv(seq, delimiter='\t', names=["Residue_Type"])
    seq_df.index += 1
    seq_dict = seq_df.to_dict()
    df["Residue_Type"] = df["Residue_Number"].map(seq_dict["Residue_Type"])
    df = df[["Residue_Number", "Residue_Type", "Atom", "PCS", "Tolerance", "Weight", "Sample"]]
    newname = os.path.splitext(file)[0] + "_converted.pcs"
    newheader = "#Residue_Number", "Residue_Type", "Atom", "PCS", "Tolerance", "Weight", "Sample"
    df.to_csv(newname, header=newheader, sep="\t", index=False, float_format='%.3f')
    print(df)
    return newname, df
