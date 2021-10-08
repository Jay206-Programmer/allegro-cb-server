from .post_process_dates import PostProcessDatesClass
from fuzzywuzzy import process

date_obj = PostProcessDatesClass()


class CommonClass:
    
    def get_matches(self,query,choices,limit=3):
        result = process.extract(query,choices,limit=limit)
        return result
    
    def fuzzy_matcher(self,sent,df):
        unq_product = [word.lower() for word in list(df.PRODUCT_SEGMENT.unique())]
        unq_bu = [word.lower() for word in list(df.BUSINESS_UNIT.unique())]
        unq_customer =  [word.lower() for word in list(df.CUSTOMER_NAME.unique())]
        final_list = unq_product + unq_customer + unq_bu
        months = ['january','jan','february','feb','march','mar','april','may','june','jun','july','jul','august','aug','september','sept','sep','october','oct','november','nov','december','dec']
        
        # file with actual words
        with open('words.txt','r') as f:
            words = f.read().split("\n")
        words = [word for word in words if word!='']
        
        lst = sent.split()
        # print(lst)
        for i in range(len(lst)):
            try:
                s = int(lst[i])
            except:
                s = lst[i]
            if not (isinstance(s,int) or (s in months) or (s in final_list)):
                # print(self.get_matches(lst[i],words))
                lst[i] = lst[i].replace(lst[i],self.get_matches(lst[i],words)[0][0])
            else:
                lst[i] = lst[i]

        new_sent = ' '.join(lst)
        new_sent = new_sent.replace("  "," ")
        return new_sent
        