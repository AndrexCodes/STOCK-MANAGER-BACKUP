from escpos.printer import Serial
from PIL import Image
import qrcode
from datetime import datetime
import json

serial_port = "COM3"
with open("config.json", "r+") as json_file:
        data = json_file.read()
        data = json.loads(data)
        serial_port = data["printer_com"]
        print(serial_port)
        
printer = Serial(serial_port, baudrate=9600)
printer.set(align='left')
printer.close()

print("Printer is configured successfully")


def receipt_print(data):
    printer.open()
    try:
        printer.set(align='center')
        printer.image("simba_app.png")
        printer.text("\n\n")
        for x in data:
            print(f"Printing lines : {x}")
            printer.text("%s\n\n"%(x))
            if x == 4:
                for _ in range(5):
                    printer.text("\n")
                printer.device.write("\x1B\x45\x01")
            if x == 5:
                printer.device.write("\x1B\x45\x00")
        printer.image("example_qrcode.png")
        printer.text("\n*** Thank you for shopping, come again ***")
        for x in range(7):
            printer.text("\n")
        printer.cut()
        printer.close()
        return True
    except:
        print("Error Occured")
        return False

def correct_print(data): # array [receipt_id, products(id,name, quantity, total), receipt_date, business_name]
    max_length = 48
    curr_datetime = datetime.now()
    receipt = [] # logo
    receipt.append("SIMBA FARM MACHINERY") # name
    receipt.append("P.O. BOX : 119-10200")
    receipt.append("MURANGA")
    receipt.append("Phone: 0706893979") # tel num
    receipt.append("Email: simba361@gmail.com") # email
    receipt.append("PIN: PO52025787L") 
    receipt.append("DATE: %s   TIME: %sHRS"%(curr_datetime.strftime('%Y-%m-%d'), curr_datetime.strftime('%H:%M'))) # date - time
    receipt.append("ITEM%sQTY%sPRICE%sAMOUNT"%('_'*19, '_'*2, '_'*3)) # item - qty - price - price - amount
    # receipt.append(len("ITEM%sQTY%sPRICE%sAMOUNT"%('_'*19, '_'*2, '_'*3)))
    # receipt.append("{:<23} {:<3} {:<7} {:<7}".format("Item", "qty", "price", "amount")) # item - qty - price - price - amount

    total_amount = 0
    for x in data[1]:
        item = x["product_name"]
        qty = x["product_quantity"]
        amount = x["product_cost"]
        total_amount += int(x["product_cost"])
        price = amount / qty
        unit_product = "{:<23} {:<3} {:<7} {:<7}".format(item, qty, price, amount)

        receipt.append(str(unit_product))

    receipt.append("TOTAL: Ksh %s"%(total_amount)) # total - amount
    receipt.append("Developed by IonexTech \n 0795359098")
    return receipt

def correct_print_2(data):
    for x in data[1]:
        # set printer to left
        unit_product = ""
        product_name = x["product_name"]
        product_qty = x["product_quantity"]
        product_amount = x["product_cost"]
        product_price = float(product_amount/product_qty)

        for y in range(48):
            if y == 0:
                unit_product = unit_product + product_name
            if y == 26:
                unit_product = unit_product + str(int(product_qty))
            if y == 28:
                unit_product = unit_product + str(float(product_price))
            if y == 38:
                unit_product = unit_product + str(float(product_amount))
            unit_product = unit_product + " "
