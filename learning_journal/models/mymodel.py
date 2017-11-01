from sqlalchemy import (
    Column,
    Index,
    Integer,
    Text,
)

from .meta import Base


class Blog(Base):
    __tablename__ = 'models'
    id = Column(Integer, primary_key=True)
    name = Column(Text)
    value = Column(Integer)

    def __init__(self, *args, **kwargs):


Index('my_index', MyModel.name, unique=True, mysql_length=255)
