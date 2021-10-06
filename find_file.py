import os

total_filename = []
nowPath = os.getcwd()
filelist = []


def walk(path):
    for item in os.listdir(path):
        subpath = os.path.join(path, item)
        if os.path.isdir(subpath):
            walk(subpath)
        else:
            if subpath.find(".avi") != -1:
                filelist.append(subpath)

walk(nowPath)
fp = open("file_list.txt", "w")
for file in filelist:
    print(file)
    fp.write(file+"\n")
