#!/usr/bin/env python3
# 
# Description: Radon Eye (RD200) remote query script 
# 
# Author: Konstantinos Xynos (2020)
# How to: 
#  * Run the application once with get_device = True
#  * Copy the address of you Radon Eye into the address variable 
#  * set get_device = False
# 
# You can get different outputs using command_line = True or False
#
# WARNING: USE THIS SCRIPT AND KNOWLEDGE AT YOUR OWN RISK. IT IS 
# POSSIBLE TO CAUSE ISSUES WITH YOUR DEVICE IF YOU TRANSMIT 
# INCORRECT CODES/COMMANDS AND DATA TO IT. 
# YOU ACCEPT FULL RESPONSILIBITY RUNNING THIS SCRIPT AND/OR ITS CONTENTS
#

import asyncio
from bleak import *
from construct import *
from datetime import datetime

def main():
    print_debug = False
    command_line = True
    get_device = False # can be True or False
    
    address = "" # copy the address here

    radon_eye_struct = Struct(
            "command" / Int8ul,
            "total_msg_size" / Int8ul,
            "measurement" / Float32l
    )

    now = datetime.now()
 
    if get_device:
        async def run():
            devices = await discover()
            print("[+] Running scan")
            print("Address: Description")
            for d in devices:
                print(d)

        loop = asyncio.get_event_loop()
        loop.run_until_complete(run())
        print("[*] Copy your device's address (e.g.named FR:R20..) and set it in the variable address.")
        print("[!] Please accept liability. By changing the flag and executing this script you accept full responsilibity of what might happpen to your device.")
        print("[!] Don't forget to set, get_device = False ")
        print("[!] EOF ")

        exit(1)

    if address == '':
        print("[!] Device address not set. Try scanning using get_device = True ")
        exit(-1)

    LBS_UUID_CONTROL = "00001524-1212-EFDE-1523-785FEABCD123"
    READOUT_UUID = "00001525-1212-EFDE-1523-785FEABCD123"
    if command_line : print("** Radon Eye measurement tracking. **")
    async def run(address):
        try:
            async with BleakClient(address) as client:
                try:

                    x = await client.is_connected()
                    if command_line : print("Connected: {0}".format(x))
                    if x :
                        value_to_send = bytearray([0x50]) # send query command
                        await client.write_gatt_char(LBS_UUID_CONTROL, value_to_send)
                        
                        uuid_results = await client.read_gatt_char(READOUT_UUID)

                        if print_debug: print("Debug message: Read GATT returned (hex): {}".format(uuid_results.hex()))

                        radon_eye_struct_ = radon_eye_struct.parse(uuid_results)
                        if radon_eye_struct_.command == 80:
                            measurement_calc = radon_eye_struct_.measurement * 37
                            if command_line :
                                date_time = now.strftime("%Y/%m/%d, %H:%M:%S")
                                print("YYYY/MM/DD, HH:MM:SS : measurement ")
                                print("{} : {:.2f}".format(date_time,measurement_calc))
                            else:
                                date_time = now.strftime("%Y/%m/%d|%H:%M:%S")
                                print("{}|{:.2f}".format(date_time,measurement_calc))
                finally:
                    await client.disconnect()
        except:
            print("[-] Failed to connect to {}".format(address))
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run(address))


if __name__ == "__main__":
    main()