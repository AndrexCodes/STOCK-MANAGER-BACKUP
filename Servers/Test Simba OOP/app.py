from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from flask_socketio import SocketIO, emit
import mysql.connector as db
from datetime import datetime
import threading
import os
import time
import os
import json

import models as models

app = Flask(__name__)
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")

img_url = "uploads"
app.config["Upload_Url"] = img_url

files_url = "files"
app.config["Files_Url"] = files_url

secret = "Not Set"
app.config["Secret"] = secret

# db_url = "postgres://businessmanager_ilqy_user:HkLLO57KcImibkqlmIOj7sYSsrM6Jkxa@dpg-cm5sluen7f5s73e7smag-a.oregon-postgres.render.com/businessmanager_ilqy"
# conn = db.connect(db_url)
# 1%^s*eXj?wZH
conn = db.connect(user="Andrew", host="127.0.0.1", password="andrew", database="businessmanager", autocommit= True)
cursor = conn.cursor()


@app.route("/", methods=["GET", "POST"])
def home():
    # Return a classic html page include software packages and mobile application
    return "Successful ......"

@app.route("/userLogin", methods=["POST"])
def login():
    request_data = request.get_json()
    username = request_data["username"]
    password = request_data["password"]
    user = models.UserAccount(business_username=username, password=password)
    if not user.AuthUser(): return jsonify({"state": "invalid"})
    if not user.is_valid(): return jsonify({"state": "invalid"})
    return jsonify({
        "state": "True",
        "user_id": user.business_id
    })

@app.route("/addNewUnit", methods=["GET", "POST"])
def addNewUnit():
    request_data = request.get_json()
    # print(request_data)
    user_id = request_data["user_id"]
    unit_name = request_data["unit_name"]
    business = models.Business(business_id=user_id, name=unit_name)
    userAccount = models.UserAccount(business_id=user_id)
    if not userAccount.is_valid(): return jsonify({"state": "False"})
    if not business.CreateBusiness(): return jsonify({"state": "False"})
    return jsonify({
            "state": "True"
        })

@app.route("/deleteUnit", methods=["GET", "POST"])
def deleteBusiness():
    request_data = request.get_json()
    if request_data:
        user_id = request_data["user_id"]
        business_id = request_data["business_id"]
        
        business = models.Business(business_id=user_id, unit_business_id=business_id)
        if not business.DeleteBusiness(): return jsonify({"state": False})

        employees = models.Employee(business_id=user_id, unit_business_id=business_id)
        if not employees.DeleteEmployee(): return jsonify({"state": False})

        products = models.Product(business_id=user_id, unit_business_id=business_id)
        if not products.DeleteProduct(): return jsonify({"state": False})

        return jsonify({
            "state": True
        })

    return jsonify({
        "state": False
    })

# This route is for administrative purpose
@app.route("/getMassData", methods=["GET", "POST"])
def getMassData():
    secret = "Not Set"
    if app.config["Secret"] == secret:
        users = models.UserAccount()
        return jsonify(users.GetUsers())
    else:
        return jsonify([])
    
@app.route("/getMassUnits", methods=["GET", "POST"])
def getMassUnits():
    request_data = request.get_json()
    user_id = request_data["user_id"]
    userAccounts = models.UserAccount(business_id=user_id)
    if not userAccounts.is_valid(): return jsonify({"state": "invalid","data": []})
    businesses = models.Business(business_id=user_id)
    unit_businesses = businesses.GetBusiness()
    if not unit_businesses: return jsonify({"state": "invalid","data": []})
    return jsonify({
        "state": "True",
        "data": unit_businesses
    })

@app.route("/getUnitProducts", methods=["GET", "POST"])
def getUnitProducts():
    request_data = request.get_json()
    user_id = request_data["user_id"]
    unit_id = request_data["unit_id"]
    userAccount = models.UserAccount(business_id=user_id)
    if not userAccount.is_valid(): return jsonify([])
    products = models.Product(business_id=user_id, unit_business_id=unit_id)
    return jsonify(products.GetProducts())

# This route is for administrative use
@app.route("/addUser", methods=["POST"])
def addUser():
    request_data = request.form
    username = request_data.get("username")
    phone = request_data.get("phone")
    email = request_data.get("email")
    pass_1 = request_data.get("password_1")
    pass_2 = request_data.get("password_2")
    if pass_1 == pass_2:
        new_user = models.UserAccount(business_username=username, email=email, phone=phone, password=pass_1)
        if not new_user.CreateUser(): return jsonify({"state": "Failed"})
        return jsonify({
            "state": "Success",
        })
    return jsonify({"state": "Failed"})

@app.route("/addNewProduct", methods=["GET", "POST"])
def addNewProduct():
    request_data = request.form
    request_files = request.files

    filename = request_files["image"].filename
    user_id = request_data["user_id"]
    biz_id = request_data["biz_id"]
    name = request_data["name"]
    price = request_data["price"]
    quantity = request_data["quantity"]

    userAccount = models.UserAccount(business_id=user_id)
    if not userAccount.is_valid(): return jsonify({"state": "False"})

    business = models.Business(business_id=user_id, unit_business_id=biz_id)
    if not business.is_valid(): return jsonify({"state": "False"})

    product = models.Product(business_id=user_id, unit_business_id=biz_id, name=name, price=price, quantity=quantity, img=request_files["image"],img_extension=filename.split(".")[-1])
    if not product.CreateProduct(): return jsonify({"state": "False"})

    return jsonify({
        "state": "True"
    })

@app.route("/deleteProduct", methods=["GET", "POST"])
def DeleteProduct():
    request_data = request.get_json()
    # print(request_data)
    user_id = request_data["user_id"]
    biz_id = request_data["biz_id"]
    product_id = request_data["product_id"]
    
    userAccounts = models.UserAccount(business_id=user_id)
    if not userAccounts.is_valid(): return jsonify({"state": True})

    product = models.Product(business_id=user_id, unit_business_id=biz_id, product_id=product_id)
    if not product.DeleteProduct(): return jsonify({"state": True})

    return jsonify({
        "state": True
    })

@app.route("/controlUser", methods=["GET", "POST"])
def controlUser():
    request_data =  request.get_json()
    if request_data:
        user_id = request_data["user_id"]
        state = request_data["state"]

        userAccount = models.UserAccount(business_id=user_id)
        if not userAccount.ToggleAccountState(state=state): return jsonify({"state": "False"})

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
            new_file_key = models.Generals().GenCode(50)
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

    request_data = {
        "user_id": request_data.get("user_id"),
        "biz_id": request_data.get("biz_id"),
        "product_id": request_data.get("product_id"),
        "new_img": new_img,
        "new_name": request_data.get("new_name"),
        "new_price": request_data.get("new_price"),
        "new_quantity": request_data.get("new_quantity")
    }

    userAccount = models.UserAccount(business_id=request_data["user_id"])
    if not userAccount.is_valid(): return jsonify({"state": "False"})

    product = models.Product(business_id=request_data["user_id"], unit_business_id=request_data["biz_id"], product_id=request_data["product_id"], name=request_data["new_name"], price=request_data["new_price"], quantity=request_data["new_quantity"], img=request_data["new_img"])
    if not product.ModifyProductData(): return jsonify({"state": "False"})

    return jsonify({
        "state": "True"
    })

@app.route("/addNewUser", methods=["GET", "POST"])
def addNewUser():
    request_data = request.get_json()
    user_id = request_data["user_id"]
    biz_id = request_data["biz_id"]
    username = request_data["username"]
    password = request_data["password"]

    userAccount = models.UserAccount(business_id=request_data["user_id"])
    if not userAccount.is_valid(): return jsonify({"state": "False"})

    business = models.Business(business_id=user_id, unit_business_id=biz_id)
    if not business.is_valid(): return jsonify({"state": "False"})

    employee = models.Employee(business_id=user_id, unit_business_id=biz_id, name=username, password=password)
    if not employee.CreateEmployee(): return jsonify({"state": "False"})

    return jsonify({
        "state": "True"
    })

@app.route("/userLoginEmployee", methods=["GET", "POST"])
def userLoginEmployee():
    request_data = request.get_json()
    if not request_data: return jsonify({"state": "False"}) 
    username = request_data["username"]
    password = request_data["password"]
    employee = models.Employee(name=username, password=password)
    if not employee.AuthEmployee(): return jsonify({"state": "invalid"})

    userAccount = models.UserAccount(business_id=employee.business_id)
    if not userAccount.is_valid(): return jsonify({"state": "invalid"})

    product = models.Product(business_id=employee.business_id, unit_business_id=employee.unit_business_id)
    products = product.GetProducts()
    return jsonify({
        "state": "True",
        "user_id": employee.employee_id,
        "business_id":employee.business_id,
        "unit_business_id": employee.unit_business_id,
        "products": products
    })

@app.route("/ProcessSales", methods=["GET", "POST"])
def processing():
    # {'business_id': 'USER_1', 'unit_business_id': 'UNIT_BIZ_5', 'product_id': 'PRODUCT_1', 'employee_id': 'EMPLOYEE_9792750894674475300272', 'quantity': 10}
    request_data = request.get_json()
    if not request_data: return
    business_id = request_data["business_id"]
    unit_business_id = request_data["unit_business_id"]
    product_ids = request_data["product_id"]
    employee_id = request_data["employee_id"]
    quantitys = request_data["quantity"]

    userAccount = models.UserAccount(business_id=business_id)
    if not userAccount.is_valid(): return jsonify({"state": "False"})

    employee = models.Employee(business_id=business_id, unit_business_id=unit_business_id, employee_id=employee_id)
    if not employee.is_present(): return jsonify({"state": "False"})

    products = models.Product(business_id=business_id, unit_business_id=unit_business_id)
    main_response = products.MakesSale_2(product_ids=product_ids, quantitys=quantitys)

    return jsonify({
        "state": "True",
        "message": main_response
    })

# @app.route("/ProcessSales_2", methods=["GET", "POST"])
# def processing_2():
#     # {'business_id': 'USER_1', 'unit_business_id': 'UNIT_BIZ_5', 'product_id': 'PRODUCT_1', 'employee_id': 'EMPLOYEE_9792750894674475300272', 'quantity': 10}
#     if request.get_json():
#         request_data = request.get_json()
#         business_id = request_data["business_id"]
#         unit_business_id = request_data["unit_business_id"]
#         product_ids = request_data["product_id"]
#         employee_id = request_data["employee_id"]
#         quantitys = request_data["quantity"]
#         main_response = ""
#         sql_query = """select count(*) from employees where business_id = %s and unit_business_id = %s and employee_id = %s"""
#         cursor.execute(sql_query,[business_id, unit_business_id, employee_id])
#         num = cursor.fetchone()[0]
#         if num == 1:
#             sql_query = """select * from products where business_id = %s and unit_business_id = %s"""
#             cursor.execute(sql_query, [business_id, unit_business_id])
#             sql_response = cursor.fetchall()
#             for x in range(len(product_ids)):
#                 for y in sql_response:
#                     if not product_ids[x] == y[2]: continue
#                     sold_items = int(y[7]) + int(quantitys[x])
#                     rem_items = int(y[8]) - int(quantitys[x])
#                     if rem_items < 0: 
#                         main_response = main_response + f"Failed sales for product: {y[3]}\n"
#                         continue
#                     min_total = int(quantitys[x]) * int(y[4])
#                     total_assets = int(y[6]) + int(min_total)
            
#                     sql_query = """update products set datetime = %s, total_assets = %s, sold = %s, rem = %s where business_id = %s and unit_business_id = %s and product_id = %s"""
#                     cursor.execute(sql_query, [str(datetime.now()).split(" ")[0],str(total_assets), str(sold_items), str(rem_items), business_id, unit_business_id, product_ids[x]])
#                     conn.commit()

#                     sql_query = """insert into employee_sales (business_id, unit_business_id, employee_id, product_id, quantity, total_cash, datetime)
#                                 values(%s, %s, %s, %s, %s, %s, %s)"""
#                     cursor.execute(sql_query, [business_id, unit_business_id, employee_id, product_ids[x], str(quantitys[x]), str(min_total), str(datetime.now())])
#                     conn.commit()

#                     sql_query = """select * from receipts where state = %s"""
#                     cursor.execute(sql_query, ["Pending"])
#                     results = cursor.fetchone()

#                     if results:
#                         receipt_id = results[2]
#                         query = json.loads(results[3])
#                         current_query = {
#                             "product_id": product_ids[x],
#                             "product_name": y[3],
#                             "product_quantity": quantitys[x],
#                             "product_cost": int(y[4])*int(quantitys[x])
#                         }
#                         query.append(current_query)
#                         state = "Pending"
#                         selltime = str(datetime.now())

#                         sql_query = """update receipts set query = %s where business_id = %s and unit_business_id = %s and receipt_id = %s"""
#                         cursor.execute(sql_query, [json.dumps(query), business_id, unit_business_id, receipt_id])
#                         conn.commit()

#                     else:
#                         receipt_id = models.Generals().GenCode(15)
#                         query = [
#                             {
#                                 "product_id": product_ids[x],
#                                 "product_name": y[3],
#                                 "product_quantity": quantitys[x],
#                                 "product_cost": int(y[4])*int(quantitys[x])
#                             }
#                         ]
#                         state = "Pending"
#                         selltime = str(datetime.now())

#                         sql_query = """insert into receipts (business_id, unit_business_id, receipt_id, query, state, datetime)
#                                         values(%s, %s, %s, %s, %s, %s)"""
#                         cursor.execute(sql_query, [business_id, unit_business_id, receipt_id, json.dumps(query), state, selltime])
#                         conn.commit()
            
#             return jsonify({
#                 "state": "True",
#                 "message": main_response
#             })
            
#     return jsonify({
#                     "state": "False"
#                 })

@app.route("/ProcessSales_2", methods=["GET", "POST"])
def processing_2():
    # {'business_id': 'USER_1', 'unit_business_id': 'UNIT_BIZ_5', 'product_id': 'PRODUCT_1', 'employee_id': 'EMPLOYEE_9792750894674475300272', 'quantity': 10}
    if request.get_json():
        request_data = request.get_json()
        business_id = request_data["business_id"]
        unit_business_id = request_data["unit_business_id"]
        product_ids = request_data["product_id"]
        employee_id = request_data["employee_id"]
        quantitys = request_data["quantity"]
    
        product = models.Product(business_id=business_id, unit_business_id=unit_business_id)
        main_response = product.MakesSale_2(product_ids=product_ids, quantitys=quantitys, employee_id=employee_id)

        return jsonify({
            "state": "True",
            "message": main_response
        })

        
    return jsonify({
                    "state": "False",
                })

@app.route("/getProductLogs", methods=["GET", "POST"])
def getLogs():
    if request.get_json():
        request_data = request.get_json()
        # print(request_data)
        sql_query = """select * from daily_sales where business_id = %s and unit_business_id = %s and product_id = %s"""
        cursor.execute(sql_query, [request_data["business_id"], request_data["unit_business_id"], request_data["product_id"]])
        sql_response = cursor.fetchall()
        return jsonify(sql_response)

    return "p"

@app.route("/totalCashOut", methods=["GET", "POST"])
def totalCashOut():
    if request.get_json():
        request_data = request.get_json()
        # print(request_data)
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
    # print(request.form)
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
                file_key = models.Generals().GenCode(50)
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
        # print(results)
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
        employees = models.Employee(business_id=user_id, unit_business_id=biz_id)
        employees = employees.GetEmployees()
        if not employees: return jsonify({"state": True,"data": []})

        return jsonify({
            "state": True,
            "data": employees
        })

@app.route("/updateEmployee",  methods=["GET", "POST"])
def update_employee():
    request_data = request.get_json()
    # print(request_data)
    if request_data:
        state = request_data["state"]
        user_id = request_data["user_id"]
        biz_id = request_data["biz_id"]
        employee_id = request_data["employee_id"]
        try:
            name = request_data["employee_name"]
            password = request_data["employee_pass"]
        except:
            name = None
            password = None
        employee = models.Employee(business_id=user_id, unit_business_id=biz_id, employee_id=employee_id, name=name)
        if state:
            # Modify employee data
            if password:
                employee.password = password
            employee.ModifyEmployee()
            return jsonify({
                    "state": True
                })
        else:
            # Delete employee
            employee.DeleteEmployee()
            return jsonify({
                "state": True
            })

@app.route("/activateReceipt", methods=["GET", "POST"])
def activateReceipt():
    if request.get_json():
        request_data = request.get_json()
        business_id = request_data["business_id"]
        unit_business_id = request_data["unit_business_id"]
        employee_id = request_data["employee_id"]

        employee = models.Employee(business_id=business_id, unit_business_id=unit_business_id, employee_id=employee_id)
        if not employee.is_present(): return jsonify({"state": True})

        receipt = models.Receipt(business_id=business_id, unit_business_id=unit_business_id)
        receipt.ActivateReceipt()
        # print("Receipt Activated .....")
        return jsonify({
                "state": True
            })


# Depricted version of fetchin receipts from server
# @app.route("/getReceipt", methods=["GET", "POST"])
# def getReceipt():
#     request_data = request.get_json()
#     if request_data:
#         business_id = request_data["business_id"]
#         unit_business_id = request_data["unit_business_id"]
        
#         receipt = models.Receipt(business_id=business_id, unit_business_id=unit_business_id)
#         response = receipt.GetReceipt()
#         if not response: return jsonify({"state": False})

#         return jsonify({
#             "state": True,
#             "data": response
#         })


pool_conn = db.connect(user="Andrew", host="127.0.0.1", password="andrew", database="businessmanager", autocommit= True)
pool_cursor = pool_conn.cursor()
pool_cursor.execute("SET SESSION TRANSACTION ISOLATION LEVEL READ COMMITTED")
connected_devices = []

def SendPrintingReports():
    while len(connected_devices) > 0:
        time.sleep(2)
        for x in connected_devices:
            client_sid = x["sid"]
            business_id = x["business_id"]
            unit_business_id = x["unit_business_id"]
            sql_query = """select * from receipts where business_id = %s and unit_business_id = %s and state = %s"""
            pool_cursor.execute(sql_query, [business_id, unit_business_id, "False"])
            response = pool_cursor.fetchall()
            print("Checking for receipts .....")
            if response:
                print("------------ RESPONSE FROM PRINTING ------------")
                print(response)
                response = response[0]
                sql_query = """update receipts set state = %s where business_id = %s and unit_business_id = %s and receipt_id = %s"""
                cursor.execute(sql_query, ["True", response[0], response[1], response[2]])
                conn.commit()
                response = {
                    "message": json.dumps(response)
                }
                socketio.emit("message", response, room=client_sid)

@socketio.on("connect")
def ClientConnection():
    print("Connected device .....")
    business_id = request.args.get("business_id")
    unit_business_id = request.args.get("unit_business_id")
    if business_id and unit_business_id:
        unit_connection = {
            "sid": request.sid,
            "business_id": business_id,
            "unit_business_id": unit_business_id
        }
        connected_devices.append(unit_connection)
    if len(connected_devices) == 1:
        x = threading.Thread(target=SendPrintingReports)
        x.start()
    # data = {
    #     "message": "Hello Andrew"
    # }
    # socketio.emit("message", data, room=request.sid)

@socketio.on("disconnect")
def ClientDisconnection():
    print("Client disconnected .........")
    for x in range(len(connected_devices)):
        if connected_devices[x]["sid"] == request.sid:
            connected_devices.pop(x)

if __name__ == "__main__":
    # app.run(debug=True)
    socketio.run(app, port=5000, debug=True)
