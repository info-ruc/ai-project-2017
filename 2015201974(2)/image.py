from aip import AipImageClassify
import cv2
APP_ID = '10325522'
API_KEY = 'bXTL5fNQLUmCufwUHU29yWXY'
SECRET_KEY = 'A0mVuuBy6hLh9MD67RfD9ntgpUBzm6Zu'

client = AipImageClassify(APP_ID, API_KEY, SECRET_KEY)

def get_file_content(filePath):
    with open(filePath, 'rb') as fp:
		    return fp.read()
f = open('time.txt',encoding='UTF-8')
for lines in f:
    vc = cv2.VideoCapture('test1.mp4')
    c=1
    if vc.isOpened():
        rval,frame=vc.read()
    else:
        rval=False
    while rval:
        rval,frame=vc.read()
        if(c==int(lines)):
	        cv2.imwrite('images/'+str(c)+'.jpg',frame)
	        print('')
	        image=get_file_content('images/'+str(c)+'.jpg')
	        options = {}
	        options["top_num"] = 3
	        result = client.animalDetect(image, options)
	        for i in range(3):
	        	print(result.get("result")[i].get("name") + "  score:" + str(result.get("result")[i].get("score")))
	        break
        c=c+1
        cv2.waitKey(1)
vc.release() 

 


