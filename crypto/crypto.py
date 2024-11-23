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
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048
    )

    public_key = private_key.public_key()

    pem_private_key = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()  
    )

    pem_public_key = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )

    with open(f"./crypto/keys/{name}","w") as file:
        file.write(pem_private_key.decode())

    with open(f"./crypto/keys/{name}.pub","w") as file:
        pub_key = base64.b64encode(pem_public_key).decode()
        file.write(pub_key)

    return {"key_id": name, "public_key_base64": pub_key}
        
keys = []
for i in range(20):
    keys.append(generate_key(generate_random_hash()))
keys.append(generate_key('ballot'))


with open(f"./keys.json","w") as file:
    file.write(json.dumps(keys))
