import datetime
import json
import os
import crypto.sign
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

user_data = []
tse_data = []


class FlashMemory:
    current_voter = None
    def register_presence(self, userid):
        self.current_voter = userid
        timestamp = datetime.datetime.now().isoformat() 
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
        vote, user_pin, tse_pin = crypto.sign.generate_vote_obj(self.current_voter, position, candidate)
        block["votes"].append({"position": vote["position"],
                               "candidate": vote["candidate"],
                               "hash": vote["hash"]})
        
        user_data.append({"user_id": self.current_voter, "position": position, "pin": user_pin})
        tse_data.append({"user_id": self.current_voter, "position": position, "pin": tse_pin})

    def sign_ballot(self):
        block["presences"].sort(key=lambda x: x["timestamp"])
        block["votes"].sort(key=lambda x: x["hash"])
        data_to_sign = json.dumps(block).replace(" ", "")
        block["signature"] = crypto.sign.sign_data(f"./crypto/keys/ballot", data_to_sign.encode()).hex()
        
        file_path = 'finalized_section.json'
        with open(file_path, 'w') as file:
            json.dump(block, file, indent=4)
        file_path = 'finalized_section.tse'
        with open(file_path, 'w') as file:
            json.dump(tse_data, file, indent=4)
        file_path = 'finalized_section.user'
        with open(file_path, 'w') as file:
            json.dump(user_data, file, indent=4)

FM = FlashMemory()
