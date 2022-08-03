import os
import itertools
from variables import db_folder, icon_folder, static_folder, STATIC_DIR, dependencies, cur_wd, host, user, password, database_fields
import mysql.connector as mysql

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


def init_db(database):
    connection_ = mysql.connect(
        host=host,
        user=user,
        password=password
    )
    cursor_ = connection_.cursor()
    cursor_.execute('SHOW DATABASES;')
    data_tuple = cursor_.fetchall()
    data_list = list(itertools.chain(*data_tuple))

    if database not in data_list:
        command = f'CREATE DATABASE {database}'
        cursor_.execute(command)


def init_tables():
    
    from db_functions import DatabaseFunctions
    dbFuncs = DatabaseFunctions()
    
    print("Creating the tables............")
    dbFuncs.create_table(table="brands", fields_dict={
                            "Brand Name": ("name", "varchar(100)", "PRIMARY KEY")})

    foreign_key_details = {
        "reference_table": "brands",
        "reference_field": "name",
        "field": "brand_name"
    }

    dbFuncs.create_table(
        table="stock", fields_dict=database_fields, foreign_key=foreign_key_details)
    dbFuncs.create_table(
        table="before_update", fields_dict=database_fields, foreign_key=foreign_key_details)
    dbFuncs.create_table(
        table="after_update", fields_dict=database_fields, foreign_key=foreign_key_details)
    dbFuncs.create_table(table="recently_deleted",
                            fields_dict=database_fields, foreign_key=foreign_key_details)
    dbFuncs.create_table(
        table="recently_added", fields_dict=database_fields, foreign_key=foreign_key_details)
    dbFuncs.create_table(
        table="stock_in", fields_dict=database_fields, foreign_key=foreign_key_details)
    dbFuncs.create_table(
        table="stock_out", fields_dict=database_fields, foreign_key=foreign_key_details)
    dbFuncs.create_table(
        table="garbage", fields_dict=database_fields, foreign_key=foreign_key_details)
    
    print("Tables created successfully!")



