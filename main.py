import pickle
import difflib
import sort
import re
from classes import AddressBook, Name, Phone, Record, Birthday, Address, Email, Note, NotePad, HashTag, datetime
from datetime import timedelta

address_book = AddressBook()
notebook = NotePad()


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

def show_birthday_within_days():
    try:
        days = int(input("Enter the number of days to check: "))
    except ValueError:
        return "Invalid input. Please enter a valid number of days."

    today = datetime.now()
    target_date = today + timedelta(days=days)
    
    birthday_contacts = []
    for name, record in address_book.data.items():
        if record.birthday:
            birth_date = record.birthday.to_datetime().replace(year=today.year)
            if birth_date.date() == target_date.date():
                birthday_contacts.append(record)

    if birthday_contacts:
        output = f"Contacts with birthdays {days} days from now ({target_date.strftime('%d.%m')}):\n\n"
        for contact in birthday_contacts:
            contact_info = f"Name: {contact.name}; Phones: {', '.join(str(phone) for phone in contact.phones)}; Birthday: {contact.birthday};"
            output += f"{contact_info}\n"
        return output
    else:
        return f"No contacts have birthdays {days} days from now ({target_date.strftime('%d.%m')})."


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

def sort_directory():
    folder_path = input("Enter the folder path to sort: ")
    result = sort.sort_folder(folder_path)  # виклик функції сортування з модуля sortfolder
    return result

@input_error
def add_note(*args):
    global notebook
    text = ' '.join(args)
    if not text:
        raise ValueError("enter the note text")
    record = Note(text)
    notebook.add_note(record)
    return "Note added"
    

@input_error
def add_tag(note, tag):
    global notebook
    if not tag:
        raise ValueError("Enter  first_letters_of_the_note... #tag")
    rec = quick_note(notebook, note)
    rec.add_tag(tag)
    notebook.sorting()
    return f'Tag "{tag}" added to record "{rec}"'

@input_error
def change_note(*args):
    global notebook
    text = ' '.join(args)
    if not text:
        raise ValueError("enter part of the note text")
    old_note, new_note = text.split("... ")
    record = quick_note(notebook, old_note)
    if record in notebook.note_list:
        notebook.change_note(record, new_note)
        return f'"{old_note}" changed to "{new_note}"'
    return f'Record "{record}" not found'

@input_error
def del_note(*args):
    global notebook
    text = ' '.join(args)
    if not text:
        raise ValueError("enter part of note text or #tag")
    record = quick_note(notebook, text)
    if record in notebook.note_list:
        notebook.delete(record)
        notebook.sorting()
        return f'"{record}" deleted successfully'
    return f'Record "{record}" not found'

@input_error
def search_note(*args):
    global notebook
    if not notebook.note_list:
        raise ValueError("No notes available")
        
    text = ' '.join(args).replace("...", "")
    list_of_notes = [note for note in notebook.note_list if text in str(note)]
    output = f"Found notes for {text}\n" + f'{", ".join(str(note) for note in list_of_notes)}'
    return output if list_of_notes else "Record not found"


    # text = ' '.join(args).replace("...", "")
    # list_of_notes = []
    # error = "Record not found"
    # for note in notebook.note_list:
    #     if text in str(note):
    #         list_of_notes.append(note)
    # output = (
    #     f"Found notes for {text}"
    #     + "\n"
    #     + f'{", ".join(str(note) for note in list_of_notes)}'
    # )
    # return output if len(list_of_notes) != 0 else error

def show_notes(*args):
    global notebook
    if not notebook.note_list:
        raise ValueError("No notes available")
        
    line = "".join(f'{", ".join(str(tag) for tag in note.tag_list)} Content: {str(note)}\n' for note in notebook.note_list)
    return "list of notes\n" + line + "end of list of notes"

    # line = ""
    # for note in notebook.note_list:
    #     tags = ", ".join(str(tag) for tag in note.tag_list)
    #     line += (
    #         f'{tags} Content: {str(note)}'
    #         + "\n"
    #     )
    # return "list of notes\n" + line + "end of list of notes"

def quick_tag(text: str):
    global notebook
    for note in notebook.note_list:
        for tag in note.tag_list:
            if str(text) in str(tag):
                return note
    return None

def quick_note(text: str):
    global notebook
    content = text.replace("...", "")
    for note in notebook.note_list:
        if content in str(note):
            return note
    return None 


def helper():
    commands = {
        hello: "hello -> displays a welcome message.",
        add_contact: "add -> adds a new contact.",
        add_birthday: " add birthday -> adds birthday to contact",
        add_note: "add note -> add a new note",
        add_tag: "add tag -> add a new tag to a note.",
        edit_birthday: "edit birthday -> changes the existing birthday value of a contact",
        days_to_birthday: "days to birthday -> shows how many days are left until the birthday",
        show_birthday_within_days: "show birthday -> display a list of contacts whose birthday is a specified number of days from the current date",
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
        search_note: "search note -> search for a note.",
        sort_directory: "sort folder -> sorts files into categories, removes empty folders in the folder path specified by the user",
        quick_tag: "quick tag -> find a note by tag.",
        quick_note: "quick note -> find a note by content.",
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


@input_error
def input_correct_phone():
    while True:
        phone = input()
        correct = ("(", ")", "-", " ")
        for i in correct:
            phone = phone.replace(i, "")
        if len(phone) == 13 and phone.startswith('+38'):
            return phone
        elif len(phone) == 12 and phone.startswith('38'):
            phone = f"+{phone}"
            return phone
        elif len(phone) == 10 and phone.startswith('0'):
            phone = f"+38{phone}"
            return phone
        else:
            raise ValueError("Invalid phone number") 
    

@input_error
def input_correct_email():
    email=input()
    def analize_email(email):
        pattern = r"([a-zA-Z0-9_.+-]{2,}+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.])"
        return re.match(pattern, email) is not None
    if analize_email(email) == True:
         return f"Good {email}"
    else:
         print("Invalid e-mail address")
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
        "add note": add_note,
        "add tag": add_tag,
        "change note": change_note,
        "del note": del_note,
        "search note": search_note,
        "show notes": show_notes,
        "quick tag": quick_tag,
        "quick note": quick_note,
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
