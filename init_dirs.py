import os
from variables import db_folder, icon_folder, static_folder, STATIC_DIR, dependencies, cur_wd

def init_dirs():
    if static_folder not in os.listdir():
        os.mkdir(static_folder)
        print(f'{static_folder} created successfully!')

    os.chdir(STATIC_DIR)
    if db_folder not in os.listdir():
        os.mkdir(db_folder)
        print(f'{db_folder} created successfully! inside {static_folder}')

    if icon_folder not in os.listdir():
        os.mkdir(icon_folder)
        print(f'{icon_folder} created successfully! inside {static_folder}')

    os.chdir(cur_wd)

    if "requirements.txt" not in os.listdir():
        with open("requirements.txt", 'w') as lib_file:
            for lib in dependencies:
                lib_file.write(lib + "\n")
            
init_dirs()