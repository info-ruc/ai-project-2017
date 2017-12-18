import cv2 
import numpy as np 
from matplotlib import pyplot as plt 
  
# ��򵥵��ԻҶ�ֱ��ͼ��Ϊ���ƱȽϵ�ʵ�� 
def classify_gray_hist(image1,image2,size = (256,256)): 
 # �ȼ���ֱ��ͼ 
 # �������������÷����������� 
 # ����ֱ���ûҶ�ͼ����ֱ��ͼ��������ʹ�õ�һ��ͨ���� 
 # Ҳ���Խ���ͨ������󣬵õ����ͨ����ֱ��ͼ 
 # bins ȡΪ16 
 image1 = cv2.resize(image1,size) 
 image2 = cv2.resize(image2,size) 
 hist1 = cv2.calcHist([image1],[0],None,[256],[0.0,255.0]) 
 hist2 = cv2.calcHist([image2],[0],None,[256],[0.0,255.0]) 
 # ���ԱȽ���ֱ��ͼ 
 plt.plot(range(256),hist1,'r') 
 plt.plot(range(256),hist2,'b') 
 plt.show() 
 # ����ֱ��ͼ���غ϶� 
 degree = 0
 for i in range(len(hist1)): 
  if hist1[i] != hist2[i]: 
   degree = degree + (1 - abs(hist1[i]-hist2[i])/max(hist1[i],hist2[i])) 
  else: 
   degree = degree + 1
 degree = degree/len(hist1) 
 return degree 
  
# ���㵥ͨ����ֱ��ͼ������ֵ 
def calculate(image1,image2): 
 hist1 = cv2.calcHist([image1],[0],None,[256],[0.0,255.0]) 
 hist2 = cv2.calcHist([image2],[0],None,[256],[0.0,255.0]) 
  # ����ֱ��ͼ���غ϶� 
 degree = 0
 for i in range(len(hist1)): 
  if hist1[i] != hist2[i]: 
   degree = degree + (1 - abs(hist1[i]-hist2[i])/max(hist1[i],hist2[i])) 
  else: 
   degree = degree + 1
 degree = degree/len(hist1) 
 return degree 
  
# ͨ���õ�ÿ��ͨ����ֱ��ͼ���������ƶ� 
def classify_hist_with_split(image1,image2,size = (256,256)): 
 # ��ͼ��resize�󣬷���Ϊ����ͨ�����ټ���ÿ��ͨ��������ֵ 
 image1 = cv2.resize(image1,size) 
 image2 = cv2.resize(image2,size) 
 sub_image1 = cv2.split(image1) 
 sub_image2 = cv2.split(image2) 
 sub_data = 0
 for im1,im2 in zip(sub_image1,sub_image2): 
  sub_data += calculate(im1,im2) 
 sub_data = sub_data/3
 return sub_data 
  
# ƽ����ϣ�㷨���� 
def classify_aHash(image1,image2): 
 image1 = cv2.resize(image1,(8,8)) 
 image2 = cv2.resize(image2,(8,8)) 
 gray1 = cv2.cvtColor(image1,cv2.COLOR_BGR2GRAY) 
 gray2 = cv2.cvtColor(image2,cv2.COLOR_BGR2GRAY) 
 hash1 = getHash(gray1) 
 hash2 = getHash(gray2) 
 return Hamming_distance(hash1,hash2) 
  
def classify_pHash(image1,image2): 
 image1 = cv2.resize(image1,(32,32)) 
 image2 = cv2.resize(image2,(32,32)) 
 gray1 = cv2.cvtColor(image1,cv2.COLOR_BGR2GRAY) 
 gray2 = cv2.cvtColor(image2,cv2.COLOR_BGR2GRAY) 
 # ���Ҷ�ͼתΪ�����ͣ��ٽ���dct�任 
 dct1 = cv2.dct(np.float32(gray1)) 
 dct2 = cv2.dct(np.float32(gray2)) 
 # ȡ���Ͻǵ�8*8����Щ����ͼƬ�����Ƶ�� 
 # ��������ȼ���c++������opencvʵ�ֵ�������� 
 # ��python�н����������������ֱ������ȡ��ͼ������ĳһ���� 
 dct1_roi = dct1[0:8,0:8] 
 dct2_roi = dct2[0:8,0:8] 
 hash1 = getHash(dct1_roi) 
 hash2 = getHash(dct2_roi) 
 return Hamming_distance(hash1,hash2) 
  
# ����Ҷ�ͼ������hash 
def getHash(image): 
 avreage = np.mean(image) 
 hash = [] 
 for i in range(image.shape[0]): 
  for j in range(image.shape[1]): 
   if image[i,j] > avreage: 
    hash.append(1) 
   else: 
    hash.append(0) 
 return hash
  
  
# ���㺺������ 
def Hamming_distance(hash1,hash2): 
 num = 0
 for index in range(len(hash1)): 
  if hash1[index] != hash2[index]: 
   num += 1
 return num 
  
  
if __name__ == '__main__': 
 img1 = cv2.imread('30.jpg') 
 cv2.imshow('img1',img1) 
 img2 = cv2.imread('31.jpg') 
 cv2.imshow('img2',img2) 
 #degree = classify_gray_hist(img1,img2) 
 #degree = classify_hist_with_split(img1,img2) 
 #degree = classify_aHash(img1,img2) 
 degree = classify_pHash(img1,img2) 
 print degree 
 cv2.waitKey(0)
