from collections import UserDict, UserString, UserList
from datetime import datetime
import datetime as dt
import re


class AddressBook(UserDict):
    index = 0

    def add_record(self, record):
        self.data.update({record.name.name: record})

    def remove_record(self, name):
        del self.data[name]

    def change_record(self, name):
        print(self.data[name])
        command_1 = input("Select 'delete_phone' or 'change_phone': \n=> ")
        command_2 = input("Select index for phone: \n=> ")
        command_2 = int(command_2)
        if command_1 == "delete_phone":
            self.data[name].remove_phone(command_2)
        elif command_1 == "change_phone":
            command_3 = input("Type new phone: \n=> ")
            self.data[name].replace_phone(command_2, Phone(command_3))
        else:
            print("Unknown command")

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
        self.name = name
        self.phone = []
        for item in args[0]:
            self.phone.append(item)
        self.birthday = ""

    def add_phone(self, *args):
        for item in args[0]:
            self.phone.append(item)

    def remove_phone(self, index):
        self.phone.pop(index)

    def replace_phone(self, index, phone):
        self.phone[index] = phone

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


