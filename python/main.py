#!/usr/bin/env python3

# -*- coding: utf-8 -*-
''' Tom Barnowsky, Nils Rothenburger, Robin Schmidt - 2018-11-26
    Netzwerkgestützte Smart-Home Steuerung via Raspberry Pi

    Dies ist der Python3 Backend script.'''

import time
import RPi.GPIO as GPIO
import xml.etree.ElementTree as et

#erstelle Klasse um XML Daten zu Laden

class devices :

    def __init__(self, number) :
        self.id = number

    def setname(self, name) :
        self.name = name

    def setstatus(self, status) :
        self.status = status

    def setsignal(self, signal) :
        self.signal = signal

    def settimer(self, timer) :
        self.timer = timer

#Setzte GPIO Nummerierung auf Broadcom
#Dauer 1 an  pin21

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(21, GPIO.OUT)
GPIO.output(21, GPIO.HIGH)


pinlock = [False]*28

def loadxml(url) :

    #lade XML, erstelle Liste mit Klassenattributen von devices
    #.id .name .signal .status .timer wie im xml

    global xml
    global root
    global devs
    
    xml = et.parse(url)
    root = xml.getroot()

    devs = []
    num = 0

    for device in root.findall('device') :

        sig = []
        timer = {'on' : 0,
                'off' : 0}

        devs.append(devices(device.get('id')))

        devs[num].setname(device.find('name').text)

        devs[num].setstatus(device.find('status').text)

        for signal in device.findall('signal') :
            for pin in signal.findall('pin') :
                sig.append(pin.text)
            devs[num].setsignal(sig)

        for timers in device.findall('timer') :
            timer['on'] = int(timers.find('on').text)
            timer['off'] = int(timers.find('off').text)
            devs[num].settimer(timer)

        num = num + 1

while True :

    #Python Hauptprogramm wiederhole für immer

    loadxml('/var/www/html/status.xml')
    changed = False

    for dev in devs :

        #Setzt den Gerätestatus auf on oder off
        #wenn die Aktuelle Zeit größer als die in Timer festgelegte und der Timer nicht 0 ist

        if time.time() >= dev.timer['on'] and dev.timer['on'] != 0 and dev.status == 'off' :
            exec("""root.find("./*[@id='""" + dev.id + """']/status").text = 'on'""")
            changed = True

        if time.time() >= dev.timer['off'] and dev.timer['off'] != 0 and dev.status == 'on' :
            exec("""root.find("./*[@id='""" + dev.id + """']/status").text = 'off'""")
            changed = True

        if dev.status == 'on' :

            #Schalte in signal bestimmte pins auf ON wenn on in status

            for pin in dev.signal :

                pin = int(pin)

                if pinlock[pin] == False :

                    #nur wenn pinlock für pin nicht gesetzt (pin schon 0)

                    GPIO.setup(pin, GPIO.OUT)
                    GPIO.output(pin, GPIO.LOW)
                    pinlock[pin] = True

        elif dev.status == 'off' :

            #Schalte in signal bestimmte pins auf 1 wenn off in status

            for pin in dev.signal :

                pin = int(pin)
            
                if pinlock[pin] == True :
                
                    #nur wenn pinlock für pin noch gesetzt

                    GPIO.setup(pin, GPIO.OUT)
                    GPIO.output(pin, GPIO.HIGH)
                    pinlock[pin] = False
        
    #wenn status geändert wurde speichere in Datei
    
    if changed :
        xml.write('/var/www/html/status.xml', encoding = 'utf-8', xml_declaration = True)
    
    time.sleep(0.2)
