from sqlalchemy import (
    Column,
    Index,
    Integer,
    Text,
)

from .meta import Base


class Blog(Base):
    """Initialize data in for database."""

    __tablename__ = 'journals'
    id = Column(Integer, primary_key=True)
    title = Column(Text)
    date = Column(Text)
    body = Column(Text)


    # def __init__(self, *args, **kwargs):
    #     """Modify the init method to do more things."""
    #     super(Expense, self).__init__(*args, **kwargs)
    #     self.creation_date = datetime.now()

        
    def to_dict(self):
        """Take all model attributes and render them as a dictionary."""
        return {
            'id': self.id,
            'title': self.title,
            'due_date': self.date,
            'body': self.body
        }



Index('my_index', Blog.title, unique=True, mysql_length=255)
