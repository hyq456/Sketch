import os
import glob
path = './venv/svg/'
path_out = './venv/svg_processed/'  # 输出文件夹


# 读取图片
def read_img(path):
    if not os.path.exists(path_out):
        os.mkdir(path_out)

    cate = [path + '/' + x for x in os.listdir(path) if os.path.isdir(path + '/' + x)]
    for folder in cate:
        for im in glob.glob(folder + '/*.svg'):
            print('processing images : %s' % (im))
            path = "./1.svg"


fi = open(path, "r")
line = fi.readlines()
pathnum = 0
for l in line:
    if l.startswith("<path"):
        pathnum = pathnum + 1
if pathnum // 3 == 0:
    p1 = pathnum // 3
    p2 = pathnum // 3 * 2
elif pathnum // 3 == 1:
    p1 = pathnum // 3 + 1
    p2 = pathnum // 3 * 2 + 1
else:
    p1 = pathnum // 3 + 1
    p2 = pathnum // 3 * 2 + 2

fo1 = open("./1-1.svg", "w")
fo2 = open("./1-2.svg", "w")
fo3 = open("./1-3.svg", "w")
fo4 = open("./1-4.svg", "w")
fo5 = open("./1-5.svg", "w")

# Picture 1
flag = 0
loc = 0
for l in line:
    if not l.startswith("<path"):
        fo1.write(l)
        loc = loc + 1
    elif flag == 0:
        for i in range(0, p1):
            l = re.sub(r'id="\d(\d)?"', 'id="{myid}"'.format(myid=i), line[i + loc], 1)
            fo1.write(l)
        flag = 1

# Picture 2
flag = 0
loc = 0
for l in line:
    if not l.startswith("<path"):
        fo2.write(l)
        loc = loc + 1
    elif flag == 0:
        for i in range(0, p2 - p1):
            l = re.sub(r'id="\d(\d)?"', 'id="{myid}"'.format(myid=i), line[i + loc + p1], 1)
            fo2.write(l)
        flag = 1

# Picture 3
flag = 0
loc = 0
for l in line:
    if not l.startswith("<path"):
        fo3.write(l)
        loc = loc + 1
    elif flag == 0:
        for i in range(0, pathnum - p2):
            l = re.sub(r'id="\d(\d)?"', 'id="{myid}"'.format(myid=i), line[i + loc + p2], 1)
            fo3.write(l)
        flag = 1

# Picture 4 前两部分组合
flag = 0
loc = 0
for l in line:
    if not l.startswith("<path"):
        fo4.write(l)
        loc = loc + 1
    elif flag == 0:
        for i in range(0, p2):
            l = re.sub(r'id="\d(\d)?"', 'id="{myid}"'.format(myid=i), line[i + loc], 1)
            fo4.write(l)
        flag = 1

# Picture 5 后两部份组合
flag = 0
loc = 0
for l in line:
    if not l.startswith("<path"):
        fo5.write(l)
        loc = loc + 1
    elif flag == 0:
        for i in range(0, pathnum - p1):
            l = re.sub(r'id="\d(\d)?"', 'id="{myid}"'.format(myid=i), line[i + loc + p1], 1)
            fo5.write(l)
        flag = 1

fo1.close()
fo2.close()
fo3.close()
fo4.close()
fo5.close()
fi.close()
