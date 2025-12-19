from sqlalchemy import Column, Integer, String, Date, ForeignKey, DateTime
from sqlalchemy.orm import relationship, DeclarativeBase
from database.modules.encryption_db import EncryptedString, BcryptPassword
from datetime import datetime
import bcrypt
import hashlib
import hmac
import os
from dotenv import load_dotenv

load_dotenv()

HASH_STATIC_SALT = os.getenv("HASH_STATIC_SALT").encode()
if not HASH_STATIC_SALT:
    raise ValueError("No HASH_STATIC_SALT found in environment variables!")


class Base(DeclarativeBase):
     pass

class User(Base):
    __tablename__ = 'user'
    
    id = Column(Integer, primary_key=True)
    firstname = Column(EncryptedString(500), nullable=False)
    lastname = Column(EncryptedString(500), nullable=False)
    username = Column(EncryptedString(500), nullable=False)
    email = Column(EncryptedString(500), nullable=False, unique=True)
    email_index = Column(String(64), unique=True, index=True)
    password = Column(BcryptPassword(128), nullable=False)
    created_at = Column(Date)

    city_id = Column(Integer, ForeignKey('city.id'))
    city = relationship('City', back_populates='user')

    object_per_user = relationship('ObjectPerUser', back_populates='user')

    token = relationship('Token', back_populates='user', cascade='all, delete-orphan')

    @staticmethod
    def generate_index(email: str) -> str:
        return hmac.new(HASH_STATIC_SALT, email.lower().strip().encode(), hashlib.sha256).hexdigest()

    def __init__(self, **kwargs):
        if 'email' in kwargs:
            kwargs['email_index'] = self.generate_index(kwargs['email'])
        super().__init__(**kwargs)

    def set_password(self, password: str):
        salt = bcrypt.gensalt()
        
        hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
        self.password = hashed.decode('utf-8')
    

    def check_password(self, password: str) -> bool:
        password_bytes = password.encode('utf-8')
    
        hash_from_db = self.password
        if isinstance(hash_from_db, str):
            hash_from_db = hash_from_db.encode('utf-8')
            
        try:
            return bcrypt.checkpw(password_bytes, hash_from_db)
        except ValueError as e:
            print(f"Bcrypt error: {e}")
            return False


class City(Base):
    __tablename__ = 'city'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False) 

    user = relationship('User', back_populates='city')

class ObjectPerUser(Base):
    __tablename__ = 'object_per_user'

    id = Column(Integer, primary_key=True)

    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship('User', back_populates='object_per_user')

    object_id = Column(Integer, ForeignKey('object.id'))
    object = relationship('Object', back_populates='user_per_object')


class Object(Base):
    __tablename__ = 'object'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    url = Column(String, nullable=False)
    date = Column(Date, nullable=False)

    user_per_object = relationship('ObjectPerUser', back_populates='object')

class Token(Base):
    __tablename__ = 'token'

    id = Column(Integer, primary_key=True)
    token = Column(String(512), nullable=False, unique=True, index=True)

    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship('User', back_populates='token')

    created_at = Column(DateTime, default=datetime.utcnow)
    expires_at = Column(DateTime)