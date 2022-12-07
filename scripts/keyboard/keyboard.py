# --------Modo Practicar--------------
import RPi.GPIO as GPIO
from time import sleep

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)


rows = [19,26, 13, 6]
for row in rows:
    GPIO.setup(row, GPIO.OUT)

columns = [17, 27, 22,1 ,12, 16,20,23]
for j in range(8):
    GPIO.setup(columns[j], GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
#GPIO.setup(40, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)


## Start reading
def read(rows, characters):
    GPIO.output(rows, GPIO.HIGH)  

    if bool(GPIO.input(columns[0])):
        print(characters[0])
    elif bool(GPIO.input(columns[1])):
        print(characters[1])
    elif bool(GPIO.input(columns[2])):
        print(characters[2])
    elif bool(GPIO.input(columns[3])):
        print(characters[3])
    elif bool(GPIO.input(columns[4])):
        print(characters[4])
    elif bool(GPIO.input(columns[5])):
        print(characters[5])
    elif bool(GPIO.input(columns[6])):
        print(characters[6])
    elif bool(GPIO.input(columns[7])):
        print(characters[7])
    GPIO.output(rows,GPIO.LOW)

try:
    while True:
        read(rows[0], ["A", "B", "C", "D", "E", "F", "G", "up"])
        read(rows[1], ["H", "I", "J", "K", "L", "M", "N", "down"])
        read(rows[2], ["O", "P", "Q", "R", "S", "T", "Ñ", "enter"])
        read(rows[3], ["left","U", "V", "W", "X", "Y", "Z", "right"])
        sleep(0.23)  # Delay

except KeyboardInterrupt:
    print("Exit...")
