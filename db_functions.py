import os
import itertools
from variables import password, database, file_name, MYSQL_BIN, DB_FILE_DIR, db_fields
from gui_funcs import GuiFuncs
import datetime
from operator import itemgetter
from db_connection import cursor, connection
from mysql.connector import errors 
from initialize import init_tables

gui_func_provider = GuiFuncs()


class DatabaseFunctions:
    def create_table(self, table, fields_dict, foreign_key=None):
        command = f"CREATE TABLE IF NOT EXISTS {table} ("

        i = 0
        # details includes a tuple like this, (field_name, datatype(length), constraint if any)
        for details in fields_dict.values():
            i += 1
            command += " ".join(details)
            if i != len(fields_dict):  # to avoid appending , at last
                command += ","
                
        if foreign_key:
            command += f' , FOREIGN KEY ({foreign_key["field"]}) references {foreign_key["reference_table"]}({foreign_key["reference_field"]}) ON UPDATE CASCADE '
            command += ")"
        else:
            command += ")"
            
        cursor.execute(command)
        connection.commit()

    def fetch(self, table, field_list=["*"], conditions={}):
        """This function fetches data from database and returns a list"""
        fetch_command = f'SELECT {",".join(field_list)} from {table}'
        # adding the opitional conditions to the command
        # condition dictionary look like, { field: [operator, value, AND-OR] }, AND-OR value is optional
        if len(conditions) != 0:
            fetch_command += " WHERE"  # we only want where once
            if len(conditions) == 1:  # if we have only one condition
                field = list(conditions.keys())[0]
                op_val = conditions[field]
                fetch_command += f" {field} {op_val[0]} {op_val[1]}"
            else:  # for multiple conditions
                i = 0
                for field, op_val in conditions.items():  # appending each condition
                    i += 1
                    if i == len(conditions):  # to avoid appending this for last condition
                        fetch_command += f" {field} {op_val[0]} {op_val[1]}"
                    else:
                        fetch_command += f" {field} {op_val[0]} {op_val[1]} {op_val[2]}"
        
        try:
            cursor.execute(fetch_command)
            fetched_tuple = cursor.fetchall()
            fetched_list = list(itertools.chain(*fetched_tuple))
            return fetched_list
        
        except errors.ProgrammingError:
            init_tables()
            
    def insert(self, table, data):
        command = f"INSERT INTO {table} VALUES ("
        for _ in range(len(data) - 1):
            command += "%s, "
        command += "%s)"
        
        cursor.execute(command, data)
        connection.commit()

    def import_data(self):
        os.chdir(DB_FILE_DIR)
        os.system(f'echo y| cacls {file_name} /P everyone:f')  # unlock
        os.chdir(MYSQL_BIN)
        # import
        os.system(
            f'mysql -u root -p%s {database} <"{DB_FILE_DIR}\\{file_name}"' % password)
        print('Imported Successfully')

    # basically this function will, recieves the table name, and then returns the list of records in following format
    # [[date at front + record - date - image], [].............]
    def custom_fetching(self, table):

        all_dates = self.fetch(table, field_list=['DISTINCT(date)'])

        sorted_time = sorted(all_dates, key=lambda g: datetime.datetime.strptime(g, "%Y-%m-%d")
                             .strftime("%Y-%m-%d"))  # sorts time in ascending order
        sorted_time.reverse()  # descending order
        all_fooking_data = []  # this list will contain list of data for each date,
        for time in sorted_time:
            com = f'SELECT * from {table} where date="{time}"'
            cursor.execute(com)
            tup = cursor.fetchall()
            fooking_data = list(itertools.chain(*tup))
            all_fooking_data.append(fooking_data)

        dmy_list = gui_func_provider.convert_all_dates_to_english(
            sorted_time)  # 5 july 2021

        index_mul = []   # index of data which have multiple records
        index_single = []   # single records
        # lets fill the data out
        for index in range(len(all_fooking_data)):
            # if we have multiple data records on same date
            if len(all_fooking_data[index]) > db_fields:
                index_mul.append(index)

            else:
                # if we have only one record of data on a particular date
                index_single.append(index)

        data_copy = all_fooking_data.copy()
        date_data_dict = {}  # this dict will contain all records corresponding to its data, like
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
            # das will contain list of single record, fetched from dictionary
            das = date_data_dict[dmy_list[ix]]
            # removing date and image information from our list which contain single_record, cuz it is not needed
            del das[10:]
            datas.append(das)  # now appending the record to datas,

        for m in index_mul:  # getting all data for 1 day multiple records removing date and image
            # dam will contain list of multiple records, means its length will be > 12
            dam = date_data_dict[dmy_list[m]]
            lg = len(dam)
            # the splited list will contain list of each record seperated from multiple records,,
            splited_list = [dam[i:i+db_fields]
                            for i in range(0, lg, db_fields)]
            # like, splited_list  = [[record1], [record2]] from [record1, record2]
            for items in splited_list:
                del items[10:]  # removing the date and image information
                datam.append(items)  # finally appending the list

        treeview_s = []  # list to store data that will be added to treeview
        # datas is like,  [[record1], [record2].....]
        # treeview_s will be like, [[date + record1], [date + record2]....]
        treeview_m = []
        # datas[lis] represents each record list,
        for lis in range(len(datas)):
            # inserting date on which this particular record was created or updated, inserting at position 0 means starting
            datas[lis].insert(0, dmy_list[index_single[lis]])
            treeview_s.append(datas[lis])

        len_mul = []  # gonna store length of records for each day
        for x in index_mul:
            # dat will include list of records, on a specific date,
            dat = date_data_dict[dmy_list[x]]
            # like, dat = [record1, record2,......] based on some particular date
            # appending the calculated, number_of_records on a specific date, say 3 records on 2 Aug 2022 something like that
            len_mul.append(int(len(dat)/db_fields))
            # len_mul will look like [2,3,4,2,3,4......]

        # so now we have, datam like.. [[record1], [record2], [record3], [record4], [record5].......]
        # and len_mul like, [3, 2.....]
        # now from len_mul we conclude that, first 3 records are of some common date, and next 2 also , then so on....

        # now we will create a list sor, which will create list of list of records with common date,
        # like, [ [[record1], [record2], [record3]], [ [record4], [record5] ]], where each list, will contain list of records on some common date
        iterator = iter(datam)
        sor = [[next(iterator) for _ in range(size)] for size in len_mul]

        for lim in range(len(sor)):
            for som in sor[lim]:
                # inserting that common date on these records
                som.insert(0, dmy_list[index_mul[lim]])
                # now finally appending each record list, with date info attached to the treeview_m list
                treeview_m.append(som)

        global total_data  # will contain both
        total_data = treeview_s + treeview_m

        for data in total_data:
            data[0] = gui_func_provider.english_to_system_date_format(
                data[0])  # converting date format for sorting

        total_data.sort(key=itemgetter(0))  # sorting list based on date,

        for data in total_data:
            data[0] = gui_func_provider.system_to_english_date_format(
                data[0])  # converting back

        total_data.reverse()
        return total_data

