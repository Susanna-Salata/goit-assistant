from collections import UserDict, UserString, UserList
from datetime import datetime
import datetime as dt
import re
import os
import pickle


class AddressBook(UserDict):
    index = 0

    def add_record(self, record):
        self.data.update({record.name.name: record})

    def remove_record(self, name):
        del self.data[name]

    def change_record(self, name, phone_old, phone_new):
        self.data[name.name].replace_phone(phone_old, phone_new)

    def remove_record_phone(self, name, phone_old):
        self.data[name.name].remove_phone(phone_old)

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

    def save(self):
        file_path = os.path.join(os.getcwd(), "address_book.bin")
        with open(file_path, "wb") as file:
            pickle.dump(self.data, file)

    def load(self):
        file_path = os.path.join(os.getcwd(), "address_book.bin")
        with open(file_path, "rb") as file:
            self.data = pickle.load(file)
        print("__")

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
        for item in args[0]:
            self.phone.append(item)
        self.birthday = ""

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

    def __repr__(self):
        phones = [p.value for p in self.phone]
        if self.birthday:
            return f"{self.name.name}: {phones} {self.birthday.value}"
        else:
            return f"{self.name.name}: {phones}"

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


