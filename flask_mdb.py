from flask import Flask, request, session, render_template, redirect, Response, jsonify
from pymongo.mongo_client import MongoClient
from wsgiref.util import request_uri
import pymongoFunc as mgf

app=Flask(__name__)
conn=MongoClient('localhost', 27017)

app.secret_key=b'aaa!111'


@app.route('/')
def mainpage():
    userid = session.get('email',None)
    return Response(render_template('index.html', userid=userid), 200)


@app.route("/sign_up", methods=['POST', 'GET'])     #회원가입
def register():
    error=None
    userid = session.get('email',None)
    if request.method == 'GET':
        if userid is not None:
            return redirect('/')
        else:
            return Response(render_template('sign_up.html'), 200)
    if request.method == 'POST':
        user={}
        userInfo={'age': None, 'sex' : None, 'height' : None, 'weight': None, 'part' : None}    #userInfo(table)에 저장할 데이터
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
            userInfo['sex'] = 0
        else:
            userInfo['sex'] = 1
        userInfo['exercise_level']=request.form.get('exercise_level')
        print(user)
        conn=mgf.connect_mongo(db='web')    #mongodb 접속
        if not(user['name'] and user['sex'] and user['id'] and user['password'] and user['Email'] and user['phoneNumber'] and userInfo['exercise_level']):
            return Response(render_template('sign_up.html', MessageInfo = "입력되지 않은 정보가 있습니다!"), 403)
        elif len(list(mgf.get_many_data(conn, 'web', 'loginInfo', {'id' : user['id']}))) != 0:
            return Response(render_template('sign_up.html', MessageInfo = "아이디가 이미 존재합니다."), 403)
        elif len(list(mgf.get_many_data(conn, 'web', 'loginInfo', {'Email' : user['Email']}))) != 0:
            return Response(render_template('sign_up.html', MessageInfo = "이메일이 이미 존재합니다."), 403)
        else:
            mgf.insert_one_data(conn, 'web', 'loginInfo', user)     #회원가입에 필요한 정보를 loginInfo(table)에 저장
            mgf.insert_one_data(conn, 'web', 'userInfo', userInfo)      #사용자 정보를 userInfo(table)에 저장
            return redirect('/')
        
        

@app.route('/login', methods=['POST', 'GET'])       #로그인
def login():
    userid = session.get('email',None)
    if request.method == 'GET':
        if userid is not None:
            return redirect('/')
        else:
            return Response(render_template('login.html'), 200)
    if request.method == 'POST':
        email = request.form['emailInput']
        pw = request.form.get("pwInput", type=str)
        conn=mgf.connect_mongo(db='web')        #mongodb 접속
        user=list(mgf.get_many_data(conn, 'web', 'loginInfo', {'Email' : email}))       #loginInfo(table)에서 입력받은 email 정보 받기
        if len(user) == 0:      #loginInfo(table)에 동일한 email이 존재하지 않는다면
            return Response(render_template('login.html', contents = "회원정보가 존재하지 않습니다."), 403)
        elif user[0]['password']==pw:
            session['email']=email      #로그인 성공 시 session에 email 저장
            return redirect('/')
        else:
            return Response(render_template('login.html', contents = "아이디가 틀렸습니다."), 403)
    
    
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
            return Response(render_template('input.html', userid=userid), 200)
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
            return Response(render_template('input.html', MessageInfo = userInfo['height']), 403)
        else:
            conn=mgf.connect_mongo(db='web')    #mongodb와 연결
            user=list(mgf.get_many_data(conn, 'web', 'loginInfo', {'Email' : userid}))      #userInfo(table)에서 동일한 Email에 해당하는 데이터 받기
            conn.web.userInfo.update_one({'id' : user[0]['id']},{'$set':userInfo})      #받은 데이터의 id에 해당하는 데이터 업데이트
            return redirect('/recommend')


@app.route('/recommend')    #recommend.html과 연결
def recommend():
    userid = session.get('email',None)
    if request.method == 'GET':
        if userid is None:
            return redirect('/login')
        else:
            return Response(render_template('recommend.html', userid=userid), 200)
    return Response(render_template('recommend.html', userid=userid), 200)

        
if __name__ == '__main__':
    app.run(debug=True)