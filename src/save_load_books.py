

import os
import json
import sys
from pathlib import Path
from src.memory import AddressBook
from src.notes_core import Notebook, Note

# Save and Load Address book when application begin and end work

def save_addressbook(address_book, FileName = None):
    # Get the path of the executable file
    exe_path = Path(sys.executable)

    # Create the "save" folder if it doesn't exist
    save_folder = exe_path.parent / "save"
    save_folder.mkdir(exist_ok=True)

    # Construct the file path for saving the AddressBook
    if FileName:
        file_path = save_folder / FileName
    else:
        file_path = save_folder / "phonebook.json"

    # Save the AddressBook to the file
    address_book.save_to_json(file_path)

def load_addressbook( filename = "phonebook.json"):
    # Get the path of the executable file
    exe_path = Path(sys.executable)

    # Create the "save" folder if it doesn't exist
    save_folder = exe_path.parent / "save"
    if save_folder.exists():
        # Construct the file path for loading the AddressBook
        file_path = save_folder / filename

        # Check if the file exists
        if file_path.exists():
            # Load the AddressBook from the file
            address_book = AddressBook.load_from_json(file_path)
            return address_book
        else:
            file_path = save_folder / "phonebook.csv"
            if file_path.exists():
                # Load the AddressBook from the file
                address_book = AddressBook.load_from_csv(file_path)
                return address_book
    else:
        return None

# Save load notebook in begin and end of work
SAVE_DIR = Path(sys.prefix) / 'save'    

def save_notebook(notebook, filename = 'notebook.json'):
    # Создаем директорию save, если она не существует
    if not os.path.exists(SAVE_DIR):
        os.makedirs(SAVE_DIR)

    # Сохраняем данные в JSON-файл в папке save
    file_path = os.path.join(SAVE_DIR, filename)
    with open(file_path, 'w') as file:
        json.dump(notebook.to_dict(), file, indent=4)
    # print(f"Notebook сохранен в файл: {file_path}")

def load_notebook(filename = 'notebook.json'):
    # Проверяем существование файла
    file_path = os.path.join(SAVE_DIR, filename)
    if not os.path.exists(file_path):
        # print(f"Файл {file_path} не существует.")
        return None

    # Загружаем данные из JSON-файла
    with open(file_path, 'r') as file:
        data = json.load(file)
    notebook = Notebook()
    for note_data in data['notes']:
        note = Note(
            note_data['title'],
            note_data['tags'],
            note_data['description']
        )
        notebook.add_note(note)
    # print(f"Notebook загружен из файла: {file_path}")
    return notebook
