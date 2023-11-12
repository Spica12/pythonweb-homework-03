import argparse
from pathlib import Path
from shutil import copyfile
from threading import Thread
import logging
import time

"""
--source -s picture
--output -o dist
--mode -m sync | thread

python3 main_sort_trash.py -s picture
python3 file_generator.py picture
"""

parser = argparse.ArgumentParser(description= 'App fo sorting folder')
parser.add_argument('-s', '--source', required=True)
parser.add_argument('-o', '--output', default='dist')
parser.add_argument('-m', '--mode', default='thread')
args = vars(parser.parse_args())    # object -> dict
source = args.get('source')
output = args.get('output')
mode = args.get('mode')

folders = []


def measure_time(func):

    def inner(*args, **kwargs):

        start_time = time.perf_counter()  
        result = func(*args, **kwargs)
        stop_time = time.perf_counter()
        delta_time = stop_time - start_time
        print(f'Total time: {func.__name__} - {round(delta_time, 4)} s')

        return result
    
    return inner


def grabs_folder(path: Path):
    for el in path.iterdir():
        if el.is_dir():
            logging.debug(f"Added {el} to folders")
            folders.append(el)
            grabs_folder(el)


def sort_file(path: Path):
    for el in path.iterdir():
        if el.is_file():
            ext = el.suffix
            new_path = output_folder / ext
            try:
                new_path.mkdir(exist_ok=True, parents=True)
                copyfile(el, new_path / el.name)
                logging.debug(f"Complete copy file {el}.")
            except OSError as e:
                logging.error(e)


@measure_time
def sort_mode_sync():
    
    for folder in folders:
        sort_file(folder)


@measure_time
def sort_mode_thread():

    threads = []

    for folder in folders:
        th = Thread(target=sort_file, args=(folder, ))
        th.start()
        threads.append(th)

    [th.join() for th in threads]       # Waiting till al threads will finish own work


def main():

    if mode == 'sync':
        sort_mode_sync()
    elif mode == 'thread':
        sort_mode_thread()
    else:
        logging.error('Repeat command use "-m sync" or "-m thread"')


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG, format="%(threadName)s %(message)s")
    logging.debug("Start program.")

    base_folder = Path(source)
    output_folder = Path(output)

    folders.append(base_folder)
    grabs_folder(base_folder)

    main()

    print('You can remove parent folder')
