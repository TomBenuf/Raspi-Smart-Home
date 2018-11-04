#!/usr/bin/python3

# -*- coding: utf-8 -*-
''' Tom Barnowsky, Nils Rothenburger, Robin Schmidt - 2018-11-04
	Netzwerkgestützte Smart-Home Steuerung via Raspberry Pi

	Dies ist der Python3 Backend script.'''

import RPi.GPIO as GPIO
import xml.etree.ElementTree as et

def main() :
	print("works fine")
	xml = et.parse('../www/status.xml')
	root = xml.getroot()
	for device in root.iter('device') :
		for name in device.iter('name') :
			print(name.text)
		
#	print(root.childNodes)
#	device1 = root.firstChild
#	print(device1.nodeName)
#    main()

main()
