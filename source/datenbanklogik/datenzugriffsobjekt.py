from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

engine = create_engine("postgresql+psycopg2://postgres:27R569RX@192.168.198.47:5432/LegoGCT")
Session = sessionmaker(engine)