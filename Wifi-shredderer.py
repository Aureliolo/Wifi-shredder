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


#def print_callback(pkt):
#	capture.pkt(display_filter='wlan.fc.type_subtype eq 4 && !wlan_mgt.ssid eq 0')


#def tshark_wifi_probe():
#	print(os.popen("unbuffer tshark -i mon0 -f 'type mgt subtype probe-req' -w tshark_logfile -F k12text").read())


#def filter_tshark():
#	print(os.popen("unbuffer tail -f tshark_logfile | grep -v SSID=Broadcast > logfile_filtered.txt").read())

def endless_print():
	print("foo")

#def tail_console():
#	print(os.popen("unbuffer tail -f logfile_filtered.txt").read())

capture = pyshark.LiveCapture('mon0', display_filter='wlan.fc.type_subtype eq 4 && !wlan_mgt.ssid eq 0')
#capture = pyshark.LiveCapture('mon0')

print("If you need to setup mon0 in monitor mode type in 2 else 1")
need_setup = input(":")
print(need_setup)
if need_setup == 2:
	print(setup_mon0())


#capture.sniff(5)

#capture.sniff()
for packet in capture.sniff_continuously():
	print('Found following stuff to print:')
	#print_callback(packet)
	tmp=packet.__dict__
	print tmp['layers'][2].get_field_value("ta")
	print tmp['layers'][3].get_field_value("ssid")
	#for in tmp['layers']:
#   print 'Just arrived:', packet

# wlan.fc.type_subtype eq 4 && !wlan_mgt.ssid eq 0
#capture.apply_on_packets(print_callback, timeout=5)

#threadshark=Thread(target=tshark_wifi_probe,name="tshark_wifi_probe")

#threadfiltertshark=Thread(target=filter_tshark,name="filter_tshark")

#threadendlessprint=Thread(target=endless_print,name="endless_print")
#threadshark.run()
#threadfiltertshark.run()
#threadendlessprint.run()
#while 1==1:
#	print(tail_console)

#fill the given variable from the Command that runs the programm into variable wifi_interface

#use wifi_interface to get the phy#????? and fill it into variable wifi_phy in this format(phy?)

#delete wifi_interface 

#make new wifi interface named mon0 type monitor on wifi_phy
#print ("foo" + os.popen("ls").read() + "foo")
#collect the wifi_mon0 data and print it
