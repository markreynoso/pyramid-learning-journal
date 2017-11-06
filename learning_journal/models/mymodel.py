"""Create model to store data in database."""
from sqlalchemy import (
    Column,
    DateTime,
    Index,
    Integer,
    String,
)

from .meta import Base


class Blog(Base):
    """Initialize data in for database."""

    __tablename__ = 'journals'
    id = Column(Integer, primary_key=True)
    title = Column(String(convert_unicode=True))
    creation_date = Column(DateTime)
    body = Column(String(convert_unicode=True))

    def to_dict(self):
        """Take all model attributes and render them as a dictionary."""
        return {
            'id': self.id,
            'title': self.title,
            'creation_date': self.creation_date,
            'body': self.body
        }


Index('my_index', Blog.title, unique=True, mysql_length=255)
