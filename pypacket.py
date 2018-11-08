#!/usr/bin/python

# ---------------- READ ME ---------------------------------------------
# This Script is Created Only For Practise And Educational Purpose Only
# This Script Is Created For http://bitforestinfo.blogspot.com
# This Script is Written By
#
#
##################################################
######## Please Don't Remove Author Name #########
############### Thanks ###########################
##################################################
#
#
__author__='''

'''
import socket,struct,binascii,os
import pye
import threading
import pandas as pd
import datetime

print pye.__author__

def printit():
    threading.Timer(7200.0, printit).start()
    global record
    record.to_csv(str(datetime.datetime.now())+ ".csv")
    record = pd.DataFrame(columns = col_names)


if os.name == "nt":
    s = socket.socket(socket.AF_INET,socket.SOCK_RAW,socket.IPPROTO_IP)
    s.bind(("YOUR_INTERFACE_IP",0))
    s.setsockopt(socket.IPPROTO_IP,socket.IP_HDRINCL,1)
    s.ioctl(socket.SIO_RCVALL,socket.RCVALL_ON)
else:
    s=socket.socket(socket.PF_PACKET, socket.SOCK_RAW, socket.ntohs(0x0800))

#Dataframe
col_names = ["source_IP", "destination_IP", "source_MAC", "destination_MAC", "source_Port"]
record = pd.DataFrame(columns = col_names)


printit()


while True:
    pkt=s.recvfrom(65565)
    unpack=pye.unpack()
    #Cleaning
    ip_header = unpack.ip_header(pkt[0][14:34])
    source_ip = ip_header['Destination Address']
    destination_ip = ip_header['Source Address']
    eth_header = unpack.eth_header(pkt[0][0:14])
    source_mac = eth_header['Source Mac']
    destination_mac = eth_header['Destination Mac']
    tcp_header = unpack.tcp_header(pkt[0][34:54])
    source_Port = tcp_header['Source Port']

    if source_ip == destination_ip:
        continue
    
    print "\n\n===>> [+] ------------ Ethernet Header----- [+]"
    for i in unpack.eth_header(pkt[0][0:14]).iteritems():
        a,b=i
        print "{} : {} | ".format(a,b),
    print "\n===>> [+] ------------ IP Header ------------[+]"
    for i in unpack.ip_header(pkt[0][14:34]).iteritems():
        a,b=i
        print "{} : {} | ".format(a,b),
    print "\n===>> [+] ------------ Tcp Header ----------- [+]"
    for  i in unpack.tcp_header(pkt[0][34:54]).iteritems():
        a,b=i
        print "{} : {} | ".format(a,b),
    record.loc[len(record)] = [source_ip,destination_ip,source_mac,destination_mac,source_Port]
    
