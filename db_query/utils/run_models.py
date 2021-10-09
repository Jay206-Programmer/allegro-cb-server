from datetime import date
from .post_process_dates import PostProcessDatesClass
import spacy
import re
from pandasql import sqldf
import zipfile
from urllib.request import urlopen
import os

date_obj = PostProcessDatesClass()

if not os.path.exists("product"):
    #? Reading file from s3 server
    print("Downloading models")
    with urlopen("https://feasta-image-bucket.s3.us-east-2.amazonaws.com/Models/Models.zip") as conn:
        with open("./temp.zip","wb") as wo:
            wo.write(conn.read())

    #? Unzipping the
    print("unzipping models")
    with zipfile.ZipFile('temp.zip') as myzip:
        myzip.extractall()
    
    print("deleting zip file")
    os.remove("temp.zip")

#? Loading models
date_nlp = spacy.load('date_model')
bu_nlp = spacy.load('(bu v2) Extended BU as Product Retrain_50-epochs_2021_10_07_15_21_38')
product_nlp = spacy.load('product')
customer_nlp = spacy.load('customer')
        
class Entity_Parser:
    
    def preprocessing_sentence(self, sent):
            '''
                Preprocessing sentence to model input format.
            '''
            raplace_patterns = {
                    "business unit": ['division','market segment','strategic business unit','business group'],
                    " business unit ": [" bu "," sbu "],
                    "product": ["product segment", "product category", "product line", "segment"],
                    "products": ['product categories'],
                    "customer": ['client']
                }
            
            #? Replacing words
            for key in raplace_patterns.keys():
                for pattern in raplace_patterns[key]:
                    sent = re.sub(pattern, key, sent)
        
            return sent


    def extract_data(self,sent):
        """
            This method is use to extract entities from models.
            ARGS:
            
        """
        entities = {}
        # for date
        date_doc = date_nlp(sent)
        date = [ent.text for ent in date_doc.ents]
        if len(date)!=0:
            processed_date = date_obj.post_process(date[0])
            print(processed_date)
            entities['SCHEDULE_SHIP_DATE'] = processed_date
        
        # for business unit
        bu_doc = bu_nlp(sent)
        business_unit = [ent.text for ent in bu_doc.ents]
        
        if len(business_unit) != 0:
            entities['BUSINESS_UNIT'] = business_unit[0]
            
            
        # for product
        product_doc = product_nlp(sent)
        product = [ent.text for ent in product_doc.ents]
        
        if len(product) != 0:
            entities['PRODUCT_SEGMENT'] = product[0]
        
        
        # for customer
        customer_doc = customer_nlp(sent)
        customer = [ent.text for ent in customer_doc.ents]
        
        if len(customer) != 0:
            entities['CUSTOMER_NAME'] = customer[0]
        
        
        return entities   



    def generate_sql(self,dic):
        lst = [(k,v) for k,v in dic.items()]
        sql = '''select SUM(EXTN_AMOUNT_USD) from df where '''
        for i in lst:
            if isinstance(i[1],list):
                sql += i[0] + " between '" + i[1][0] + "' and '" + i[1][1] + "' and "
            else:
                sql += i[0] + " = '" + str(i[1]).upper() + "' and "

        sql = re.sub(' and $', '', sql)
        
        return sql