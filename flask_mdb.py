from flask import Flask, request, session, render_template, redirect
from pymongo.mongo_client import MongoClient
from wsgiref.util import request_uri
import pymongoFunc as mgf

app=Flask(__name__)
conn=MongoClient('localhost', 27017)

app.secret_key=b'aaa!111'


@app.route('/')
def mainpage():
    userid = session.get('email',None)
    return render_template('index.html', userid=userid)


@app.route("/sign_up", methods=['POST', 'GET'])
def register():
    error=None
    userid = session.get('email',None)
    if request.method == 'GET':
        if userid is not None:
            return redirect('/')
        else:
            return render_template('sign_up.html')
    if request.method == 'POST':
        user={}
        userInfo={'age': None, 'sex' : None, 'height' : None, 'weight': None, 'part' : None}
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
        conn=mgf.connect_mongo(db='web')
        if not(user['name'] and user['sex'] and user['id'] and user['password'] and user['Email'] and user['phoneNumber'] and userInfo['exercise_level']):
            return render_template('sign_up.html', MessageInfo = "입력되지 않은 정보가 있습니다!")
        elif len(list(mgf.get_many_data(conn, 'web', 'loginInfo', {'id' : user['id']}))) != 0:
            return render_template('sign_up.html', MessageInfo = "아이디가 이미 존재합니다.")
        else:
            mgf.insert_one_data(conn, 'web', 'loginInfo', user)
            mgf.insert_one_data(conn, 'web', 'userInfo', userInfo)
            return redirect('/')
        
        

@app.route('/login', methods=['POST', 'GET'])
def login():
    userid = session.get('email',None)
    if request.method == 'GET':
        if userid is not None:
            return redirect('/')
    if request.method == 'POST':
        email = request.form['emailInput']
        pw = request.form.get("pwInput", type=str)
        conn=mgf.connect_mongo(db='web')
        user=list(mgf.get_many_data(conn, 'web', 'loginInfo', {'Email' : email}))
        if len(user) == 0:
            return render_template('login.html', contents = "회원정보가 존재하지 않습니다.")
        elif user[0]['password']==pw:
            session['email']=email
        return redirect('/')
    return render_template('login.html')
    
    
@app.route('/logout')
def logout():
    session.pop('email', None)
    return redirect('/')


@app.route("/input", methods=['POST', 'GET'])
def input():
    userid = session.get('email',None)
    if request.method == 'GET':
        if userid is None:
            return redirect('/login')
        else:
            return render_template('input.html', userid=userid)
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
                
        userInfo['part'] = j
        if not(userInfo['age'] and userInfo['height'] and userInfo['weight'] and userInfo['exercise_level']):
            return render_template('input.html', MessageInfo = userInfo['height'])
        else:
            conn=mgf.connect_mongo(db='web')
            user=list(mgf.get_many_data(conn, 'web', 'loginInfo', {'Email' : userid}))
            conn.web.userInfo.update_one({'id' : user[0]['id']},{'$set':userInfo})
            return redirect('/recommend')
#     error=None
#     if request.method == 'GET':
#         return render_template("input.html")
#     if request.method == 'POST':
#         conn=mgf.connect_mongo(db='web')
#         userInfo=list(mgf.get_many_data(conn, 'web', 'loginInfo', {'id' : session['id']}))
#         if len(userInfo)!=0:  #이미 저장된 정보가 있는가?
#             userInfo=userInfo[0]
#             #정보가 있다면 수정할 수 있도록
#         else: #없다면 새로 추가
#             userInfo={}
#             #input.html에서 수정해야함
#             #userInfo['id']=session['id']    id를 받을 것인가?
#             userInfo['age']=request.form.get('ageInput')
#             userInfo['sex']=request.form.get('inlineRadioOptions')
#             userInfo['id']=request.form.get('IdInput')
#             userInfo['height']=request.form.get('heightInput')
#             userInfo['weight']=request.form.get('weightInput')
#             userInfo['part']=request.form.get('part')
            
#         if not(userInfo['age'] and userInfo['sex'] and userInfo['sex'] and userInfo['id'] and userInfo['height'] and userInfo['weight'] and userInfo['part']):
#             return render_template('input.html', MessageInfo = "입력되지 않은 정보가 있습니다!")
#         else:
#             mgf.insert_one_data(conn, 'web', 'userInfo', userInfo)
#             return redirect('/')

@app.route('/recommend')
def recommend():
    userid = session.get('email',None)
    if request.method == 'GET':
        if userid is None:
            return redirect('/login')
        else:
            return render_template('recommend.html')
    return render_template('recommend.html', userid=userid)

        
if __name__ == '__main__':
    app.run(debug=True)