from className import Name
from classPhone import Phone
from classBirthday import Birthday
from datetime import datetime


class Record:
    """Клас Record представляє запис контакту в телефонній книзі.

    Attributes:
        self.name (Name): Ім'я контакту.
        self.phones (list of Phone): Список телефонних номерів контакту.
        self.birthday (Birthday): Дата народження контакту.

    Methods:
        days_to_birthday(): Повертає кількість днів до наступного дня народження контакту, якщо вказана дата народження.
        add_birthday(value): Додає дату народження контакту.
        edit_birthday(new_value): Змінює дату народження контакту.
        add_phone(phone): Додає телефонний номер контакту.
        remove_phone(phone): Видаляє телефонний номер контакту.
        edit_phone(old_phone, new_phone): Редагує існуючий телефонний номер контакту.
        find_phone(phone): Знаходить телефонний номер контакту за значенням номера.
        get_all_phones(): Повертає список всіх телефонних номерів контакту.
    """

    def __init__(self, name, birthday=None):
        """Ініціалізує новий об'єкт Record з ім'ям та датою народження (за бажанням)."""
        self.name = Name(name)
        self.phones = []
        self.birthday = Birthday(birthday) if birthday else None

    def days_to_birthday(self):
        """Повертає кількість днів до наступного дня народження контакту, якщо вказана дата народження.

                Returns:
                    int or None: Кількість днів до наступного дня народження, або None, якщо дата народження не вказана.
                """
        if self.birthday:
            today = datetime.now()
            # print(today)
            # print("1", self.birthday)
            # print( datetime.strptime(self.birthday, '%Y-%m-%d').replace(year=today.year))
            birthday = datetime.strptime(self.birthday, '%Y-%m-%d').replace(year=today.year)

            if today > birthday:
                birthday = birthday.replace(year=today.year + 1)

            delta = birthday - today
            # print("d", delta.days)
            return delta.days
        else:
            return None

    def add_birthday(self, value):
        """Додає дату народження контакту.

               Args:
                   value (str): Рядок з датою народження у форматі '%Y-%m-%d'.
               """
        self.birthday = value

    def edit_birthday(self, new_value):
        """Редагує дату народження контакту.

                Args:
                    new_value (str): Рядок з датою народження у форматі '%Y-%m-%d'.
                """
        if not new_value:
            self.birthday = None
        else:
            self.birthday = new_value

    def add_phone(self, phone):
        """Додає телефонний номер контакту.

        Args:
            phone (str): Телефонний номер для додавання.
        """
        if not isinstance(phone, Phone):
            phone = Phone(phone)
        self.phones.append(phone)

    def remove_phone(self, phone):
        """Видаляє телефонний номер контакту.

        Args:
            phone (str): Телефонний номер для видалення.
        """
        if phone in [p.value for p in self.phones]:
            self.phones = [p for p in self.phones if p.value != phone]

    def edit_phone(self, old_phone, new_phone):
        """Редагує існуючий телефонний номер контакту.

        Args:
            old_phone (str): Старий телефонний номер для редагування.
            new_phone (str): Новий телефонний номер.

        Raises:
            ValueError: Якщо старий телефонний номер не знайдено.
        """
        is_found_old_phone = False
        for i, p in enumerate(self.phones):
            if p.value == old_phone:
                self.phones[i] = Phone(new_phone)
                is_found_old_phone = True
        if not is_found_old_phone:
            raise ValueError('Phone not found')

    def find_phone(self, phone):
        """Знаходить телефонний номер контакту за значенням номера.

        Args:
            phone (str): Телефонний номер для пошуку.

        Returns:
            Phone or None: Знайдений телефоний номер або None, якщо не знайдено.
        """
        for p in self.phones:
            if p.value == phone:
                return p

    def get_all_phones(self):
        """Повертає список всіх телефонних номерів контакту.

        Returns:
            list of str: Список телефонних номерів контакту.
        """
        result = [p.value for p in self.phones]
        return result

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}, " \
               f"birthday: {self.birthday}"
