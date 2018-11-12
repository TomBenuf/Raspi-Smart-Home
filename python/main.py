#!/usr/bin/python3

# -*- coding: utf-8 -*-
''' Tom Barnowsky, Nils Rothenburger, Robin Schmidt - 2018-11-12
    Netzwerkgestützte Smart-Home Steuerung via Raspberry Pi

    Dies ist der Python3 Backend script.'''

import time
import RPi.GPIO as GPIO
import xml.etree.ElementTree as et

GPIO.setmode(GPIO.BCM)

pinlock = [False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False] 

def loadxml(url) :

    #lade XML erstelle Klasse dev[ZAHL] mit Attributen
    #.id .name .type .signal .status wie im xml

    xml = et.parse(url)
    root = xml.getroot()

    class devices :

        def __init__(self, number) :
            self.id = number

        def setname(self, name) :
            self.name = name

        def setstatus(self, status) :
            self.status = status

        def settype(self, type) :
            self.type = type

        def setsignal(self, signal) :
            self.signal = signal

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

        for type in device.iter('type') :
            devs[num].settype(type.text)

        for signal in device.iter('signal') :
            for pin in signal.iter('pin') :
                sig.append(pin.text)
            devs[num].setsignal(sig)

        num = num + 1

while 1:

    #Python Hauptprogramm wiederhole für immer

    loadxml('/var/www/html/status.xml')

    for dev in devs :

        if dev.status == 'on' :

            #Schalte in signal bestimmte pins auf ON wenn on in status

            for pin in dev.signal :

                pin = int(pin)

                if pinlock[pin] == False :

                    #nur wenn pinlock für pin nicht gesetzt (pin schon an)

                    GPIO.setup(pin, GPIO.OUT)
                    GPIO.output(pin, GPIO.HIGH)
                    pinlock[pin] = True

        elif dev.status == 'off' :

            #Schalte in signal bestimmte pins auf OFF wenn off in status

            for pin in dev.signal :

                pin = int(pin)
                GPIO.setup(pin, GPIO.OUT)
                GPIO.output(pin, GPIO.LOW)
                pinlock[pin] = False

        time.sleep(0.5)
