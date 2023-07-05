

from commands import greetings,get_command_input,find_closest_command
from save_load_book import save_address_book,load_address_book
from memory import AddressBook,SetterValueIncorrect

def main():
    work_book = load_address_book()
    if not work_book:
        print("(debug) Book not loaded.")
        work_book = AddressBook()
    print("Welcome to the Assistant bot! ")
    print(greetings())
    while True:
        input_string = get_command_input("Enter a command: ")
        #parse input function that get back command or None
        command = find_closest_command(input_string)
        if command:
            try:
                cmd_func = command['func']
                if len(command['arguments']) > 0:
                    print(f'For {command.get("name")} please write {command.get("arguments")} splitted by comma.')
                    input_string = get_command_input("Enter arguments: ")
                    arguments = list(input_string.split(','))
                    result = cmd_func(work_book,*arguments)
                else:
                    result = cmd_func(work_book)
                if isinstance(result,list):
                    for i in result:
                        print
                else:
                    print(result) if result else None

                if command["name"] == 'ending':
                    break
            except SetterValueIncorrect as e:
                print(e.message)
        else:
            print("Sorry, i don't understand this your command. Please try again.")
    save_address_book(work_book)

if __name__ == '__main__':
    main()
