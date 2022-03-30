import RPi.GPIO as GPIO
import time
dac = [26, 19, 13, 6, 5, 11, 9, 10]
bits = len(dac)
levels = 2**bits
maxVoltage = 3.3
TroykaMoudle = 17
comparator = 4


GPIO.setmode(GPIO.BCM)
GPIO.setup(dac, GPIO.OUT, initial = GPIO.LOW)
GPIO.setup(TroykaMoudle, GPIO.OUT, initial = GPIO.HIGH)
GPIO.setup(comparator, GPIO.IN)

def decimal2binary(i):
    return [int(elem) for elem in bin(i)[2:].zfill(bits)]

def bin2dac(i):
     signal = decimal2binary(i)
     GPIO.output(dac, signal)
     return signal

def adc():
     signal = bin2dac(i)
     time.sleep(0.0005)
     voltage = i / levels * maxVoltage
     comparatorValue = GPIO.input(comparator)
     if comparatorValue == 0:
         return i

try:
    while True:
       const = adc()
       print("ADC value =  {:^3} -> {}, input VOLTAGE = {:.2f}".format(const,bin2dac(const), const / levels * maxVoltage))

except KeyboardInterrupt:
    print("programma ostanovlena klavoy")
else:
    print("Nikakix isklucheniy")
finally:
    GPIO.output(dac, GPIO.LOW)
    GPIO.cleanup(dac)
    print("GPIO cleanup completed")
