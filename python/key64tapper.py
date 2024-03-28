#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import argparse
import serial
import serial.tools.list_ports
from readchar import readkey, key
import re
from keymaps import matrix_map, matrix_map_sv, key_map,alt_keys, special_keys, LINE_PREFIX

import sys
import termios
import os

# Convert values to hex format
key_matrix = matrix_map_sv
matrix_map_hex = {k: f"0x{v:02X}" for k, v in key_matrix.items()}

BAUD = 19200
serialDevice = None

parser = argparse.ArgumentParser(description='key64tapper, a C64 keyboard emulator.')
specifyDevices = parser.add_mutually_exclusive_group(required=True)
specifyDevices.add_argument('-l', '--list', action='store_true',
                            help='List available USB devices and exit. Use this option to find a device for the -d / --device option.')
specifyDevices.add_argument('-d', '--device', action='store', type=str, dest='usbDevice',
                            help='Specify an Arduino-like USB device to use.')
specifyDevices.add_argument('-D', '--dummy', action='store_true',
                            help='Dummy mode. Don\'t connect to a device, print all serial output to STDOUT instead.')
parser.add_argument('-r', action='store', type=str, dest='rawString', required=False, help='User-supplied string of keys to send.')
parser.add_argument('-i', '--interactive', action='store_true', help='Interactive mode. Whatever you type is passed on to Commodore.')
# parser.add_argument('-u', '--to_uppercase', action='store_true', help='In interactive mode, changes typed-in lower case letters to uppercase.')
parserResults = parser.parse_args()

def get_matrix_value(c) -> int:
    if c in key_matrix:
        return key_matrix[c]
    return -1

def get_special_value(c) -> int:
    if c in special_keys:
        return special_keys[c] | 0x40
    return -1

def combination_to_matrix(c) -> int:
    values = bytearray()
    for l in c.split('+'):
        value = get_matrix_value(l)
        if value >= 0 and values.count(value) == 0:
            values.append(value)
        value = get_special_value(l)
        if value >= 0 and values.count(value) == 0:
            values.append(value)
        
    return values

def build_key_combination(c) -> str:
    key_combo = ""
    if get_matrix_value(c) >=0:
        key_combo = c
       
    elif c in key_map:
        key_combo = key_map[c]
        if key_combo in alt_keys:
            c = readkey()
            key_combo += "+" + build_key_combination(c)
        
    elif re.match('[A-ZÅÄÖ]', c):
        key_combo = "SHIFT_LEFT+" + c.lower()
    else:
        return ""
    if parserResults.dummy:
        print (f"key combination: {key_combo}")
    return key_combo     

def parse_key_combinations(key_combo):
    values = combination_to_matrix(key_combo)

    if len(values) > 0:
        if parserResults.dummy:
            hex_string = ''
            for element in values:
                hex_string += f"0x{element:02X} "
            print(f"values: {hex_string}")
            print('------------ Sent-----------------------' )
        else:
            v_len =len(values)
            written =  arduino.write(bytearray([v_len]))
            written =  arduino.write(values)
            arduino.flush()


def process_key(c) -> int:
    if parserResults.dummy:
        hex_string = ''
        if re.match('[\\w!@#$%^&*()-_=+\\\\|,<.>/?`~\\[\\]{}"\\\']', c):
            print(f"'{c}' in hex = 0x{ord(c):02X}")
        else:
            for element in c:
                hex_string += f"0x{ord(element):02X} "
            print(f"other key: {hex_string}")

    key_combo = build_key_combination(c)
    if key_combo.startswith(LINE_PREFIX):
        for m in re.finditer(r"(\{(\w+)\})|.", key_combo[len(LINE_PREFIX):]):
            # print (m.group().strip("{}"))
            key_combo = build_key_combination(m.group().strip("{}"))
            parse_key_combinations(key_combo)
            time.sleep(.05)    
    else:
        parse_key_combinations(key_combo)    
        
if parserResults.list:
    for p in serial.tools.list_ports.comports():
        print( f"Device: {p.device} ; description: {p.description}")
    exit(0)

elif parserResults.usbDevice:
    print (f"Using device: {parserResults.usbDevice}")

    serialDevice = parserResults.usbDevice

if not parserResults.dummy:
    try:
        arduino = serial.Serial(serialDevice, BAUD, timeout=.1)
        # arduino = serial.Serial(serialDevice, BAUD)
    except:
        print ("Cannot open serial device, exiting.")
        exit(1)
# Give serial interface time to settle down
time.sleep(1)

# Now that we have the connection open, write to it
if parserResults.rawString:
    for k in parserResults.rawString.split(' '):
        combined = ''
        if '+' in k:
            for l in k.split('+'):
                combined += ','.join(list(key_matrix[l]))
                combined += ',_,'
            combined = combined.rstrip(',_,')
        else:
            combined = ','.join(list(key_matrix[k]))

        if parserResults.dummy:
            print(combined)
        else:
            arduino.write(combined + '\n')
        time.sleep(.05)

elif parserResults.interactive or True:
    print("Ready to type.")

    while True:
        c = readkey()
        if  c == key.CTRL_C:
            exit(1)
        if len(c) > 0:
            res = process_key(c)

        if not parserResults.dummy:
            while True:
                line = arduino.readline()
                if line.strip():
                    data = line.decode("utf-8").strip()
                    print(f" --> {data}")  # strip out the new lines for now
                else:
                    break

if not parserResults.dummy:
    arduino.close()
    
    
