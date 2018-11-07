import serial

ser = serial.Serial(port="COM13", baudrate=19200)

try:
    ser.isOpen()
    print("Serial port is open")
except:
    print("Error")
    exit()

if(ser.isOpen()):
    try:
        while(1):
            print(ser.read())
    except Exception:
        print("error")
else:
    print("Cannot open serial port")
