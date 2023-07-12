import openai
import sys
from pathlib import Path
from cryptography.fernet import Fernet

STR_OPENAI_HELP = """
To find your OpenAI API key:
    Go to https://platform.openai.com/account/api-keys. You will need to log in (or sign up) to your OpenAI account.
    Click "Create new secret key", and copy it.
    You should then paste it into VS Code when prompted.
"""

def activate_openai(key = None):
    if key:
        openai.api_key = key
        return True
    else:
        try:
            exe_path = Path(sys.executable)
            save_folder = exe_path.parent / "save"
            if save_folder.exists():
                # Construct the file path for loading the AddressBook
                file_path = save_folder / 'secrets.bin'
                if file_path.exists():
                    with open(file_path,'r') as fh:
                        lines = fh.readlines()
                        key = lines[0].strip() # Read Fernet key from the first line
                        encrypted_api_key = lines[1].strip() # Read encrypted API k
                    decrypted_api_key  = decrypt_key(encrypted_api_key,key)
                    openai.api_key = decrypted_api_key
                    return True
                else:
                    return False
            else:
                return False
        except:
            return False

        

def decrypt_key(encrypted_key, encryption_key):
    cipher_suite = Fernet(encryption_key)
    decrypted_key = cipher_suite.decrypt(encrypted_key)
    return decrypted_key.decode()

def encrypt_key(api_key, encryption_key):
    cipher_suite = Fernet(encryption_key)
    encrypted_key = cipher_suite.encrypt(api_key.encode())
    return encrypted_key

def save_openai():
    # Generate Fernet key
    key = Fernet.generate_key()

    # Encrypt the API key
    api_key = openai.api_key
    encrypted_api_key = encrypt_key(api_key,key)

    exe_path = Path(sys.executable)

    # Create the "save" folder if it doesn't exist
    save_folder = exe_path.parent / "save"
    save_folder.mkdir(exist_ok=True)

    # Construct the file path for saving the AddressBook
    file_path = save_folder / "secrets.bin"

    with open(file_path,'w') as fh:
        fh.write(key.decode() +'\n')
        fh.write(encrypted_api_key.decode())



def input_answer_from_ai(customer_input = str):
    prompt_string = customer_input + ' You have only 150 symbols, fit in them.'

    # Generate text relevant to the command using OpenAI
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt_string,
        max_tokens=150,
        n=1,
        stop=None,
        temperature=0.6,
        frequency_penalty=0.2,
        presence_penalty=0.2
    )
    generated_text = response.choices[0].text.strip()
    return generated_text
