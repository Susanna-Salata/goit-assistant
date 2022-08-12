from datetime import datetime

from mongoengine import EmbeddedDocument, Document
from mongoengine.fields import BooleanField, DateTimeField, EmbeddedDocumentField, ListField, StringField, DateField


class Phone(EmbeddedDocument):
    phone = StringField()


class Record(Document):
    name = StringField()
    created = DateTimeField(default=datetime.now())
    birthday = DateField()
    phones = ListField(EmbeddedDocumentField(Phone))
    meta = {'allow_inheritance': True}
