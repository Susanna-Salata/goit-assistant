from collections import UserDict, UserString, UserList


class AddressBook(UserDict):

    def add_record(self, record):
        self.data.update({record.name.value: record})

    def remove_record(self, name):
        del self.data[name]


class Record:

    def __init__(self, name, phone=[], email=[]):
        self.name = Name(name)
        self.phone = Phone(phone)
        self.email = Email(email)

    def add_record(self, phone, type="phone"):
        self.phone.data.append(phone)

    def add_records(self, phones, type="phone"):
        self.phone.data.extend(phones)

    def remove_record(self, phone, type="phone"):
        pass

class Field(UserList):
    name = None
    value = None
    is_mandatory = True


class Name(Field):
    name = "name"
    value = None
    is_mandatory = True

    def __init__(self, name):
        self.value = name


class Phone(Field):
    name = "phone"
    value = []
    is_mandatory = False

    def __init__(self):
        self.value = self.data


class Email(Field):
    name = "e-mail"
    value = []
    is_mandatory = False

    contacts = {
        "Ivan": {"name": "Ivan", "phone": ["+380501234567", "+380501234569"], "e-mail": ["ivan@gmail.com"]},
        "Roman": {"name": "Roman", "phone": ["+3805039876543"], "e-mail": ["roman@gmail.com", "roma@gmail.com"]}
    }