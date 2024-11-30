import time
import board
import serial
from adafruit_fingerprint import Adafruit_Fingerprint

# Create a serial connection
uart = serial.Serial('/dev/serial0', 57600)  # Adjust based on your connection

# Create an instance of the fingerprint sensor
finger = Adafruit_Fingerprint(uart)

def enroll_fingerprint(id_slot):
    print("Place your finger on the sensor...")
    
    # Wait for a finger to be placed on the sensor
    while finger.get_image() != Adafruit_Fingerprint.OK:
        pass

    print("Finger detected. Converting to template...")
    finger.image2Tz(1)  # Convert image to template

    print("Remove your finger.")
    time.sleep(2)

    print("Place the same finger again...")
    
    while finger.get_image() != Adafruit_Fingerprint.OK:
        pass

    print("Finger detected. Converting to template...")
    finger.image2Tz(2)  # Convert second image to template

    print("Creating model...")
    if finger.create_model() == Adafruit_Fingerprint.OK:
        print(f"Storing model in slot {id_slot}...")
        if finger.store_model(id_slot) == Adafruit_Fingerprint.OK:
            print(f"Fingerprint successfully enrolled in slot {id_slot}!")
        else:
            print("Failed to store fingerprint.")
    else:
        print("Failed to create model.")

# Enroll a fingerprint to slot 1

print('type id')

enroll_fingerprint(input())