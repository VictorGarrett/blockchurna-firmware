from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from crypto.sign import generate_random_hash

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
        file.write(pem_public_key.decode())

for i in range(5):
    generate_key(generate_random_hash())
    

