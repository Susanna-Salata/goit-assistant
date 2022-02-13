
def hello():
    print("How can I help you?")


def add_contact():
    pass


def change():
    pass


def phone():
    pass


def show_all():
    pass


def close():
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


def assistant():
    good_bye = False
    while True:
        command = input("Hello. Enter your command: ")
        func = commands.get(command)
        func()
        good_bye = close()
        if good_bye:
            break


if __name__ == "__main__":
    contacts = {
        "Ivan": "+380501234567",
        "Roman": "+3805039876543"
    }
    assistant()
