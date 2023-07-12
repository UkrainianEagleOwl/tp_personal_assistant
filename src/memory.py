import re
import json
import csv
from datetime import datetime, timedelta
from collections import UserDict
from prettytable import PrettyTable
from colorama import Fore,Style


class SetterValueIncorrect(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class AddressBook(UserDict):
    # Class representing an address book, which is a subclass of UserDict

    def get_birthdays_per_week(self):

        days_week = {0: 'Monday', 1: 'Tuesday', 2: 'Wednesday',
                     3: 'Thursday', 4: 'Friday', 5: 'Saturday', 6: 'Sunday'}

        # Визначення інтервалу, в якому потрібно вітати
        current_time = datetime.now()
        one_week_interval = timedelta(weeks=1)
        max_date = current_time + one_week_interval

        list_contacts =[]

        # Приведення дати народження до поточного року
        for user_data in self.data.values():
            if user_data.user_birthday.value:
                bday = user_data.user_birthday.value
                bday = bday.replace(year=current_time.year)
                list_contacts.append(Record(user_data.user_name,user_data.user_phones,bday,user_data.user_email,user_data.user_address))

        # Створення списку користувачів, яких потрібно привітати
        birthday_users = []
        for user_data in list_contacts:
            if user_data.user_birthday.value:
                user_birthday = user_data.user_birthday.value
                if current_time < user_birthday <= max_date:
                    if user_birthday.weekday() > 4:
                        greeting_day = days_week[0]
                    else:
                        greeting_day = days_week[user_birthday.weekday()]
                    user_info = {
                        'user_name': user_data.user_name.value,
                        'user_phones': ', '.join([str(x) for x in user_data.user_phones]),
                        'user_birthday': user_data.user_birthday.value.strftime("%d %B"),
                        'day': '🎂' + ' ' + greeting_day
                    }
                    birthday_users.append(user_info)

        # Вивід списку користувачів за допомогою prettytable
        table = PrettyTable()
        table.field_names = ['Greeting Day', 'Name', 'Phone', 'Date of Birth']
        for user_info in birthday_users:
            table.add_row([user_info['day'], user_info['user_name'],
                           user_info['user_phones'], user_info['user_birthday']])
        print(table)
        return table

    def add_record(self, aRecord):
        # Method to add a record to the address book
        self.data[aRecord.user_name.value] = aRecord

    def remove_record(self, name):
        # Method to remove a record from the address book
        self.data.pop(name)

    def find_in_values(self, aRecord):
        # Method to find a record in the address book's values
        if aRecord in self.data.values():
            for i in self.data.values():
                if i == aRecord:
                    return (aRecord.user_name.value, aRecord)
        return None

    def find_users(self, search_string):
        # Find users whose name or phone number matches the search string
        matching_users = []
        for record in self.data.values():
            if record.user_name.value.find(search_string) != -1:
                matching_users.append(record)
            elif record.user_email.value:
                if record.user_email.value.find(search_string) != -1:
                    matching_users.append(record)
                elif record.user_address.value:
                    if record.user_address.value.find(search_string) != -1:
                        matching_users.append(record)
                    else:
                        for phone in record.user_phones:
                            if phone.value.find(search_string) != -1:
                                matching_users.append(record)
                                break
            else:
                for phone in record.user_phones:
                    if phone.value.find(search_string) != -1:
                        matching_users.append(record)
                        break
        return matching_users

    def to_dict(self):
        # create dictionary based on class book
        return {
            'data': {
                name: record.to_dict() for name, record in self.data.items()
            }
        }

    def from_dict(cls, data):
        # get address book object from dictionary represantation
        address_book = cls()
        records = [Record.from_dict(record_data)
                   for record_data in data['data'].values()]
        for record in records:
            address_book.add_record(record)
        return address_book

    def save_to_json(self, filename):
        # method for saving book in json format
        with open(filename, 'w') as file:
            json.dump(self.to_dict(), file, indent=4)

    @classmethod
    def load_from_json(cls, filename):
        # method for loading book from json format
        with open(filename, 'r') as file:
            data = json.load(file)
        address_book = cls()
        records = [Record.from_dict(record_data)
                   for record_data in data['data'].values()]
        for record in records:
            address_book.add_record(record)
        return address_book

    def save_to_csv(self, filename):
        # method for saving book in csv format
        with open(filename, "w", newline="") as file:
            writer = csv.writer(file)
            for record in self.data.values():
                phones = [phone.value for phone in record.user_phones]
                writer.writerow([record.user_name.value, *phones])

    @classmethod
    def load_from_csv(cls, filename):
        # method for loading book from csv format
        address_book = cls()
        with open(filename, "r", newline="") as file:
            reader = csv.reader(file)
            for row in reader:
                name = Name(row[0])
                phones = [Phone(phone) for phone in row[1:]]
                record = Record(name)
                for phone in phones:
                    record.add_phone(phone)
                address_book.add_record(record)
        return address_book


class Field():
    # Base class representing a field
    def __eq__(self, other):
        if isinstance(other, Field):
            return self.value == other.value
        return False

    def __init__(self, new_value = ''):
        # Constructor to initialize the field with a value
        self._value = new_value


class Name(Field):
    def __init__(self, new_value = ''):
        # Constructor to initialize the field with a value
        self.value = new_value

    # Class representing a name field, which is a subclass of Field
    @property
    def value(self):
        # Getter method for the value property
        return self._value

    @value.setter
    def value(self, new_value):
        # Setter method for the value property
        if isinstance(new_value, str):
            self._value = new_value
        else:
            raise SetterValueIncorrect('Only string accepted')

    def __str__(self) -> str:
        return f'{self.value}'
    
    def __repr__(self) -> str:
        return f'Name: {self.value}'


class Phone(Field):
    def __init__(self, new_value = ''):
        # Constructor to initialize the field with a value
        self.value = new_value

    # Class representing a phone field, which is a subclass of Field

    @property
    def value(self):
        # Getter method for the value property
        return self._value

    @value.setter
    def value(self, new_value):
        # Setter method for the value property
        if not isinstance(new_value, str):
            try:
                new_value = str(new_value)
            except TypeError:
                raise SetterValueIncorrect(
                    Fore.RED +
                    'Incorrect type of information for phone number.' + Style.RESET_ALL)
            
        if re.search(r"^\+?[0-9]{1,4}\s?[0-9]{4,14}$", new_value):
            self._value = new_value
        else:
            raise_mesage = Fore.RED + 'You write phone number incorrectly. \n' + Style.RESET_ALL + 'Number must begin with plus, and be without spaces,hyphen or brackets. Example: ' + Fore.BLUE + '"+380990658131"' + Style.RESET_ALL
            raise SetterValueIncorrect(raise_mesage)
        
    def __str__(self):
        return f'{self.value}'
    
    def __repr__(self) -> str:
        return f'Phone: {self.value}'


class Birthday(Field):
    def __init__(self, new_value = ''):
        # Constructor to initialize the field with a value
        self.value = new_value

    # Class representing a birthday field, which is a subclass of Field

    @property
    def value(self):
        # Getter method for the value property
        return self._value

    @value.setter
    def value(self, new_value):
        if new_value == None:
            self._value = new_value
        else:
            # Setter method for the value property
            if isinstance(new_value, datetime):
                self._value = new_value
            elif isinstance(new_value, str):
                try:
                    self._value = datetime.strptime(new_value, '%d/%m/%Y') # Output: 28/06/2023
                except:
                    raise_mesage = Fore.RED + 'You write birthday data incorrectly. \n' + Style.RESET_ALL + 'Format of birthday data is day/month/year. Example: ' + Fore.BLUE + '"28/06/2023"' + Style.RESET_ALL
                    raise SetterValueIncorrect(raise_mesage)
            else:
                raise SetterValueIncorrect( Fore.RED +'Only string data or datetime accepted' + Style.RESET_ALL)
    
    def __str__(self) -> str:
        return f'{self.value.strftime("%d/%m/%Y") if self.value else None}'
    
    def __repr__(self) -> str:
        return f'Birthday: {self.value.strftime("%d/%m/%Y") if self.value else None}'

class Email(Field):
    def __init__(self, new_value = ''):
        # Constructor to initialize the field with a value
        self.value = new_value

    @property
    def value(self):
        # Getter method for the value property
        return self._value

    @value.setter
    def value(self, new_value):
        if new_value == None:
            self._value = new_value
        else:
            if not isinstance(new_value, str):
                try:
                    new_value = str(new_value)
                except TypeError:
                    raise SetterValueIncorrect(Fore.RED +
                        'Incorrect type of information for email.' + Style.RESET_ALL)
                
            if re.search(r'^[\w\.-]+@[\w\.-]+\.\w+$', new_value):
                self._value = new_value
            else:
                raise_mesage = Fore.RED + 'You write email incorrectly. \n' + Style.RESET_ALL + 'Here is a template for email: ' + Fore.BLUE + '"test@example.com"' + Style.RESET_ALL
                raise SetterValueIncorrect(raise_mesage)
    
    def __str__(self) -> str:
        return f'{self.value}'
    
    def __repr__(self) -> str:
        return f'Email: {self.value}'

class Address(Field):
    def __init__(self, new_value = ''):
        # Constructor to initialize the field with a value
        self.value = new_value

    @property
    def value(self):
        # Getter method for the value property
        return self._value

    @value.setter
    def value(self, new_value):
        if new_value == None:
            self._value = new_value
        else:
            if not isinstance(new_value, str):
                try:
                    new_value = str(new_value)
                except TypeError:
                    raise SetterValueIncorrect(Fore.RED +
                        'Incorrect type of information for address.' + Style.RESET_ALL)
                
            if re.search(r'^\w+\s+\d+(?:,\s+\w+)?(?:,\s+\w+)?$', new_value):
                self._value = new_value
            else:
                raise_mesage = Fore.RED + 'You write address incorrectly. \n' + Style.RESET_ALL + 'The correct entry of the address is the street, number, city and, if desired, the country. Here is a template: ' + Fore.BLUE + '"Potyomkinskya 30, Kyiv"' + Style.RESET_ALL
                raise SetterValueIncorrect(raise_mesage)
            
    def __str__(self) -> str:
        return f'{self.value}'
    
    def __repr__(self) -> str:
        return f'Address: {self.value}'

class Record():
    # Class representing a record
    @staticmethod
    def check_argument_for_init(input_str,class_name):
        if class_name == 'name':
            return Name(input_str)
        elif class_name == 'phone':
            return Phone(input_str)
        elif class_name == 'email':
            return Email(input_str)
        elif class_name == 'birthday':
            return Birthday(input_str)
        elif class_name == 'address':
            return Address(input_str)
        else:
            return input_str

    def __init__(self, name, phone=None, birthday=None, email=None,address=None):
        # Constructor to initialize the record with a name, phone, and birthday
        self.user_name = name if isinstance(name, Name) else self.check_argument_for_init(name,'name')
        self.user_phones = []
        self.user_birthday = birthday if isinstance(birthday, Birthday) else self.check_argument_for_init(birthday,'birthday')
        self.user_email = email if isinstance(email, Email) else self.check_argument_for_init(email,'email')
        self.user_address = address if isinstance(address, Address) else self.check_argument_for_init(address,'address')
        if isinstance(phone, list):
            self.user_phones = phone
        elif phone:
            self.add_phone(phone)

    def __eq__(self, other):
        if isinstance(other, Record):
            return self.user_name.value == other.user_name.value
        return False

    def __str__(self):
        table = PrettyTable()
        table.field_names = ['Name', 'Phones', 'Birthday', 'Email', 'Address']
        phone_numbers = ', '.join(str(phone) for phone in self.user_phones)
        table.add_row([
            self.user_name,
            phone_numbers,
            self.user_birthday,
            self.user_email,
            self.user_address
        ])
        return str(table)
    
    def to_dict(self):
        # create dictionary based on class record
        return {
            'user_name': self.user_name.value,
            'user_phones': [phone.value for phone in self.user_phones],
            'user_birthday': self.user_birthday.value.strftime("%d/%m/%Y") if self.user_birthday.value else None,
            'user_email': self.user_email.value if self.user_email else None,
            'user_address': self.user_address.value if self.user_address else None
            }

    @classmethod
    def from_dict(cls, data):
        #method get record from dictionary form
        data_name = Name(data.get('user_name'))
        phones_data = data.get('user_phones', [])
        phones = [Phone(phone_number) for phone_number in phones_data]
        if data['user_birthday']:
            data_birthday = datetime.strptime(data['user_birthday'],"%d/%m/%Y")
        else:
            data_birthday = None 
        data_email = Email(data.get('user_email'))
        data_address = Address(data.get('user_address'))
        record = Record(data_name, birthday = data_birthday,email=data_email,address=data_address)
        for phone in phones:
            record.add_phone(phone)
        return record

    def add_phone(self, aPhone):
        # Method to add a phone to the record
        if isinstance(aPhone, str):
            self.user_phones.append(Phone(aPhone))
        elif isinstance(aPhone, Phone):
            self.user_phones.append(aPhone)

    def remove_phone(self, aPhone):
        # Method to remove a phone from the record
        try:
            if isinstance(aPhone, Phone):
                self.user_phones.remove(aPhone)
            elif isinstance(aPhone, str):
                self.user_phones.remove(Phone(aPhone))
        except ValueError:
            print('Not find such phone')

    def remove_n_phone(self, aPhoneIndex):
        # Method to remove the phone at a specified index from the record
        self.user_phones.pop(aPhoneIndex)

    def change_n_phone(self, aPhoneIndex, aNewPhone):
        # Method to change the phone at a specified index to a new phone
        self.user_phones[aPhoneIndex].value = aNewPhone

    def change_record_info(self,change_field,new_info):
        if change_field == 'phone':
            self.user_phones[0].value = new_info if isinstance(new_info, Phone) else self.check_argument_for_init(new_info,'phone')
        elif change_field == 'email':
            self.user_email = new_info if isinstance(new_info, Email) else self.check_argument_for_init(new_info,'email')
        elif change_field == 'birthday':
            self.user_birthday = new_info if isinstance(new_info, Birthday) else self.check_argument_for_init(new_info,'birthday')
        elif change_field == 'address':
            self.user_address = new_info if isinstance(new_info, Address) else self.check_argument_for_init(new_info,'address')

    def days_to_birthday(self):
        # Method to calculate the number of days to the birthday
        if not self.user_birthday:
            return None

        current_datetime = datetime.now()
        this_year_birthday = datetime(
            year=current_datetime.year, month=self.user_birthday.value.month, day=self.user_birthday.value.day)
        return (this_year_birthday - current_datetime).days
