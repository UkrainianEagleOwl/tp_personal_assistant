import os
import json
import sys
from src.notes_core import Notebook, Note
from pathlib import Path

SAVE_DIR = Path(sys.prefix) / 'save'

def save_notebook(notebook):
    # Создаем директорию save, если она не существует
    if not os.path.exists(SAVE_DIR):
        os.makedirs(SAVE_DIR)

    # Сохраняем данные в JSON-файл в папке save
    file_path = os.path.join(SAVE_DIR, 'notebook.json')
    with open(file_path, 'w') as file:
        json.dump(notebook.to_dict(), file, indent=4)
    # print(f"Notebook сохранен в файл: {file_path}")

def load_notebook():
    # Проверяем существование файла
    file_path = os.path.join(SAVE_DIR, 'notebook.json')
    if not os.path.exists(file_path):
        print(f"Файл {file_path} не существует.")
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
    print(f"Notebook загружен из файла: {file_path}")
    return notebook