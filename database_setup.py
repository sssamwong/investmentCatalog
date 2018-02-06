from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
import datetime

Base = declarative_base()

class User(Base):
  __tablename__ = 'user'

  name = Column(String(250), nullable = False)
  email = Column(String(250), nullable=False)
  picture = Column(String(250))
  id = Column(Integer, primary_key = True)

class Catalog(Base):
  __tablename__ = 'catalog'

  id = Column(Integer, primary_key=True)
  name = Column(String(250), nullable=False)
  user_id = Column(Integer,ForeignKey('user.id'))
  user = relationship(User)

  @property
  def serialize(self):
    """Return object data in easily serializeable format"""
    return {
      'name'  : self.name,
      'id'    : self.id,
    }

class Investment(Base):
  __tablename__ = 'investment'


  name =Column(String(80), nullable = False)
  id = Column(Integer, primary_key = True)
  description = Column(String(250))
  price = Column(String(8))
  catalog_id = Column(Integer,ForeignKey('catalog.id'))
  catalog = relationship(Catalog)
  user_id = Column(Integer,ForeignKey('user.id'))
  user = relationship(User)
  createDate = Column(DateTime, default=datetime.datetime.utcnow)

  @property
  def serialize(self):
    """Return object data in easily serializeable format"""
    return {
      'name'         : self.name,
      'description'  : self.description,
      'id'           : self.id,
      'price'        : self.price,
  }

engine = create_engine('sqlite:///itemcatalog.db')
 

Base.metadata.create_all(engine)
