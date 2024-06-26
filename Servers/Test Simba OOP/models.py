from passlib.hash import sha256_crypt
from datetime import datetime
from random import randint
import os
import json
import notifications

import mysql.connector as db
conn = db.connect(user="Andrew", host="127.0.0.1", password="andrew", database="businessmanager")
cursor = conn.cursor()

sql_query = ""
sql_data = ""
images_path_folder = "uploads"
code_choice = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUWXYZ1234567890"

class Generals:
    def GenCode(self, size):
        code = ""
        for _ in range(size):
            code += code_choice[randint(0, len(code_choice)-1)]
        return code

class UserAccount(Generals):
    def __init__(self, business_id = None, business_username = None, phone = None, email = None, password = None, activation = False, state = False):
        self.business_id = business_id
        self.business_username = business_username
        self.phone = phone
        self.email = email
        self.password = password
        self.activation = activation
        self.state = state
        self.datetime = str(datetime.now())

    def CreateUser(self):
        sql_query = """select * from users where business_username = %s or phone = %s or email = %s"""
        sql_data = [self.business_username, self.phone, self.email]
        cursor.execute(sql_query, sql_data)
        response = cursor.fetchall()
        if response:
            # return negative response -> Account Exists
            return False

        while True:
            self.business_id = f"USER_{self.GenCode(10)}"
            sql_query = """select * from users where business_id = %s"""
            sql_data = [self.business_id]
            cursor.execute(sql_query, sql_data)
            response = cursor.fetchall()
            if not response:
                break
        
        sql_query = """insert into users(business_id, business_username, phone, email, password, activation, state, datetime)
                        values(%s, %s, %s, %s, %s, %s, %s, %s)"""
        sql_data = [self.business_id, self.business_username, self.phone, self.email, sha256_crypt.hash(self.password), str(self.activation), str(self.state), self.datetime]
        for x in sql_data:
            if not x:
                # Return negativer response -> DataFields Empty
                return
            
        cursor.execute(sql_query, sql_data)
        conn.commit()
        # Return positive response -> User Account created successfully
        return True
     
    def DeleteUser(self):
        pass

    def GetUsers(self):
        if self.business_id:
            sql_query = """select * from users where business_id = %s"""
            cursor.execute(sql_query, [self.business_id])
            sql_response = cursor.fetchall()
            return sql_response[0]
        else:
            sql_query = """select * from users"""
            cursor.execute(sql_query)
            sql_response = cursor.fetchall()
            return sql_response

    def AuthUser(self):
        sql_query = """select password, business_id from users where business_username = %s or phone = %s or email = %s"""
        sql_data = [self.business_username, self.phone, self.email]
        cursor.execute(sql_query, sql_data)
        response = cursor.fetchall()
        if response: # User Details Exists
            hash_pass = response[0][0]
            if sha256_crypt.verify(self.password, hash_pass):
                # Return positive response -> Success Auth User
                self.business_id = response[0][1]
                return response[0][1]
        
        # Negative Auth Failed
        return False

    def ToggleAccountState(self, state="True"):
        if state == "False":
            sql_query = """update users set activation = %s where business_id = %s"""
            cursor.execute(sql_query, ["True", self.business_id])
            conn.commit()
            return True
        elif state == "True":
            sql_query = """update users set activation = %s where business_id = %s"""
            cursor.execute(sql_query, ["False", self.business_id])
            conn.commit()
            return True

        return False
    
    def is_valid(self):
        sql_query = """select activation from users where business_id = %s"""
        sql_data = [self.business_id]
        cursor.execute(sql_query, sql_data)
        response = cursor.fetchall()
        if not response: return False
        if response[0][0] == "False": return False
        return True

class Business(Generals):
    def __init__(self, business_id=None, unit_business_id=None, name=None, total_assets="0", no_products="0", no_employees="0", activation="True"):
        self.business_id = business_id
        self.unit_business_id = unit_business_id
        self.name = name
        self.total_assets = total_assets
        self.no_products = no_products
        self.no_employees = no_employees
        self.activation = activation
        self.datetime = str(datetime.now())

    def CreateBusiness(self):
        while True:
            self.unit_business_id = f"UNIT_BIZ_{self.GenCode(7)}"
            sql_query = """select * from unit_business where business_id = %s and unit_business_id = %s"""
            cursor.execute(sql_query, [self.business_id, self.unit_business_id])
            response = cursor.fetchall()
            if not response:
                break
        sql_query = """insert into unit_business (business_id, unit_business_id, unit_name, total_assets, no_products, no_employees, activation, dateetime)
                        values(%s, %s, %s, %s, %s, %s, %s, %s)"""
        sql_data = [self.business_id, self.unit_business_id, self.name,self.total_assets, self.no_products, self.no_employees, self.activation, str(datetime.now())]
        for x in sql_data:
            if not x:
                return False
        cursor.execute(sql_query, sql_data)
        conn.commit()
        return True

    def DeleteBusiness(self):
        sql_query = """delete from unit_business where business_id = %s and unit_business_id = %s"""
        cursor.execute(sql_query, [self.business_id, self.unit_business_id])
        conn.commit()
        # Add deletion of employees linked to the business
        # Add deletion of product linked to the business
        # Add deletion of product_images lined to the business
        return True
    
    def is_valid(self):
        sql_query = """select * from unit_business where business_id = %s and unit_business_id = %s"""
        sql_data = [self.business_id, self.unit_business_id]
        cursor.execute(sql_query, sql_data)
        response = cursor.fetchall()
        if not response:
            return False
        return True

    def GetBusiness(self):
        sql_query = """select * from unit_business where business_id = %s"""
        cursor.execute(sql_query, [self.business_id])
        response = cursor.fetchall()
        if response:
            return response
        return False
         
class Product(Generals):
    def __init__(self, business_id=None, unit_business_id=None, product_id=None, name=None, price=0, quantity=0, img=None, img_extension=None, total_assets=0, rem=0):
        self.business_id = business_id
        self.unit_business_id = unit_business_id
        self.product_id = product_id
        self.name = name
        self.price = price
        self.quantity = quantity
        self.img = img
        self.img_extension = img_extension
        self.total_assets = total_assets
        self.rem = rem
        self.datetime = str(datetime.now())

    def CreateProduct(self):
        # Validate user account wuth UserAccount Class
        while True:
            product_code = "PRODUCT_%s"%(self.GenCode(6))
            sql_query = """select * from products where business_id = %s and unit_business_id = %s and product_id = %s"""
            cursor.execute(sql_query, [self.business_id, self.unit_business_id, product_code])
            valid_product = cursor.fetchall()
            if not valid_product:
                break
        # Start saving the image to local folder
        filename = f"{self.business_id}~~{self.unit_business_id}~~{product_code}.{self.img_extension}"
        self.img.save(os.path.join(images_path_folder, filename))
        # End of saving image

        img_url = f"https://ionextechsolutions.com/businessmanager/images/{filename}"
        sql_query = """insert into products (business_id, unit_business_id, product_id, name, price, img, total_assets, sold, rem, datetime)
                        values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
        sql_data = [self.business_id, self.unit_business_id, product_code, self.name, self.price, img_url, str(int(self.price)*int(self.quantity)), "0", str(self.quantity), self.datetime]
        for x in sql_data:
            if not x:
                # Negative -> DataField Missing
                return False
        cursor.execute(sql_query, sql_data)
        conn.commit()
        return True

    def DeleteProduct(self):
        if self.product_id:
            sql_query = """select img from products where business_id = %s and unit_business_id = %s and product_id = %s"""
            cursor.execute(sql_query, [self.business_id, self.unit_business_id, self.product_id])
            img_response = cursor.fetchall()
            if not img_response:
                # Negative -> Product Not Found
                return False
            img_response = img_response[0][0]
            img_response = img_response.split("/")[5]
            # Deleting image from local folder
            file_path = os.path.join(images_path_folder, img_response)
            if os.path.exists(file_path):
                os.remove(file_path)
                print(f"{file_path} has been deleted.")
            else:
                print(f"The file {file_path} does not exist.")
            # End of deletion
            sql_query = "delete from products where business_id = %s and unit_business_id = %s and product_id = %s"
            cursor.execute(sql_query, [self.business_id, self.unit_business_id, self.product_id])
            conn.commit()
            # Positive -> Product deleted successfully
            return True
        else:
            sql_query = """select img from products where business_id = %s and unit_business_id = %s"""
            cursor.execute(sql_query, [self.business_id, self.unit_business_id])
            product_imgs = cursor.fetchall()
            if product_imgs:
                for img in product_imgs:
                    img = img[0]
                    img = img.split("/")[5]
                    file_path = os.path.join(images_path_folder, img)
                    if os.path.exists(file_path):
                        os.remove(file_path)
                        print(f"{file_path} has been deleted.")
                    else:
                        print(f"The file {file_path} does not exist.")

            sql_query = """delete from products where business_id = %s and unit_business_id = %s"""
            cursor.execute(sql_query, [self.business_id, self.unit_business_id])
            conn.commit()
            return True

    def ModifyProductData(self):
        sql_query = """select total_assets, img from products where business_id = %s and unit_business_id = %s and product_id = %s"""
        cursor.execute(sql_query, [self.business_id, self.unit_business_id, self.product_id])
        raw_response = cursor.fetchall()
        if not raw_response:
            # Negative -> Product Not Found
            return False
        
        product_assets = str(int(self.quantity)*int(self.price))
        if self.img:
            filename = raw_response[0][1].split("/")[5]
            # Remove image for replacenemt
            file_path = os.path.join(images_path_folder, filename)
            if os.path.exists(file_path):
                os.remove(file_path)
                print(f"{file_path} has been deleted.")
            else:
                print(f"The file {file_path} does not exist.")
            
            # Saving new image under same name
            self.img.save(os.path.join(images_path_folder, filename))
            sql_query = """update products set name = %s, total_assets = %s, rem = %s, price = %s where business_id = %s and unit_business_id = %s and product_id = %s"""
            sql_data = [self.name, product_assets, self.quantity, self.price, self.business_id, self.unit_business_id, self.product_id]
            cursor.execute(sql_query, sql_data)
            conn.commit()
            # Positive -> Product Updates made Successfully
            return True
        else:
            sql_query = """update products set name = %s, total_assets = %s, rem = %s, price = %s where business_id = %s and unit_business_id = %s and product_id = %s"""
            sql_data = [self.name, product_assets, self.quantity, self.price, self.business_id, self.unit_business_id, self.product_id]
            cursor.execute(sql_query, sql_data)
            conn.commit()
            return True

    def GetProducts(self):
        print(self.business_id)
        print(self.unit_business_id)
        if len(self.unit_business_id[0]) == 1:
            sql_query = """select * from products where business_id = %s and unit_business_id = %s"""
            cursor.execute(sql_query, [self.business_id, self.unit_business_id])
            response = cursor.fetchall()
            return response
        else:
            sql_query = """select * from products where business_id = %s and unit_business_id = %s"""
            cursor.execute(sql_query, [self.business_id, self.unit_business_id[0]])
            response = cursor.fetchall()
            return response

    def MakeSale(self):
        sql_query = """select * from products where business_id = %s and unit_business_id = %s and product_id = %s"""
        cursor.execute(sql_query, [self.business_id, self.unit_business_id, self.product_id])
        response = cursor.fetchall()
        if not response: return False

        sold_items = int(response[0][7]) + int(self.quantity)
        rem_items = int(response[0][8]) - int(self.quantity)
        if rem_items < 0: return False

        min_total = int(self.quantity) * int(response[0][4])
        sql_query = """update products set datetime = %s, sold = %s, rem = %s where business_id = %s and unit_business_id = %s and product_id = %s"""
        cursor.execute(sql_query, [self.datetime.split(" ")[0], str(sold_items), str(rem_items), self.business_id, self.unit_business_id, self.product_id])
        conn.commit()
        return {
            "product_id": self.product_id,
            "product_name": response[0][3],
            "product_quantity": self.quantity,
            "product_cost": min_total
        }

    def MakesSale_2(self, product_ids=[], quantitys=[], employee_id=None):
        sql_query = """select * from products where business_id = %s and unit_business_id = %s"""
        cursor.execute(sql_query, [self.business_id, self.unit_business_id])
        response = cursor.fetchall()
        if not response: return False

        main_response = ""
        sql_response = response
        for x in range(len(product_ids)):
            for y in sql_response:
                if not product_ids[x] == y[2]: continue
                sold_items = int(y[7]) + int(quantitys[x])
                rem_items = int(y[8]) - int(quantitys[x])
                if rem_items < 0: main_response = main_response + f"Failed sales for product: {y[3]}\n"; continue
                min_total = int(quantitys[x]) * int(y[4])
                total_assets = int(y[6]) + int(min_total)

                # Enter code to notify user when product threshold is reached
                product_threshold = 5
                if rem_items < product_threshold:
                    # Send actual notification including product details -> (Name, Quantity, datetime)
                    # Use SMS Only, Emails for future implementations
                    user = UserAccount(business_id=self.business_id)
                    user_data = user.GetUsers()
                    message = f"Notification for {user_data[1]}\nPRODUCT BELOW THRESHOLD OF {product_threshold}\n\nProduct Name : {y[3]}\nProduct Rem  : {rem_items}\n\nThe following message is  auto-generated please DONT REPLY\nDelivered by IonexTechSolutions"
                    communication = notifications.SMS(user_data[2], message)
                    communication.SendSMS()
                # End of Block

                sql_query = """update products set datetime = %s, total_assets = %s, sold = %s, rem = %s where business_id = %s and unit_business_id = %s and product_id = %s"""
                cursor.execute(sql_query, [str(datetime.now()).split(" ")[0],str(total_assets), str(sold_items), str(rem_items), self.business_id, self.unit_business_id, product_ids[x]])
                conn.commit()

                sql_query = """insert into employee_sales (business_id, unit_business_id, employee_id, product_id, quantity, total_cash, datetime)
                                values(%s, %s, %s, %s, %s, %s, %s)"""
                cursor.execute(sql_query, [self.business_id, self.unit_business_id, employee_id, product_ids[x], str(quantitys[x]), str(min_total), str(datetime.now())])
                conn.commit()

                current_query = {
                    "product_id": product_ids[x],
                    "product_name": y[3],
                    "product_quantity": quantitys[x],
                    "product_cost": int(y[4])*int(quantitys[x])
                }
                r = Receipt(business_id=self.business_id, unit_business_id=self.unit_business_id, query=current_query)
                if not r.CreateReceipt(): main_response = main_response + f"Failed sales for product: {y[3]}\n"; continue
        return main_response
                













        # sold_items = int(response[0][7]) + int(self.quantity)
        # rem_items = int(response[0][8]) - int(self.quantity)
        # if rem_items < 0: return False

        # min_total = int(self.quantity) * int(response[0][4])
        # sql_query = """update products set datetime = %s, sold = %s, rem = %s where business_id = %s and unit_business_id = %s and product_id = %s"""
        # cursor.execute(sql_query, [self.datetime.split(" ")[0], str(sold_items), str(rem_items), self.business_id, self.unit_business_id, self.product_id])
        # conn.commit()
        # return {
        #     "product_id": self.product_id,
        #     "product_name": response[0][3],
        #     "product_quantity": self.quantity,
        #     "product_cost": min_total
        # }

class Employee(Generals):
    def __init__(self, business_id=None, unit_business_id=None, employee_id=None, name=None, sales="0", password=None, activation="False"):
        self.business_id = business_id
        self.unit_business_id = unit_business_id
        self.employee_id = employee_id
        self.name = name
        self.sales = sales
        self.password = password
        self.activation = activation
        self.datetime = str(datetime.now())

    def CreateEmployee(self):
        sql_query = """select * from employees where name = %s"""
        cursor.execute(sql_query, [self.name])
        presence = cursor.fetchall()
        if presence: return False

        while True:
            self.employee_id = f"EMPLOYEE_{self.GenCode(10)}"
            sql_query = """select * from employees where business_id = %s and unit_business_id = %s and employee_id = %s"""
            cursor.execute(sql_query, [self.business_id, self.unit_business_id, self.employee_id])
            response = cursor.fetchall()
            if not response:
                break

        sql_query = """insert into employees (business_id, unit_business_id, employee_id, name, sales, password, activation, datetime)
                        values(%s, %s, %s, %s, %s, %s, %s, %s)"""
        sql_data = [self.business_id, self.unit_business_id, self.employee_id, self.name, self.sales, sha256_crypt.hash(self.password), self.activation, self.datetime]
        count = 0
        for x in sql_data:
            if not x:
                print(f"Failed at ---- {count} Data ------ {sql_data[count]}")
                return False
            count +=1
        cursor.execute(sql_query, sql_data)
        conn.commit()
        return True

    def DeleteEmployee(self):
        if self.employee_id:
            sql_query = """delete from employees where business_id = %s and unit_business_id = %s and employee_id = %s"""
            cursor.execute(sql_query, [self.business_id, self.unit_business_id, self.employee_id])
            conn.commit()
            return True
        else:
            sql_query = """delete from employees where business_id = %s and unit_business_id = %s"""
            cursor.execute(sql_query, [self.business_id, self.unit_business_id])
            conn.commit()
            return True
        
    def ModifyEmployee(self):
        if self.password:
            sql_query = """update employees set name = %s, password = %s where business_id = %s and unit_business_id = %s and employee_id = %s"""
            sql_data = [self.name, sha256_crypt.hash(self.password), self.business_id, self.unit_business_id, self.employee_id]
            cursor.execute(sql_query, sql_data)
            conn.commit()
            return True
        else:
            sql_query = """update employees set name = %s where business_id = %s and unit_business_id = %s and employee_id = %s"""
            sql_data = [self.name, self.business_id, self.unit_business_id, self.employee_id]
            cursor.execute(sql_query, sql_data)
            conn.commit()
            return True

    def AuthEmployee(self):
        sql_query = """select * from employees where name = %s"""
        sql_data = [self.name]
        cursor.execute(sql_query, sql_data)
        response = cursor.fetchall()
        if not response:
            return False
        if sha256_crypt.verify(self.password, response[0][5]):
            self.business_id = response[0][0]
            self.unit_business_id = response[0][1],
            self.employee_id = response[0][2]
            return True
        return False

    def MakeSales(self):
        pass

    def GetEmployees(self):
        sql_query = """select * from employees where business_id = %s and unit_business_id = %s"""
        cursor.execute(sql_query, (self.business_id, self.unit_business_id))
        response = cursor.fetchall()
        if response:
            return response
        return False

    def is_present(self):
        sql_query = """select * from employees where business_id = %s and unit_business_id = %s and employee_id = %s"""
        sql_data = [self.business_id, self.unit_business_id, self.employee_id]
        cursor.execute(sql_query, sql_data)
        response = cursor.fetchall()
        if not response:
            return False
        return True
    
class Receipt(Generals):
    def __init__(self, business_id=None, unit_business_id=None, receipt_id=None, query=None, state="Pending"):
        self.business_id = business_id
        self.unit_business_id = unit_business_id
        self.receipt_id = receipt_id
        self.query = query
        self.state = state
        self.datetime = str(datetime.now())

    def CreateReceipt(self):
        sql_query = """select * from receipts where business_id = %s and unit_business_id = %s and state = %s"""
        cursor.execute(sql_query, [self.business_id, self.unit_business_id, "Pending"])
        response = cursor.fetchall()
        if response:
            new_query = json.loads(response[0][3]).append(self.query)
            sql_query = """update receipts set query = %s where business_id = %s and unit_business_id = %s and receipt_id = %s"""
            cursor.execute(sql_query, [json.dumps(new_query), self.business_id, self.unit_business_id, self.receipt_id])
            conn.commit()
            return True
        else:
            while True:
                self.receipt_id = self.GenCode(10)
                sql_query = """select * from receipts where business_id = %s and unit_business_id = %s and receipt_id = %s"""
                sql_data = [self.business_id, self.unit_business_id, self.receipt_id]
                cursor.execute(sql_query, sql_data)
                response = cursor.fetchall()
                if not response:
                    break
            
            print(self.query)
            sql_query = """insert into receipts (business_id, unit_business_id, receipt_id, query, state, datetime)
                            values(%s, %s, %s, %s, %s, %s)"""
            sql_data = [self.business_id, self.unit_business_id, self.receipt_id, json.dumps([self.query]), self.state, self.datetime]
            print(sql_data)
            for x in sql_data:
                if not x: return False
            cursor.execute(sql_query, sql_data)
            conn.commit()
            return True

    def ActivateReceipt(self):
        sql_query = """update receipts set state = %s where business_id = %s and unit_business_id = %s and state = %s"""
        cursor.execute(sql_query, ["False", self.business_id, self.unit_business_id, "Pending"])
        conn.commit()
        return True
    
    def GetReceipt(self):
        sql_query = """select * from receipts where business_id = %s and unit_business_id = %s and state = %s"""
        cursor.execute(sql_query, [self.business_id, self.unit_business_id, "False"])
        response = cursor.fetchall()
        if not response: return False
        sql_query = """update receipts set state = %s where business_id = %s and unit_business_id = %s and receipt_id = %s"""
        cursor.execute(sql_query, ["True", self.business_id, self.unit_business_id, response[0][2]])
        conn.commit()
        return response

class Files(Generals):
    def __init__(self):
        pass
