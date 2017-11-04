"""Create model to store data in database."""
from sqlalchemy import (
    Column,
    DateTime,
    Index,
    Integer,
    Unicode,
)

from .meta import Base


class Blog(Base):
    """Initialize data in for database."""

    __tablename__ = 'journals'
    id = Column(Integer, primary_key=True)
    title = Column(Unicode)
    creation_date = Column(DateTime)
    body = Column(Unicode)

    def to_dict(self):
        """Take all model attributes and render them as a dictionary."""
        return {
            'id': self.id,
            'title': self.title,
            'creation_date': self.creation_date.strftime('%B %d, %Y'),
            'body': self.body
        }


Index('my_index', Blog.title, unique=True, mysql_length=255)
