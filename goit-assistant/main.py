import re

def hello(*args):
    print("How can I help you?")


def add_contact(*args):
    pass


def change(*args):
    pass


def phone(*args):
    pass


def show_all(*args):
    pass


def close(*args):
    print("Good bye!")
    return True



commands = {
    "hello": hello,
    "add": add_contact,
    "change": change,
    "phone": phone,
    "show_all": show_all,
    "good_bye": close,
    "close": close,
    "exit": close
}


def handler(string):
    string = string.lower()
    pattern = "^hello|^add|^change|^phone|^show all|^good bye|^close|^exit"
    try:
        command = re.search(pattern, string).group(0)
        args = re.sub(pattern, "", string).split()
    except ValueError:
        print("Command input error")
    except:
        command, args = None, None
        print("ERROR")
    return command, args


def main():
    good_bye = False
    while True:
        input_string = input("Hello. Enter your command: ")
        command, args = handler(input_string)
        func = commands.get(command)
        func(args)
        good_bye = close()
        if good_bye:
            break


if __name__ == "__main__":
    contacts = {
        "Ivan": "+380501234567",
        "Roman": "+3805039876543"
    }
    main()
