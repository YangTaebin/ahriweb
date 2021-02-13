import schedule
import time
import pymysql
from sub_func import ahristock_bal, new_balance_ahri

def tick_open():
    tick = pymysql.connect(host="localhost",passwd="taebin0408!",user="root",db="tick")
    tick_cursor = tick.cursor(pymysql.cursors.DictCursor)
    sql="update tick set TICK=1;"
    tick_cursor.execute(sql)
    tick.commit()
    print(ahristock_bal())

def tick_close():
    tick = pymysql.connect(host="localhost",passwd="taebin0408!",user="root",db="tick")
    tick_cursor = tick.cursor(pymysql.cursors.DictCursor)
    sql="update tick set TICK=0;"
    tick_cursor.execute(sql)
    tick.commit()
    ahribal = pymysql.connect(host="localhost",passwd="taebin0408!",user="root",db="ahriweb")
    ahribal_cursor = tick.cursor(pymysql.cursors.DictCursor)
    sql="select * from ahristock;"
    ahribal_cursor.execute(sql)
    n = len(ahribal_cursor.fetchall())
    new_bal = new_balance_ahri()
    sql="insert into ahristock (num,stock) values ("+str(n+1)+","+str(new_bal)+");"
    ahribal_cursor.execute(sql)
    ahribal.commit()

schedule_time = [
    "9:10"
]

schedule.every().day.at("").do(tick_open)

while True:
    schedule.run_pending()
    time.sleep(1)
