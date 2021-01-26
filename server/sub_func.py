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
