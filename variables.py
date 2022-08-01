import os

password = '2332'
database = 'store_record_test'
host = 'localhost'
user = 'root'


MYSQL_BIN = 'C:\\Program Files\\MySQL\MySQL Server 8.0\\bin'

# folders
db_folder = 'Database_File' # in static
icon_folder = 'Icons'     # in static
static_folder = 'Static'  # in store_book where main.py is located

file_name = 'stock.sql'
file_name_xl = 'stock.xlsx'

# dirs
cur_wd = os.getcwd()
STATIC_DIR = cur_wd + f'\\{static_folder}'
ICON_PATH = STATIC_DIR + f'\\{icon_folder}'
DB_FILE_DIR = STATIC_DIR + f'\\{db_folder}'

#dependencies
dependencies = ["tkcalendar", "pandas", "numpy", "mysql-connector-python", "xlsxwriter"]
