import os
import csv

total_filename = []
nowPath = os.getcwd()
filelist = []
patient = set()
patient_csv = []


def walk(path):
    for item in os.listdir(path):
        subpath = os.path.join(path, item)
        if os.path.isdir(subpath):
            walk(subpath)
        else:
            if subpath.find(".avi") != -1:
                filelist.append(subpath)
                patient.add(subpath.split('\\')[-2])


walk(nowPath)
fp = open("log\\file_list.txt", "w")
for file in filelist:
    print(file)
    fp.write(file+"\n")
fp.close()

patient_sort = sorted(patient)
print(patient_sort)

with open("log\\patient_type.csv", "w", newline='') as file:
    writer = csv.writer(file)
    for num in patient_sort:
        writer.writerow([str(num), 0, 0, 0, 0, 0, 0, 0, 0])
        # writer.writerow([str(123)])


fp = open("log\\log.txt", "w")
fp.write("0")
fp.close()

try:
    fp = open("log\\done.txt", "r")
    fp.close()
except:
    fp = open("log\\done.txt", "w")
    fp.close()
