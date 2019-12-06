#!/usr/bin/env python3
import usb
import sys


class UsbDevice:
    def __init__(self, vendor_id, product_id):
        busses = usb.busses()
        self.handle = None
        for bus in busses:
            devices = bus.devices
            for dev in devices:
                if dev.idVendor == vendor_id and dev.idProduct == product_id:
                    self.dev = dev
                    self.conf = self.dev.configurations[0]
                    self.intf = self.conf.interfaces[0][0]
                    self.endpoints = []
                    for endpoint in self.intf.endpoints:
                        self.endpoints.append(endpoint.address)
                    return
        raise IndentationError("Not found device!")

    def open(self):
        if self.handle:
            self.handle = None
        self.handle = self.dev.open()
        self.handle.setConfiguration(self.conf)
        self.handle.claimInterface(self.intf)
        self.handle.setAltInterface(self.intf)


def setup():
    global dev, mascon, brake
    dev = UsbDevice(0x0AE4, 0x0004)
    dev.open()
    mascon, brake = 0, 0


def main():
    try:
        array = dev.handle.bulkRead(dev.endpoints[0], 6)
        check = True
    except usb.core.USBError:
        check = False
    except KeyboardInterrupt:
        sys.exit(0)
    except:
        check = False
    if check:
        if array[1] != 255:
            global brake
            brake = array[1]
            brake = brake - 121
            if brake == 0:
                brake = 0
            elif brake == 17:
                brake = 1
            elif brake == 27:
                brake = 2
            elif brake == 33:
                brake = 3
            elif brake == 41:
                brake = 4
            elif brake == 47:
                brake = 5
            elif brake == 54:
                brake = 6
            elif brake == 57:
                brake = 7
            elif brake == 60:
                brake = 8
            else:
                brake = 9
        if array[2] != 255:
            if brake != 0:
                return [0, brake]
            mascon = array[2]
            mascon = 129 - mascon
            if mascon == 20:
                mascon = 1
            elif mascon == 45:
                mascon = 2
            elif mascon == 66:
                mascon = 3
            elif mascon == 96:
                mascon = 4
            elif mascon == 129:
                mascon = 5
            else:
                mascon = 0
    return [mascon, brake]


if __name__ == "__main__":
    setup()
    while True:
        print(main())
