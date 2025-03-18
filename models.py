from database import Base
from sqlalchemy import Column, Integer, String

class Kavita(Base):
    __tablename__ = 'kavita'

    id = Column(Integer,primary_key=True, index=True)
    kavitaText = Column(String)
    DoP = Column(String)
