

from src.commands import find_closest_command, get_command_input
from src.save_load_books import *
# AddressBook,SetterValueIncorrect,Name,Phone,Birthday,Address,Email
from src.memory import *
from src.notes_core import Notebook,Tag
from src.common_functions import STR_EPIC_ASSISTANT
from colorama import init


def start_work():
    # Initialize colorama
    init()

    # Load the address book from storage, or create a new one if it doesn't exist
    try:
        address_book = load_addressbook()
    except:
        print("Unfortunately, load address book failed")
    if not address_book:
        address_book = AddressBook()
    # Load the notes book from storage, or create a new one if it doesn't existя
    try:
        notes_book = load_notebook()
    except:
        print("Unfortunately, load  notebook failed")
    if not notes_book:
        notes_book = Notebook()
    print(STR_EPIC_ASSISTANT)
    address_book.get_birthdays_per_week()
    return (address_book, notes_book)



def command_exe(command=dict, adress_book=AddressBook, note_book=Notebook):
    cmd_func = command.get('func')
    if len(command.get('arguments')) > 0:
        # Prompt the user to enter arguments for the command
        args = []
        mes = f'For this command we need {str(command.get("arguments"))}'
        if command.get('name') == 'add new contact':
            mes += 'If you want to skip unimportant argument (email,address or birthday) write pass.'
        elif command.get('name') == 'change exist contact':
            mes += 'For second argument "changed field" write: "phone","email","birthday" or "address"'
        elif command.get('name') == 'edit note info':
            mes += 'For second argument "changed field" write: "title","tag" or "description"'
        print(mes)
        got_args = False
        i = 0
        while not got_args:
            f_arg = command.get("arguments")[i]
            if f_arg == 'name':
                f_class = Name
            elif f_arg == 'phone':
                f_class = Phone
            elif f_arg == 'birthday':
                f_class = Birthday
            elif f_arg == 'email':
                f_class = Email
            elif f_arg == 'address':
                f_class = Address
            elif f_arg == 'tag':
                f_class = Tag
            else:
                f_class = None
            args.append(get_command_input(
                f'Enter {f_arg}: ', check_class=f_class, need_comp=False,check_add_command=command, arg_number = i))
            if len(args) == len(command.get("arguments")):
                got_args = True
            else:
                i += 1
        try:
            return cmd_func(*args, a_book=adress_book, n_book=note_book)
        except SetterValueIncorrect as e:
            print(e.message + '\n Please try again this command or another one.')
            return None
    else:
        return cmd_func(a_book=adress_book, n_book=note_book)


def main():
    work_books = start_work()
    a_book = work_books[0]
    n_book = work_books[1]
    while True:
        # Get user input for a command
        input_string = get_command_input("Enter a command: ")
        # parse input function that get back command or None
        command = find_closest_command(input_string)
        if command:
            result = command_exe(command, a_book, n_book)
            if isinstance(result, list):
                # Print each item in the result listc
                for i in result:
                    print(i)
            else:
                print(result) if result else None
            # End of app
            if command["name"] == 'ending':
                break
        else:
            print("Sorry, i don't understand this your command. Please try again.")
    # Save the address book to storage
    try:
        save_addressbook(a_book)
        save_notebook(n_book)
    except:
        print("Unfortunately, save failed :(")


if __name__ == '__main__':
    main()
