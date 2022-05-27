from flask import Flask, request, session, render_template, redirect, Response, jsonify
from pymongo.mongo_client import MongoClient
from wsgiref.util import request_uri
from config import MONGO_URL
from flask_cors import CORS

app=Flask(__name__)
CORS(app)
app.secret_key=b'aaa!111'

client = MongoClient(MONGO_URL)  
KWIX = client.KWIX  #db 접근

@app.route('/')
def mainpage():
    userid = session.get('email',None)
    return Response(jsonify({"status" : 200}), 200) # jsonify({"status" : 200})


@app.route("/sign_up", methods=['POST', 'GET'])     #회원가입
def sign_up():
    error=None
    userid = session.get('email',None)
    if request.method == 'GET':
        if userid is not None:
            return redirect('/')
        else:
            return Response(jsonify({"status" : 200}), 200)
    if request.method == 'POST':
        userInfo={'id' : None, 'height' : None, 'weight' : None, 'sex' : None, 'age' : None, 'bmi' : None, 'during' : None}

        user = request.get_json()       
        userInfo['id']=user['id']
        userInfo['sex'] = user['sex']
        if not(user['name'] and user['id'] and user['birthdayDate'] and user['password'] and user['email'] and user['phoneNumber']):
            return Response(jsonify({"status": 403}), 403)
        elif len(list(KWIX.loginInfo.find({'id' : user['id']}))) != 0:
            return Response(jsonify({"status": 403}), 403)
        elif len(list(KWIX.loginInfo.find({'email' : user['email']}))) != 0:
            return Response(jsonify({"status": 403}), 403)
        else:
            KWIX.loginInfo.insert_one(user) #회원가입에 필요한 정보를 loginInfo(table)에 저장
            KWIX.userInfo.insert_one(userInfo)  #사용자 정보를 userInfo(table)에 저장
            return jsonify(message="success"), 200


@app.route('/login', methods=['POST', 'GET'])  # 로그인
def login():
    userid = session.get('email', None)
    if request.method == 'GET':
        if userid is not None:
            return redirect('/')
        else:
            return Response(jsonify({"status": 200}), 200)
    if request.method == 'POST':
        # if request.is_json():
        data = request.get_json()
        email = data['email']
        print(data)
        print(email)
        pw = data['password']
        user = list(KWIX.loginInfo.find({'email': email}))
        print(user)
        if len(user) == 0:  # loginInfo(table)에 동일한 email이 존재하지 않는다면
            return Response(jsonify({"status": 403}), 403)
        elif user[0]['password'] == pw:
            session['email'] = email  # 로그인 성공 시 session에 email 저장
            return jsonify(message="success"), 200
        else:
            return Response(jsonify({"status": 403}), 403)
    
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
        user={}
        userInfo = request.get_json()
        if not(userInfo['age'] and userInfo['height'] and userInfo['weight']):
            return Response(jsonify({"status" : 403}), 403)
        else:
            user['age']=userInfo['age']
            user['height']=userInfo['height']
            user['weight']=userInfo['weight']
            user=list(KWIX.loginInfo.find({'email' : userid}))
            KWIX.userInfo.update_one({'id' : user[0]['id']},{'$set':user})
            return jsonify(message="success"), 200


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