#!/usr/bin/env python3

# -*- coding: utf-8 -*-
''' Tom Barnowsky, Nils Rothenburger, Robin Schmidt - 2019-03-23
    Netzwerkgestützte Smart-Home Steuerung via Raspberry Pi

    Dies ist der Python3 Backend script.'''

import time
import RPi.GPIO as GPIO
import xml.etree.ElementTree as et
from random import choice
from os import path

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

    def setholiday(self, holiday) :
        self.holiday = holiday

#Setzte GPIO Nummerierung auf Broadcom
#Dauer 1 an  pin21

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(21, GPIO.OUT)
GPIO.output(21, GPIO.HIGH)


pinlock = [False]*28

holiday = {'status' : 'off',
        'interval' : 0,
        'running' : False,
        'timer' : 0}


def loadxml(url) :

    #lade XML, erstelle Liste mit Klassenattributen von devices
    #.id .name .signal .status .timer wie im xml

    global xml
    global root
    global devs
    global holiday

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


        devs[num].setholiday(device.find('holiday').text)

        num = num + 1

    for holidays in root.findall('holiday') :

        holiday['status'] = holidays.find('status').text
        holiday['interval'] = float(holidays.find('interval').text)

while True :

    #Python Hauptprogramm wiederhole für immer

    exists = path.isfile('/var/www/html/status.lock') 
    if not exists :
        loadxml('/var/www/html/status.xml')
        changed = False

        if holiday['status'] == 'off' and holiday['running'] :
            id = 0
            for pinl in pinlock:
                if pinl == True :
                    GPIO.setup(id, GPIO.OUT)
                    GPIO.output(id, GPIO.LOW)
                    pinlock[id]  = False
                id += 1
            holiday['running'] = False
            print('holiday turned off', pinlock)


        if holiday['status'] == 'on' and time.time() >= holiday['timer'] :

            id = 0
            for pinl in pinlock :
                if pinl == True :
                    GPIO.setup(id, GPIO.OUT)
                    GPIO.output(id, GPIO.LOW)
                    pinl = False
                id += 1

            shufsel = []

            for dev in devs :
                if dev.holiday == 'on' :
                    shufsel.append(dev)

            if shufsel :

                dev = choice(shufsel)

                for pin in dev.signal :

                    pin = int(pin)
                    GPIO.setup(pin, GPIO.OUT)
                    GPIO.output(pin, GPIO.HIGH)
                    pinlock[pin] = True
                    #print(pin , 'on')

                holiday['timer'] = time.time() + holiday['interval']

            holiday['running'] = True
            #print('holiday turned on')

        for dev in devs :

            #Setzt den Gerätestatus auf on oder off
            #wenn die Aktuelle Zeit größer als die in Timer festgelegte und der Timer nicht 0 ist

            if time.time() >= dev.timer['on'] and dev.timer['on'] != 0 and dev.status == 'off' :
                exec("""root.find("./*[@id='""" + dev.id + """']/status").text = 'on'""")
                exec("""root.find("./*[@id='""" + dev.id + """']/timer").find('on').text = '0'""")
                changed = True

            if time.time() >= dev.timer['off'] and dev.timer['off'] != 0 and dev.status == 'on' :
                exec("""root.find("./*[@id='""" + dev.id + """']/status").text = 'off'""")
                exec("""root.find("./*[@id='""" + dev.id + """']/timer").find('off').text = '0'""")
                changed = True

            if dev.status == 'on' :

                #Schalte in signal bestimmte pins auf ON wenn on in status

                for pin in dev.signal :

                    pin = int(pin)

                    if pinlock[pin] == False :

                        #nur wenn pinlock für pin nicht gesetzt (pin schon 0)

                        GPIO.setup(pin, GPIO.OUT)
                        GPIO.output(pin, GPIO.HIGH)
                        pinlock[pin] = True

            if dev.status == 'off' :

                #Schalte in signal bestimmte pins auf 1 wenn off in status

                for pin in dev.signal :

                    pin = int(pin)

                    if pinlock[pin] == True :

                        #nur wenn pinlock für pin noch gesetzt

                        GPIO.setup(pin, GPIO.OUT)
                        GPIO.output(pin, GPIO.LOW)
                        pinlock[pin] = False


        #wenn status geändert wurde speichere in Datei

        if changed :
            xml.write('/var/www/html/status.xml', encoding = 'utf-8', xml_declaration = True)

        time.sleep(0.2)
