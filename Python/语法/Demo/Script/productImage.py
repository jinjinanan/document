#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PIL import Image
import os,sys

#创建文件夹
def createDir(pathDir):
    print(pathDir)
    # 获得此目录下所有的文件名
    names = os.listdir(pathDir)
    # 在此目录下生成新的子目录
    base, curentDir = os.path.split(pathDir)
    # 如果此目录下没有指定目录名，生成
    if not os.path.exists(pathDir + '/' + curentDir):
        os.mkdir(pathDir + '/' + curentDir)
    else:
        print('该目录已经存在：' + pathDir + '/' + curentDir)
        #遍历该文件夹下的文件，过滤掉默认文件
    for n in names :
        b,e = os.path.splitext(n)
        #如果是图片格式，生成缩略图，保存在指定文件夹
        if e == '.jpg' or e == '.png' :
            print('进入')
            productThum(n,pathDir,curentDir)



# 生成缩略图
def productThum(name,path,outpath):
    temp = path + '/' + name
    im = Image.open(temp)
    w,h = im.size
    out, type = os.path.splitext(name)
    outname = path + '/' + outpath + '/' + name
    if type == '.jpg':
        type = 'jpeg'
    if type == '.png':
        type = 'PNG'
    print(temp,outname,type,w/3*2,h/3*2,name)
    im.thumbnail((int(w/3*2),int(h/3*2)))
    im.save(outname,type)

#f 文件
#p 路径
def test(ary):
    print(ary)
    hasParamater = 0

    if not len(ary) > 0:
        print('没有参数')
        hasParamater = 1

    for i,a in enumerate(ary):
        if a == 'f' or a == '-f':
            print(ary[i+1])
            Image.open(ary[i+1]).show()
            hasParamater = 1
        elif a == 'p' or a == '-p':
            createDir(ary[i + 1])
            hasParamater = 1
    if hasParamater == 0:
        print('参数格式不正确')
       



test(sys.argv[1:])