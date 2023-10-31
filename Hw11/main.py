"""hw_11"""
from field import Field
from classPhone import Phone
from className import Name
from classAddressBook import AddressBook
from classRecord import Record
from decorators.input_errors import input_errors
from sanitize_phone_nr import sanitize_phone_number

RED = "\033[91m"
GREEN = "\033[92m"
BLUE = "\033[94m"
YELLOW = "\033[43m"
PINK = "\033[95m"
RESET = "\033[0m"
#  ================================
book = AddressBook()

sanitize_phone_number = input_errors(sanitize_phone_number)


def greeting(*_):
    """Greet the user.

    Returns:
        str: A greeting message.
    """
    return "How can I help you?"


def good_bye(*_):
    """Bid farewell to the user.

    Returns:
        str: A farewell message.
    """
    return "Good bye!"


@input_errors
def add_contact(name, *phones):
    """Add a contact to the address book.

    Args:
        name (str): The name of the contact.
        *phones (str): One or more phone numbers to associate with the contact.

    Returns:
        str: A message indicating the result of the operation.
    """
    contact = book.find(name)
    if contact is None:
        contact = Record(name)
        book.add_record(contact)
    for phone in phones:
        sanitized_phone = sanitize_phone_number(phone)
        if sanitized_phone.isdigit():
            contact.add_phone(sanitized_phone)
            return f"{GREEN}Phone {phone} was added to {name}{RESET}"
        else:
            return f"{RED}Phone {phone} is not valid and not added to {name}{RESET}"


@input_errors
def change_contact(name, old_phone, phone):
    """Change the phone number associated with a contact.

        Args:
            name (str): The name of the contact.
            old_phone (str): The old phone number.
            phone (str): The new phone number.

        Returns:
            str: A message indicating the result of the operation.
        """
    if name in book.data:
        record = book.data[name]
        if old_phone in record.get_all_phones():
            record.edit_phone(old_phone, phone)
            return f"{GREEN} Contact {name}: {old_phone} was successfully changed!\n New data: {name}: {phone}{RESET}"
        else:
            return f"{RED}There is no number {phone} in {name} contact{RESET}"
    else:
        return f"{RED}There is no {name} contact!{RESET}"


@input_errors
def get_phone(name):
    """Retrieve the phone numbers associated with a contact.

        Args:
            name (str): The name of the contact.

        Returns:
            str: A message containing the contact's name and phone numbers.
        """
    if name in book.data:
        record = book.data[name]
        return f"{GREEN}{name} was found with phones - {'; '.join(record.get_all_phones())}{RESET}"
    else:
        return f"{RED}There is no contact with this name!{RESET}"


@input_errors
def showall(chunk_size=1):
    """Display all contacts in the address book.

        Returns:
            None
        """
    print(f"{BLUE}{'NAME':^15}{RESET} | {BLUE}{'PHONES':^15}{RESET} | {BLUE}{'BIRTHDAY':^15}{RESET}")
    print(f"_" * 48)

    records = list(book.values())
    num_records = len(records)
    i = 0
    while i < num_records:
        chunk = records[i:i + chunk_size]
        for record in chunk:
            name = record.name.value
            phones = "; ".join([str(phone) for phone in record.phones])
            birthday = str(record.birthday) if record.birthday else "N/A"
            print(f"{BLUE}{name:<15}{RESET} | {BLUE}{phones:^15}{RESET} | {BLUE}{birthday:^15}{RESET}")
        i += chunk_size

        if i < num_records:
            # Wait for Enter keypress to continue
            input(f"{PINK}Press Enter to show the next chunk...{RESET}")


@input_errors
def days_to_birthday(name):
    """Calculate the number of days to the next birthday for a contact.

    Args:
        name (str): The name of the contact.

    Returns:
        str: A message indicating the number of days to the next birthday or an error message.
    """
    contact = book.find(name)
    print(f"{YELLOW}{contact}{RESET}")

    if contact is None:
        return f"{RED}There is no contact with the name '{name}'{RESET}"

    if contact.birthday:
        days = contact.days_to_birthday()
        print(days)
        if days > 0:
            return f"{GREEN}{name} has {days} days before their next birthday{RESET}"
        elif days == 0:
            return f"{GREEN}{name}'s birthday is today!{RESET}"
        else:
            # will never be executed.... because of Record class....
            return f"{GREEN}{name}'s birthday is in {-days} days{RESET}"
    else:
        return f"{RED}{name} has no birthday set{RESET}"


@input_errors
def add_birthday(name, date):
    contact = book.find(name)

    if contact is None:
        return f"{RED}There is no contact with the name '{name}'{RESET}"
    elif contact.birthday:
        return f"{RED}If you want to change {name}'s birthday, use 'edit-birthday <new value>'{RESET}"
    else:
        contact.add_birthday(date)
        return f"{GREEN} Was update {name}'s birthday date{RESET}"


@input_errors
def edit_birthday(name, date):
    contact = book.find(name)

    if contact is None:
        return f"{RED}There is no contact with the name '{name}'{RESET}"
    else:
        contact.edit_birthday(date)
        return f"{GREEN} Was update {name}'s birthday date{RESET}"


known_commands = ("add", "change", "phone", "show", "hello")
exit_commands = ("goodbye", "close", "exit", ".")


def main():
    """Main function for user interaction.

        Returns:
            None
        """
    while True:
        input_text = input("... ")
        input_command = (input_text.split()[0].lower())
        input_data = input_text.split()
        if input_command in exit_commands:
            print(f"{RED} Goodbye!{RESET}")
            break
        elif input_command in known_commands:
            if input_command == "hello":
                print(f"{BLUE} {greeting()} {RESET}")
            elif input_command == "add":
                try:
                    print(add_contact(input_data[1], input_data[2]))
                except IndexError:
                    print(f"{RED}You have to put name and phone after add. Example: \nadd <name> <phone>{RESET}")
            elif input_command == "change":
                if len(input_data) < 4:
                    print(
                        f"{RED}You have to put name, old phone, and new phone after change. Example: \nchange <name> "
                        f"<old_phone> <new_phone>{RESET}")
                else:
                    print(change_contact(input_data[1], input_data[2], input_data[3]))
            elif input_command == "phone":
                print(get_phone(input_data[1]))
            elif "show" in input_text:
                try:
                    showall(int(input_data[1]))
                except IndexError:
                    print(f"{RED}You have to put correct chunk size. Example: \nshow <chunk size>{RESET}")
        elif input_command == "days-to-birthday":
            if len(input_data) < 2:
                # noinspection LongLine
                print(
                    f"{RED}You need to provide a name after 'days-to-birthday'. "
                    f"Example: days-to-birthday <name>{RESET}"
                )
            else:
                print(days_to_birthday(input_data[1]))
        elif input_command == "add-birthday":
            if len(input_data) < 3:
                print(f"{RED}You need to provide a name and birthday date after 'add-birthday'.{RESET}")
                print(f"{RED}Example: \nadd-birthday <name> <YYYY-MM-DD>{RESET}")
            else:
                add_birthday(input_data[1], input_data[2])
        elif input_command == "edit-birthday":
            if len(input_data) < 3:
                print(f"{RED}You need to provide a name and birthday date after 'add-birthday'.{RESET}")
                print(f"{RED}Example: \nedit-birthday <name> <YYYY-MM-DD>{RESET}")
            else:
                edit_birthday(input_data[1], input_data[2])
        else:
            print(f"{RED}Don't know this command{RESET}")


if __name__ == "__main__":
    main()
