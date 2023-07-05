

import sys
from pathlib import Path
from memory import AddressBook

# Save and Load Address book when application begin and end work

def save_address_book(address_book):
    # Get the path of the executable file
    exe_path = Path(sys.executable)

    # Create the "save" folder if it doesn't exist
    save_folder = exe_path.parent / "save"
    save_folder.mkdir(exist_ok=True)

    # Construct the file path for saving the AddressBook
    file_path = save_folder / "phonebook.json"

    # Save the AddressBook to the file
    address_book.save_to_json(file_path)

def load_address_book():
    # Get the path of the executable file
    exe_path = Path(sys.executable)

    # Create the "save" folder if it doesn't exist
    save_folder = exe_path.parent / "save"
    if save_folder.exists():
        # Construct the file path for loading the AddressBook
        file_path = save_folder / "phonebook.json"

        # Check if the file exists
        if file_path.exists():
            # Load the AddressBook from the file
            address_book = AddressBook.load_from_json(file_path)
            return address_book
        else:
            file_path = save_folder / "phonebook.csv"
            if file_path.exists():
                # Load the AddressBook from the file
                address_book = AddressBook.load_from_csv(file_path)
                return address_book
    else:
        return None
