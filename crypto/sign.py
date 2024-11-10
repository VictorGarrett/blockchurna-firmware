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

def sign_data(key_path: str, data: str):
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048
    )

    with open(key_path, "wb") as pem_out:
        pem_out.write(private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()  
        ))
    
    return private_key.sign(
        data,
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    )

    
def register_vote(user_id: str, vereador_number: str, prefeito_number: str):
    presence_data = {
        "user_id": user_id,
        "timestamp": datetime.datetime.now().isoformat()  
    }
    data_to_sign = json.dumps(presence_data).encode()

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
    data_to_sign = json.dumps(VOTE_DATA).encode()
    VOTE_DATA["presences"].sort(key=lambda x: x["timestamp"])
    VOTE_DATA["votes"].sort(key=lambda x: x["hash"])

    VOTE_DATA["signature"] = sign_data(f"./crypto/keys/ballot", data_to_sign).hex()
    with open("signed_presence.json", "w") as json_file:
        json.dump(VOTE_DATA, json_file, indent=4)

def simulate_voting():
    register_vote("9a282e0d496f47a", "12345", "12")
    register_vote("19f3cd308f1455b", "54321", "21")
    end_voting()
    
simulate_voting()