import os
import shutil
from pathlib import Path


# Перевірка на розширення.
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


# Транслітерація кириличного алфавіту на латинський.
def normalize(name):
    CYRILLIC_SYMBOLS = "абвгдеёжзийклмнопрстуфхцчшщъыьэюяєіїґ"
    TRANSLATION = ("a", "b", "v", "g", "d", "e", "e", "j", "z", "i", "j", "k", "l", "m", "n", "o", "p", "r", "s", "t", "u",
                   "f", "h", "ts", "ch", "sh", "sch", "", "y", "", "e", "yu", "ya", "je", "i", "ji", "g")

    TRANS = {}
    for c, l in zip(CYRILLIC_SYMBOLS, TRANSLATION):
        TRANS[ord(c)] = l
        TRANS[ord(c.upper())] = l.upper()

    return name.translate(TRANS, '_').replace('_', '').replace(' ', '_')


# Розпаковує архіви та переносить їх вміст до папки "archives".
def unpack_archives(path):
    for item in os.listdir(path):
        item_path = os.path.join(path, item)
        if os.path.isfile(item_path) and item.endswith('.zip'):
            archive_folder = os.path.join(path, 'archives')
            if not os.path.exists(archive_folder):
                os.mkdir(archive_folder)
            shutil.unpack_archive(item_path, archive_folder)
            os.remove(item_path)


# Сортує файли в папці.
def sort_files(path):
    for item in os.listdir(path):
        item_path = os.path.join(path, item)
        
        # Якщо це файл
        if os.path.isfile(item_path):
            # Отримуємо розширення файлу
            extension = item.split('.')[-1].upper()
            
            # Якщо розширення відоме, переміщуємо файл
            if extension in ['JPEG', 'PNG', 'JPG', 'SVG', 'AVI', 'MP4', 'MOV', 'MKV', 'DOC', 'DOCX', 'TXT', 'PDF', 'XLSX', 'PPTX', 'MP3', 'OGG', 'WAV', 'AMR']:
                category_folder = category(extension)
                category_path = os.path.join(path, category_folder)
                
                if not os.path.exists(category_path):
                    os.mkdir(category_path)
                
                src_path = os.path.join(path, item)
                dst_path = os.path.join(category_path, item)
                shutil.move(src_path, dst_path)
            
            # Якщо розширення невідоме, не робимо нічого
            else:
                pass
        
        # Якщо це папка
        elif os.path.isdir(item_path):
            if item not in ['archives', 'video', 'audio', 'documents', 'images']:
                sort_files(item_path)
                # Удаляем пустую папку после рекурсивного вызова
                if not os.listdir(item_path):
                    os.rmdir(item_path)
            else:
                shutil.rmtree(item_path)


def main():
    path = Path(input("Введіть шлях до папки: "))
    unpack_archives(path)
    sort_files(path)


if __name__ == "__main__":
    main()
