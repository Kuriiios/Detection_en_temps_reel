from sqlalchemy import String, TypeDecorator
from cryptography.fernet import Fernet
from dotenv import load_dotenv
import bcrypt
import os

load_dotenv()

ENCRYPTION_KEY = os.getenv("ENCRYPTION_KEY")
if not ENCRYPTION_KEY:
    raise ValueError("No ENCRYPTION_KEY found in environment variables!")
CIPHER = Fernet(ENCRYPTION_KEY)

class EncryptedString(TypeDecorator):
    impl = String

    def process_bind_param(self, value, dialect):
        if value is not None:
            return CIPHER.encrypt(value.encode()).decode()
        return value

    def process_result_value(self, value, dialect):
        if value is not None:
            return CIPHER.decrypt(value.encode()).decode()
        return value
    
class BcryptPassword(TypeDecorator):
    impl = String
    cache_ok = True

    def process_bind_param(self, value, dialect):
        if value is not None:
            if value.startswith('$2b$'):
                return value
            
            salt = bcrypt.gensalt()
            hashed = bcrypt.hashpw(value.encode('utf-8'), salt)
            return hashed.decode('utf-8')
        return value

    def process_result_value(self, value, dialect):
        return value