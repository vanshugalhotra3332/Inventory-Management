from math import prod
from tkinter import *
from tkinter import ttk
import itertools
from db_connection import cursor, connection
from variables import db_fields

class CustomTreeview(ttk.Treeview):
    def __init__(self, master, columns, show="headings", height=30, row=2, column=0):
        super().__init__(master, columns=columns, show=show, height=height)
        
        # setting up the scrollbar
        self.scroll_bar = ttk.Scrollbar(
            master, orient='vertical', command=self.yview)
        self.configure(yscroll=self.scroll_bar.set)
        self.scroll_bar.grid(row=row, column=2, sticky='ns')

        for cols in columns:
            # .title() will capitalize the first letter
            self.heading(cols, text=cols.title())

        # setting up column widths
        self.column(columns[0], width=80)
        self.column(columns[1], width=220)
        self.column(columns[2], width=80)
        self.column(columns[3], width=120)
        self.column(columns[4], width=180)
        self.column(columns[5], width=80)
        self.column(columns[6], width=80)
        self.column(columns[7], width=60)
        self.column(columns[8], width=240)
        self.column(columns[9], width=60)
        self.column(columns[10], width=60)

        # placing the treeview on grid
        self.grid(row=row, column=column)
        
    def search(self, sort_by, to_search, table, special_data=[], special_search=False):
        parameter = '%' + f'{to_search}' + '%'
        if to_search != 0:
            try:
                self.delete(*self.get_children())
                
                if not special_search:
                    command_ = f"SELECT date, product_name, tractor,brand_name,part_number,code,mrp,box_no,description,quantity,warning_qty FROM {table} WHERE {sort_by} LIKE '{parameter}'"
                    cursor.execute(command_)
                    fetch = cursor.fetchall()
                    fetch_list = list(itertools.chain(*fetch))
                                                
                    for i in range(0, len(fetch_list), db_fields-1): # db_fields - 1 cuz we dont have image info
                        self.insert('', 'end', values=fetch_list[i: i+db_fields-1])
                        
                else:
                    command = f"SELECT product_name FROM {table} WHERE {sort_by} LIKE '{parameter}'"
                    cursor.execute(command)
                    fetch = cursor.fetchall()
                    product_names_list = list(itertools.chain(*fetch))
                                
                    length = int(len(special_data) / 2)
                    before_list = special_data[0 : length] # can use after also,
                    after_list = special_data[length:] # can use after also,
                    
                    for product_name in product_names_list:
                        for index in range(len(before_list)):
                            if product_name == before_list[index][1]:
                                self.insert('', 'end', values=before_list[index], tags=('oddrow'))
                                self.insert('', 'end', values=after_list[index], tags=('evenrow'))
                            

            except TypeError:
                pass