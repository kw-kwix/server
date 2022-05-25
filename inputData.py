#user.csv를 table에 추가하는 파일

from pymongo.mongo_client import MongoClient
import pandas as pd

# pandas to mongodb
def pd_to_dic(df):
    return df.to_dict('records')

# mongodb to pandas
def dic_to_pd(dic):
    return pd.DataFrame.from_records(dic)


conn=MongoClient('localhost', 27017)    #db 연결

pd_data = pd.read_csv("user.csv")
dic_data=pd_to_dic(pd_data)

data=conn.web.Data  #conn.db.table 접근

data.insert_many(dic_data)  #table에 데이터 추가