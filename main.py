import sys
from shutil import copyfile
import os


def endMessage(message):
    print(message)
    input()
    exit()

def getNewNames():
    names = []
    for (_, _, filenames) in os.walk("input"):
        names.extend(filenames)
        break
    
    config = {}
    config["replace"] = []
    config["startremove"] = []
    config["dublicate"] = []
    with open('config.txt', encoding="utf-8") as fp:
        line = fp.readline().replace("\n","")
        while line:
            data = line.split(":")
            config[data[0]].append(data[1:])
            line = fp.readline().replace("\n","")
    print(config)
    newNames = []
    namesDict = {}
    
    global dublicates
    for name in names:
        tmp = name
        for starts,sl in config["startremove"]:
            if (tmp.startswith(starts)):
                tmp = tmp[int(sl):]
        oldlevel = 999
        for level,old, new in config["replace"]:
            if (oldlevel < int(level)):
                continue
            if (old in tmp):
                oldlevel = int(level)
            tmp = tmp.replace(old, new)

        if tmp in namesDict:
            if (len(config["dublicate"]) > 0):
                index = int(tmp[tmp.index(config["dublicate"][0][0])+1:-4])
                ind = index +1
                tmpNew = tmp.replace(config["dublicate"][0][0]+str(index),config["dublicate"][0][0]+str(ind))
                while (tmpNew in namesDict):
                    ind += 1
                    tmpNew = tmp.replace(config["dublicate"][0][0]+str(index),config["dublicate"][0][0]+str(ind))
                tmp = tmp.replace(config["dublicate"][0][0]+str(index),config["dublicate"][0][0]+str(ind))
                newNames.append(name+"\t"+tmp+'\n')
            else:
                newNames.insert(0,">>>>>>"+name+"\t"+tmp+'\n')
                dublicates += 1
        else: 
            newNames.append(name+"\t"+tmp+'\n')
        namesDict[tmp] = 1
    
    fo = open("names.txt","w",encoding="utf-8")
    fo.writelines(newNames)
    fo.close

def renameFiles():
    f = open("names.txt","r", encoding="utf-8") 
    names = f.readlines()
    f.close()
    if (len(names) > 0):
        if (len(names[-1]) == 0):
            names = names[:-1]
    print("Переименовываем "+str(len(names))+" фалов")
    try:
        for name in names:
            oldName, newName = name.strip('\n').split("\t")
            copyfile("input\\"+oldName, "output\\"+newName)
    except Exception as e:
        print("Ошибка!")
        print(e)

if __name__ == "__main__":
    if (len(sys.argv) == 1):
        endMessage("-n создать список файлов, -r переменовать файлы по списку names.txt")
    print(sys.argv[1])
    if sys.argv[1] == "-n":
        dublicates = 0
        getNewNames()
        endMessage("Успешно!")
    if sys.argv[1] == "-r":
        renameFiles()
        endMessage("Успешно!")