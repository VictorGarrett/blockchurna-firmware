from adafruit_fingerprint import Adafruit_Fingerprint
import adafruit_fingerprint

class FingerprintSensor:

    def __init__(self):
        pass
        # Create a serial connection
        # uart = serial.Serial('/dev/serial0', 57600, timeout=0.5)  # Adjust based on your connection

        # time.sleep(1)
        # # Create an instance of the fingerprint sensor
        
        # success = False
        # while success == False:
        #     try:
        #         self.finger = Adafruit_Fingerprint(uart)
        #         success = True
        #     except:
        #         success = False

    def get_user_from_fingerprint(self):
        # print("Tryong to get image from sensor")

        try:
            if self.finger.get_image() != adafruit_fingerprint.OK:
                return None
        except:
            return None
        # print("Finger detected. Converting to template...")
        try:
            self.finger.image_2_tz()  # Convert image to template
        except:
            return None
        # print("Searching for a matching fingerprint...")
        result = self.finger.finger_fast_search()  # Search for the fingerprint

        if result == adafruit_fingerprint.OK:
            # print(f"Fingerprint matched! ({self.finger.finger_id})")
            return self.finger.finger_id
        elif result == adafruit_fingerprint.NOFINGER:
            # print("No finger detected.")
            return None
        elif result == adafruit_fingerprint.NOTFOUND:
            # print("No match found.")
            return -1
        else:
            print(f"Error: {result}")

