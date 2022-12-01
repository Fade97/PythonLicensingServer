from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from pathlib import Path
import json
import codecs
import uuid

privKey = rsa.generate_private_key(65537, 2048, default_backend)
if not Path('privkey.pem').is_file():
    with open('privkey.pem', 'wb') as f:
        f.write(privKey.private_bytes(serialization.Encoding.PEM, serialization.PrivateFormat.PKCS8, serialization.NoEncryption()))
if not Path('pubkey.pem').is_file():
    with open('pubkey.pem', 'wb') as f:
        f.write(privKey.public_key().public_bytes(serialization.Encoding.PEM, serialization.PublicFormat.SubjectPublicKeyInfo))
del privKey

private_key = None
with open("privkey.pem", "rb") as key_file:
    private_key = serialization.load_pem_private_key(
        key_file.read(),
        password=None,
        backend=default_backend()
    )

public_key = None
with open("pubkey.pem", "rb") as key_file:
    public_key = serialization.load_pem_public_key(
        key_file.read(),
        backend=default_backend()
    )

licenses = []

def generateLicense(data: dict):
    encrypted = public_key.encrypt(
            json.dumps(data, ensure_ascii=False).encode('utf-8'),
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        ).hex()
    licenses.append(encrypted)

def checkLicense(license: str) -> dict:
    original_message = private_key.decrypt(
        codecs.decode(license, "hex_codec"),
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    ).decode("utf-8")
    print(original_message)
    return json.loads(original_message)

if __name__ == "__main__":
    generateLicense({"id":51, "name":"John Doe"})
    print([l for l in licenses])
    checkLicense(licenses[0])