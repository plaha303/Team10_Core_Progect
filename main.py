import pickle
import difflib

from classes import AddressBook, Name, Phone, Record, Birthday, Address, Email

address_book = AddressBook()


def input_error(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyError:
            return "Contact not found."
        except ValueError:
            return "Invalid input. Please enter name and phone number separated by a space."
        except IndexError:
            return "Invalid input. Please enter a command."
        except TypeError:
            return func()
    return wrapper


@input_error
def hello():
    return "How can I help you?"


@input_error
def add_contact():
    name = Name(input("Enter the name: "))

    rec: Record = address_book.get(str(name))
    if rec:
        return "Contact already exists. Use 'edit phone', 'edit birthday', etc., to modify the contact."

    phone_input = input("Enter the phone number (10 digits), or leave empty: ")
    while phone_input and (not phone_input.isdigit() or len(phone_input) != 10):
        print("Invalid phone number. Please enter a 10-digit number.")
        phone_input = input("Enter the phone number (10 digits), or leave empty: ")

    birthday_input = input("Enter birthday in format 'DD.MM.YYYY' (or leave empty if not available): ")
    while birthday_input and not Record.is_valid_birthday_format(birthday_input):
        print("Incorrect birthday format. Please use the format DD.MM.YYYY.")
        birthday_input = input("Enter birthday in format 'DD.MM.YYYY' (or leave empty if not available): ")

    address_input = input("Enter the address, or leave empty: ")
    email_input = input("Enter the email, or leave empty: ")

    phone = Phone(phone_input) if phone_input else None
    birthday = Birthday(birthday_input) if birthday_input else None
    address = Address(address_input) if address_input else None
    email = Email(email_input) if email_input else None

    rec = Record(name, phone, birthday, address, email)
    address_book.add_record(rec)
    return f"Contact {name} successfully added."


def del_phone():
    name = Name(input("Enter the name: "))
    phone = Phone(input("Enter the phone number: "))
    rec: Record = address_book.get(str(name))
    if rec:
        rec.del_phone(phone)
        return f"The phone number {phone} has been removed from the contact {name}."
    return f"No contact {name} in address book"


@input_error
def add_phone():
    name = Name(input("Enter the name: "))
    rec: Record = address_book.get(str(name))
    if rec:
        phone_input = input("Enter the new phone number (10 digits): ")
        while not phone_input.isdigit() or len(phone_input) != 10:
            print("Invalid phone number. Please enter a 10-digit number.")
            phone_input = input("Enter the new phone number (10 digits): ")

        new_phone = Phone(phone_input)
        rec.add_phone(new_phone)
        return f"Phone number {new_phone} added to contact {name}."
    return f"No contact {name} in the address book"


@input_error
def edit_phone():
    name = Name(input("Enter the name: "))
    rec: Record = address_book.get(str(name))
    if rec:
        phone_input = input("Enter the new phone number (10 digits): ")
        while not phone_input.isdigit() or len(phone_input) != 10:
            print("Invalid phone number. Please enter a 10-digit number.")
            phone_input = input("Enter the new phone number (10 digits): ")

        new_phone = Phone(phone_input)
        rec.add_phone(new_phone)
        return f"Phone number {new_phone} added to contact {name}."
    return f"No contact {name} in address book"


@input_error
def change_phone():
    name = Name(input("Enter the name: "))
    old_phone = Phone(input("Enter the old phone number: "))
    new_phone = Phone(input("Enter the new phone number: "))
    rec: Record = address_book.get(str(name))
    if rec:
        rec.edit_phone(old_phone, new_phone)
        return f"The old phone number {old_phone} has been updated to {new_phone} for contact {name}."
    return f"No contact {name} in address book"


@input_error
def add_birthday():
    name = Name(input("Enter the name: "))
    birthday = Birthday(input("Enter birthday in format 'DD.MM.YYYY': "))
    rec: Record = address_book.get(str(name))
    if rec:
        rec.birthday = birthday
        return f"Birthday updated for contact {name}."
    return f"No contact {name} in address book"


@input_error
def days_to_birthday():
    name = Name(input("Enter the name: "))
    rec: Record = address_book.get(str(name))
    if rec and rec.birthday:
        days_left = rec.days_to_birthday()
        if days_left is not None:
            if days_left == 0:
                return f"Contact {name} birthday is today!"
            elif days_left == 1:
                return f"Contact {name} birthday is tomorrow!"
            return f"Contact {name} birthday is in {days_left} days."
        return f"Contact {name} birthday is today!"
    return f"The contact {name} is not found in the address book or the birthday is not specified."


@input_error
def edit_birthday():
    name = Name(input("Enter the name: "))
    rec: Record = address_book.get(str(name))
    if rec:
        new_birthday = Birthday(input("Enter a new birthday (in DD.MM.YYYY format): "))
        rec.birthday = new_birthday
        return f"Birthday updated for contact {name}."
    return f"No contact {name} in address book"


@input_error
def show_all():
    page_number = 1
    batch_size = 5

    while True:
        records_batch = list(address_book.iterator(batch_size, page_number - 1))
        if not records_batch:
            print("No more contacts to display.")
            break

        for record in records_batch:
            birthday_info = f"Birthday: {record.birthday.value}" if record.birthday else ""
            phones_info = f"Phones: {', '.join(str(phone) for phone in record.phones)}"
            address_info = f"Address: {record.address.value}" if record.address else ""
            email_info = f"Email: {record.email.value}" if record.email else ""
            print(f"Name: {record.name}; {phones_info}; {birthday_info}; {address_info}; {email_info}")

        print("\nPage:", page_number)
        print("Press Enter to see the next page or type 'exit' to return to the main menu.")
        user_input = input()

        if user_input.lower() == 'exit':
            break
        else:
            page_number += 1


def search_by_name():
    name_query = input("Enter the name or part of the name to search: ")
    results = address_book.search_by_name(name_query)
    if results:
        return "\n".join(str(record) for record in results)
    return "No contacts found for the given name."


def search_by_phone():
    phone_query = input("Enter the phone or part of the phone to search: ")
    results = address_book.search_by_phone(phone_query)
    if results:
        return "\n".join(str(record) for record in results)
    return "No contacts found for the given phone."


def helper():
    commands = {
        hello: "hello -> displays a welcome message.",
        add_contact: "add -> adds a new contact.",
        add_birthday: " add birthday -> adds birthday to contact",
        edit_birthday: "edit birthday -> changes the existing birthday value of a contact",
        days_to_birthday: "days to birthday -> shows how many days are left until the birthday",
        edit_phone: "edit phone -> changes the phone number of an existing contact.",
        del_phone: "del phone -> delete number from contact.",
        add_phone: "add phone -> adds phone to exist contact",
        change_phone: "change phone -> replaces the old number with a new one",
        show_all: "show all -> displays all contacts and their phone numbers.",
        search_by_name: "search by name -> searches for contacts in which the name coincides",
        search_by_phone: "search by phone -> looking for contacts with a matching phone number",
        helper: "help -> displays the list of available commands.",
        exit: "exit, close, good bye -> exits the program."
    }
    help_text = "Available commands:\n"
    for command, description in commands.items():
        help_text += f"{description}\n"
    return help_text


def find_closest_command(text, commands):
    available_commands = list(commands.keys())
    closest_command = difflib.get_close_matches(text.lower(), available_commands, n=1)
    if closest_command and closest_command[0] != text.lower():
        return closest_command[0]
    return None


def main():
    file_path = 'address_book.pkl'

    try:
        address_book.load_from_file(file_path)
    except pickle.UnpicklingError:
        print("Failed to load the address book. Starting with an empty address book.")

    print("Welcome!")
    commands = {
        "hello": hello,
        "add": add_contact,
        "add birthday": add_birthday,
        "edit birthday": edit_birthday,
        "days to birthday": days_to_birthday,
        "edit phone": edit_phone,
        "del phone": del_phone,
        "change phone": change_phone,
        "show all": show_all,
        "search by name": search_by_name,
        "search by phone": search_by_phone,
        "help": helper,
        "exit": exit,
        "good bye": exit,
        "close": exit
    }

def test():
    pass


    while True:
        command = input("Enter a command: ").lower()

        closest_command = find_closest_command(command, commands)
        if closest_command:
            print(f"Did you mean '{closest_command}'")
        else:
            if command in commands:
                func = commands[command]
                print(func())
            else:
                print("Invalid command. Please try again.")

        address_book.save_to_file(file_path)


if __name__ == "__main__":
    main()
