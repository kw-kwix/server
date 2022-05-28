from flask import Flask, request, redirect, Response, jsonify
from pymongo.mongo_client import MongoClient
from config import MONGO_URL
from flask_cors import CORS
import mongo
import model

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
        elif mongo.find_user_id(KWIX, userInfo['id']) is not None:
            return jsonify(message="이미 있는 id입니다."), 403
        elif mongo.find_login_info(KWIX, user['email']) is not None:
            return jsonify(message="이미 있는 email입니다."), 403
        else:
            # 회원가입에 필요한 정보를 loginInfo(table)에 저장
            mongo.create_login_info(KWIX, user)
            mongo.create_user_info(KWIX, userInfo)
            return jsonify(message="success"), 200


@app.route('/login', methods=['POST', 'GET'])  # 로그인
def login():
    if request.method == 'POST':
        data = request.get_json()
        email = data['email']
        pw = data['password']
        user = mongo.find_login_info(KWIX, email)
        if user is None:  # loginInfo(table)에 동일한 email이 존재하지 않는다면
            return jsonify(message="이메일 주소가 없습니다."), 403
        elif user['password'] == pw:
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
            id = mongo.find_login_info(KWIX, userInfo["email"])["id"]
            mongo.update_user_info(KWIX, id, user)
            return jsonify(message="success"), 200


@app.route('/recommend', methods=['POST'])
def recommend():
    """Recommend API

    Request Body
    {
        "email": "example@example.com"
    }

    Returns:
        _type_: _description_
    """
    if request.method == 'POST':
        userInfo = request.get_json()
        email = userInfo["email"]
        user_id = mongo.find_login_info(KWIX, email)["id"]
        user_input = mongo.get_user(KWIX, user_id)[0]
        result = model.recommend(user_input)
        return jsonify(result=result.tolist())


if __name__ == '__main__':
    app.run(debug=True)
