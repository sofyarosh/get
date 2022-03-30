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
def adc(i, value):
    if i == -1:
        return value
    bin2dac(value +2**i)
    time.sleep(0.0005)
    comparatorValue = GPIO.input(comparator)
    if comparatorValue == 0:
        return adc(i-1, value)
    else:
        return adc(i-1, value+2**i)
try:
    while True:
       value = adc(bits-1, 0)
       voltage = maxVoltage / levels * value
       print("digital value =  {:^3}, analog VOLTAGE = {:.2f}".format(value, voltage))
except KeyboardInterrupt:
    print("programma ostanovlena klavoy")
else:
    print("Nikakix isklucheniy")
finally:
    GPIO.output(dac, GPIO.LOW)
    GPIO.cleanup(dac)
    print("GPIO cleanup completed")
