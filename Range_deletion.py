import pandas as pd


def pcs_range_deletion(file, min, max, column="Residue_Number", iter="off", inverse="off"):
    """
    DESCRIPTION
    This takes a .pcs file (pre-cleaned with CHILL and no metal centers header) and remove all pcs between the provided
    range of residue number (min-max, both included in the deletion).
    At the moment you can only delete a range a time because I am a noob so for multiple ranges deletions just load
    the returned pandas DataFrame into another round of the function with the option iter="on" (so it knows that it is
    not a file but a dataframe).
    Returns a pandas DataFrame.
  USAGE
    pcs_range_deletion(file, min, max)
  ARGUMENTS
    file = .pcs file pre-cleaned with CHILL.
    min = start of the deletion range.
    max = end of the deletion range.
    column = column on which to apply the range deletion. Available columns are the numeric ones ("Residue_Number", "PCS", "Error", "Weight" and "Sample"). Default = "Residue_Number"
    iter = option to pass an already made pandas DataFrame (e.g. from a previous round of function), if "on". Default="off".
    inverse = option to select the inverse of the provided range, so deleting everything that it is NOT in that range. Boundaries are kept. Default = "off"
  NOTES
    Function used to delete specific helices in the context of the Zoolander project.
  EXAMPLES
    result1 = pcs_range_deletion("/Users/stefanocucuzza/Desktop/mypcs.pcs", 1, 50)
    result2 = pcs_range_deletion(result1, 100, 150, iter="on")
        """
    # read dataframes
    if not (column == "Residue_Number" or column == "PCS" or column == "Error" or column == "Weight" or column == "Sample"):
        print("Selected column is not valid. Valid names are 'Residue_Number', 'PCS', 'Error', 'Weight' or 'Sample' (with capitals)")
        exit(1)
    if iter == "on":
        f_read = pd.DataFrame(file)
    else:
        f_read = pd.read_csv(file, sep=' ', names=["Residue_Number","Residue_Type","Atom","PCS","Error","Weight","Sample"], skiprows=1)
    # deleting
    if inverse == "on":
        deleted = f_read.drop(f_read[(f_read[column] < min) & (f_read[column] > max)].index)
    else:
        deleted = f_read.drop(f_read[(f_read[column] >= min) & (f_read[column] <= max)].index)
    deleted = deleted.round(3)
    # internal test
    def test(initialdf, finaldf):
        if inverse == "on":
            toremove = initialdf[(initialdf[column] < min) & (initialdf[column] > max)].index
        else:
            toremove = initialdf[(initialdf[column] >= min) & (initialdf[column] <= max)].index
        if len(initialdf)-len(toremove) == len(finaldf):
            print("Internal test SUCCESFUL.")
        else:
            print(f"Internal test FAILED for file {file}")
    test(f_read, deleted)
    # finalizing
    return deleted