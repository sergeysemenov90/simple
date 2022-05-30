from datetime import datetime

from sqlalchemy import Column, Integer, String, TIMESTAMP, Boolean, Text, ForeignKey

from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class User(Base):
    __tablename__ = 'simple_user'

    id = Column(Integer, primary_key=True, autoincrement=True)
    site_owner = Column(Boolean, default=False)
    first_name = Column(String(30), nullable=True)
    last_name = Column(String(30), nullable=True)
    username = Column(String(50), unique=True)
    password = Column(String(200))
    registered = Column(TIMESTAMP(timezone=False), default=datetime.now(), index=True)

    notes = relationship('Note', back_populates='author')

    def __repr__(self):
        return f'{self.username}'


class Note(Base):
    __tablename__ = 'note'

    id = Column(Integer, primary_key=True, autoincrement=True)
    author_id = Column(Integer, ForeignKey('simple_user.id'), nullable=False)
    title = Column(String(200), index=True)
    text = Column(Text)
    created_at = Column(TIMESTAMP(timezone=False), default=datetime.now(), index=True)
    is_published = Column(Boolean, default=False)
    views = Column(Integer)

    author = relationship('User', back_populates='notes')

