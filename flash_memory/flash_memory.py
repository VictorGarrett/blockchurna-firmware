import datetime
import json
import os
import crypto.sign
import shutil

block = {
    "presences": [
       
    ],
    "votes": [
       
    ],
    "city": "Curitiba",
    "state": "PR",
    "section": "077",
    "zone": "UTFPR"
}


# usb_drive_path = '/media/pi/blockchurna_drive'
usb_drive_path = os.path.join('/media', 'pi', 'blockchurna_drive')

class FlashMemory:
    def __init__(self):
        self.current_voter = None
        self.already_voted = []
        self.user_data = []
        self.tse_data = []

    def set_current_voter(self, voter_info):
        self.current_voter = voter_info

    def register_presence(self):
        userid = self.current_voter["key_id"]
        self.already_voted.append(userid)
        timestamp = str(datetime.datetime.now().timestamp()).split(".")[0]
        presence_data = {
            "user_id": userid,
            "timestamp": timestamp
        }
        data_to_sign = (presence_data['user_id'] + presence_data['timestamp']).encode()
        signature = crypto.sign.sign_data(f"./crypto/keys/{userid}", data_to_sign).hex()
        block["presences"].append({"user_id": userid, 
                                   "timestamp": timestamp,
                                    "signature": signature})
        

    def register_vote(self, position, candidate):
        vote, user_pin, tse_pin = crypto.sign.generate_vote_obj(self.current_voter["key_id"], position, candidate)
        block["votes"].append({"position": vote["position"],
                               "candidate": vote["candidate"],
                               "hash": vote["hash"]})
        
        self.user_data.append({"user_id": self.current_voter["key_id"], "position": position, "pin": user_pin})
        self.tse_data.append({"user_id": self.current_voter["key_id"], "position": position, "pin": tse_pin})
        self.sign_ballot()

    def sign_ballot(self):
        block["presences"].sort(key=lambda x: x["timestamp"])
        block["votes"].sort(key=lambda x: x["hash"])
        data_to_sign = json.dumps(block).replace(" ", "")
        block["signature"] = crypto.sign.sign_data(f"./crypto/keys/ballot", data_to_sign.encode()).hex()
        
        file_path = os.path.join(usb_drive_path, 'finalized_section.section')
        with open(file_path, 'w+') as file:
            json.dump(block, file, indent=4)
            # self.send_data_to_flash(file_path)

        file_path = os.path.join(usb_drive_path, 'finalized_section.tse')
        with open(file_path, 'w+') as file:
            json.dump(self.tse_data, file, indent=4)
            # self.send_data_to_flash(file_path)

        file_path = os.path.join(usb_drive_path, 'finalized_section.user')
        with open(file_path, 'w+') as file:
            json.dump(self.user_data, file, indent=4)
            # self.send_data_to_flash(file_path)

    def send_data_to_flash(self, source_file):
        if os.path.exists(usb_drive_path):
            try:
                destination_file = os.path.join(usb_drive_path, source_file)
                shutil.copy(source_file, destination_file)
                print(f"File successfully copied to {usb_drive_path}")
            except Exception as e:
                print(f"Error occurred: {e}")
        else:
            print(f"USB drive not found at {usb_drive_path}")


FM = FlashMemory()
