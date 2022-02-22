from collections import UserDict, UserString, UserList


class AddressBook(UserDict):

    def add_record(self, record):
        self.data.update({record.name.value: record})

    def remove_record(self, name):
        del self.data[name]


class Record:

    def __init__(self, name, phone):
        self.name = Name(name)
        self.phone = Phone(phone)

    def add_phone(self, phone):
        self.phone.value.append(phone)

    def add_phones(self, phones):
        self.phone.value.extend(phones)

    def remove_phone(self, phone):
        index = self.phone.index(phone)
        self.phone.value.pop(index)

    def __repr__(self):
        return f"{self.name.value}: {self.phone.value}"


class Field():
    name = None
    value = None
    is_mandatory = True


class Name(Field):
    name = "name"

    def __init__(self, name):
        self.value = name


class Phone(Field):
    name = "phone"
    is_mandatory = False

    def __init__(self, phone):
        if isinstance(phone, list):
            self.value = phone
        else:
            self.value = [phone]
