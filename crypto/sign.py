from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import rsa, padding
import datetime
import json
import hashlib
import os

VOTE_DATA = {
    "presences": [],
    "votes": [],
}

def sign_data(private_key_path: str, data: str) -> str:
    with open(private_key_path, "rb") as key_file:
        private_key = serialization.load_pem_private_key(
            key_file.read(),
            password=None
        )

    signature = private_key.sign(
        data,
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    )
    return signature

    
def register_vote(user_id: str, vereador_number: str, prefeito_number: str):
    presence_data = {
        "user_id": user_id,
        "timestamp": datetime.datetime.now().isoformat()  
    }
    data_to_sign = (presence_data['user_id'] + presence_data['timestamp']).encode()
    presence_data["signature"] = sign_data(f"./crypto/keys/{user_id}", data_to_sign).hex()

    vote_vereador, v_user_pin, v_tse_pin = generate_vote_obj(user_id, "vereador", vereador_number)
    vote_prefeito, p_user_pin, p_user_pin = generate_vote_obj(user_id, "prefeito", prefeito_number)

    VOTE_DATA["presences"].append(presence_data)
    VOTE_DATA["votes"].append(vote_vereador)
    VOTE_DATA["votes"].append(vote_prefeito)

    return {
        "presence_data": presence_data,
        "vote_vereador": vote_vereador,
        "vote_prefeito": vote_prefeito,
        "user_pin_vereador": v_user_pin,
        "tse_pin_vereador": v_tse_pin,
        "user_pin_prefeito": p_user_pin,
        "tse_pin_prefeito": p_user_pin,
    }

def generate_hash(data: str):
    hash_object = hashlib.sha256(data.encode())
    random_hash = hash_object.hexdigest()
    return random_hash

def generate_vote_obj(user_id: str, position: str, candidate_number: str):
    vote = {
      "position": position,
      "candidate": candidate_number,
    }

    user_pin = generate_random_hash()
    tse_pin = generate_random_hash()

    vote["hash"] = generate_hash(user_id + user_pin + tse_pin)

    return vote, user_pin, tse_pin

def generate_random_hash():
    random_data = os.urandom(32)  
    hash_object = hashlib.sha256(random_data)
    random_hash = hash_object.hexdigest()
    return random_hash[:20]

def end_voting(): 
    VOTE_DATA["presences"].sort(key=lambda x: x["timestamp"])
    VOTE_DATA["votes"].sort(key=lambda x: x["hash"])
    data_to_sign = json.dumps(VOTE_DATA).replace(" ", "")
    print(data_to_sign)
    VOTE_DATA["signature"] = sign_data(f"./crypto/keys/ballot", data_to_sign.encode()).hex()
    with open("signed_presence.json", "w") as json_file:
        json.dump(VOTE_DATA, json_file, indent=4)

def simulate_voting():
    register_vote("fd7de658119bf6541d49", "12345", "12")
    register_vote("f6b518b2ecd9f47761ed", "54321", "21")
    end_voting()
    
simulate_voting()