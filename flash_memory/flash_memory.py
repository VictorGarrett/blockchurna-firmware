import datetime
import json
import os
import crypto.sign
block = {
    "presences": [
       
    ],
    "votes": [
       
    ],
    "signature": ""
}

userid_tmp = ""

class FlashMemory:
    def register_presence(userid):
        userid_tmp = userid
        timestamp = datetime.datetime.now().isoformat() 
        presence_data = {
            "user_id": userid,
            "timestamp": timestamp
        }
        data_to_sign = json.dumps(presence_data).encode()
        signature = crypto.sign.sign_data(f"./crypto/keys/{userid}", data_to_sign).hex()
        block["presences"].append({"user_id": userid, 
                                   "timestamp": timestamp,
                                    "signature": signature})
        

    def register_vote(position, candidate):
        vote, _, _ = crypto.sign.generate_vote_obj(userid_tmp, position, candidate)
        block["votes"].append({"position": vote["position"],
                               "candidate": vote["candidate"],
                               "hash": vote["hash"]})

    def sign_ballot():
        data_to_sign = json.dumps(block).encode()
        block["signature"] = crypto.sign.sign_data(f"./crypto/keys/ballot", data_to_sign).hex()
        
        file_path = 'finalized_section.json'
        with open(file_path, 'w') as file:
            json.dump(block, file, indent=4)