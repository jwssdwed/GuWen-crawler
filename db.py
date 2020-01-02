import sqlalchemy
from sqlalchemy.orm import sessionmaker
from sqlalchemy import UniqueConstraint
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

engine = sqlalchemy.create_engine('mysql://root@localhost:3306/GuWen?charset=utf8mb4', echo=True)
Session = sessionmaker(bind=engine)
session = Session()

#------------------- TABLES BEGIN -----------------------
class CiAuthor(Base):
    __tablename__ = 'authors'
    __table_args__ = (
        UniqueConstraint('name', name='uc_author_name'),
        {'mysql_engine': 'InnoDB', 'mysql_charset': 'utf8mb4'}
    )

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(32))
    desc = Column(String(1000))

    def __repr__(self):
        return f'User {self.name}'
#------------------- TABLES END -----------------------

Base.metadata.create_all(engine)
