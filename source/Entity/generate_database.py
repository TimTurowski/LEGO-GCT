from entities import Base
from sqlalchemy import create_engine

"""Ausführbare Datei zum Aufsetzen der in entities bestimmte Datenbankschema"""
engine = create_engine("postgresql+psycopg2://postgres:27R569RX@192.168.198.47:5432/LegoGCT")
Base.metadata.create_all(bind=engine)
