from dataclasses import fields
from tkinter import *
from tkinter import ttk
import re
from db_connection import cursor
from variables import db_fields, database_fields, product_name_field, part_number_field, description_field
from gui_funcs import GuiFuncs
from db_functions import DatabaseFunctions

funcProvider = GuiFuncs()
dbFuncProvider = DatabaseFunctions()


class CustomTreeview(ttk.Treeview):
    columns = []
    fields = []  # fields in database

    def __init__(self, master, columns, show="headings", height=30, row=2, column=0):
        super().__init__(master, columns=columns, show=show, height=height)

        # setting the attributes
        self.columns = columns

        # setting the corresponding database fields
        self.fields = [database_fields[field][0] for field in self.columns]

        # setting up the scrollbar
        self.scroll_bar = ttk.Scrollbar(
            master, orient='vertical', command=self.yview)
        self.configure(yscroll=self.scroll_bar.set)
        self.scroll_bar.grid(row=row, column=2, sticky='ns')

        for cols in columns:
            # .title() will capitalize the first letter
            self.heading(cols, text=cols.title())
            
        # extracting the length of the columns in database, using regex
        pattern = r'[a-zA-Z]+\((\d+)\)'  # this will extract numbers from varchar(244), 
        length_strs = [database_fields[val][1] for val in columns] # extracting only datatype(length) from database_fields dict, based on our columns
        lengths = []
        
        for eachStr in length_strs:
            r = re.search(pattern, eachStr)
            if r: # if there is a match, then our length extracted will be stored in r[1]
                lengths.append(r[1])
            else: # if there is no match, in case of "int", re.search returns None, so for none values we set column width = 60
                lengths.append(60)
                
        
        # setting up column widths
        for i in range(len(columns)):
            self.column(columns[i], width=lengths[i])

        # placing the treeview on grid
        self.grid(row=row, column=column)

    def search(self, to_search, table, sort_by=None, special_data=[], special_search=False):
        parameter = '%' + f'{to_search}' + '%'
        if to_search != 0:
            try:
                self.delete(*self.get_children())
                if not sort_by:  # if user did'nt provided sort by field then we will use product_name, desc, part_Number by default
                    conditions = {
                        product_name_field: ['LIKE', parameter, 'OR'],
                        part_number_field: ['LIKE', parameter, 'OR'],
                        description_field: ['LIKE', parameter]
                    }

                else:
                    conditions = {
                        sort_by: ['LIKE', parameter]
                    }

                if not special_search:

                    fetch_list = dbFuncProvider.fetch(
                        table=table, field_list=self.fields, conditions=conditions)

                    # db_fields - 1 cuz we dont have image info
                    for i in range(0, len(fetch_list), db_fields-1):
                        fetch_list[i] = funcProvider.system_to_english_date_format(
                            fetch_list[i])  # converting the system dates to english format
                        self.insert(
                            '', 'end', values=fetch_list[i: i+db_fields-1])

                else:
                    product_names_list = dbFuncProvider.fetch(
                        table=table, field_list=['product_name'], conditions=conditions)

                    length = int(len(special_data) / 2)
                    # can use after also,
                    before_list = special_data[0: length]
                    after_list = special_data[length:]  # can use after also,

                    for product_name in product_names_list:
                        for index in range(len(before_list)):
                            if product_name == before_list[index][1]:
                                self.insert(
                                    '', 'end', values=before_list[index], tags=('oddrow'))
                                self.insert(
                                    '', 'end', values=after_list[index], tags=('evenrow'))

            except TypeError:
                pass