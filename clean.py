import os

try:
    os.mkdir("roi")
except:
    None
try:
    os.mkdir("log")
except:
    None

fp = open("log\done.txt", "w")
fp.close()

fp = open("log\log.txt", "w")
fp.write("0")
fp.close()

os.system('del roi\*.txt')
os.system('python3 find_file.py')
