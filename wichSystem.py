#!/usr/bin/python3
#coding: utf-8

import re, sys, subprocess
import ipaddress

if len(sys.argv) != 2:
    print("\n[!] Uso: python3" + sys.argv[0] +" <direccion_ip>\n")
    sys.exit(1)

def IpCorrect(ip_address):
    for i in range(0,3):
        try:
            ip_address = ipaddress.ip_address(ip_address)
            return str(ip_address)
        except ValueError:
            print("\n[!] Error: is not an IP, try again")
        if i < 3:
            ip_address = input("IP:").strip()
    sys.exit("\n\n[!!!]BAD INPUT!")
     
def get_ttl(ip_address):

    IpCorrect(ip_address)
        
    proc = subprocess.Popen(["/usr/bin/ping -c 1 %s" % ip_address, ""], stdout = subprocess.PIPE, shell=True)
    (out,err) = proc.communicate()

    out = out.split()
    out = out[12].decode('utf-8')

    ttl_value = re.findall(r"\d{1,3}", out)[0]
    return ttl_value


def get_os(ttl_value):
    ttl_value = int(ttl_value)

    if ttl_value >= 0 and ttl_value <= 64: 
        return "Linux"

    elif ttl_value >= 65 and ttl_value <=128:
        return "windows"

    else:
        return "Not found"
    
if __name__ == '__main__':
    ip_address = sys.argv[1]

    ttl_value = get_ttl(ip_address)
    get_os(ttl_value)

    os_name = get_os(ttl_value)

    print("%s (ttl ->  %s): %s" % (ip_address, ttl_value, os_name))
