import schedule
import time
import pymysql
from sub_func import ahristock_bal, new_balance_ahri, clear_tick

def tick_open():
    tick = pymysql.connect(host="localhost",passwd="taebin0408!",user="root",db="tick")
    tick_cursor = tick.cursor(pymysql.cursors.DictCursor)
    sql = "select * from tick;"
    tick_cursor.execute(sql)
    res = tick_cursor.fetchall()
    if res[0]["TICK"] == 1:
        print("장이 이미 열려있음")
        return 0
    sql="update tick set TICK=1;"
    tick_cursor.execute(sql)
    tick.commit()
    print(ahristock_bal())

def tick_close():
    tick = pymysql.connect(host="localhost",passwd="taebin0408!",user="root",db="tick")
    tick_cursor = tick.cursor(pymysql.cursors.DictCursor)
    sql = "select * from tick;"
    tick_cursor.execute(sql)
    res = tick_cursor.fetchall()
    if res[0]["TICK"] == 0:
        print("장이 이미 닫혀있음")
        return 0
    sql="update tick set TICK=0;"
    tick_cursor.execute(sql)
    tick.commit()
    new_balance_ahri()
    clear_tick()

tick_close()
tick_open()
#schedule.every().day.at("").do(tick_open)

#while True:
    #schedule.run_pending()
    #time.sleep(1)
