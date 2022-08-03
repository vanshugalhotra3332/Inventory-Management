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

# database

product_name_field = 'product_name'
tractor_field = 'tractor'
brand_name_field = 'brand_name'
part_number_field = 'part_number'
code_field = 'code'
mrp_field = 'mrp'
box_no_field = 'box_no'
description_field = 'description'
quantity_field = 'quantity'
warning_qty_field = 'warning_qty'
date_field = 'date'
image_field = 'image'

database_fields = {
    'Product Name': (product_name_field, 'varchar(230)', 'PRIMARY KEY'), # (field in database, datatype(length), constraints)
    'Tractor': (tractor_field, 'varchar(80)', 'NOT NULL'), 
    'Brand Name': (brand_name_field, 'varchar(120)'), 
    'Part No.': (part_number_field, 'varchar(190)', 'DEFAULT NULL UNIQUE'),
    'Code': (code_field, 'varchar(50)'),
    'MRP': (mrp_field, 'int', 'NOT NULL'),
    'Box': (box_no_field, 'varchar(60)'),
    'Description': (description_field, 'varchar(255)'),
    'Quantity': (quantity_field, 'int', 'NOT NULL'),
    'Warning Qty': (warning_qty_field, 'int', 'NOT NULL'),
    'Date': (date_field, 'varchar(90)'),
    'Image': (image_field, 'varchar(110)')
}

db_fields = len(database_fields)

#dependencies
dependencies = ["tkcalendar", "pandas", "mysql-connector-python", "xlsxwriter"]
