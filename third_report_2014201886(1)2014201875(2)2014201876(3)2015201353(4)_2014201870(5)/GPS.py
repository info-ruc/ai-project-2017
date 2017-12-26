#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import serial
import time
import sys
import string
import numpy as np

def distance(vec1,vec2):
	
	MLatA = 90 - (vec1[0]/100)
	MLonA = vec1[1]/100
	MLatB = 90 - (vec2[0]/100)
	MLonB = vec2[1]/100

	C = np.sin(MLatA)* np.sin(MLatB)* np.cos(MLonA-MLonB) + np.cos(MLatA)* np.cos(MLatB)
	Distance = 6378137 * np.arccos(C) * np.pi/180

	print Distance
	return Distance

def main():
	print "start"
	port ="COM3"
	bluetooth = serial.Serial(port, 9600)
	print "Connected"
	bluetooth.flushInput()

	previousDistance = 10000000

	target = sys.argv[1]
	[latitude,longitude] = target.split("##")
	[latitue_value,unuse] = latitude.split(" ")
	[longitude_value,unuse] = longitude.split(" ")

	while(True):
		current = bluetooth.readline()
		current = current.replace("\n","")
		print(current + "!")
		if current != "" or current != " ":
			#current = "3958.14217 N##11618.53351 E"
			try:
				[latitude_current,longitude_current] = current.split("##")
			except Exception, e:
				continue
			
			[latitue_value_current,unuse] = latitude_current.split(" ")
			[longitude_value_current,unuse] = longitude_current.split(" ")

			target_vec = [string.atof(latitue_value),string.atof(longitude_value)]
			current_vec = [string.atof(latitue_value_current),string.atof(longitude_value_current)]

			print(target_vec,current_vec)

			currentDistance = distance(target_vec,current_vec)

			if currentDistance < 0.4:
				print("arrive")
				bluetooth.write('5')
				break

			#keep going
			elif currentDistance < previousDistance:
				previousDistance = currentDistance
				bluetooth.write('1')


			#randomright
			else:
				bluetooth.write('9')
				print("turn")

	# print str

	bluetooth.close()

if __name__ == '__main__':
	main()


