import os
import shutil
from pathlib import Path
import time
import re


def loading_bar(total, interval):
    for i in range(total):
        progress = (i + 1) / total
        bar_length = 30
        filled_length = int(bar_length * progress)
        bar = '▇︎' * filled_length + '-' * (bar_length - filled_length)
        percentage = progress * 100
        print(f'Progress: [{bar}] {percentage:.2f}%', end='\r')
        time.sleep(interval)

TRANS = {}  # Global variable TRANS

# Check file extension.
def category(extension):
    if extension in ['JPEG', 'PNG', 'JPG', 'SVG']:
        return 'images'
    elif extension in ['AVI', 'MP4', 'MOV', 'MKV']:
        return 'video'
    elif extension in ['DOC', 'DOCX', 'TXT', 'PDF', 'XLSX', 'PPTX']:
        return 'documents'
    elif extension in ['MP3', 'OGG', 'WAV', 'AMR']:
        return 'audio'
    elif extension in ['ZIP', 'GZ', 'TAR']:
        return 'archives'
    else:
        return 'Unknown extensions'

# Transliteration from Cyrillic to Latin.
def normalize(s):
    s2 = s.translate(TRANS)
    l = s2.split('.')
    if len(l) > 1:
        ext = '.' + l.pop()
        s2 = '.'.join(l)
    else:
        ext =''
    return re.sub(r'[^a-zA-Z0-9]', '_', s2) + ext


# Unpack archives and move their contents to the "archives" folder.
def unpack_archives(path):
    for item in os.listdir(path):
        item_path = os.path.join(path, item)
        if os.path.isfile(item_path) and item.endswith('.zip'):
            archive_folder = os.path.join(path, 'archives')
            if not os.path.exists(archive_folder):
                os.mkdir(archive_folder)
            shutil.unpack_archive(item_path, archive_folder)
            os.remove(item_path)

# Sort files in the given path.
def sort_files(path):
    for item in os.listdir(path):
        item_path = os.path.join(path, item)

        # If it's a file
        if os.path.isfile(item_path):
            # Get the file extension
            extension = item.split('.')[-1].upper()

            # If the extension is known, move the file
            if extension in ['JPEG', 'PNG', 'JPG', 'SVG', 'AVI', 'MP4', 'MOV', 'MKV', 'DOC', 'DOCX', 'TXT', 'PDF', 'XLSX', 'PPTX', 'MP3', 'OGG', 'WAV', 'AMR']:
                category_folder = category(extension)
                category_path = os.path.join(path, category_folder)

                if not os.path.exists(category_path):
                    os.mkdir(category_path)

                # Normalize the filename
                normalized_name = normalize(item)
                normalized_name_with_extension = f"{normalized_name}.{extension}"
                
                src_path = os.path.join(path, item)
                dst_path = os.path.join(category_path, normalized_name_with_extension)
                shutil.move(src_path, dst_path)

            # If the extension is unknown, do nothing
            else:
                pass

        # If it's a directory
        elif os.path.isdir(item_path):
            if item not in ['archives', 'video', 'audio', 'documents', 'images']:
                sort_files(item_path)
                # Remove empty directory after recursive call
                if not os.listdir(item_path):
                    os.rmdir(item_path)
            elif item in ['archives', 'video', 'audio', 'documents', 'images']:
                # Skip the predefined category folders
                continue
            else:
                shutil.rmtree(item_path)

def initialize_trans():
    CYRILLIC_SYMBOLS = "абвгдеёжзийклмнопрстуфхцчшщъыьэюяєіїґ"
    TRANSLATION = ("a", "b", "v", "g", "d", "e", "e", "j", "z", "i", "j", "k", "l", "m", "n", "o", "p", "r", "s", "t", "u",
                   "f", "h", "ts", "ch", "sh", "sch", "", "y", "", "e", "yu", "ya", "je", "i", "ji", "g")

    for c, l in zip(CYRILLIC_SYMBOLS, TRANSLATION):
        TRANS[ord(c)] = l
        TRANS[ord(c.upper())] = l.upper()

def sort_files_in_this_path(path):
    initialize_trans()  # Initialize TRANS
    unpack_archives(path)
    sort_files(path)

if __name__ == "__main__":
    path = Path(input("Enter the path to the folder: "))
    loading_bar(50, 0.1)
    sort_files_in_this_path(path)


