import os


def create_directory(directory: str):
    if not os.path.exists(directory):
        os.makedirs(directory)


def write_file(path: str, data: str):
    f = open(path, 'w')
    f.write(data)
    f.close()


def create_data_files(project_name: str, base_url: str):
    
    queue = project_name + '/queue.txt'
    if not os.path.isfile(queue):
        write_file(queue, base_url)
    
    crawled = project_name + '/crawled.txt'
    if not os.path.isfile(crawled):
        write_file(crawled, '')


def append_to_file(file_name: str, data: str):
    with open(file_name, 'a') as f:
        f.write(data + '\n')


def delete_file_contents(file_name: str):
    with open(file_name, 'w') as f:
        pass


def file_to_set(file_name: str) -> set[str]:
    results = set()
    with open(file_name, 'rt') as f:
        for line in f:
            results.add(line.replace('\n', ''))
    return results


def set_to_file(links: set[str], file_name: str):
    delete_file_contents(file_name)
    for link in sorted(links):
        append_to_file(file_name, link)