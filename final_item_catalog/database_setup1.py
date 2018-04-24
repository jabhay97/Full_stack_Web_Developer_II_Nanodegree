from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()

class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    email = Column(String(250), nullable=False)
    picture = Column(String(250))


class Company(Base):
    __tablename__ = 'company'

    id = Column(Integer, primary_key=True)
    name = Column(String(200), nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)
    product = relationship('Product', cascade='all, delete-orphan')

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'name': self.name,
            'id': self.id,
        }


class Product(Base):
    __tablename__ = 'product'

    name = Column(String(90), nullable=False)
    id = Column(Integer, primary_key=True)
    categary=Column(String(50))
    price = Column(String(8))
    description = Column(String(200))
    company_id = Column(Integer, ForeignKey('company.id'))
    company = relationship(Company)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)


    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'name': self.name,
            'id': self.id,
            'description': self.description,
            'categary':self.categary,
            'price': self.price
        }

python engine = create_engine('postgresql://catalog:catalog@localhost/catalog')


Base.metadata.create_all(engine)
