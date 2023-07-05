

import collections
import difflib
from memory import AddressBook, Record

address_book = AddressBook()
Person = collections.namedtuple('Person',['name','phone'])

def get_command_input(Input_message=''):
    Input_value = None
    while Input_value is None:
        Input_value = input(f'{Input_message} ')
    return Input_value

#Функція find_closest_command(user_input) знаходить найближчу команду до введеної користувачем, за допомогою алгоритму Левенштейну.
def find_closest_command(user_input):
    closest_command = difflib.get_close_matches(user_input, input_variants, n=1)
    if closest_command:
        closest_command = closest_command[0]
        for command_dict in commands:
            if closest_command in command_dict["inpute view"]:
                cmd = command_dict
        if cmd:
            return cmd
        else:
            return None
    else:
        return None


def input_error(func):
    def wrapper(adress_book, name, phone = None):
        try:
            result = func(adress_book,name, phone)
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
    return arg[0].find_users(arg[1])
     
def ending(*arg):
    return 'Goodbye!'

input_variants = ['hello','hi','start','add contact','new contact','create contact','change contact','change phone','change contact details',
                  'get number contact','get phone','show phone','show all contacts','show book','show all','goodbye','close','end','search','find','find user']

# Define available commands
commands = [
    {
        "name": "greet",
        "inpute view":["hello",'hi','start'],
        "arguments": [],
        "func":greetings
    },
    {
        "name": "add_new_contact",
        "inpute view": ['add contact','new contact','create contact'],
        "arguments": ["name", "phone"],
        "func":add_new_contact
    },
    {
        "name": "change_exist_contact",
        "inpute view": ['change contact','change phone','change contact details'],
        "arguments": ["name","phone"],
        "func":change_exist_contact
    },
    {
        "name": "show_phone",
        "inpute view": ['get number contact','get phone','show phone'],
        "arguments": ["name"],
        "func":show_phone
    },
    {
        "name": "show_all",
        "inpute view":  ['show all contacts','show book','show all'],
        "arguments": [],
        "func":show_all
    },
    {
        "name": "find_user",
        "inpute view":  ['search','find','find user'],
        "arguments": ['text_for_search'],
        "func":find_user
    },
    # {
    #     "name" : "delete_contact",
    #     "inpute view":
    # }
    {
        "name": "ending",
        "inpute view": ['goodbye','close','end'],
        "arguments": [],
        "func":ending
    }
    ]

def get_command(name):
    return list(filter(lambda cmd: cmd["name"] == name, commands))[0]
