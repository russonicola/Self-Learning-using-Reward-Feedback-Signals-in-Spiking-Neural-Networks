from dv import NetworkEventInput
import time
import serial
import statistics

net = None
ser = None

def connect_serial(ser):
    while(ser == None):
        try:
            ser=serial.Serial(

                port='/dev/cu.usbmodem21101',
                baudrate=115200,
                parity=serial.PARITY_NONE,
                stopbits=serial.STOPBITS_ONE,
                bytesize=serial.EIGHTBITS,
                timeout=0 # was 1
                )
        except:
            ser = None
    return ser

def connect_tcp(net):
    while(net == None):
        try:
            net = NetworkEventInput(address='127.0.0.1', port=7777)
        except:
            net = None
    return net

def read():
    count = 0
    events_array=[]
    try:
        for event in net:
            count += 1

            #ser.write((str(event.x)+'\n').encode('utf-8'))
            #ser.flushOutput()

            #time.sleep(0.000001) 
            
            
            if count > 30:
                x = round(statistics.median(events_array))
                print(x)
                ser.write((str(x)+'\n').encode('utf-8'))
                ser.flushOutput()
                events_array=[]
                #print("20")
                #time.sleep(0.1) 
                #break
            else:
                events_array.append(event.x)
        return True
    except:
        return False

ser = connect_serial(ser)
net = connect_tcp(net)
while(True):
    ret = read()
    if ret == False:
        del net
        net = connect_tcp(None)
    ser = connect_serial(ser)
    
    