import requests
import json
from requests.auth import HTTPBasicAuth
from datetime import datetime
import base64

class login_credentials:
    def __init__(self):
        self.app_key = "9fPs2Ma7S6GZHEyAYfGfuLOaDeIWIAgF"
        # DxBnBiLVM3pGs382a4r6069P32NUCJPB
        self.app_secret = "rYmoWnUNJjAu35Uw"
        # A6HA3sWs7qa5X6gG
        self.getAuthToken_url = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"
    def getAuthToken(self):
        self.auth_response = requests.get(self.getAuthToken_url, auth=HTTPBasicAuth(self.app_key, self.app_secret))
        self.auth_token = json.loads(self.auth_response.text)
        self.auth_token = self.auth_token["access_token"]
        return self.auth_token
    
# print(login_credentials().getAuthToken())