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

    # from [2022-08-01] to 1 Aug 2022
    def system_to_english_date_format(self, date):

        months = {'01': 'Jan', '02': 'Feb', '03': 'March', '04': 'April', '05': 'May', '06': 'June',
                  '07': 'July', '08': 'Aug', '09': 'Sep', '10': 'Oct', '11': 'Nov', '12': 'Dec'}

        # using regex to extract year-month-day from date string
        pattern = r'(\d+)-(\d+)-(\d+)'
        result = re.search(pattern, date)
        
        year = result[1]
        month = result[2]
        day = result[3]
        
        engMonth = months[month]
        
        english_format = "{} {} {}".format(day, engMonth, year)
        return english_format
        
    def convert_all_dates_to_english(self, list_of_dates):
        dmy_list = []
        for eachDate in list_of_dates:
            dmy_list.append(self.system_to_english_date_format(eachDate))
        
        return dmy_list
    
    # from 1 Aug 2022 to [2022-08-01]
    def english_to_system_date_format(self, date):
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
