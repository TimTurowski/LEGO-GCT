from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date

Base = declarative_base()
class Einzelteil(Base):
    __tablename__ = 'Einzelteile'
    element_id = Column(String, primary_key=True)
    name = Column(String)

    def __repr__(self):
        return "<Book(element_id='{}', name='{}')>" \
            .format(self.element_id, self.name)

