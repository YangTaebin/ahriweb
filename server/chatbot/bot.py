from flask import Flask, jsonify, request
import pymysql
from sub_func import is_univ_id, is_sys_kakao,kakao_to_univ

app = Flask(__name__)

@app.route('/',methods=['POST'])
def chat():
    temp = request.get_json()
    user_id = temp["userRequest"]["user"]["id"]
    resp = {
        "version":"2.0",
        "template":{
            "outputs":[
                {
                    "simpleText":{
                        "text":"Responce"
                    }
                }
            ]
        }
    }
    msg = str(temp['userRequest']['utterance'])

    sys_kakao = pymysql.connect(host="localhost",passwd="taebin0408!",user="root",db="les_kakao")
    sys_kakao_cursor = sys_kakao.cursor(pymysql.cursors.DictCursor)

    if msg == "등록":
        if is_sys_kakao(user_id):
            resp["template"]["outputs"][0]["simpleText"]["text"]="오류 이미 등록 중이십니다."
            return jsonify(resp)
        univ_id = temp["action"]["params"]["univid"]
        if is_univ_id(univ_id):
            sql="insert into is_les (univ_id,kakao_id) values ('"+univ_id+"','"+user_id+"');"
            sys_kakao_cursor.execute(sql)
            sys_kakao.commit()
            resp['template']['outputs'][0]['simpleText']['text']="등록되었습니다."
        else:
            resp["template"]["outputs"][0]["simpleText"]["text"]="오류 잘못된 univ_id 입니다."

    if not is_sys_kakao(user_id):
        resp["template"]["outputs"][0]["simpleText"]["text"]="오류 등록을 해주세요."
        return jsonify(resp)

    univ_id = kakao_to_univ(user_id)

    if msg == "계정 연결 해제":
        sql = "delete from is_les where kakao_id='"+user_id+"';"
        sys_kakao_cursor.execute(sql)
        sys_kakao.commit()
        resp['template']['outputs'][0]['simpleText']['text']="계정 연결이 해제되었습니다."

    if msg == "계정 정보":
        resp['template']['outputs'][0]['simpleText']['text']="닉네임: "+str(univ_id)

    return jsonify(resp)

if __name__ == "__main__":
    app.run(host="0.0.0.0",port=5000)
