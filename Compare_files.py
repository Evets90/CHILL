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
    print("START.")
    f1 = open(file1, 'r')
    f2 = open(file2, 'r')
    outname = os.path.splitext(file1)[0] + output
    f3 = open(outname, 'w+')
    diff = []
    line = 0
    for line1 in f1:
        for line2 in f2:
            line += 1
            if line1 != line2:
                f3.write(line1 + line2)
                print(f"File '{file1}': {line1}\nFile '{file2}': {line2}")
                diff.append("Line number " + str(line))
                diff.append("File 1:")
                diff.append(line1)
                diff.append("File 2:")
                diff.append(line2)
                diff.append("Line " + str(line) + "\nFile 1: " + line1 + "File 2: " + line2+"\n")
            break
    return diff
