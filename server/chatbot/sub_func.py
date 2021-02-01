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
