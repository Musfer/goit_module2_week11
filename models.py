
from datetime import datetime

from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import ForeignKey, Table, MetaData
from sqlalchemy.sql.sqltypes import DateTime

from db import Base, engine, db_session

# таблица для связи many2many

note_m2m_tag = Table(
    "note_m2m_tag",
    Base.metadata,
    Column("id", Integer, primary_key=True),
    Column("note", Integer, ForeignKey("notes.id")),
    Column("tag", Integer, ForeignKey("tags.id")),
)


class Note(Base):
    __tablename__ = "notes"
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    created = Column(DateTime, default=datetime.now())
    description = Column(String(150), nullable=False)
    done = Column(Boolean, default=False)
    tags = relationship("Tag", secondary=note_m2m_tag, backref="notes")


class Contact(Base):
    __tablename__ = "contacts"
    id = Column(Integer, primary_key=True)
    fullname = Column(String(50), nullable=False, unique=True)
    date_of_birth = Column(DateTime, nullable=True)


class Phone(Base):
    __tablename__ = "phones"
    id = Column(Integer, primary_key=True)
    number = Column(String(50), nullable=True)
    contact_id = Column(Integer, ForeignKey(Contact.id, ondelete="CASCADE"))


class Email(Base):
    __tablename__ = "emails"
    id = Column(Integer, primary_key=True)
    mail = Column(String(50), nullable=True)
    contact_id = Column(Integer, ForeignKey(Contact.id, ondelete="CASCADE"), nullable=False)


class Tag(Base):
    __tablename__ = "tags"
    id = Column(Integer, primary_key=True)
    name = Column(String(25), nullable=False, unique=True)

    def __repr__(self) -> str:
        return self.name


if __name__ == "__main__":
    Base.metadata.create_all(engine)