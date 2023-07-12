import json
from colorama import Fore, Style
from src.memory import SetterValueIncorrect


class Tag:
    def __init__(self, name):
        self._name = name

    @property
    def name(self):
        # Getter method for the value property
        return self._name

    @name.setter
    def name(self, new_name):
        # Setter method for the value property
        if isinstance(new_name, str):
            self._name = new_name
        else:
            raise SetterValueIncorrect('Only string accepted')


class Note:
    def __init__(self, title, tags, description):
        self.title = title
        self.tags = []
        if isinstance(tags, list):
            self.tags = [Tag(t) if isinstance(t, str) else t for t in tags]
        elif tags != None:
            self.tags.append(Tag(tags) if isinstance(tags, str) else tags)
        self.description = description

    def __repr__(self):
        tags_str = ""
        if self.tags:
            tags_str = ", ".join(tag.name for tag in self.tags)
        return "Title: {}\nTags: {}\nDescription: {}".format(self.title, tags_str, self.description)
    
    def change_note_info(self,change_field, new_info):
        if change_field == 'tag':
            self.tags[-1] = new_info if isinstance(new_info, Tag) else Tag(new_info)
        elif change_field == 'title':
            self.title = new_info
        elif change_field == "description":
            self.description = new_info

    def add_tag(self,tag):
        self.tags.append(Tag(tag) if isinstance(tag, str) else tag)


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
            return "Notebook is empty."
        else:
            return self.put_notes_in_stringlist(self.notes)
    
    @staticmethod
    def put_notes_in_stringlist(notes):
        table = []
        i = 1
        for note in notes:
            table.append(f'Note №{i}')
            table.append("Title :" + Fore.YELLOW +  f"{note.title}" + Style.RESET_ALL)
            table.append("Tags :" + ','.join([(Fore.CYAN + '#' + tag.name + Style.RESET_ALL) for tag in note.tags]))
            table.append("Description:" + note.description + '\n')
            i +=1
        return table

    def search_notes_by_tag(self, tag_name):
        matching_notes = []
        for note in self.notes:
            for tag in note.tags:
                if tag.name.lower() == tag_name.lower():
                    matching_notes.append(note)
                    # Stop check, if tag in found in note
                    break
        return self.put_notes_in_stringlist(matching_notes)

    def search_notes_by_title(self,title):
        for note in self.notes:
            if title.lower() == note.title.lower():
                return note

    def search_notes_by_text(self, text):
        matching_notes = []
        for note in self.notes:
            if text.lower() in note.title.lower() or text.lower() in note.description.lower():
                matching_notes.append(note)
        return self.put_notes_in_stringlist(matching_notes)

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
