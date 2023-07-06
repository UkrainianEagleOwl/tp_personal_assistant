# Створити структуру сберігання нотатків. 
# Класс нотатків містить назву, список тегів і опис.
# Тег є классом який містить тільки назву.


class Teg:
    def __init__(self, name):
        self.name = name


class Notes:
    def __init__(self, title, tags, description):
        self.title = title
        if isinstance(tags, list):
            self.tags = tags
        else:
            self.tags = []
        self.description = description


tag1 = Teg('command_project')
tag2 = Teg("WORK")

note1 = Notes()