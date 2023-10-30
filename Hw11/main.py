"""hw_10"""
from field import Field
from className import Name
from classPhone import Phone
from classRecord import Record
from classAddressBook import AddressBook
from decorators.input_errors import input_errors
from sanitize_phone_nr import sanitize_phone_number


RED = "\033[91m"
GREEN = "\033[92m"
BLUE = "\033[94m"
YELLOW = "\033[43m"
RESET = "\033[0m"
#  ================================
book = AddressBook()

sanitize_phone_number = input_errors(sanitize_phone_number)
    
def greeting(*_):
    """greeting"""
    return "How can I help you?"

def good_bye(*_):
    """farewell"""
    return "Good bye!"


@input_errors
def add_contact(name, *phones):
    """add contact to dict"""
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
    if name in book.data:
        record = book.data[name]
        return f"{GREEN}{name} was found with phones - {'; '.join(record.get_all_phones())}{RESET}"
    else:
        return f"{RED}There is no contact with this name!{RESET}"
@input_errors
def showall():
    print(f"{BLUE}{'NAME':^15}{RESET} | {BLUE}{'PHONES':^15}{RESET}")
    print(f"_" * 30)
    for record in book.values():
        phones = "; ".join([str(phone) for phone in record.phones])
        print(f"{BLUE}{record.name.value:<15}{RESET} | {BLUE}{phones:^15}{RESET}")

known_commands = ("add", "change", "phone", "show","hello")
exit_commands = ("goodbye", "close", "exit", ".")


def main():
    

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
                    print(f"{RED}You have to put name, old phone, and new phone after change. Example: \nchange <name> <old_phone> <new_phone>{RESET}")
                else:
                    print(change_contact(input_data[1], input_data[2], input_data[3]))
            elif input_command == "phone":
                print(get_phone(input_data[1]))
            elif "show" in input_text:
                showall()
        else:
            print(f"{RED}Don't know this command{RESET}")

if __name__ == "__main__":
    main()


