#!/usr/bin/env python2
import os
import time
import pyshark
from threading import Thread


def setup_mon0():
    """
    function to sem-automatic delete interface that will be the new Monitor Device standard is mon0
    """

    print("The following output are your wifi interfaces:")

    """
    gives user time to read
    """
    time.sleep(1)

    """
    prints all current Interfaces to the Console
    """
    print(os.popen("iw dev").read())

    """
    get the Information about which Interface to delete and where the new one should be
    """
    print("Please type in the Name of the Wifi Interface that should be deleted and be the new Monitoring Device")
    wifi_interface = raw_input(":")
    print("Please type in the Number that follows after phy# of the interface")
    wifi_ph = input(":")

    """
    add phy to the number of the interface so its easy to use
    """
    wifi_phy = "phy" + str(wifi_ph)

    """
    delete old Interface
    """
    print(os.popen("sudo iw dev " + wifi_interface + " del").read())

    """
    make new Interface onphy of old Interface with name mon0 and type monitor
    """
    print(os.popen("sudo iw phy " + wifi_phy + " interface add mon0 type monitor").read())

    """
    activates new mon0 Interface
    """
    print(os.popen("sudo ip link set mon0 up").read())


def endless_print():
    """
    yet to be made function to send output to endless Printer for into Shredder
    """
    print("foo")


"""
defines which Packages should be captured and on which Interface
"""
capture = pyshark.LiveCapture('mon0', display_filter='wlan.fc.type_subtype eq 4 && !wlan_mgt.ssid eq 0')

"""
asks user if he needs to setup mon0 or if he already has a mon0 in place in type monitor
"""
print("If you need to setup mon0 in monitor mode type in 2 else 1")
need_setup = input(":")
print(need_setup)
if need_setup == 2:
    print(setup_mon0())

"""
for every Package that goes trough the above defined filter in capture print the Sentence "Found following stuff to print"
and on the following Lines it gets the Mac and the SSID as values out of the made dictionary
"""
for packet in capture.sniff_continuously():
    print('Found following stuff to print:')
    tmp = packet.__dict__
    print(tmp['layers'][2].get_field_value("ta"))
    print(tmp['layers'][3].get_field_value("ssid"))

"""
yet to be made thread to print the output out of irl printer
"""
#threadendlessprint=Thread(target=endless_print,name="endless_print")
#threadendlessprint.run()
