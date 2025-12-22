from sqlalchemy.orm import Session, sessionmaker
from  database.data.models import User, City, Token
from database.data.db_init import ENGINE
import datetime
import secrets
from loguru import logger
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta

load_dotenv()

HASH_STATIC_SALT = os.getenv("HASH_STATIC_SALT").encode()
if not HASH_STATIC_SALT:
    raise ValueError("No HASH_STATIC_SALT found in environment variables!")

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=ENGINE)

def generate_access_token():
    return secrets.token_urlsafe(32)

def get_db_session() -> Session:
    """Fournit une session de BDD."""
    return SessionLocal()

def add_new_user(user):
    with get_db_session() as session:
        created_at = datetime.datetime.now()
        try:
            city_from_db = session.query(City).filter_by(name = user.city).first()
            logger.success('Successfully retrieved city from db')
            if city_from_db is None:
                new_city = City(name=user.city)
                session.add(new_city)
                session.commit()
                city_from_db = session.query(City).filter_by(name = user.city).first()
                logger.success('Successfully inserted and retrieved city from db')
        except Exception as e:
            session.rollback()
            logger.error(f'Failed to retrieve and insert city into db with error: {e}')
            city_from_db = None
        try:
            new_user = User(firstname = user.firstname, lastname = user.lastname, username = user.username, email = user.email, password = user.password, city_id = city_from_db.id, created_at = created_at)
            session.add(new_user)
            session.commit()
            logger.success('Successfully inserted user into db')
            return {"response": True}
        except Exception as e:
            session.rollback()
            logger.error(f'Failed to insert new user into db with error: {e}')
            return {"response": False}

def sign_in(user_connection):
    with get_db_session() as session:
        try:
            email_index = User.generate_index(user_connection.email)
            user_from_db = session.query(User).filter_by(email_index = email_index).first()
            logger.success('User found')
            is_valid = user_from_db.check_password(user_connection.password)
            if is_valid is True:
                access_token = generate_access_token()
                created_at = datetime.now()
                expires_at = datetime.now() + timedelta(minutes=30)

                new_token = Token(token = access_token, user = user_from_db, created_at = created_at, expires_at = expires_at )
                session.add(new_token)
                session.commit()

                logger.success('Connection success')
                return {"access_token": access_token, "token_type": "Bearer", "expires_in": 1800}
            else : 
                logger.warning('Connection failed')
        except Exception as e:
            logger.warning(f'User not found {e}')

def sign_out(deconnection_data):
    with get_db_session() as session:
        try:
            token_to_delete = deconnection_data.access_token
            token_record = session.query(Token).filter_by(token=token_to_delete).first()
            
            if token_record:
                session.delete(token_record)
                session.commit()
                logger.success(f"Token {token_to_delete[:10]}... deleted successfully.")
                return {"response": True}
            else:
                logger.warning(f"Sign out failed: Token not found.")
                return {"response": False}
        except Exception as e:
            session.rollback()
            logger.error(f"Error during sign out: {e}")
            return {"response": False}

def get_user_infos(current_user):
    return {
        "firstname": current_user["firstname"],
        "lastname": current_user["lastname"],
        "username": current_user["username"],
        "email": current_user["email"],
        "created_at": current_user["created_at"],
        "city": current_user["city"],
    }