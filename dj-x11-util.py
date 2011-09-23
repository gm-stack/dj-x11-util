#!/usr/bin/env python
import sys,serial
serialport = sys.argv[1]
print "Opening serial port: %s" % serialport
ser = serial.Serial(serialport,57600,timeout=1)

def issueCommand(command):
    ser.write(command + "\r")
    ser.readline()
    return ser.readline()[:-2]

print "Checking for device: ",
print issueCommand("AL~DJ-X11E")

print "Issuing read: ",
print issueCommand("AL~F01900R")