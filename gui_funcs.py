from tkinter import *
import re

class GuiFuncs:
    def custom_entry_labels(self, screen, text, r, var, state='normal'):
        lbl_name = Label(screen, text=text, font=('arial', 15, 'bold'),
                         padx=2, pady=2, bd=2)
        lbl_name.grid(row=r, column=0)

        entry_name = Entry(screen, width=40, textvariable=var, font=('arial', 15, 'bold'),
                           cursor='xterm', state=state)
        entry_name.grid(row=r, column=1)

    def focus_on(self, screen, state=True):
        screen.lift()
        screen.attributes('-topmost', state)

    # yyyy mm dd [2021-07-04] to 4 July 2021
    # TODO: optimise this function and split this to 2 seperate functions
    def int_dateformat_english(self, data): 
        months = {'01': 'Jan', '02': 'Feb', '03': 'March', '04': 'April', '05': 'May', '06': 'June',
                  '07': 'July', '08': 'Aug', '09': 'Sep', '10': 'Oct', '11': 'Nov', '12': 'Dec'}

        year_list = []   # will store all years from the given date data yyyy-mm-dd
        month_list = []
        day_list = []

        for y in data:
            year_list.append(y[0:4])  # gonna append all years

        for m in data:
            month_list.append(m[5:7])  # months

        for d in data:
            day_list.append(d[8:])

        month_list_alpha = []     # will store months like dec, nov etc. here
        for month in month_list:    # converting number months to there alpha character like 11 to nov
            # using months dictionary for this declared above
            month_list_alpha.append(months[month])

        day_month_list_alpha = []   # here we gonna store day+month like 3 dec
        # this is list which contains 2 separate lists of days and months_alpha
        # like [ ['day1', 'day2'], ['mon1','mon2'] ]
        day_month_list = [day_list] + [month_list_alpha]
        for index in range(0, len(day_month_list[1])):
            # index will include values from 0 to len(['day1','day2'])that is 2
            # now put value of day_month_list[0] and index to understand following.
            # day_month_list means ['day1', 'day2'] and index will be 0 at first loop
            # so day_month_list[0][index] is day1 which is concatenated with day_month_list[1][index] or mon1
            # which results day1 mon1 and then appended to day_month_list_alpha list
            day_month_list_alpha.append(
                day_month_list[0][index] + ' ' + day_month_list[1][index])

        # now we gonna concatenate day_month_alpha with year like 30nov 2020
        dmy_list = []  # creating empty list to store values later on
        # creating list of 2 lists that is day_month_alpha created above and year list
        dm_y_list = [day_month_list_alpha] + [year_list]
        for index_ in range(0, len(dm_y_list[0])):
            dmy_list.append(dm_y_list[0][index_] + ' ' + dm_y_list[1][index_])

        return dmy_list

    def english_to_system_date_format(self, date):  # from 1 Aug 2022 to [2022-08-01]
        months = {'Jan': '01', 'Feb': '02', 'March': '03', 'April': '04', 'May': '05', 'June': '06',
                  'July': '07', 'Aug': '08', 'Sep': '09', 'Oct': '10', 'Nov': '11', 'Dec': '12'}

        # extracting the year, month, day from the date string
        # using regex to extract this information
        pattern = r'(\d+) ([a-zA-Z]+) (\d+)'
        result = re.search(pattern, date)
        
        day = result[1]
        month = result[2]
        year = result[3]
        
        intMonth = months[month]
        
        system_format = f"{year}-{intMonth}-{day}"
        return system_format
        
        
        