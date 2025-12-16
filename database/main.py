from db_init import ENGINE
from sqlalchemy.orm import sessionmaker
from models import *

Base.metadata.create_all(ENGINE)
Session = sessionmaker(bind=ENGINE)