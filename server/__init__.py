from flask import Flask, render_template
import pymysql

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

@app.route('/setahristock')
def setstock():
    pass

if __name__ == "__main__":
    app.run(host="0.0.0.0",port=80)
