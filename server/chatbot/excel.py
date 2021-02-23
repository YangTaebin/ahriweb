from win32com.client import Dispatch
import pymysql

ahriweb = pymysql.connect(host="172.30.2.209",user="ahri",passwd="taebin0408!",db="ahriweb")
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
