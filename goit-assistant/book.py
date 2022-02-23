from collections import UserDict, UserString, UserList
from datetime import datetime
import datetime as dt


class AddressBook(UserDict):
    index = 0

    def add_record(self, record):
        self.data.update({record.name.name: record})

    def remove_record(self, name):
        del self.data[name]

    def iterator(self, N=2):
        page = {}
        items_left = len(self.data)-self.index
        if items_left < N:
            N = items_left
        for i in range(N):
            element = self.data[self.data.keys()[self.index+i]]
            page.update(element)
            self.index += 1
        yield page


class Record:

    def __init__(self, name, *args):
        self.name = Name(name)
        self.phone = []
        for item in args[0]:
            self.phone.append(Phone(item))
        self.birthday = ""

    def add_phone(self, *args):
        for item in args[0]:
            self.phone.append(Phone(item))

    # def remove_phone(self, phone):
    #     index = self.phone.index(phone)
    #     self.phone.pop(index)

    def __repr__(self):
        phones = [p.value for p in self.phone]
        return f"{self.name.name}: {phones} {self.birthday.value}"

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
    pass


class Name(Field):

    def __init__(self, name="Bob", is_mandatory=True):
        self.name = name
        self.is_mandatory = is_mandatory


class Phone(Field):

    def __init__(self, phone, is_mandatory=False):
        self.value = phone
        self.is_mandatory = is_mandatory


class Birthday(Field):

    def __init__(self, date, is_mandatory=False):
        self.value = datetime.strptime(date, "%d.%m.%Y")
        self.is_mandatory = is_mandatory


