#!/usr/bin/env python3

# -*- coding: utf-8 -*-
''' Tom Barnowsky, Nils Rothenburger, Robin Schmidt - 2018-11-26
    Netzwerkgestützte Smart-Home Steuerung via Raspberry Pi

    Dies ist die Ulaubs-Modus Steuerung '''

import time
import random
import xml.etree.ElementTree as et

def loadxml() :
    
    global xml
    global root
    
    xml = et.parse('/var/www/html/status.xml')
    root = xml.getroot()
loadxml()
while 1 :
    while root.find('holiday').text == 'on' :
        shufsel = [[device] for device in root.findall('device')]
        device = random.choice(shufsel)[0]
        num = device.get('id')

        changed = False
        print(device.find('name').text)
        exec("""root.find("./*[@id='""" + num + """']/status").text = 'on' """)
        xml.write('/var/www/html/status.xml', encoding = 'utf-8', xml_declaration = True)
        print(device.find('status').text)
        time.sleep(12)
        loadxml()
        if device.find('status').text == 'on' :
            exec("""root.find("./*[@id='""" + num + """']/status").text = 'off' """)
            print(device.find('status').text)
            xml.write('/var/www/html/status.xml', encoding = 'utf-8', xml_declaration = True)
    time.sleep(0.5)
    loadxml()
