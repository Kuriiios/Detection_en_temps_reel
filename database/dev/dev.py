from sqlalchemy import create_engine, Column, Integer, String
from database.data.models import EncryptedString, BcryptPassword
from sqlalchemy.orm import sessionmaker, declarative_base
from cryptography.fernet import Fernet
import hashlib
import hmac
import bcrypt
from sqlalchemy.sql import text

# --- 1. CONFIGURATION ---
# In production, move these to your .env file
KEY = Fernet.generate_key() 
CIPHER = Fernet(KEY)

Base = declarative_base()


# --- 3. THE MODEL ---
class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    
    # These use the automatic encryption type
    id = Column(Integer, primary_key=True)
    firstname = Column(EncryptedString(500), nullable=False)
    lastname = Column(EncryptedString(500), nullable=False)
    username = Column(EncryptedString(500), nullable=False)
    email = Column(EncryptedString(500), nullable=False, unique=True)
    email_index = Column(String(64), unique=True, index=True)
    password = Column(BcryptPassword(128), nullable=False)

    @staticmethod
    def generate_index(email: str) -> str:
        """The one and only way we calculate the search index."""
        key = b'static-salt-for-hashing' # In production, pull this from an Env Var
        return hmac.new(key, email.lower().strip().encode(), hashlib.sha256).hexdigest()

    def __init__(self, **kwargs):
        if 'email' in kwargs:
            kwargs['email_index'] = self.generate_index(kwargs['email'])
        super().__init__(**kwargs)

    def set_password(self, password: str):
        """Hashes the password and stores it."""
        salt = bcrypt.gensalt()
        # Hashpw returns a byte string; we decode to utf-8 to store in DB
        hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
        self.password = hashed.decode('utf-8')
    

    def check_password(self, password: str) -> bool:
        """Verifies the password against the stored hash."""
        password_bytes = password.encode('utf-8')
    
        # 2. Ensure the stored hash is bytes
        # If your DB returns a string, encode it to bytes
        hash_from_db = self.password
        if isinstance(hash_from_db, str):
            hash_from_db = hash_from_db.encode('utf-8')
            
        try:
            return bcrypt.checkpw(password_bytes, hash_from_db)
        except ValueError as e:
            print(f"Bcrypt error: {e}")
            return False

# --- 5. EXECUTION & TESTING ---
engine = create_engine('sqlite:///:memory:') # Using in-memory DB for test
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

# A. INSERT DATA
new_user = User(firstname='Charles', lastname='Leclerc', username ='El Predestinato', email='charles.leclerc@ferrari.com', password="SuperSecret123!")
#new_user.set_password("SuperSecret123!") # Hashes automatically
session.add(new_user)
session.commit()

print("--- TEST RESULT ---")

# B. QUERY VIA SQLALCHEMY (The "Smart" way)
# Notice we just access .firstname and it's already decrypted
user_from_db = session.query(User).first()

is_valid = user_from_db.check_password("SuperSecret123!")
print(is_valid)
print(f"Login Attempt 'SuperSecret123!': {'Success' if is_valid else 'Failed'}")

# C. QUERY VIA RAW SQL (The "Database" way)
# This shows what a hacker or DBA would see without your encryption key
raw_data = session.execute(text("SELECT * FROM user")).fetchone()
print("\n--- DATABASE RAW VIEW (Encrypted) ---")
print(f"Stored Password:     {raw_data[5]}")

raw_data = session.execute(text("SELECT password FROM user")).fetchone()
print("\n--- DATABASE RAW VIEW ---")
print(f"Stored Password Hash: {raw_data[0]}")