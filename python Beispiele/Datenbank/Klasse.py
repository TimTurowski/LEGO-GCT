from sqlalchemy import create_engine, String, ForeignKey, Column, CHAR, BOOLEAN
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.schema import Table

Base = declarative_base()

class Personen(Base):
    personen_id = Column(String,primary_key = True)
    name = Column(String)

class Wohnort(Base):
    plz = Column(String,primary_key = True)
    ort = Column(String)