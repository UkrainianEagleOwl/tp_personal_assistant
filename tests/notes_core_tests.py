import unittest
from src.notes_core import *
from colorama import Fore, Style


class TagTestCase(unittest.TestCase):
    def test_name_property(self):
        # Test getting the name property
        tag = Tag('tag1')
        self.assertEqual(tag.name, 'tag1')

        # Test setting the name property with a string
        tag.name = 'tag2'
        self.assertEqual(tag.name, 'tag2')

        # Test setting the name property with a non-string value
        with self.assertRaises(SetterValueIncorrect):
            tag.name = 123

    def test_name_setter(self):
        # Test setting the name property with a string
        tag = Tag('tag1')
        tag.name = 'tag2'
        self.assertEqual(tag.name, 'tag2')

        # Test setting the name property with a non-string value
        with self.assertRaises(SetterValueIncorrect):
            tag.name = 123

class NoteTestCase(unittest.TestCase):
    def setUp(self):
        self.note = Note('Note 1', ['tag1', 'tag2'], 'Description')

    def test_init(self):
        self.assertEqual(self.note.title, 'Note 1')
        self.assertEqual(len(self.note.tags), 2)
        self.assertIsInstance(self.note.tags[0], Tag)
        self.assertIsInstance(self.note.tags[1], Tag)
        self.assertEqual(self.note.tags[0].name, 'tag1')
        self.assertEqual(self.note.tags[1].name, 'tag2')
        self.assertEqual(self.note.description, 'Description')

    def test_repr(self):
        expected_repr = "Title: Note 1\nTags: tag1, tag2\nDescription: Description"
        self.assertEqual(repr(self.note), expected_repr)

    def test_change_note_info_tag(self):
        self.note.change_note_info('tag', 'new_tag')
        self.assertEqual(len(self.note.tags), 2)
        self.assertEqual(self.note.tags[1].name, 'new_tag')

    def test_change_note_info_title(self):
        self.note.change_note_info('title', 'New Title')
        self.assertEqual(self.note.title, 'New Title')

    def test_change_note_info_description(self):
        self.note.change_note_info('description', 'New Description')
        self.assertEqual(self.note.description, 'New Description')

    def test_add_tag(self):
        self.note.add_tag('tag3')
        self.assertEqual(len(self.note.tags), 3)
        self.assertEqual(self.note.tags[2].name, 'tag3')


class NotebookTestCase(unittest.TestCase):
    def setUp(self):
        self.notebook = Notebook()
        self.note1 = Note('Note 1', ['tag1', 'tag2'], 'Description 1')
        self.note2 = Note('Note 2', ['tag2', 'tag3'], 'Description 2')
        self.note3 = Note('Note 3', ['tag3', 'tag4'], 'Description 3')
        self.notebook.add_note(self.note1)
        self.notebook.add_note(self.note2)
        self.notebook.add_note(self.note3)

    def test_init(self):
        self.assertEqual(len(self.notebook.notes), 3)

    def test_add_note(self):
        note4 = Note('Note 4', ['tag4'], 'Description 4')
        self.notebook.add_note(note4)
        self.assertEqual(len(self.notebook.notes), 4)
        self.assertEqual(self.notebook.notes[-1], note4)

    def test_remove_note(self):
        self.notebook.remove_note('Note 1')
        self.assertEqual(len(self.notebook.notes), 2)
        self.assertNotIn(self.note1, self.notebook.notes)

    def test_show_notes_empty(self):
        empty_notebook = Notebook()
        expected_output = "Notebook is empty."
        self.assertEqual(empty_notebook.show_notes(), expected_output)

    def test_show_notes(self):
        expected_output = [
            'Note №1',
            f"Title :{Fore.YELLOW}Note 1{Style.RESET_ALL}",
            f"Tags :{Fore.CYAN}#tag1{Style.RESET_ALL},{Fore.CYAN}#tag2{Style.RESET_ALL}",
            "Description:Description 1\n",
            'Note №2',
            f"Title :{Fore.YELLOW}Note 2{Style.RESET_ALL}",
            f"Tags :{Fore.CYAN}#tag2{Style.RESET_ALL},{Fore.CYAN}#tag3{Style.RESET_ALL}",
            "Description:Description 2\n",
            'Note №3',
            f"Title :{Fore.YELLOW}Note 3{Style.RESET_ALL}",
            f"Tags :{Fore.CYAN}#tag3{Style.RESET_ALL},{Fore.CYAN}#tag4{Style.RESET_ALL}",
            "Description:Description 3\n"
        ]
        self.assertEqual(self.notebook.show_notes(), expected_output)

    def test_search_notes_by_tag(self):
        expected_output = [
            'Note №1',
            f"Title :{Fore.YELLOW}Note 1{Style.RESET_ALL}",
            f"Tags :{Fore.CYAN}#tag1{Style.RESET_ALL},{Fore.CYAN}#tag2{Style.RESET_ALL}",
            "Description:Description 1\n",
            'Note №2',
            f"Title :{Fore.YELLOW}Note 2{Style.RESET_ALL}",
            f"Tags :{Fore.CYAN}#tag2{Style.RESET_ALL},{Fore.CYAN}#tag3{Style.RESET_ALL}",
            "Description:Description 2\n"
        ]
        self.assertEqual(self.notebook.search_notes_by_tag('tag2'), expected_output)

    def test_search_notes_by_title(self):
        expected_note = self.notebook.search_notes_by_title('Note 2')
        self.assertEqual(expected_note, self.note2)

    def test_search_notes_by_text(self):
        matching_notes = self.notebook.search_notes_by_text('description')
        expected_notes = [self.note1, self.note2, self.note3]
        self.assertEqual(matching_notes, self.notebook.put_notes_in_stringlist(expected_notes))

    def test_sort_notes_by_tag(self):
        self.notebook.sort_notes_by_tag()
        expected_order = [self.note1, self.note2, self.note3]
        self.assertEqual(self.notebook.notes, expected_order)

    # def test_save_and_load_json(self):
    #     filename = 'notebook.json'
    #     self.notebook.save_json(filename)
    #     loaded_notebook = Notebook.load_json(filename)
    #     self.assertEqual(len(loaded_notebook.notes), 3)
    #     self.assertEqual(loaded_notebook.notes[0].title, 'Note 1')
    #     self.assertEqual(loaded_notebook.notes[0].tags[0].name, 'tag1')
    #     self.assertEqual(loaded_notebook.notes[0].description, 'Description 1')

    def test_to_dict(self):
        expected_dict = {
            'notes': [
                {
                    'title': 'Note 1',
                    'tags': ['tag1', 'tag2'],
                    'description': 'Description 1'
                },
                {
                    'title': 'Note 2',
                    'tags': ['tag2', 'tag3'],
                    'description': 'Description 2'
                },
                {
                    'title': 'Note 3',
                    'tags': ['tag3', 'tag4'],
                    'description': 'Description 3'
                }
            ]
        }
        self.assertEqual(self.notebook.to_dict(), expected_dict)

    def test_default(self):
        tag = Tag('tag')
        self.assertEqual(self.notebook.default(tag), 'tag')
        with self.assertRaises(TypeError):
            self.notebook.default(123)

if __name__ == '__main__':
    unittest.main()
