import os
import threading


lock = threading.Lock()


def create_directory(directory: str):
    if not os.path.exists(directory):
        os.makedirs(directory)


def write_to_file(path: str, data: str):
    with lock:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(data)


def write_to_file_in_binary_mode(path: str, data: bytes):
    with lock:
        with open(path, 'wb') as f:
            f.write(data)



def create_data_files(project_name: str, base_url: str):
    
    queue = project_name + '/queue.txt'
    if not os.path.isfile(queue):
        write_to_file(queue, base_url)
    
    crawled = project_name + '/crawled.txt'
    if not os.path.isfile(crawled):
        write_to_file(crawled, '')


def add_line_to_file(file_name: str, data: str):
    with lock:
        with open(file_name, 'a', encoding='utf-8') as f:
            f.write(data + '\n')


def read_from_file(path: str) -> str:
    with lock:
        with open(path, 'r', encoding='utf-8') as f:
            return f.read()


def delete_file_contents(file_name: str):
    with lock:
        open(file_name, 'w').close()


def convert_file_to_set(file_name: str) -> set[str]:
    with lock:
        results = set()
        with open(file_name, 'rt', encoding='utf-8') as f:
            for line in f:
                results.add(line.replace('\n', ''))
        return results


def convert_set_to_file(links: set[str], file_name: str):
    delete_file_contents(file_name)
    for link in links:
        add_line_to_file(file_name, link)