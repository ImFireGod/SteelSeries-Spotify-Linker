from os import path


def fetch_content_path(content):
    return path.abspath(path.join(path.dirname(path.abspath(__file__)), '../', content))
