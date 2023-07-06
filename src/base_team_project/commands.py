

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
    }
    ]
