from flask import Flask, request, session, render_template, redirect, Response, jsonify
from pymongo.mongo_client import MongoClient
from wsgiref.util import request_uri
#import pymongoFunc as mgf
import os

app=Flask(__name__)

app.secret_key=b'aaa!111'

mongodb_url = os.environ.get("mongodb_url")
client = MongoClient(mongodb_url)  
KWIX = client.KWIX  #db 접근

@app.route('/')
def mainpage():
    userid = session.get('email',None)
    return Response(jsonify({"status" : 200}), 200) # jsonify({"status" : 200})


@app.route("/sign_up", methods=['POST', 'GET'])     #회원가입
def register():
    error=None
    userid = session.get('email',None)
    if request.method == 'GET':
        if userid is not None:
            return redirect('/')
        else:
            return Response(jsonify({"status" : 200}), 200)
    if request.method == 'POST':
        user={}
        userInfo={'id' : None, 'height' : None, 'weight' : None, 'sex' : None, 'age' : None, 'bmi' : None, 'during' : None}
            
        #userInfo={'age': None, 'sex' : None, 'height' : None, 'weight': None, 'part' : None}    #userInfo(table)에 저장할 데이터
        user['name']=request.form.get('NameInput')
        user['birthdayDate']=request.form.get('BirthInput')
        user['sex']=request.form.get('inlineRadioOptions')
        user['id']=request.form.get('IdInput')
        user['password']=request.form.get('pwInput')
        user['Email']=request.form.get('EmailInput')
        user['phoneNumber']=request.form.get('PhoneInput')
        # 
        userInfo['id']=user['id']
        userInfo['sex'] = user['sex']
        if user['sex'] == 'male':
            userInfo['sex'] = 1
        else:
            userInfo['sex'] = 0
        userInfo['exercise_level']=request.form.get('exercise_level')
        print(user)
        #conn=mgf.connect_mongo(db='web')    #mongodb 접속
        if not(user['name'] and user['sex'] and user['id'] and user['password'] and user['Email'] and user['phoneNumber'] and userInfo['exercise_level']):
            return Response(jsonify({"status" : 403}), 403)
        #elif len(list(mgf.get_many_data(conn, 'web', 'loginInfo', {'id' : user['id']}))) != 0:
        elif len(list(KWIX.loginInfo.find({'id' : user['id']}))) != 0:
            return Response(jsonify({"status" : 403}), 403)
        elif len(list(KWIX.loginInfo.find({'Email' : user['Email']}))) != 0:
            return Response(jsonify({"status" : 403}), 403)
        else:
            #mgf.insert_one_data(conn, 'web', 'loginInfo', user)     #회원가입에 필요한 정보를 loginInfo(table)에 저장
            #mgf.insert_one_data(conn, 'web', 'userInfo', userInfo)      #사용자 정보를 userInfo(table)에 저장
            KWIX.loginInfo.insert_one(user)
            KWIX.userInfo.insert_one(userInfo)
            return redirect('/')
        
@app.route('/login', methods=['POST', 'GET'])       #로그인
def login():
    userid = session.get('email',None)
    if request.method == 'GET':
        if userid is not None:
            return redirect('/')
        else:
            return Response(jsonify({"status" : 200}), 200)
    if request.method == 'POST':
        # if request.is_json():
            data = request.get_json()
            email = data['email']
            print(data)
            print(email)
            pw = data['password']
            user=list(KWIX.loginInfo.find({'email' : email}))
            print(user)
            if len(user) == 0:      #loginInfo(table)에 동일한 email이 존재하지 않는다면
                return Response(jsonify({"status" : 403}), 403)
            elif user[0]['password']==pw:
                session['email']=email      #로그인 성공 시 session에 email 저장
                return jsonify(message="success"), 200
            else:
                return Response(jsonify({"status" : 403}), 403)
            
            
# @app.route('/login', methods=['POST', 'GET'])       #로그인
# def login():
#     userid = session.get('email',None)
#     if request.method == 'GET':
#         if userid is not None:
#             return redirect('/')
#         else:
#             return Response(jsonify({"status" : 200}), 200)
#     if request.method == 'POST':
#         if request.is_json():
#             data = request.get_json()
#             email = data['email']
#             pw = data['password']
#             user=list(KWIX.loginInfo.find({'Email' : email}))
#             if len(user) == 0:      #loginInfo(table)에 동일한 email이 존재하지 않는다면
#                 return Response(jsonify({"status" : 403}), 403)
#             elif user[0]['password']==pw:
#                 session['email']=email      #로그인 성공 시 session에 email 저장
#                 return redirect('/')
#             else:
#                 return Response(jsonify({"status" : 403}), 403)

    
@app.route('/logout')       #로그아웃
def logout():
    session.pop('email', None)      #session에서 email 제거
    return redirect('/')


@app.route("/input", methods=['POST', 'GET'])       #유저 정보를 받음
def input():
    userid = session.get('email',None)
    if request.method == 'GET':
        if userid is None:
            return redirect('/login')
        else:
            return Response(jsonify({"status" : 200}), 200)
    if request.method == 'POST':
        userInfo={}
        userInfo['age'] = request.form.get('ageInput')
        userInfo['sex'] = request.form.get('inlineRadioOptions')
        userInfo['height'] = request.form.get('heightInput')
        userInfo['weight'] = request.form.get('weightInput')
        userInfo['exercise_level'] = request.form.get('exercise_level')
        j = 0
        for i in range(3):
            k = i+1
            st = 'scales' + str(k)
            if request.form.get(st) == 'on':
                if i == 0:
                    j = j + 1
                else:
                    j = j + 2 * i
        userInfo['part'] = j    #2진수로 받음
        if not(userInfo['age'] and userInfo['height'] and userInfo['weight'] and userInfo['exercise_level']):
            return Response(jsonify({"status" : 403}), 403)
        else:
            #conn=mgf.connect_mongo(db='web')    #mongodb와 연결
            #user=list(mgf.get_many_data(conn, 'web', 'loginInfo', {'Email' : userid}))      #userInfo(table)에서 동일한 Email에 해당하는 데이터 받기
            user=list(KWIX.loginInfo.find({'Email' : userid}))
            #conn.web.userInfo.update_one({'id' : user[0]['id']},{'$set':userInfo})      #받은 데이터의 id에 해당하는 데이터 업데이트
            KWIX.userInfo.update_one({'id' : user[0]['id']},{'$set':userInfo})
            return redirect('/recommend')


@app.route('/recommend')    #recommend.html과 연결
def recommend():
    userid = session.get('email',None)
    if request.method == 'GET':
        if userid is None:
            return redirect('/login')
        else:
            return Response(jsonify({"status" : 200}), 200)
    return Response(jsonify({"status" : 200}), 200)

        
if __name__ == '__main__':
    app.run(debug=True)