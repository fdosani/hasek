import os

def file_exists(path):
    try:
        with open(path):
            return True
    except (OSError, IOError):
        return False


def file_delimiter(path):
    valid = " abcdefghijklmnopqrstuvwxyz1234567890_"
    possible = ",|\t"
    with open(path, "r") as f:
        header = f.readline().strip()
        for c in header.lower():
            if c not in valid and c in possible:
                return c
        return None


def file_permissions(path):
    return os.stat(path).st_mode & 0o777


def home_file(filename):
    return os.path.join(os.path.expanduser("~"), filename)


def isfile(s):
    if isinstance(s, (str, bytes)) and " " not in s and file_exists(s):
        return True
    return False
