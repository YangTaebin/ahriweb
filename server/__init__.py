from flask import Flask, render_template,request,redirect
import pymysql
from sub_func import already_user, id_to_univ_id, already_univ, set_ahristock,quit_sys
import string
import random

app = Flask(__name__)

@app.route('/')
def main():
    return render_template('index.html',title="AHRIAHRI")

@app.route('/stock')
def stock():
    ahristock = pymysql.connect(
        user="root",
        passwd="taebin0408!",
        host="localhost",
        db="ahriweb"
    )
    ahristock_cursor = ahristock.cursor(pymysql.cursors.DictCursor)

    sql="SELECT * FROM `ahristock`;"
    ahristock_cursor.execute(sql)
    ahristock_result = ahristock_cursor.fetchall()

    ahristock_num = len(ahristock_result)
    ahristock_now = int(ahristock_result[ahristock_num-1]['stock'])

    return render_template("stock.html",title="아리아리 주식",ahristock=ahristock_now)

@app.route('/setstock')
def setstock():
    return render_template("setstock.html",title="주식 설정")

@app.route('/stock_change',methods=['POST'])
def changing_p():
    jong = request.form['jong']
    value = request.form['value']
    if jong=="ahri":
        ahristock=pymysql.connect(
            user="root",
            passwd="taebin0408!",
            db="ahriweb",
            host="localhost"
        )
        ahristock_cursor = ahristock.cursor(pymysql.cursors.DictCursor)

        sql="SELECT * FROM `ahristock`;"
        ahristock_cursor.execute(sql)
        ahristock_result = ahristock_cursor.fetchall()

        ahristock_num = len(ahristock_result)

        sql="insert into `ahristock` (num,stock) values ("+str(ahristock_num+1)+","+value+")"
        ahristock_cursor.execute(sql)
        ahristock.commit()
        return render_template('stock_changing.html',title="변경 완료",jong=jong,value=value)

@app.route('/log_res',methods=["POST"])
def log_res():
    id = request.form['id']
    print(id)

    ahriweb_user = pymysql.connect(
        user="root",
        passwd="taebin0408!",
        db="ahriweb_user",
        host="localhost"
    )
    ahri_system = pymysql.connect(
        user="root",
        passwd="taebin0408!",
        db="ahri_system",
        host="localhost"
    )
    sys_kakao = pymysql.connect(user="root",passwd="taebin0408!",db="les_kakao",host="localhost")
    ahriweb_user_cursor = ahriweb_user.cursor(pymysql.cursors.DictCursor)
    ahri_system_cursor = ahri_system.cursor(pymysql.cursors.DictCursor)
    sys_kakao_cursor = sys_kakao.cursor(pymysql.cursors.DictCursor)

    sql="SELECT * FROM `user`;"
    ahriweb_user_cursor.execute(sql)
    ahriweb_user_result = ahriweb_user_cursor.fetchall()
    print(ahriweb_user_result)
    n = len(ahriweb_user_result)

    if not already_user(id):
        univ = ""
        while 1:
            for i in range(6):
                univ += random.choice(string.ascii_lowercase)
                print(univ)
            if not already_univ(univ):
                break
            univ = ""
        sql = "insert into `user` (kakao_login_id,univ_id) values ("+id+",'"+univ+"');"
        sql_sys = "insert into `sys_user` (univ_id,is_les) values ('"+univ+"',0);"
        print(sql_sys)
        ahriweb_user_cursor.execute(sql)
        ahri_system_cursor.execute(sql_sys)
        ahriweb_user.commit()
        ahri_system.commit()

    else: print("이미 등록 완료")

    return id

@app.route('/profile',methods=['POST'])
def profile():
    id = request.form['id']
    print(id)

    univ_id = id_to_univ_id(id)
    print(univ_id)

    ahri_system = pymysql.connect(
        user="root",
        passwd="taebin0408!",
        db="ahri_system",
        host="localhost"
    )
    ahri_system_cursor = ahri_system.cursor(pymysql.cursors.DictCursor)

    sql = "select * from sys_user;"
    ahri_system_cursor.execute(sql)
    ahri_system_result = ahri_system_cursor.fetchall()
    for i in ahri_system_result:
        if i["univ_id"] == univ_id:
            lesisted = i["is_les"]
    if str(lesisted) == "0":
        return render_template("profile.html", title="사용자 프로필", num = univ_id, is_le=str(lesisted))
    if str(lesisted) == "1":
        balance = pymysql.connect(user="root",passwd="taebin0408!",db="balance",host="localhost")
        balance_cursor = balance.cursor(pymysql.cursors.DictCursor)
        sql = "select * from balance_user;"
        balance_cursor.execute(sql)
        balance_result = balance_cursor.fetchall()
        for i in balance_result:
            if i["univ_id"]==univ_id:
                balance_money = i["balance"]
        return render_template("profile.html", title="사용자 프로필", num = univ_id, is_le=str(lesisted), balance=balance_money)

@app.route('/community')
def community():
    commun = pymysql.connect(
        user="root",
        passwd="taebin0408!",
        db="community",
        host="localhost"
    )
    commun_cursor = commun.cursor(pymysql.cursors.DictCursor)

    sql="SELECT * FROM `content`;"
    commun_cursor.execute(sql)
    commun_result = commun_cursor.fetchall()
    return render_template("community.html", title="커뮤니티",content=reversed(commun_result))

@app.route('/writing')
def writing():
    return render_template("writing.html",title="글쓰기")

@app.route('/submit_write',methods=['POST'])
def sub_write():
    writer = request.form['writer']
    content = request.form['content']
    print(writer, content)

    commun = pymysql.connect(
        user="root",
        passwd="taebin0408!",
        db="community",
        host="localhost"
    )
    commun_cursor = commun.cursor(pymysql.cursors.DictCursor)

    sql="SELECT * FROM `content`;"
    commun_cursor.execute(sql)
    commun_result = commun_cursor.fetchall()
    print(commun_result)
    n = len(commun_result)

    sql = "insert into content (Num, content, writer) values ("+str(n+1)+",'"+str(content)+"','"+writer+"');"
    commun_cursor.execute(sql)
    commun.commit()

    return redirect("/community")

@app.route('/show_content')
def show_content():
    Num = request.args.get('N',"0")

    commun = pymysql.connect(
        user="root",
        passwd="taebin0408!",
        db="community",
        host="localhost"
    )
    commun_cursor = commun.cursor(pymysql.cursors.DictCursor)

    sql="SELECT * FROM `content`;"
    commun_cursor.execute(sql)
    commun_result = commun_cursor.fetchall()

    return render_template("show_content.html",title="커뮤니티",writer=commun_result[int(Num)-1]["writer"],content=commun_result[int(Num)-1]["content"])

@app.route("/les_sys",methods=["POST"])
def les_sys():
    id = request.form["id"]
    print(id)

    univ_id = id_to_univ_id(id)

    ahri_system = pymysql.connect(
        user="root",
        passwd="taebin0408!",
        db="ahri_system",
        host="localhost"
    )
    balance = pymysql.connect(user="root",passwd="taebin0408!",db="balance",host="localhost")
    balance_cursor = balance.cursor(pymysql.cursors.DictCursor)
    ahri_system_cursor = ahri_system.cursor(pymysql.cursors.DictCursor)

    sql="update sys_user set is_les=1 where univ_id='"+univ_id+"';"
    sql_balance = "insert into balance_user (univ_id,balance) values ('"+univ_id+"',100000);"
    ahri_system_cursor.execute(sql)
    balance_cursor.execute(sql_balance)
    ahri_system.commit()
    balance.commit()

    set_ahristock(univ_id)

    return redirect("/")

@app.route("/quit",methods=["POST"])
def quit():
    id = request.form["id"]
    univ_id = id_to_univ_id(id)
    quit_sys(univ_id)
    return redirect("/")

if __name__ == "__main__":
    app.run(host="0.0.0.0",port=80)
