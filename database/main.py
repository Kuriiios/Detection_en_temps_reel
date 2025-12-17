from database.data.db_init import ENGINE
from sqlalchemy.orm import sessionmaker
from database.data.models import *
import os
from loguru import logger

file = os.path.splitext(os.path.basename(__file__))

logger.remove()
logger.add(sink=os.getenv("LOG_PATH") + '_' +file[0] + ".log", rotation="500 MB", level="INFO")

try:
    if os.path.isfile("database/users.db") is False:
        Base.metadata.create_all(ENGINE)
        Session = sessionmaker(bind=ENGINE)
        logger.success('Successfully created database')
    else:
        logger.info(f"Database still exist in folder {os.getenv('LOG_PATH') + '_' +file[0] + '.log'}")
except Exception as e:
    logger.error(f"Something failed during database checking or creation {e}")
