import json
from prettytable import PrettyTable
from colorama import init, Fore, Style


class Tag:
    def __init__(self, name):
        self.name = name


class Note:
    def __init__(self, title, tags, description):
        self.title = title
        if isinstance(tags, list):
            self.tags = [Tag(t) if isinstance(tags, str) else t for t in tags]
        elif tags is None:
            self.tags = []
        else:
            self.tags = Tag(tags) if isinstance(tags, str) else tags
        self.description = description

    def __repr__(self):
        tags_str = ""
        if self.tags:
            tags_str = ", ".join(tag.name for tag in self.tags)
        return "Title: {}\nTags: {}\nDescription: {}".format(self.title, tags_str, self.description)

    def to_dict(self):
        notes_data = []
        for note in self.notes:
            # Сохраняем только имена тегов
            tags_data = [tag.name for tag in note.tags]
            notes_data.append({
                'title': note.title,
                'tags': tags_data,  # Используем сохраненные имена тегов
                'description': note.description
            })
        return {'notes': notes_data}


class Notebook:
    def __init__(self):
        self.notes = []

    def add_note(self, note):
        self.notes.append(note)

    def remove_note(self, title):
        matching_notes = []
        for note in self.notes:
            if note.title.lower() == title.lower():
                matching_notes.append(note)
        for matching_note in matching_notes:
            self.notes.remove(matching_note)

    def show_notes(self):
        if not self.notes:
            print("У нотатника нет записей.")
        else:
            print("Заметки в нотатнике:")
            table = PrettyTable()
            table.field_names = ['№', 'Title', 'Tags', 'Description']
            counter = 1
            for note in self.notes:
                tags = [Fore.CYAN + '#' + tag +
                        Style.RESET_ALL for tag in note['tags']]
                table.add_row([counter, note['title'],
                              ', '.join(tags), note['description']])
                counter += 1
        print(table)

    def search_notes_by_tag(self, tag_name):
        matching_notes = []
        for note in self.notes:
            for tag in note.tags:
                if tag.name.lower() == tag_name.lower():
                    matching_notes.append(note)
                    # Stop check, if tag in found in note
                    break
        table = PrettyTable()
        table.field_names = ['№', 'Title', 'Tags', 'Description']
        counter = 1
        for note in matching_notes:
            tags = [Fore.CYAN + '#' + tag +
                    Style.RESET_ALL for tag in note['tags']]
            table.add_row([counter, note['title'],
                           ', '.join(tags), note['description']])
            counter += 1
        print(table)

    def sort_notes_by_tag(self):
        self.notes.sort(key=lambda note: [
                        tag.name.lower() for tag in note.tags])

    # добавляем методы сохр/загрузки json и методы преобразования в словарь

    def save_json(self, filename):
        with open(filename, 'w') as file:
            json.dump(self.to_dict(), file, indent=4)

    @classmethod
    def load_json(cls, filename):
        with open(filename, 'r') as file:
            data = json.load(file)
        notebook = cls()
        for note_data in data['notes']:
            title = note_data['title']
            tags = [Tag(tag_name)
                    for tag_name in note_data['tags']]  # Создаем объекты Teg
            description = note_data['description']
            note = Note(title, tags, description)
            notebook.add_note(note)
        return notebook

    def to_dict(self):
        notes_data = []
        for note in self.notes:
            # Сохраняем только имена тегов
            tags_data = [tag.name for tag in note.tags]
            notes_data.append({
                'title': note.title,
                'tags': tags_data,  # Используем сохраненные имена тегов
                'description': note.description
            })
        return {'notes': notes_data}

    def default(self, obj):
        if isinstance(obj, Tag):
            return obj.name
        raise TypeError(
            f'Object of type {obj.__class__.__name__} is not JSON serializable')
