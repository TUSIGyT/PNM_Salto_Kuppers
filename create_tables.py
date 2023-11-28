import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import Base

load_dotenv()

engine = create_engine(os.getenv("DB_URL"), echo=True)

Session = sessionmaker(bind=engine)

Base.metadata.create_all(engine)
