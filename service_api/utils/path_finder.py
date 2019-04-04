import os

def get_abs_path(file=''):
    """
    Function for getting abs path to file to be opened:
    depending on flag "file" returns path to fixtures folder
    or to the file.json
    """
    return os.path.join(os.getcwd(), 'fixtures', file)