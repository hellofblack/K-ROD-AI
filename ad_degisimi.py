import glob
import os

path = os.path.abspath(os.getcwd())
print(path)
jpgler = glob.glob("*.jpg")
txler = glob.glob("*.txt")
print(len(jpgler), len(txler))

def changetxt():
    n = 1
    for jpg in jpgler:
        exname = path + "\\" + jpg
        os.rename(exname, str(n) + ".jpg")
        n += 1

def changejpg():
    n = 1
    for txt in txler:
        exname = path + "\\" + txt
        os.rename(exname, str(n) + ".txt")
        n += 1


changetxt()
changejpg()
