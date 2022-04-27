import numpy as np
from matplotlib import pyplot as plt

MAXVOLTAGE = 3.3

with open ("settings.txt", "r") as settings:
    TMP = [float(i) for i in settings.read().split("\n")]

volt = np.loadtxt("data.txt", dtype = int)
volt = volt/256 * MAXVOLTAGE
fig, ax = plt.subplots(figsize=(16, 10), dpi=300)

with open ("settings.txt", "r") as settings:
    T= float(settings.readline())

TMP = np.arange(0, len(volt)*T, T)

xmax = np.argmax(TMP)*T
qmax = volt.argmax()
str1 = "Время заряда =" + str(qmax*T) + "c"
str2 = "Время разряда =" + (str((len(volt)-qmax)*T)) + "c"

ax.set_title("Процесс заряда и разяда конденсатора в RC-цепочке", fontsize = 17, wrap=True) # заголовок
ax.set_xlabel("Время, с", fontsize = 15) # ось абсцисс
ax.set_ylabel("Напяржение, В", fontsize = 15) # ось ординат
ax.plot(TMP,volt, color = 'b', label="V(t)", marker = 'o', markevery = 100)
ax.minorticks_on()
ax.grid(which='major', color = 'k', linewidth = 0.5)
ax.grid(which='minor', color = 'k', linestyle = ':')
ax.legend()
ax.set(xlim=(0, xmax), ylim=(0, MAXVOLTAGE))
plt.text(0.3*len(TMP)*T,2, str1)
plt.text(0.3*len(TMP)*T,1.5, str2)

fig.savefig("test.png")
