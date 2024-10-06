from collections import UserDict
from typing import Optional


class PhoneValidation(Exception):
    def __init__(self, message: str = "Довжина телефонного номера повинна бути 10 символів.") -> None:
        self.message = message
        super().__init__(self.message)


class NameValidation(Exception):
    def __init__(self, message: str = "Довжина має бути хоча б 1 символ у форматі строки") -> None:
        self.message = message
        super().__init__(self.message)


class Field:
    def __init__(self, value: str):
        self.value = value

    def __str__(self) -> str:
        return str(self.value)


class Name(Field):
    def __init__(self, value: str):
        if self.validate(value):
            super().__init__(value)
        else:
            raise NameValidation()

    @staticmethod
    def validate(value: str) -> bool:
        return isinstance(value, str) and len(value) > 1


class Phone(Field):
    def __init__(self, value: str):
        if self.validate(value):
            super().__init__(value)
        else:
            raise PhoneValidation()

    @staticmethod
    def validate(value: str) -> bool:
        return len(value) == 10 and value.isdigit()


class Record:
    def __init__(self, name: str):
        self.name = Name(name)
        self.phones = []

    def add_phone(self, value: str) -> None:
        self.phones.append(Phone(value))

    def remove_phone(self, value: str) -> None:
        for phone in self.phones:
            if phone.value == value:
                self.phones.remove(phone)
                return
        raise ValueError(f"Phone number {value} not found.")

    def find_phone(self, value: str) -> Optional[Phone]:
        matching_phones = [
            phone for phone in self.phones if phone.value == value]
        return matching_phones[0] if matching_phones else None

    def edit_phone(self, old_value: str, new_value: str) -> None:
        if Phone.validate(new_value):
            self.remove_phone(old_value)
            self.add_phone(new_value)
        else:
            raise PhoneValidation()

    def __str__(self) -> str:
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"


class AddressBook(UserDict):
    def add_record(self, record: Record) -> None:
        self.data[record.name.value] = record

    def find(self, name: str) -> Optional[Record]:
        return self.data.get(name)

    def delete(self, name: str) -> None:
        if name in self.data:
            del self.data[name]
        else:
            raise ValueError(f"Record for {name} not found.")

    def __str__(self) -> str:
        return '\n'.join(str(record) for record in self.data.values())


# Приклад використання
if __name__ == "__main__":
    # Створення нової адресної книги
    book = AddressBook()

    # Створення запису для John
    john_record = Record("John")
    john_record.add_phone("1234567890")
    john_record.add_phone("5555555555")

    # Додавання запису John до адресної книги
    book.add_record(john_record)

    # Створення та додавання нового запису для Jane
    jane_record = Record("Jane")
    jane_record.add_phone("9876543210")
    book.add_record(jane_record)

    # Виведення всіх записів у книзі
    print(book)

    # Знаходження та редагування телефону для John
    john = book.find("John")
    john.edit_phone("1234567890", "1112223333")

    print(john)  # Виведення: Contact name: John, phones: 1112223333; 5555555555

    # Пошук конкретного телефону у записі John
    found_phone = john.find_phone("5555555555")
    print(f"{john.name}: {found_phone}")  # Виведення: John: 5555555555

    # Видалення запису Jane
    book.delete("Jane")
    print(book)  # Виведення: залишився лише запис для John
