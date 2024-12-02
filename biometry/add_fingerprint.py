import time
import board
import serial
from adafruit_fingerprint import Adafruit_Fingerprint
import adafruit_fingerprint
import states.config as config




def enroll_fingerprint_with_sensor(id_slot, finger_sensor):

    id_slot = int(id_slot)
    finger = finger_sensor.finger

    print("Place your finger on the sensor...")
    
    # Wait for a finger to be placed on the sensor
    try:
        while finger.get_image() != adafruit_fingerprint.OK:
            pass
    except:
        return -1
    print("Finger detected. Converting to template...")
    finger.image_2_tz(1)  # Convert image to template

    config.pirilim_candidate.play()
    print("Remove your finger.")
    time.sleep(2)

    print("Place the same finger again...")
    
    try:
        while finger.get_image() != adafruit_fingerprint.OK:
            pass
    except:
        return -1
    print("Finger detected. Converting to template...")
    finger.image_2_tz(2)  # Convert second image to template

    print("Creating model...")
    if finger.create_model() == adafruit_fingerprint.OK:
        print(f"Storing model in slot {id_slot}...")
        if finger.store_model(id_slot) == adafruit_fingerprint.OK:
            print(f"Fingerprint successfully enrolled in slot {id_slot}!")
        else:
            print("Failed to store fingerprint.")
            return -1
    else:
        print("Failed to create model.")
        return -1
    return 0


def enroll_fingerprint(id_slot):

        # Create a serial connection
    print('initing uart')
    uart = serial.Serial('/dev/serial0', 57600)  # Adjust based on your connection
    # Create an instance of the fingerprint sensor
    finger = Adafruit_Fingerprint(uart)

    print('initing sensor')

    print("Place your finger on the sensor...")
    
    # Wait for a finger to be placed on the sensor
    while finger.get_image() != adafruit_fingerprint.OK:
        pass

    print("Finger detected. Converting to template...")
    finger.image_2_tz(1)  # Convert image to template

    print("Remove your finger.")
    time.sleep(2)

    print("Place the same finger again...")
    
    while finger.get_image() != adafruit_fingerprint.OK:
        pass

    print("Finger detected. Converting to template...")
    finger.image_2_tz(2)  # Convert second image to template

    print("Creating model...")
    if finger.create_model() == adafruit_fingerprint.OK:
        print(f"Storing model in slot {id_slot}...")
        if finger.store_model(id_slot) == adafruit_fingerprint.OK:
            print(f"Fingerprint successfully enrolled in slot {id_slot}!")
        else:
            print("Failed to store fingerprint.")
            uart.close()
            return -1
    else:
        print("Failed to create model.")
        uart.close()
        return -1
    uart.close()
    return 0


if __name__ == '__main__':
    # Enroll a fingerprint to slot 1

    print('type id')

    enroll_fingerprint(int(input()))