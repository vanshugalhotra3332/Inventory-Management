from db_functions import DatabaseFunctions
from db_connection import cursor, connection
import tkinter.messagebox
import mysql.connector as mysql

function_provider = DatabaseFunctions()

class RegisterBrand:
    def register_brand(self, brand_name):
        try:
            insert_command = 'INSERT INTO brands(name) VALUES(%s)'
            value = (brand_name,)
            cursor.execute(insert_command, value)
            connection.commit()
            tkinter.messagebox.showinfo('Success', f'Brand Name "{brand_name}" Added Successfully!')

        except mysql.errors.IntegrityError:
            tkinter.messagebox.showerror('Error!', f'Brand Name "{brand_name}" Already Exists!')

    def delete_brand(self, brand_name):
        list_of_all_names = function_provider.fetch('brands', ['name'])

        if brand_name in list_of_all_names:
            delete_command = f'DELETE FROM brands WHERE name={brand_name}'
            cursor.execute(delete_command)
            connection.commit()
        
        else:
            tkinter.messagebox.showerror('Error!', f"{brand_name} doesn't exists")
        
        # not working

    def update_brand(self, old_brand_name, new_brand_name):
        all_brands = function_provider.fetch('brands', field_list=['name'])
        for i in  range(len(all_brands)):
            all_brands[i] = all_brands[i].lower()

        if old_brand_name.lower() in all_brands:
            update_command = f'UPDATE brands SET name="{new_brand_name}" where name="{old_brand_name}"'
            cursor.execute(update_command)
            connection.commit()
            tkinter.messagebox.showinfo('Success!', f"'{old_brand_name}' changed to '{new_brand_name}'")
        
        else:
            tkinter.messagebox.showerror('Error!', f"{old_brand_name} doesn't exists")