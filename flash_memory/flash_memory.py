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
        if userid in self.already_voted:
            return

        self.already_voted.append(userid)
        timestamp = str(int(datetime.datetime.now().timestamp()))
        presence_data = {
            "user_id": userid,
            "timestamp": timestamp
        }
        data_to_sign = (presence_data['user_id'] + presence_data['timestamp']).encode()
        signature = crypto.sign.sign_data(f"./crypto/keys/{userid}", data_to_sign).hex()
        block["presences"].append({
            "user_id": userid,
            "timestamp": timestamp,
            "signature": signature
        })

    def register_vote(self, position, candidate):
        vote, user_pin, tse_pin = crypto.sign.generate_vote_obj(self.current_voter["key_id"], position, candidate)
        block["votes"].append({
            "position": vote["position"],
            "candidate": vote["candidate"],
            "hash": vote["hash"]
        })

        self.user_data.append({
            "user_id": self.current_voter["key_id"],
            "position": position,
            "pin": user_pin
        })
        self.tse_data.append({
            "user_id": self.current_voter["key_id"],
            "position": position,
            "pin": tse_pin
        })
        self.sign_ballot()

    def sign_ballot(self):
        block["presences"].sort(key=lambda x: x["timestamp"])
        block["votes"].sort(key=lambda x: x["hash"])
        
        if "signature" in block:
            del block["signature"]

        data_to_sign = json.dumps(block, separators=(',', ':'))  # Minify JSON for exact signature match
        block["signature"] = crypto.sign.sign_data(f"./crypto/keys/ballot", data_to_sign.encode()).hex()

        self.save_to_usb('finalized_section.section', block)
        self.save_to_usb('finalized_section.tse', self.tse_data)
        self.save_to_usb('finalized_section.user', self.user_data)

    def save_to_usb(self, filename, data):
        if not os.path.exists(usb_drive_path):
            print(f"USB drive not found at {usb_drive_path}")
            return

        file_path = os.path.join(usb_drive_path, filename)
        try:
            with open(file_path, 'w') as file:
                json.dump(data, file, indent=4)
                file.flush()
                os.fsync(file.fileno())  # Ensure data is written to disk
            print(f"File {filename} saved successfully.")
        except Exception as e:
            print(f"Error saving {filename}: {e}")

FM = FlashMemory()
