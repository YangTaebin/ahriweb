import string
import pymysql
from win32com.client import Dispatch

def is_univ_id(univ_id):
    lowercase = list(string.ascii_lowercase)
    if len(univ_id) != 6: return False
    for i in range(6):
        if univ_id[i] not in lowercase:
            return False
    return True

def is_sys_kakao(kakao_id):
    sys_kakao = pymysql.connect(host="172.30.0.139",passwd="@dkfldkfl2021@",user="ahri",db="les_kakao")
    sys_kakao_cursor = sys_kakao.cursor(pymysql.cursors.DictCursor)
    sql="select * from `is_les`;"
    sys_kakao_cursor.execute(sql)
    is_les = sys_kakao_cursor.fetchall()

    for i in is_les:
        if i["kakao_id"] == kakao_id: return True
    return False

def kakao_to_univ(kakao_id):
    sys_kakao = pymysql.connect(host="172.30.0.139",passwd="@dkfldkfl2021@",user="ahri",db="les_kakao")
    sys_kakao_cursor = sys_kakao.cursor(pymysql.cursors.DictCursor)
    sql="select * from `is_les`;"
    sys_kakao_cursor.execute(sql)
    is_les = sys_kakao_cursor.fetchall()

    for i in is_les:
        if i["kakao_id"] == kakao_id:
            return i["univ_id"]

def money_balance(univ_id):
    balance = pymysql.connect(host="172.30.0.139",passwd="@dkfldkfl2021@",user="ahri",db="balance")
    balance_cursor = balance.cursor(pymysql.cursors.DictCursor)
    sql="select * from `balance_user`;"
    balance_cursor.execute(sql)
    balance_list = balance_cursor.fetchall()

    for i in balance_list:
        if i["univ_id"] == univ_id:
            return i["balance"]

def ahristock_amount(univ_id):
    stock_type=["ahristock","stocka"]
    type_dict={"ahristock":"아리아리","stocka":"주식1"}
    return_dict={}
    for i in stock_type:
        stock = pymysql.connect(host="172.30.0.139",user="ahri",passwd="@dkfldkfl2021@", db=str(i))
        stock_cursor = stock.cursor(pymysql.cursors.DictCursor)
        sql = "select * from "+str(i)+";"
        stock_cursor.execute(sql)
        res = stock_cursor.fetchall()
        for j in res:
            if j["univ_id"] == univ_id:
                return_dict[type_dict[i]] = j["amount"]
    return return_dict

def test_pattern_buy(buy_type, buy_amount):
    stock_list = ["아리아리","주식1"]
    if buy_type not in stock_list:
        return 1
    if ((buy_amount[-1] != "개") or (not buy_amount[:-1].isdigit())):
        return 2
    return 0

def ahristock_bal():
    stock_type=["ahristock","stocka"]
    type_dict={"ahristock":"아리아리","stocka":"주식1"}
    return_dict={}
    for i in stock_type:
        stock = pymysql.connect(host="172.30.0.139",user="ahri",passwd="@dkfldkfl2021@", db="ahriweb")
        stock_cursor = stock.cursor(pymysql.cursors.DictCursor)
        sql = "select * from "+str(i)+";"
        stock_cursor.execute(sql)
        res = stock_cursor.fetchall()
        return_dict[type_dict[i]] = res[len(res)-1]["stock"]
    return return_dict

def change_stock(univ_id, type, amount):
    cs = pymysql.connect(host="172.30.0.139",user="ahri",passwd="@dkfldkfl2021@",db=type)
    cs_cursor = cs.cursor(pymysql.cursors.DictCursor)
    sql = "update "+type+" set amount="+str(amount)+" where univ_id='"+univ_id+"';"
    cs_cursor.execute(sql)
    cs.commit()

def change_balance(univ_id, amount):
    cs = pymysql.connect(host="172.30.0.139",user="ahri",passwd="@dkfldkfl2021@",db="balance")
    cs_cursor = cs.cursor(pymysql.cursors.DictCursor)
    sql = "update balance_user set balance="+str(amount)+" where univ_id='"+univ_id+"';"
    cs_cursor.execute(sql)
    cs.commit()

def center_hav():
    stock_type=["ahristock","stocka"]
    type_dict={"ahristock":"아리아리","stocka":"주식1"}
    return_dict={}
    for i in stock_type:
        stock = pymysql.connect(host="172.30.0.139",user="ahri",passwd="@dkfldkfl2021@", db="center")
        stock_cursor = stock.cursor(pymysql.cursors.DictCursor)
        sql = "select * from "+str(i)+";"
        stock_cursor.execute(sql)
        res = stock_cursor.fetchall()
        return_dict[type_dict[i]] = res[0]["center_have"]
    return return_dict

def change_center(type, amount):
    ch = pymysql.connect(host="172.30.0.139",user="ahri",passwd="@dkfldkfl2021@",db="center")
    ch_cursor = ch.cursor(pymysql.cursors.DictCursor)
    sql = "update "+str(type)+" set center_have="+str(amount)+";"
    ch_cursor.execute(sql)
    ch.commit()

def already_used_univ(univ_id):
    auu = pymysql.connect(host="172.30.0.139",user="ahri",passwd="@dkfldkfl2021@",db="les_kakao")
    auu_cursor = auu.cursor(pymysql.cursors.DictCursor)
    sql = "select * from is_les;"
    auu_cursor.execute(sql)
    auu_res = auu_cursor.fetchall()
    for i in auu_res:
        if i["univ_id"] == univ_id:
            return True
    return False

def sys_used(univ_id):
    su = pymysql.connect(host="172.30.0.139",user="ahri",passwd="@dkfldkfl2021@",db="ahri_system")
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

def add_tick_buy(type, amount):
    tick_buy = pymysql.connect(host="172.30.0.139",user="ahri",passwd="@dkfldkfl2021@",db="tick_buy")
    tick_buy_cursor = tick_buy.cursor(pymysql.cursors.DictCursor)
    sql="select * from "+str(type)+";"
    tick_buy_cursor.execute(sql)
    now_buy = int(tick_buy_cursor.fetchall()[0]["amount"])
    sql = "update "+str(type)+" set amount="+str(amount+now_buy)+";"
    tick_buy_cursor.execute(sql)
    tick_buy.commit()

def add_tick_sell(type, amount):
    tick_sell = pymysql.connect(host="172.30.0.139",user="ahri",passwd="@dkfldkfl2021@",db="tick_sell")
    tick_sell_cursor = tick_sell.cursor(pymysql.cursors.DictCursor)
    sql="select * from "+str(type)+";"
    tick_sell_cursor.execute(sql)
    now_sell = int(tick_sell_cursor.fetchall()[0]["amount"])
    sql = "update "+str(type)+" set amount="+str(amount+now_sell)+";"
    tick_sell_cursor.execute(sql)
    tick_sell.commit()

def new_balance_ahri():
    stock_type=["ahristock","stocka"]
    buy = pymysql.connect(host="172.30.0.139",user="ahri",passwd="@dkfldkfl2021@",db="tick_buy")
    buy_cursor = buy.cursor(pymysql.cursors.DictCursor)
    sell = pymysql.connect(host="172.30.0.139",user="ahri",passwd="@dkfldkfl2021@",db="tick_sell")
    sell_cursor = sell.cursor(pymysql.cursors.DictCursor)

    tot_rjf = 0

    for i in stock_type:
        sql_buy = "select * from "+str(i)+";"
        buy_cursor.execute(sql_buy)
        tick_buy = int(buy_cursor.fetchall()[0]["amount"])
        sql_sell = "select * from "+str(i)+";"
        sell_cursor.execute(sql_sell)
        tick_sell = int(sell_cursor.fetchall()[0]["amount"])

        if tick_buy > tick_sell:
            tot_rjf += tick_sell
        if tick_buy <= tick_sell:
            tot_rjf += tick_buy

    for i in stock_type:
        sql_buy = "select * from "+str(i)+";"
        buy_cursor.execute(sql_buy)
        tick_buy = int(buy_cursor.fetchall()[0]["amount"])
        sql_sell = "select * from "+str(i)+";"
        sell_cursor.execute(sql_sell)
        tick_sell = int(sell_cursor.fetchall()[0]["amount"])

        sto_bal = pymysql.connect(host="172.30.0.139",user="ahri",passwd="@dkfldkfl2021@",db="ahriweb")
        sto_bal_cursor = sto_bal.cursor(pymysql.cursors.DictCursor)
        sql="select * from "+str(i)+";"
        sto_bal_cursor.execute(sql)
        res = sto_bal_cursor.fetchall()
        n = len(res)
        now_stock = res[n-1]["stock"]

        print(tick_sell, tick_buy, tot_rjf)

        changed_bal = (((tick_sell-tick_buy)/tot_rjf)*0.6+1)*now_stock

        if changed_bal<0:
            changed_bal = 0

        print(changed_bal)
        sql = "insert into "+str(i)+" (num,stock) values ("+str(n+1)+","+str(changed_bal)+");"
        sto_bal_cursor.execute(sql)
        sto_bal.commit()

def clear_tick():
    tick_buy = pymysql.connect(host="172.30.0.139",user="ahri",passwd="@dkfldkfl2021@",db="tick_buy")
    tick_buy_cursor = tick_buy.cursor(pymysql.cursors.DictCursor)
    tick_sell = pymysql.connect(host="172.30.0.139",user="ahri",passwd="@dkfldkfl2021@",db="tick_sell")
    tick_sell_cursor = tick_sell.cursor(pymysql.cursors.DictCursor)
    stock_type=["ahristock","stocka"]
    for i in stock_type:
        sql="update "+str(i)+" set amount=1;"
        tick_buy_cursor.execute(sql)
        tick_buy.commit()
        tick_sell_cursor.execute(sql)
        tick_sell.commit()

def chart_set():
    ahriweb = pymysql.connect(host="172.30.0.139",user="ahri",passwd="@dkfldkfl2021@",db="ahriweb")
    ahriweb_cursor = ahriweb.cursor(pymysql.cursors.DictCursor)
    excel = Dispatch("Excel.Application")

    excel_file = excel.Workbooks.Open("C:\\Users\\KSA\Documents\\ahriweb\\server\\chatbot\\ahristock.xlsx")
    excel_ws = excel_file.Worksheets("Sheet1")

    sql="select*from ahristock;"
    ahriweb_cursor.execute(sql)
    stock_li = ahriweb_cursor.fetchall()

    for i in range(len(stock_li)):
        excel_ws.Cells(i+1,1).Value = str(stock_li[i]["stock"])

    excel_file.Save()

    chart = excel_ws.ChartObjects(1)
    chart.Chart.Export(Filename="C:\\Users\\KSA\\Documents\\ahriweb\\server\\chatbot\\static\\res.jpg")

    excel.quit()
