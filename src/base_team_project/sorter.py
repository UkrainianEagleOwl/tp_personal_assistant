from pathlib import Path
import os

#The extensions dictionary maps folder names to lists of corresponding file extensions.
#Словник extensions містить відповідності назв папок до списків відповідних розширень файлів.
extensions = {
    'video': ['mp4', 'mov', 'avi', 'mkv', 'wmv', '3gp', '3g2', 'mpg', 'mpeg', 'm4v', 'h264', 'flv', 'rm', 'swf', 'vob'],
    'audio': ['mp3', 'wav', 'ogg', 'flac', 'aif', 'mid', 'midi', 'mpa', 'wma', 'wpl', 'cda'],
    'image': ['png', 'jpg', 'bpm', 'ai', 'psd', 'ico', 'jpeg', 'ps', 'svg', 'tif', 'tiff'],
    'data': ['sql', 'sqlite', 'sqlite3', 'csv', 'dat', 'db', 'log', 'mdb', 'sav', 'tar', 'xml'],
    'archive': ['zip', 'rar', '7z', 'z', 'gz', 'rpm', 'arj', 'pkg', 'deb'],
    'text': ['pdf', 'txt', 'doc', 'docx', 'rtf', 'tex', 'wpd', 'odt'],
    'presentation': ['pptx', 'ppt', 'pps', 'key', 'odp'],
    'font': ['otf', 'ttf', 'fon', 'fnt'],
    'gif': ['gif'],
    'exe': ['exe'],
    'apk': ['apk'],
    'bat': ['bat']
}

#The user is prompted to enter the path to the folder that needs to be sorted
#Від користувача потребується ввести шлях до папки, яку потрібно відсортувати
main_path = input("Enter the path to the folder that needs to be sorted: ")
main_path = Path(main_path)

#The folders_create function creates the necessary folders based on the folder_names and checks if any files with matching extensions exist in the parent folder before creating the folder.
#Функція folders_create створює необхідні папки на основі folder_names та перевіряє, чи існують файли з відповідними розширеннями у батьківскій папці, перш ніж створювати папку.
def folders_create(folder_path, folder_names):
    for folder in folder_names:
        folder_path = folder_path / folder
        if not folder_path.exists():
            file_paths = get_file_paths(folder_path)
            exts = folder_names[folder]
            if any(file_path.suffix[1:] in exts for file_path in file_paths):
                folder_path.mkdir()



def get_subfolder_paths(folder_path):
    subfolder_paths = [f for f in folder_path.iterdir() if f.is_dir()]
    return subfolder_paths

#The get_file_paths function retrieves the paths of all files in the specified folder.
#Функція get_file_paths отримує шляхи до всіх файлів у вказаній папці.
def get_file_paths(folder_path):
    file_paths = folder_path.glob('*')
    return [f for f in file_paths if f.is_file()]

#The sort_files function iterates over the file paths and moves them to the corresponding folders based on their extensions.
#Функція sort_files перебирає шляхи файлів і переміщує їх до відповідних папок на основі їх розширень.
def sort_files(folder_path):
    file_paths = get_file_paths(folder_path)
    ext_list = list(extensions.items())

    for file_path in file_paths:
        extension = file_path.suffix[1:]
        file_name = file_path.name

        for folder_name, exts in ext_list:
            if extension in exts:
                print(f'Moving {file_name} to {folder_name} folder')
                destination_folder = folder_path / folder_name
                destination_folder.mkdir(exist_ok=True)
                destination_file = destination_folder / file_name
                file_path.rename(destination_file)

#The remove_empty_folders function removes any empty subfolders.
#Функція remove_empty_folders видаляє порожні підпапки.
def remove_empty_folders(folder_path):
    subfolder_paths = get_subfolder_paths(folder_path)

    for subfolder_path in subfolder_paths:
        if not any(subfolder_path.iterdir()):
            print(f'Removing empty folder: {subfolder_path.name}')
            os.rmdir(subfolder_path)


if __name__ == "__main__":
    folders_create(main_path, extensions)
    sort_files(main_path)
    remove_empty_folders(main_path)
