
# #ТЕСТ ПРАЦЮЄ
from src.memory import *
import unittest
import tempfile
import os
from datetime import datetime, timedelta
from prettytable import PrettyTable

def Create_simple_record(name = 'Alex'):
    return Record(name, '+380505435391', datetime(year=1970, month=11, day=7),'alex@gmail.com','Leva 16, Kiev')


class AddressBookTest(unittest.TestCase):
    def setUp(self):
    # Create a sample address book with some records
        self.address_book = self.create_simple_book()

    @staticmethod
    def create_simple_book():
        address_book = AddressBook()
        # Add some data to the address book
        record1 = Record(
            "John Doe", "+380505435391", datetime(year=1970, month=11, day=7),'john_12@gmail.com','Leva 16, Kiev')
        record2 = Record(
            "Jane Smith", "+38067777877776", datetime(year=2000, month=6, day=15),'jane_45d@gmail.com','Andrievsk 50, Lviv')
        record3 = Record(
            "Mike Johnson", "+380504605222", datetime(year=1980, month=3, day=29), 'mike_vazovskiy@gmail.com', 'Vodoprovidna 99, Odessa')

        address_book.add_record(record1)
        address_book.add_record(record2)
        address_book.add_record(record3)
        return address_book

    def test_find_users(self):
        search_string = "John"
        matching_users = self.address_book.find_users(search_string)
        self.assertEqual(len(matching_users), 2)
        self.assertEqual(matching_users[0].user_name.value, "John Doe")
        self.assertEqual(matching_users[1].user_name.value, "Mike Johnson")

        search_string = "222"
        matching_users = self.address_book.find_users(search_string)
        self.assertEqual(len(matching_users), 1)
        self.assertEqual(matching_users[0].user_name.value, "Mike Johnson")

        search_string = "Smith"
        matching_users = self.address_book.find_users(search_string)
        self.assertEqual(len(matching_users), 1)
        self.assertEqual(matching_users[0].user_name.value, "Jane Smith")

        search_string = "Kiev"
        matching_users = self.address_book.find_users(search_string)
        self.assertEqual(len(matching_users), 1)
        self.assertEqual(matching_users[0].user_name.value, "John Doe")

        search_string = "999"
        matching_users = self.address_book.find_users(search_string)
        self.assertEqual(len(matching_users), 0)

    def test_save_load_from_json(self):
        # Create a temporary file to save the JSON data
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            temp_filename = temp_file.name

        # Save the address book to the temporary file
        self.address_book.save_to_json(temp_filename)

        # Check if the file exists
        self.assertTrue(os.path.isfile(temp_filename))

        # Load the address book from the temporary file
        loaded_address_book = AddressBook.load_from_json(temp_filename)

        # Check if the loaded address book is an instance of AddressBook
        self.assertIsInstance(loaded_address_book, AddressBook)

        # Check if the loaded address book has the same records
        self.assertEqual(len(loaded_address_book.data),
                         len(self.address_book.data))
        for key, value in self.address_book.data.items():
            self.assertIn(key, loaded_address_book.data)
            self.assertEqual(value, loaded_address_book.data[key])
        # Delete the temporary file
        os.remove(temp_filename)

    def test_save_load_from_csv(self):
        # Create a temporary file to save the JSON data
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            temp_filename = temp_file.name

        # Save the address book to the temporary file
        self.address_book.save_to_csv(temp_filename)

        # Check if the file exists
        self.assertTrue(os.path.isfile(temp_filename))

        # Load the address book from the temporary file
        loaded_address_book = AddressBook.load_from_csv(temp_filename)

        # Check if the loaded address book is an instance of AddressBook
        self.assertIsInstance(loaded_address_book, AddressBook)

        # Check if the loaded address book has the same records
        self.assertEqual(len(loaded_address_book.data),
                         len(self.address_book.data))
        for key, value in self.address_book.data.items():
            self.assertIn(key, loaded_address_book.data)
            self.assertEqual(value, loaded_address_book.data[key])
        # Delete the temporary file
        os.remove(temp_filename)

    def test_add_record(self):
        address_book = self.address_book
        record = Create_simple_record()
        address_book.add_record(record)
        self.assertIn(record.user_name.value, address_book.data)

    def test_remove_record(self):
        address_book = self.address_book
        record = Create_simple_record('Ann')
        address_book.add_record(record)
        self.assertIn(record.user_name.value, address_book.data)
        address_book.remove_record('Ann')
        self.assertNotIn('Ann', address_book.data)
        self.assertIn('Jane Smith', address_book.data)
        self.assertEqual(len(address_book.data), 3)


    def test_find_in_values(self):
        address_book = self.address_book
        record = Record("Dmytro Felix", '+380505435391',datetime(year=1970, month=11, day=7),'john_12@gmail.com','Leva 16, Kiev')
        address_book.add_record(record)
        result = address_book.find_in_values(record)
        self.assertEqual(result, ("Dmytro Felix", record))

    def test_get_birthdays_per_week(self):
        # Create an AddressBook instance
        address_book = self.address_book

        birthday1 = Birthday(datetime.now() + timedelta(days=2))
        birthday2 = Birthday(datetime.now() + timedelta(days=5))
        birthday3 = Birthday(datetime.now() + timedelta(days=8))
        address_book.add_record(Record('John', '+380505435391', birthday1))
        address_book.add_record(Record('Jane', '+380505435391', birthday2))
        address_book.add_record(Record('Alice', '+380505435391', birthday3))

        # Call the function under test
        output = address_book.get_birthdays_per_week()

        # Assert the output matches the expected result
        expected_output = PrettyTable()
        expected_output.field_names = ['Greeting Day', 'Name', 'Phone', 'Date of Birth']
        expected_output.add_row(['🎂 Friday', 'John', '+380505435391', birthday1.value.strftime("%d.%m.%Y")])
        expected_output.add_row(['🎂 Monday', 'Jane', '+380505435391', birthday2.value.strftime("%d.%m.%Y")])
        self.assertEqual(str(output), str(expected_output))

class NameTest(unittest.TestCase):
    def test_get_set_value(self):
        name = Name('Alex')            
        with self.assertRaises(SetterValueIncorrect):
            name.value = 123
        self.assertEqual(name.value, 'Alex')

class PhoneTest(unittest.TestCase):
    def test_get_set_value(self):
        phone = Phone('+380505435391')
        with self.assertRaises(SetterValueIncorrect):
            phone.value = 123
        with self.assertRaises(SetterValueIncorrect):
            phone.value = 'Anna'
        with self.assertRaises(SetterValueIncorrect):
            phone.value = '380(67)7778-77-776'
        self.assertEqual(phone.value, '+380505435391')


class BirthdayTestCase(unittest.TestCase):
    def test_value_property(self):
        # Test the getter and setter of the value property
        birthday = Birthday('01/01/2000')

        # Test setting the value with a valid datetime object
        valid_datetime = datetime(year=2000, month=1, day=1)
        birthday.value = valid_datetime
        self.assertEqual(birthday.value, valid_datetime)

        # Test setting the value with a valid string representation
        valid_string = "06/01/2006"
        valid_datetime = datetime(year=2006, month=1, day=6)
        birthday.value = valid_string
        self.assertEqual(birthday.value, valid_datetime)

        # Test setting the value with an invalid string representation
        invalid_string = "Invalid Date"
        with self.assertRaises(SetterValueIncorrect):
            birthday.value = invalid_string

        # Test setting the value with an invalid type
        invalid_type = 123
        with self.assertRaises(SetterValueIncorrect):
            birthday.value = invalid_type


class RecordTestCase(unittest.TestCase):
    def test_add_phone(self):
        # Test adding a phone to the record
        record = Record("John Doe")
        phone = '+380505435391'
        record.add_phone(phone)

        self.assertEqual(len(record.user_phones), 1)
        self.assertEqual(record.user_phones[0].value, phone)

    def test_remove_phone(self):
        # Test removing a phone from the record
        record = Record("John Doe")
        phone = '+380505435391'
        record.add_phone(phone)

        record.remove_phone(phone)

        self.assertEqual(len(record.user_phones), 0)

    def test_days_to_birthday(self):
        # Test calculating the number of days to the birthday
        record = Record("John Doe", birthday=datetime.now())

        days = record.days_to_birthday()

        self.assertIsNotNone(days)

    def test_remove_n_phone(self):
        # Test removing a phone at a specified index from the record
        record = Record("John Doe")
        phones = ['+380505665391', '+380933455391','+380505438391']
        for phone in phones:
            record.add_phone(phone)

        index_to_remove = 1
        record.remove_n_phone(index_to_remove)

        self.assertEqual(len(record.user_phones), len(phones) - 1)
        self.assertNotIn(phones[index_to_remove], [
                         phone.value for phone in record.user_phones])

    def test_change_n_phone(self):
        # Test changing a phone at a specified index in the record
        record = Record("John Doe")
        phones = ['+380505665391', '+380933455391','+380505438391']
        for phone in phones:
            record.add_phone(phone)

        index_to_change = 0
        new_phone = 'anna'
        with self.assertRaises(SetterValueIncorrect):
            record.change_n_phone(index_to_change, new_phone)
        new_phone = '+380936666666'
        record.change_n_phone(index_to_change, new_phone)

        self.assertEqual(record.user_phones[index_to_change].value, new_phone)

    def test_check_argument_for_init(self):
        record = Record('Alex')

        # Test initializing Name
        result_name = record.check_argument_for_init('John', 'name')
        self.assertIsInstance(result_name, Name)
        self.assertEqual(result_name.value, 'John')

        # Test initializing Phone
        result_phone = record.check_argument_for_init('+123456789', 'phone')
        self.assertIsInstance(result_phone, Phone)
        self.assertEqual(result_phone.value, '+123456789')

        # Test initializing Email
        result_email = record.check_argument_for_init('john@example.com', 'email')
        self.assertIsInstance(result_email, Email)
        self.assertEqual(result_email.value, 'john@example.com')

        # Test initializing Birthday
        result_birthday = record.check_argument_for_init('01/01/1990', 'birthday')
        self.assertIsInstance(result_birthday, Birthday)
        self.assertEqual(result_birthday.value, datetime(day = 1, month = 1, year = 1990))

        # Test initializing Address
        result_address = record.check_argument_for_init('Leva 16', 'address')
        self.assertIsInstance(result_address, Address)
        self.assertEqual(result_address.value, 'Leva 16')

        # Test invalid class name
        result_invalid = record.check_argument_for_init('Some value', 'invalid')
        self.assertEqual(result_invalid, 'Some value')

    def test_init(self):
        # Test initializing a record with all arguments
        record1 = Record('John', phone='+123456789', birthday='01/01/1990', email='john@example.com', address='Leva 16')
        self.assertIsInstance(record1.user_name, Name)
        self.assertIsInstance(record1.user_phones, list)
        self.assertIsInstance(record1.user_birthday, Birthday)
        self.assertIsInstance(record1.user_email, Email)
        self.assertIsInstance(record1.user_address, Address)
        self.assertEqual(record1.user_name.value, 'John')
        self.assertEqual(record1.user_phones, [Phone('+123456789')])
        self.assertEqual(record1.user_birthday.value, datetime(day = 1, month = 1, year = 1990))
        self.assertEqual(record1.user_email.value, 'john@example.com')
        self.assertEqual(record1.user_address.value, 'Leva 16')

        # Test initializing a record with only name
        record2 = Record('Jane')
        self.assertIsInstance(record2.user_name, Name)
        self.assertIsInstance(record2.user_phones, list)
        self.assertIsNone(record2.user_birthday.value)
        self.assertIsNone(record2.user_email.value)
        self.assertIsNone(record2.user_address.value)
        self.assertEqual(record2.user_name.value, 'Jane')
        self.assertEqual(record2.user_phones, [])

        # Test initializing a record with a phone as a list
        record3 = Record('Bob', phone=['+38095432123', '+30989823456'])
        self.assertIsInstance(record3.user_name, Name)
        self.assertIsInstance(record3.user_phones, list)
        self.assertIsNone(record3.user_birthday.value)
        self.assertIsNone(record3.user_email.value)
        self.assertIsNone(record3.user_address.value)
        self.assertEqual(record3.user_name.value, 'Bob')
        self.assertEqual(record3.user_phones, ['+38095432123', '+30989823456'])


if __name__ == '__main__':
    unittest.main()
