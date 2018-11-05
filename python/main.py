#!/usr/bin/python3

# -*- coding: utf-8 -*-
''' Tom Barnowsky, Nils Rothenburger, Robin Schmidt - 2018-11-05
    Netzwerkgestützte Smart-Home Steuerung via Raspberry Pi

    Dies ist der Python3 Backend script.'''

import RPi.GPIO as GPIO
import xml.etree.ElementTree as et

def main() :

    #lade XML erstelle Klasse dev[ZAHL] mit Attributen
    #.id .name .type .signal .status wie im xml

    xml = et.parse('../www/status.xml')
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

    dev = []
    num = 0

    for device in list(root) :

        sig = []
        dev.append(devices(device.get('id')))

        for name in device.iter('name') :
            dev[num].setname(name.text)

        for status in device.iter('status') :
            dev[num].setstatus(status.text)

        for type in device.iter('type') :
            dev[num].settype(type.text)

        for signal in device.iter('signal') :
            for pin in signal.iter('pin') :
                sig.append(pin.text)
            dev[num].setsignal(sig)

        num = num + 1

    #Das ist nur eine Testanzeige ob alles korrekt aus dem xml geladen wird

    print(dev[0].id, dev[0].name, dev[0].type, dev[0].signal, dev[0].status)
    print(dev[1].id, dev[1].name, dev[1].type, dev[1].signal, dev[1].status)
main()
