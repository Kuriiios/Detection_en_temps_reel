from sqlalchemy.orm import Session, sessionmaker
from  database.data.models import User, City
from database.data.db_init import ENGINE
import datetime
from loguru import logger

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=ENGINE)

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
