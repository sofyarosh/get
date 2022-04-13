import matplotlib.pyplot as plt
import RPi.GPIO as GPIO
import time


spisok = []
leds = [21, 20, 16, 12, 7, 8, 25, 24]
dac = [26, 19, 13, 6, 5, 11, 9, 10]
bits = 8
TroykaMoudle = 17
comparator = 4
levels = 2**bits
maxVOLTAGE = 3.3

GPIO.setmode(GPIO.BCM)
GPIO.setup(leds, GPIO.OUT, initial = GPIO.LOW)
GPIO.setup(TroykaMoudle, GPIO.OUT, initial = GPIO.HIGH)
GPIO.setup(dac,GPIO.OUT)
GPIO.setup(comparator, GPIO.IN)

def decimal2binary(i):
    return [int(elem) for elem in bin(i)[2:].zfill(bits)]
def bin2dac(i):
     signal = decimal2binary(i)
     GPIO.output(dac, signal)
     return signal
def adc():
    value = 0
    for i in range(7, -1, -1):
        bin2dac(value + 2 ** i)
        time.sleep(0.0008)
        comparatorValue = GPIO.input(comparator)
        if comparatorValue == 1:
            value += 2 ** i
    return value

try:
    check = True
    GPIO.output(17,1) #Подаем питание на тройку-модуль
    start = time.time() #Засекаем начало эксперимента
    print('Началась зарядка конденсатора.')
    while True:
        value = adc() #Считываем аналоговый сигнал с конденсатора
        GPIO.output(leds, decimal2binary(value)) #Отображаем значение value на панели leds
        if value >= 240 and check: #Если зарядились, то отключаем питание
            GPIO.output(17, 0)
            print('Началась разрядка конденастора')
            check = False
        if not check and value <= 5: #Если зарядились, то заканчиваем эксперимент
            end = time.time() #Засекаем конец эксперимента
            T = (end - start)/(len(spisok)-1) #Считаем период
            nu = 1/T #Считаем частоту
            dv = maxVOLTAGE / levels
            spisok.append(value)
            break
        spisok.append(value) #Добавляем значение в список всех аналоговых значений
        voltage = maxVOLTAGE / levels * value
        print("digital value = {:^3}, anallog VOLTAGE = {:.2f}". format(value, voltage))
    plt.plot(spisok)
    with open('data.txt', 'w') as outputfile1: # Создаем файл data.txt
        for i in range(len(spisok)):
            outputfile1.write(str(spisok[i])+ '\n')
    with open('settings.txt', 'w') as outputfile2: # Создаем файл settings.txt
            outputfile2.write('T = '+ str(T) + '\n')
            outputfile2.write('dV = ' + str(dv)+ '\n')
            outputfile2.write('vremya = ' + str(end - start)+ '\n') 
            outputfile2.write('nu = '+ str(nu) + '\n')
    plt.show() # Показ графика
    
finally:
    GPIO.output(leds, GPIO.LOW)
    GPIO.cleanup(leds)
    GPIO.output(dac, GPIO.LOW)
    GPIO.cleanup(dac)
    print("GPIO cleanup completed")
