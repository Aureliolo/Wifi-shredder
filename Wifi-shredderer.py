#!/usr/bin/python
import os
import time
import pyshark
from threading import Thread 


def setup_mon0():
	print ("The following output are your wifi interfaces:")

	time.sleep(1)

	print (os.popen("iw dev").read())

	print ("Please type in the Name of the Wifi Interface that should be deleted and be the new Monitoring Device")
	wifi_interface = raw_input(":")
	print ("Please type in the Number that follows after phy# of the interface")
	wifi_ph = input(":")

	wifi_phy = "phy" + str(wifi_ph)

	print (os.popen("sudo iw dev " + wifi_interface + " del" ).read())

	print (os.popen("sudo iw phy " + wifi_phy + " interface add mon0 type monitor").read())

	print (os.popen("sudo ip link set mon0 up").read())


def endless_print():
	print("foo")

capture = pyshark.LiveCapture('mon0', display_filter='wlan.fc.type_subtype eq 4 && !wlan_mgt.ssid eq 0')

print("If you need to setup mon0 in monitor mode type in 2 else 1")
need_setup = input(":")
print(need_setup)
if need_setup == 2:
	print(setup_mon0())


for packet in capture.sniff_continuously():
	print('Found following stuff to print:')
	tmp=packet.__dict__
	print tmp['layers'][2].get_field_value("ta")
	print tmp['layers'][3].get_field_value("ssid")

#threadendlessprint=Thread(target=endless_print,name="endless_print")
#threadendlessprint.run()

