

import unittest
import sys
from memory import AddressBook,Record
from save_load_book import load_address_book, save_address_book
from pathlib import Path
from datetime import datetime


class AddressBookTests(unittest.TestCase):
    def setUp(self):
        self.address_book = self.create_simple_book()

    def tearDown(self):
        # Delete the test save folder and file if they exist
        save_folder = Path(sys.executable).parent / "save"
        file_path = save_folder / "address_book.json"
        if file_path.exists():
            file_path.unlink()
        if save_folder.exists():
            save_folder.rmdir()

    @staticmethod
    def create_simple_book():
        address_book = AddressBook()
        # Add some data to the address book
        record1 = Record(
            "John Doe", "+380(50)543-5-391", datetime(year=1970, month=11, day=7))
        record2 = Record(
            "Jane Smith", "380(67)7778-77-776", datetime(year=2000, month=1, day=1))
        record3 = Record(
            "Mike Johnson", "+380(50)460-5-222", datetime(year=1980, month=3, day=29))

        address_book.add_record(record1)
        address_book.add_record(record2)
        address_book.add_record(record3)
        return address_book

    def test_save_load_address_book(self):
        # Call the function to save the AddressBook
        save_address_book(self.address_book)

        # Check if the file exists
        file_path = Path(sys.executable).parent / "save" / "address_book.json"
        self.assertTrue(file_path.exists())
        loaded_address_book = load_address_book()

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

if __name__ == "__main__":
    unittest.main()
