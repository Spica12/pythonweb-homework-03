import argparse
import logging
from pathlib import Path
from random import randint, choice, choices





"""
-- output -o dist
-- len -l 12
-- deep -d 3
-- folders -f 3
-- files -f

cd pyweb_hw_03
python3 main_sort_trash.py -s picture
python3 main_file_generator.py -0 picture
"""

parser = argparse.ArgumentParser(description= 'App fo generate random folders and files')
parser.add_argument('-o', '--output', default='dist')       # 
parser.add_argument('-l', '--len', default=12)              # Максимальна довжина назви файлу або папки
parser.add_argument('-d', '--deep', default=10)              # Максимальна глибина вкладень в папках
parser.add_argument('-f', '--folders', default=2)           # Максимальна кількість папок
parser.add_argument('-i', '--files', default=50)            # Максимальна кількість файлів

args = vars(parser.parse_args())    # object -> dict
output = args.get('output')
MAX_LEN_NAME = args.get('len')
MAX_FOLDERS_DEEP = args.get('deep')
MAX_RANDOM_FOLDERS = args.get('folders')
MAX_RANDOM_FILES = args.get('files')

folders = []

type_files = ('DOC', 'DOCX', 'TXT', 'PDF', 'XLSX', 'PPTX', \
                  'JPEG', 'PNG', 'JPG', 'SVG', \
                  'AVI', 'MP4', 'MOV', 'MKV', \
                  'MP3', 'OGG', 'WAV', 'AMR', \
                  'LMN', 'PLO', 'DBXS', 'VMXSA', 'ALFE', '')


def generate_name():

    all_symbols = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'\
            'абвгґдеєжзиіїйклмнопрстуфхцчшщьюяАБВГҐДЕЄЖЗИІЇЙКЛМНОПРСТУФХЦЧШЩЬЮЯ'\
            '$%\'- @~!(){}^#&+;=[]0123456789'

    return ''.join(choices(all_symbols, k=MAX_LEN_NAME))



def generate_folders(path: Path, deep):
    if deep < 0:
        return None

    for _ in range(MAX_RANDOM_FOLDERS):
        name_folder = generate_name()
        new_folder = path / name_folder
        new_folder.mkdir(parents=True, exist_ok=True)
        logging.debug(f"Added new random folder: {new_folder}")
        folders.append(new_folder)
        generate_folders(new_folder, deep-1)



def generate_random_file(path: Path):
    function_list = [generate_file, generate_archive]

    for _ in range(MAX_RANDOM_FILES):
        choice(function_list)(path)


def generate_file(path: Path):
    with open(f'{path}/{generate_name()}.{choice(type_files).lower()}', 'wb') as file:
        file.write('Some text'.encode())



def generate_archive(path: Path):
    pass


def main():
    logging.basicConfig(level=logging.DEBUG, format="%(threadName)s %(message)s")
    logging.debug("Start program.")

    output_folder = Path(output)
    output_folder.mkdir(parents=True, exist_ok=True)
    logging.debug(f"Created target folder: {output_folder}")

    generate_folders(output_folder, MAX_FOLDERS_DEEP)

    for folder in folders:
        generate_random_file(folder)


if __name__ == '__main__':
    main()

    

