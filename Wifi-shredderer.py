#!/usr/bin/env python2
import os
from collections import defaultdict
import time
import pyshark
import sys
from tabulate import tabulate
from operator import itemgetter


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

def check_if_existing(mac, ssid):
    """
    Checks if the combination of Mac and SSID is already present in the dictionary
    """
    if mac in mac_ssid:
        if mac_ssid[mac] == ssid:
            return 1 
    return 0

"""
asks user if he needs to setup mon0 or if he already has a mon0 in place in type monitor
"""
print("If you need to setup mon0 in monitor mode type in 1 else 0")
need_setup = input(":")
if need_setup == 1:
    setup_mon0()

"""
defines which Packages should be captured and on which Interface
"""
capture = pyshark.LiveCapture('mon0', display_filter='wlan.fc.type_subtype eq 4 && !wlan_mgt.ssid eq 0')

"""
Creates a empty Dictionary where the Mac and SSID is gonna be filled in
"""
mac_ssid = {}

max_len=18
#def myTabulate(data):
 #   ret=""
  #  for i in range(0,len(data)):
   #     ret+'|\t'
    #    ret+data[i][0]
#        ret+'\t|\t'
    #    ret+data[i][0]
    #    ret+'\t|\t'
    #return ret

"""
for every Package that goes trough the above defined filter in capture this for loop takes the ssid and the mac adress out of the packet
and then checks by calling the function check_if_existing if this combination already exists in the dictionary and if not it adds it and
prints the whole dictionary after a clear in the console in a fancy way using tabulate.
"""
for packet in capture.sniff_continuously():
    tmp = packet.__dict__
    mac_address = (tmp['layers'][2].get_field_value("ta"))
    ssid_name = (tmp['layers'][3].get_field_value("ssid"))
    check = check_if_existing(mac_address, ssid_name)
    if check == 0:
        mac_ssid.setdefault(mac_address, set()).add(ssid_name)
        # mac_ssid[mac_address] = ssid_name
        print(os.popen('clear').read())
        headers = ['Mac_Adress', 'SSID']
        data = sorted(mac_ssid.items(), key = itemgetter(0, 1))
       # if len(data) > max_len:

        print(tabulate(data, headers=headers, tablefmt="grid"))
        #else:
         #   print(myTabulate(data))