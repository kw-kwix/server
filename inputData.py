#user.csv를 table에 추가하는 코드

from pymongo.mongo_client import MongoClient
import pandas as pd
import os
from config import MONGO_URL

# pandas to mongodb
def pd_to_dic(df):
    return df.to_dict('records')

# mongodb to pandas
def dic_to_pd(dic):
    return pd.DataFrame.from_records(dic)

client = MongoClient(MONGO_URL)
KWIX = client.KWIX    #db 연결
KWIX.userInfo.drop()

pd_data = pd.read_csv("user.csv")
dic_data=pd_to_dic(pd_data)

data=KWIX.recommendData  #conn.db.table 접근

data.insert_many(dic_data)  #table에 데이터 추가