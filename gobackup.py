import os
import pandas
import netmiko
import time

f = open('c:/users/louis/desktop/devops/list.xlsx','rb')
form = pandas.read_excel(f)
firstRouter = form.loc[0].IP.encode("ascii")
InvalidPass = ''
loginVerify = 'true'
output = ''
verifyPass = ''

net_connect = netmiko.ConnectHandler(device_type='cisco_ios', ip='100.100.100.100', username='username', password='password')
net_connect.write_channel('telnet vrf vrf-name ' + firstRouter + '\n')
time.sleep(3)
net_connect.write_channel('username'+'\n')
time.sleep(2)
net_connect.write_channel('password'+'\n')
time.sleep(2)
net_connect.write_channel('en'+'\n')
time.sleep(2)
net_connect.write_channel('en-password'+'\n')
time.sleep(2)
net_connect.write_channel('show run'+'\n')
time.sleep(5)
output = net_connect.read_channel()

filename = form.loc[0].RouterName + '.txt'
fp=open(filename,"w")
fp.write(output.replace('username', ''))
fp.close()

i = 1
while i <= 24:
    net_connect.write_channel('telnet '+ form.loc[i].IP + '\n')
    time.sleep(2)
    net_connect.write_channel('username'+'\n')
    time.sleep(1)
    net_connect.write_channel('password'+'\n')
    time.sleep(4)
    verifyPass = net_connect.read_channel()
    if 'invalid' in verifyPass or 'failed' in verifyPass:
        net_connect.write_channel('cisco'+'\n')
        time.sleep(1)
        net_connect.write_channel('cisco'+'\n')
        time.sleep(4)
        verifyPass = net_connect.read_channel()
        if 'invalid' in verifyPass or 'failed' in verifyPass:
            ID = form.loc[i].RouterName
            print ID
            loginVerify = 'false'
            net_connect.write_channel('another-username'+'\n')
            time.sleep(1)
            net_connect.write_channel('another-password'+'\n')
            time.sleep(4)
            InvalidPass = InvalidPass + form.loc[i].RouterName + '\n'
    if loginVerify == 'true':
        net_connect.write_channel('en'+'\n')
        time.sleep(2)
        net_connect.write_channel('en-password'+'\n')
        time.sleep(65)
        net_connect.write_channel('show run'+'\n')
        time.sleep(7)
        output = net_connect.read_channel()
        filename = form.loc[i].RouterName + '.txt'
        fp=open(filename,"w")
        fp.write(output.replace('username', ''))
        fp.close()
        net_connect.write_channel('quit'+'\n')
        time.sleep(2)
    i += 1
    loginVerify = 'true'

filename = 'NoPass.txt'
fp=open(filename,"w")
fp.write(InvalidPass)
fp.close()

net_connect.write_channel('quit'+'\n')
net_connect.write_channel('quit'+'\n')