from dataclasses import field
from math import prod
from shelve import DbfilenameShelf
import subprocess
import datetime
import os
import tkinter.messagebox
from tkinter import filedialog, ttk
from tkinter import *
from db_connection import cursor, connection
from gui_funcs import GuiFuncs
from register_brand import RegisterBrand
from db_functions import DatabaseFunctions
from variables import MYSQL_BIN, file_name, cur_wd, DB_FILE_DIR, database, file_name_xl, ICON_PATH, password, product_name_field, tractor_field, brand_name_field, part_number_field, code_field, mrp_field, box_no_field, description_field, quantity_field, warning_qty_field, date_field, image_field

from initialize import init_dirs
from interface import CustomTreeview

# init_dirs()  # initializing directories in use

try:
    from tkcalendar import Calendar
    import mysql.connector as mysql
    import pandas

except ModuleNotFoundError:  # installing dependencies
    subprocess.call(['pip', 'install', '-r', f'{cur_wd}//requirements.txt'])
    from tkcalendar import Calendar
    import mysql.connector as mysql
    import pandas


class StoreBook:
    def __init__(self):
        self.root = root
        self.root.title('Store Book')
        self.root.geometry('1500x900')

        style = ttk.Style()

        # ________________________variables

        # Objects
        Registrar = RegisterBrand()
        guiFuncProvider = GuiFuncs()
        dbFuncProvider = DatabaseFunctions()

        # formatting
        button_color = 'gold2'
        button_font = 'proxima'
        button_size = 17
        cal_text = "📆"  # type text if doesn't support unicode
        img_text = "pick"  # type text if doesn't support unicode

        # dates etc
        now = datetime.datetime.now()
        cur_year = now.year
        cur_month = now.month
        cur_day = now.day
        current_date = datetime.date.today()

        if cur_month < 10:
            cur_month = f'0{cur_month}'

        cur_date_list = [f'{cur_year}-{cur_month}-{cur_day}']
        print(cur_date_list)
        today_date = guiFuncProvider.convert_all_dates_to_english(
            cur_date_list)

        # string vars
        add_product_name = StringVar()
        add_tractor_name = StringVar()
        add_brand_name = StringVar()
        add_part_no = StringVar()
        add_code = StringVar()
        add_mrp = StringVar()
        add_box_no = StringVar()
        add_description = StringVar()
        add_quantity = StringVar()
        add_warning_qty = StringVar()
        add_date = StringVar()
        add_img = StringVar()

        brand_name_ = StringVar()
        old_brand_name = StringVar()
        new_brand_name = StringVar()
        inv_search = StringVar()

        up_product_name = StringVar()
        up_tractor_name = StringVar()
        up_brand_name = StringVar()
        up_part_no = StringVar()
        up_code = StringVar()
        up_mrp = StringVar()
        up_box_no = StringVar()
        up_description = StringVar()
        up_quantity = StringVar()
        up_warning_qty = StringVar()
        up_date = StringVar()
        up_img = StringVar()

        part_ind = StringVar()
        mrp_ind = StringVar()
        pdf_ind = StringVar()

        del_product_name = StringVar()

        updation_search = StringVar()
        deletion_search = StringVar()
        addition_search = StringVar()
        si_search = StringVar()
        so_search = StringVar()

        treeview_columns = ['Date', 'Product Name', 'Tractor', 'Brand Name', 'Part No.', 'Code', 'MRP',
                            'Box', 'Description', 'Quantity', 'Warning Qty']

        update_fields = [tractor_field, code_field, mrp_field, box_no_field,
                         description_field, quantity_field, warning_qty_field, date_field, image_field]

        # __________________________________styling___________________________________________________
        style.configure("Treeview",
                        background='mint cream',
                        foreground='black',
                        rowheight=25,
                        feildbackground='snow')

        style.map('Treeview',
                  background=[('selected', 'gray21')])

        # ____________________________________________________functions_________________________________________________________________________
        def export_db(direc):
            # changing the directory to MYSQL Bin folder where mysqldump is located
            os.chdir(MYSQL_BIN)
            # export
            os.system(
                f'mysqldump -u root -p%s {database} > "{direc}"' % password)
            tkinter.messagebox.showinfo(
                'Success!', 'Database File Saved Successfully')
            os.chdir(cur_wd)

        def end_func():
            dir_ = DB_FILE_DIR + f'\\{file_name}'
            dir_xl = DB_FILE_DIR + f'\\{today_date}{file_name_xl}'
            export_db(dir_)
            export_xlsx(dir_xl)
            os.chdir(DB_FILE_DIR)
            # os.system(f'echo y| cacls {file_name} /P everyone:n')  # locking the database file to avoid unintended deletion or updation
            connection.commit()
            root.destroy()

        def exit_system(screen):
            if screen == root:
                ans = tkinter.messagebox.askyesno(
                    'Quit!', 'Confirm If You Want To Exit!')
                if ans is True:
                    end_func()
            else:
                screen.destroy()

        def reset(*str_vars):
            for StringVars in str_vars:
                StringVars.set('')

        def save_db(_event=None):
            files = [('MySQL Database File', '.sql')]
            save_path_ = filedialog.asksaveasfilename(
                filetypes=files, initialdir=cur_wd)
            save_path = str(save_path_) + '.sql'
            if len(save_path) != 0:
                export_db(save_path)

        def register_brand_finally(_event=None):
            brand_name__ = brand_name_.get()
            Registrar.register_brand(brand_name__)
            brand_name_.set('')
            brand_window.destroy()

        def update_brand_finally():
            old_name = old_brand_name.get()
            new_name = new_brand_name.get()
            Registrar.update_brand(old_name, new_name)

        def delete_product_finally(_event=None):
            del_name = del_product_name.get()
            all_products = dbFuncProvider.fetch('stock', [product_name_field])

            all_products = [products.lower() for products in all_products]

            if del_name.lower() in all_products:
                permission = tkinter.messagebox.askyesno(
                    'Permission Required!', f"Confirm to delete product'{del_name}'")
                if permission is True:
                    # sending data to recently deleted table
                    conditions = {
                        product_name_field: ['=', del_name]
                    }
                    # this command will be like, SELECT * from stock WHERE product_name = 'del_name'
                    del_data_ = dbFuncProvider.fetch(
                        table='stock', conditions=conditions)

                    del_data = del_data_.copy()

                    del_data[10] = str(current_date)

                    rd_tractor = del_data[1]
                    rd_code = del_data[4]
                    rd_mrp = del_data[5]
                    rd_box = del_data[6]
                    rd_desc = del_data[7]
                    rd_qty = del_data[8]
                    rd_war = del_data[9]
                    rd_img = del_data[11]
                    if rd_qty == 0:  # if quantity for product is 0 then and only then it can be deleted

                        dbFuncProvider.delete(
                            table='stock', conditions=conditions)
                        dbFuncProvider.delete(
                            table='recently_added', conditions=conditions)
                        dbFuncProvider.delete(
                            table='stock_in', conditions=conditions)
                        try:
                            dbFuncProvider.insert(
                                table="recently_deleted", data=del_data)

                        except mysql.errors.IntegrityError:  # if we have deleted this product already, then we will just update the data
                            values = [rd_tractor, rd_code, rd_mrp, rd_box,
                                      rd_desc, rd_qty, rd_war, str(current_date), rd_img]

                            conditions = {product_name_field: ['=', del_name]}

                            dbFuncProvider.update(
                                table="recently_deleted", fields=update_fields, values=values, conditions=conditions)

                            tkinter.messagebox.showinfo(
                                'Success!', f"Product '{del_name}' delete successfully!")
                            delete_window.destroy()

                    else:
                        tkinter.messagebox.showerror(
                            'Error!', f"Quantity for Product '{del_name}' is not 0 so Product can't be deleted")

            else:
                tkinter.messagebox.showerror(
                    'Error!', f"'{del_name}' product name doesn't exists")
                guiFuncProvider.focus_on(delete_window)

        def recently_added():
            reca_window = Toplevel(root)
            reca_window.title('Recently Added Records')
            reca_window.geometry('1350x1000')

            # top label
            lbl_name = Label(reca_window, text="Recently Added Records", font=('arial', 30, 'bold'),
                             padx=2, pady=2, bd=2)
            lbl_name.grid(row=0, column=0)

            def search_(sort_by):
                searched = addition_search.get()
                reca_treeview.search(
                    sort_by=sort_by, to_search=searched, table="recently_added")

            """menu button________________________"""
            menu_bar = ttk.Menubutton(
                reca_window, text='Sort By', cursor='mouse')
            menu_bar.grid(row=1, column=2)
            menu_ = Menu(menu_bar, tearoff=0)
            menu_bar["menu"] = menu_
            menu_.add_command(
                label='Brand Name', command=lambda sort_by=brand_name_field: search_(sort_by))
            menu_.add_command(
                label='MRP', command=lambda sort_by=mrp_field: search_(sort_by))
            menu_.add_command(label='Box Number',
                              command=lambda sort_by=box_no_field: search_(sort_by))
            menu_.add_command(
                label='date', command=lambda sort_by=date_field: search_(sort_by))

            # treeview
            global reca_treeview
            reca_treeview = CustomTreeview(
                reca_window, columns=treeview_columns)

            # search bar
            sb_entry = Entry(
                reca_window, textvariable=addition_search, width=110, font=('arial', 15))
            sb_entry.grid(row=1, column=0)

            sb_entry.bind('<KeyRelease>', lambda event,
                          sort_by=None: search_(sort_by))
            search_btn = Button(reca_window, text="Search", bd=1, pady=1, padx=1,
                                relief=RIDGE, overrelief=SUNKEN, cursor='mouse', font=('arial', 8, 'italic'),
                                bg='snow')
            search_btn.grid(row=1, column=1)

            # adding data to treeview fetching from table
            global total_data
            total_data = dbFuncProvider.custom_fetching(table='recently_added')
            for treeview_data in total_data:
                reca_treeview.insert('', 'end', values=treeview_data)

        def recently_deleted():
            rec_window = Toplevel(root)
            rec_window.title('Recently Deleted Records')
            rec_window.geometry('1350x1000')

            # top label
            lbl_name = Label(rec_window, text="Recently deleted Records", font=('arial', 30, 'bold'),
                             padx=2, pady=2, bd=2)
            lbl_name.grid(row=0, column=0)

            def search_(sort_by):
                searched = deletion_search.get()
                rec_treeview.search(
                    sort_by=sort_by, to_search=searched, table="recently_deleted")

            """menu button________________________"""
            menu_bar = ttk.Menubutton(
                rec_window, text='Sort By', cursor='mouse')
            menu_bar.grid(row=1, column=2)
            menu_ = Menu(menu_bar, tearoff=0)
            menu_bar["menu"] = menu_
            menu_.add_command(
                label='Brand Name', command=lambda sort_by=brand_name_field: search_(sort_by))
            menu_.add_command(
                label='MRP', command=lambda sort_by=mrp_field: search_(sort_by))
            menu_.add_command(label='Box Number',
                              command=lambda sort_by=box_no_field: search_(sort_by))
            menu_.add_command(
                label='date', command=lambda sort_by=date_field: search_(sort_by))

            # treeview
            global rec_treeview
            rec_treeview = CustomTreeview(rec_window, columns=treeview_columns)

            # search bar
            sb_entry = Entry(
                rec_window, textvariable=deletion_search, width=110, font=('arial', 15))
            sb_entry.grid(row=1, column=0)

            sb_entry.bind('<KeyRelease>', lambda event,
                          sort_by=None: search_(sort_by))
            search_btn = Button(rec_window, text="Search", bd=1, pady=1, padx=1,
                                relief=RIDGE, overrelief=SUNKEN, cursor='mouse', font=('arial', 8, 'italic'),
                                bg='snow')
            search_btn.grid(row=1, column=1)

            # adding data to treeview fetching from table
            global total_data
            total_data = dbFuncProvider.custom_fetching(
                table='recently_deleted')
            for treeview_data in total_data:
                rec_treeview.insert('', 'end', values=treeview_data)

        def updation_transactions(_event=None):
            tran_window = Toplevel(root)
            tran_window.title('Recent Updation Records')
            tran_window.geometry('1350x1000')

            before_color = 'light blue'
            after_color = 'pale turquoise'

            # top label
            lbl_name = Label(tran_window, text="Updation Records", font=('arial', 30, 'bold'),
                             padx=2, pady=2, bd=2)
            lbl_name.grid(row=0, column=0)

            lbl_name = Label(tran_window, text="Before: ", font=('arial', 15, 'bold'),
                             padx=2, pady=2, bd=2, background=before_color)
            lbl_name.grid(row=1, column=0)
            lbl_name = Label(tran_window, text="  After:  ", font=('arial', 15, 'bold'),
                             padx=2, pady=2, bd=2, background=after_color)
            lbl_name.grid(row=2, column=0)

            def _search_(sort_by):
                searched = updation_search.get()
                tran_treeview.search(sort_by=sort_by, to_search=searched,
                                     table="before_update", special_data=total, special_search=True)

            """menu button________________________"""
            menu_bar = ttk.Menubutton(
                tran_window, text='Sort By', cursor='mouse')
            menu_bar.grid(row=3, column=2)
            menu_ = Menu(menu_bar, tearoff=0)
            menu_bar["menu"] = menu_
            menu_.add_command(
                label='Brand Name', command=lambda sort_by=brand_name_field: _search_(sort_by))
            menu_.add_command(
                label='MRP', command=lambda sort_by=mrp_field: _search_(sort_by))
            menu_.add_command(
                label='Box Number', command=lambda sort_by=box_no_field: _search_(sort_by))
            menu_.add_command(
                label='date', command=lambda sort_by=date_field: _search_(sort_by))

            # treeview
            global tran_treeview
            tran_treeview = CustomTreeview(
                tran_window, columns=treeview_columns, row=4)

            # search bar
            sb_entry = Entry(
                tran_window, textvariable=updation_search, width=110, font=('arial', 15))
            sb_entry.grid(row=3, column=0)

            search_btn = Button(tran_window, text="Search", bd=1, pady=1, padx=1,
                                relief=RIDGE, overrelief=SUNKEN, cursor='mouse', font=('arial', 8, 'italic'),
                                bg='snow')
            search_btn.grid(row=3, column=1)
            sb_entry.bind('<KeyRelease>', lambda event,
                          sort_by=None: _search_(sort_by))

            tran_treeview.tag_configure('oddrow', background=before_color)
            tran_treeview.tag_configure('evenrow', background=after_color)

            # getting data from database to add in treeview
            before_data = dbFuncProvider.custom_fetching(table='before_update')
            after_data = dbFuncProvider.custom_fetching(table='after_update')
            global total
            total = before_data + after_data

            length = int(len(total) / 2)
            for i in range(0, length):
                tran_treeview.insert(
                    '', 'end', values=total[i], tags=('oddrow'))
                tran_treeview.insert(
                    '', 'end', values=total[i + length], tags=('evenrow'))

        def stock_in():
            si_window = Toplevel(root)
            si_window.title('Stock INs')
            si_window.geometry('1350x1000')

            # top label
            lbl_name = Label(si_window, text="Stock INs", font=('arial', 30, 'bold'),
                             padx=2, pady=2, bd=2)
            lbl_name.grid(row=0, column=0)

            def search_(sort_by):
                searched = si_search.get()
                si_treeview.search(
                    sort_by=sort_by, to_search=searched, table="stock_in")

            """menu button________________________"""
            menu_bar = ttk.Menubutton(
                si_window, text='Sort By', cursor='mouse')
            menu_bar.grid(row=1, column=2)
            menu_ = Menu(menu_bar, tearoff=0)
            menu_bar["menu"] = menu_
            menu_.add_command(
                label='Brand Name', command=lambda sort_by=brand_name_field: search_(sort_by))
            menu_.add_command(
                label='MRP', command=lambda sort_by=mrp_field: search_(sort_by))
            menu_.add_command(label='Box Number',
                              command=lambda sort_by=box_no_field: search_(sort_by))
            menu_.add_command(
                label='date', command=lambda sort_by=date_field: search_(sort_by))

            # treeview
            global si_treeview
            si_treeview = CustomTreeview(si_window, columns=treeview_columns)
            # search bar
            sb_entry = Entry(si_window, textvariable=si_search,
                             width=110, font=('arial', 15))
            sb_entry.grid(row=1, column=0)

            sb_entry.bind('<KeyRelease>', lambda event,
                          sort_by=None: search_(sort_by))
            search_btn = Button(si_window, text="Search", bd=1, pady=1, padx=1,
                                relief=RIDGE, overrelief=SUNKEN, cursor='mouse', font=('arial', 8, 'italic'),
                                bg='snow')
            search_btn.grid(row=1, column=1)

            # adding data to treeview fetching from table
            global total_data
            total_data = dbFuncProvider.custom_fetching(table='stock_in')
            for treeview_data in total_data:
                si_treeview.insert('', 'end', values=treeview_data)

        def stock_out():
            so_window = Toplevel(root)
            so_window.title('Stock OUTs')
            so_window.geometry('1350x1000')

            # top label
            lbl_name = Label(so_window, text="Stock OUTs", font=('arial', 30, 'bold'),
                             padx=2, pady=2, bd=2)
            lbl_name.grid(row=0, column=0)

            def search_(sort_by):
                searched = so_search.get()
                so_treeview.search(
                    sort_by=sort_by, to_search=searched, table="stock_out")

            """menu button________________________"""
            menu_bar = ttk.Menubutton(
                so_window, text='Sort By', cursor='mouse')
            menu_bar.grid(row=1, column=2)
            menu_ = Menu(menu_bar, tearoff=0)
            menu_bar["menu"] = menu_
            menu_.add_command(
                label='Brand Name', command=lambda sort_by=brand_name_field: search_(sort_by))
            menu_.add_command(
                label='MRP', command=lambda sort_by=mrp_field: search_(sort_by))
            menu_.add_command(label='Box Number',
                              command=lambda sort_by=box_no_field: search_(sort_by))
            menu_.add_command(
                label='date', command=lambda sort_by=date_field: search_(sort_by))

            # treeview
            global so_treeview
            so_treeview = CustomTreeview(so_window, columns=treeview_columns)

            # search bar
            sb_entry = Entry(so_window, textvariable=so_search,
                             width=110, font=('arial', 15))
            sb_entry.grid(row=1, column=0)

            sb_entry.bind('<KeyRelease>', lambda event,
                          sort_by=None: search_(sort_by))
            search_btn = Button(so_window, text="Search", bd=1, pady=1, padx=1,
                                relief=RIDGE, overrelief=SUNKEN, cursor='mouse', font=('arial', 8, 'italic'),
                                bg='snow')
            search_btn.grid(row=1, column=1)

            # adding data to treeview fetching from table
            global total_data
            total_data = dbFuncProvider.custom_fetching(table='stock_out')
            for treeview_data in total_data:
                so_treeview.insert('', 'end', values=treeview_data)

        # TODO: Improve this function, finding only product_name is difficult
        def delete_product(_event=None):
            global delete_window
            delete_window = Toplevel(root)
            delete_window.title('Delete Product')
            delete_window.geometry('1000x400')

            lbl_name = Label(delete_window, text="Delete Product Name", font=(
                'arial', 30, 'bold'), padx=2, pady=2, bd=2)
            lbl_name.grid(row=0, column=0)

            lbl_name = Label(delete_window, text='Product Name:*', font=('arial', 15, 'bold'),
                             padx=2, pady=2, bd=2)
            lbl_name.grid(row=1, column=0)

            entry_del = Entry(delete_window, width=40, textvariable=del_product_name, font=('arial', 15, 'bold'),
                              cursor='xterm', state='normal')
            entry_del.grid(row=1, column=1)
            entry_del.focus()

            add_btn = Button(delete_window, text="Delete", bd=3, pady=1, padx=1,
                             relief=RIDGE, overrelief=SUNKEN, cursor='plus', font=('arial', 15, 'bold', 'italic'),
                             bg=button_color, command=delete_product_finally)
            add_btn.grid(row=2, column=1)
            delete_window.bind('<Control-x>', delete_product_finally)

        def register_brand_name(_event=None):
            global brand_window
            brand_window = Toplevel(root)
            brand_window.title('Register Brand Name')
            brand_window.geometry('950x400')

            lbl_name = Label(brand_window, text="Register Brand Name", font=(
                'arial', 30, 'bold'), padx=2, pady=2, bd=2)
            lbl_name.grid(row=0, column=0)

            lbl_name = Label(brand_window, text='Brand Name:*', font=('arial', 15, 'bold'),
                             padx=2, pady=2, bd=2)
            lbl_name.grid(row=1, column=0)

            entry_nmw = Entry(brand_window, width=40, textvariable=brand_name_, font=('arial', 15, 'bold'),
                              cursor='xterm', state='normal')
            entry_nmw.grid(row=1, column=1)
            entry_nmw.focus()

            add_btn = Button(brand_window, text="Register", bd=3, pady=1, padx=1,
                             relief=RIDGE, overrelief=SUNKEN, cursor='plus', font=('arial', 15, 'bold', 'italic'),
                             bg=button_color, command=register_brand_finally)
            add_btn.grid(row=2, column=1)
            brand_window.bind('<Control-e>', register_brand_finally)

        def update_brand_name(_event=None):
            global brand_window_
            brand_window_ = Toplevel(root)
            brand_window_.title('Update Brand Name')
            brand_window_.geometry('950x400')

            lbl_name = Label(brand_window_, text="Update Brand Name", font=(
                'arial', 30, 'bold'), padx=2, pady=2, bd=2)
            lbl_name.grid(row=0, column=0)
            guiFuncProvider.custom_entry_labels(
                brand_window_, text=' Old Brand Name:', r=1, var=old_brand_name)
            guiFuncProvider.custom_entry_labels(
                brand_window_, text=' New Brand Name:', r=2, var=new_brand_name)

            add_btn = Button(brand_window_, text="Update", bd=3, pady=1, padx=1,
                             relief=RIDGE, overrelief=SUNKEN, cursor='plus', font=('arial', 15, 'bold', 'italic'),
                             bg=button_color, command=update_brand_finally)
            add_btn.grid(row=3, column=1)

        def update_mrp_finally():
            guiFuncProvider.focus_on(mrp_window, state=False)
            part_column = part_ind.get()
            mrp_column = mrp_ind.get()
            file_path = pdf_ind.get()

            db_part_numbers = dbFuncProvider.fetch(
                table='stock', field_list=['part_number'])

            if file_path != '':
                record_df = pandas.read_excel(file_path, sheet_name=0)
                try:
                    excel_parts = record_df[part_column].tolist()
                    for i in range(len(excel_parts)):
                        excel_parts[i] = str(excel_parts[i]).lower()

                    db_part = []
                    for i in range(len(db_part_numbers)):
                        if db_part_numbers[i].lower() in excel_parts:
                            db_part.append(db_part_numbers[i])

                    mrp_part = []
                    for part_no in db_part:
                        mrp_record = record_df[record_df[part_column].str.lower(
                        ) == part_no]
                        mrp_list = mrp_record[mrp_column].tolist()
                        mrp_part.append(mrp_list)

                    mrp_list_needed = []
                    for sublists in mrp_part:
                        for item in sublists:
                            mrp_list_needed.append(item)

                    # dictionary comprehension to create key value pair or part number and mrp
                    part_mrp_dict = {db_part[i]: mrp_list_needed[i]
                                     for i in range(len(db_part))}
                    print(part_mrp_dict)

                    for part_no in part_mrp_dict:
                        dbFuncProvider.update(table='stock', fields=[mrp_field], values=[part_mrp_dict[part_no]], conditions={
                            part_number_field: ['=', part_no]
                        })

                    guiFuncProvider.focus_on(mrp_window, state=False)
                    tkinter.messagebox.showinfo(
                        'Success!', f'Total {len(part_mrp_dict)} Records Updated!')
                    mrp_window.destroy()

                except KeyError:
                    tkinter.messagebox.showerror(
                        'Error', f"Column Name for Part Number '{part_column}' or for MRP '{mrp_column}' is wrong!")
                    guiFuncProvider.focus_on(mrp_window)

            else:
                tkinter.messagebox.showerror('Error!', 'No File Chosen!')
                guiFuncProvider.focus_on(mrp_window)

        def update_mrp(_event=None):
            def pdf_picker():
                files = [('Microsoft Excel File', '.xlsx'),
                         ('Microsoft Excel File', '.xls')]
                open_path_ = filedialog.askopenfilename(
                    filetypes=files, initialdir=cur_wd)
                pdf_ind.set(open_path_)
                guiFuncProvider.focus_on(mrp_window)

            global mrp_window
            mrp_window = Toplevel(root)
            mrp_window.title('Update MRP')
            mrp_window.geometry('800x500')

            lbl_name = Label(mrp_window, text="Update MRP", font=(
                'arial', 30, 'bold'), padx=2, pady=2, bd=2)
            lbl_name.grid(row=0, column=0)

            guiFuncProvider.custom_entry_labels(
                mrp_window, text='Part Number Column Name:', var=part_ind, r=2)
            guiFuncProvider.custom_entry_labels(
                mrp_window, text='MRP Column Name:', var=mrp_ind, r=3)
            guiFuncProvider.custom_entry_labels(
                mrp_window, text='Excel File:', var=pdf_ind, r=4, state='disabled')

            cal_btn = Button(mrp_window, text=img_text, bd=3, pady=1, padx=1,
                             font=('arial', 10, 'bold'), relief=FLAT, overrelief=RIDGE,
                             command=pdf_picker)
            cal_btn.grid(row=4, column=2)

            add_btn = Button(mrp_window, text="Update", bd=3, pady=1, padx=1,
                             relief=RIDGE, overrelief=SUNKEN, cursor='spider', font=('arial', 15, 'bold', 'italic'),
                             bg=button_color, command=update_mrp_finally)
            add_btn.grid(row=5, column=1)

        def total_stock(_event=None):
            stock_list = dbFuncProvider.fetch(
                table='stock', field_list=[f'SUM({mrp_field}*{quantity_field})'])
            tkinter.messagebox.showinfo(
                'Total Stock!', f'Total Stock is Rs. {stock_list[0]}')

        def export_xlsx(save_dir):
            # by default it fetches all items
            record_list = dbFuncProvider.fetch('stock')

            # slicing all product names from list
            slice_product_name = slice(0, len(record_list), 12)
            # slicing all tractor from list
            slice_tractor = slice(1, len(record_list), 12)
            # slicing all brand names from list
            slice_brand_name = slice(2, len(record_list), 12)
            # slicing all part numbers from list
            slice_part_no = slice(3, len(record_list), 12)
            # slicing all code  from list
            slice_code = slice(4, len(record_list), 12)
            # slicing all mrp from list
            slice_mrp = slice(5, len(record_list), 12)
            # slicing all box_no from list
            slice_box_no = slice(6, len(record_list), 12)
            # slicing all description from list
            slice_desc = slice(7, len(record_list), 12)
            # slicing all quantity from list
            slice_qty = slice(8, len(record_list), 12)
            slice_warning_qty = slice(9, len(record_list), 12)
            # slicing all date from list
            slice_date = slice(10, len(record_list), 12)
            # slicing all img from list
            slice_img = slice(11, len(record_list), 12)

            product_name_list = record_list[slice_product_name]
            tractor_list = record_list[slice_tractor]
            brand_name_list = record_list[slice_brand_name]
            part_no_list = record_list[slice_part_no]
            code_list = record_list[slice_code]
            mrp_list = record_list[slice_mrp]
            box_no_list = record_list[slice_box_no]
            desc_list = record_list[slice_desc]
            qty_list = record_list[slice_qty]
            warning_qty = record_list[slice_warning_qty]
            date_list = record_list[slice_date]
            img_list = record_list[slice_img]

            data_dict = {
                'Product Name': product_name_list,

                'Quantity': qty_list,  # change of order

                'Brand': brand_name_list,
                'Part Number': part_no_list,
                'Code': code_list,
                'MRP': mrp_list,
                'Box Number': box_no_list,
                'Description': desc_list,
                'Tractor': tractor_list,  # change of order
                'Warning Quantity': warning_qty,
                'Date': date_list,
                'Image': img_list
            }

            if len(save_dir) != 0:
                try:
                    writer = pandas.ExcelWriter(save_dir, engine='xlsxwriter')
                except ModuleNotFoundError:
                    subprocess.call(["pip", "install", "xlsxwriter"])
                    writer = pandas.ExcelWriter(save_dir, engine='xlsxwriter')
                columns = []
                for j in data_dict.keys():
                    columns.append(j)

                index_ = [i for i in range(len(product_name_list))]
                df = pandas.DataFrame(data_dict, index=index_)
                df.to_excel(writer, sheet_name='Records',
                            index=False, columns=columns)

                workbook = writer.book
                box_format = workbook.add_format({
                    'bg_color': '#00FFFF',  # your setting
                    'bold': True,           # additional stuff...
                    'text_wrap': True,
                    'valign': 'top',
                    'align': 'center',
                    'border': 1})

                worksheet = writer.sheets['Records']
                worksheet.set_column('A:A', 65)  # for product name
                worksheet.set_column('B:B', 15)  # for qty
                worksheet.set_column('C:C', 20)  # for brand
                worksheet.set_column('D:D', 30)     # for part
                worksheet.set_column('E:E', 15)   # for code
                worksheet.set_column('F:F', 15)     # mrp
                worksheet.set_column('G:G', 25, box_format)     # box
                worksheet.set_column('H:H', 40)     # desc
                worksheet.set_column('I:I', 10)         # tractor
                worksheet.set_column('J:J', 10)     # warning
                worksheet.set_column('K:K', 20)  # date
                worksheet.set_column('L:L', 40)  # img

                # Add a header format.
                qty_format = workbook.add_format({
                    'bg_color': '#FFFF00',  # your setting
                    'bold': True,           # additional stuff...
                    'text_wrap': True,
                    'valign': 'top',
                    'align': 'center',
                    'border': 1})

                worksheet.conditional_format(f'B1:B{len(index_)+1}', {'type':     'cell',
                                                                      'criteria': '>',
                                                                      'value':    0,
                                                                      'format':   qty_format})

                mrp_format = workbook.add_format({
                    'bg_color': '#00FF00',  # your setting
                    'bold': True,           # additional stuff...
                    'text_wrap': True,
                    'valign': 'top',
                    'align': 'center',
                    'border': 1})

                worksheet.conditional_format(f'F1:F{len(index_)+1}', {'type': 'cell',
                                                                      'criteria': '>',
                                                                      'value':    0,
                                                                      'format':   mrp_format})

                writer.save()
                connection.commit()
                tkinter.messagebox.showinfo(
                    'Success!', 'File Saved Successfully!')

        def save_xlsx(_event=None):
            files = [('Microsoft Excel File', '.xlsx')]
            save_path_ = filedialog.asksaveasfilename(
                filetypes=files, initialdir=cur_wd)
            save_path = str(save_path_) + '.xlsx'
            export_xlsx(save_path)

        def check_warnings(_event=None):
            treeview.delete(*treeview.get_children())
            output_list = dbFuncProvider.fetch(
                'stock', field_list=[product_name_field, brand_name_field, quantity_field, warning_qty_field])

            list_needed = []
            i = 0
            while i < int(len(output_list)):
                a = output_list[i: i+4]
                i += 4
                list_needed.append(a)

            for sep in list_needed:
                if sep[2] < sep[3]:  # if quatity < warning_qty
                    treeview.insert('', 'end', values=sep)

        def save_warning_sheet():
            output_list = dbFuncProvider.fetch(
                'stock', field_list=[product_name_field, brand_name_field, quantity_field, warning_qty_field])

            list_needed = []

            i = 0
            while i < int(len(output_list)):
                a = output_list[i: i+4]
                i += 4
                list_needed.append(a)
            data_list_ = []
            for sep in list_needed:
                if sep[2] < sep[3]:
                    # for warning sheet
                    data_list_.append(sep[0])
                    data_list_.append(sep[1])
                    data_list_.append(sep[2])

            # slicing all product names from list
            slice_product_name = slice(0, len(data_list_), 3)

            # slicing all brand names from list
            slice_brand_name = slice(1, len(data_list_), 3)

            # slicing all quantity from list
            slice_qty = slice(2, len(data_list_), 3)

            product_name_list = data_list_[slice_product_name]

            brand_name_list = data_list_[slice_brand_name]

            qty_list = data_list_[slice_qty]

            data_dict = {
                'Product Name': product_name_list,

                'Quantity': qty_list,  # change of order

                'Brand': brand_name_list,
            }

            files = [('Microsoft Excel File', '.xlsx')]
            save_path_ = filedialog.asksaveasfilename(
                filetypes=files, initialdir=cur_wd)
            save_dir = str(save_path_) + '.xlsx'

            if len(save_dir) != 0:
                writer = pandas.ExcelWriter(save_dir, engine='xlsxwriter')
                columns = []
                for j in data_dict.keys():
                    columns.append(j)

                index_ = [i for i in range(len(product_name_list))]
                df = pandas.DataFrame(data_dict, index=index_)
                df.to_excel(writer, sheet_name='Warnings',
                            index=False, columns=columns)

                workbook = writer.book
                box_format = workbook.add_format({
                    'bg_color': '#00FFFF',  # your setting
                    'bold': True,           # additional stuff...
                    'text_wrap': True,
                    'valign': 'top',
                    'align': 'center',
                    'border': 1})

                worksheet = writer.sheets['Warnings']
                worksheet.set_column('A:A', 65)  # for product name
                worksheet.set_column('B:B', 15)  # for qty
                worksheet.set_column('C:C', 20)  # for brand

                qty_format = workbook.add_format({
                    'bg_color': '#FFFF00',  # your setting
                    'bold': True,           # additional stuff...
                    'text_wrap': True,
                    'valign': 'top',
                    'align': 'center',
                    'border': 1})

                worksheet.conditional_format(f'B1:B{len(index_)+1}', {'type':     'cell',
                                                                      'criteria': '=',
                                                                      'value':    0,
                                                                      'format':   qty_format})

                writer.save()
                connection.commit()
                tkinter.messagebox.showinfo(
                    'Success!', 'File Saved Successfully!')

        def update_finally(_event=None):
            product_name_up = up_product_name.get()
            tractor_up = up_tractor_name.get()
            brand_name_up = up_brand_name.get()
            part_no_up = up_part_no.get()
            code_up = up_code.get()
            mrp_up = up_mrp.get()
            box_no_up = up_box_no.get()
            description_up = up_description.get()
            quantity_up = up_quantity.get()   #
            warning_qty_up = up_warning_qty.get()
            img_up = up_img.get()
            date_up = str(current_date)
            update_data = [product_name_up, tractor_up, brand_name_up, part_no_up, code_up, mrp_up,
                           box_no_up, description_up, quantity_up, warning_qty_up, date_up, img_up]
            # validation
            try:
                float(mrp_up)
                float(quantity_up)
                float(warning_qty_up)

            except ValueError:
                tkinter.messagebox.showerror(
                    'Error!', 'MRP , Quantity and Warning Quantity must be number')
                guiFuncProvider.focus_on(up_screen)

            if tractor_up == '':
                tkinter.messagebox.showerror(
                    'Error!', "Tractor Name Can't be empty!")
                guiFuncProvider.focus_on(up_screen)

            elif quantity_up == '':
                tkinter.messagebox.showerror(
                    'Error!', "Quantity Can't be empty")
                guiFuncProvider.focus_on(up_screen)

            elif description_up == '':
                up_description.set(None)

            elif warning_qty_up == '':
                up_warning_qty.set(0)

            elif code_up == '':
                up_code.set(None)

            elif box_no_up == '':
                up_box_no.set(None)

            elif img_up == '':
                up_img.set(None)

            else:
                conditions = {
                    product_name_field: ['=', product_name_up]
                }

                old_data = dbFuncProvider.fetch(
                    table='stock', conditions=conditions)

                old_data[10] = str(current_date)
                old_name = old_data[0]
                old_tractor = old_data[1]
                old_code = old_data[4]
                old_mrp = old_data[5]
                old_box = old_data[6]
                old_desc = old_data[7]
                old_qty = old_data[8]
                old_war = old_data[9]

                old_img = old_data[11]
                # _________________________adding data to before_update table
                try:
                    dbFuncProvider.insert(table="before_update", data=old_data)

                except mysql.errors.IntegrityError:
                    before_values = [old_tractor, old_code, old_mrp, old_box,
                                     old_desc, old_qty, old_war, str(current_date), old_img]

                    before_conditions = {product_name_field: ['=', old_name]}

                    dbFuncProvider.update(
                        table="before_update", fields=update_fields, values=before_values, conditions=before_conditions)

                # _________________________________updating the data

                fields = [tractor_field, code_field, mrp_field, box_no_field,
                          description_field, quantity_field, warning_qty_field, image_field]

                up_values = [tractor_up, code_up, mrp_up, box_no_up,
                             description_up, quantity_up, warning_qty_up, img_up]

                values = [tractor_up, code_up, mrp_up, box_no_up, description_up,  # including
                          quantity_up, warning_qty_up, str(current_date), img_up]

                dbFuncProvider.update(
                    table="stock", fields=fields, values=up_values, conditions=conditions)

                # ___________________________adding data to after_update table
                try:
                    dbFuncProvider.insert("after_update", update_data)

                except mysql.errors.IntegrityError:
                    dbFuncProvider.update(
                        table="after_update", fields=update_fields, values=values, conditions=conditions)

                # adding data to stock_in and stock_out tables;
                table = ''
                up_data = update_data.copy()
                upd_qty = 0
                if old_qty < int(quantity_up):
                    table = 'stock_in'
                    up_data[8] = int(quantity_up) - old_qty
                    upd_qty = int(quantity_up) - old_qty

                elif old_qty > int(quantity_up):
                    table = 'stock_out'
                    up_data[8] = old_qty - int(quantity_up)
                    upd_qty = old_qty - int(quantity_up)

                else:
                    table = 'garbage'

                try:
                    dbFuncProvider.insert(table=table, data=up_data)

                except mysql.errors.IntegrityError:
                    values = [tractor_up, code_up, mrp_up, box_no_up, description_up,
                              upd_qty, warning_qty_up, str(current_date), img_up]
                    dbFuncProvider.update(
                        table=table, fields=update_fields, values=values, conditions=conditions)

                guiFuncProvider.focus_on(up_screen, state=False)
                tkinter.messagebox.showinfo(
                    'Success', f"Record '{product_name_up}' updated successfully!")
                # guiFuncProvider.focus_on(inv_screen)
                inv_screen.destroy()
                up_screen.destroy()

        def update(_event=None):
            items = records_treeview.focus()
            data = records_treeview.item(items)
            values_data = data['values']
            if len(values_data) != 0:
                try:
                    def img_picker_():
                        files = [('PNG File', '.png'), ('JPEG file', '.jpg')]
                        open_path_ = filedialog.askopenfilename(
                            filetypes=files, initialdir=cur_wd)
                        up_img.set(open_path_)

                        guiFuncProvider.focus_on(up_screen)

                    # previous values
                    up_product_name.set(values_data[1])
                    up_tractor_name.set(values_data[2])
                    up_brand_name.set(values_data[3])
                    up_part_no.set(values_data[4])
                    up_code.set(values_data[5])
                    up_mrp.set(values_data[6])
                    up_box_no.set(values_data[7])
                    up_description.set(values_data[8])
                    up_quantity.set(values_data[9])
                    up_warning_qty.set(values_data[10])
                    up_date.set(values_data[0])
                    # up_img.set(values_data[11])

                    global up_screen
                    up_screen = Toplevel(root)
                    up_screen.title("Update")
                    up_screen.geometry('1100x800')

                    # ignore frames (pretty wasting of lines for formatting)
                    main_frame__ = Frame(up_screen, bd=10)
                    main_frame__.grid()

                    top__ = Frame(main_frame__, bd=10, width=100, relief=RIDGE)
                    top__.pack(side=TOP)

                    up_ent_frame = LabelFrame(main_frame__, bd=10, width=500, height=150, font=('helvetica', 20, 'bold'),
                                              relief=RIDGE)
                    up_ent_frame.pack(side=TOP)

                    up_but_frame = LabelFrame(main_frame__, bd=10, width=700, height=400, font=('helvetica', 20, 'bold'),
                                              relief=RIDGE)
                    up_but_frame.pack(side=BOTTOM)

                    # top label
                    lbl_name = Label(top__, text="Update", font=('arial', 30, 'bold'),
                                     padx=2, pady=2, bd=2)
                    lbl_name.grid(row=0, column=0)

                    # entries
                    """____________________________product_name____________________________________"""
                    guiFuncProvider.custom_entry_labels(
                        up_ent_frame, text='Product Name:*', r=1, var=up_product_name, state='disabled')
                    """____________________________tractor_name____________________________________"""
                    guiFuncProvider.custom_entry_labels(
                        up_ent_frame, text='Tractor Name:', r=2, var=up_tractor_name)

                    """____________________________brand_name____________________________________"""
                    guiFuncProvider.custom_entry_labels(
                        up_ent_frame, text='Brand Name:*', r=3, var=up_brand_name, state='disabled')
                    """____________________________part number____________________________________"""
                    guiFuncProvider.custom_entry_labels(
                        up_ent_frame, text='Part Number:', r=4, var=up_part_no, state='disabled')

                    """____________________________code____________________________________"""
                    guiFuncProvider.custom_entry_labels(
                        up_ent_frame, text='Code:', r=5, var=up_code)

                    """____________________________mrp____________________________________"""
                    guiFuncProvider.custom_entry_labels(
                        up_ent_frame, text='MRP:*', r=6, var=up_mrp)

                    """____________________________box no____________________________________"""
                    guiFuncProvider.custom_entry_labels(
                        up_ent_frame, text='Box Number:', r=7, var=up_box_no)
                    """____________________________description____________________________________"""
                    guiFuncProvider.custom_entry_labels(
                        up_ent_frame, text='Description:', r=8, var=up_description)

                    """____________________________Quantity____________________________________"""
                    guiFuncProvider.custom_entry_labels(
                        up_ent_frame, text='Quantity:*', r=9, var=up_quantity)

                    """____________________________Warning Quantity____________________________________"""
                    guiFuncProvider.custom_entry_labels(
                        up_ent_frame, text='Warning Quantity:*', r=10, var=up_warning_qty)

                    """____________________________date____________________________________"""
                    guiFuncProvider.custom_entry_labels(
                        up_ent_frame, text='Date:', r=11, var=up_date, state='disabled')
                    """_________________________________Image_____________________________________"""
                    guiFuncProvider.custom_entry_labels(
                        up_ent_frame, text='Image:', r=12, var=up_img, state='disabled')
                    cal_btn = Button(up_ent_frame, text=img_text, bd=3, pady=1, padx=1,
                                     font=('arial', 10, 'bold'), relief=FLAT, overrelief=RIDGE,
                                     command=img_picker_)
                    cal_btn.grid(row=12, column=2)

                    add_btn = Button(up_but_frame, text="Update", bd=3, pady=1, padx=1,
                                     relief=RIDGE, overrelief=SUNKEN, cursor='plus', font=('arial', 20, 'bold', 'italic'),
                                     bg=button_color, command=update_finally)
                    add_btn.grid(row=0, column=0)

                    add_btn = Button(up_but_frame, text=" Exit  ", bd=3, pady=1, padx=1,
                                     relief=RIDGE, overrelief=SUNKEN, cursor='pirate', font=('arial', 20, 'bold', 'italic'),
                                     bg=button_color, command=lambda screen=up_screen: exit_system(screen))
                    add_btn.grid(row=0, column=1)

                except IndexError:
                    tkinter.messagebox.showerror(
                        "Can't Proceed", "Try Doing Empty Search and Then Press Control-u")
                    inv_screen.destroy()
                # shortcut key
                up_screen.bind('<Control-u>', update_finally)

        def inventory(_event=None):
            global inv_screen
            inv_screen = Toplevel(root)
            inv_screen.title('Inventory')
            inv_screen.geometry('1500x900')

            def search_(sort_by=None):
                searched = inv_search.get()
                records_treeview.search(
                    to_search=searched, table="stock", sort_by=sort_by)
            """menu button________________________"""
            menu_bar = ttk.Menubutton(
                inv_screen, text='Sort By', cursor='mouse')
            menu_bar.grid(row=2, column=2)
            menu_ = Menu(menu_bar, tearoff=0)
            menu_bar["menu"] = menu_
            menu_.add_command(
                label='Brand Name', command=lambda sort_by=brand_name_field: search_(sort_by))
            menu_.add_command(
                label='MRP', command=lambda sort_by=mrp_field: search_(sort_by))
            menu_.add_command(label='Box Number',
                              command=lambda sort_by=box_no_field: search_(sort_by))
            menu_.add_command(
                label='date', command=lambda sort_by=date_field: search_(sort_by))
            menu_.add_command(
                label='quantity', command=lambda sort_by=quantity_field: search_(sort_by))
            menu_.add_command(label='warning Quantity',
                              command=lambda sort_by=warning_qty_field: search_(sort_by))

            # top label
            lbl_name = Label(inv_screen, text="Inventory", font=('arial', 30, 'bold'),
                             padx=2, pady=2, bd=2)
            lbl_name.grid(row=1, column=0)

            # update
            lbl_name = Label(inv_screen, text="Select & Press        Ctrl-u         to update", font=('roboto', 15, 'bold'),
                             padx=2, pady=2, bd=2)
            lbl_name.grid(row=0, column=0)

            # search bar
            sb_entry = Entry(inv_screen, textvariable=inv_search,
                             width=110, font=('arial', 15))
            sb_entry.grid(row=2, column=0)
            sb_entry.focus_set()  # setting focus on the entry widget

            sb_entry.bind('<KeyRelease>', lambda event,
                          sort_by=None: search_(sort_by))

            search_btn = Button(inv_screen, text="Search", bd=1, pady=1, padx=1,
                                relief=RIDGE, overrelief=SUNKEN, cursor='mouse', font=('arial', 8, 'italic'),
                                bg='snow', command=lambda sort_by=None: search_(sort_by))
            search_btn.grid(row=2, column=1)

            # treeview
            global records_treeview
            records_treeview = CustomTreeview(
                inv_screen, columns=treeview_columns, row=3)

            global total_data
            total_data = dbFuncProvider.custom_fetching(table='stock')
            for treeview_data in total_data:
                records_treeview.insert('', 'end', values=treeview_data)

            # for updating values
            records_treeview.bind('<Control-u>', update)
            inv_screen.bind('<Escape>', lambda event, screen=inv_screen: exit_system(screen))

        def add_finally(_event=None):
            # fetching variable values
            product_name = add_product_name.get()  # primary key
            tractor_name = add_tractor_name.get()    # nt null
            brand_name = add_brand_name.get()     # not null
            part_number = add_part_no.get()     # unique , can be null
            code = add_code.get()
            mrp = add_mrp.get()                    # not null  # int
            box_no = add_box_no.get()
            description = add_description.get()
            quantity = add_quantity.get()            # not null   # int
            warning_qty = add_warning_qty.get()             # not null # int
            date = add_date.get()
            add_image = add_img.get()

            if date == '':                     # auto fill date if date is empty
                global date_
                date_ = str(current_date)

            else:
                date_ = date

            try:
                if mrp == '':
                    add_mrp.set(0)

                else:                    # make sure these are integers
                    global mrp_
                    mrp_ = float(mrp)

                    global qty_
                    qty_ = float(quantity)

                    global w_qty
                    w_qty = float(warning_qty)

            except ValueError:
                tkinter.messagebox.showerror(
                    'Error!', 'MRP , Quantity and Warning Quantity must be a number')

            if product_name == '':
                tkinter.messagebox.showerror(
                    'Error!', 'Product Name is necessary!')

            elif brand_name == '':
                tkinter.messagebox.showerror(
                    'Error!', 'Brand Name is necessary!')

            elif tractor_name == '':
                tkinter.messagebox.showerror(
                    'Error!', 'Tractor Name is necessary!')

            elif quantity == '':
                tkinter.messagebox.showerror(
                    'Error!', 'Quantity is necessary!')

            elif description == '':
                add_description.set(None)

            elif warning_qty == '':
                add_warning_qty.set(0)

            elif code == '':
                add_code.set(None)

            elif box_no == '':
                add_box_no.set(None)

            elif add_image == '':
                add_img.set(None)

            else:
                try:
                    all_brands = dbFuncProvider.fetch('brands', ['name'])
                    all_brands = [brand.lower() for brand in all_brands]
                    if brand_name.lower() in all_brands:

                        values = (product_name, tractor_name, brand_name, part_number, code, mrp, box_no,
                                  description, quantity, warning_qty, date_, add_image)

                        dbFuncProvider.insert('stock', values)
                        dbFuncProvider.insert('recently_added', values)
                        dbFuncProvider.insert('stock_in', values)
                        guiFuncProvider.focus_on(add_screen, state=False)
                        tkinter.messagebox.showinfo(
                            'Success', f'Product "{product_name}" added Successfully!')

                        data = [product_name, brand_name, box_no, mrp]
                        recents_treeview.insert('', 'end', values=data)

                        add_screen.destroy()
                        reset(add_product_name, add_tractor_name, add_brand_name, add_code, add_part_no,
                              add_description, add_date, add_img, add_box_no, add_quantity, add_warning_qty, add_mrp)

                    else:
                        tkinter.messagebox.showerror(
                            'Error!', f'"{brand_name}" Brand Name is not registered!')
                        register_brand_name()
                        brand_name_.set(brand_name)
                        guiFuncProvider.focus_on('add_screen')

                except mysql.errors.IntegrityError:
                    tkinter.messagebox.showerror(
                        'Error', f'Product Name "{product_name}" or Part Number "{part_number}"already exists!')

        def add_inventory(_event=None):
            # checking if there is atleast 1 brand registered
            brand_list = dbFuncProvider.fetch('brands', ['name'])
            if len(brand_list) != 0:
                def date_picker():
                    def select_date():
                        selected_date = cal.selection_get()    # YEAR MONTH DAY
                        add_date.set(selected_date)
                        cal_window.destroy()
                    cal_window = Toplevel(root)
                    cal_window.title('Calendar')
                    cal_window.geometry('260x250+100+100')
                    cal = Calendar(cal_window, selectmode="day", year=cur_year, month=int(
                        cur_month), day=cur_day, cursor='hand1')
                    cal.grid(row=0, column=0, padx=3, pady=3)
                    pick_btn = Button(
                        cal_window, text='Select', command=select_date)
                    pick_btn.grid(row=1, column=0)

                def img_picker():
                    files = [('PNG File', '.png'), ('JPEG file', '.jpg')]
                    open_path_ = filedialog.askopenfilename(
                        filetypes=files, initialdir=cur_wd)
                    add_img.set(open_path_)

                    guiFuncProvider.focus_on(add_screen)

                def store_br(br_name):
                    add_brand_name.set(br_name)

                def auto_complete(total_values, textvar):
                    to_match = textvar.get().lower()
                    for items in total_values:
                        if items.lower().startswith(to_match):
                            textvar.set(items.title())

                global add_screen
                add_screen = Toplevel(root)
                add_screen.title('Add Inventory')
                add_screen.geometry('1000x900')
                add_screen.bind('<Escape>', lambda event, screen=add_screen: exit_system(screen))

                # ignore frames (pretty wasting of lines for formatting)
                main_frame_ = Frame(add_screen, bd=10)
                main_frame_.grid()

                top_ = Frame(main_frame_, bd=10, width=100, relief=RIDGE)
                top_.pack(side=TOP)

                add_ent_frame = LabelFrame(main_frame_, bd=10, width=500, height=150, font=('helvetica', 20, 'bold'),
                                           relief=RIDGE)
                add_ent_frame.pack(side=TOP)

                add_but_frame = LabelFrame(main_frame_, bd=10, width=700, height=400, font=('helvetica', 20, 'bold'),
                                           relief=RIDGE)
                add_but_frame.pack(side=BOTTOM)

                # top label
                lbl_name = Label(top_, text="Add Inventory", font=('arial', 30, 'bold'),
                                 padx=2, pady=2, bd=2)
                lbl_name.grid(row=0, column=0)

                """____________________________product_name____________________________________"""
                lbl_name = Label(add_ent_frame, text='Product Name:*', font=('arial', 15, 'bold'),
                                 padx=2, pady=2, bd=2)
                lbl_name.grid(row=1, column=0)

                global entry_nm
                entry_nm = Entry(add_ent_frame, width=40, textvariable=add_product_name, font=('arial', 15, 'bold'),
                                 cursor='xterm', state='normal')
                entry_nm.grid(row=1, column=1)
                entry_nm.focus()
                """____________________________tractor_name____________________________________"""
                lbl_name = Label(add_ent_frame, text='Tractor:*', font=('arial', 15, 'bold'),
                                 padx=2, pady=2, bd=2)
                lbl_name.grid(row=2, column=0)

                global entry_trac
                entry_trac = Entry(add_ent_frame, width=40, textvariable=add_tractor_name, font=('arial', 15, 'bold'),
                                   cursor='xterm', state='normal')
                entry_trac.grid(row=2, column=1)

                # code for auto complete
                all_tractors = dbFuncProvider.fetch(
                    'stock', ['DISTINCT(tractor)'])

                entry_trac.bind('<Tab>', lambda event, total_values=all_tractors,
                                textvar=add_tractor_name: auto_complete(total_values, textvar))

                """____________________________brand_name____________________________________"""
                lbl_name = Label(add_ent_frame, text='Brand Name:*', font=('arial', 15, 'bold'),
                                 padx=2, pady=2, bd=2)
                lbl_name.grid(row=3, column=0)

                global entry_name
                entry_name = Entry(add_ent_frame, width=40, textvariable=add_brand_name, font=('arial', 15, 'bold'),
                                   cursor='xterm', state='normal')
                entry_name.grid(row=3, column=1)

                # code for auto complete
                all_brands = dbFuncProvider.fetch('brands', ['name'])

                entry_name.bind('<Tab>', lambda event, total_values=all_brands,
                                textvar=add_brand_name: auto_complete(total_values, textvar))

                menu_button = ttk.Menubutton(
                    add_ent_frame, text='Brand Names:', cursor='mouse')
                menu_button.grid(row=3, column=2)

                menu_ = Menu(menu_button, tearoff=0)
                menu_button['menu'] = menu_

                brands_data = dbFuncProvider.fetch('brands', ['name'])
                for brands in brands_data:
                    menu_.add_command(
                        label=f'{brands}', command=lambda br_name=brands: store_br(br_name))

                """____________________________part number____________________________________"""
                guiFuncProvider.custom_entry_labels(
                    add_ent_frame, text='Part Number:', r=4, var=add_part_no)

                """____________________________code____________________________________"""
                guiFuncProvider.custom_entry_labels(
                    add_ent_frame, text='Code:', r=5, var=add_code)

                """____________________________mrp____________________________________"""
                guiFuncProvider.custom_entry_labels(
                    add_ent_frame, text='MRP:*', r=6, var=add_mrp)

                """____________________________box no____________________________________"""
                guiFuncProvider.custom_entry_labels(
                    add_ent_frame, text='Box Number:', r=7, var=add_box_no)
                """____________________________description____________________________________"""
                guiFuncProvider.custom_entry_labels(
                    add_ent_frame, text='Description:', r=8, var=add_description)

                """____________________________Quantity____________________________________"""
                guiFuncProvider.custom_entry_labels(
                    add_ent_frame, text='Quantity:*', r=9, var=add_quantity)

                """____________________________Warning Quantity____________________________________"""
                guiFuncProvider.custom_entry_labels(
                    add_ent_frame, text='Warning Quantity:*', r=10, var=add_warning_qty)

                """____________________________date____________________________________"""
                guiFuncProvider.custom_entry_labels(
                    add_ent_frame, text='Date:', r=11, var=add_date, state='disabled')

                cal_btn = Button(add_ent_frame, text=cal_text, bd=3, pady=1, padx=1,
                                 font=('arial', 20, 'bold'), relief=FLAT, overrelief=RIDGE,
                                 command=date_picker)
                cal_btn.grid(row=11, column=2)

                """____________________________img____________________________________"""
                guiFuncProvider.custom_entry_labels(
                    add_ent_frame, text='Image:', r=12, var=add_img, state='disabled')

                try:
                    img_path = ICON_PATH + '\\pick.png'
                    img = PhotoImage(file=(img_path))

                    cal_btn = Button(add_ent_frame, text=img_text, bd=3, pady=1, padx=1,
                                     font=('arial', 10, 'bold'), relief=FLAT, overrelief=RIDGE, image=img,
                                     command=img_picker)

                    cal_btn.image = img  # preventing image get destroying by garbage collection

                    cal_btn.grid(row=12, column=2)

                except Exception:
                    tkinter.messagebox.showwarning(
                        'Warning!', f"Icon is deleted so program will use '{img_text}' instead of icon")
                    guiFuncProvider.focus_on(add_screen)

                    cal_btn = Button(add_ent_frame, text=img_text, bd=3, pady=1, padx=1,
                                     font=('arial', 10, 'bold'), relief=FLAT, overrelief=RIDGE,
                                     command=img_picker)
                    cal_btn.grid(row=12, column=2)

                """________________________________buttons___________________________________"""
                add_btn = Button(add_but_frame, text=" Add  ", bd=3, pady=1, padx=1,
                                 relief=RIDGE, overrelief=SUNKEN, cursor='plus', font=('arial', 20, 'bold', 'italic'),
                                 bg=button_color, command=add_finally)
                add_btn.grid(row=0, column=0)

                add_btn = Button(add_but_frame, text="Reset", bd=3, pady=1, padx=1,
                                 relief=RIDGE, overrelief=SUNKEN, cursor='hand1', font=('arial', 20, 'bold', 'italic'),
                                 bg=button_color, command=lambda: reset(add_product_name, add_tractor_name, add_brand_name, add_part_no, add_mrp, add_code, add_description, add_quantity, add_warning_qty, add_date, add_img, add_box_no))
                add_btn.grid(row=0, column=1)

                add_btn = Button(add_but_frame, text=" Exit  ", bd=3, pady=1, padx=1,
                                 relief=RIDGE, overrelief=SUNKEN, cursor='pirate', font=('arial', 20, 'bold', 'italic'),
                                 bg=button_color, command=lambda screen=add_screen: exit_system(screen))
                add_btn.grid(row=0, column=2)

                add_screen.bind('<Control-a>', add_finally)

            else:
                tkinter.messagebox.showerror(
                    'Error!', 'Register a Brand Name first!     (Ctrl+r)')
                register_brand_name()

        """___________________________________________________________________frames"""
        main_frame = Frame(self.root, bd=10)
        main_frame.pack(side=LEFT)

        div_frame = Frame(self.root, bd=10)
        div_frame.pack(side=RIGHT)

        top = Frame(main_frame, bd=10, width=100, relief=RIDGE)
        top.grid(row=0, column=0, sticky='nswe')
        # top.pack(side=TOP)

        recent_frame = LabelFrame(main_frame, bd=10, width=700, height=400, font=('helvetica', 20, 'bold'),
                                  relief=RIDGE)
        recent_frame.grid(row=2, column=0, sticky='nswe')

        # recent_frame.pack(side=BOTTOM, fill=X)

        button_frame = LabelFrame(main_frame, bd=10, width=500, height=150, font=('helvetica', 20, 'bold'),
                                  relief=RIDGE)
        button_frame.grid(row=1, column=0)
        # button_frame.pack(side=TOP)

        side_frame = LabelFrame(div_frame, text='Warning...☠☠', fg='red',  bd=10, width=350, height=500, font=('impact', 20, 'bold'),
                                relief=RIDGE)

        side_frame.grid(row=0, column=0)

        """__________________top frame_____________________"""
        self.lbl1 = Label(top, font=('helvetica', 31, 'bold'), text="\t  Inventory Record\t  ",
                          justify=CENTER, cursor='sailboat')
        self.lbl1.grid(row=0, column=1)

        """______________________button_frame________________________"""
        global add_button
        add_button = Button(button_frame, text="Add Inventory", bd=6, pady=3, padx=3, bg=button_color,
                            relief=RIDGE, overrelief=SOLID, cursor='plus', font=(button_font, button_size, 'bold', 'italic'),
                            command=add_inventory)
        add_button.grid(row=0, column=0)

        global inv_button
        inv_button = Button(button_frame, text="  Inventory  ", bd=6, pady=3, padx=3, bg=button_color,
                            relief=RIDGE, overrelief=SOLID, cursor='man', font=(button_font, button_size, 'bold', 'italic'),
                            command=inventory)
        inv_button.grid(row=0, column=1)
        global items_button
        items_button = Button(button_frame, text="    Items    ", bd=6, pady=3, padx=3, bg=button_color,
                              relief=RIDGE, overrelief=SOLID, cursor='heart', font=(button_font, button_size, 'bold', 'italic'))
        items_button.grid(row=0, column=2)

        global exit_button
        exit_button = Button(button_frame, text="    Exit     ", bd=6, pady=3, padx=3, bg=button_color,
                             relief=RIDGE, overrelief=SOLID, cursor='pirate', font=(button_font, button_size, 'bold', 'italic'),
                             command=lambda screen=root: exit_system(screen))
        exit_button.grid(row=0, column=3)

        warning_button = Button(button_frame, text="Check Warnings", bd=6, pady=3, padx=3, bg=button_color,
                                relief=RIDGE, overrelief=SOLID, cursor='pirate', font=(button_font, button_size, 'bold', 'italic'),
                                command=check_warnings)
        warning_button.grid(row=0, column=4)

        """__________________recent_frame______________________________"""
        self.lbl = Label(recent_frame, font=('arial', 15, 'bold'), text='Recent records:',
                         justify=CENTER)
        self.lbl.grid(row=0, column=0)

        recents = ['Product Name', 'Brand Name', 'Box Number', 'MRP']
        recents_treeview = ttk.Treeview(
            recent_frame, column=recents, show='headings', height=9, cursor='hand1')
        scroll_bar1 = ttk.Scrollbar(
            recent_frame, orient='vertical', command=recents_treeview.yview)
        recents_treeview.configure(yscroll=scroll_bar1.set)
        scroll_bar1.grid(row=1, column=2, sticky='ns')
        for i in recents:
            recents_treeview.heading(i, text=i.title())
        recents_treeview.grid(row=1, column=0)

        lbl4 = Label(recent_frame, text="© Copyright : Vanshu Galhotra", font=('helvetica', 9, 'bold'),
                     bd=2)
        lbl4.grid(row=2, column=0)

        '''________________________________--side frame----------------------------------'''
        labels = ['Product Name', 'Brand Name', 'Quantity']
        global treeview
        treeview = ttk.Treeview(side_frame, column=labels,
                                show='headings', height=90, cursor='hand1')
        scroll_bar_ = ttk.Scrollbar(
            side_frame, orient='vertical', command=treeview.yview)
        treeview.configure(yscroll=scroll_bar_.set)
        scroll_bar_.grid(row=1, column=2, sticky='ns')
        for columns in labels:
            treeview.heading(columns, text=columns.title())
            treeview.column(columns, width=120)
        treeview.grid(row=1, column=0)

        # menu bars
        main_menu = Menu(root)
        root.configure(menu=main_menu)
        file_sub = Menu(main_menu)   # file menu sub menu of main menu
        tool_sub = Menu(main_menu)   # tool menu sub menu of main menu
        tran_sub = Menu(main_menu)   # transaction menu sub menu of main menu

        record_sub = Menu(file_sub)   # sub menu of file menu

        main_menu.add_cascade(label="File", menu=file_sub)  # m1
        file_sub.add_cascade(label="Save Record", menu=record_sub)  # f1
        record_sub.add_command(label="Excel Sheet(ctrl-s)",
                               command=save_xlsx)  # f1r1
        record_sub.add_command(
            label="Database File(ctrl-alt-s)", command=save_db)  # f1r2
        record_sub.add_command(label="Warnings Sheet",
                               command=save_warning_sheet)  # f1r3

        main_menu.add_cascade(label='Tools', menu=tool_sub)  # m2
        tool_sub.add_command(label='Register Brand (Ctrl-r)',
                             command=register_brand_name)  # t1
        tool_sub.add_command(label='Update Brand (Ctrl-Alt-r)',
                             command=update_brand_name)  # t2
        tool_sub.add_command(label='Total Stock (Ctrl-t)',
                             command=total_stock)  # t3
        tool_sub.add_command(label='Update MRP (Ctrl-m)',
                             command=update_mrp)  # t4
        tool_sub.add_command(label='Delete Product (Ctrl-d)',
                             command=delete_product)  # t5

        main_menu.add_cascade(label='Transactions', menu=tran_sub)  # m3
        tran_sub.add_command(label='Updation', command=updation_transactions)
        tran_sub.add_command(label='Deletion', command=recently_deleted)
        tran_sub.add_command(label='Addition', command=recently_added)
        tran_sub.add_command(label='Stock INs', command=stock_in)
        tran_sub.add_command(label='Stock OUTs', command=stock_out)

        # bindings for shortcut keys
        root.bind('<Alt-i>', add_inventory)    # for adding new product
        root.bind('<Control-r>', register_brand_name)
        root.bind('<Alt-r>', update_brand_name)    
        root.bind('<Control-w>', check_warnings)
        root.bind('<Control-s>', save_xlsx)
        root.bind('<Control-t>', total_stock)
        root.bind('<Control-m>', update_mrp)
        root.bind('<Control-d>', delete_product)
        root.bind('<Control-i>', inventory)  # to open inventory window
        root.bind('<Alt-s>', save_db)
        root.bind('<Alt-u>', updation_transactions)
        root.bind('<Escape>', lambda event, screen=root: exit_system(screen))

        root.protocol("WM_DELETE_WINDOW", end_func)


if __name__ == '__main__':
    root = Tk()
    OT = StoreBook()
    root.mainloop()
