import time
import smbus as smbus
import RPi.GPIO as GPIO

ADC=smbus.SMBus(1)

flame_ain_raw = 0x14
flame_ain_v = 0x24
flame_ain_p	= 0x34


if __name__ == '__main__':
	while True:
		print("---------------")
		print(ADC.read_word_data(0x24, flame_ain_raw))
		print(ADC.read_word_data(0x24, flame_ain_v))
		print(ADC.read_word_data(0x24, flame_ain_p))
		time.sleep(1)