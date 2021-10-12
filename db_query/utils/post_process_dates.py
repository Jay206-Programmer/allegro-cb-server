from datetime import datetime,timedelta
from dateutil import relativedelta,parser
import re
import calendar



class PostProcessDatesClass:
    
    def text2int (self,textnum, numwords={}):
        """
        This method is use to convert numbers in text to integer
        e.g. twenty one -> 21
        ARGS:
        textnum['string'] : number in string e.g. twenty one
        
        RETURNS:
        curstring: integer representation of provided string
        """
        if not numwords:
            units = [
            "zero", "one", "two", "three", "four", "five", "six", "seven", "eight",
            "nine", "ten", "eleven", "twelve", "thirteen", "fourteen", "fifteen",
            "sixteen", "seventeen", "eighteen", "nineteen",
            ]

            tens = ["", "", "twenty", "thirty", "forty", "fifty", "sixty", "seventy", "eighty", "ninety"]

            scales = ["hundred", "thousand", "million", "billion", "trillion"]

            numwords["and"] = (1, 0)
            for idx, word in enumerate(units):  numwords[word] = (1, idx)
            for idx, word in enumerate(tens):       numwords[word] = (1, idx * 10)
            for idx, word in enumerate(scales): numwords[word] = (10 ** (idx * 3 or 2), 0)

        ordinal_words = {'first':1, 'second':2, 'third':3, 'fifth':5, 'eighth':8, 'ninth':9, 'twelfth':12}
        ordinal_endings = [('ieth', 'y'), ('th', '')]

        textnum = textnum.replace('-', ' ')

        current = result = 0
        curstring = ""
        onnumber = False
        for word in textnum.split():
            if word in ordinal_words:
                scale, increment = (1, ordinal_words[word])
                current = current * scale + increment
                if scale > 100:
                    result += current
                    current = 0
                onnumber = True
            else:
                for ending, replacement in ordinal_endings:
                    if word.endswith(ending):
                        word = "%s%s" % (word[:-len(ending)], replacement)

                if word not in numwords:
                    if onnumber:
                        curstring += repr(result + current) + " "
                    curstring += word + " "
                    result = current = 0
                    onnumber = False
                else:
                    scale, increment = numwords[word]

                    current = current * scale + increment
                    if scale > 100:
                        result += current
                        current = 0
                    onnumber = True

        if onnumber:
            curstring += repr(result + current)

        return curstring


    
    def only_year(self,date):
        """
        This method is used when only year is provided 
        ARGS:
        date['string'] : only year e.g. two thousand nineteen, 2019
        
        RETURNS:
        dates['list]: first and last day of given year 
        """
        int_year = self.text2int(date)
        if int(int_year):
            first_day_year = parser.parse(int_year).replace(month=1).replace(day=1).strftime('%Y-%m-%d')
            last_day_year = parser.parse(int_year).replace(month=12).replace(day=31).strftime('%Y-%m-%d')

            dates = []
            dates.append(first_day_year)
            dates.append(last_day_year)

        return dates

    

    def only_month(self,date):
        """
        This method is used when only month is provided 
        ARGS:
        date['string'] : only month e.g. january, jan, feb, february
        
        RETURNS:
        dates['list]: first and last day of given month 
        """
        months = ['january','jan','february','feb','march','mar','april','may','june','jun','july','jul','august','aug','september','sept','sep','october','oct','november','nov','december','dec']
        if date in months:
            date = parser.parse(date)
            first_day = date.replace(day=1).strftime('%Y-%m-%d')
            last_day = date.replace(day = calendar.monthrange(date.year, date.month)[1]).strftime('%Y-%m-%d')

            dates = []
            dates.append(first_day)
            dates.append(last_day)

        return dates



    def quarter(self,date):
        """
        This method is used when only quarter is provided 
        ARGS:
        date['string'] : only quarter e.g. quarter 1, first quarter, second quarter, quarter 2
        
        RETURNS:
        dates['list]: first and last day of given quarter 
        """
        quarter = ['quarter 1','quarter 2','quarter 3','quarter 4','1 quarter','2 quarter','3 quarter','4 quarter']
        date = self.text2int(date).strip()
        if date in quarter:
            temp_date = datetime.now()
            if '1' in date:
                first_date = temp_date.replace(month=1).replace(day=1).strftime('%Y-%m-%d')
                last_date = temp_date.replace(month=3).replace(day=31).strftime('%Y-%m-%d') 
            if '2' in date:
                first_date = temp_date.replace(month=4).replace(day=1).strftime('%Y-%m-%d')
                last_date = temp_date.replace(month=6).replace(day=30).strftime('%Y-%m-%d')
            if '3' in date:
                first_date = temp_date.replace(month=7).replace(day=1).strftime('%Y-%m-%d')
                last_date = temp_date.replace(month=9).replace(day=30).strftime('%Y-%m-%d')
            if '4' in date:
                first_date = temp_date.replace(month=10).replace(day=1).strftime('%Y-%m-%d')
                last_date = temp_date.replace(month=12).replace(day=31).strftime('%Y-%m-%d')

            dates = []
            dates.append(first_date)
            dates.append(last_date)

        return dates



    def this_month(self):
        """
        This method is used when provided date contains 'this month'
        ARGS:
        date['string'] : this month 
        
        RETURNS:
        dates['list]: first and last day of current month 
        """
        date = datetime.now()
        first_day = date.replace(day=1).replace(hour=0,minute=0,second=0).strftime('%Y-%m-%d')
        last_day = date.replace(day = calendar.monthrange(date.year, date.month)[1]).strftime('%Y-%m-%d')
        dates = []
        dates.append(first_day)
        dates.append(last_day)
        return dates


    def last_year(self):
        """
        This method is used when provided date contains 'this month'
        ARGS:
        date['string'] : this month 
        
        RETURNS:
        dates['list]: first and last day of current month 
        """
        date = datetime.now()
        first_day = date.replace(day=1,month=1,year=date.year-1).strftime('%Y-%m-%d')
        last_day = date.replace(day =31,month=12,year=date.year-1).strftime('%Y-%m-%d')
        dates = []
        dates.append(first_day)
        dates.append(last_day)
        return dates



    def previous_month(self):
        """
        This method is used when provided date contains 'previous month' or 'last month' 
        ARGS:
        date['string'] : 'previous month' or 'last month'
        
        RETURNS:
        dates['list]: first and last day of last month 
        """
        date = datetime.now()
        last_month = date + relativedelta.relativedelta(months=-1)
        
        first_day = last_month.replace(day=1).strftime('%Y-%m-%d')
        last_day = last_month.replace(day = calendar.monthrange(last_month.year, last_month.month)[1]).strftime('%Y-%m-%d')
        
        dates = []
        dates.append(first_day)
        dates.append(last_day)
        
        return dates



    def last_week(self):
        """
        This method is used when date contains 'last week'  
        ARGS:
        date['string'] : 'last week'
        
        RETURNS:
        dates['list]: first and last day of last week 
        """
        today = datetime.now()
        weekday = today.weekday()
        first_day = today - timedelta(days=weekday, weeks=1)
        last_day = first_day + timedelta(days=6)
        dates = []
        dates.append(first_day.replace(hour=0,minute=0,second=0).strftime('%Y-%m-%d'))
        dates.append(last_day.replace(hour=11,minute=59,second=59).strftime('%Y-%m-%d'))
        return dates
    
    
    
    

    
    def this_week(self):
        """
        This method is used when date contains 'this week'  
        ARGS:
        date['string'] : 'this week'
        
        RETURNS:
        dates['list]: first and last day of this week 
        """
        date_str = datetime.now().strftime('%d-%m-%y')
        date_obj = datetime.strptime(date_str, '%d-%m-%y')

        first_day = date_obj - timedelta(days=date_obj.weekday())  # Monday
        last_day = first_day + timedelta(days=6)  # Sunday
        dates = []
        dates.append(first_day.replace(hour=0,minute=0,second=0).strftime('%Y-%m-%d'))
        dates.append(last_day.replace(hour=11,minute=59,second=59).strftime('%Y-%m-%d'))
        return dates
    
    def this_year(self):
        """
        This method is used when provided date contains 'this year'
        ARGS:
        date['string'] : this year 
        
        RETURNS:
        dates['list]: first and last day of current year 
        """
        date = datetime.now()
        first_day = date.replace(day=1,month=1,year=date.year).strftime('%Y-%m-%d')
        last_day = date.replace(day =31,month=12,year=date.year).strftime('%Y-%m-%d')
        dates = []
        dates.append(first_day)
        dates.append(last_day)
        return dates


    def convert_date(self,date):
        month_dict = {'01':'JAN','02':'FEB','03':'MAR','04':'APR','05':'MAY','06':'JUN','07':'JUL','08':'AUG','09':'SEP',
                  '10':'OCT','11':'NOV','12':'DEC'}
        lst = []
        # print('convert date'+str(date))
        for i in range(len(date)):
            d = date[i].split('-')
            # print('in convert date: '+str(d[1]))
            d[1] = d[1].replace(d[1],month_dict[d[1]])
            d = '-'.join(d)
            lst.append(d)
        return lst
    
    def date_like_month_year_or_day_month(self,date):
        lst = date.split()
        # print('day month '+str(lst))
        if lst[0].isdigit() or len(lst[1])<=2:
            date = parser.parse(date)
            first_day = date.replace(day=date.day,month=date.month).strftime('%Y-%m-%d')
            last_day = date.replace(day=date.day,month=date.month).strftime('%Y-%m-%d')
            # print(first_day)

        else:
            if len(lst[1]) > 2:
                date = parser.parse(date)
                # print(date.year)
                first_day = date.replace(day=1,month=date.month,year=int(lst[1])).strftime('%Y-%m-%d')
                last_day = date.replace(day = calendar.monthrange(date.year, date.month)[1],month=date.month,year=date.year).strftime('%Y-%m-%d')
                # print(first_day)
                # print(last_day)
        
        dates = []
        dates.append(first_day)
        dates.append(last_day)
        
        return dates

    def post_process(self,date):
        """
            This is the main method which takes raw date from user and call required method defined above
            and gives date in proper formate.
            
            ARGS:
            date['string]: raw date from user
            
            RETURNS:
            final_date['list'] : list of date  
        """
        regex = "(\d{1,3})[a-zA-Z]{2}"
        p = re.compile(regex)
        
        if re.search(p,date):
            if 'st' in date:
                date = date.replace('st','')
            if 'nd' in date:
                date = date.replace('nd','')
            if 'th' in date:
                date = date.replace('th','')
            if 'rd' in date:
                date = date.replace('rd','')
            
        if date not in ['last week','current month','last month','this week','this year','this month','previous month','last year','previous year']:
            date = self.text2int(date).strip()
            # print('if'+str(date))
        elif date in ['last week','current month','last month','this week','this year','this month','previous month','last year','previous year'] or len(date.split) == 2: 
            date = date.strip()
            # print('elif'+str(date))
            
        months = ['january','jan','february','feb','march','mar','april','may','june','jun','july','jul','august','aug','september','sept','sep','october','oct','november','nov','december','dec']

        if 'today' in date:
            final_date = []
            date = datetime.now()
            date_start = date.replace(hour=0,minute=0,second=0).strftime('%Y-%m-%d')
            date_end = date.replace(hour=11,minute=59,second=59).strftime('%Y-%m-%d')
            final_date.append(date_start)
            final_date.append(date_end)
        elif date == 'yesterday':
            final_date = []
            date = datetime.now() - timedelta(days=1)
            date_start = date.replace(hour=0,minute=0,second=0).strftime('%Y-%m-%d')
            date_end = date.replace(hour=11,minute=59,second=59).strftime('%Y-%m-%d')
            final_date.append(date_start)
            final_date.append(date_end)
        elif 'day before yesterday' in date:
            final_date = []
            date = datetime.now() - timedelta(days=2)
            date_start = date.replace(hour=0,minute=0,second=0).strftime('%Y-%m-%d')
            date_end = date.replace(hour=11,minute=59,second=59).strftime('%Y-%m-%d')
            final_date.append(date_start)
            final_date.append(date_end)
        elif date in months:
            # print('only month')
            final_date = self.only_month(date)
        elif date.isdigit():
            # print('only year')
            final_date = self.only_year(date)
        elif 'quarter' in date:
            # print('quarter')
            final_date = self.quarter(date)
        elif 'last week' in date:
            final_date = self.last_week()
        elif ('last month' in date) or ('previous month' in date):
            final_date = self.previous_month()
        elif ('this month' in date) or ('current month' in date):
            final_date = self.this_month()
        elif 'this week' in date:
            final_date = self.this_week()
        elif ('last year' in date) or ('previous year' in date):
            final_date = self.last_year()
        elif ('this year' in date) or ('current year' in date):
            final_date = self.this_year()
        elif len(date.split())==2:
            final_date = self.date_like_month_year_or_day_month(date)
            # print('5 july '+str(final_date))
        else:
            final_date = []
            # print('else:'+str(date))
            final_date_start = parser.parse(date).strftime('%Y-%m-%d')
            final_date_end = parser.parse(date).strftime('%Y-%m-%d')
            final_date.append(final_date_start)
            final_date.append(final_date_end)
            # print(final_date)
        
        # print(final_date)
        # final_date = self.convert_date(final_date)
        # print(final_date)
        return final_date