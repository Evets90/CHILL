import os


def file_compare(file1, file2, output="_compare_output.txt"):
    """This takes two files and check them line by line for any differences. Anything that is perceived by a software
     as '!==' is reported so for example if File 1 has a single line with the number '6.0' and File 2 has also a
     single line with the number '6.00' this will be counted as a difference.
    This function is meant primarly to check between file differences between different sotwares and so on
    where there will be only very small modifications in a huge file.

    Parameters:
        -File 1: the first file to be compared.
        -File 2: the second file to be compared.
        -Result: for every line not matching, it will be printed out and the output is stored in a "_compare_output.txt"
    """
    f1 = open(file1, 'r')
    f2 = open(file2, 'r')
    line = 0
    for line1 in f1:
        for line2 in f2:
            line += 1
            if line1 != line2:
                #print("Line number " + str(line))
                #print("File 1:")
                #print(line1)
                #print("File 2:")
                #print(line2)
                print("Line " + str(line) + "\nFile 1: " + line1.strip() + "\nFile 2: " + line2.strip() + "\n")
            break