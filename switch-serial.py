#!/usr/bin/env python3
import serial
import time
import sys

def connect_switch():
    ser = serial.Serial('/dev/ttyUSB0', 38400, timeout=1)
    time.sleep(0.3)
    ser.read(4096)  # Clear buffer
    
    # Get prompt
    ser.write(b'\r\n')
    time.sleep(0.3)
    ser.read(4096)
    
    return ser

def send_cmd(ser, cmd, wait=0.5, read_more=True):
    ser.write(cmd.encode() + b'\r\n')
    time.sleep(wait)
    output = ser.read(4096).decode('utf-8', errors='ignore')
    
    # Handle "More" prompts
    while read_more and '---- More ----' in output:
        ser.write(b' ')
        time.sleep(0.3)
        output += ser.read(4096).decode('utf-8', errors='ignore')
    
    return output.strip()

def get_info(ser):
    # Summary already works
    output = send_cmd(ser, 'summary', 1)
    print("=== SYSTEM INFO ===")
    print(output)
    
    # Get IP configuration
    print("\n=== IP CONFIG ===")
    output = send_cmd(ser, 'ipsetup', 0.5)
    print(output)

if __name__ == '__main__':
    if len(sys.argv) > 1:
        cmd = ' '.join(sys.argv[1:])
        ser = connect_switch()
        output = send_cmd(ser, cmd, 1)
        print(output)
        ser.close()
    else:
        ser = connect_switch()
        get_info(ser)
        ser.close()