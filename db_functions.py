import mysql.connector as mysql
import tkinter.messagebox
import sys
import os
import itertools
from variables import password, user, host, database, file_name, MYSQL_BIN, DB_FILE_DIR, db_fields
from gui_funcs import GuiFuncs
import datetime
from operator import itemgetter
try:
    from db_connection import cursor , connection

except mysql.errors.ProgrammingError:
    print('Database Created Successfully!')

gui_func_provider = GuiFuncs()
class DatabaseFunctions:
    def init_db(self, database):
        connection_ = mysql.connect(
            host = host,
            user = user,
            password = password
        )
        cursor_ = connection_.cursor()
        cursor_.execute('SHOW DATABASES;')
        data_tuple = cursor_.fetchall()
        data_list = list(itertools.chain(*data_tuple))

        if database not in data_list:
            command = f'CREATE DATABASE {database}'
            cursor_.execute(command)

    def init_tables(self):
            try:
                table_command_brand = 'CREATE TABLE IF NOT EXISTS brands(name varchar(100) PRIMARY KEY)'
                cursor.execute(table_command_brand)

                table_command_stock = "CREATE TABLE IF NOT EXISTS stock(product_name varchar(250) PRIMARY KEY,"\
                                "tractor Varchar(50) NOT NULL,brand_name varchar(100),part_number varchar(200) DEFAULT NULL UNIQUE,"\
                                "code varchar(30), mrp int NOT NULL, box_no varchar(30), description varchar(255),"\
                                "quantity int NOT NULL , warning_qty int NOT NULL, date varchar(200), image varchar(255),"\
                                "FOREIGN KEY(brand_name) references brands(name) ON UPDATE CASCADE)"
                cursor.execute(table_command_stock)

                table_command_bu = "CREATE TABLE IF NOT EXISTS before_update(product_name varchar(250) PRIMARY KEY,"\
                                "tractor Varchar(50) NOT NULL,brand_name varchar(100),part_number varchar(200) DEFAULT NULL UNIQUE,"\
                                "code varchar(30), mrp int NOT NULL, box_no varchar(30), description varchar(255),"\
                                "quantity int NOT NULL , warning_qty int NOT NULL, date varchar(200), image varchar(255),"\
                                "FOREIGN KEY(brand_name) references brands(name) ON UPDATE CASCADE)"
                cursor.execute(table_command_bu)

                table_command_au = "CREATE TABLE IF NOT EXISTS after_update(product_name varchar(250) PRIMARY KEY,"\
                                "tractor Varchar(50) NOT NULL,brand_name varchar(100),part_number varchar(200) DEFAULT NULL UNIQUE,"\
                                "code varchar(30), mrp int NOT NULL, box_no varchar(30), description varchar(255),"\
                                "quantity int NOT NULL , warning_qty int NOT NULL, date varchar(200), image varchar(255),"\
                                "FOREIGN KEY(brand_name) references brands(name) ON UPDATE CASCADE)"
                cursor.execute(table_command_au)


                table_command_rd = "CREATE TABLE IF NOT EXISTS recently_deleted(product_name varchar(250) PRIMARY KEY,"\
                                "tractor Varchar(50) NOT NULL,brand_name varchar(100),part_number varchar(200) DEFAULT NULL UNIQUE,"\
                                "code varchar(30), mrp int NOT NULL, box_no varchar(30), description varchar(255),"\
                                "quantity int NOT NULL , warning_qty int NOT NULL, date varchar(200), image varchar(255),"\
                                "FOREIGN KEY(brand_name) references brands(name) ON UPDATE CASCADE)"
                cursor.execute(table_command_rd)

                table_command_ra = "CREATE TABLE IF NOT EXISTS recently_added(product_name varchar(250) PRIMARY KEY,"\
                                "tractor Varchar(50) NOT NULL,brand_name varchar(100),part_number varchar(200) DEFAULT NULL UNIQUE,"\
                                "code varchar(30), mrp int NOT NULL, box_no varchar(30), description varchar(255),"\
                                "quantity int NOT NULL , warning_qty int NOT NULL, date varchar(200), image varchar(255),"\
                                "FOREIGN KEY(brand_name) references brands(name) ON UPDATE CASCADE)"
                cursor.execute(table_command_ra)

                table_command_si = "CREATE TABLE IF NOT EXISTS stock_in(product_name varchar(250) PRIMARY KEY,"\
                                "tractor Varchar(50) NOT NULL,brand_name varchar(100),part_number varchar(200) DEFAULT NULL UNIQUE,"\
                                "code varchar(30), mrp int NOT NULL, box_no varchar(30), description varchar(255),"\
                                "quantity int NOT NULL , warning_qty int NOT NULL, date varchar(200), image varchar(255),"\
                                "FOREIGN KEY(brand_name) references brands(name) ON UPDATE CASCADE)"
                cursor.execute(table_command_si)

                table_command_so = "CREATE TABLE IF NOT EXISTS stock_out(product_name varchar(250) PRIMARY KEY,"\
                                "tractor Varchar(50) NOT NULL,brand_name varchar(100),part_number varchar(200) DEFAULT NULL UNIQUE,"\
                                "code varchar(30), mrp int NOT NULL, box_no varchar(30), description varchar(255),"\
                                "quantity int NOT NULL , warning_qty int NOT NULL, date varchar(200), image varchar(255),"\
                                "FOREIGN KEY(brand_name) references brands(name) ON UPDATE CASCADE)"
                cursor.execute(table_command_so)

                table_command_gb = "CREATE TABLE IF NOT EXISTS garbage(product_name varchar(250) PRIMARY KEY,"\
                                "tractor Varchar(50) NOT NULL,brand_name varchar(100),part_number varchar(200) DEFAULT NULL UNIQUE,"\
                                "code varchar(30), mrp int NOT NULL, box_no varchar(30), description varchar(255),"\
                                "quantity int NOT NULL , warning_qty int NOT NULL, date varchar(200), image varchar(255),"\
                                "FOREIGN KEY(brand_name) references brands(name) ON UPDATE CASCADE)"
                cursor.execute(table_command_gb)

                connection.commit()
            except NameError:
                tkinter.messagebox.showinfo('Success!', 'Everything is set Kindly rerun the code :)')
                sys.exit()

    def get_list_from_database(self, table, field):
        fetch_command = f'SELECT {field} from {table}'
        cursor.execute(fetch_command)
        fetched_tuple = cursor.fetchall()
        fetched_list = list(itertools.chain(*fetched_tuple))
        return fetched_list

    def import_data(self):
        os.chdir(DB_FILE_DIR)
        os.system(f'echo y| cacls {file_name} /P everyone:f') # unlock
        os.chdir(MYSQL_BIN)
        os.system(f'mysql -u root -p%s {database} <"{DB_FILE_DIR}\\{file_name}"'%password)  # import
        print('Imported Successfully')

    def custom_fetching(self, table): # basically this function will, recieves the table name, and then returns the list of records in following format
        # [[date at front + record - date - image], [].............]
        date_com = f'SELECT DISTINCT(date) from {table}'
        cursor.execute(date_com)
        date_tup = cursor.fetchall()
        all_dates = list(itertools.chain(*date_tup))

        sorted_time = sorted(all_dates, key=lambda g: datetime.datetime.strptime(g, "%Y-%m-%d")
                                .strftime("%Y-%m-%d"))  # sorts time in ascending order
        sorted_time.reverse() # descending order
        all_fooking_data = [] # this list will contain list of data for each date, 
        for time in sorted_time:
            com = f'SELECT * from {table} where date="{time}"'
            cursor.execute(com)
            tup = cursor.fetchall()
            fooking_data = list(itertools.chain(*tup))
            all_fooking_data.append(fooking_data)

        dmy_list = gui_func_provider.convert_all_dates_to_english(sorted_time)  # 5 july 2021

        index_mul = []   # index of data which have multiple records
        index_single = []   # single records
        # lets fill the data out
        for index in range(len(all_fooking_data)):
            if len(all_fooking_data[index]) > db_fields: # if we have multiple data records on same date
                index_mul.append(index)

            else:
                index_single.append(index) # if we have only one record of data on a particular date

        data_copy = all_fooking_data.copy()
        date_data_dict = {} # this dict will contain all records corresponding to its data, like
        # { "3 Aug 2022": [record 1, record 2], "1 Aug 2022": [record 1, ..] }
        # where record means all 12 database fields, product_name ... to image
        for key in dmy_list:
            for value in data_copy:
                date_data_dict[key] = value
                data_copy.remove(value)
                break
        
        datas = []  # for single data, this will contain all the single_records whose date and image is removed
        datam = []  # for multiple data
        
        for ix in index_single:    # getting all data for 1 day 1 record removing date and image
            das = date_data_dict[dmy_list[ix]] # das will contain list of single record, fetched from dictionary
            del das[10:] # removing date and image information from our list which contain single_record, cuz it is not needed 
            datas.append(das) # now appending the record to datas, 
        
        for m in index_mul:  # getting all data for 1 day multiple records removing date and image
            dam = date_data_dict[dmy_list[m]] # dam will contain list of multiple records, means its length will be > 12
            lg = len(dam)
            splited_list = [dam[i:i+db_fields] for i in range(0,lg,db_fields)] # the splited list will contain list of each record seperated from multiple records,,
            # like, splited_list  = [[record1], [record2]] from [record1, record2]
            for items in splited_list:
                del items[10:] # removing the date and image information
                datam.append(items) # finally appending the list
        
        treeview_s = []  # list to store data that will be added to treeview 
        # datas is like,  [[record1], [record2].....]
        # treeview_s will be like, [[date + record1], [date + record2]....]
        treeview_m = []
        for lis in range(len(datas)): # datas[lis] represents each record list, 
            datas[lis].insert(0, dmy_list[index_single[lis]])  # inserting date on which this particular record was created or updated, inserting at position 0 means starting
            treeview_s.append(datas[lis]) 
        
        len_mul = [] # gonna store length of records for each day
        for x in index_mul:
            dat = date_data_dict[dmy_list[x]] # dat will include list of records, on a specific date, 
            # like, dat = [record1, record2,......] based on some particular date
            len_mul.append(int(len(dat)/db_fields))    # appending the calculated, number_of_records on a specific date, say 3 records on 2 Aug 2022 something like that
            # len_mul will look like [2,3,4,2,3,4......]

        # so now we have, datam like.. [[record1], [record2], [record3], [record4], [record5].......]
        # and len_mul like, [3, 2.....]
        # now from len_mul we conclude that, first 3 records are of some common date, and next 2 also , then so on....
        
        # now we will create a list sor, which will create list of list of records of common date, 
        # like, [ [[record1], [record2], [record3]], [ [record4], [record5] ]], where each list, will contain list of records on some common date
        iterator = iter(datam)
        sor = [[next(iterator) for _ in range(size)] for size in len_mul]
        
        for lim in range(len(sor)):
            for som in sor[lim]:
                som.insert(0, dmy_list[index_mul[lim]]) # inserting that common date on these records
                treeview_m.append(som) # now finally appending each record list, with date info attached to the treeview_m list
    
        global total_data # will contain both 
        total_data = treeview_s + treeview_m
                
        for data in total_data:
            data[0] = gui_func_provider.english_to_system_date_format(data[0]) # converting date format for sorting
        
        total_data.sort(key = itemgetter(0)) # sorting list based on date, 
        
        for data in total_data:
            data[0] = gui_func_provider.system_to_english_date_format(data[0]) # converting back
        
        total_data.reverse()
        return total_data 