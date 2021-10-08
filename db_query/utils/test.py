from .run_models import Entity_Parser
import spacy
import pandas as pd
from pandasql import sqldf
import re
from .common import CommonClass

ep = Entity_Parser()
cm_obj = CommonClass()

df = pd.read_csv(r'db_query\utils\APR-19_2019_1_17SEP21.txt',sep='~')

def get_answer(sent):
    
    entity = ep.extract_data(sent)
    
    cols = ['SCHEDULE_SHIP_DATE', 'BUSINESS_UNIT', 'PRODUCT_SEGMENT', 'CUSTOMER_NAME']
    for i in range(len(cols)):
        if cols[i] in entity and cols[i] != 'SCHEDULE_SHIP_DATE':
            if not entity[cols[i]].upper() in list(df[cols[i]].unique()):
                del entity[cols[i]]    
    print(entity)

    # for date
    # if 'SCHEDULE_SHIP_DATE' in entity:
    #     for i in range(len(entity['SCHEDULE_SHIP_DATE'])):
    #         if entity['SCHEDULE_SHIP_DATE'][i] not in list(df['SCHEDULE_SHIP_DATE'].unique()):
    #             del entity['SCHEDULE_SHIP_DATE']
    
    sql = ep.generate_sql(entity)
    print(sql)

    if len(entity) != 0:
        # sql_command = "select SUM(EXTN_AMOUNT_USD) from df where SCHEDULE_SHIP_DATE between '5-MAR-18' and '5-MAR-18'"
        output = sqldf(sql)
        if output.iloc[0,0]:
            output = output.iloc[0,0]
        else:
            output = "0"
            
        string = 'The sales for '
        for k,v in entity.items():
            if isinstance(k,list):
                string += str(k) + ' between ' + str(v[0]) + ', ' + str(v[1]) +' and '
            else:
                string += str(k) + ' ' + str(v) + ' and '
                
        string = re.sub(' and $', '', string)
        ans = string+' is $'+str(int(output))+"."
    else:
        ans = 'No data found!'
        
    return ans