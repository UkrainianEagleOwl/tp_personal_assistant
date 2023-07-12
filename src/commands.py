

import difflib
from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter
from colorama import Fore,Style
from prettytable import PrettyTable
from src.common_functions import STR_EPIC_COMMANDS
from src.memory import Record,SetterValueIncorrect,AddressBook,Phone
from src.notes_core import *
from src.sorter import sort_files_in_this_path

CHECK_SECOND_ARG_CHANGE_CONTACT = ("phone","email","birthday","address")
CHECK_SECOND_ARG_CHANGE_NOTE = ("title","tag","description")

def get_command_input_agree(Input_message=''):
    Input_value = None
    while True:
        Input_value = prompt(Input_message)
        if (Input_value.lower() == 'yes') or (Input_value.lower() == 'no'):
            return Input_value
        else:
            print("You can write only 'yes' or 'no'!")

def get_command_input(Input_message='',check_class = None,need_comp = True, check_add_command = None, arg_number = None):
    Input_value = None
    while True:
        if need_comp:
            Input_value = prompt(Input_message, completer=completer)
        else:
            Input_value = prompt(Input_message)
        if Input_value == 'pass':
            Input_value = None
        if check_class:
            try:
                check_obj = check_class(Input_value)
            except SetterValueIncorrect as e:
                print(e.message)
            else:
                break
        elif check_add_command and (arg_number == 1):
            if check_add_command["name"] == "change exist contact":
                if Input_value in CHECK_SECOND_ARG_CHANGE_CONTACT:
                    break
                else:
                    print(f'You can write only {CHECK_SECOND_ARG_CHANGE_CONTACT}')
            elif check_add_command["name"] == 'edit note info':
                if Input_value in CHECK_SECOND_ARG_CHANGE_NOTE:
                    break
                else:
                    print(f'You can write only {CHECK_SECOND_ARG_CHANGE_NOTE}')
            elif Input_value:
                break
        elif Input_value:
            break
    return Input_value

#Функція find_closest_command(user_input) знаходить найближчу команду до введеної користувачем, за допомогою алгоритму Левенштейну.
def find_closest_command(user_input):
    cmd = None
    closest_command = difflib.get_close_matches(user_input, input_variants, n=1)
    if closest_command:
        closest_command = closest_command[0]
        for command_dict in commands:
            if closest_command in command_dict["input view"]:
                cmd = command_dict
        if cmd:
            return cmd
        else:
            return None
    else:
        return None

def input_error(func):
    def wrapper(*arg,a_book = AddressBook,n_book = Notebook):
        try:
            result = func(*arg,a_book = a_book,n_book = n_book)
            return result
        except KeyError:
            print( Fore.RED + "The contact is missing. Please try again" + Style.RESET_ALL)
        except IndexError:
            print(Fore.RED + "The contact is missing. Please try again" + Style.RESET_ALL) 
        except ValueError:
            print(Fore.RED + "ValueError. Please try again." + Style.RESET_ALL)
    return wrapper    
        
def greetings(*arg,a_book = AddressBook,n_book = Notebook):
    return "Hello. How i can help you?"

@input_error
def add_new_contact(*arg,a_book = AddressBook,n_book = Notebook):
    rec = Record(name=arg[0].capitalize(),phone=arg[1],birthday=arg[2],email=arg[3],address=arg[4])
    a_book.add_record(rec)
    while True:
        input_bool = get_command_input("Do you want to add more phone numbers? Write Yes or No: ",need_comp = False)
        if input_bool.lower() == 'yes':
            new_phone = get_command_input("Enter additional phone: ", Phone ,need_comp = False)
            rec.add_phone(new_phone)
        elif input_bool.lower() == 'no':
            break

    return 'Contact added.'

@input_error
def change_exist_contact(*arg,a_book = AddressBook,n_book = Notebook):
    contact = a_book.get(arg[0])
    if contact:
        contact.change_record_info(arg[1],arg[2])
        return f"Contact's phone was changed."
    else:
        return "Can't find such contact. Try again."

@input_error
def show_contact(*arg,a_book = AddressBook,n_book = Notebook):#first always address book second name
    if arg[0] in a_book.data:
        return str(a_book.data[arg[0]])
    else:
        return f"Contact {arg[0]} does not exist. "


def show_all(*arg, a_book=AddressBook, n_book=Notebook):
    table = PrettyTable()
    table.field_names = ['№', 'Name', 'Phone',
                         'Email', 'Date of Birth', 'Address']
    # сортування за "user_name"
    sorted_data = sorted(a_book.values(), key=lambda x: x.user_name.value)
    counter = 1
    for user_data in sorted_data:
        phones = user_data.user_phones
        formatted_numbers = []
        for number in phones:
            formatted_number = str(number)
            formatted_numbers.append(formatted_number)
        formatted_phone = '\n'.join(formatted_numbers)
        table.add_row([counter, user_data.user_name, formatted_phone,
                      user_data.user_email, user_data.user_birthday, user_data.user_address])
        counter += 1
    return table

@input_error
def find_user(*arg,a_book = AddressBook,n_book = Notebook):
    results = a_book.find_users(arg[0])
    string_list = [str(result) for result in results] if results else "No matches found among contacts."
    return string_list

def help_commands(*arg,a_book = AddressBook,n_book = Notebook):
    l_cmd = []
    l_cmd.append(STR_EPIC_COMMANDS)
    for cmd in commands:
        s = "Command: " + Fore.YELLOW + f"{cmd.get('name')}" + Style.RESET_ALL
        s2 = "Write: " + Fore.GREEN + f"{cmd['input view'][0]}"+ Style.RESET_ALL + ',' + Fore.GREEN + f" {cmd['input view'][1]}" + Style.RESET_ALL + " or " + Fore.GREEN + f"{cmd['input view'][2]}" + Style.RESET_ALL
        s = '|{:<40}|{:<95}|'.format(s, s2)
        if len(cmd["arguments"]) > 0:
            s3 = "Arguments: " + Fore.BLUE + f"{cmd['arguments']}" + Style.RESET_ALL
            s3 = '{:<50}'.format(s3)
            s += s3
        l_cmd.append(s)
    return l_cmd

@input_error
def remove_contact(*arg,a_book = AddressBook,n_book = Notebook):
    a_book.remove_record(arg[0])
    return 'Contact was removed.'

def sort_files(*arg,a_book = AddressBook,n_book = Notebook):#first ALWAYS address book. next every you need, just ignore the first
    sort_files_in_this_path(arg[0])

@input_error
def add_note(*arg,a_book = AddressBook,n_book = Notebook): 
    tags = get_command_input("Enter note tags (comma-separated):",need_comp = False).split(",")
    tags = [Tag(tag.strip()) for tag in tags]
    note = Note(arg[0], tags, arg[1])
    n_book.add_note(note)
    return 'Note added. \n'# + str(note)

@input_error
def remove_note(*arg,a_book = AddressBook,n_book = Notebook):
    title = arg[0]
    n_book.remove_note(title)
    return 'Note removed.'

@input_error
def find_notes(*args, a_book=AddressBook, n_book=Notebook):
    text = args[0]
    return n_book.search_notes_by_text(text)

@input_error
def edit_note_info(*arg, a_book=AddressBook, n_book=Notebook):
    note = n_book.search_notes_by_title(arg[0])
    if note:
        note.change_note_info(arg[1],arg[2])
        if arg[1] == 'tag':
            while True:
                input_bool = get_command_input("Do you want to add more tags? Write Yes or No: ",need_comp = False)
                if input_bool.lower() == 'yes':
                    new_tag = get_command_input("Enter tag:", Tag ,need_comp = False)
                    note.add_tag(new_tag)
                elif input_bool.lower() == 'no':
                    break
        return "Note information updated."
    else:
        return "Note not found."


@input_error
def search_notes_by_tag(*arg, a_book=AddressBook, n_book=Notebook):
    tag_name = arg[0]
    matching_notes = n_book.search_notes_by_tag(tag_name)
    if matching_notes:
        return [str(note) for note in matching_notes]
    else:
        return "No notes found for the given tag."

@input_error
def sort_notes_by_tag(*arg, a_book=AddressBook,n_book=Notebook):
    n_book.sort_notes_by_tag()
    return "Notes sorted by tags."

def show_all_notes(*arg, a_book=AddressBook,n_book=Notebook):
    table = n_book.show_notes()
    return table

def start_game(*arg,a_book = AddressBook,n_book = Notebook):
    return "Starting the game..."

def ending(*arg,a_book = AddressBook,n_book = Notebook):
    return 'Goodbye!'

input_variants = ['hello','hi','start','add contact','new contact','create contact','change contact','change phone','change contact details',"sort","sort files","need sort",
                  'get contact', 'show contact','show person','show contacts','show address book','show all book','goodbye','close','end','search user','find contact','find user', "help","commands",
                  "need help",'remove note','delete note','get note out','add note', 'new note','create note','find notes', 'search notes','remove contact','delete contact','take out contact'
                  ,"edit note", "change note", "search by tag","sort by tag",'show all notes','show notebook','show notes','give me note',"find by tag","give me note by tag"
                  ,"tag sorting","notebook sort by tag","remake note", 'game', 'play', 'fun']
# Ініціалізація автодоповнювача зі списком команд
completer = WordCompleter(input_variants)

# Define available commands
commands = [
    {
        "name": "greet",
        "input view":["hello",'hi','start'],
        "arguments": [],
        "func":greetings
    },
    {
        "name": "game",
        "input view": ['game','play','fun'],
        "arguments": [],
        "func":start_game
    },
    {
        "name": "add new contact",
        "input view": ['add contact','new contact','create contact'],
        "arguments": ["name", "phone","birthday","email","address"],
        "func":add_new_contact
    },
    {
        "name": "change exist contact",
        "input view": ['change contact','change phone','change contact details'],
        "arguments": ["name","changed field","new value"],
        "func":change_exist_contact
    },
    {
        "name": "remove contact",
        "input view": ['remove contact','delete contact','take out contact'],
        "arguments": ["name"],
        "func":remove_contact
    },
    {
        "name": "show contact",
        "input view": ['get contact','show contact','show person'],
        "arguments": ["name"],
        "func":show_contact
    },
    {
        "name": "show all",
        "input view":  ['show contacts','show address book','show all book'],
        "arguments": [],
        "func":show_all
    },
    {
        "name": "find user",
        "input view":  ['search user','find contact','find user'],
        "arguments": ['text_for_search'],
        "func":find_user
    },
    {
        "name": "help",
        "input view": ["help","commands","need help"],
        "arguments": [],
        "func":help_commands
    },
    {
        "name": "sort",
        "input view": ["sort","sort files","need sort"],
        "arguments": ['path to the folder'],
        "func":sort_files
    },
    {
        "name": "add_note",
        "input view": ['add note', 'new note','create note'],
        "arguments": ['title', 'description'],
        "func": add_note
    },
    {
        "name": "remove_note",
        "input view": ['remove note','delete note','get note out'],
        "arguments": ['title'],
        "func": remove_note
    },
    {
        "name": "find_notes",
        "input view": ['find notes', 'search notes','give me note'],
        "arguments": ['text'],
        "func": find_notes
    },  
    {
        "name": "edit note info",
        "input view": ["edit note", "change note","remake note"],
        "arguments": ["title", "changed field", "new info"],
        "func": edit_note_info
    },   
    {
        "name": "search notes by tag",
        "input view": ["search by tag","find by tag","give me note by tag"],
        "arguments": ["tag name"],
        "func": search_notes_by_tag
    },   
    {
        "name": "sort notes by tag",
        "input view": ["sort by tag","tag sorting","notebook sort by tag"],
        "arguments": [],
        "func": sort_notes_by_tag
    },
    {
        "name": "show all notes",
        "input view":  ['show all notes','show notebook','show notes'],
        "arguments": [],
        "func":show_all_notes
    },
    {
        "name": "ending",
        "input view": ['goodbye','close','end'],
        "arguments": [],
        "func":ending
    }
    ]
