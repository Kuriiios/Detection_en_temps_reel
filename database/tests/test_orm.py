import pytest
from sqlalchemy.exc import IntegrityError
from database.data.models import User
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database.data.models import Base

@pytest.fixture(scope="module")
def engine_test():
    return create_engine("sqlite:///:memory:")

@pytest.fixture(scope="module")
def setup_db(engine_test):
    Base.metadata.create_all(engine_test)
    yield
    Base.metadata.drop_all(engine_test)

@pytest.fixture(scope="function")
def test_session(engine_test, setup_db):
    connection = engine_test.connect()
    transaction = connection.begin()

    SessionTest = sessionmaker(bind=engine_test, autocommit=False, autoflush=False)
    session = SessionTest(bind=connection)

    yield session

    session.close()
    connection.close()

def test_create_user(test_session):
    user = User(firstname='Charles', lastname='Leclerc', username ='El Predestinato', email='charles.leclerc@ferrari.com', password='leo')
    test_session.add(user)
    test_session.commit()
    
    assert user.id is not None
    assert user.firstname == 'Charles'
    assert user.lastname == 'Leclerc'
    assert user.username == 'El Predestinato'
    assert user.email == 'charles.leclerc@ferrari.com'


def test_unique_email_constraint(test_session):
    user1 = User(firstname='Charles', lastname='Leclerc', username ='El Predestinato', email='charles.leclerc@ferrari.com', password='leo')
    user2 = User(firstname='Lewis', lastname='Hamilton', username ='Goat', email='charles.leclerc@ferrari.com', password='lh44')
    
    test_session.add(user1)
    test_session.commit()
    
    test_session.add(user2)
    with pytest.raises(IntegrityError):
        test_session.commit()


def test_query_user(test_session):
    user = User(firstname='Charles', lastname='Leclerc', username ='El Predestinato', email='charles.leclerc@ferrari.com', password='leo')
    test_session.add(user)
    test_session.commit()

    search_index = User.generate_index('charles.leclerc@ferrari.com')   
 
    queried_user = test_session.query(User).filter_by(email_index=search_index).first()
    assert queried_user is not None
    assert queried_user.firstname == 'Charles'
    assert queried_user.email == 'charles.leclerc@ferrari.com'


def test_update_user(test_session):
    user = User(firstname='Charles', lastname='Leclerc', username ='El Predestinato', email='charles.leclerc@ferrari.com', password='leo')
    test_session.add(user)
    test_session.commit()
    
    user.name = 'Arthur'
    test_session.commit()
    
    updated_user = test_session.query(User).filter_by(id=user.id).first()
    assert updated_user.name == 'Arthur'


def test_delete_user(test_session):
    user = User(firstname='Charles', lastname='Leclerc', username ='El Predestinato', email='charles.leclerc@ferrari.com', password='leo')
    test_session.add(user)
    test_session.commit()
    
    test_session.delete(user)
    test_session.commit()
    
    deleted_user = test_session.query(User).filter_by(id=user.id).first()
    assert deleted_user is None

def test_correct_password(test_session):
    user = User(firstname='Charles', lastname='Leclerc', username ='El Predestinato', email='charles.leclerc@ferrari.com', password="Leo_Leclerc_Saint_Mleux")
    test_session.add(user)
    test_session.commit()

    user_from_db = test_session.query(User).first()
    is_valid = user_from_db.check_password("Leo_Leclerc_Saint_Mleux")
    assert is_valid is True
