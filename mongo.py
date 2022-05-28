from pymongo.database import Database
from db import dic_to_pd


def create_login_info(db: Database, login_info):
    db.loginInfo.insert_one(login_info)


def create_user_info(db: Database, user_info):
    db.userInfo.insert_one(user_info)


def update_user_info(db: Database, user_id, user_info):
    db.userInfo.update_one({'id': user_id}, {'$set': user_info})


def find_login_info(db: Database, email):
    return db.loginInfo.find_one({'email': email})


def find_user_id(db: Database, user_id):
    return db.loginInfo.find_one({'id': user_id})


def get_user(db: Database, user_id):
    userInfo = db.userInfo
    rows = userInfo.find({'id': user_id})
    data = []
    for row in rows:
        data.append(row)

    pd = dic_to_pd(data)

    data = pd[['id', 'height', 'weight', 'sex',
               'age', 'bmi', 'during']].to_numpy()

    return data
