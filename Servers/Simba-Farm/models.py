from passlib.hash import sha256_crypt
from datetime import datetime
from random import randint
import os
import json

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
            pass

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
        sql_data = [self.business_id, self.business_username, self.phone, self.email, sha256_crypt.genhash(self.password), str(self.activation), str(self.state), self.datetime]
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

    def AuthUser(self):
        sql_query = """select password, business_id from users where business_username = %s or phone = %s or email = %s"""
        sql_data = [self.business_username, self.phone, self.email]
        cursor.execute(sql_query, sql_data)
        response = cursor.fetchall()
        if response: # User Details Exists
            hash_pass = response[0][0]
            if sha256_crypt.verify(self.password, hash_pass):
                # Return positive response -> Success Auth User
                return response[0][1]
        
        # Negative Auth Failed
        return False

    def UserAccountValidation(self):
        sql_query = """select * from users where business_id = %s and state = %s"""
        sql_data = [self.business_id, "True"]
        cursor.execute(sql_query, sql_data)
        response = cursor.fetchall()
        if response:
            return True
        return False

    def ToggleAccountState(self, state="True"):
        if state == "False:":
            sql_query = """update users set activation = %s where business_id = %s"""
            cursor.execute(sql_query, ["True", self.business_id])
            conn.commit()
            return True
        else:
            sql_query = """update users set activation = %s where business_id = %s"""
            cursor.execute(sql_query, ["False", self.business_id])
            conn.commit()
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

    def GetBusiness(self):
        sql_query = """select * from unit_business where business_id = %s"""
        cursor.execute(sql_query, [self.business_id])
        response = cursor.fetchall()
        if response:
            return response
        return False
        
class Product(Generals):
    def __init__(self, business_id=None, unit_business_id=None, product_id=None, name=None, price=None, quantity=0, img=None, img_extension=None, total_assets=0, rem=0):
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
        return True

    def DeleteProduct(self):
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

    def ModifyProductData(self):
        sql_query = """select total_assets, img from products where business_id = %s and unit_business_id = %s and product_id = %s"""
        cursor.execute(sql_query, [self.business_id, self.unit_business_id, self.product_id])
        raw_response = cursor.fetchall()
        if not raw_response:
            # Negative -> Product Not Found
            return False
        
        product_assets = str(int(self.quantity)*int(self.price))
        if not self.img:
            # Negative -> Product img missing
            return False
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

    def GetProducts(self):
        pass

    def MakeSale(self):
        sql_query = """select * from products where business_id = %s and unit_business_id = %s and product_id = %s"""
        cursor.execute(sql_query, [self.business_id, self.unit_business_id, self.product_id])
        response = cursor.fetchall()
        if not response: return False

        sold_items = int(response[0][7]) + int(self.quantity)
        rem_items = int(response[0][8]) - int(self.quantity)
        if rem_items < 0: return False

        min_total = int(self.quantity) * int(response[0][4])
        print("sold_items === %s"%(sold_items))
        print("rem_items === %s"%(rem_items))
        print("sub_total === %s"%(min_total))
        sql_query = """update products set datetime = %s sold = %s, rem = %s where business_id = %s and unit_business_id = %s and product_id = %s"""
        cursor.execute(sql_query, [self.datetime.split(" ")[0], str(sold_items), str(rem_items), self.business_id, self.unit_business_id, self.product_id])
        conn.commit()
        return {
            "product_id": self.product_id,
            "product_name": response[0][3],
            "product_quantity": self.quantity,
            "product_cost": min_total
        }

class Employee(Generals):
    def __init__(self, business_id=None, unit_business_id=None, employee_id=None, name=None, sales="0", password=None, activation=False):
        self.business_id = business_id
        self.unit_business_id = unit_business_id
        self.employee_id = employee_id
        self.name = name
        self.sales = sales
        self.password = password
        self.activation = activation
        self.datetime = str(datetime.now())

    def CreateEmployee(self):
        # Validate UserAcconut
        while True:
            self.employee_id = f"EMPLOYEE_{self.GenCode(10)}"
            sql_query = """select * from employees where business_id = %s and unit_business_id = %s and employee_id = %s"""
            cursor.execute(sql_query, [self.business_id, self.unit_business_id], self.employee_id)
            response = cursor.fetchall()
            if not response:
                break

        sql_query = """insert into employees (business_id, unit_business_id, employee_id, name, sales, password, activation, datetime)
                        values(%s, %s, %s, %s, %s, %s, %s, %s)"""
        sql_data = [self.business_id, self.unit_business_id, self.employee_id, self.name, self.sales, sha256_crypt.hash(self.password), self.activation, self.datetime]
        for x in sql_data:
            if not x:
                return False
        return True

    def DeleteEmployee(self):
        sql_query = """delete from employees where business_id = %s and unit_business_id = %s and employee_id = %s"""
        cursor.execute(sql_query, [self.business_id, self.unit_business_id, self.employee_id])
        conn.commit()
        return True

    def ModifyEmployee(self, state=False):
        if state:
            sql_query = """update employees set name = %s, password = %s where business_id = %s and unit_business_id = %s and employee_id = %s"""
            sql_data = [self.name, sha256_crypt.hash(self.password), self.business_id, self.unit_business_id, self.employee_id]
            cursor.execute(sql_query, sql_data)
        else:
            sql_query = """update employees set name = %swhere business_id = %s and unit_business_id = %s and employee_id = %s"""
            sql_data = [self.name, self.business_id, self.unit_business_id, self.employee_id]
            cursor.execute(sql_query, sql_data)
        conn.commit()
        return True

    def AuthEmployee(self):
        sql_query = """select password, employee_id, business_id, unit_business_id from employees where name = %s"""
        sql_data = [self.name]
        cursor.execute(sql_query, sql_data)
        response = cursor.fetchall()
        if not response:
            return False
        if sha256_crypt.verify(self.password, response[0][0]):
            return {
                "business_id": response[0][2],
                "unit_business_id": response[0][3],
                "employee_id": response[0][1]
            }
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
        sql_query = """select * from employees where name = %s"""
        sql_data = [self.name]
        cursor.execute(sql_query, sql_data)
        response = cursor.fetchall()
        if not response:
            return False
        return True
    
    def is_valid(self):
        sql_query = """select * from employees where name = %s and activation = %s"""
        sql_data = [self.name, "True"]
        cursor.execute(sql_query, sql_data)
        response = cursor.fetchall()
        if not response:
            return False
        return True
    
    def is_valid(self):
        sql_query = """select * from employees where employee_id = %s and activation = %s"""
        sql_data = [self.employee_id, "True"]
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
        while True:
            self.receipt_id = self.GenCode(10)
            sql_query = """select * from receipts where business_id = %s and unit_business_id = %s and receipt_id = %s"""
            sql_data = [self.business_id, self.unit_business_id, self.receipt_id]
            cursor.execute(sql_query, sql_data)
            response = cursor.fetchall()
            if not response:
                break

        sql_query = """insert into receipts (business_id, unit_business_id, receipt_id, query, state, datetime)
                                    values(%s, %s, %s, %s, %s, %s)"""
        sql_data = [self.business_id, self.unit_business_id, self.receipt_id, json.dumps(self.query), self.state, self.datetime]
        for x in sql_data:
            if not x: return False
        cursor.execute(sql_query, sql_data)
        conn.commit()
        return True
    
    def AppendProduct(self, new_query=None):
        pass

    def ActivateReceipt(self):
        pass