import re


def hello(*args):
    return "How can I help you?"


def add_contact(*args):
    name = args[0][0]
    phone = args[0][1]
    contacts.update({name: phone})
    return f"{name}: {phone} was added"


def change(*args):
    name = args[0][0]
    phone = args[0][1]
    contacts.update({name: phone})
    return f"{name}: {phone} was updated"


def phone(*args):
    name = args[0]
    return contacts[name]


def show_all(*args):
    return contacts


def close(*args):
    return "Good bye!"


commands = {
    "hello": hello,
    "add": add_contact,
    "change": change,
    "phone": phone,
    "show all": show_all,
    "good bye": close,
    "close": close,
    "exit": close
}


def handler(string):
    pattern = "^hello|^add|^change|^phone|^show all|^good bye|^close|^exit"
    try:
        command = re.search(pattern, string, re.IGNORECASE).group(0)
        command = command.lower()
        args = re.sub(pattern, "", string, re.IGNORECASE).split()
    except ValueError:
        print("Command input error")
    except:
        command, args = None, None
        print("ERROR")
    return command, args


def main(contacts):
    good_bye = False
    print("Hello. Enter your command: ")
    while True:
        input_string = input("=> ")
        command, args = handler(input_string)
        func = commands.get(command)
        print(func(args))
        if func.__name__ == "close":
            break


if __name__ == "__main__":
    contacts = {
        "Ivan": "+380501234567",
        "Roman": "+3805039876543"
    }
    main(contacts)
