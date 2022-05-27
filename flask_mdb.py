from flask import Flask, request, redirect, Response, jsonify
from pymongo.mongo_client import MongoClient
from config import MONGO_URL
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
app.secret_key = b'aaa!111'

client = MongoClient(MONGO_URL)
KWIX = client.KWIX  # db 접근


@app.route("/sign_up", methods=['POST', 'GET'])  # 회원가입
def sign_up():
    if request.method == 'POST':
        userInfo = {'id': None, 'height': None, 'weight': None,
                    'sex': None, 'age': None, 'bmi': None, 'during': None}
        user = request.get_json()
        userInfo['id'] = user['id']
        userInfo['sex'] = user['sex']
        if not(user['name'] and user['id'] and user['birthdayDate'] and user['password'] and user['email'] and user['phoneNumber']):
            return jsonify(message="정보가 부족합니다."), 403
        elif len(list(KWIX.loginInfo.find({'id': user['id']}))) != 0:
            return jsonify(message="이미 있는 id입니다."), 403
        elif len(list(KWIX.loginInfo.find({'email': user['email']}))) != 0:
            return jsonify(message="이미 있는 email입니다."), 403
        else:
            # 회원가입에 필요한 정보를 loginInfo(table)에 저장
            KWIX.loginInfo.insert_one(user)
            KWIX.userInfo.insert_one(userInfo)  # 사용자 정보를 userInfo(table)에 저장
            return jsonify(message="success"), 200


@app.route('/login', methods=['POST', 'GET'])  # 로그인
def login():
    if request.method == 'POST':
        data = request.get_json()
        email = data['email']
        pw = data['password']
        user = list(KWIX.loginInfo.find({'email': email}))
        if len(user) == 0:  # loginInfo(table)에 동일한 email이 존재하지 않는다면
            return jsonify(message="이메일 주소가 없습니다."), 403
        elif user[0]['password'] == pw:
            return jsonify(message="success"), 200
        else:
            return jsonify(message="비밀번호가 틀렸습니다."), 403


@app.route('/logout')  # 로그아웃
def logout():
    return jsonify(message="success"), 200


@app.route("/input", methods=['POST', 'GET'])  # 유저 정보를 받음
def input():
    if request.method == 'POST':
        user = {}
        userInfo = request.get_json()
        if not(userInfo['age'] and userInfo['height'] and userInfo['weight']):
            return jsonify(message="정보를 모두 입력하세요."), 403
        elif userInfo.get("email") is None:
            return jsonify(message="로그인이 필요합니다."), 403
        else:
            user['age'] = userInfo['age']
            user['height'] = userInfo['height']
            user['weight'] = userInfo['weight']
            id = KWIX.loginInfo.find_one({'email': userInfo["email"]})["id"]
            KWIX.userInfo.update_one({'id': id}, {'$set': user})
            return jsonify(message="success"), 200


@app.route('/recommend')  # recommend.html과 연결
def recommend():
    if request.method == 'GET':
        return Response(jsonify({"status": 200}), 200)


if __name__ == '__main__':
    app.run(debug=True)
