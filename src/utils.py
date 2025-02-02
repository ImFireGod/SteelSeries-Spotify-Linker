from os import path, getenv

def fetch_app_data_path(content=''):
    return path.abspath(getenv('APPDATA') + '/SpotifyLinker/' + content)

def fetch_content_path(content):
    return path.abspath(path.join(path.dirname(path.abspath(__file__)), '../', content))