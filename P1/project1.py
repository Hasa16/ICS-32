import os
from pathlib import Path
from shutil import copy
from sys import exit

def files_with_files():
    while True:
        try:
            input1 = input()
            input1_act = input1.split(" ", 1)
            if input1_act[0] == "R":
                filepaths = get_path(Path(input1_act[1]), True)
                for x in filepaths:
                    print(x)
                return filepaths
                break
            elif input1_act[0] == "D":
                filepaths = get_path(Path(input1_act[1]), False)
                for x in filepaths:
                    print(x)
                return filepaths
                break
            else:
                print("ERROR")
        except:
            print("ERROR")



def get_path(path: Path, sub: bool) -> list:
    """Find the path of every file in the directory specified, return list of file paths
        sub argument indicates whether it should recurse through
        subdirectories for files or not
        Automatically sort in lexicographical order
    """
    paths = [i for i in path.iterdir()]
    final = []
    sort = []
    for path in paths:
        if path.is_dir():
            sort += get_path(path, True)
        else:
            final.append(path)
    final.sort()
    return final + sort


def interestA(filepaths: list) -> list:
    interests = []
    print(*filepaths, sep = "\n")
    interests = filepaths
    return interests


        
def interestN(filepaths: list, action1, action2) -> list:
    interests = []
    for files in filepaths:
        root = os.path.basename(files)
        if action2 == root:
            print(files)
            interests.append(Path(files))
        else:
            continue
    return interests

        
def interestE(filepaths: list, action1, action2) -> list:
    interests = []
    extension = action2
    for files in filepaths:
        if files.suffix == ('.' + extension):
            print(files)
            interests.append(Path(files))
        else:
            continue
    return interests



def interestT(filepaths: list, input2) -> list:
    interests = []
    text = input2[2:]
    for files in filepaths:
        f = open(files, 'r', encoding = "utf8", errors = 'ignore')
        if text in f.read():
            print(files)
            interests.append(Path(files))
            f.close()
    return interests



def interestLess(filepaths: list, action1, action2) -> list:
    interests = []
    if action2.isnumeric():
        byte = int(action2)
        for files in filepaths:
            if os.stat(files).st_size < byte:
                print(files)
                interests.append(Path(files))
        return interests



def interestMore(filepaths: list, action1, action2) -> list:
    interests = []
    if action2.isnumeric():
        byte = int(action2)
        for files in filepaths:
            if os.stat(files).st_size > byte:
                print(files)
                interests.append(Path(files))
        return interests
    

def interests_take_action(interests: list):
    while True:
        input3 = input()
        if input3 == "F":
            for files in interests:
                try:
                    f = open(files, 'r', encoding = "utf8")
                    info = f.readline().strip()
                except UnicodeDecodeError:
                    print("NOT TEXT")
                else:
                    print(info)
            break
        if input3 == "D":
            for files in interests:
                copy(files, files.with_suffix(files.suffix + '.dup'))
            break
        if input3 == "T":
            for files in interests:
                files.touch()
            break
        else:
            print("ERROR")

            
def interest_chooser(filepaths: list):
    while True:
        interets = []
        input2 = input()
        input2_act = input2.split(" ", 1)
        act1 = input2_act[0]
        if act1 == ("A") and len(input2_act) == 1:
            interests = interestA(filepaths)
            return interests
        elif act1 == ("N") and len(input2_act) == 2:
            interests = interestN(filepaths, act1, input2_act[1])
            return interests
        elif act1 == ("E") and len(input2_act) == 2:
            interests = interestE(filepaths, act1, input2_act[1])
            return interests
        elif act1 == ("T"):
            interests = interestT(filepaths, input2)
            return interests
        elif act1 == ("<") and len(input2_act) == 2:
            interests = interestLess(filepaths, act1, input2_act[1])
            return interests
        elif act1 == (">") and len(input2_act) == 2:
            interests = interestMore(filepaths, act1, input2_act[1])
            return interests
        else:
            print("ERROR")
    if len(interests) == 0:
        exit()

        
def run():
    filepaths = files_with_files()
    interests = interest_chooser(filepaths)
    interests_take_action(interests)

    

run()
