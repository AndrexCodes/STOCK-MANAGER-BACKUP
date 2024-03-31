from login import login_credentials
from datetime import datetime
import base64
import requests

# 254792363591

class lipa_mpeas:
    def __init__(self):
        self.business_code = "174379"
        self.pass_key = "bfb279f9aa9bdbcf158e97dd71a467cd2e0c893059b10f78e6b72ada1ed2c919"
        self.timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        self.stk_url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
        self.headers = {
            "Authorization": "Bearer %s" %(login_credentials().getAuthToken())
        }
        self.data = {
            "BusinessShortCode": self.business_code,
            "Password": self.gen_online_pass(),
            "Timestamp": self.timestamp,
            "TransactionType": "CustomerPayBillOnline",
            "Amount": 1,
            "PartyA": 254795359098,
            "PartyB": self.business_code,
            "PhoneNumber": 254795359098,
            "CallBackURL": "https://andrewmacharia.loca.lt/stk_callback",
            "AccountReference": "HUSTLE POINT APP",
            "TransactionDesc": "Testing stk push"
        }

    def gen_online_pass(self):
        self.online_pass = base64.b64encode((self.business_code+self.pass_key+self.timestamp).encode()).decode('utf-8')
        return self.online_pass


# x = lipa_mpeas()
# mpesa_response = requests.post(x.stk_url, json=x.data, headers=x.headers)
# print(mpesa_response.text)


    
#### Helpful mpesa tutorial "https://nyagilo.medium.com/mpesa-stk-push-integration-step-by-step-guide-to-integrating-lipa-na-mpesa-online-in-python-be68d30ea2f1"
#### Ngrok domain name "excited-ultimately-pup.ngrok-free.app"
#### CANCEL CART REQUEST IN 10MINUTES #####
#### MPESA VALID RESPONSE ####

mpesa_response = {    
        "Body": {        
            "stkCallback": {            
                "MerchantRequestID": "29115-34620561-1",            
                "CheckoutRequestID": "ws_CO_191220191020363925",            
                "ResultCode": 0,            
                "ResultDesc": "The service request is processed successfully.",            
                "CallbackMetadata": {                
                    "Item": [{                        
                    "Name": "Amount",                        
                    "Value": 1.00                    
                    },                    
                    {                        
                    "Name": "MpesaReceiptNumber",                        
                    "Value": "NLJ7RT61SV"                    
                    },                    
                    {                        
                    "Name": "TransactionDate",                        
                    "Value": 20191219102115                    
                    },                    
                    {                        
                    "Name": "PhoneNumber",                        
                    "Value": 254708374149                    
                    }]            
                }        
            }    
        }
        }

ResultCode = mpesa_response["Body"]["stkCallback"]["ResultCode"]
MerchantRequestID = mpesa_response["Body"]["stkCallback"]["MerchantRequestID"]
CheckoutRequestID = mpesa_response["Body"]["stkCallback"]["CheckoutRequestID"]
ReceiptNo=mpesa_response['Body']['stkCallback']['CallbackMetadata']['Item'][1]["Value"]
PhoneNumber = mpesa_response['Body']['stkCallback']['CallbackMetadata']['Item'][-1]["Value"]
Amount = mpesa_response['Body']['stkCallback']['CallbackMetadata']['Item'][0]["Value"]
TimeStamp = mpesa_response['Body']['stkCallback']['CallbackMetadata']['Item'][-2]["Value"]

mpesa_response = {
        "Body": {        
            "stkCallback": {            
                "MerchantRequestID": "29115-34620561-1",            
                "CheckoutRequestID": "ws_CO_191220191020363925",            
                "ResultCode": 0,            
                "ResultDesc": "The service request is processed successfully.",            
                "CallbackMetadata": {                
                    "Item": [{                        
                    "Name": "Amount",                        
                    "Value": 1.00                    
                    },                    
                    {                        
                    "Name": "MpesaReceiptNumber",                        
                    "Value": "NLJ7RT61SV"                    
                    },                    
                    {                        
                    "Name": "TransactionDate",                        
                    "Value": 20191219102115                    
                    },                    
                    {                        
                    "Name": "PhoneNumber",                        
                    "Value": 254708374149                    
                    }]            
                }        
            }    
        }
        }

                