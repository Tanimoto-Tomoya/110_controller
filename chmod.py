#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os, subprocess

def main():
    process = subprocess.Popen('usb-devices', stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, error = process.communicate()
    dev_info = str(out).split('\\n')
    del dev_info[0], dev_info[-1], error
    dev_id = -1
    for i in range(len(dev_info)):
        if dev_info[i].find('0ae4') != -1 and dev_info[i].find('0004') != -1:
            dev_id = i
            break
    if dev_id == -1:
        os.sys.exit("Device not connect")
    text = dev_info[dev_id-2].split('=')
    for i in range(len(text)):
        if text[i].find('Dev') != -1:
            dev_id = text[i+1].split(' ')
            break
    for i in range(len(dev_id)):
        try:
            int(dev_id[i])
        except:
            pass
        else:
            dev_id = int(dev_id[i])
            break
    if dev_id <= 9:
        path = "/dev/bus/usb/001/00" + str(dev_id)
    else:
        path = "/dev/bus/usb/001/0" + str(dev_id)
    os.system("sudo chmod 777 "+ path)

if __name__ == "__main__":
    main()

