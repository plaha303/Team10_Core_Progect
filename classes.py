from collections import UserDict
from datetime import datetime
import pickle
import re

class Field:
    def __init__(self, value=None):
        self._value = value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_value):
        self.validate(new_value)
        self._value = new_value

    def validate(self, value):
        pass

    def __str__(self):
        return str(self._value)

    def __repr__(self):
        return str(self._value)


class Name(Field):
    def validate(self): # LS -->
        if not self or not isinstance(self, str): # LS -->
            raise ValueError("The name must be a non-empty string.")


class Phone(Field):
    
    def validate_phone(self: str):
        correct = ("(", ")", "-", " ")
        while len(self) != 0 or len(self) == 13 and self.startswith('+38'):
            for i in correct:
                self = self.replace(i, "")
            if len(self) == 13 and self.startswith('+38'):
                return self
            elif len(self) == 12 and self.startswith('38'):
                self = f"+{self}"
                return self
            elif len(self) == 10 and self.startswith('0'):
                self = f"+38{self}"
                return self
            else:
                self = Phone.validate_phone(input("Invalid phone number. Please enter a new number: ").strip())  
        return self


class Birthday(Field):
    def validate(self, value):
        if value:
            try:
                datetime.strptime(value, "%d.%m.%Y")
            except ValueError:
                raise ValueError("Incorrect birthday format. Please use the format DD.MM.YYYY")

    def to_datetime(self):
        if self._value:
            return datetime.strptime(self._value, "%d.%m.%Y")


class Address(Field):
    pass


class Email(Field):
    def input_correct_email(self):
        while len(self) != 0:
            def analize_email(self):
                pattern = r"(^[a-zA-Z0-9_.+-]{2,}@([a-zA-Z0-9-]{2,}\.[a-zA-Z0-9]+$|[a-zA-Z0-9-]{2,}\.[a-zA-Z0-9]+\.[a-zA-Z0-9]+$))"
                return re.match(pattern, self) is not None
            if analize_email(self) == True:
                return f"Good {self}"
            else:
                self = Email.input_correct_email(input("Invalid e-mail address. Enter the email, or leave empty: ")) #
            return self
        return self

class Note:
    def __init__(self, text, tags=[]):
        self.text = text
        self.tags = tags

    def add_tag(self, tag):
        if tag not in self.tags:
            self.tags.append(tag)

    def __str__(self):
        return self.text + " (Tags: " + ", ".join(self.tags) + ")"

    def __eq__(self, other):
        return self.text == other.text

class NoteBook:
    def __init__(self):
        self.notes = []

    def add_note(self, note):
        self.notes.append(note)

    def add_tag_to_note(self, text, tag):
        for note in self.notes:
            if note.text == text:
                note.add_tag(tag)
                return f"Tag '{tag}' added to note with text '{text}'."
        return f"Note with text '{text}' not found."

    def delete_note_by_text(self, text):
        for note in self.notes:
            if note.text == text:
                self.notes.remove(note)
                return f"Note with text '{text}' removed."
        return f"Note with text '{text}' not found."

    def edit_note(self, old_text, new_text):
        for note in self.notes:
            if note.text == old_text:
                note.text = new_text
                return f"Note updated from '{old_text}' to '{new_text}'."
        return f"Note with text '{old_text}' not found."
    
    def search_untagged_notes(self):
        results = [note for note in self.notes if not note.tags]
        return results
    
    def search_notes_by_tag(self, tag):
        results = [note for note in self.notes if tag in note.tags]
        return results

    def search_notes_by_tags(self, tags):
        results = [note for note in self.notes if all(tag in note.tags for tag in tags)]
        return results

    def to_dict(self):
        notes_data = [{'text': note.text, 'tags': note.tags} for note in self.notes]
        return {'notes': notes_data}

    @classmethod
    def from_dict(cls, data):
        notebook = cls()
        notes_data = data.get('notes', [])
        for note_data in notes_data:
            note = Note(note_data['text'], note_data['tags'])
            notebook.add_note(note)
        return notebook
    
    # def save_to_file(self, filename):
    #     with open(filename, 'wb') as file:
    #         pickle.dump(self, file)

    # @classmethod
    # def load_from_file(cls, filename):
    #     with open(filename, 'rb') as file:
    #         return pickle.load(file)

    def get_notes(self):
        return self.notes

    def __str__(self):
        return "\n".join(str(note) for note in self.notes)


class Record:
    def __init__(self, name: Name,
                 phone: Phone = None,
                 birthday: Birthday = None,
                 address: Address = None,
                 email: Email = None):
        self.name = name
        self.phones = []
        if phone:
            self.phones.append(phone)
        self.birthday = birthday
        self.address = address
        self.email = email

    def add_phone(self, phone=None, birthday=None):
        if phone and phone.value not in [p.value for p in self.phones]:
            self.phones.append(phone)
        if birthday:
            while not self.is_valid_birthday_format(birthday.value):
                print("Incorrect birthday format. Please use the format DD.MM.YYYY")
                birthday = Birthday(input("Enter birthday in format 'DD.MM.YYYY' (or leave empty if not available): "))
            if not self.birthday:
                self.birthday = birthday
            else:
                self.birthday.value = birthday.value

    def add_birthday(self, birthday: Birthday):
        self.birthday = birthday

    @staticmethod
    def is_valid_birthday_format(value):
        try:
            datetime.strptime(value, "%d.%m.%Y")
            return True
        except ValueError:
            return False

    def del_phone(self, phone: Phone):
        for p in self.phones:
            if p.value == phone.value:
                self.phones.remove(p)
                return f"phone {phone} removed from contact {self.name}"
        return f"{phone} not present in phones of contact {self.name}"

    def edit_phone(self, old_phone, new_phone):
        for idx, p in enumerate(self.phones):
            if old_phone == p.value: # LS -->
                self.phones[idx].value = new_phone # LS -->
                return f"old phone {old_phone} change to {new_phone}"
            return f"{old_phone} not present in phones of contact {self.name}"

    def days_to_birthday(self):
        if self.birthday:
            today = datetime.now()
            next_birthday = self.birthday.to_datetime().replace(year=today.year)
            if next_birthday < today:
                next_birthday = next_birthday.replace(year=today.year + 1)
            days_remaining = (next_birthday - today).days
            return days_remaining
        return None

    def __str__(self):
        phones_str = ", ".join(str(p) for p in self.phones)
        return f"Name: {self.name}, Phones: {phones_str}"


class AddressBook(UserDict):
    def add_record(self, record: Record):
        self.data[str(record.name)] = record
        return f"Contact {record} add success"

    def delete_record(self, name):
        del self.data[name]

    def edit_record(self, name, new_record):
        self.data[name] = new_record

    def search_records(self, **kwargs):
        results = []
        for record in self.data.values():
            match = True
            for key, value in kwargs.items():
                if key == "name":
                    if str(record.name).lower() != value.lower():
                        match = False
                        break
                elif key == "phone":
                    phone_match = False
                    for phone in record.phones:
                        if str(phone).lower() == value.lower():
                            phone_match = True
                            break
                    if not phone_match:
                        match = False
                        break
            if match:
                results.append(record)
        return results

    def search_by_name(self, name_query):
        results = []
        for record in self.data.values():
            if name_query.lower() in str(record.name).lower():
                results.append(record)
        return results

    def search_by_phone(self, phone_query):
        results = []
        for record in self.data.values():
            for phone in record.phones:
                if phone_query in str(phone):
                    results.append(record)
                    break
        return results

    def save_to_file(self, file_path):
        with open(file_path, 'wb') as f:
            pickle.dump(self.data, f)

    def load_from_file(self, file_path):
        try:
            with open(file_path, 'rb') as f:
                self.data = pickle.load(f)
        except FileNotFoundError:
            self.data = {}

    def iterator(self, batch_size, page_number):
        data_values = list(self.data.values())
        start_idx = page_number * batch_size
        end_idx = min((page_number + 1) * batch_size, len(data_values))
        return data_values[start_idx:end_idx]

    def __str__(self) -> str:
        return "\n".join(str(r) for r in self.data.values())
