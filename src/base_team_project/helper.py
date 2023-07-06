from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter
from fuzzywuzzy import fuzz, process
import time

# Список можливих команд
commands = ['hello','hi','start','add contact','new contact','create contact','change contact','change phone','change contact details',
                  'get number contact','get phone','show phone','show all contacts','show book','show all','goodbye','close','end']

# Ініціалізація автодоповнювача зі списком команд
completer = WordCompleter(commands)

# Функція для обробки введеної команди
def process_command(command):
    if command in commands:
        print(f'Thanks, you have chosen "{command}"')
        print("Good Bye!")
        return False
    else:
        # print(f"You have chosen: {command}")
        # print(command)
        return True
        
# Додаткова функція для пошуку збігів, якщо користувач не отримає підказку  на початку
def ratio(command, commands):
    a = process.extract(command, commands, limit=len(commands))
    max_ratio = 0
    max_word = ''
    for i in range(len(a)):
        ratio = a[i][1]
        if ratio > max_ratio:
            max_ratio = ratio
            max_word = a[i][0]

    if max_ratio > 30:
        print(f"Maybe you meant a command : '{max_word}'?")
        while True:
            user_input = input("Enter Y or N: ")
            if user_input.lower() == 'y':
                command = max_word                
                return command
            elif user_input.lower() == 'n':
                return None
            else:
                continue
    else:
        print(f"Your command is '{command}'? I didn`t find this command.")
        return None        
            
# Основний цикл
while True:
    user_input = prompt('Enter a command: ', completer=completer)

    if user_input in commands:
        print(f'Thanks, you have chosen "{user_input}"')
        break

    result = ratio(user_input, commands)
    if result is None:
        print('OK, let`s try again')
    else:
        print(f'Thanks, you have chosen "{result}"')
        break    

    

