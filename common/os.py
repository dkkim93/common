import os


def remove_file(filename):
    if os.path.exists(filename):
        os.remove(filename)
