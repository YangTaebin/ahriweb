import string
import pymysql

def is_univ_id(univ_id):
    lowercase = list(string.ascii_lowercase)
    if len(univ_id) != 6: return False
    for i in range(6):
        if univ_id[i] not in lowercase:
            return False
    return True

def is_sys_kakao(kakao_id):
    sys_kakao = pymysql.connect(host="localhost",passwd="taebin0408!",user="root",db="les_kakao")
    sys_kakao_cursor = sys_kakao.cursor(pymysql.cursors.DictCursor)
    sql="select * from `is_les`;"
    sys_kakao_cursor.execute(sql)
    is_les = sys_kakao_cursor.fetchall()

    for i in is_les:
        if i["kakao_id"] == kakao_id: return True
    return False

def kakao_to_univ(kakao_id):
    sys_kakao = pymysql.connect(host="localhost",passwd="taebin0408!",user="root",db="les_kakao")
    sys_kakao_cursor = sys_kakao.cursor(pymysql.cursors.DictCursor)
    sql="select * from `is_les`;"
    sys_kakao_cursor.execute(sql)
    is_les = sys_kakao_cursor.fetchall()

    for i in is_les:
        if i["kakao_id"] == kakao_id:
            return i["univ_id"]

def money_balance(univ_id):
    balance = pymysql.connect(host="localhost",passwd="taebin0408!",user="root",db="balance")
    balance_cursor = balance.cursor(pymysql.cursors.DictCursor)
    sql="select * from `balance_user`;"
    balance_cursor.execute(sql)
    balance_list = balance_cursor.fetchall()

    for i in balance_list:
        if i["univ_id"] == univ_id:
            return i["balance"]

def ahristock_amount(univ_id):
    ahristock = pymysql.connect(host="localhost",user="root",passwd="taebin0408!",db="ahristock")
    ahristock_cursor = ahristock.cursor(pymysql.cursors.DictCursor)
    sql = "select * from ahristock;"
    ahristock_cursor.execute(sql)
    ahristock_list = ahristock_cursor.fetchall()

    for i in ahristock_list:
        if i["univ_id"] == univ_id:
            return i["amount"]

def test_pattern_buy(buy_type, buy_amount):
    stock_list = ["아리아리"]
    if buy_type not in stock_list:
        return 1
    if ((buy_amount[-1] != "개") or (not buy_amount[:-1].isdigit())):
        return 2
    return 0

def ahristock_bal():
    bal = pymysql.connect(host="localhost",user="root",passwd="taebin0408!",db="ahriweb")
    bal_cursor = bal.cursor(pymysql.cursors.DictCursor)
    sql="select * from ahristock;"
    bal_cursor.execute(sql)
    bal_li = bal_cursor.fetchall()
    return bal_li[-1]["stock"]

def change_stock(univ_id, type, amount):
    cs = pymysql.connect(host="localhost",user="root",passwd="taebin0408!",db=type)
    cs_cursor = cs.cursor(pymysql.cursors.DictCursor)
    sql = "update "+type+" set amount="+str(amount)+" where univ_id='"+univ_id+"';"
    cs_cursor.execute(sql)
    cs.commit()

def change_balance(univ_id, amount):
    cs = pymysql.connect(host="localhost",user="root",passwd="taebin0408!",db="balance")
    cs_cursor = cs.cursor(pymysql.cursors.DictCursor)
    sql = "update balance_user set balance="+str(amount)+" where univ_id='"+univ_id+"';"
    cs_cursor.execute(sql)
    cs.commit()

def center_hav():
    ch = pymysql.connect(host="localhost",user="root",passwd="taebin0408!",db="center")
    ch_cursor = ch.cursor(pymysql.cursors.DictCursor)
    sql = "select * from center;"
    ch_cursor.execute(sql)
    center_li = ch_cursor.fetchall()
    return center_li[0]["center_have"]

def change_center(amount):
    ch = pymysql.connect(host="localhost",user="root",passwd="taebin0408!",db="center")
    ch_cursor = ch.cursor(pymysql.cursors.DictCursor)
    sql = "update center set center_have="+str(amount)+";"
    ch_cursor.execute(sql)
    ch.commit()

def already_used_univ(univ_id):
    auu = pymysql.connect(host="localhost",user="root",passwd="taebin0408!",db="les_kakao")
    auu_cursor = auu.cursor(pymysql.cursors.DictCursor)
    sql = "select * from is_les;"
    auu_cursor.execute(sql)
    auu_res = auu_cursor.fetchall()
    for i in auu_res:
        if i["univ_id"] == univ_id:
            return True
    return False

def sys_used(univ_id):
    su = pymysql.connect(host="localhost",user="root",passwd="taebin0408!",db="ahri_system")
    su_cursor = su.cursor(pymysql.cursors.DictCursor)
    sql = "select * from sys_user;"
    su_cursor.execute(sql)
    su_li = su_cursor.fetchall()
    for i in su_li:
        if i["univ_id"] == univ_id:
            if i["is_les"] == 1:
                return True
            else:
                return False


def new_balance_ahri():
    
