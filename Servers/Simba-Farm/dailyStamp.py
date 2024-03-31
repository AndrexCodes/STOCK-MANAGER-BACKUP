import mysql.connector as db
from datetime import datetime

conn = db.connect(user="Andrew", host="127.0.0.1", password="andrew", database="businessmanager")

cursor = conn.cursor()

def GetTimeStamp():
    date = str(datetime.now()).split(" ")[0]
    sql_query = """select * from daily_hosts where datetime = %s"""
    cursor.execute(sql_query, [date])
    sql_response = cursor.fetchall()
    print(sql_response)
    for x in sql_response:
        sql_query = """insert into daily_sales (business_id, unit_business_id, product_id, product_name, total_assets, no_items, datetime)
                    values(%s, %s, %s, %s, %s, %s, %s)"""
        sql_data = [x[0], x[1], x[2], x[3], x[4], x[5], str(datetime.now()).split(" ")[0]]
        cursor.execute(sql_query, sql_data)
        
        sql_query = """delete from daily_hosts"""
        cursor.execute(sql_query)
    conn.commit()


