

import unittest
import sys
from src.memory import AddressBook,Record
from src.notes_core import *
from src.save_load_books import *
from pathlib import Path
from datetime import datetime


class BooksSaveLoadTests(unittest.TestCase):
    def setUp(self):
        self.address_book = self.create_simple_book()
        self.notebook = self.create_simple_notebook()

    def tearDown(self):
        # Delete the test save folder and file if they exist
        save_folder = Path(sys.executable).parent / "save"
        file_path = save_folder / "phonebook_test.json"
        if file_path.exists():
            file_path.unlink()
        file_path = save_folder / "notebook_test.json"
        if file_path.exists():
            file_path.unlink()

    @staticmethod
    def create_simple_book():
        address_book = AddressBook()
        # Add some data to the address book
        record1 = Record(
            "John Doe", "+380505435391", datetime(year=1970, month=11, day=7),'john_12@gmail.com','Leva 16, Kiev')
        record2 = Record(
            "Jane Smith", "+38067777877776", datetime(year=2000, month=1, day=1),'jane_45d@gmail.com','Andrievsk 50, Lviv')
        record3 = Record(
            "Mike Johnson", "+380504605222", datetime(year=1980, month=3, day=29), 'mike_vazovskiy@gmail.com', 'Vodoprovidna 99, Odessa')

        address_book.add_record(record1)
        address_book.add_record(record2)
        address_book.add_record(record3)
        return address_book
    
    @staticmethod
    def create_simple_notebook():
        note_book = Notebook()
        note1 = Note('Greece','greece, history','Greece, officially the Hellenic Republic, is a country in Southeast Europe.')
        note2 = Note('Alex','greece, history','Following the assassination of Phillip II, his son Alexander III The Great assumed the leadership of the League of Corinth and launched an invasion of the Persian Empire with the combined forces of the League in 334 BC.')
        note3 = Note('Rome','italy, history','"Rome is the capital city of Italy.')
        note_book.add_note(note1)
        note_book.add_note(note2)
        note_book.add_note(note3)
        return note_book

    def test_save_load_address_book(self):
        # Call the function to save the AddressBook
        save_addressbook(self.address_book,"phonebook_test.json")

        # Check if the file exists
        file_path = Path(sys.executable).parent / "save" / "phonebook_test.json"
        self.assertTrue(file_path.exists())
        loaded_address_book = load_addressbook("phonebook_test.json")

        # Check if the loaded AddressBook is not None
        self.assertIsNotNone(loaded_address_book)
        # Check if the loaded address book is an instance of AddressBook
        self.assertIsInstance(loaded_address_book, AddressBook)

        # Check if the loaded address book has the same records
        self.assertEqual(len(loaded_address_book.data),
                         len(self.address_book.data))
        for key, value in self.address_book.data.items():
            self.assertIn(key, loaded_address_book.data)
            self.assertEqual(value, loaded_address_book.data[key])


    def test_save_load_notebook(self):
        # Call the function to save the AddressBook
        save_notebook(self.notebook,"notebook_test.json")

        # Check if the file exists
        file_path = Path(sys.executable).parent / "save" / "notebook_test.json"
        self.assertTrue(file_path.exists())
        loaded_notebook = load_notebook("notebook_test.json")

        # Check if the loaded AddressBook is not None
        self.assertIsNotNone(loaded_notebook)
        # Check if the loaded address book is an instance of AddressBook
        self.assertIsInstance(loaded_notebook, Notebook)

        # Check if the loaded address book has the same records
        self.assertEqual(len(loaded_notebook.notes),
                         len(self.notebook.notes))
        for index in range(len(self.notebook.notes)):
            loaded_note = loaded_notebook.notes[index]
            base_note = self.notebook.notes[index]
            self.assertEqual(base_note.title, loaded_note.title)
            self.assertEqual(len(base_note.tags), len(loaded_note.tags))
            for i2 in range(len(base_note.tags)):
                self.assertEqual(base_note.tags[i2].name, loaded_note.tags[i2].name)
            self.assertEqual(base_note.description, loaded_note.description)

if __name__ == "__main__":
    unittest.main()
