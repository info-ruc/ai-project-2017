# -*- coding: utf-8 -*-
"""
Created on Sun Dec 24 22:25:03 2017

@author: Nicholas
"""

from skimage import io,transform
import glob
import os
import tensorflow as tf
import numpy as np
import time
 
#数据集地址
path='D:/document/artificial/data/y'
#模型保存地址
 
#将所有的图片resize成100*100
w=100
h=100
c=3
 
#读取图片
def read_img(path):
    cate=[path+x for x in os.listdir(path) if os.path.isdir(path+x)]
    imgs=[]
    labels=[]
    for idx,folder in enumerate(cate):
        for im in glob.glob(folder+'/*.png'):
            img=io.imread(im)
            img=transform.resize(img,(w,h))
            imgs.append(img)
            labels.append(idx)
    return np.asarray(imgs,np.float32),np.asarray(labels,np.int32)

data,label=read_img(path)
print(data,label)