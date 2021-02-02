import pymysql

def already_user(id):
    user = pymysql.connect(
        user="root",
        passwd="taebin0408!",
        db="ahriweb_user",
        host="localhost"
    )

    user_cursor = user.cursor(pymysql.cursors.DictCursor)

    sql="SELECT * FROM `user`;"
    user_cursor.execute(sql)
    user_list = user_cursor.fetchall()

    for i in user_list:
        if id == i['kakao_login_id']:
            return True
    return False

def id_to_univ_id(id):
    user = pymysql.connect(
        user="root",
        passwd="taebin0408!",
        db="ahriweb_user",
        host="localhost"
    )

    user_cursor = user.cursor(pymysql.cursors.DictCursor)

    sql="SELECT * FROM `user`;"
    user_cursor.execute(sql)
    user_list = user_cursor.fetchall()

    for i in user_list:
        if id == i['kakao_login_id']:
            return i['univ_id']
    return 0

def already_univ(univ_id):
    user = pymysql.connect(
        user="root",
        passwd="taebin0408!",
        db="ahriweb_user",
        host="localhost"
    )

    user_cursor = user.cursor(pymysql.cursors.DictCursor)

    sql="SELECT * FROM `user`;"
    user_cursor.execute(sql)
    user_list = user_cursor.fetchall()

    for i in user_list:
        if univ_id==i['univ_id']:
            return True
    return False

def set_ahristock(univ_id):
    ahristock = pymysql.connect(host="localhost",user="root",passwd="taebin0408!",db="ahristock")
    ahristock_cursor = ahristock.cursor(pymysql.cursors.DictCursor)
    sql="insert into ahristock (univ_id,amount) values ('"+univ_id+"',0);"
    ahristock_cursor.execute(sql)
    ahristock.commit()

def quit_sys(univ_id):
    ahri_sys = pymysql.connect(host="localhost",user="root",passwd="taebin0408!",db="ahri_system")
    ahristock = pymysql.connect(host="localhost",user="root",passwd="taebin0408!",db="ahristock")
    balance = pymysql.connect(host="localhost",user="root",passwd="taebin0408!",db="balance")
    les_kakao = pymysql.connect(host="localhost",user="root",passwd="taebin0408!",db="les_kakao")
    ahri_sys_cursor = ahri_sys.cursor(pymysql.cursors.DictCursor)
    ahristock_cursor = ahristock.cursor(pymysql.cursors.DictCursor)
    balance_cursor = balance.cursor(pymysql.cursors.DictCursor)
    les_kakao_cursor = les_kakao.cursor(pymysql.cursors.DictCursor)

    sql = "update sys_user set is_les=0 where univ_id='"+univ_id+"';"
    ahri_sys_cursor.execute(sql)
    ahri_sys.commit()

    sql = "delete from ahristock where univ_id='"+univ_id+"';"
    ahristock_cursor.execute(sql)
    ahristock.commit()

    sql = "delete from balance_user where univ_id='"+univ_id+"';"
    balance_cursor.execute(sql)
    balance.commit()

    sql = "delete from is_les where univ_id='"+univ_id+"';"
    les_kakao_cursor.execute(sql)
    les_kakao.commit()
