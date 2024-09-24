import hashlib

# Hashing the password without a salt
def hash_password(password):
    # Create a hash using SHA-256
    hash_obj = hashlib.sha256(password.encode())
    hashed_password = hash_obj.hexdigest()
    return hashed_password

# Example usage:
password = "my_secure_password"
hashed = hash_password(password)
print(f"Hashed password: {hashed}")
