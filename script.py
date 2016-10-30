import os
from progressbar import ProgressBar
import time


#default block
counter = 0
tag = ".html"
file_list = []
default_max_length = 32
default_split_symbol = "_"
new_name_list = []


#function block
def ReplaceLineInFile(fileName, sourceText, replaceText):
    print("Replacing in ", fileName)
    file = open(fileName, 'r')
    text = file.read() #Reads the file and assigns the value to a variable
    file.close() #Closes the file (read session)
    file = open(fileName, 'w') #Opens the file again, this time in write-mode
    file.write(text.replace(sourceText, replaceText)) #replaces all instances of our keyword
    file.close() #Closes the file (write session)


def DelTag(name):
    if ".h" in name:
        pos = name.find(".h")
        name = name[:pos]
        name = name + ".html"
    while "'" in name:
        pos = name.find("'")
        name = name[:pos] +"&apos;"+ name[pos+1:]
    if name[0] == '_':
        name = name[1:]
    return name


def LenList(word_list):
    length = 0
    for index in word_list:
        length += len(index)
    return length


def ShortNamesComponer(word_list, split_symbol):
    name = ""
    for index in word_list:
        name = name + index + split_symbol
    return name


def LongNameComponer(word_list, max_length):
    index = 0
    mid_name = ""
    while max_length - len(word_list[0]) - len(word_list[-1]) - len(mid_name) -5> 0:
        index += 1
        if index < len(word_list) and (word_list[index] != word_list[-1]):
            mid_name = mid_name + split_symbol + word_list[index]

    name = NameCutterNoSplit(str(word_list[0] + mid_name + split_symbol + word_list[-1]), max_length)
    return name


def NameCutterNoSplit(long_name, max_length):
    short_name = long_name[0:(max_length-5)]
    while short_name[-1].isalnum() == False:
        short_name = short_name[:-1]
    if ".h" not in short_name:
        short_name = short_name + ".html"
    return short_name


def NameCutterSplit(long_name, max_length, split_symbol):
    word_list = long_name.split(split_symbol)
    if LenList(word_list) <= 32:
        new_name = ShortNamesComponer(word_list, split_symbol)
    else:
        new_name = LongNameComponer(word_list, max_length)
    return new_name

#body
print("EFnS v0.1 - Easy Filename Shortener.")
if os.name != "posix":
    print("Warning EFnS was tested only on linux-based system.")

print("Current dir:")
print(os.getcwd())
default_dir = os.getcwd()

try:
    os.mkdir("new")
except OSError:
    pass
    
for file in os.listdir(default_dir):
    if tag in file:
        print("--" + str(file))
        counter += 1
        file_list.append(file)

print("TOTAL: %s files with %s tag" % (counter, tag))

try:
    max_length = int(input("Max length of filenames(default = 32, min = 6):"))
    if max_length < 6:
        print('Length value was set to 32!')
except ValueError:
    max_length = default_max_length

answer = input("Do you want to select split symbol (y/n)?:")

if (answer == "y") or (answer == "Y"):
    split_symbol = input("Plese, select split symbol(default = '_'):")
    if split_symbol == "":
        split_symbol = default_split_symbol
    for index in file_list:
        name_raw = NameCutterSplit(index, max_length, split_symbol)
        name = DelTag(name_raw)
        print(name, " LEN:", len(name))
        new_name_list.append(name)
else:
    for index in file_list:
        name_raw = NameCutterNoSplit(index, max_length)
        name = DelTag(name_raw)
        print(name, " LEN:", len(name))
        new_name_list.append(name)


#body2
for index in range(0, len(file_list)):
    ffile = file_list[index]
    with open(ffile, 'r') as file:
        NewFile = new_name_list[index]
        print("Replacing %s" % (ffile))
        for line in file.readlines():
            for indx in range(0, len(file_list)):
                pos1 = line.find(file_list[indx])
                pos2 = pos1 + len(file_list[indx])
                if (pos1 != -1):
                    line = line[:pos1] + new_name_list[indx] + line[pos2:]
            new_file = open("new/%s" % (NewFile), 'a')
            new_file.write(line)
            new_file.close()

print("Done")
