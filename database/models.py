from sqlalchemy import Column, Integer, String, Date, LargeBinary, ForeignKey, DateTime
from sqlalchemy.orm import relationship, DeclarativeBase
from datetime import datetime
import bcrypt

class Base(DeclarativeBase):
     pass

class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    firstname = Column(LargeBinary, nullable=False)
    lastname = Column(LargeBinary, nullable=False)
    username = Column(LargeBinary, nullable=False)
    email = Column(String(255), nullable=False, unique=True)
    password = Column(String(100), nullable=False)
    created_at = Column(Date)

    city_id = Column(Integer, ForeignKey('city.id'))
    city = relationship('City', back_populates='user')

    object_per_user = relationship('ObjectPerUser', back_populates='user')

    tokens = relationship('Token', back_populates='user', cascade='all, delete-orphan')

    def set_password(self, plaintext_password: str):
        password_bytes = plaintext_password.encode('utf-8')
        hashed_password = bcrypt.hashpw(password_bytes, bcrypt.gensalt())
        self.password = hashed_password.decode('utf-8')

    def check_password(self, plaintext_password: str) -> bool:
        input_bytes = plaintext_password.encode('utf-8')
        stored_hash_bytes = self.password.encode('utf-8')
        return bcrypt.checkpw(input_bytes, stored_hash_bytes)


class City(Base):
    __tablename__ = 'city'

    id = Column(Integer, primary_key=True, autoincrement=True)
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

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    url = Column(String, nullable=False)
    date = Column(Date, nullable=False)

    user_per_object = relationship('ObjectPerUser', back_populates='object')

class Token(Base):
    id = Column(Integer, primary_key=True)
    token = Column(String(512), nullable=False, unique=True, index=True)

    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship('User', back_populates='tokens')

    created_at = Column(DateTime, default=datetime.utcnow)
    expires_at = Column(DateTime)