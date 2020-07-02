from netmiko import ConnectHandler
import netmiko
import xlrd
import time
import getpass
import re

'''
This script uses an excel spreadsheet to configure multiple devices.
You need a excel spreadhseet interdesc.xlsx
Two text files name failed_devices.txt and success_devices.txt
'''

ip = input('Enter ip address: ')
username = input('Username: ')
password = getpass.getpass()

device_type = 'cisco_ios'

imported_dictionary_raw = {}
imported_dictionary = {}

file_location = 'interdesc.xlsx'
workbook = xlrd.open_workbook(file_location)
sheet = workbook.sheet_by_index(0)
number_of_rows = sheet.nrows

i = 0

for x in range(0, number_of_rows):
    k = sheet.cell_value(i, 0)
    v = sheet.cell_value(i, 1)
    imported_dictionary_raw[k] = v
    i += 1
    
interface = (sheet.cell_value(1, 0))
imported_dictionary[interface] = v

net_connect = ConnectHandler(ip=ip, username=username, password=password, device_type=device_type)

for k, v in imported_dictionary_raw.items():
    interface = k
    interface_descr = v
    print('\n Connecting to: %s.' % ip)
    # enter_interface = net_connect.send_config_set('%s \n %s' % (interface, interface_descr))
    net_connect.write_channel('config t \n')
    net_connect.write_channel('%s \n' % interface)
    show_interface = net_connect.read_channel()
    print(show_interface)
    net_connect.write_channel('no description \n')
    net_connect.read_channel()
    net_connect.write_channel('%s \n' % interface_descr)
    net_connect.read_channel()
    showinterface = net_connect.send_config_set('exit \n do show int descr | sec %s' % interface)
    # print(enter_interface)
    print('Successfully removed %s' % showinterface)
