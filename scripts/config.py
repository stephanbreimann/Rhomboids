#! /usr/bin/python3
"""
Config with folder structure
"""
import os
import platform


# Helper Function
def _folder_path(super_folder, folder_name):
    """Modification of separator (OS depending)"""
    path = os.path.join(super_folder, folder_name + sep)
    return path


def _get_sep():
    """Get operating system dependent separator"""
    if platform.system() == 'Linux':
        sep = '/'
    elif platform.system() == 'Windows':
        sep = '\\'
    elif platform.system() == 'Darwin':
        sep = '/'
    else:
        sep = '/'
    return sep


# Main Function
sep = _get_sep()
folder_project = os.path.dirname(os.path.abspath(__file__)).split('scripts')[0].replace('/', sep)
folder_scripts = _folder_path(folder_project, 'scripts')
folder_data = _folder_path(folder_project, 'data')
folder_results = _folder_path(folder_project, 'results')


def dir_meth(x):
    """Magic dir function for methods"""
    dlist = list(name for name in dir(x) if not name.startswith("_"))
    slices = list(range(1, ((len(dlist)) // 5) + 2))
    lines = [dlist[((i - 1) * 5):(i * 5)] for i in slices]
    print('Methods for: ' + str(type(x)).strip('<class').strip('>'))
    for i, line in enumerate(lines):
        if line is not None:
            print(i + 1, line)
    return 'n Methods: ' + str(len(dlist))


def dir_op(x):
    """dir function for operators"""
    dlist = list(name for name in dir(x) if name.startswith("_"))
    slices = list(range(1, ((len(dlist)) // 5) + 2))
    lines = [dlist[((i - 1) * 5):(i * 5)] for i in slices]
    print('Operator for:' + str(type(x)).strip('<class').strip('>'))
    for i, line in enumerate(lines):
        if line is not None:
            print(i + 1, line)
    return 'n overloaded Operator: ' + str(len(dlist))


def dir_all(x):
    """dir function for methods and operators"""
    print('Operator and Methods for:' + str(type(x)).strip('<class').strip('>'))
    methods = int(dir_meth(x).strip('n Methods: '))
    print('n Methods: ' + str(methods))
    operator = int(dir_op(x).strip('n overloaded Operator: '))
    print('n overloaded Operator: ' + str(operator))
    return 'Total: ' + str(methods + operator)
