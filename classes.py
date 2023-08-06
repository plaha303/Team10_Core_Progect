from collections import UserDict
from datetime import datetime
import pickle


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
    def validate(self, value):
        if not value or not isinstance(value, str):
            raise ValueError("The name must be a non-empty string.")


class Phone(Field):
    def validate(self, value):
        if not value.isdigit() or len(value) != 10:
            raise ValueError("Invalid phone number. Please enter a 10-digit number.")


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
    pass


class Note:
    def __init__(self, text, tag=None):
        self.text = text
        self.tag_list = [HashTag(tag)] if tag else []

    def add_tag(self, tag):
        tag_obj = HashTag(tag)
        if tag_obj not in self.tag_list:
            self.tag_list.append(tag_obj)
            self.tag_list.sort(key=lambda x: x.tag)

    def __repr__(self) -> str:
        return str(self.text)

    def __eq__(self, other):
        return self.text == other.text
    
    @staticmethod
    def from_string(string):
        text, *tags = string.strip().split(';')
        note = Note(text)
        for tag in tags:
            note.add_tag(tag) 
        return note

    def to_string(self):
        return f"{self.text};{';'.join([tag.tag for tag in self.tag_list])}"

    
class HashTag:
    def __init__(self, tag):
        self.tag = tag

    def __eq__(self, other):
        return self.tag == other.tag

    def __repr__(self):
        return f"#{self.tag}"


class NotePad:
    def __init__(self):
        self.note_list = []

    def add_note(self, note):
        self.note_list.append(note)

    def change_note(self, note, new_text):
        for rec in self.note_list:
            if note == rec:
                rec.text = new_text

    def delete(self, note):
        if note in self.note_list:
            self.note_list.remove(note)
        else:
            print("Note not found in notebook")

    def search_by_tag(self, tag):
        tag_obj = HashTag(tag)
        return [note for note in self.note_list if tag_obj in note.tag_list]

    def sorting(self):
        self.note_list.sort(key=lambda note: len(note.tag_list), reverse=True)

    def save_to_file(self, filename):
        with open(filename, 'w') as file:
            for note in self.note_list:
                file.write(note.to_string() + '\n')

    def load_from_file(self, filename):
        self.note_list.clear()
        with open(filename, 'r') as file:
            for line in file:
                note = Note.from_string(line.strip())
                self.note_list.append(note)


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
            if old_phone.value == p.value:
                self.phones[idx] = new_phone
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
