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
        uart = serial.Serial('/dev/ttyAMA0', 57600)  # Adjust based on your connection

        # Create an instance of the fingerprint sensor
        self.finger = Adafruit_Fingerprint(uart)

    def get_user_from_fingerprint(self):
        pass