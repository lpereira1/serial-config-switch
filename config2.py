import serial
from time import sleep
import time
# Open the serial port. The settings are set to Cisco default.
serial_port = serial.Serial(port='COM3', baudrate=9600, timeout=None, parity=serial.PARITY_NONE, bytesize=serial.EIGHTBITS,
                            stopbits=serial.STOPBITS_ONE, xonxoff=False)

# Make sure there is not any lingering input - input in this case being data waiting to be received
serial_port.flushInput()

print(serial_port.name)

serial_port.write("\n\r\n\r".encode())

serial_port.write("?".encode())

bytes_to_read = serial_port.inWaiting()

# Give the line a small amount of time to receive data
sleep(.5)

# 9600 baud is not very fast so if you call serial_port.inWaiting() without sleeping at all it will likely just say
# 0 bytes. This loop sleeps 1 second each iteration and updates bytes_to_read. If serial_port.inWaiting() returns a
# higher value than what is in bytes_to_read we know that more data is still coming in. I noticed just by doing a ?
# command it had to iterate through the loop twice before all the data arrived.
while bytes_to_read < serial_port.inWaiting():
    bytes_to_read = serial_port.inWaiting()
    sleep(1)
input_data = serial_port.read(serial_port.inWaiting()).decode()
if 'Username' in input_data:
    console.write(credentials.username.encode() + '\r\n'.encode())
time.sleep(1)
input_data = serial_port.read(serial_port.inWaiting())

# This line reads the amount of data specified by bytes_to_read in. The .decode converts it from a type of "bytes" to a
# string type, which we can then properly print.
data = serial_port.read(bytes_to_read).decode()
print(data)

# This is an alternate way to read data. However it presents a problem in that it will block even after there is no more
# IO. I solved it using the loop above.
# for line in serial_port:
# print(line)

serial_port.close()