import os
from shutil import copy
import random
import json
import sys
def mkfile(file):
    if not os.path.exists(file):
        os.makedirs(file)


# 读取json文件
path = r"data_set/garbage_classify_rule.json"
mkfile('data_set/train')
mkfile('data_set/val')
try:
    f = open(path, encoding='utf-8')
    classes = json.load(f)
    f.close()
except:
    print(sys.exc_info())
for i in range(40):
    mkfile('data_set/pictures/' + classes[str(i)])
    mkfile('data_set/train/' + classes[str(i)])
    mkfile('data_set/val/' + classes[str(i)])

# 打标
import pandas as pd
train_path = r"./data_set/pictures/"
filelist = [file for file in os.listdir(train_path) if ".txt" in file]
piclist = []
for num,txt in enumerate(filelist):
    try:
        print("Prcessing: " + str(num))
        fp = open(train_path + txt,"r")
        content = fp.readline()
        filename,cla = content.split(", ")
        piclist.append({"id":filename,"class":cla})
    except IOError:
        print("Open File Error: " + txt)
    except ValueError:
        print("Error:" + filename)

classinf = pd.DataFrame(piclist)
print("sample numbers: ",classinf.__len__())
classinf.to_csv(r"./data_set/" + "datainfo.csv",index=False)
classinf['class'] = classinf['class'].astype(str)
df = classinf.groupby('class').count().reset_index()
df.to_csv(r"./data_set/classinfo.csv",index=False)

#将图片按照类别划分到不同目录
import pandas as pd
from os import remove
import json
from shutil import move
classinf = pd.read_csv(r"./data_set/datainfo.csv")
classinf['class'] = classinf['class'].astype(str)
path = r"./data_set/garbage_classify_rule.json"
f = open(path, encoding='utf-8')
classes = json.load(f)
despath = r"./data_set/pictures/"
import sys
def mvPicToDic(df):
    """根据类别转移到相应目录"""
    srcpath = r"./data_set/pictures/" + df['id']
    try:
        move(srcpath,despath + classes[df['class']])
    except:
        print("Unexcept error:",sys.exc_info()[0])
        pass
def removeTxt(df):
    name = df['id'].split(".")[0]
    name = name + ".txt"
    try:
        remove(despath + name)
    except FileNotFoundError as err:
        print(err)
        pass


classinf.apply(mvPicToDic,axis=1)
classinf.apply(removeTxt,axis=1)

#随机采样划分训练测试集，采样率0.1
split_rate = 0.1
path = r"data_set/garbage_classify_rule.json"
train = r"data_set/pictures"
f = open(path, encoding='utf-8')
classes = json.load(f)
for _,cla in classes.items():
    cla_path = train + '/' + cla + '/'
    images = os.listdir(cla_path)
    num = len(images)
    eval_index = random.sample(images, k=int(num*split_rate))
    for index, image in enumerate(images):
        if image in eval_index:
            image_path = cla_path + image
            new_path = 'data_set/val/' + cla
            copy(image_path, new_path)
        else:
            image_path = cla_path + image
            new_path = 'data_set/train/' + cla
            copy(image_path, new_path)
        print("\r[{}] processing [{}/{}]".format(cla, index+1, num), end="")  # processing bar
    print()

print("processing done!")
