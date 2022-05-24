import pandas as pd
import pymongo

# 1. conn 연결하는 함수
def connect_mongo(host='localhost', port=27017, username=None, passwd=None, db=None):
    if username and passwd:
        mongo_uri = 'mongodb://%s:%s@%s:%s/%s' % (username, passwd, host, port, db)
        conn = pymongo.MongoClient(mongo_uri)
    else:
        conn = pymongo.MongoClient(host, port)
        
    return conn # conn을 출력한다.

# 2. db의 종류를 보여주는 함수
def show_dblist(conn):
    print(conn.list_database_names())
    
# 2-2 db를 받는 함수
def get_dblist(conn): # db들을 list로 반환한다.
    return conn.list_database_names()

# 2-3 collection의 종류를 보여주는 함수
def show_collection_list(conn, db):
    print(conn[db].list_collection_names())
    
# 2-4 collection의 종류를 list로 받는 함수
def get_collection_list(conn, db):
    return conn[db].list_collection_names()
    
# 3. 정보를 입력하는 함수 

def insert_one_data(conn, db, collection, dict):
    if 'dict' in str(type(dict)):
        conn[db][collection].insert_one(dict)
    elif 'list' in str(type(dict)):
        if len(dict) > 1:
            raise ValueError
        conn[db][collection].insert_one(dict[0])

def insert_many_data(conn, db, collection, list): # dict을 원소로하는 list를 받아서 입력
    conn[db][collection].insert_many(list)
    
# 4. 정보를 받아주는 함수 -> find 사용

def get_many_data(conn, db, collection, query={}): # dict을 원소로하는 list 반환
    return conn[db][collection].find(query)  #cursor type이므로 list로 변환해주어야 함

def get_one_data(conn, db, collection):
    val = []# find_one을 수행해주는 함수
    val.append(conn[db][collection].find_one())
    return val  #list type

# 5. pandas to mongodb
def pd_to_dic(df):
    return df.to_dict('records')

# 6. mongodb to pandas
def dic_to_pd(dic):
    return pd.DataFrame.from_records(dic)
##################

# 받는 형식을 li나 dict이 아닌 형태로 변환해주는 함수
# 넣는 형식을 dict이나 li가 아닌 pandas로 변환