# server

## Command

### Install

```shell
pip install -r requirements.txt
```

### Start

```shell
python flask_mdb.py
```

### Docker

- use docker

```shell
docker build -t .
docker run -dp 5000:5000 server
```

- use docker-compose

```shell
docker-compose up -d --build
```

---
## table
- loginInfo : 로그인과 관련된 정보 저장
- suerInfo : 사용자의 정보 저장
- data : 'user.csv' 저장
---
1. /sign_up : 회원가입
  - name, birthdayDate, sex, id, password, Email, phoneNumber를 받아서 loginInfo(table)에 저장
  - 생성된 유저의 정보 중 추가할 수 있는 정보를 userInfo(table)에 저장
  - 생성된 유저의 정보를 NULL로 userInfo(table)에 저장(후에 userInfo(table)에서 update만 할 수 있도록)
  - 공백란이 존재 X
  - 동일한 아이디, 이메일 사용 X
---
2. /login : 로그인
  - Email를 받아 loginInfo(table)의 Email에 동일한 Email이 존재하는지 비교
  - Email이 존재한다면 loginInfo(table)에 데이터를 받아 pw를 비교 후 동일하다면 session에 Email저장 후 로그인
  - pw가 다르거나 Email이 존재하지 않는다면 로그인 X
---

3. /logout : 로그아웃
  - session에 email pop
---
4. /input : 유저 정보를 받음
  - session에 존재하는 email로 id를 받아서 id를 정보로 userInfo(table)에 접근
  - age, sex, height, weight, exercise_level, part를 받아서 userInfo(table)에 저장 (part는 2진수로 저장)
---
5. /recommend : recommend.html과 연결
