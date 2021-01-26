from flask import Flask, render_template,request
import pymysql
from sub_func import already_user

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
    ahriweb_user_cursor = ahriweb_user.cursor(pymysql.cursors.DictCursor)

    sql="SELECT * FROM `user`;"
    ahriweb_user_cursor.execute(sql)
    ahriweb_user_result = ahriweb_user_cursor.fetchall()
    print(ahriweb_user_result)
    user_num = len(ahriweb_user_result)

    if not already_user(id):
        sql = "insert into `user` (kakao_login_id,univ_id) values ("+id+","+str(user_num+1)+");"
        ahriweb_user_cursor.execute(sql)
        ahriweb_user.commit()

    else: print("이미 등록 완료")

    return id

if __name__ == "__main__":
    app.run(host="0.0.0.0",port=80)
