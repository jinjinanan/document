#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PIL import Image
import os,sys
# from __future__ import print_function

# handBook https://pillow.readthedocs.io/en/latest/handbook/index.html

#-------API----------
im = Image.open('/Users/chenlinbo/Desktop/test/test.jpg')
print(im.format,im.size,im.mode)
# im.show()   #打开图片

#   Convert files to png
infile = '/Users/chenlinbo/Desktop/test/test.jpg'
f,e =os.path.splitext(infile)
outfile = f+'.png'
if infile != outfile :
    try:
        Image.open(infile).save(outfile)    #链式编程
    except IOError :
        print('不可以转换',infile)

# Create JPEG thumbnails






# print('请输入你要转换图片的名字:\n')
# fileName = input()
#
# # print('请输入你想要输出图片的文件夹:\n')
# # directoryPath = input()
#
#
#
#
# im = Image.open(fileName)
# w,h = im.size

# smallImage = im.resize((int(w/2),int(h/2)))
# smallImagePath = directoryPath + '/smallImage.jpg'
# os.mkdir(directoryPath+'/smallImage')
# newImageName = directoryPath+'/smallImage/'+ im.tile+ '.jpg'
# print(newImageName)
# smallImage.save(newImageName,'jpeg')


