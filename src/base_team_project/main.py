

from commands import greetings, find_closest_command, get_command_input
from save_load_book import save_address_book, load_address_book
from memory import AddressBook, SetterValueIncorrect


def main():
    # Load the address book from storage, or create a new one if it doesn't exist
    work_book = load_address_book()
    if not work_book:
        work_book = AddressBook()
    print("Welcome to the Assistant bot! ")
    print(greetings())
    work_book.get_birthdays_per_week()
    while True:
        # Get user input for a command
        input_string = get_command_input("Enter a command: ")

        # parse input function that get back command or None
        command = find_closest_command(input_string)
        if command:
            try:
                cmd_func = command['func']
                if len(command['arguments']) > 0:
                    # Prompt the user to enter arguments for the command
                    print(
                        f'For {command.get("name")} please write {command.get("arguments")} splitted by comma.')
                    input_string = get_command_input("Enter arguments: ")
                    arguments = list(input_string.split(','))
                    result = cmd_func(work_book, *arguments)
                else:
                    result = cmd_func(work_book)
                if isinstance(result, list):
                    # Print each item in the result listc
                    for i in result:
                        print(i)
                else:
                    print(result) if result else None

                if command["name"] == 'ending':
                    break
            except SetterValueIncorrect as e:
                # Print the exception message if a SetterValueIncorrect exception is raised
                print(e.message)
        else:
            print("Sorry, i don't understand this your command. Please try again.")
    # Save the address book to storage
    save_address_book(work_book)


if __name__ == '__main__':
    main()
