def task_test():
    """Preform tests."""
    yield {'actions': ['coverage run -m unittest -v'], 'name': "run"}
    yield {'actions': ['coverage report'], 'verbosity': 2, 'name': "report"}


def task_pot():
    """Re-create .pot ."""
    return {
            'actions': ['pybabel extract -o prog.pot po'],
            'file_dep': glob.glob('po/*.py'),
            'targets': ['prog.pot'],
           }
           
def task_po():
    """Update translations."""
    return {
            'actions': ['pybabel update -D prog -d po -i prog.pot'],
            'file_dep': ['prog.pot'],
            'targets': ['po/ru/LC_MESSAGES/prog.po'],
           }
           
def task_mo():
    """Compile translations."""
    return {
            'actions': [
                (create_folder, ['po/ru/LC_MESSAGES']),
                'pybabel compile -D prog -l ru -i po/ru/LC_MESSAGES/prog.po -d po'
                       ],
            'file_dep': ['po/ru/LC_MESSAGES/prog.po'],
            'targets': ['po/ru/LC_MESSAGES/prog.mo'],
           }
