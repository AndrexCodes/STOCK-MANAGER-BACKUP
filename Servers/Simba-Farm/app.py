from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from flask_socketio import SocketIO, emit
import mysql.connector as db
from passlib.hash import sha256_crypt
from datetime import datetime
from genQCodes import genCode
from dailyStamp import GetTimeStamp
import schedule
import threading
import os
import time
import random
import mysql.connector as db
import os
import json
import time

app = Flask(__name__)
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")

img_url = "uploads"
app.config["Upload_Url"] = img_url

files_url = "files"
app.config["Files_Url"] = files_url

# db_url = "postgres://businessmanager_ilqy_user:HkLLO57KcImibkqlmIOj7sYSsrM6Jkxa@dpg-cm5sluen7f5s73e7smag-a.oregon-postgres.render.com/businessmanager_ilqy"
# conn = db.connect(db_url)
# 1%^s*eXj?wZH
conn = db.connect(user="Andrew", host="127.0.0.1", password="andrew", database="businessmanager")
cursor = conn.cursor()

def createTables():
    sql_query = """create table if not exists users(
                business_id varchar(255),
                business_username varchar(255),
                phone varchar(255),
                email varchar(255),
                password varchar(255),
                activation varchar(255),
                state varchar(255),
                datetime varchar(255)
                )"""
    cursor.execute(sql_query)

    sql_query = """create table if not exists unit_business (
                business_id varchar(255),
                unit_business_id varchar(255),
                unit_name varchar(255),
                total_assets varchar(255),
                no_products varchar(255),
                no_employees varchar(255),
                activation varchar(255),
                dateetime varchar(255)
                )"""
    cursor.execute(sql_query)

    sql_query = """create table if not exists products (
                business_id varchar(255),
                unit_business_id varchar(255),
                product_id varchar(255),
                name varchar(255),
                price varchar(255),
                img varchar(255),
                total_assets varchar(255),
                sold varchar(255),
                rem varchar(255),
                datetime varchar(255)
                )"""
    cursor.execute(sql_query)

    sql_query = """create table if not exists employees (
                business_id varchar(255),
                unit_business_id varchar(255),
                employee_id varchar(255),
                name varchar(255),
                sales varchar(255),
                password varchar(255),
                activation varchar(255),
                datetime varchar(255)
                )"""
    cursor.execute(sql_query)

    sql_query = """create table if not exists daily_sales (
                    business_id varchar(255),
                    unit_business_id varchar(255),
                    product_id varchar(255), 
                    product_name varchar(255),
                    total_assets varchar(255),
                    no_items varchar(255),
                    datetime varchar(255)
                    )"""
    cursor.execute(sql_query)

    sql_query = """create table if not exists daily_hosts (
                    business_id varchar(255),
                    unit_business_id varchar(255),
                    product_id varchar(255), 
                    product_name varchar(255),
                    total_assets varchar(255),
                    no_items varchar(255),
                    datetime varchar(255)
                    )"""
    cursor.execute(sql_query)

    sql_query = """create table if not exists employee_sales (
                business_id varchar(255),
                unit_business_id varchar(255),
                employee_id varchar(255),
                product_id varchar(255),
                quantity varchar(255),
                total_cash varchar(255),
                datetime varchar(255)
                )"""
    cursor.execute(sql_query)

    sql_query = """create table if not exists mpesa_transactions (
                    business_id varchar(255),
                    unit_business_id varchar(255),
                    employee_id varchar(255),
                    MerchantRequestID varchar(255),
                    CheckoutRequestID varchar(255),
                    Recipt_no varchar(255),
                    phone_number varchar(255),
                    amount varchar(255),
                    State varchar(255),
                    datetime varchar(255)
                    )"""
    cursor.execute(sql_query)

    sql_query = """create table if not exists cloudfiles (
                    business_id varchar(255),
                    unit_business_id varchar(255),
                    file_key varchar(255),
                    file_name varchar(255),
                    file_type varchar(255),
                    file_size varchar(255),
                    datetime varchar(255)
                    )"""
    cursor.execute(sql_query)

    sql_query = """create table if not exists receipts (
                    business_id varchar(255),
                    unit_business_id varchar(255),
                    receipt_id varchar(255),
                    query varchar(5000),
                    state varchar(255),
                    datetime varchar(255)
                    )"""
    cursor.execute(sql_query)
    
    conn.commit()

def clearTables():
    tables = ["users", "unit_business", "products", "employees", "daily_sales", "daily_hosts", "employee_sales", "mpesa_transactions", "cloudfiles", "receipts"]
    for x in tables:
        sql_query = """delete from %s"""%(x)
        cursor.execute(sql_query)
        conn.commit()

def dropTables():
    tables = ["users", "unit_business", "products", "employees", "daily_sales", "daily_hosts", "employee_sales", "mpesa_transactions", "cloudfiles", "receipts"]
    for x in tables:
        sql_query = """drop table if exists %s"""%(x)
        cursor.execute(sql_query)
        conn.commit()

# dropTables()
# clearTables()
createTables()

def schedule_task():
    schedule.every().day.at("00:00").do(GetTimeStamp)
    while True:
        schedule.run_pending()
        time.sleep(1)

# schedule_task_thread = threading.Thread(target=schedule_task)
# schedule_task_thread.start()

@app.route("/", methods=["GET", "POST"])
def home():
    return "Successful .."

@app.route("/userLogin", methods=["GET", "POST"])
def login():
    request_data = request.get_json()
    username = request_data["username"]
    password = request_data["password"]
    sql_query = """select password, business_id, activation from users where business_username = %s"""
    cursor.execute(sql_query, [username])
    resultsMain = cursor.fetchall()
    if resultsMain:
        resultsMain = resultsMain[0]
        if resultsMain[2] == "False":
            return jsonify({
            "state": "False"
            })
        results = resultsMain[0]
        print(results)
        if sha256_crypt.verify(password, results):
            # sql_query = """update users set state = %s where business_username = %s and password = %s"""
            # cursor.execute(sql_query, ["online", username, results])
            # conn.commit()
            print("Suucess login")
            return jsonify({
                "state": "True",
                "user_id": resultsMain[1]
            })
    else:
        return jsonify({
            "state": "invalid"
        })
    return jsonify({
            "state": "invalid"
        })

@app.route("/addNewUnit", methods=["GET", "POST"])
def addNewUnit():
    request_data = request.get_json()
    print(request_data)
    user_id = request_data["user_id"]
    unit_name = request_data["unit_name"]
    sql_query = """select count(*) from users where business_id = %s and activation = %s"""
    cursor.execute(sql_query, [user_id, "True"])
    num = cursor.fetchone()[0]
    print(num)
    if num == 1:
        sql_query = """select count(*) from unit_business where business_id = %s"""
        cursor.execute(sql_query, [user_id])
        num = cursor.fetchone()[0]
        sql_query = """insert into unit_business (business_id, unit_business_id, unit_name, total_assets, no_products, no_employees, activation, dateetime)
                        values(%s, %s, %s, %s, %s, %s, %s, %s)"""
        cursor.execute(sql_query, [user_id, "UNIT_BIZ_%s"%(num+1), unit_name,"0", "0", "0", "True", str(datetime.now())])
        conn.commit()
        return jsonify({
            "state": "True"
        })

    return jsonify({
            "state": "False"
        })

@app.route("/deleteUnit", methods=["GET", "POST"])
def deleteBusiness():
    request_data = request.get_json()
    if request_data:
        user_id = request_data["user_id"]
        business_id = request_data["business_id"]
        sql_query = """delete from unit_business where business_id = %s and unit_business_id = %s"""
        cursor.execute(sql_query, [user_id, business_id])
        sql_query = """delete from employees where business_id = %s and unit_business_id = %s"""
        cursor.execute(sql_query, [user_id, business_id])

        sql_query = """select img from products where business_id = %s and unit_business_id = %s"""
        cursor.execute(sql_query, [user_id, business_id])
        product_imgs = cursor.fetchall()
        if product_imgs:
            for img in product_imgs:
                img = img[0]
                img = img.split("/")[5]
                file_path = os.path.join(app.config["Upload_Url"], img)
                if os.path.exists(file_path):
                    os.remove(file_path)
                    print(f"{file_path} has been deleted.")
                else:
                    print(f"The file {file_path} does not exist.")

        sql_query = """delete from products where business_id = %s and unit_business_id = %s"""
        cursor.execute(sql_query, [user_id, business_id])

        return jsonify({
            "state": True
        })

    return jsonify({
        "state": False
    })

@app.route("/getMassData", methods=["GET", "POST"])
def getMassData():
    sql_query = """select * from users"""
    cursor.execute(sql_query)
    sql_response = cursor.fetchall()
    return jsonify(sql_response)

@app.route("/getMassUnits", methods=["GET", "POST"])
def getMassUnits():
    request_data = request.get_json()
    print(request_data)
    if request_data["user_id"] == None:
        return jsonify({
            "state": "invalid",
            "data": []
        })
    else:
        sql_query = """select * from unit_business where business_id = %s"""
        cursor.execute(sql_query, [request_data["user_id"]])
        sql_response = cursor.fetchall()
        return jsonify({
                "state": "True",
                "data": sql_response
            })

@app.route("/getUnitProducts", methods=["GET", "POST"])
def getUnitProducts():
    request_data = request.get_json()
    user_id = request_data["user_id"]
    unit_id = request_data["unit_id"]
    sql_query = """select * from products where business_id = %s and unit_business_id = %s"""
    cursor.execute(sql_query, [user_id, unit_id])
    sql_response = cursor.fetchall()
    return jsonify(sql_response)

@app.route("/addUser", methods=["POST"])
def addUser():
    request_data = request.form
    username = request_data.get("username")
    phone = request_data.get("phone")
    email = request_data.get("email")
    pass_1 = request_data.get("password_1")
    pass_2 = request_data.get("password_2")
    print(username)
    if pass_1 == pass_2:
        sql_query = """select count(*) from users"""
        cursor.execute(sql_query)
        num = cursor.fetchone()[0]
        sql_query = """insert into users(business_id, business_username, phone, email, password, activation, state, datetime)
                        values(%s, %s, %s, %s, %s, %s, %s, %s)"""
        sql_data = ["USER_%s"%(num+1), username, phone, email, sha256_crypt.hash(pass_1), "False", "offline",str(datetime.now())]
        cursor.execute(sql_query, sql_data)
        conn.commit()
    else:
        pass
    return "Andrew"

@app.route("/addNewProduct", methods=["GET", "POST"])
def addNewProduct():
    request_data = request.form
    request_files = request.files
    print(request_data)
    filename = request_files["image"].filename
    user_id = request_data["user_id"]
    biz_id = request_data["biz_id"]
    name = request_data["name"]
    price = request_data["price"]
    quantity = request_data["quantity"]

    sql_query = """select count(*) from users where business_id = %s"""
    cursor.execute(sql_query, [user_id])
    num = cursor.fetchall()[0][0]
    print("-----"*20)
    print(num)
    if num == 1:
        product_code = "PRODUCT_%s"%(genCode(6))
        while True:
            sql_query = """select * from products where business_id = %s and unit_business_id = %s and product_id = %s"""
            cursor.execute(sql_query, [user_id, biz_id, product_code])
            valid_product = cursor.fetchall()
            if not valid_product:
                break
            else:
                product_code = "PRODUCT_%s"%(genCode(6))
        
        filename = "%s~~%s~~%s.%s"%(user_id, biz_id, product_code, filename.split('.')[-1])
        ## make secure file
        request_files["image"].save(os.path.join(app.config["Upload_Url"], filename))

        filename = "https://ionextechsolutions.com/businessmanager/images/%s"%(filename)
        sql_query = """insert into products (business_id, unit_business_id, product_id, name, price, img, total_assets, sold, rem, datetime)
                        values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
        sql_data = [user_id, biz_id, product_code, name, price, filename, str(int(price)*int(quantity)), "0", quantity, str(datetime.now()).split(" ")[0]]
        cursor.execute(sql_query, sql_data)
        conn.commit()

        sql_query = """select total_assets from unit_business where business_id = %s and unit_business_id = %s"""
        cursor.execute(sql_query, [user_id, biz_id])
        response = cursor.fetchall()
        print(response)
        if response:
            total_assets = int(response[0][0])
            total_assets = total_assets + (int(price)*int(quantity))

        sql_query = """update unit_business set total_assets = %s where business_id = %s and unit_business_id = %s"""
        cursor.execute(sql_query, [str(total_assets), user_id, biz_id])
        conn.commit()

        return jsonify({
            "state": "True"
        })
    else:
        return jsonify({
            "state": "False"
        })

@app.route("/deleteProduct", methods=["GET", "POST"])
def DeleteProduct():
    request_data = request.get_json()
    print(request_data)
    user_id = request_data["user_id"]
    biz_id = request_data["biz_id"]
    product_id = request_data["product_id"]
    sql_query = """select img from products where business_id = %s and unit_business_id = %s and product_id = %s"""
    cursor.execute(sql_query, [user_id, biz_id, product_id])
    img_response = cursor.fetchall()
    if img_response:
        img_response = img_response[0][0]
        img_response = img_response.split("/")[5]
        file_path = os.path.join(app.config["Upload_Url"], img_response)
        if os.path.exists(file_path):
            os.remove(file_path)
            print(f"{file_path} has been deleted.")
        else:
            print(f"The file {file_path} does not exist.")

        sql_query = "delete from products where business_id = %s and unit_business_id = %s and product_id = %s"
        cursor.execute(sql_query, [user_id, biz_id, product_id])
        conn.commit()
    return jsonify({
        "state": True
    })

@app.route("/controlUser", methods=["GET", "POST"])
def controlUser():
    state = request.get_json()["state"]
    print(state)
    if state == "False":
        sql_query = """update users set activation = %s where business_id = %s"""
        cursor.execute(sql_query, ["True", request.get_json()["user_id"]])
        conn.commit()
        return jsonify({
            "state": "True"
        })
    else:
        sql_query = """update users set activation = %s where business_id = %s"""
        cursor.execute(sql_query, ["False", request.get_json()["user_id"]])
        conn.commit()
        return jsonify({
            "state": "True"
        })

@app.route("/images/<image_url>")
def getImages(image_url):
    file_path = os.path.join(app.config["Upload_Url"], image_url)
    if os.path.exists(file_path):
        return send_file(os.path.join(app.config["Upload_Url"], image_url))
    else:
        return send_file(os.path.join(app.config["Upload_Url"], "error.jpg"))

@app.route("/files/<file_key>")
def getFile(file_key):
    sql_query = """select * from cloudfiles where file_key = %s"""
    cursor.execute(sql_query, [file_key])
    results = cursor.fetchall()
    if results:
        file_name = results[0][3]
        return send_file(os.path.join(app.config["Files_Url"], file_name))
    else:
        return "Not Found"

@app.route("/resetFileKey", methods=["GET", "POST"])
def resetFileKey():
    if request.get_json():
        request_data = request.get_json()
        old_file_key = request_data["file_key"]
        while True:
            new_file_key = genCode(50)
            sql_query = """select * from cloudfiles where file_key = %s"""
            cursor.execute(sql_query, [new_file_key])
            results = cursor.fetchall()
            if not results:
                break

        sql_query = """update cloudfiles set file_key = %s where file_key = %s"""
        cursor.execute(sql_query, [new_file_key, old_file_key])
        conn.commit()
        return jsonify({
            "state": True,
            "new_file_key": new_file_key
        })
    return "key"

@app.route("/updateProductData", methods=["GET", "POST"])
def updateProductData():
    request_data = request.form
    try:
        new_img = request.files["new_img"]
    except:
        new_img = None
    print(request_data)
    request_data = {
        "user_id": request_data.get("user_id"),
        "biz_id": request_data.get("biz_id"),
        "product_id": request_data.get("product_id"),
        "new_img": new_img,
        "new_name": request_data.get("new_name"),
        "new_price": request_data.get("new_price"),
        "new_quantity": request_data.get("new_quantity")
    }
    sql_query = """select total_assets, img from products where business_id = %s and unit_business_id = %s and product_id = %s"""
    cursor.execute(sql_query, [request_data["user_id"], request_data["biz_id"], request_data["product_id"]])
    product_assests_raw = cursor.fetchall()

    sql_query = """select total_assets from unit_business where business_id = %s and unit_business_id = %s"""
    cursor.execute(sql_query, [request_data["user_id"], request_data["biz_id"]])
    total_assets = cursor.fetchall()

    if total_assets and product_assests_raw:
        total_assets = int(total_assets[0][0]) # unit_business
        product_assests = int(product_assests_raw[0][0])# product assets
        new_update = (int(request_data["new_quantity"])*int(request_data["new_price"]))
        new_assets = total_assets - product_assests
        new_assets = new_assets + new_update
        
        sql_query = """update unit_business set total_assets = %s where business_id = %s and unit_business_id = %s"""
        cursor.execute(sql_query, [str(new_assets), request_data["user_id"], request_data["biz_id"]])

    if request_data["new_img"]:
        filename = product_assests_raw[0][1].split("/")[5]
        print(filename)
        file_path = os.path.join(app.config["Upload_Url"], filename)
        if os.path.exists(file_path):
            os.remove(file_path)
            print(f"{file_path} has been deleted.")
        else:
            print(f"The file {file_path} does not exist.")

        request.files["new_img"].save(file_path)
        print("img saved successfully ....")
    sql_query = """update products set name = %s, total_assets = %s, rem = %s, price = %s where business_id = %s and unit_business_id = %s and product_id = %s"""
    sql_data = [request_data["new_name"], str(int(request_data["new_quantity"])*int(request_data["new_price"])), request_data["new_quantity"], request_data["new_price"], request_data["user_id"], request_data["biz_id"], request_data["product_id"]]
    cursor.execute(sql_query, sql_data)

    conn.commit()
    return jsonify({
        "state": "True"
    })

@app.route("/addNewUser", methods=["GET", "POST"])
def addNewUser():
    request_data = request.get_json()
    print(request_data)
    sql_query = """select * from employees where name = %s"""
    cursor.execute(sql_query, [request_data["username"]])
    presence = cursor.fetchall()
    if not presence:
        sql_query = """insert into employees (business_id, unit_business_id, employee_id, name, sales, password, activation, datetime)
                        values(%s, %s, %s, %s, %s, %s, %s, %s)"""
        sql_data = [request_data["user_id"], request_data["biz_id"], "EMPLOYEE_%s"%(random.randint(0, 9999999999999999999999)),request_data["username"], "0", sha256_crypt.hash(request_data["password"]), "True", str(datetime.now())]
        cursor.execute(sql_query, sql_data)

        sql_query = """select no_employees from unit_business where business_id = %s and unit_business_id = %s"""
        cursor.execute(sql_query, [request_data["user_id"], request_data["biz_id"]])
        num = cursor.fetchone()[0]
        num = int(num) + 1

        sql_query = """update unit_business set no_employees = %s where business_id = %s and unit_business_id = %s"""
        cursor.execute(sql_query, [str(num), request_data["user_id"], request_data["biz_id"]])
        conn.commit()
        
        return jsonify({
            "state": "True"
        })
    else:
        return jsonify({
            "state": "False"
        })

@app.route("/userLoginEmployee", methods=["GET", "POST"])
def userLoginEmployee():
    request_data = request.get_json()
    print(request_data)
    sql_query = """select password, employee_id, business_id, unit_business_id from employees where name = %s"""
    cursor.execute(sql_query, [request_data["username"]])
    password = cursor.fetchone()
    if password:
        password_1 = password[0]
        print(password_1)
        if sha256_crypt.verify(request_data["password"], password_1):
            sql_query = """select * from products where business_id = %s and unit_business_id = %s"""
            cursor.execute(sql_query, [password[2], password[3]])
            data = cursor.fetchall()

            sql_query = """select activation from users where business_id = %s"""
            cursor.execute(sql_query, [password[2]])
            activation = cursor.fetchone()[0]
            if activation == "False":
                return jsonify({
                        "state": "False"
                    })
            else:
                return jsonify({
                "state": "True",
                "user_id": password[1],
                "business_id":password[2],
                "unit_business_id": password[3],
                "products": data
            })

    return jsonify({
        "state": "invalid"
    })

@app.route("/ProcessSales", methods=["GET", "POST"])
def processing():
    # {'business_id': 'USER_1', 'unit_business_id': 'UNIT_BIZ_5', 'product_id': 'PRODUCT_1', 'employee_id': 'EMPLOYEE_9792750894674475300272', 'quantity': 10}
    if request.get_json():
        request_data = request.get_json()
        print(request_data)
        business_id = request_data["business_id"]
        unit_business_id = request_data["unit_business_id"]
        product_id = request_data["product_id"]
        employee_id = request_data["employee_id"]
        quantity = request_data["quantity"]
        sql_query = """select count(*) from employees where business_id = %s and unit_business_id = %s and employee_id = %s"""
        cursor.execute(sql_query,[business_id, unit_business_id, employee_id])
        num = cursor.fetchone()[0]
        if num == 1:
            sql_query = """select * from products where business_id = %s and unit_business_id = %s and product_id = %s"""
            cursor.execute(sql_query, [business_id, unit_business_id, product_id])
            sql_response = cursor.fetchall()
            print(sql_response)
            if len(sql_response) == 1:
                sold_items = int(sql_response[0][7]) + int(quantity)
                rem_items = int(sql_response[0][8]) - int(quantity)
                if rem_items < 0:
                    return jsonify({
                        "state": "insufficient"
                    })
                min_total = int(quantity) * int(sql_response[0][4])
                total_assets = int(sql_response[0][6]) + int(min_total)
                print("sold_items === %s"%(sold_items))
                print("rem_items === %s"%(rem_items))
                print("min_total === %s"%(min_total))
                print("total_assets === %s"%(total_assets))
                sql_query = """update products set datetime = %s, total_assets = %s, sold = %s, rem = %s where business_id = %s and unit_business_id = %s and product_id = %s"""
                cursor.execute(sql_query, [str(datetime.now()).split(" ")[0],str(total_assets), str(sold_items), str(rem_items), business_id, unit_business_id, product_id])
                conn.commit()

                # Compromise calcualtion of assets in unit_business and in business
                sql_query = """select total_assets from unit_business where business_id = %s and unit_business_id = %s"""
                cursor.execute(sql_query, [business_id, unit_business_id])
                unit_assets = cursor.fetchone()[0]
                unit_assets = int(unit_assets) + min_total

                sql_query = """update unit_business set total_assets = %s where business_id = %s and unit_business_id = %s"""
                cursor.execute(sql_query, [str(unit_assets), business_id, unit_business_id])
                conn.commit()

                sql_query = """select * from daily_hosts where business_id = %s and unit_business_id = %s and product_id = %s"""
                cursor.execute(sql_query, [business_id, unit_business_id, product_id])
                data = cursor.fetchall()
                if data:
                    total_assets_2 = int(data[0][4]) + (int(quantity) * int(sql_response[0][4]))
                    quantity_2 = int(data[0][5]) + int(quantity)
                    sql_query = """update daily_hosts set total_assets = %s, no_items = %s, datetime = %s where business_id = %s and unit_business_id = %s and product_id = %s"""
                    cursor.execute(sql_query, [str(total_assets_2), str(quantity_2), str(datetime.now()).split(" ")[0], business_id, unit_business_id, product_id])
                    conn.commit()
                else:
                    total_assets_2 = int(quantity) * int(sql_response[0][4])
                    quantity_2 = quantity
                    sql_query = """insert into daily_hosts (business_id, unit_business_id, product_id, product_name, total_assets, no_items, datetime)
                                    values(%s, %s, %s, %s, %s, %s, %s)"""
                    cursor.execute(sql_query, [business_id, unit_business_id, product_id, sql_response[0][3], str(total_assets_2), str(quantity_2), str(datetime.now()).split(" ")[0]])
                    conn.commit()

                sql_query = """insert into employee_sales (business_id, unit_business_id, employee_id, product_id, quantity, total_cash, datetime)
                                values(%s, %s, %s, %s, %s, %s, %s)"""
                cursor.execute(sql_query, [business_id, unit_business_id, employee_id, product_id, str(quantity), str(min_total), str(datetime.now())])
                conn.commit()

                sql_query = """select * from receipts where state = %s"""
                cursor.execute(sql_query, ["Pending"])
                results = cursor.fetchone()

                if results:
                    business_id = request_data["business_id"]
                    unit_business_id = request_data["unit_business_id"]
                    receipt_id = results[2]
                    query = json.loads(results[3])
                    current_query = {
                        "product_id": request_data["product_id"],
                        "product_name": sql_response[0][3],
                        "product_quantity": request_data["quantity"],
                        "product_cost": int(sql_response[0][4])*int(request_data["quantity"])
                    }
                    query.append(current_query)
                    state = "Pending"
                    selltime = str(datetime.now())

                    sql_query = """update receipts set query = %s where business_id = %s and unit_business_id = %s and receipt_id = %s"""
                    cursor.execute(sql_query, [json.dumps(query), business_id, unit_business_id, receipt_id])
                    conn.commit()
                else:
                    business_id = request_data["business_id"]
                    unit_business_id = request_data["unit_business_id"]
                    receipt_id = genCode(50)
                    query = [
                        {
                            "product_id": request_data["product_id"],
                            "product_name": sql_response[0][3],
                            "product_quantity": request_data["quantity"],
                            "product_cost": int(sql_response[0][4])*int(request_data["quantity"])
                        }
                    ]
                    state = "Pending"
                    selltime = str(datetime.now())

                    sql_query = """insert into receipts (business_id, unit_business_id, receipt_id, query, state, datetime)
                                    values(%s, %s, %s, %s, %s, %s)"""
                    cursor.execute(sql_query, [business_id, unit_business_id, receipt_id, json.dumps(query), state, selltime])
                    conn.commit()
                
                return jsonify({
                    "state": "True"
                })
    return jsonify({
                    "state": "False"
                })

@app.route("/getProductLogs", methods=["GET", "POST"])
def getLogs():
    if request.get_json():
        request_data = request.get_json()
        print(request_data)
        sql_query = """select * from daily_sales where business_id = %s and unit_business_id = %s and product_id = %s"""
        cursor.execute(sql_query, [request_data["business_id"], request_data["unit_business_id"], request_data["product_id"]])
        sql_response = cursor.fetchall()
        return jsonify(sql_response)

    return "p"

@app.route("/totalCashOut", methods=["GET", "POST"])
def totalCashOut():
    if request.get_json():
        request_data = request.get_json()
        print(request_data)
        business_id = request_data["user_id"]
        unit_business_id = request_data["unit_business_id"]
        sql_query = """update products set total_assets = %s, sold = %s where business_id = %s and unit_business_id = %s"""
        cursor.execute(sql_query, ["0", "0", business_id, unit_business_id])
        sql_query = """update unit_business set total_assets = %s where business_id = %s and unit_business_id = %s"""
        cursor.execute(sql_query, ["0", business_id, unit_business_id])
        conn.commit()
        return jsonify({
            "state": "True"
        })
    return "p"

@app.route("/addNewFile", methods=["GET", "POST"])
def addNewFile():
    print(request.form)
    if request.form and request.files:
        request_data = request.form
        business_id = request_data.get("business_id")
        unit_business_id = request_data.get("unit_business_id")
        file_name = request_data.get("file_name")
        doc_file = request.files["doc_file"]
        sql_query = """select * from users where business_id = %s and activation = %s"""
        cursor.execute(sql_query, [business_id, "True"])
        results = cursor.fetchone()
        if results:
            file_path = os.path.join(app.config["Files_Url"], "%s.%s"%(file_name, str(doc_file.filename).split(".")[-1]))
            doc_file.save(file_path)
            file_size = os.path.getsize(file_path)

            while True:
                file_key = genCode(50)
                sql_query = """select * from cloudfiles where file_key = %s"""
                cursor.execute(sql_query, [file_key])
                results = cursor.fetchall()
                if not results:
                    break

            file_name = "%s.%s"%(file_name, str(doc_file.filename).split(".")[-1])

            sql_query = """insert into cloudfiles (business_id, unit_business_id, file_key, file_name, file_type, file_size, datetime)
                            values(%s, %s, %s, %s, %s, %s, %s)"""
            cursor.execute(sql_query, [business_id, unit_business_id, file_key, file_name, str(doc_file.content_type), str(file_size), str(datetime.now())])
            conn.commit()
            
            return jsonify({
                "state": "True"
            })
        else:
            return jsonify({
                "state": "invalid"
            })
    return "p"

@app.route("/getFiles", methods=["GET", "POST"])
def getFiles():
    if request.get_json():
        request_data = request.get_json()
        business_id = request_data["business_id"]
        unit_business_id = request_data["unit_business_id"]
        sql_query = """select * from users where business_id = %s"""
        cursor.execute(sql_query, [business_id])
        results = cursor.fetchall()
        print(results)
        if results:
            sql_query = """select * from cloudfiles where business_id = %s and unit_business_id = %s"""
            cursor.execute(sql_query, [business_id, unit_business_id])
            response = cursor.fetchall()
            return jsonify({
                "state": "True",
                "data": response
            })
        else:
            return jsonify({
                "state": "False"
            })
    return "p"

@app.route("/getEmployees", methods=["GET", "POST"])
def getEmployees():
    request_data = request.get_json()
    if request_data:
        user_id = request_data["business_id"]
        biz_id = request_data["unit_business_id"]
        sql_query = """select * from employees where business_id = %s and unit_business_id = %s"""
        cursor.execute(sql_query, (user_id, biz_id))
        response = cursor.fetchall()
        return jsonify({
        "state": True,
        "data": response
    })
    print(request_data)
    return jsonify({
        "state": False
    })

@app.route("/updateEmployee",  methods=["GET", "POST"])
def update_employee():
    request_data = request.get_json()
    print(request_data)
    if request_data:
        state = request_data["state"]
        user_id = request_data["user_id"]
        biz_id = request_data["biz_id"]
        employee_id = request_data["employee_id"]
        try:
            name = request_data["employee_name"]
            password = request_data["employee_pass"]
        except:
            print("failed to get details")
        if state:
            if password:
                sql_query = """update employees set name = %s, password = %s where business_id = %s and unit_business_id = %s and employee_id = %s"""
                sql_data = [name, sha256_crypt.hash(password), user_id, biz_id, employee_id]
                cursor.execute(sql_query, sql_data)
                conn.commit()
                return jsonify({
                    "state": True
                })
            else:
                sql_query = """update employees set name = %swhere business_id = %s and unit_business_id = %s and employee_id = %s"""
                sql_data = [name, user_id, biz_id, employee_id]
                cursor.execute(sql_query, sql_data)
                conn.commit()
                return jsonify({
                    "state": True
                })
        else:
            sql_query = """delete from employees where business_id = %s and unit_business_id = %s and employee_id = %s"""
            cursor.execute(sql_query, [user_id, biz_id, employee_id])
            conn.commit()
            return jsonify({
                "state": True
            })
    return jsonify({
        "state": False
    })

@app.route("/activateReceipt", methods=["GET", "POST"])
def activateReceipt():
    if request.get_json():
        request_data = request.get_json()
        business_id = request_data["business_id"]
        unit_business_id = request_data["unit_business_id"]
        employee_id = request_data["employee_id"]

        sql_query = """select * from employees where business_id = %s and unit_business_id = %s and employee_id = %s"""
        cursor.execute(sql_query, [business_id, unit_business_id, employee_id])
        results = cursor.fetchone()
        print(results)
        if results:
            sql_query = """update receipts set state = %s where business_id = %s and unit_business_id = %s and state = %s"""
            cursor.execute(sql_query, ["False", business_id, unit_business_id, "Pending"])
            conn.commit()
            return jsonify({
                "state": True
            })
        else:
            return jsonify({
                "state": False
            })

    return "p"

@app.route("/getReceipt", methods=["GET", "POST"])
def getReceipt():
    if request.get_json():
        request_data = request.get_json()
        business_id = request_data["business_id"]
        unit_business_id = request_data["unit_business_id"]
        print(request_data)

        sql_query = """select * from receipts where business_id = %s and unit_business_id = %s and state = %s"""
        cursor.execute(sql_query, [business_id, unit_business_id, "False"])
        # cursor.execute(sql_query, [business_id, unit_business_id, "False"])

        response = cursor.fetchall()
        print(response)
        if response:
            response = response[0]
            sql_query = """update receipts set state = %s where business_id = %s and unit_business_id = %s and receipt_id = %s"""
            cursor.execute(sql_query, ["True", response[0], response[1], response[2]])
            conn.commit()
            print(response)
            return jsonify({
                "state": True,
                "data": response
            })
        else:
            return jsonify({
                "state": False
            })
    return jsonify({
                "state": False
            })

# connected_devices = []

# def SendPrintingReports():
#     while len(connected_devices) > 0:
#         time.sleep(4)
#         for x in connected_devices:
#             client_sid = x["sid"]
#             business_id = x["business_id"]
#             unit_business_id = x["unit_business_id"]
#             sql_query = """select * from receipts where business_id = %s and unit_business_id = %s and state = %s"""
#             cursor.execute(sql_query, [business_id, unit_business_id, "False"])
#             response = cursor.fetchall()
#             print("------------ RESPONSE FROM PRINTING ------------")
#             print(response)
#             if response:
#                 response = response[0]
#                 sql_query = """update receipts set state = %s where business_id = %s and unit_business_id = %s and receipt_id = %s"""
#                 cursor.execute(sql_query, ["True", response[0], response[1], response[2]])
#                 conn.commit()
#                 response = {
#                     "message": json.dumps(response)
#                 }
#                 socketio.emit("message", response, room=client_sid)

# @socketio.on("connect")
# def ClientConnection():
#     print("Connected device .....")
#     business_id = request.args.get("business_id")
#     unit_business_id = request.args.get("unit_business_id")
#     if business_id and unit_business_id:
#         unit_connection = {
#             "sid": request.sid,
#             "business_id": business_id,
#             "unit_business_id": unit_business_id
#         }
#         connected_devices.append(unit_connection)
#     if len(connected_devices) == 1:
#         x = threading.Thread(target=SendPrintingReports)
#         x.start()
#     # data = {
#     #     "message": "Hello Andrew"
#     # }
#     # socketio.emit("message", data, room=request.sid)

# @socketio.on("disconnect")
# def ClientDisconnection():
#     print("Client disconnected .........")
#     for x in range(len(connected_devices)):
#         if connected_devices[x]["sid"] == request.sid:
#             connected_devices.pop(x)

if __name__ == "__main__":
    app.run(debug=True)
    # socketio.run(app, port=5000, debug=True)
