# https://xlsxwriter.readthedocs.io/
# Note: XlsxWriter can only create new files. It cannot read or modify existing files.
from netmiko import ConnectHandler
import getpass
import time
import datetime
import xlsxwriter 
"""
2. This script updates the enable secret on Cisco devices
   Prints results with hostname, ip, serial, and time to device_result.xlsx
"""


workbook = xlsxwriter.Workbook('device_update.xlsx')
worksheet = workbook.add_worksheet('updated')

ip = input('Please enter the ip address: ')

username = input('Enter username: ')
password = getpass.getpass()
device_type = 'cisco_ios'
now = datetime.datetime.now()

net_connect = ConnectHandler(ip=ip, device_type=device_type, username=username, password=password)
print('Connecting to %s' % ip)
time.sleep(1)
device_hostname = net_connect.send_command('show run | include hostname')
hostname = device_hostname[9:]
device_serial = net_connect.send_command('show inventory | include PID')
time.sleep(1)
net_connect.write_channel('config t \n')
time.sleep(1)
net_connect.write_channel('enable secret NewCiscoPassword2019 \n')
time.sleep(1)
net_connect.write_channel('exit \n')
time.sleep(1)
net_connect.write_channel('wri mem \n')
time.sleep(2)
show_session = net_connect.read_channel()
print(show_session)

clock = now.strftime('%m-%d-%Y %H:%M')

bold = workbook.add_format({'bold': True})
worksheet.write("A1", 'Hostname', bold)
worksheet.write("B1", 'IP Address', bold)
worksheet.write("C1", 'Serial Number', bold)
worksheet.write("D1", 'DateTime', bold)
worksheet.write("A2", hostname)
worksheet.write("B2", ip)
worksheet.write("C2", device_serial)
worksheet.write("D2", clock)

workbook.close()

input('##### Enable Secret Update Successfully #####\n Press Enter to Exit')
