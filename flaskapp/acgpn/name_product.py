from os import listdir
from os.path import isfile, join
onlyfiles = [f for f in listdir("C:/Users/jjm/Desktop/ACGPN/Data_preprocessing/train_color") if isfile(join("C:/Users/jjm/Desktop/ACGPN/Data_preprocessing/train_color", f))]
# print(onlyfiles)

with open("train_pair.txt", "w") as f:
    for i in onlyfiles:
        f.write(f"{i[0:7]}0{i[8:]} {i}\n")