

import difflib
from sorter import sort_files_in_this_path
from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter
from common_functions import STR_EPIC_COMMANDS, YELLOW,RESET,BLUE,GREEN
from memory import Record

def get_command_input(Input_message=''):
    Input_value = None
    while Input_value is None:
        Input_value = prompt(Input_message, completer=completer)
    return Input_value

#Функція find_closest_command(user_input) знаходить найближчу команду до введеної користувачем, за допомогою алгоритму Левенштейну.
def find_closest_command(user_input):
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
    def wrapper(*arg):
        try:
            result = func(*arg)
            return result
        except KeyError:
            print("The contact is missing. ")
        except IndexError:
            print("Enter the name and number separated by a space. ")
        except ValueError:
            print("ValueError. Please try again. ")
    return wrapper    
        
def greetings(*arg):
    return "Hello. How i can help you?"

@input_error
def add_new_contact(*arg):#first always address book,second Name, third phone
    arg[0].add_record(Record(arg[1].capitalize(),arg[2]))
    return 'Contact added.'

@input_error
def change_exist_contact(*arg):#first always address book
    contact = arg[0].get(arg[1])
    if contact:
        contact.change_n_phone(0, arg[2])
        return f"Contact's phone was changed."
    else:
        return "Can't find such contact. Try again."

@input_error
def show_phone(*arg):#first always address book second name
    if arg[1] in arg[0].data:
        return f"The phone number of {arg[1]} is {arg[0].data[arg[1]].user_phones[0]}. "
    else:
        return f"Contact {arg[1]} does not exist. "

def show_all(*arg):
    return [str(contact) for contact in arg[0].values()]

@input_error
def find_user(*arg):
    result = arg[0].find_users(arg[1])
    return result if result else "No matches found among contacts."

def help_commands(*arg):
    l_cmd = []
    l_cmd.append(STR_EPIC_COMMANDS)
    for cmd in commands:
        s = "Command:" + YELLOW + f"{cmd.get('name')}" + RESET
        s2 = "For calling write" + GREEN + f":{cmd['input view'][0]}"+ RESET + ',' + GREEN + f" {cmd['input view'][1]}" + RESET + " or " + GREEN + f"{cmd['input view'][2]}" + RESET
        s = '|{:<40}|{:<110}|'.format(s, s2)
        if len(cmd["arguments"]) > 0:
            s3 = "Need arguments:" + BLUE + f"{cmd['arguments']}" + RESET
            s3 = '{:<50}'.format(s3)
            s += s3
        l_cmd.append(s)
    return l_cmd

def sort_files(*arg):#first ALWAYS address book. next every you need, just ignore the first
    sort_files_in_this_path(arg[1])
          
def ending(*arg):
    return 'Goodbye!'

def add_notes(*arg):
    title = get_command_input("Enter note title:")
    description = get_command_input("Enter note description:")
    tags = get_command_input("Enter note tags (comma-separated):").split(",")
    tags = [Teg(tag.strip()) for tag in tags]
    note = Notes(title, tags, description)
    arg[0].add_note(note)
    return 'Note added.'

def remove_notes(*arg):
    title = get_command_input("Enter note title to remove:")
    if arg[0].remove_note(title):
        return 'Note removed.'
    else:
        return 'Note not found.'

def edit_title(*arg):
    contact = arg[0].get(arg[1])
    if contact:
        contact.edit_title(arg[2])
        return f'Contact a title was changed.'
    else:
        return "Can't find such contact. Try again."

def search_notes_by_title(*arg):
    mathcing_notes = []
    for note in arg[0].notes:
        if note.title.lower() == arg[1].lower():
            mathcing_notes.append(note)
    return mathcing_notes

def sort_notes_by_tag(*arg):
    arg[0].sort_notes_by_tag()
    return 'Notes sorted by tag.'

def edit_description(*arg):
    note_title = get_command_input("Enter the title of the note to edit: ")
    new_description = get_command_input("Enter the new description: ")
    matching_notes = arg[0].search_notes_by_title(note_title)
    if matching_notes:
        for note in matching_notes:
            note.edit_description(new_description)
        return 'Note description edited.'
    else:
        return 'Note not found.'

def edit_note_title(*arg):
    old_title = get_command_input("Enter the current title of the note: ")
    new_title = get_command_input("Enter the new title: ")
    matching_notes = arg[0].search_notes_by_title(old_title)
    if matching_notes:
        for note in matching_notes:
            note.edit_title(new_title)
        return 'Note title edited.'
    else:
        return 'Note not found'


input_variants = ['hello','hi','start','add contact','new contact','create contact','change contact','change phone','change contact details',"sort","sort files","need sort",
                  'get number contact','get phone','show phone','show all contacts','show book','show all','goodbye','close','end','search','find','find user', "help","commands","need help"]
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
        "name": "add new contact",
        "input view": ['add contact','new contact','create contact'],
        "arguments": ["name", "phone"],
        "func":add_new_contact
    },
    {
        "name": "change exist contact",
        "input view": ['change contact','change phone','change contact details'],
        "arguments": ["name","phone"],
        "func":change_exist_contact
    },
    {
        "name": "show phone",
        "input view": ['get number contact','get phone','show phone'],
        "arguments": ["name"],
        "func":show_phone
    },
    {
        "name": "show all",
        "input view":  ['show all contacts','show book','show all'],
        "arguments": [],
        "func":show_all
    },
    {
        "name": "find user",
        "input view":  ['search','find','find user'],
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
        "name": "ending",
        "input view": ['goodbye','close','end'],
        "arguments": [],
        "func":ending
    },
    {
        "name": "add_notes",
        "inpute view": ['add notes'],
        "arguments": ['title, description'],
        "func": add_notes
    },
    {
        "name": "remove_notes",
        "inpute view": ['remove notes'],
        "arguments": ['title'],
        "func": remove_notes
    }
    {
        "name": "edit title",
        "input view": ["edit tags", "change tags"],
        "arguments": ["note_title", "new_tags"],
        "func": edit_title
    }
    
    {
        "name": "search_notes_by_title",
        "input view": ["search title", "find title"],
        "arguments": ["note_title"],
        "func": search_notes_by_title
    }
    
    {
        "name": "sort_notes_by_tag",
        "input view": ["sort notes by tag", "sort by tag"],
        "arguments": [],
        "func": sort_notes_by_tag
    }
    
    {
        "name": "edit_description",
        "input view": ["edit description", "change description"],
        "arguments": [],
        "func": edit_description
    }
    
    {
        "name": "edit_note_title",
        "input view": ["edit note title", "change note title"]
        "arguments": [],
        "func": edit_note_title
    }
]
