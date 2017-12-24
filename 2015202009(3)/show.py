#!/bin/python

import time
import numpy as np
from PIL import Image
from keras.models import load_model
from cv2 import *
import cv2
import h5py

model = load_model('model.h5')

def load_image(imageurl):
	im = cv2.resize(cv2.imread(imageurl), (224,224)).astype(np.float32)
	im[:,:,0] -= 103.939
	im[:,:,1] -= 116.779
	im[:,:,2] -= 123.68
	im = im.transpose((2,0,1))
	im = np.expand_dims(im, axis = 0)
	return im

def predict(url):
	im = load_image(url)
	pre = np.argmax(model.predict(im))
	print(url, "done")

# 
cam = VideoCapture(0)   # 0 -> 
# 
for x in range(0,100):
	s, img = cam.read()
	time.sleep(2)
	if s:
		# 
		imwrite("Images/"+str(x)+".jpg",img)
		print("saved", x)
		
		im = Image.open('Images/' + str(x) + '.jpg').convert('L').resize((100, 100))
		im = np.array(im).reshape(1, 100, 100, 1)
		print(x, "read")
		
		#print("predict", x)
		#predict("Images/" + str(x) + ".jpg")


		print(model.predict(im))

