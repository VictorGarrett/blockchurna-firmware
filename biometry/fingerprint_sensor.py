import time
import serial
from adafruit_fingerprint import Adafruit_Fingerprint


import json

def load_number_key_mapping(json_file):

    with open(json_file, 'r', encoding='utf-8') as file:
        data = json.load(file)
    
    keys = data.get("keys", [])
    
    return {i: keys[i] for i in len(keys)}


class FingerprintSensor:

    def __init__(self):
        
        # Create a serial connection
        uart = serial.Serial('/dev/serial0', 57600)  # Adjust based on your connection

        # Create an instance of the fingerprint sensor
        self.finger = Adafruit_Fingerprint(uart)

    def get_user_from_fingerprint(self):
        print("Place your finger on the sensor...")

        while self.finger.get_image() != Adafruit_Fingerprint.OK:
            pass

        print("Finger detected. Converting to template...")
        self.finger.image2Tz()  # Convert image to template

        print("Searching for a matching fingerprint...")
        result = self.finger.finger_fast_search()  # Search for the fingerprint

        if result == Adafruit_Fingerprint.OK:
            print("Fingerprint matched!")
            return self.finger.finger_id
        elif result == Adafruit_Fingerprint.NOFINGER:
            print("No finger detected.")
            return None
        elif result == Adafruit_Fingerprint.NOTFOUND:
            print("No match found.")
            return -1
        else:
            print(f"Error: {result}")

