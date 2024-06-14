# This is a sample Python script.


# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import os


def rename_gopro_all():
    # Use a breakpoint in the code line below to debug your script.

    path = "./"
    file_list = os.listdir(path)
    print(file_list)
    for file in file_list:
        olddir = os.path.join(path, file)
        if os.path.isdir(olddir):
            continue
        filename = os.path.splitext(file)[0]
        filetype = os.path.splitext(file)[1].upper()

        if filetype in [".MP4", ".JPG", ".LRV", ".THM"] and filename[0] == "G" and "_" not in filename:
            print(filename)
            NAME_PREFIX = "GP"
            NAME_DATE = "_"
            NAME_ID = ""
            NAME_INDEX = filename[4:8]
            # filename[x,y]位数是从x到y的前一位，包含filename[x],不包含filename[y]
            NAME_SEQ = ""
            if filename[0] == "G" and filename[1] == "O":
                NAME_SEQ = ""
            if filename[0] == "G" and filename[1] == "P":
                NAME_SEQ = "_" + filename[2:4]

            newdir = os.path.join(
                path, NAME_PREFIX + NAME_DATE + NAME_ID + NAME_INDEX + NAME_SEQ + filetype.lower())
            print(filename, newdir)
            os.rename(olddir, newdir)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    rename_gopro_all()
