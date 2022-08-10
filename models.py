from datetime import datetime

from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import ForeignKey, Table
from sqlalchemy.sql.sqltypes import DateTime


Base = declarative_base()


class Contact(Base):
    __tablename__ = "contacts"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    birthday = Column(DateTime, nullable=True)

    phones = relationship("Phone", back_populates="contact")
    emails = relationship("Email", back_populates="contact")


class Phone(Base):
    __tablename__ = "phones"
    id = Column(Integer, primary_key=True, autoincrement=True)
    phone = Column(String(13), nullable=False)
    contact_id = Column(Integer, ForeignKey(Contact.id, ondelete="CASCADE"))

    contact = relationship("Contact", back_populates="phones")


class Email(Base):
    __tablename__ = "emails"
    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(50), nullable=False)
    contact_id = Column(Integer, ForeignKey(Contact.id, ondelete="CASCADE"))

    contact = relationship("Contact", back_populates="emails")
