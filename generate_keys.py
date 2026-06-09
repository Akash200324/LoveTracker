import base64
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import serialization

# Generate a new ECDSA private key for the P-256 curve
private_key = ec.generate_private_key(ec.SECP256R1())
public_key = private_key.public_key()

# Serialize the private key to a raw integer representation
private_value = private_key.private_numbers().private_value
private_bytes = private_value.to_bytes(32, 'big')

# Serialize the public key to its uncompressed point representation (0x04 prefix)
public_bytes = public_key.public_bytes(
    encoding=serialization.Encoding.X962,
    format=serialization.PublicFormat.UncompressedPoint
)

# Base64 url-safe encode both keys without padding
def b64urlsafe(data):
    return base64.urlsafe_b64encode(data).decode('utf-8').rstrip('=')

vapid_private_key = b64urlsafe(private_bytes)
vapid_public_key = b64urlsafe(public_bytes)

with open('core/settings.py', 'a') as f:
    f.write('\n# VAPID KEYS FOR WEB PUSH NOTIFICATIONS\n')
    f.write(f'VAPID_PUBLIC_KEY = "{vapid_public_key}"\n')
    f.write(f'VAPID_PRIVATE_KEY = "{vapid_private_key}"\n')
    f.write('VAPID_ADMIN_EMAIL = "mailto:admin@lovetracker.com"\n')

print("Keys generated successfully.")
