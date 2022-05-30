from flask import jsonify
from pymongo.mongo_client import MongoClient
from config import MONGO_URL
from flask_cors import CORS
from flask_pydantic import validate
from flask_openapi3 import Info
from flask_openapi3 import OpenAPI
import mongo
import model
from models.user import UserBodyModel
from models.auth import LoginBodyModel, SignUpBodyModel
from models.recommend import RecommendBodyModel

info = Info(title='KWIX Recommend API', version='1.0.0')
app = OpenAPI(__name__, info=info)

CORS(app)
app.secret_key = b'aaa!111'

client = MongoClient(MONGO_URL)
KWIX = client.KWIX  # db 접근


@app.post("/sign_up")  # 회원가입
@validate()
def sign_up(body: SignUpBodyModel):
    userInfo = {'id': None, 'height': None, 'weight': None,
                'sex': None, 'age': None, 'bmi': None, 'during': None}
    userInfo['id'] = body.id
    userInfo['sex'] = body.sex
    if not(body.name and body.id and body.birthdayDate and body.password and body.email and body.phoneNumber):
        return jsonify(message="정보가 부족합니다."), 403
    elif mongo.find_user_id(KWIX, userInfo['id']) is not None:
        return jsonify(message="이미 있는 id입니다."), 403
    elif mongo.find_login_info(KWIX, body.email) is not None:
        return jsonify(message="이미 있는 email입니다."), 403
    else:
        # 회원가입에 필요한 정보를 loginInfo(table)에 저장
        mongo.create_login_info(KWIX, body.dict())
        mongo.create_user_info(KWIX, userInfo)
        return jsonify(message="success"), 200


@app.post('/login')  # 로그인
@validate()
def login(body: LoginBodyModel):
    user = mongo.find_login_info(KWIX, body.email)
    if user is None:  # loginInfo(table)에 동일한 email이 존재하지 않는다면
        return jsonify(message="이메일 주소가 없습니다."), 403
    elif user['password'] == body.password:
        return jsonify(message="success"), 200
    else:
        return jsonify(message="비밀번호가 틀렸습니다."), 403


@app.get('/logout')  # 로그아웃
def logout():
    return jsonify(message="success"), 200


@app.post("/input")  # 유저 정보를 받음
@validate()
def input(body: UserBodyModel):
    user = {}
    if not(body.age and body.height and body.weight):
        return jsonify(message="정보를 모두 입력하세요."), 403
    elif body.email is None:
        return jsonify(message="로그인이 필요합니다."), 403
    else:
        user['age'] = body.age
        user['height'] = body.height
        user['weight'] = body.weight
        id = mongo.find_login_info(KWIX, body.email)["id"]
        mongo.update_user_info(KWIX, id, user)
        return jsonify(message="success"), 200


@app.post('/recommend')
@validate()
def recommend(body: RecommendBodyModel):
    user_id = mongo.find_login_info(KWIX, body.email)["id"]
    user_input = mongo.get_user(KWIX, user_id)[0]
    result = model.recommend(user_input)
    return jsonify(result=result.tolist())


if __name__ == '__main__':
    app.run(debug=True)
