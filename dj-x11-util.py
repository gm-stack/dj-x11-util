#!/usr/bin/env python
import sys,serial
serialport = sys.argv[1]
print "Opening serial port: %s" % serialport
ser = serial.Serial(serialport,57600,timeout=1)

def issueCommand(command):
    ser.write(command + "\r")
    ser.readline()
    return ser.readline()[:-2]

def readSlot(slot):
    return issueCommand("AL~%.6XR" % (0xF01200 + (slot * 0x40)))

def decodeFreq(data):
    bytes = [data[0:2],data[2:4], data[4:6],data[6:8]]
    dataS = "".join(bytes[::-1])
    return int(dataS,16)

def decodeName(data):
    res = ""
    for character in data[::2]:
        res += chr(int(character,16))
    return res

def decodeChannel(data):
# this looks like a job for struct but it's really not, it's not binary
    result = {}
    print "data is: " + data
    result['overflow'] = data[0:2]
    result['freq'] = decodeFreq(data[2:10])
    result['modulation'] = data[10:12]
    result['step'] = data[12:14]
    result['shiftfreq'] = data[14:22]
    result['shift'] = data[22:24]
    result['tsqmode'] = data[24:26]
    result['tsqfreq'] = data[26:28]
    result['dcs'] = data[28:30]
    result['unknown'] = data[30:36]
    result['skip'] = data[36:38]
    result['name'] = decodeName(data[64:])
    return result
    
    

print "Checking for device: ",
print issueCommand("AL~DJ-X11E")

print "Issuing read: ",
result = readSlot(0)
print decodeChannel(result)