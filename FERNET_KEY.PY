from cryptography.fernet import Fernet

# Generate a key
key = Fernet.generate_key()
print(key.decode())  # You can print and save this key for future use
