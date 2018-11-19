#!/usr/bin/env python3

# -*- coding: utf-8 -*-
''' Tom Barnowsky, Nils Rothenburger, Robin Schmidt - 2018-11-19
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

#Setzte GPIO Nummerierung auf Broadcom
#Dauer 1 an  pin21

GPIO.setmode(GPIO.BCM)
GPIO.setup(21, GPIO.OUT)
GPIO.output(21, GPIO.HIGH)


pinlock = [False]*28

def loadxml(url) :

    #lade XML, erstelle Liste mit Klassenattributen von devices
    #.id .name .type .signal .status wie im xml

    xml = et.parse(url)
    root = xml.getroot()


    global devs

    devs = []
    num = 0

    for device in list(root) :

        sig = []
        devs.append(devices(device.get('id')))

        for name in device.iter('name') :
            devs[num].setname(name.text)

        for status in device.iter('status') :
            devs[num].setstatus(status.text)

        for signal in device.iter('signal') :
            for pin in signal.iter('pin') :
                sig.append(pin.text)
            devs[num].setsignal(sig)

        num = num + 1

while 1 :

    #Python Hauptprogramm wiederhole für immer

    loadxml('/var/www/html/status.xml')

    for dev in devs :

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

        time.sleep(0.5)
