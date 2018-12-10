#!/usr/bin/env python3

# -*- coding: utf-8 -*-
''' Tom Barnowsky, Nils Rothenburger, Robin Schmidt - 2018-12-10
    Netzwerkgestützte Smart-Home Steuerung via Raspberry Pi

    Dies ist die Ulaubs-Modus Steuerung '''

from time import sleep
from random import choice
import xml.etree.ElementTree as et

def loadxml() :
    
    #läd xml status.xml

    global xml
    global root
    
    xml = et.parse('/var/www/html/status.xml')
    root = xml.getroot()

while True:

    #Endlosschleife wenn fragt holiday in xml ab

    loadxml()
    if root.find('holiday').find('status').text == 'on' :

        #wenn holiday/status 'on' ist wird zufälliges device/status=on Gerät gewählt,
        #angeschlatet und nach in holiday/interval festgelegtem Zeitintervall wieder ausgeschaltet

        shufsel = []
        changed = False

        for device in root.findall("./device/[holiday='on']") :
            shufsel.append(device)

            if device.find('status').text == 'on' :

                #Schaltet alle für holiday gewählten Geräte aus

                device.find('status').text = 'off'
                changed = True

            if changed :
                xml.write('/var/www/html/status.xml', encoding = 'utf-8', xml_declaration = True)

        if shufsel :

            #überspringt wenn kein Gerät ausgewählt
            
            device = choice(shufsel)
            num = device.get('id')
            #print(device.find('name').text)

            exec("""root.find("./*[@id='""" + num + """']/status").text = 'on' """)
            xml.write('/var/www/html/status.xml', encoding = 'utf-8', xml_declaration = True)
            #print('on')

            interval = 2*int(root.find('holiday').find('interval').text)
            stop = False

            for x in range(0,interval):

                #fragt alle 0.5s holiday/status

                loadxml()
                if root.find('holiday').find('status').text == 'on' :
                    sleep(0.5)

                else :
                    break

            exec("""root.find("./*[@id='""" + num + """']/status").text = 'off' """)
            xml.write('/var/www/html/status.xml', encoding = 'utf-8', xml_declaration = True)
            #print('off')
            #print(root.findall("./device/[status='on']"))

    sleep(0.5)
