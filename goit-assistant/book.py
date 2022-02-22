from collections import UserDict, UserString, UserList
from datetime import datetime
import datetime as dt


class AddressBook(UserDict):
    index = 0

    def add_record(self, record):
        self.data.update({record.name.value: record})

    def remove_record(self, name):
        del self.data[name]

    def iterator(self, N=2):
        page = {}
        for i in range(N):
            element = self.data[self.data.keys()[self.index+i]]
            page.update(element)
            self.index += 1
        yield element


class Record:

    def __init__(self, name, phone):
        self.name = Name(name)
        self.phone = [Phone(phone)]
        self.birthday = ""

    def add_phone(self, phone):
        self.phone.value.append(phone)

    def add_phones(self, phones):
        self.phone.value.extend(phones)

    def remove_phone(self, phone):
        index = self.phone.index(phone)
        self.phone.value.pop(index)

    def __repr__(self):
        return f"{self.name.value}: {self.phone.value} {self.birthday.value}"

    def add_birthday(self, birthday):
        self.birthday = Birthday(birthday)

    def days_to_birthday(self):
        if self.birthday.timetuple().tm_yday > datetime.today().date().timetuple().tm_yday:
            days = dt.date(datetime.today().year, self.birthday.month, self.birthday.day)
            days = days - datetime.today().date()
        else:
            days = dt.date(datetime.today().year + 1, self.birthday.month, self.birthday.day)
            days = days - datetime.today().date()
        return days.days


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
        self.value = phone


class Birthday(Field):
    name = "birthday"

    def __init__(self, date):
        self.value = datetime.strptime(date, "%d.%m.%Y")


