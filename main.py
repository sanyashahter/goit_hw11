import re
from collections import UserDict
from datetime import date

class Field:
    def __init__(self):
        self._value = None

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_value):
        self._value = new_value

class AdressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    def show_all(self):
        for name, record in self.data.items():
            print(f"{name}")
            print(f"{record}")
            print()

    def __str__(self):
        return f'AdressBOOK = {str(self.data)}'

    def __iter__(self):
        return self

    def __next__(self):
        # Визначаємо розмір пакета записів для виведення
        package_size = 2

        if not hasattr(self, '_iter_index'):
            self._iter_index = 0

        if self._iter_index >= len(self.data):
            raise StopIteration

        start_index = self._iter_index
        end_index = min(start_index + package_size, len(self.data))

        records = list(self.data.values())[start_index:end_index]
        self._iter_index += package_size

        return records

class Name(Field):
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return f'Имя  === {str(self.value)}'

class Birthday(Field):
    def __init__(self, value):
        self.value = value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_value):
        # Перевірка на коректність дати народження за патерном
        pattern = r'^\d{2}\.\d{2}\.\d{4}$'
        if re.match(pattern, new_value):
            self._value = new_value
        else:
            raise ValueError("Некоректний формат дати народження")

    def to_date(self):
        date_split = self.value.split(".")
        a = int(date_split[2])
        b = int(date_split[1])
        c = int(date_split[0])
        return date(a, b, c)

    def days_to_birthday(self):
        if self.value is None:
            return None
        date2 = date.today()
        date_birthday = self.to_date()
        if date_birthday < date2:
            date_birthday = date(date2.year + 1, date_birthday.month, date_birthday.day)
        days_left = (date_birthday - date2).days
        return f'{days_left}'

class Phone(Field):
    def __init__(self, value):
        self.value = value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_value):
        # Перевірка на коректність номера телефону за патерном
        pattern = r'^\+?\d{1,3}[-.\s]?\(?\d{1,3}\)?[-.\s]?\d{1,4}[-.\s]?\d{1,4}[-.\s]?\d{1,9}$'
        if re.match(pattern, new_value):
            self._value = new_value
        else:
            raise ValueError("Некоректний формат номера телефону")

    def __repr__(self):
        return f'Телефон = {self.value}'

class Record:
    def __init__(self, name, phone, birthday=None):
        self.name = Name(name)
        self.phone = Phone(phone)
        self.birthday = Birthday(birthday)
        self.phones = []

    def add_phone(self, phone):
        phone = Phone(phone)
        self.phones.append(phone)
        print(f"Телефон {phone} добавлен в список телефонов")

    def days_to_birthday(self):
        if self.birthday.value is None:
            return None
        else:
            return self.birthday.days_to_birthday()

    def edit_phone(self, old_phone, new_phone):
        for i in self.phones:
            if i.value == old_phone:
                index = self.phones.index(i)
                self.phones[index] = Phone(new_phone)
                print(f"Старий номер телефона {old_phone} замінено на новий {new_phone}")

    def del_phone(self, phone):
        if phone in self.phones:
            self.phones.remove(phone)
        else:
            print("Такого телефона не існує")

    def __repr__(self):
        days_left = self.days_to_birthday()
        if days_left is None:
            return f'Дані про обліковий запис: ({repr(self.name)}, {repr(self.phone)})'
        return f'Дані про обліковий запис: ({repr(self.name)}, {repr(self.phone)}, до дня народження залишилося {days_left} днів)'

address_book = AdressBook()
record1 = Record("Саня", "+380962893087", "18.02.1987")
address_book.add_record(record1)
address_book.show_all()

for records in address_book:
    print(records)

