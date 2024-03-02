from collections import defaultdict
from datetime import datetime, timedelta


def get_birthdays_per_week(users):
    today = datetime.today().date()
    birthdays = defaultdict(list)
    res = ""

    for user in users:
        name = users[user].name.value
        if users[user].birthday is None or users[user].birthday.birthday is None:
            continue
        birthday = (users[user].birthday.birthday).date()
    
        birthday_this_year = birthday.replace(year=today.year)

        if birthday_this_year < today:
            birthday_this_year = birthday_this_year.replace(year=today.year + 1)

        delta_days = (birthday_this_year - today).days

        if delta_days < 7:
            day_of_week = birthday_this_year.weekday()
            if day_of_week >= 5:  # if it's weekend then move to Monday
                day_of_week = 0
            birthdays[day_of_week].append(name)
    days_of_week = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
    for i, day in enumerate(days_of_week):
        if birthdays[i]:
            res += f"{day}: {', '.join(birthdays[i])}\n"
    return res.strip()


from collections import UserDict
import re

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

class Name(Field):
    def __init__(self, value):
        if not self.validate_name(value):
            raise ValueError("Invalid name")
        super().__init__(value)

    def validate_name(self, value):
        return len(value) > 1

class Phone(Field):
    def __init__(self, value):
        if not self.validate_phone(value):
            raise ValueError("Invalid phone number")
        super().__init__(value)

    def validate_phone(self, value):
        return len(str(value)) == 10 and str(value).isdigit()
    
    def __repr__(self):
        return self.value

class Birthday:
    def __init__(self, birthday=None):
        self.birthday = None
        if birthday is not None:
            self.birthday = self.validate_birthday(birthday)

    def validate_birthday(self, birthday):
        if re.match(r'\d{2}.\d{2}.\d{4}', birthday):
            return datetime.strptime(birthday, '%d.%m.%Y')
        else:
            raise ValueError("Birthday must be in DD.MM.YYYY format")


class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None
        
    def add_birthday(self, birthday):
        self.birthday = Birthday(birthday)

    def add_phone(self, phone):
        new_phone = Phone(phone)
        self.phones.append(new_phone)

    def remove_phone(self, phone):
        self.phones = [p for p in self.phones if str(p) != str(phone)]

    def edit_phone(self, old_phone, new_phone):
        for i, phone in enumerate(self.phones):
            if str(phone) == str(old_phone):
                self.phones[i] = Phone(new_phone)
                break

    def find_phone(self, phone):
        for p in self.phones:
            if str(p) == str(phone):
                return p
        return None

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(str(p) for p in self.phones)}"


class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        return self.data.get(name)

    def delete(self, name):
        del self.data[name]

    def get_birthdays_per_week(self):
        return get_birthdays_per_week(dict(self.data))


def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except (ValueError, IndexError) as e:
            print(e)
            return "Give me name and phone please."
        except KeyError as e:
            print(e)
            return "Enter user name."
    return inner

def input_error_birthday(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except (ValueError, IndexError) as e:
            print(e)
            return "Give correct date please."
    return inner


@input_error
def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args

@input_error
def add_contact(args, book):
    name, phone = args
    record = Record(name)
    record.add_phone(phone)
    book.add_record(record)
    return "Contact added."

@input_error
def change_contact(args, book):
    name, phone = args
    record = book.find(name)
    if record:
        record.edit_phone(record.phones[0], phone)
        return "Contact updated."
    else:
        return "Contact not found."

@input_error
def show_phone(args, book):
    name = args[0]
    record = book.find(name)
    return record.phones[0] if record else "Contact not found."

@input_error_birthday
def add_birthday(args, book):
    name, birthday = args
    record = book.find(name)
    if record:
        record.add_birthday(birthday)
        return "Birthday added."
    else:
        return "Contact not found."

@input_error
def show_birthday(args, book):
    name = args[0]
    record = book.find(name)
    return record.birthday.birthday.strftime("%d.%m.%Y") if record and record.birthday else "Contact and birthday not found."

def birthdays(book):
    return book.get_birthdays_per_week()

def show_all(book):
    return "\n".join(f"{record.name}: {record.phones}" for name, record in book.data.items())


def main():
    book = AddressBook()
    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")
        command, *args = parse_input(user_input)

        if command in ["close", "exit"]:
            print("Good bye!")
            break
        elif command == "hello":
            print("How can I help you?")
        elif command == "add":
            print(add_contact(args, book))
        elif command == "change":
            print(change_contact(args, book))
        elif command == "phone":
            print(show_phone(args, book))
        elif command == "all":
            print(show_all(book))
        elif command == "add-birthday":
            print(add_birthday(args, book))
        elif command == "show-birthday":
            print(show_birthday(args, book))
        elif command == "birthdays":
            print(birthdays(book))
        else:
            print("Invalid command.")

if __name__ == "__main__":
    main()
