from collections import UserDict, UserString, UserList
from datetime import datetime
import datetime as dt
import re
import os
import pickle

from models import Contact, Phone as PhoneDB, Email as EmailDB

from sqlalchemy.engine import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine("sqlite:///../addressbook.db")
Session = sessionmaker(bind=engine)
session = Session()


class AddressBook(UserDict):
    index = 0

    def add_record(self, record):
        session.add(record.contact)
        session.commit()

    # def add_record(self, record):
    #     self.data.update({record.name.name: record})

    def remove_record(self, name):
        session.query(Contact).filter_by(name=name.name).delete()
        session.commit()

    def change_record(self, name, phone_old, phone_new):
        contact_ids = session.query(Contact.id).\
            filter(Contact.name == name.name)
        contact_ids = [c.id for c in contact_ids]
        session.query(PhoneDB).\
            filter(PhoneDB.phone == phone_old.value,
                   PhoneDB.contact_id.in_(contact_ids)).\
            update({'phone': phone_new.value})
        session.commit()

    def remove_record_phone(self, name, phone_old):
        contact_ids = session.query(Contact.id). \
            filter(Contact.name == name.name)
        contact_ids = [c.id for c in contact_ids]
        session.query(PhoneDB). \
            filter(PhoneDB.phone == phone_old.value,
                   PhoneDB.contact_id.in_(contact_ids)). \
            delete()
        session.commit()

    def iterator(self, N=2):
        page = {}
        data = session.query(Contact).execute().fetch_all()
        items_left = len(data)-self.index
        if items_left < N:
            N = items_left
        for i in range(N):
            element = data[data.keys()[self.index+i]]
            page.update(element)
            self.index += 1
        yield page

    def __repr__(self):
        for c in session.query(Contact):
            return(f'{c.name}: {c.birthday}\n phones: {c.phones} \n emails: {c.emails}')

    def __str__(self):
        return self.__repr__()

    # def save(self):
    #     file_path = os.path.join(os.getcwd(), "address_book.bin")
    #     with open(file_path, "wb") as file:
    #         pickle.dump(self.data, file)
    #
    # def load(self):
    #     file_path = os.path.join(os.getcwd(), "address_book.bin")
    #     with open(file_path, "rb") as file:
    #         self.data = pickle.load(file)
    #     print("__")

    def search(self, query):
        result = AddressBook()
        for key, value in self.data.items():
            if query in str(value):
                result.add_record(value)
        return result


class Record:

    def __init__(self, name, *args):
        self.name = name
        self.phone = []
        self.email = []
        self.birthday = ""
        self.contact = Contact(name=self.name.name)
        for item in args[0]:
            new_phone = PhoneDB(phone=item.value)
            self.contact.phones.append(new_phone)


    def add_phone(self, *args):
        for item in args[0]:
            self.phone.append(item)

    def remove_phone(self, phone):
        index = self.phone.index(phone)
        self.phone.pop(index)

    def replace_phone(self, phone_old, phone_new):
        index = self.phone.index(phone_old)
        self.phone[index] = phone_new

    def change_phone(self, index, phone):
        self.phone[index] = phone

    def add_email(self, *args):
        for item in args[0]:
            self.email.append(item)

    def remove_email(self, email):
        index = self.email.index(email)
        self.email.pop(index)

    def replace_email(self, email_old, email_new):
        index = self.email.index(email_old)
        self.email[index] = email_new

    def change_email(self, index, email):
        self.email[index] = email

    def __repr__(self):
        phones = [p.value for p in self.phone]
        emails = [p.value for p in self.email]
        if self.birthday:
            return f"{self.name.name}: {phones} {emails} {self.birthday.value}"
        else:
            return f"{self.name.name}: {phones} {emails}"

    def add_birthday(self, birthday):
        self.birthday = birthday

    def days_to_birthday(self):
        if self.birthday.timetuple().tm_yday > datetime.today().date().timetuple().tm_yday:
            days = dt.date(datetime.today().year, self.birthday.month, self.birthday.day)
            days = days - datetime.today().date()
        else:
            days = dt.date(datetime.today().year + 1, self.birthday.month, self.birthday.day)
            days = days - datetime.today().date()
        return days.days


class Field():

    def __init__(self):
        self.__value = None

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):
        self.__value = value


class Name(Field):

    def __init__(self, name="Bob", is_mandatory=True):
        self.name = name
        self.is_mandatory = is_mandatory


class Phone(Field):

    def __init__(self, phone, is_mandatory=False):
        self.__value = self.check(phone)
        self.is_mandatory = is_mandatory

    def check(self, value):
        pattern = "^\+[0-9]{12}$"
        if re.match(pattern, value):
            return value
        else:
            raise ValueError

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):
        self.__value = self.check(value)

    def __eq__(self, other):
        return self.__value == other.value


class Birthday(Field):

    def __init__(self, date, is_mandatory=False):
        self.__value = self.check(date)
        self.is_mandatory = is_mandatory

    def check(self, value):
        try:
            return datetime.strptime(value, "%d.%m.%Y")
        except:
            raise ValueError

    def __repr__(self):
        return str(self.__value)

    @property
    def value(self):
        if self.__value:
            return self.__value.strftime('%d.%m.%Y')
        else:
            return ""

    @value.setter
    def value(self, value):
        self.__value = self.check(value)

class Email(Field):

    def __init__(self, email, is_mandatory=False):
        self.__value = self.check(email)
        self.is_mandatory = is_mandatory

    def check(self, value):
        pattern = "[0-9A-Za-z\.\_\-]+@[0-9A-Za-z\.\-]+\.[A-Za-z]+$"
        if re.match(pattern, value):
            return value
        else:
            raise ValueError

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):
        self.__value = self.check(value)

    def __eq__(self, other):
        return self.__value == other.value
