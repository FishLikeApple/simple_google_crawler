from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

db_file_name = 'google_search_results.db'

Base = declarative_base()

class KeyWord(Base):
    __tablename__ = 'keyword'
   
    id = Column(Integer, primary_key=True)
    word = Column(String(1000))
 
class Content(Base):
    __tablename__ = 'content'

    id = Column(Integer, primary_key = True)
    title = Column(String(10000))
    url = Column(String(65536))

    keyword_id = Column(Integer,ForeignKey('keyword.id'))
    keyword = relationship(KeyWord) 

def create_database(db_file_name=db_file_name):
    engine = create_engine('sqlite:///'+db_file_name, echo=True)
    Base.metadata.create_all(engine)