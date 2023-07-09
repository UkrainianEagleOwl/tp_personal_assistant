# to memory
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

    def __repr__(self):
        tags_str = ""
        if self.tags:
            tags_str = ", ".join(tag.name for tag in self.tags)
        return "Title: {}\nTags: {}\nDescription: {}".format(self.title, tags_str, self.description)
    
    def edit_title(self, new_title):
        self.title = new_title
        
    def edit_tags(self, new_tags):
        if isinstance(new_tags, list):
            self.tags = new_tags
        else:
            self.tags = []
            
    def edit_description(self, new_description):
        self.description = new_description

    def change_rec_info(self, change_field, new_info):
        match change_field:
            case 'title':
                self.edit_title(new_info)
            case 'tags':
                self.edit_tags(new_info)
            case 'description':
                self.edit_description(new_info)
                
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
            print("У нотатнику немає записів.")
        else:
            print("Нотатки в нотатнику:")
            for note in self.notes:
                print("Назва:", note.title)
                print("Теги:")
                for tag in note.tags:
                    print("- ", tag.name)
                print("Опис:", note.description)
                print()
                
    def search_notes_by_tag(self, tag_name):
        matching_notes = []
        for note in self.notes:
            for tag in note.tags:
                if tag.name.lower() == tag_name.lower():
                    matching_notes.append(note)
                    #Stop check, if tag in found in note
                    break
        return matching_notes
    
    def sort_notes_by_tag(self):
        self.notes.sort(key=lambda note: [tag.name.lower() for tag in note.tags])

# notebook = Notebook()   # в мейн?

# to commands
# def add_notes(*arg):
#     title = get_command_input("Enter note title:")
#     description = get_command_input("Enter note description:")
#     tags = get_command_input("Enter note tags (comma-separated):").split(",")
#     tag_list = []
#     for tag in tags:     
#         tag_list.append(Teg(tag))
#     note = Notes(title, tag_list, description)
#     notebook.add_note(note)
#     notebook.show_notes()
#     return 'Note added.'
    
    
# def remove_notes(*args):
#     title = get_command_input("Enter note title to remove:")
#     if notebook.remove_note(title):
#         return 'Note removed.'
#     else:
#         return 'Note not found.'
    


# commands = [
#   {
#         "name": "add_notes",
#         "inpute view": ['add notes'],
#         "arguments": ['title, description'],
#         "func": add_notes
#     },
#     {
#         "name": "remove_notes",
#         "inpute view": ['remove notes'],
#         "arguments": ['title'],
#         "func": remove_notes
#     }
# ]