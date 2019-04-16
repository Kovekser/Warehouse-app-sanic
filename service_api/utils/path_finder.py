import os


def get_abs_path(file=''):
    """
    Function for getting abs path to file to be opened:
    depending on flag "file" returns path to fixtures folder
    or to the file.json
    """
    return os.path.join(os.getcwd(), 'fixtures', file)


def get_tab_name(abs_path):
    """Function retuns name of table in database
    (filename without .json)"""
    filename, file_extension = os.path.splitext(abs_path)
    return os.path.basename(filename).capitalize()
