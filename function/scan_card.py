import time
try:
   import serial
except ImportError:
   import pip
   pip.main(['install', 'pyserial'])
   import serial


def scan():

    serial_arduino = None
    i = 0
    while i < 5:
       try:
           serial_arduino = serial.Serial('COM3', 9600, timeout=2)
           i = 6
       except:
            i += 1
            time.sleep(1)

    if not serial_arduino:
        return None
    else:
        serial_arduino.readline()

        while True:
            number = serial_arduino.readline()
            number = number.decode("utf-8")
            number = number.replace('\n', "").replace('\r', '')

            return number
