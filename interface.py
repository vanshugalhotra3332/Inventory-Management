from tkinter import *
from tkinter import ttk
import itertools
from db_connection import cursor, connection

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
        
    def search(self, sort_by, to_search, total_data, table):
                parameter = '%' + f'{to_search}' + '%'
                if to_search != 0:
                    try:
                        self.delete(*self.get_children())
                        command_ = f"SELECT product_name FROM {table} WHERE {sort_by} LIKE '{parameter}'"
                        cursor.execute(command_)
                        fetch = cursor.fetchall()
                        fetch_list = list(itertools.chain(*fetch))
                        for names in fetch_list:
                            for items in total_data:
                                if names == items[1]:  # items[1] represents the product_name
                                    self.insert('', 'end', values=items)
                                    self.column('Date', width=80)
                                    self.column('Product Name', width=220)
                                    self.column('Tractor', width=80)
                                    self.column('Brand Name', width=120)
                                    self.column('Part No.', width=180)
                                    self.column('Code', width=80)
                                    self.column('MRP', width=80)
                                    self.column('box_no', width=60)
                                    self.column('Description', width=240)
                                    self.column('Quantity', width=60)
                                    self.column('Warning Qty', width=60)

                    except TypeError:
                        pass