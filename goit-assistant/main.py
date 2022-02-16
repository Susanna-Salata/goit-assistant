import re


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
        return result
    return inner


@input_error
def hello(*args):
    return "How can I help you?"


@input_error
def add_contact(*args):
    name = args[0][0]
    phone = args[0][1]
    contacts.update({name: phone})
    return f"{name}: {phone} was added"


@input_error
def change(*args):
    name = args[0][0]
    phone = args[0][1]
    contacts.update({name: phone})
    return f"{name}: {phone} was updated"


@input_error
def phone(*args):
    name = args[0]
    return contacts[name]


@input_error
def show_all(*args):
    return contacts


@input_error
def close(*args):
    return "Good bye!"


@input_error
def help_instructions(*args):
    return """ 
    Please select any command from listed below with examples:
    "hello": hello,
    "add": add Sasha +380505550055,
    "change": change Sasha +380505550000,
    "phone": phone Sasha,
    "show all": show all,
    "good bye": good bye,
    "close": close,
    "exit": exit,
    "help": help
    """

commands = {
    "hello": hello,
    "add": add_contact,
    "change": change,
    "phone": phone,
    "show all": show_all,
    "good bye": close,
    "close": close,
    "exit": close,
    "help": help_instructions
}


def handler(string):
    pattern = "^hello|^add|^change|^phone|^show all|^good bye|^close|^exit|^help"
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


def main(contacts):
    good_bye = False
    print("Hello. Enter your command: ")
    while True:
        input_string = input("=> ")
        command, args = handler(input_string)
        func = commands.get(command)
        if command:
            print(func(args))
            if func.__name__ == "close":
                break


if __name__ == "__main__":
    contacts = {
        "Ivan": "+380501234567",
        "Roman": "+3805039876543"
    }
    main(contacts)
