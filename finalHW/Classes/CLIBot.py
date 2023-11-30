from Classes.Record import Record
from Classes.AddressBook import AddressBook
from decorators.input_errors import input_errors
from Utils.sanitize_phone_nr import sanitize_phone_number

# I'm applying the decorator directly, overwriting the function
sanitize_phone_number = input_errors(sanitize_phone_number)

RED = "\033[91m"
GREEN = "\033[92m"
BLUE = "\033[94m"
YELLOW = "\033[43m"
PINK = "\033[95m"
RESET = "\033[0m"


#  ================================

class Bot:
    def __init__(self):
        self.__known_commands = (
            "add", "change", "phone", "find",
            "show", "hello", "days-to-birthday", "add-birthday", "edit-birthday")
        self.__exit_commands = ("goodbye", "close", "exit", ".")
        self.book = self.load_address_book()

    @staticmethod
    def load_address_book():
        try:
            return AddressBook.load_from_file('outputs/address_book.json')
        except (FileNotFoundError, EOFError) as e:
            print(f"{RED}Error loading address book: {e}{RESET}")
            print(f"{YELLOW}Creating a new address book.{RESET}")
            return AddressBook()  # Creating a new instance

    @staticmethod
    def greeting():
        """Greet the user.

        Returns:
            str: A greeting message.
        """
        return "How can I help you?"

    @staticmethod
    def good_bye():
        """Bid farewell to the user.

        Returns:
            str: A farewell message.
        """
        return "Good bye!"

    @input_errors
    def add_contact(self, name, *phones):
        """Add a contact to the address book.

        Args:
            name (str): The name of the contact.
            *phones (str): One or more phone numbers to associate with the contact.

        Returns:
            str: A message indicating the result of the operation.
        """
        contact = self.book.find_name(name)
        if contact is None:
            contact = Record(name)
            self.book.add_record(contact)
        for phone in phones:
            sanitized_phone = sanitize_phone_number(phone)
            if sanitized_phone.isdigit():
                contact.add_phone(sanitized_phone)
            else:
                return f"{RED}Phone {phone} is not valid and not added to {name}{RESET}"
        self.book.save_to_file('outputs/address_book.json')
        return f"{GREEN}Contact {name} was added successfully!{RESET}"

    @input_errors
    def change_contact(self, name, old_phone, phone):
        """Change the phone number associated with a contact.

            Args:
                name (str): The name of the contact.
                old_phone (str): The old phone number.
                phone (str): The new phone number.

            Returns:
                str: A message indicating the result of the operation.
            """
        if name in self.book.data:
            record = self.book.data[name]
            if old_phone in record.get_all_phones():
                record.edit_phone(old_phone, phone)
                # Save the address book to a file after making the change
                self.book.save_to_file('outputs/address_book.json')
                return (f"{GREEN} Contact {name}: {old_phone} was successfully changed!\n "
                        f"New data: {name}: {phone}{RESET}")
            else:
                return f"{RED}There is no number {phone} in {name} contact{RESET}"
        else:
            return f"{RED}There is no {name} contact!{RESET}"

    @input_errors
    def showall(self, chunk_size=1):
        """Display all contacts in the address book.

            Returns:
                None
            """
        print(f"{BLUE}{'NAME':^15}{RESET} | {BLUE}{'PHONES':^15}{RESET} | {BLUE}{'BIRTHDAY':^15}{RESET}")
        print("_" * 48)

        records = list(self.book.values())
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
    def get_phone(self, name):
        """Retrieve the phone numbers associated with a contact.

            Args:
                name (str): The name of the contact.

            Returns:
                str: A message containing the contact's name and phone numbers.
            """
        if name in self.book.data:
            record = self.book.data[name]
            return f"{GREEN}{name} was found with phones - {'; '.join(record.get_all_phones())}{RESET}"
        else:
            return f"{RED}There is no contact with this name!{RESET}"

    @input_errors
    def days_to_birthday(self, name):
        """Calculate the number of days to the next birthday for a contact.

        Args:
            name (str): The name of the contact.

        Returns:
            str: A message indicating the number of days to the next birthday or an error message.
        """
        contact = self.book.find_name(name)
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
    def add_birthday(self, name, date):
        contact = self.book.find_name(name)

        if contact is None:
            return f"{RED}There is no contact with the name '{name}'{RESET}"
        elif contact.birthday:
            return f"{RED}If you want to change {name}'s birthday, use 'edit-birthday <new value>'{RESET}"
        else:
            contact.add_birthday(date)
            # Save the address book to a file after adding the birthday
            self.book.save_to_file('outputs/address_book.json')
            return f"{GREEN} Was update {name}'s birthday date{RESET}"

    @input_errors
    def edit_birthday(self, name, date):
        contact = self.book.find_name(name)

        if contact is None:
            return f"{RED}There is no contact with the name '{name}'{RESET}"
        else:
            contact.edit_birthday(date)
            # Save the address book to a file after editing the birthday
            self.book.save_to_file('outputs/address_book.json')
            return f"{GREEN} Was update {name}'s birthday date{RESET}"

    known_commands = (
        "add", "change", "phone",
        "show", "hello", "find",
        "edit-birthday", "add-birthday", "days-to-birthday",)
    exit_commands = ("goodbye", "close", "exit", ".")

    def run(self):
        """Main function for user interaction.

               Returns:
                   None
               """
        try:
            book = AddressBook.load_from_file('outputs/address_book.json')
        except (FileNotFoundError, EOFError) as e:
            print(f"{RED}Error loading address book: {e}{RESET}")
            print(f"{YELLOW}Creating a new address book.{RESET}")
            book = AddressBook()  # Creating a new instance

        while True:
            user_input = input("... ")
            if user_input == "":
                print(f"{RED}Empty input !!!{RESET}")
                continue
            input_data = user_input.split()
            input_command = input_data[0].lower()
            if input_command in self.__exit_commands:
                print(f"{RED}{self.good_bye()}{RESET}")
                break
            elif input_command in self.__known_commands:
                match input_command:
                    case 'hello':
                        print(f"{BLUE}{self.greeting()} {RESET}")
                    case 'add':
                        try:
                            print(self.add_contact(input_data[1], input_data[2]))
                        except IndexError:
                            print(f"{RED}You have to put name and phone after add. Example: \n"
                                  f"add <name> <phone>{RESET}")
                    case "change":
                        if len(input_data) < 4:
                            print(
                                f"{RED}You have to put name, old phone, and new phone after change. "
                                f"Example: \nchange <name> "
                                f"<old_phone> <new_phone>{RESET}")
                        else:
                            print(self.change_contact(input_data[1], input_data[2], input_data[3]))
                    case "show":
                        try:
                            self.showall(int(input_data[1]))
                        except IndexError:
                            print(f"{RED}You have to put correct chunk size. Example: \nshow <chunk size>{RESET}")

                    case "phone":
                        print(self.get_phone(input_data[1]))
                    case "days-to-birthday":
                        if len(input_data) < 2:
                            print(
                                f"{RED}You need to provide a name after 'days-to-birthday'. "
                                f"Example: days-to-birthday <name>{RESET}"
                            )
                        else:
                            print(self.days_to_birthday(input_data[1]))
                    case "add-birthday":
                        if len(input_data) < 3:
                            print(f"{RED}You need to provide a name and birthday date after 'add-birthday'.{RESET}")
                            print(f"{RED}Example: \nadd-birthday <name> <YYYY-MM-DD>{RESET}")
                        else:
                            self.add_birthday(input_data[1], input_data[2])
                    case "edit-birthday":
                        if len(input_data) < 3:
                            print(f"{RED}You need to provide a name and birthday date after 'add-birthday'.{RESET}")
                            print(f"{RED}Example: \nedit-birthday <name> <YYYY-MM-DD>{RESET}")
                        else:
                            self.edit_birthday(input_data[1], input_data[2])
                    case "find":
                        try:
                            search_param = input_data[1]
                            result = book.find(search_param)
                            print(f"{GREEN}Matching records:\n{result}{RESET}")
                        except IndexError:
                            print(f"{RED}You have to provide a search parameter after 'find'.{RESET}")

            else:
                print(f"{RED}Don't know this command{RESET}")
