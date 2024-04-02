# SMS Notification class
import requests
import json

def SendDailySales():
    # Send daily sales as per business to registered customers phone number
    # Iteration -> users -> unit_businesses -> receipts
    # Get daily sales by unwrapping receipts
    # SMS Details -> Business Name, Product_name, Quantity, Unit_Price, Total_Cost
    pass

class SMS:
    def __init__(self, number, message):
        self.base_url = 'https://sms.textsms.co.ke/api/services/sendsms'
        self.payload = {
            "apikey":"5f7157aa5e206f7f5402ffd5abc79c95",
            "partnerID":"9064",
            "message":message,
            "shortcode":"TextSMS",
            "mobile":number
        }

    def SendSMS(self):
        formated_number = self.CorrectNumber(self.payload["mobile"])
        if not formated_number: return False
        self.payload["mobile"] = formated_number
        self.response = requests.post(self.base_url, data=self.payload)
        self.response = json.loads(self.response.text)
        print(self.response)
        # status_code = self.response
        return True

    def CorrectNumber(self, number):
        if not len(number) == 12: return False
        return number
    
# x = SMS("254795359098", "Testing Message")
# x.SendSMS()


