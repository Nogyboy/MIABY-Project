import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522

reader = SimpleMFRC522()

try:
        text = input('New data:')
        print("Now put the card on reader:")
        reader.write(text)
        print(f"It has saved {text} on the card.")
finally:
        GPIO.cleanup()