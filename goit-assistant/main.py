from book import *


def input_error(func):
    def inner(*args, **kwargs):
        result = "Enter help for more information"
        try:
            result = func(*args, **kwargs)
        except KeyError:
            print(f"Incorrect command")
        except ValueError:
            print(f"Incorrect value provided")
        except IndexError:
            print(f"Not enough arguments")
        except NameError:
            pass
        return result
    return inner


@input_error
def hello(*args):
    return "How can I help you?"


@input_error
def add_contact(*args):
    name = args[0][0]
    phone = args[0][1:]
    phones = [Phone(p) for p in phone]
    record = Record(Name(name), phones)
    contacts.add_record(record)
    return f"{name}: {phone} was added"


@input_error
def change(*args):
    name = args[0][0]
    phone = args[0][1:]
    phones = [Phone(p) for p in phone]
    contacts.change_record(Name(name), phones[0], phones[1])
    return f"{name} was updated"


@input_error
def remove(*args):
    name = args[0][0]
    phone = args[0][1:]
    phones = [Phone(p) for p in phone]
    contacts.remove_record_phone(Name(name), phones[0])
    return f"{name} was updated"


@input_error
def phone(*args):
    name = args[0][0]
    return contacts[name]


@input_error
def email(*args):
    name = args[0][0]
    return contacts[name]


@input_error
def birthday(*args):
    name = args[0][0]
    birthday = args[0][1]
    contacts[name].add_birthday(Birthday(birthday))
    return f"{name}: {birthday} was updated"


@input_error
def show_all(*args):
    return print(contacts)


@input_error
def search(*args):
    query = args[0][0]
    return contacts.search(query)


@input_error
def close(*args):
    contacts.save()
    return "Good bye!"


@input_error
def help_instructions(*args):
    return """ 
    Please select any command from listed below with examples:
    "hello": hello,
    "add": add Sasha +380505550055 +380505550099
    "change": change Sasha +380505550055 +380505550000
    "remove": remove Sasha +380505550055
    "phone": phone Sasha,
    "email": e-mail Sasha,
    "birthday": birthday Sasha 03.05.1985,
    "show all": show all,
    "search": search Sas,
    "good bye": good bye,
    "close": close,
    "exit": exit,
    "help": help
    """

commands = {
    "hello": hello,
    "add": add_contact,
    "change": change,
    "remove": remove,
    "phone": phone,
    "email": email,
    "birthday": birthday,
    "show all": show_all,
    "search": search,
    "good bye": close,
    "close": close,
    "exit": close,
    "help": help_instructions
}


def handler(string):
    pattern = "^hello|^add|^change|^remove|^phone|^birthday|^show all|^search|^good bye|^close|^exit|^help"
    try:
        command = re.search(pattern, string, re.IGNORECASE).group(0)
        command = command.lower()
        args = re.sub(pattern, "", string, re.IGNORECASE).split()
    except ValueError:
        print("Command input error")
    except:
        command, args = None, None
        print("Unknown command. Enter help for more information")
    return command, args


def main():
    global contacts
    contacts = AddressBook()
    # to_load = input("Do you want to load existing AddressBook? y/n: ")
    # if to_load == "y":
    #     contacts.load()
    print("Hello. Enter your command: ")
    while True:
        input_string = input("=> ")
        command, args = handler(input_string)
        func = commands.get(command)
        if command:
            result = func(args)
            print(result)
        if result == "Good bye!":
            break



if __name__ == "__main__":
    # contacts = {
    #     "Ivan": {"phone": "+380501234567", "email": "ivan@gmail.com"},
    #     "Roman": {"phone": "+3805039876543", "email": "roman@gmail.com"}
    # }
    main()
