from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
import base64
import hashlib
import os
import json 
def generate_random_hash():
    random_data = os.urandom(32)  
    hash_object = hashlib.sha256(random_data)
    random_hash = hash_object.hexdigest()
    return random_hash[:20]


def generate_key(name: str):
    path = "./crypto/keys/" + name
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048
    )
    
    public_key = private_key.public_key()

    with open(path, "wb") as private_file:
        private_file.write(private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        ))

    # Save public key as Base64-encoded text
    public_key_pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    public_key_base64 = base64.b64encode(public_key_pem).decode()

    with open(path + ".pub", "w") as public_file:
        public_file.write(public_key_base64)

    return {"key_id": name, "public_key_base64": public_key_base64}
        
keys = []
for i in range(20):
    keys.append(generate_key(generate_random_hash()))
keys.append(generate_key('ballot'))


with open(f"./keys.json","w") as file:
    file.write(json.dumps(keys))
