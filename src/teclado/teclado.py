# --------Modo Practicar--------------
import RPi.GPIO as GPIO
from time import sleep

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)


Filas = [19,26, 13, 6]
for row in Filas:
    GPIO.setup(row, GPIO.OUT)

#Columnas = [21, 20, 16, 12, 1, 22, 27,17]
Columnas = [17, 27, 22,1 ,12, 16,20,23]
for j in range(8):
    GPIO.setup(Columnas[j], GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
#GPIO.setup(40, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

#def teclado():
    ##no esta programada

##Inicia la funcion lectura
def lectura(FILAS, CARACTERES):
    GPIO.output(FILAS, GPIO.HIGH)  
    #for pin in Columnas:
        #if bool(GPIO.input(pin)):
            #print()
    if bool(GPIO.input(Columnas[0])):
        print(CARACTERES[0])
    elif bool(GPIO.input(Columnas[1])):
        print(CARACTERES[1])
    elif bool(GPIO.input(Columnas[2])):
        print(CARACTERES[2])
    elif bool(GPIO.input(Columnas[3])):
        print(CARACTERES[3])
    elif bool(GPIO.input(Columnas[4])):
        print(CARACTERES[4])
    elif bool(GPIO.input(Columnas[5])):
        print(CARACTERES[5])
    elif bool(GPIO.input(Columnas[6])):
        print(CARACTERES[6])
    elif bool(GPIO.input(Columnas[7])):
        print(CARACTERES[7])
    GPIO.output(FILAS,GPIO.LOW)

##termina la funcion lectura

try:
    while True:
        lectura(Filas[0], ["A", "B", "C", "D", "E", "F", "G", "up"])
        lectura(Filas[1], ["H", "I", "J", "K", "L", "M", "N", "down"])
        lectura(Filas[2], ["O", "P", "Q", "R", "S", "T", "Ñ", "enter"])
        lectura(Filas[3], ["left","U", "V", "W", "X", "Y", "Z", "right"])
        sleep(0.23)  # SENSIBILIDAD

except KeyboardInterrupt:
    print("Programa finalizado...")
