from sqlalchemy.orm import Session, sessionmaker
from  database.data.models import User, City, Token, Object, ObjectPerUser
from database.data.db_init import ENGINE
import datetime
import base64
import secrets
from loguru import logger
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta, date

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
        created_at = datetime.now()
        try:
            city_obj = session.query(City).filter_by(name=user.city).first()

            if city_obj is None:
                city_obj = City(name=user.city)
                session.add(city_obj)
                session.flush() 
                logger.success(f"Created new city object for {user.city}")
        except Exception as e:
            session.rollback()
            logger.error(f'Failed to retrieve and insert city into db with error: {e}')
            city_obj = None
        try:
            new_user = User(
                firstname = user.firstname, 
                lastname = user.lastname, 
                username = user.username, 
                email = user.email, 
                password = user.password, 
                city_id = city_obj.id,
                created_at = created_at)
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

def get_user_id(user_email):
    with get_db_session() as session:
        try:
            email_index = User.generate_index(user_email)
            user_from_db = session.query(User).filter_by(email_index = email_index).first()
            return user_from_db.id
        except Exception as e:
            logger.warning(f'User not found {e}')

def get_user_objects(current_user_id):
    with get_db_session() as session:
        try:
            objects_from_db = (session.query(Object)
                               .join(ObjectPerUser, Object.id == ObjectPerUser.object_id)
                               .join(User, ObjectPerUser.user_id == User.id)
                               .where(User.id == current_user_id)
                               .all())
            return objects_from_db
        except Exception as e:
            logger.warning(f'User not found {e}')
            return []
            
def get_user_id_by_token(token_string: str):
    """
    Retrieves the user_id associated with a valid, non-expired token.
    Returns the user_id if valid, None if the token is invalid or expired.
    """
    with get_db_session() as session:
        try:
            token_record = session.query(Token).filter_by(token=token_string).first()

            if not token_record:
                logger.warning(f"Token validation failed: Token not found.")
                return None

            if token_record.expires_at and datetime.now() > token_record.expires_at:
                logger.warning(f"Token validation failed: Token expired at {token_record.expires_at}")
                return None

            logger.success(f"Token validated for user_id: {token_record.user_id}")
            return token_record.user_id

        except Exception as e:
            logger.error(f"Error validating token: {e}")
            return None

def get_object_id(object):
    with get_db_session() as session:
        try:
            object_from_db = session.query(Object).filter_by(name = object.name, confidence = object.confidence, img_binary = object.img_binary,).first()
            return object_from_db.id
        except Exception as e:
            logger.warning(f'User not found {e}')

def add_bulk_objects(objects_list, token_string):
    with get_db_session() as session:
        try:
            user_id = get_user_id_by_token(token_string)
            current_date = date.today()            
            
            for obj_data in objects_list:
                binary_data = base64.b64decode(obj_data.img_binary)
                # Use obj_data.name instead of obj_data['name']
                new_obj = Object(
                    name=obj_data.name, 
                    confidence=obj_data.confidence, 
                    img_binary=binary_data, 
                    date=current_date
                )
                session.add(new_obj)
                session.flush()

                link = ObjectPerUser(user_id=user_id, object_id=new_obj.id)
                session.add(link)
         
            session.commit()
            return True
        except Exception as e:
            session.rollback()
            logger.error(f"Bulk save error: {e}")
            return False