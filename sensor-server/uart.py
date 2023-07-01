import pigpio
import serial
import time

ser = serial.Serial(
	port='/dev/serial0',
	baudrate=9600,
	timeout=1
)

registered_tags = {'1234567890AB','A1B2C3D4E5F6'}

while True:
	if ser.in_waiting:
		rfid = ser.readline().decode().strip()

		if rfid in registered_tags:
			ser.write(b'found\n')
		else:
			ser.write('notfound\n')
