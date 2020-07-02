from netmiko import ConnectHandler
from openpyxl import load_workbook
import getpass
import time
import datetime
"""
3. This script updates the enable secret on Cisco devices
   Appends results with hostname, ip, serial, and time to device_result.xlsx
"""


file_location = ('device_update.xlsx')
workbook = load_workbook(file_location)
sheet = workbook.worksheets[0]

ip = input('Please enter the ip address: ')

username = input('Enter username: ')
password = getpass.getpass()
device_type = 'cisco_ios'


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

now = datetime.datetime.now()
clock = now.strftime('%m-%d-%Y %H:%M')
output = [hostname,ip,device_serial,clock]
sheet.append(output)
    
workbook.save(file_location)


input('##### Enable Secret Update Successfully #####\n Press Enter to Exit')
