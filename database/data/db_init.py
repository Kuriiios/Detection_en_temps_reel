from sqlalchemy import create_engine
from dotenv import load_dotenv
import os
load_dotenv()

ENGINE = create_engine(f"sqlite:///{os.getenv('DATABASE_PATH')}", echo=True)