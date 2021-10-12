from .run_models import Entity_Parser
import pandas as pd
# from pandasql import sqldf
import re
from .common import CommonClass
import os
from urllib.request import urlopen
import gc
from datetime import datetime,timedelta

ep = Entity_Parser()
cm_obj = CommonClass()

if not os.path.exists("Combined_Allegro_Data.csv"):
    #? Reading file from s3 server
    print("Downloading CSV")
    with urlopen("https://feasta-image-bucket.s3.us-east-2.amazonaws.com/Models/Combined_Allegro_Data.csv") as conn:
        with open("Combined_Allegro_Data.csv","wb") as wo:
            wo.write(conn.read())
        del conn

df = pd.read_csv('Combined_Allegro_Data.csv')
df['ACTUAL_SHIP_DATE'] = pd.to_datetime(df['ACTUAL_SHIP_DATE'])

# os.remove('Combined_Allegro_Data.csv')
gc.collect()

cols = ['BUSINESS_UNIT', 'PRODUCT_SEGMENT', 'CUSTOMER_NAME']
unique_list = [list(df[cols[i]].unique()) for i in range(len(cols))]
exception_words = ['tyco for 2018','tyco for 2019']

def get_answer(sent):
    
    #? Preprocessing sentence
    sent = sent.lower()
    sent = sent.replace("?","")
    sent = sent.replace("...","")
    for i in ['month', 'year', 'week','quarter']:
        sent = sent.replace(f"current {i}",f"this {i}")
    # sent = sent.replace(r"\xa0","")
    if sent[-1]=='.':
        sent = sent[:-1]
    
    entity = ep.extract_data(sent)
    print("\nFetched entities: "+str(entity))
    
    lst = []
    for i in range(len(cols)):
        if cols[i] in entity:
            if entity[cols[i]].upper() in unique_list[i]:
                # del entity[cols[i]]
                continue 
            elif entity[cols[i]].isnumeric():
                del entity[cols[i]]
            elif entity[cols[i]] in exception_words:
                del entity[cols[i]]
            else:
                lst.append(entity[cols[i]])
                del entity[cols[i]]
    
    print("Entities after cross-verification : "+str(entity))
    
    if len(lst)!=0:
        return f'''data not found for entities {" ".join(list(map(lambda x: f"'{x}'",lst)))}!'''
    
    # for date
    # if 'SCHEDULE_SHIP_DATE' in entity:
    #     for i in range(len(entity['SCHEDULE_SHIP_DATE'])):
    #         if entity['SCHEDULE_SHIP_DATE'][i] not in list(df['SCHEDULE_SHIP_DATE'].unique()):
    #             del entity['SCHEDULE_SHIP_DATE']
    
    sql = ep.generate_sql(entity)
    print("Generated SQL Command: "+ sql+"\n")

    if len(entity) != 0:
        # sql_command = "select SUM(EXTN_AMOUNT_USD) from df where SCHEDULE_SHIP_DATE between '5-MAR-18' and '5-MAR-18'"
        # output = sqldf(sql)
        
        temp_df = df.copy()
        for key,val in entity.items():
            if isinstance(val,list):
                end_date = str((datetime.strptime(val[1],'%Y-%m-%d') + timedelta(days=1)).strftime('%Y-%m-%d'))
                temp_df = temp_df[(temp_df[key] > val[0]) & (temp_df[key] < end_date)]
            else:
                temp_df = temp_df[temp_df[key] == val.upper()]
        
        output_2 = temp_df['EXTN_AMOUNT_USD'].sum()
        
        del temp_df
        gc.collect()
        
        # if output.iloc[0,0]:
        #     output = output.iloc[0,0]
        # else:
        # return 'No data found!'
            
        # string = 'The sales for '
        # for k,v in entity.items():
        #     if isinstance(v,list):
        #         string += str(k).lower() + ' between ' + str(v[0]) + ', ' + str(v[1]) +' and '
        #     else:
        #         string += str(k).lower() + ' ' + str(v) + ' and '
                
        # string = re.sub(' and $', '', string)
        # print(output)
        # ans = string+' is $'+str(int(output))+"."
        ans = '$ '+"{:,}".format(int(output_2))
    else:
        ans = 'No data found!'
        
    return ans