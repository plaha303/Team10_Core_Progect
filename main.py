import pickle
import difflib
import sort
import json
from classes import AddressBook, Name, Phone, Record, Birthday, Address, Email, Note, NoteBook

address_book = AddressBook()
notebook = NoteBook()


def input_error(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyError:
            return "Contact not found."
        except ValueError:
            return "Invalid input. Please enter name or phone number."  # LS -->
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
    name = Name(input("Enter the name: ").strip())  # LS -->

    rec: Record = address_book.get(str(name))
    if rec:
        return "Contact already exists. Use 'edit phone', 'edit birthday', etc., to modify the contact."

    phone_input = Phone(input("Enter the phone number: ").strip())

    birthday_input = input("Enter birthday in format 'DD.MM.YYYY' (or leave empty if not available): ")
    while birthday_input and not Record.is_valid_birthday_format(birthday_input):
        print("Incorrect birthday format. Please use the format DD.MM.YYYY.")
        birthday_input = input("Enter birthday in format 'DD.MM.YYYY' (or leave empty if not available): ")

    address_input = input("Enter the address, or leave empty: ")
    email_input = Email.input_correct_email(input("Enter the email, or leave empty: "))

    phone = Phone(phone_input) if phone_input else None
    birthday = Birthday(birthday_input) if birthday_input else None
    address = Address(address_input) if address_input else None
    email = Email(email_input) if email_input else None

    rec = Record(name, phone, birthday, address, email)
    address_book.add_record(rec)
    return f"Contact '{name}' successfully added."


def del_phone():
    name = Name(input("Enter the name: "))
    phone = Phone(input("Enter the phone number: ").strip())
    rec: Record = address_book.get(str(name))
    if rec:
        rec.del_phone(Phone(phone))  # LS -->
        return f"The phone number '{phone}' has been removed from the contact '{name}'."
    return f"No contact '{name}' in address book"


@input_error
def add_phone():
    name = Name(input("Enter the name: ").strip())
    rec: Record = address_book.get(str(name))
    if rec:
        phone_input = Phone(input("Enter the phone number: ").strip())

        new_phone = Phone(phone_input)
        rec.add_phone(new_phone)
        return f"Phone number '{new_phone}' added to contact '{name}'."
    return f"No contact '{name}' in the address book"


@input_error
def edit_phone():
    name = Name(input("Enter the name: ").strip())
    rec: Record = address_book.get(str(name))
    if rec:
        phone_input = Phone(input("Enter the phone number: ").strip())

        new_phone = Phone(phone_input)
        rec.add_phone(new_phone)
        return f"Phone number '{new_phone}' added to contact '{name}'."
    return f"No contact '{name}' in address book"


@input_error
def change_phone():
    name = Name(input("Enter the name: ").strip())
    old_phone = Phone(input("Enter the old phone number: ").strip())
    new_phone = Phone(input("Enter the new phone number: ").strip())

    rec: Record = address_book.get(str(name))
    if rec:
        rec.edit_phone(old_phone, new_phone)
        return f"The old phone number '{old_phone}' has been updated to '{new_phone}' for contact '{name}'."
    return f"No contact '{name}' in address book"


@input_error
def add_birthday():
    name = Name(input("Enter the name: ").strip())
    birthday = Birthday(input("Enter birthday in format 'DD.MM.YYYY': "))
    rec: Record = address_book.get(str(name))
    if rec:
        rec.birthday = birthday
        return f"Birthday updated for contact '{name}'."
    return f"No contact '{name}' in address book"


@input_error
def days_to_birthday():
    name = Name(input("Enter the name: ").strip())
    rec: Record = address_book.get(str(name))
    if rec and rec.birthday:
        days_left = rec.days_to_birthday()
        if days_left is not None:
            if days_left == 0:
                return f"Contact '{name}' birthday is today!"
            elif days_left == 1:
                return f"Contact '{name}' birthday is tomorrow!"
            return f"Contact '{name}' birthday is in '{days_left}' days."
        return f"Contact '{name}' birthday is today!"
    return f"The contact '{name}' is not found in the address book or the birthday is not specified."


@input_error
def edit_birthday():
    name = Name(input("Enter the name: ").strip())
    rec: Record = address_book.get(str(name))
    if rec:
        new_birthday = Birthday(input("Enter a new birthday (in DD.MM.YYYY format): "))
        rec.birthday = new_birthday
        return f"Birthday updated for contact '{name}'."
    return f"No contact '{name}' in address book"


def show_birthday_within_days():
    try:
        days = int(input("Enter the number of days to check: "))
    except ValueError:
        return "Invalid input. Please enter a valid number of days."

    birthday_contacts = []
    for name, record in address_book.data.items():
        if record.birthday and record.days_to_birthday() == days:
            birthday_contacts.append(record)

    if birthday_contacts:
        output = f"Contacts with birthdays {days} days from now:\n\n"
        for contact in birthday_contacts:
            contact_info = f"Name: {contact.name};" \
                           f" Phones: {', '.join(str(phone) for phone in contact.phones)};" \
                           f" Birthday: {contact.birthday};"
            output += f"{contact_info}\n"
        return output
    else:
        return f"No contacts have birthdays {days} days from now."


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
            birthday_info = f"birthday: {record.birthday.value};" if record.birthday else ""  # LS -->
            phones_info = f"phones: {' / '.join(str(phone) for phone in record.phones)};" if record.phones else ""
            address_info = f"address: {record.address.value};" if record.address else ""  # LS -->
            email_info = f"email: {record.email.value}." if record.email else ""  # LS -->
            print(f"Contact: name '{record.name}' {phones_info} {birthday_info} {address_info} {email_info}")  # LS -->

        print("\nPage:", page_number)
        print("Press Enter to see the next page or type 'exit' to return to the main menu.\n")
        user_input = input()

        if user_input.lower() == 'exit':
            break
        else:
            page_number += 1
    return "Continue...\n"


def search_by_name():
    name_query = input("Enter the name or part of the name to search: ").strip()
    results = address_book.search_by_name(name_query)
    if results:
        return "\n".join(str(record) for record in results)
    return "No contacts found for the given name."


def search_by_phone():
    phone_query = input("Enter the phone or part of the phone to search: ").strip()
    results = address_book.search_by_phone(phone_query)
    if results:
        return "\n".join(str(record) for record in results)
    return "No contacts found for the given phone."


def sort_directory():
    folder_path = input("Enter the folder path to sort: ")
    result = sort.sort_folder(folder_path)  
    return result


def add_note():
    text = input("Enter the note text: ")
    note = Note(text)
    notebook.add_note(note)
    return f"Note '{text}' added."


@input_error
def add_tag():
    attempts = 0
    while attempts < 3:
        note_text = input("Enter the note text: ")
        note = notebook.get_note_by_text(note_text)
        if note is None:
            attempts += 1
            print(f"Note with text '{note_text}' not found. Please try again.")
        else:
            break
    else:
        print("Failed to find the note. Exiting tag addition.")
        return

    tag = input("Enter the tag: ")
    notebook.add_tag_to_note(note_text, tag)
    result = f"Tag '{tag}' added to note with text '{note_text}'."
    return result


def change_note():
    text = input("Enter the note text: ")
    new_text = input("Enter the new note text: ")
    result = notebook.edit_note(text, new_text)
    return result


def del_note():
    text = input("Enter the note text: ")
    result = notebook.delete_note_by_text(text)
    return result


@input_error
def search_note_by_tag():
    while True:
        tag = input("Enter the tag to search for notes or type 'exit' to return to the main menu: ")
        if tag.lower() == 'exit':
            return
        notes_with_tag = notebook.search_notes_by_tag(tag)
        
        if len(notes_with_tag) == 0:
            print(f"No notes found with tag '{tag}'. Please try again or type 'exit' to return to the main menu.")
        else:
            result = []
            for note in notes_with_tag:
                result.append(f"Note: {note.text}")
            return "\n\n".join(result)


@input_error
def search_note():
    while True:
        search_word = input("Enter the word to search in notes or type 'exit' to try searching by tag: ")
        if search_word.lower() == 'exit':
            return
        notes_with_word = notebook.search_notes_by_word(search_word)
        
        if len(notes_with_word) == 0:
            print(f"No notes found containing the word '{search_word}'."
                  f" Please try again or type 'exit' to search by tag.")
        else:
            result = []
            for note in notes_with_word:
                result.append(f"Note: {note.text}")
            return "\n\n".join(result)


def show_notes():
    notes = notebook.get_notes()
    if len(notes) == 0:
        return "No notes found."
    
    result = []
    for note in notes:
        if len(note.tags) == 0:
            result.append(f"Note: {note.text}")
        else:
            result.append(str(note))
    
    return "\n\n".join(result)


def helper():
    commands = {
        hello: "hello -> displays a welcome message.",
        add_contact: "add -> adds a new contact.",
        add_birthday: " add birthday -> adds birthday to contact",
        add_note: "add note -> add a new note",
        add_tag: "add tag -> add a new tag to a note.",
        edit_birthday: "edit birthday -> changes the existing birthday value of a contact",
        days_to_birthday: "days to birthday -> shows how many days are left until the birthday",
        show_birthday_within_days: "show birthday -> display a list of contacts whose birthday is a specified number"
                                   " of days from the current date",
        edit_phone: "edit phone -> changes the phone number of an existing contact.",
        del_phone: "del phone -> delete number from contact.",
        del_note: "del note -> delete a note.",
        add_phone: "add phone -> adds phone to exist contact",
        change_phone: "change phone -> replaces the old number with a new one",
        change_note: "change note -> modify an existing note.", 
        show_all: "show all -> displays all contacts and their phone numbers.",
        show_notes: "show notes -> display all notes.",
        search_by_name: "search by name -> searches for contacts in which the name coincides",
        search_by_phone: "search by phone -> looking for contacts with a matching phone number",
        search_note_by_tag: "search note by tag -> search for a note with a tag.",
        search_note: "search note -> Search for a note in the text",
        sort_directory: "sort folder -> sorts files into categories,"
                        " removes empty folders in the folder path specified by the user",
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
    file_path_note = 'notebook.txt'
    try:
        with open(file_path_note, 'r') as file:
            notebook_data = json.load(file)
            notebook = NoteBook.from_dict(notebook_data)
    except (FileNotFoundError, json.JSONDecodeError):
        notebook = NoteBook()
        print("Failed to load the notebook. Starting with an empty notebook.")

    try:
        address_book.load_from_file(file_path)
    except pickle.UnpicklingError:
        print("Failed to load the address book. Starting with an empty address book.")

    print("\nWelcome!\n")
    commands = {
        "hello": hello,
        "add": add_contact,
        "add note": add_note,
        "add tag": add_tag,
        "change note": change_note,
        "del note": del_note,
        "search note": search_note,
        "search note by tag": search_note_by_tag,
        "show notes": show_notes,
        "add birthday": add_birthday,
        "edit birthday": edit_birthday,
        "show birthday": show_birthday_within_days,
        "days to birthday": days_to_birthday,
        "edit phone": edit_phone,
        "del phone": del_phone,
        "change phone": change_phone,
        "show all": show_all,
        "search by name": search_by_name,
        "search by phone": search_by_phone,
        "sort folder": sort_directory,
        "help": helper,
        "exit": exit,
        "good bye": exit,
        "close": exit
    }

    while True:
        command = input("\nEnter a command: ").lower().strip()

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
        with open(file_path_note, 'w') as file:
            json.dump(notebook.to_dict(), file)
            

if __name__ == "__main__":
    main()
