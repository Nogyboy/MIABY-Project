import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522

reader = SimpleMFRC522()

try:
        text = input('Nuevos datos:')
        print("Ahora coloca la tarjeta:")
        reader.write(text)
        print(f"Se ha almacenado {text} en la tarjeta.")
finally:
        GPIO.cleanup()