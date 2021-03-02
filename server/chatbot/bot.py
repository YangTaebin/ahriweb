from flask import Flask, jsonify, request
import pymysql
from sub_func import is_univ_id, is_sys_kakao,kakao_to_univ,money_balance,ahristock_amount,test_pattern_buy,change_stock,change_balance,ahristock_bal,center_hav,change_center,already_used_univ,sys_used,add_tick_buy,add_tick_sell

app = Flask(__name__)

@app.route('/',methods=['POST'])
def chat():
    tick = pymysql.connect(host="172.30.0.139",passwd="@dkfldkfl2021@",user="ahri",db="tick")
    tick_cursor = tick.cursor(pymysql.cursors.DictCursor)
    sql="select * from tick;"
    tick_cursor.execute(sql)
    tick_result = str(tick_cursor.fetchall()[0]['TICK'])

    temp = request.get_json()
    user_id = temp["userRequest"]["user"]["id"]
    print(temp)
    resp = {
        "version":"2.0",
        "template":{
            "outputs":[
                {
                    "simpleText":{
                        "text":""
                    }
                }
            ]
        }
    }
    resp_image = {
        "version":"2.0",
        "template":{
            "outputs":[
                {
                    "simpleImage":{
                        "imageUrl":""
                    }
                }
            ]
        }
    }
    msg = str(temp['userRequest']['utterance'])
    print(msg)

    sys_kakao = pymysql.connect(host="172.30.0.139",passwd="@dkfldkfl2021@",user="ahri",db="les_kakao")
    sys_kakao_cursor = sys_kakao.cursor(pymysql.cursors.DictCursor)

    if msg == "사진":
        resp_image["template"]["outputs"][0]["simpleImage"]["imageUrl"]="http://bf191e72268d.ngrok.io/static/res.jpg"
        return jsonify(resp_image)

    if msg == "등록":
        if is_sys_kakao(user_id):
            resp["template"]["outputs"][0]["simpleText"]["text"]="오류 이미 등록 중이십니다."
            return jsonify(resp)
        univ_id = temp["action"]["params"]["univid"]
        if not sys_used(univ_id):
            resp["template"]["outputs"][0]["simpleText"]["text"]="웹사이트에서 사용 등록을 하신 후에 이용해주시기 바랍니다."
            return jsonify(resp)
        if is_univ_id(univ_id):
            if already_used_univ(univ_id):
                resp['template']['outputs'][0]['simpleText']['text']="오류 이미 등록 중인 id입니다."
                return jsonify(resp)
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
    balance = money_balance(univ_id)
    ahristock = ahristock_amount(univ_id)
    stock_bal = ahristock_bal()
    center_have = center_hav()

    if msg == "주가":
        stock_type=["아리아리","주식1"]
        res = "총 주가"
        for i in stock_type:
            res += "\n"+str(i)+": "+str(stock_bal[i])
        resp['template']['outputs'][0]['simpleText']['text'] = res

    if msg == "계정 연결 해제":
        sql = "delete from is_les where kakao_id='"+user_id+"';"
        sys_kakao_cursor.execute(sql)
        sys_kakao.commit()
        resp['template']['outputs'][0]['simpleText']['text']="계정 연결이 해제되었습니다."

    if msg == "계정 정보":
        resp['template']['outputs'][0]['simpleText']['text']="닉네임: "+str(univ_id)+"\n잔액: "+str(balance)+"\n아리아리 주식수: "+str(ahristock["아리아리"])+"\n주식1 주식수: "+str(ahristock["주식1"])

    if msg=="매수":
        if tick_result == "0":
            resp["template"]["outputs"][0]["simpleText"]["text"] = "현재 거래 시간이 아닙니다."
            return jsonify(resp)
        buy_type = temp["action"]["params"]["type"]
        buy_amount = temp["action"]["params"]["amount"]
        stock_type_dict={"아리아리":"ahristock","주식1":"stocka"}
        print(buy_type,buy_amount)
        if test_pattern_buy(buy_type,buy_amount)==1:
            resp["template"]["outputs"][0]["simpleText"]["text"] = "주식 목록\n(아리아리, 주식1)\n에 해당하지 않는 목록입니다."
            return jsonify(resp)
        if test_pattern_buy(buy_type,buy_amount)==2:
            resp["template"]["outputs"][0]["simpleText"]["text"] = "갯수를 (1개) 의 형식으로 입력해주세요."
            return jsonify(resp)
        buy_amount = int(buy_amount[:-1])
        if int(balance)-(int(stock_bal[buy_type])*buy_amount) < 0:
            resp["template"]["outputs"][0]["simpleText"]["text"] = "잔액이 모자랍니다."
            return jsonify(resp)
        if (int(center_have[buy_type]) - int(buy_amount))<0:
            resp["template"]["outputs"][0]["simpleText"]["text"] = "죄송합니다. 주식이 더 이상 남아있지 않습니다."
            return jsonify(resp)
        change_center(stock_type_dict[buy_type], center_have[buy_type]-buy_amount)
        change_stock(univ_id, stock_type_dict[buy_type], int(ahristock[buy_type])+int(buy_amount))
        change_balance(univ_id, int(balance)-(int(stock_bal[buy_type])*buy_amount))
        add_tick_buy(stock_type_dict[buy_type], buy_amount)


        resp["template"]["outputs"][0]["simpleText"]["text"] = str(buy_type)+" 주식을 "+str(buy_amount)+"개 구입했습니다."

    if msg=="매도":
        if tick_result == "0":
            resp["template"]["outputs"][0]["simpleText"]["text"] = "현재 거래 시간이 아닙니다."
            return jsonify(resp)
        buy_type = temp["action"]["params"]["type"]
        buy_amount = temp["action"]["params"]["amount"]
        stock_type_dict={"아리아리":"ahristock","주식1":"stocka"}
        print(buy_type,buy_amount)
        if test_pattern_buy(buy_type,buy_amount)==1:
            resp["template"]["outputs"][0]["simpleText"]["text"] = "주식 목록\n(아리아리, 주식1)\n에 해당하지 않는 목록입니다."
            return jsonify(resp)
        if test_pattern_buy(buy_type,buy_amount)==2:
            resp["template"]["outputs"][0]["simpleText"]["text"] = "갯수를 (1개) 의 형식으로 입력해주세요."
            return jsonify(resp)
        buy_amount = int(buy_amount[:-1])
        if ahristock[buy_type]-buy_amount < 0:
            resp["template"]["outputs"][0]["simpleText"]["text"] = "판매할 주식이 모자랍니다."
            return jsonify(resp)
        change_center(stock_type_dict[buy_type], center_have[buy_type]+buy_amount)
        change_stock(univ_id, stock_type_dict[buy_type],int(ahristock[buy_type])-int(buy_amount))
        change_balance(univ_id, int(balance)+((int(stock_bal[buy_type])*buy_amount)*0.997))
        add_tick_sell(stock_type_dict[buy_type], buy_amount)


        resp["template"]["outputs"][0]["simpleText"]["text"] = str(buy_type)+" 주식을 "+str(buy_amount)+"개 판매했습니다."

    return jsonify(resp)

if __name__ == "__main__":
    app.run(host="0.0.0.0",port=5000)
