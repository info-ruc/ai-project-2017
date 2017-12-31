# -*- coding: utf-8 -*-
"""
Created on Sun Dec 24 19:29:40 2017

@author: Nicholas
"""

from skimage import io,transform
import tensorflow as tf
import numpy as np
 
 
path1 = "D:/document/artificial/present/forward.png"
path2 = "D:/document/artificial/present/left.png"
path3 = "D:/document/artificial/present/right.png"
path4 = "D:/document/artificial/present/back.png"
 
flower_dict = {0:'forward',1:'left',2:'right',3:'back'}
 
w=100
h=100
c=3
 
def read_one_image(path):
    img = io.imread(path)
    img = transform.resize(img,(w,h))
    return np.asarray(img)
 
with tf.Session() as sess:
    data = []
    data1 = read_one_image(path1)
    data2 = read_one_image(path2)
    data3 = read_one_image(path3)
    data4 = read_one_image(path4)
    data.append(data1)
    data.append(data2)
    data.append(data3)
    data.append(data4)
 
    saver = tf.train.import_meta_graph('D:/document/artificial/model/model.ckpt.meta')
    saver.restore(sess,tf.train.latest_checkpoint('D:/document/artificial/model/'))
 
    graph = tf.get_default_graph()
    x = graph.get_tensor_by_name("x:0")
    feed_dict = {x:data}
 
    logits = graph.get_tensor_by_name("logits_eval:0")
 
    classification_result = sess.run(logits,feed_dict)
 
    #打印出预测矩阵
    print(classification_result)
    #打印出预测矩阵每一行最大值的索引
    print(tf.argmax(classification_result,1).eval())
    #根据索引通过字典对应花的分类
    output = []
    output = tf.argmax(classification_result,1).eval()
    
    for i in range(len(output)):
        print("第",i+1,"张图预测:"+flower_dict[output[i]])