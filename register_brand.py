from db_functions import DatabaseFunctions
from db_connection import cursor, connection
import tkinter.messagebox
import mysql.connector as mysql

dbFuncProvider = DatabaseFunctions()

class RegisterBrand:
    def register_brand(self, brand_name):
        try:
            value = (brand_name,)
            dbFuncProvider.insert(table='brands', data=value)
            tkinter.messagebox.showinfo('Success', f'Brand Name "{brand_name}" Added Successfully!')

        except mysql.errors.IntegrityError:
            tkinter.messagebox.showerror('Error!', f'Brand Name "{brand_name}" Already Exists!')

    def delete_brand(self, brand_name): # ! Not working
        list_of_all_names = dbFuncProvider.fetch('brands', ['name'])

        if brand_name in list_of_all_names:
            dbFuncProvider.delete(table="brands", conditions={'name': ['=', brand_name]})
        
        else:
            tkinter.messagebox.showerror('Error!', f"{brand_name} doesn't exists")
        
    def update_brand(self, old_brand_name, new_brand_name):
        all_brands = dbFuncProvider.fetch('brands', field_list=['name'])
        for i in  range(len(all_brands)):
            all_brands[i] = all_brands[i].lower()

        if old_brand_name.lower() in all_brands:
            
            conditions = {'name': ['=', old_brand_name]}
            dbFuncProvider.update(table="brands", fields=['name'], values=[new_brand_name], conditions=conditions)
            
            tkinter.messagebox.showinfo('Success!', f"'{old_brand_name}' changed to '{new_brand_name}'")
        
        else:
            tkinter.messagebox.showerror('Error!', f"{old_brand_name} doesn't exists")