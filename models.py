import os

from dotenv import load_dotenv
from geoalchemy2 import Geometry
from sqlalchemy import (
    Column,
    Date,
    DateTime,
    Float,
    Integer,
    String,
    Uuid,
    create_engine,
)
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy_utils import URLType

load_dotenv()

engine = create_engine(os.getenv("DB_URL"), echo=True)

Session = sessionmaker(bind=engine)

Base = declarative_base()


class Flora(Base):
    __tablename__ = "flora"

    uuid = Column(Uuid, primary_key=True)
    created_at = Column(DateTime)
    uploaded_at = Column(DateTime)
    created_by = Column(String(60))
    field_date = Column(Date)
    title = Column(String)
    especie = Column(String)
    otro = Column(String)
    lat = Column(Float)
    lon = Column(Float)
    accuracy = Column(Integer)
    UTM_N = Column(Integer)
    UTM_E = Column(Integer)
    UTM_Zone = Column(String(4))
    foto = Column(URLType)
    file_name = Column(String)
    geometry = Column(Geometry("POINT", srid=4326, spatial_index=True))
