from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding

# Завантаження публічного ключа
with open("keys/public.pem", "rb") as pub_file:
    public_key = serialization.load_pem_public_key(pub_file.read())

# Завантаження приватного ключа
with open("keys/private.pem", "rb") as priv_file:
    private_key = serialization.load_pem_private_key(priv_file.read(), password=None)

# Твоє повідомлення
message = b"Привіт, RSA!"

# Шифрування
encrypted = public_key.encrypt(
    message,
    padding.OAEP(
        mgf=padding.MGF1(algorithm=hashes.SHA256()),
        algorithm=hashes.SHA256(),
        label=None
    )
)

print("Зашифроване повідомлення:", encrypted)

# Розшифрування
decrypted = private_key.decrypt(
    encrypted,
    padding.OAEP(
        mgf=padding.MGF1(algorithm=hashes.SHA256()),
        algorithm=hashes.SHA256(),
        label=None
    )
)

print("Розшифроване повідомлення:", decrypted.decode())
